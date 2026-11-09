# pyDDR / pydance `.step` (and other "step" files)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown (text probably)

## Overview

The upstream list (`README.md` at commit `503382a`) has a bare `.step:` line. The extension belongs to three unrelated things:

1. pyDDR/pydance `.step`, the format of pydance's early versions ("`.step` (its old format)"; since 0.7.0 pydance loads "`.dance` (its native format), .step (its old format), DWI, and SM files", FAQ). The pydance spec: "The dance format is basically the step format, but generalized, smaller, and more readable. A script to convert .step files to .dance files is forthcoming" (`dance-spec.txt`). The ncurses DDR clone Text Text Revolution "supports pydance's (formerly pyDDR) .step file format (which has now been superceeded by the .dance format)" and (2-25-2003 changelog) "just plays back .step files". This is the likely meaning of the README line.
2. DDR "STEP": binary data of DDR 2nd..3rd Mix Plus exported by "DDR Utility" ([ddr/step](../../ddr/step/README.md)); not known as `.step`.
3. ISO 10303 STEP CAD files, and PyDDR-labelled `.step` files on file-extension sites.

No grammar of the pydance `.step` format was found: the mbenkmann/pydance mirror has no `.step` parser (`fileparsers.py` knows `.dance`, `.dwi`, `.sm`, KSF). Because `.dance` "generalizes" it, `.step` was a line-per-note-set text format with beat symbols [inference].

## Container & encoding

Unknown.

## Structure / metadata

Unknown.

## Timing model

Unknown.

## Notes

Unknown.

## Audio & images

Unknown.

## Versions & variants

pyDDR (early) -> pydance 0.7.0 (loads both) -> `.dance` (native, spec v1.0 2003-06-01 "No more I command").

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

Text Text Revolution (https://ttr.sourceforge.net/): plays `.step`. pydance <= 0.6.x: original loader (source not retrieved).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (real pyDDR files from April 2003 Wayback captures of the pyDDR site).

Line-based text: header lines `version`, `file`, `song`, `group`, `bpm`, `offset`, `mix`; then `SINGLE`/`DOUBLE`, a `<DIFFICULTY> <feet>` line, and step lines `delay <beats>`, `ready`, `lyric`, `trans`, and note-length keywords (`eight`, `halfn`, `whole` ...) followed by four two-digit panel codes, e.g. `halfn 08 00 00 00` [observed: 0forkbomb.step, 6jan.step; keyword and code meanings Unknown].

More: other pre-0.9 pyDDR/pydance tarballs (`pydance-0.7.x`, `0.8.x` are Wayback 404s); Text Text Revolution songs (https://ttr.sourceforge.net/). The binary DDR STEP data is in [`../../ddr/step`](../../ddr/step/README.md).

## Sources

- https://icculus.org/pyddr/faq.php
- https://ttr.sourceforge.net/
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/dance-spec.txt
- https://github.com/mbenkmann/pydance (fileparsers.py)
- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md
