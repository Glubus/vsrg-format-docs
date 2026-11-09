# pop'n music arcade chart (no extension known; `arcade-chart`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview
Arcade pop'n music chart data. The only public reader is `popnchart.js` in Gi-z/popntowav (renders IFS/chart files to WAV); no specification exists.

- Charts sit in Konami `.ifs` archives with `.2dx` keysound containers (popntowav README: "relies on IFSTools (mon/ifstools)"). The constructor accepts any filename. [Unknown: file name pattern, difficulty/slot layout.]
- One chart per file, no directory: events run from offset 0 to end of file. A relation to the IIDX `.1` events ([`../../beatmania-iidx/1`](../../beatmania-iidx/1/README.md)) is unchecked [inference: both start with a little-endian int32 offset].

## Container & encoding
Binary little-endian. Events are read sequentially to EOF (no stop on an "end of song" event).

`checkFormat()` detects two layouts: byte at offset 16 equals `69` -> new format (12-byte events); else byte at offset 12 equals `69` -> old format (8-byte events); otherwise "Chart format not supported". The probe reads byte +4 of the second event, which the reader otherwise skips. The meaning of `69` (0x45) is Unknown.

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
Offsets are ticks; the tick rate is Unknown (the tool renders audio by events and never converts to seconds).

## Notes
Columns 0-8 = the nine buttons. The new layout's 4 extra bytes hold long-note data (encoding unknown). Keysound indices refer to the `.2dx` container; the BGM track may sit at the end, shifting indices by one (`offsetKeysounds`).

## Audio & images
`.2dx` containers, see [`../../beatmania-iidx/2dx`](../../beatmania-iidx/2dx/README.md). `twodx.js` (adapted from mon/SDVX-Song-Extractor `bm2dx.py`) reads each sample's `2DX9` header and takes the keysound index as sequential (popn files do not store it). A sample whose two flag bytes are `0000` is a background track, moved to index 0 (`late_bg` records that it was not first).

## Versions & variants
Old (8-byte) and new (12-byte) layouts, detected by the byte probe. Which game versions use which: Unknown.

## Quirks & pitfalls
- 12-bit param / 4-bit value packing for flags 2 and 7 only.
- The reader ignores the end-of-song event.
- The magic-byte probe is fragile.

## Example
Unknown.

## ROX support

Not read by ROX.

## Parsers & tools
- https://github.com/Gi-z/popntowav (`popnchart.js`, `twodx.js`, `popntowav.js`, `msadpcm.js`; JavaScript)
- https://github.com/mon/ifstools ("Extractor for Konami IFS files", MIT)
- Community charts are mostly `.pms` ([`../../bms/pms`](../../bms/pms/README.md)) or BMS conversions; popn.tools lists official charts (https://popn.tools/).

## Getting samples
None committed: no real file could be obtained. Searches on 2026-11-09 (GitHub path search through Sourcegraph for `*.2dx`, `<id>.1`, `*_op.bin`/`*_hp.bin`/`*.ifs`; repositories of every parser/converter named here; archive.org full-text/title search; web search) found no public copy. The tools ship no fixtures; the archive.org items are whole-game dumps or soundtracks (far above the 20 MB limit, or audio). The data exists only inside a game installation. No hand-written binary was made: the layout is unverified.

To get real files (own copy of the game required):

- [observed in popntowav.js, lines 21-26 of commit 469b6de82c6e5654eae42d130341d4c4d8b963a9] The tool runs `ifstools <song>.ifs`, reads the chart from `<ifsname>_ifs/<ifsname>_op.bin` (fallback `<ifsname>_hp.bin`) and the keysounds from `<ifsname>_ifs/<ifsname>.2dx`. So official charts are `.bin` files inside each song's `.ifs`; other difficulty suffixes are not in the sources read.
- Unpack the `.ifs` with mon/ifstools (https://github.com/mon/ifstools, MIT).
- Wii game: the Cutting Room Floor page "pop'n music (Wii)" lists charts such as `note\us\0101_bluebird_n5.bin` and `..._h5.bin` (search snippet only; the page returned HTTP 403).
- Community PMS conversions of official charts exist (ZIv thread "beatmania, beatmania IIDX and pop'n music official BMS/PMS simfiles preservation project"); they are `.pms` ([`../../bms/pms`](../../bms/pms/README.md)).

## Sources

- https://github.com/Gi-z/popntowav and `https://raw.githubusercontent.com/Gi-z/popntowav/master/popnchart.js`, `twodx.js`
- https://popn.tools/ (search result only)
