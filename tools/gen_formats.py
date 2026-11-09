#!/usr/bin/env python3
"""Regenerates the tables of FORMATS.md (between the GENERATED markers) from three sources:

- README.md: the format index (extension, name, game, "Read by ROX");
- SAMPLES-STATUS.md: real and synthetic chart counts per format, and why a format has fewer than 5 real ones;
- a decode report of Prism (TSV): `cargo run --release -p game-core --example corpus_decode -- <this repo> > decode.tsv`
  in the Prism repository (crates/core/examples/corpus_decode.rs).

Usage: python3 tools/gen_formats.py decode.tsv
Everything outside the markers (the introduction, the known reader gaps) is written by hand and kept as is.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- BEGIN GENERATED (tools/gen_formats.py) -->", "<!-- END GENERATED -->"

# What the game does with a format beyond "plays what ROX decodes": the library scan's own rules (Prism's crates/library/src/scan.rs).
PRISM_NOTES = {
    "vsrg/friday-night-funkin/vslice-chart-json": "Plays (needs its `-metadata.json` beside it)",
    "vsrg/friday-night-funkin/vslice-metadata-json": "Part of a V-Slice chart",
    "vsrg/stepmania/edit": "Plays with the song it names",
    "vsrg/clone-hero/ini": "Metadata of a `.chart`/`.mid`",
    "vsrg/o2jam/ojm": "Keysounds of an `.ojn`",
}
# FNF engine charts ROX decodes but the scan never lists (it lists V-Slice, `.fnfc`, Codename and Ludum Dare charts only).
FNF_UNLISTED = {"legacy-json", "psych-json", "kade-json", "troll-json", "maru-json", "nmv-json", "fps-plus-json"}
# Files that come with a chart and are no chart themselves: their samples are not decoded.
COMPANIONS = {"vsrg/clone-hero/ini", "vsrg/friday-night-funkin/vslice-metadata-json", "vsrg/o2jam/ojm"}

# Why ROX did not decode a sample, from its error. All but `error` are files that are no chart of this format: `error` is a file ROX
# should read and does not. A `not a chart file` (a README, a fuzz seed, a MIDI not named notes.mid) is not counted at all.
REASONS = [
    ("not a chart file", re.compile(r"unsupported format: \w+$|is a MIDI file, not a Clone Hero chart")),
    ("other mode", re.compile(r"Not a mania beatmap|Malody mode|pump-couple")),
    ("needs its companion file", re.compile(r"metadata file|song of this edit")),
    ("broken file", re.compile(r"truncated|runs past the end|size of the file is not|is not after the BPM table|mapping values are not allowed")),
    ("no note", re.compile(r"no playable (note|object)|aucune note", re.I)),
    ("events or metadata, not a chart", re.compile(r"FNF parse error: missing field `song`")),
]
LAYOUT = re.compile(r"Unsupported layout: (\d+)K")


def esc(text):
    return text.replace("|", "\\|")


def read_index():
    index = {}
    pattern = re.compile(r"\| \[`([^`]*)`\]\([^)]*/\) (.*?) \| (.*?) \| (vsrg|others) \| (\w+) \| (.*?) \| \[`([^`]+)`\]")
    for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            index[match.group(7)] = {"ext": match.group(1), "name": match.group(2), "game": match.group(3), "rox": match.group(6)}
    return index


def read_status():
    status = {}
    pattern = re.compile(r"\| \[`([^`]+)`\]\([^)]*\) .*? \| (\d+) \| (\d+) \| (.*) \|$")
    for line in (ROOT / "SAMPLES-STATUS.md").read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            status[match.group(1)] = (int(match.group(2)), int(match.group(3)), match.group(4))
    return status


def reason_of(message):
    for name, pattern in REASONS:
        if pattern.search(message):
            return name
    return "error"


def read_decode(path):
    """Per format folder: the files ROX decoded, the files tried, why each other file was not decoded, and the key counts of decoded
    charts the game has no layout for."""
    decoded, tried, errors, no_layout = defaultdict(set), defaultdict(set), defaultdict(dict), defaultdict(set)
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        match = re.search(r"/((?:vsrg|others)/[^/]+/[^/]+)/samples/", fields[1])
        if not match:
            continue
        folder = match.group(1)
        tried[folder].add(fields[1])
        # `OK <path> <variant> <name> <keys> <notes> <fingerprint> <plays>`: a chart counts as decoded when ROX found a note in it.
        if fields[0] == "OK" and len(fields) >= 8 and fields[5] != "0":
            decoded[folder].add(fields[1])
            layout = LAYOUT.search(fields[-1])
            if layout:
                no_layout[folder].add(int(layout.group(1)))
        elif fields[0] == "OK":
            errors[folder].setdefault(fields[1], "no note")
        else:
            errors[folder].setdefault(fields[1], reason_of(fields[-1]))
    why = defaultdict(lambda: defaultdict(int))
    for folder, files in errors.items():
        for file, reason in files.items():
            if file in decoded[folder]:
                continue
            if reason == "not a chart file":
                tried[folder].discard(file)
            else:
                why[folder][reason] += 1
    return decoded, tried, why, no_layout


def rox_columns(path, rox, decoded):
    if rox.startswith("Yes"):
        read, write = "Yes", "Yes"
    elif rox.startswith("Decode only"):
        read, write = "Yes" + rox[len("Decode only"):], "No"
    elif rox.startswith("Partial"):
        read, write = rox, "No"
    else:
        read, write = "No", "No"
    if read == "No" and decoded:
        # A format of a shared extension another decoder reads (FNF engines through the FNF codec, a SUS dialect).
        read = "Partial (read by the FNF codec)" if "friday-night-funkin" in path else "Partial (read as Project SEKAI SUS)" if path.endswith("sus") else "Partial"
    return read, write


def prism(path, decoded, no_layout):
    if path in PRISM_NOTES:
        return PRISM_NOTES[path]
    if not decoded:
        return "No"
    if path.startswith("vsrg/friday-night-funkin/") and path.rsplit("/", 1)[1] in FNF_UNLISTED:
        return "Not listed (the scan lists V-Slice, Codename and Ludum Dare only)"
    if path.startswith("others/") and not path.endswith("/sus"):
        return "No"
    played = "Plays (12K, as a Project SEKAI chart)" if path == "others/chunithm/sus" else "Plays"
    if no_layout:
        played += " except " + ", ".join(f"{keys}K" for keys in sorted(no_layout))
    return played


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    index, status = read_index(), read_status()
    decoded, tried, why, no_layout = read_decode(sys.argv[1])
    missing = sorted(set(index) ^ set(status))
    if missing:
        sys.exit(f"README.md and SAMPLES-STATUS.md list different formats: {missing}")

    rows, totals = {"vsrg": [], "others": []}, defaultdict(int)
    for path in sorted(index):
        entry, (real, synthetic, reason) = index[path], status[path]
        category = path.split("/")[0]
        ok, files = len(decoded[path]), len(tried[path])
        read, write = rox_columns(path, entry["rox"], ok)
        played = prism(path, ok, no_layout[path])
        corpus = f"{ok}/{files}" if files and (read != "No" or ok) and path not in COMPANIONS else "—"
        not_read = ", ".join(f"{count} {name}" for name, count in sorted(why[path].items(), key=lambda item: item[0] != "error")) if corpus != "—" else ""
        if category == "vsrg" and corpus != "—":
            totals["errors"] += why[path].get("error", 0)
        gaps = []
        if real < 5:
            gaps.append(esc(reason.split("; ")[0]))
        if category == "vsrg" and read == "No" and path not in PRISM_NOTES:
            gaps.append("no ROX reader")
        rows[category].append(
            f"| [`{esc(entry['ext'])}`]({path}/) {esc(entry['name'])} | {esc(entry['game'])} | {real} | {synthetic} | {read} | {write} | {corpus} | {not_read} | {played} | {'; '.join(gaps)} |"
        )
        totals["formats"] += 1
        totals["vsrg"] += category == "vsrg"
        totals["rox_read"] += category == "vsrg" and read != "No"
        totals["rox_write"] += write == "Yes"
        totals["plays"] += played.startswith("Plays")
        totals["five"] += real >= 5
        totals["few"] += 0 < real < 5
        totals["none"] += real == 0

    header = "| Format | Game | Real charts | Synthetic | ROX read | ROX write | ROX decoded | Not decoded, why | In Prism | What is missing |\n|---|---|---:|---:|---|---|---:|---|---|---|"
    generated = "\n".join([
        BEGIN,
        "",
        f"{totals['formats']} formats ({totals['vsrg']} VSRG). ROX reads {totals['rox_read']} VSRG formats, writes {totals['rox_write']}; Prism plays {totals['plays']}. "
        f"Real charts: at least 5 for {totals['five']} formats, 1 to 4 for {totals['few']}, none for {totals['none']}. "
        f"ROX errors on VSRG samples: {totals['errors']}.",
        "",
        "\"ROX decoded\": charts where ROX found at least one note. \"Not decoded, why\": only `error` is a ROX failure; the other "
        "reasons are files that are no chart of this format (another mode, a missing companion file, a broken or empty file, events or "
        "metadata). \"In Prism\" lists the key counts the game has no layout for.",
        "",
        "## VSRG",
        "",
        header,
        *rows["vsrg"],
        "",
        "## Other games",
        "",
        "Only CHUNITHM `.sus` plays in Prism (as a Project SEKAI chart).",
        "",
        header,
        *rows["others"],
        "",
        END,
    ])
    target = ROOT / "FORMATS.md"
    text = target.read_text(encoding="utf-8")
    start, stop = text.index(BEGIN), text.index(END) + len(END)
    target.write_text(text[:start] + generated + text[stop:], encoding="utf-8")
    print(f"FORMATS.md: {totals['formats']} formats written")


if __name__ == "__main__":
    main()
