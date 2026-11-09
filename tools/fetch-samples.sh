#!/bin/sh
# Fetch the sample files that are listed in samples.manifest.json but not committed
# (licence does not allow redistribution, or the file is too big).
#
#   sh tools/fetch-samples.sh                 fetch everything
#   sh tools/fetch-samples.sh vsrg/osu-mania  fetch only the entries whose format path starts with this prefix
#
# Files land in samples-local/<format path>/<target> (gitignored). Idempotent: a file whose size and
# sha256 already match is left alone; a file that does not match is downloaded again. Needs POSIX sh,
# curl, sha256sum, awk. Exit status 1 if any entry failed (download error or hash/size mismatch).
set -u

root=$(cd "$(dirname "$0")/.." && pwd)
manifest=${SAMPLES_MANIFEST:-$root/samples.manifest.json}
dest=${SAMPLES_DIR:-$root/samples-local}
prefix=${1:-}

for tool in curl sha256sum awk; do
  command -v "$tool" >/dev/null 2>&1 || { echo "fetch-samples: '$tool' not found" >&2; exit 2; }
done
[ -f "$manifest" ] || { echo "fetch-samples: $manifest not found" >&2; exit 2; }

tab=$(printf '\t')
tmp=$(mktemp -d "${TMPDIR:-/tmp}/fetch-samples.XXXXXX") || exit 2
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

# The manifest is written one key per line (json.dumps(indent=2)); no JSON parser needed.
awk '
  function val(line,   v) { v = line; sub(/^[^:]*:[ \t]*/, "", v); sub(/,[ \t]*$/, "", v); gsub(/^"|"$/, "", v); return v }
  /"format":/ { f = val($0) }
  /"target":/ { t = val($0) }
  /"url":/    { u = val($0) }
  /"sha256":/ { h = val($0) }
  /"size":/   { s = val($0) }
  /^[ \t]*}/ && f != "" { printf "%s\t%s\t%s\t%s\t%s\n", f, t, u, h, s; f = t = u = h = s = "" }
' "$manifest" >"$tmp/list"

total=0 ok=0 skipped=0 failed=0
while IFS="$tab" read -r format target url sha size; do
  case $format in "$prefix"*) ;; *) continue ;; esac
  total=$((total + 1))
  case $format$target in *..*|*"$tab"*) echo "BAD   $format/$target (unsafe path)"; failed=$((failed + 1)); continue ;; esac
  case $target in */*) echo "BAD   $format/$target (target has a slash)"; failed=$((failed + 1)); continue ;; esac

  dir=$dest/$format
  file=$dir/$target
  if [ -f "$file" ]; then
    have=$(sha256sum "$file" | awk '{print $1}')
    if [ "$have" = "$sha" ]; then
      echo "SKIP  $format/$target"
      skipped=$((skipped + 1))
      continue
    fi
  fi

  mkdir -p "$dir" || { failed=$((failed + 1)); continue; }
  part=$tmp/download
  rm -f "$part"
  if ! curl -fsSL --retry 3 --retry-delay 2 --connect-timeout 20 --max-time 600 \
       -A "vsrg-format-docs-fetch/1.0" -o "$part" "$url"; then
    echo "FAIL  $format/$target (download error: $url)"
    failed=$((failed + 1))
    continue
  fi
  got_sha=$(sha256sum "$part" | awk '{print $1}')
  got_size=$(wc -c <"$part" | awk '{print $1}')
  if [ "$got_sha" != "$sha" ] || [ "$got_size" != "$size" ]; then
    echo "FAIL  $format/$target (expected $sha $size bytes, got $got_sha $got_size bytes)"
    failed=$((failed + 1))
    continue
  fi
  mv "$part" "$file"
  echo "OK    $format/$target"
  ok=$((ok + 1))
done <"$tmp/list"

echo "fetch-samples: $total entries, $ok downloaded, $skipped already present, $failed failed"
[ "$failed" -eq 0 ]
