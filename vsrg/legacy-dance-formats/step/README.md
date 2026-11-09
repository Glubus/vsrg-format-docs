# pyDDR / pydance `.step` (and other "step" files)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown (text probably)

## Overview

The upstream list (`README.md` at commit `503382a`) has a bare `.step:` line. The extension is used by at least these dance-game formats:

1. **pyDDR/pydance `.step`**: the format of pydance's early versions ("`.step` (its old format)", "pydance supports loading .dance (its native format), .step (its old format), DWI, and SM files" since 0.7.0; FAQ). The pydance format spec says: "The dance format is basically the step format, but generalized, smaller, and more readable. A script to convert .step files to .dance files is forthcoming" (`dance-spec.txt`). The ncurses DDR clone **Text Text Revolution** "supports pydance's (formerly pyDDR) .step file format (which has now been superceeded by the .dance format)" and (2-25-2003 changelog) "just plays back .step files". This is the most plausible meaning of the README line.
2. **DDR "STEP"** (not a file extension known to be `.step`): the binary data of DDR 2nd..3rd Mix Plus exported by "DDR Utility" ([ddr/step](../../ddr/step/README.md)).
3. Unrelated: ISO 10303 STEP CAD files (`.step`), PyDDR-labelled `.step` files on file-extension sites.

No grammar of the pydance `.step` format was found: the pydance repository mirror (mbenkmann/pydance) has no `.step` parser (`fileparsers.py` knows `.dance`, `.dwi`, `.sm`, KSF), so the old parser was removed before the SVN import. Because `.dance` "generalizes" it, `.step` was a line-per-note-set text format with beat symbols [inference].

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

Not applicable (not documented).

## Example

Not available.

## ROX support

Not read by ROX.

## Parsers & tools

Text Text Revolution (https://ttr.sourceforge.net/): plays `.step`. pydance <= 0.6.x: original loader (source not retrieved).

## Getting samples

Committed in [`samples/`](samples/SOURCES.md): two REAL pyDDR `.step` files from Wayback captures of the pyDDR site (April 2003): `0forkbomb.step` (`version 0.61`) and `6jan.step` (`version 0.3`). The format is line-based text: header lines `version`, `file`, `song`, `group`, `bpm`, `offset`, `mix`; then `SINGLE`/`DOUBLE`, a `<DIFFICULTY> <feet>` line, and step lines `delay <beats>`, `ready`, `lyric`, `trans`, and note-length keywords (`eight`, `halfn`, `whole` ...) followed by four two-digit panel codes, e.g. `halfn 08 00 00 00` [observed in `samples/0forkbomb.step`, `samples/6jan.step`; not a documented grammar, the exact meaning of the keywords and codes is Unknown].

More: other pre-0.9 pyDDR/pydance tarballs (`pydance-0.7.x`, `0.8.x` are captured in Wayback only as 404s); Text Text Revolution songs (https://ttr.sourceforge.net/, which loads pydance `.step`). For the unrelated binary DDR STEP data see [`../../ddr/step`](../../ddr/step/README.md).

## Sources

- https://icculus.org/pyddr/faq.php
- https://ttr.sourceforge.net/
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/dance-spec.txt
- https://github.com/mbenkmann/pydance (fileparsers.py)
- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md
