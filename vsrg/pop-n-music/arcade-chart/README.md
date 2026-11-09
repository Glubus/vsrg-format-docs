# pop'n music arcade chart (no extension known; `arcade-chart`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

Official pop'n music arcade chart data. Only one public reader was found: `popnchart.js` in Gi-z/popntowav (a tool that renders pop'n music IFS/chart files to WAV). No specification exists; this page records what that code does.

## Overview

- Charts of the arcade game are stored in Konami `.ifs` archives together with `.2dx` keysound containers (README of popntowav: "relies on IFSTools (mon/ifstools)"). The chart file name/extension is not stated in the sources read; the constructor accepts any filename. [Unknown: file name pattern, difficulty/slot layout.]
- The reader handles one chart per file and has no directory: it reads events from offset 0 to end of file. A possible relation to the IIDX `.1` events ([`../../beatmania-iidx/1`](../../beatmania-iidx/1/README.md)) was not checked [inference: both start with a little-endian int32 offset].

## Container & encoding

Binary little-endian. The code reads events sequentially until the end of the file (it does not stop on an "end of song" event).

Two layouts, auto-detected by `checkFormat()`: the byte at offset 16 equals `69` -> *new* format (12-byte events); else the byte at offset 12 equals `69` -> *old* format (8-byte events); otherwise "Chart format not supported". The probe reads the byte at +4 of the second event, which the reader otherwise skips. The meaning of `69` (0x45) is not documented [Unknown].

## Structure / metadata

Per event (code):

| Offset | Size | Meaning |
| --- | --- | --- |
| +0 | int32 LE | event offset (ticks) |
| +4 | 1 | skipped by the reader (unknown) |
| +5 | int8 | event flag (type) |
| +6 | 2 | param/value (see below) |
| +8 | 4 | (new format only) long-note data, read but unused by the tool ("Long note data isn't needed for GSTs, however it's here") |

Parameter/value decoding: for flags 2 and 7, the 16-bit value `w` (little-endian) is split: `value = w >> 12` (first nibble after swapping bytes), `param = w & 0x0FFF` (12 bits). For other flags, `param` = first byte, `value` = second byte.

Event flags used by the tool:

| Flag | Meaning in `popnchart.js` |
| --- | --- |
| 1 | Playable note; `param` = column (0-8). Plays the sample currently assigned to that column. |
| 2 | Sample change: `value` = column, `param` = keysound index. |
| 3 | Background track start (plays keysound 0). |
| 4 | BPM change (`param` = BPM). |
| 7 | BGM sample: `param` = keysound index. |

Other flags exist in the files but were ignored by the tool [Unknown].

## Timing model

Offsets are in ticks; the tick rate is not given in the code (the tool does not convert ticks to seconds, it renders audio by events). [Unknown.]

## Notes

Nine columns (0-8) = the nine buttons. Long-note data is present in the new layout (4 extra bytes) but its encoding is unknown here. Keysound indices refer to the `.2dx` container; the BGM track may be at the end so indices are shifted by one (`offsetKeysounds`).

## Audio & images

`.2dx` containers, see [`../../beatmania-iidx/2dx`](../../beatmania-iidx/2dx/README.md). `twodx.js` (adapted from mon/SDVX-Song-Extractor `bm2dx.py`) reads each sample's `2DX9` header and takes the keysound index as sequential, because the popn files do not store it. A sample whose two flag bytes are `0000` is treated as a background track and moved to index 0 (`late_bg` records that it was not first).

## Versions & variants

Old (8-byte) and new (12-byte) event layouts, detected by the byte probe above. Which game versions use which is not documented.

## Quirks & pitfalls

- 12-bit param / 4-bit value packing for flags 2 and 7 only.
- Reader ignores the end-of-song event and reads to EOF.
- Format probe by a magic byte value is fragile.

## Example

None available (no sample file).

## ROX support

Not read by ROX.

## Parsers & tools

- https://github.com/Gi-z/popntowav (`popnchart.js`, `twodx.js`, `popntowav.js`, `msadpcm.js`; JavaScript)
- https://github.com/mon/ifstools ("Extractor for Konami IFS files", MIT licence; the popntowav README names it as the IFS extractor it relies on)
- pop'n charts in the community are mostly distributed as `.pms` ([`../../bms/pms`](../../bms/pms/README.md)) or BMS conversions; popn.tools lists the official charts (https://popn.tools/).

## Getting samples

No sample is committed and none is in `samples.manifest.json`: official pop'n music chart data is Konami game data, and no publicly downloadable, redistributable file was found (Gi-z/popntowav ships no fixtures; its repository tree at commit 469b6de82c6e5654eae42d130341d4c4d8b963a9 holds only `.js`, `package.json`, `README.md`). A hand-written binary was not made: the layout is unverified (Doc status: stub).

How to obtain real files (you need your own copy of the game):

- Observed in `popntowav.js` (lines 21-26 of commit 469b6de82c6e5654eae42d130341d4c4d8b963a9): the tool runs `ifstools <song>.ifs`, then reads the chart from `<ifsname>_ifs/<ifsname>_op.bin`, falling back to `<ifsname>_hp.bin` when `_op.bin` does not exist, and the keysounds from `<ifsname>_ifs/<ifsname>.2dx`. So the official charts are `.bin` files inside each song's `.ifs` archive; this resolves the "file name pattern" left Unknown above for those two names (`_op`/`_hp`; the other difficulty suffixes are not in the sources read). [observed in popntowav.js]
- Unpack the `.ifs` with mon/ifstools (https://github.com/mon/ifstools, MIT).
- A second naming example, for the Wii game: the Cutting Room Floor page "pop'n music (Wii)" lists charts such as `note\us\0101_bluebird_n5.bin` and `..._h5.bin` (search-result snippet only; the page returned HTTP 403 when fetched, so this is not verified).
- Community PMS conversions of official pop'n charts exist (ZIv thread "beatmania, beatmania IIDX and pop'n music official BMS/PMS simfiles preservation project"); they are `.pms` files, see [`../../bms/pms`](../../bms/pms/README.md), not this format.

## Sources

- https://github.com/Gi-z/popntowav and `https://raw.githubusercontent.com/Gi-z/popntowav/master/popnchart.js`, `twodx.js`
- https://popn.tools/ (search result only)
