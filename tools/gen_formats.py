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

# What the game does with a format beyond "decodes into a playable chart": the library scan's own rules (Prism's
# crates/library/src/scan.rs). A format absent here is "Plays" when the decoder reads its samples, else "No".
PRISM_NOTES = {
    "vsrg/friday-night-funkin/vslice-chart-json": "Plays (needs its `-metadata.json` beside it)",
    "vsrg/friday-night-funkin/vslice-metadata-json": "Part of a V-Slice chart",
    "vsrg/stepmania/edit": "Plays with the song it names",
    "vsrg/clone-hero/ini": "Metadata of a `.chart`/`.mid`",
    "vsrg/o2jam/ojm": "Keysounds of an `.ojn`",
    "others/chunithm/sus": "Plays (12K, as a Project SEKAI chart)",
}
# FNF engine charts ROX decodes but the scan never lists (it lists V-Slice charts and `.fnfc` only).
FNF_UNLISTED = {"legacy-json", "psych-json", "kade-json", "troll-json", "maru-json", "nmv-json", "codename-json", "fps-plus-json", "ludum-dare-png"}
NOT_A_GAP = ("Part of", "Metadata", "Keysounds")


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


def read_decode(path):
    decoded, tried = defaultdict(set), defaultdict(set)
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        match = re.search(r"/((?:vsrg|others)/[^/]+/[^/]+)/samples/", fields[1])
        if not match:
            continue
        tried[match.group(1)].add(fields[1])
        if fields[0] == "OK":
            decoded[match.group(1)].add(fields[1])
    return decoded, tried


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


def prism(path, decoded, reason):
    if path in PRISM_NOTES:
        return PRISM_NOTES[path]
    if path.startswith("others/"):
        return "No"
    if path.startswith("vsrg/friday-night-funkin/") and path.rsplit("/", 1)[1] in FNF_UNLISTED:
        return "Decoded, not listed (the scan lists V-Slice only)" if decoded else "No"
    return "Plays" if decoded else "No"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    index, status = read_index(), read_status()
    decoded, tried = read_decode(sys.argv[1])
    missing = sorted(set(index) ^ set(status))
    if missing:
        sys.exit(f"README.md and SAMPLES-STATUS.md list different formats: {missing}")

    rows, totals = {"vsrg": [], "others": []}, defaultdict(int)
    for path in sorted(index):
        entry, (real, synthetic, reason) = index[path], status[path]
        ok, files = len(decoded[path]), len(tried[path])
        read, write = rox_columns(path, entry["rox"], ok)
        played = prism(path, ok, reason)
        corpus = f"{ok}/{files}" if files and (read != "No" or ok) else "—"
        gaps = []
        if real < 5:
            gaps.append(esc(reason.split("; ")[0]))
        category = path.split("/")[0]
        if category == "vsrg" and read == "No" and not played.startswith(NOT_A_GAP):
            gaps.append("no ROX reader")
        rows[category].append(
            f"| [`{esc(entry['ext'])}`]({path}/) {esc(entry['name'])} | {esc(entry['game'])} | {real} | {synthetic} | {read} | {write} | {corpus} | {played} | {'; '.join(gaps)} |"
        )
        totals["formats"] += 1
        totals["vsrg"] += category == "vsrg"
        totals["rox_read"] += category == "vsrg" and read != "No"
        totals["rox_write"] += write == "Yes"
        totals["plays"] += played.startswith("Plays")
        totals["five"] += real >= 5
        totals["few"] += 0 < real < 5
        totals["none"] += real == 0

    header = "| Format | Game | Real charts | Synthetic | ROX read | ROX write | Corpus decoded | In Prism | What is missing |\n|---|---|---:|---:|---|---|---:|---|---|"
    generated = "\n".join([
        BEGIN,
        "",
        f"Totals: {totals['formats']} formats ({totals['vsrg']} VSRG). ROX reads {totals['rox_read']} VSRG formats and writes {totals['rox_write']}; "
        f"Prism plays {totals['plays']}. Real charts: {totals['five']} formats with at least 5, {totals['few']} with 1 to 4, {totals['none']} with none.",
        "",
        "## VSRG",
        "",
        header,
        *rows["vsrg"],
        "",
        "## Other games",
        "",
        "Not played by Prism except CHUNITHM `.sus` (read as a Project SEKAI chart); listed for the sample counts.",
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
