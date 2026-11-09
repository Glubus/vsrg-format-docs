# Pump It Up NOT / NOT5 step file (`.not`, `.not5`)
Kind: chart

Doc status: partial (step data and tempo fields decoded; title/other header fields skipped by the only parser) · ROX: decode only · Category: vsrg · Encoding: binary (little-endian; NOT4 step data XOR-obfuscated)

## Overview

`.not` ("NOT4", older) and `.not5` ("NOT5", header `pump 5.0`) are per-chart step files of Andamiro's Pump It Up arcade series. One file holds one chart (single or double). UCSConverterTool converts them to `.ucs`, which per its README "supports all NOT5 features fully". No public specification exists; this page is derived from `lib/step_files/not_file.dart` and `not_converter.dart` in that tool, which also encodes the "official converter" quirks. Which arcade versions ship NOT4 or NOT5 is not stated.

## Container & encoding

- Binary, little-endian, float32 BPMs.
- First 8 bytes ASCII `pump 5.0` (`70 75 6D 70 20 35 2E 30`): NOT5. Otherwise NOT4.
- NOT4 step data uses a repeating 256-byte XOR key: `key[i] = (0xD2 + 0x95 * i) & 0xFF` (the source table starts `D2 67 FC 91 26 BB 50 E5 ...`; verified here to equal this progression for all 256 entries). Decrypted byte = `data[i] ^ key[i % 256]`.
- Single vs double is not stored in the header the converter uses. It reads the file name: `_XD` or `_DB` means double, otherwise single. Step lines are always 10 columns wide.
- One chart per file.

## Structure / metadata

### NOT5 (`pump 5.0`)

| Offset | Size | Field |
|---|---|---|
| 0 | 8 | magic `pump 5.0` |
| 8 | 2 | not read |
| 10 | `uint32` | line count `N` |
| 14 | 2 | not read |
| 16 | 10 x float32 | BPM table (`maxChanges = 10`) |
| 56 | 10 x `uint32` | start times (centiseconds) |
| 96 | 10 x `uint32` | "bunki" values |
| 136 | `uint32` | beat split (lines per beat) |
| 140 | `uint32` | beats per measure (0 means 16, "follow official converter default") |
| 144 | ... | not read (up to 0xD8) |
| 0xD8 (216) | `N x 2` bytes | step array |
| +`2N` | `N x 2` bytes | hold-begin array |
| +`4N` | `N x 2` bytes | hold-end array |

Each line `i` has one 2-byte value in each array: `mask = ((b[1] & 3) << 8) | b[0]`, a 10-bit panel mask. Bit `j` (0..9) is a panel. Bit 0 is the right-most panel of 2P and bit 9 the left-most panel of 1P ("we go from the right step of 2P all the way to left step of 1P"). The parser reverses this so column 0 = 1P left. A bit in the step mask is a step. The same bit in the hold-begin mask starts a hold, in the hold-end mask ends it; steps of that panel between begin and end are hold bodies. The parser rejects begin+end together, begin while already holding and end while not holding.

### NOT4 (pre-NOT5)

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | not interpreted ("number of steps") |
| 4 | 4 | not read |
| 8 | 3 x float32 | BPM table (`maxChangesNOT4 = 3`) |
| 20 | 4 | not read |
| 24 | 3 x `uint32` | start times (centiseconds) |
| 36 | 4 | not read |
| 40 | 2 x `uint32` | bunki values (only 2) |
| 48 | 8 | not read |
| 56 | `uint32` | beat split |
| 60 | `uint32` | beats per measure (0 means 4) |
| 64 | 4 | track number (ignored) |
| 68 | 4 | title (ignored) |
| 0x84 (132) | `uint16` | line count (the following 2 bytes repeat the count for doubles and are ignored) |
| 0x88 (136) | ... | XOR-obfuscated sparse step records |

After XOR decryption, step records are 4 bytes: `uint16 stepIndex` (line number, 1-based: padding lines inserted so that the new line becomes index `stepIndex - 1`), then `uint16 mask` (`b[3] << 8 | b[2]`). Bits 6..15 are the ten panels (bit 6 = right-most 2P ... bit 15 = left-most 1P); the low 6 bits are lightmap/padding. Lines with no record are empty. NOT4 has no holds: every set bit is a regular step. A truncated last record is dropped; the line count pads the chart's end.

## Timing model

`beat split` = lines per beat. A bunki is the time (centiseconds) at which the next BPM from the table takes over. A bunki of 0 ends the list. Repeated bunkis are ignored ("common on official charts where a bunki and bpm would be repeated 2x"). The converter derives line indices with `rawLines = (bunki - startTime) * (BPM / 6000) * beatSplit` (BPM/6000 beats per centisecond). Exit line = floor, enter line = ceil. Fractional centisecond remainders carry into the next block's start time, adjusted by 16 cs for NOT4 and 14 cs for NOT5 "or the chart will be out of sync". Start times are in centiseconds (the UCS `:Delay` = start time x 10 ms). NOT4 files get one empty line inserted at the beginning "to emulate official converters".

## Notes

Taps (all versions), holds (NOT5 only), 5 columns (single) or 10 (double), 10-bit masks. No mines, no special steps.

## Audio & images

Not in the file (NOT4 has a title field the parser skips).

## Versions & variants

NOT4: no magic, XOR obfuscation, 3 BPM entries, 2 bunkis, no holds. NOT5: `pump 5.0`, 10 BPM/start/bunki entries, hold arrays, plain data.

## Quirks & pitfalls

- Single vs double comes from the file name, not the header.
- The converter's sync adjustments (16 / 14 cs) are empirical.
- Start times are centiseconds, not ms.
- Bit order is right-to-left (bit 0 = 2P right).

## Example

No sample in the repo. NOT5 header magic: `70 75 6D 70 20 35 2E 30` (`pump 5.0`).

## ROX support

Decode only (`rox::formats::pump::NotDecoder`, `decode_named`): `NOT4` records (line = the record's step index, panels = bits 6-15; light-only records skipped) and `NOT5` arrays with holds. Line `p` of tempo segment `j` at `start[j] + p / (BPM[j] / 6000 × split)` cs; the converter's 16/14 cs adjustments are not reproduced (no corpus file has a bunki). Columns: 10 when the name has `_XD`/`_DB` or a 2P panel is used (observed: the `DOUBLE` folder files and two others use all 10 panels; the converter's name rule alone would read them as single), else 5. All 12 corpus `NOT4` decode. Observed: the line count at 0x84 is 0 in most files, the first `u32` is the record count.

## Parsers & tools

UCSConverterTool (Dart/Flutter): https://github.com/valius/UCSConverterTool (`lib/step_files/not_file.dart`, `lib/converters/not_converter.dart`). Its README lists NOT5 as supported and plans NOT (pre-NOT5), KSF, SMA, SEE and NX (NX10) support.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Source: PC release "Pump It Up: The Fusion (3rd Dance Floor)", archive.org item `piupc3rd`, `DATA/STEP/{EASY,HARD,DOUBLE,REMIX}/`, 251 `.NOT` files (fetched with HTTP range requests; skip the mp3/avi/bmp/jpg members). No `pump 5.0` (NOT5) file found; [valius/UCSConverterTool](https://github.com/valius/UCSConverterTool) has no fixtures. The 1st/2nd Dance Floor disc (`pump-it-up-fusion-1st-2nd-dance-floor`) holds 155 obfuscated `.stf` files, a different extension. NOT5 files come from later Andamiro PC/arcade data (exact path Unknown here) and convert with UCSConverterTool to `.ucs` (see [`../ucs`](../ucs/samples/SOURCES.md)).

## Sources

- https://github.com/valius/UCSConverterTool (commit `bc9298390ace230499480a65ccdf8c2f3dc92ef0`): `README.md`, `lib/step_files/not_file.dart`, `lib/converters/not_converter.dart`, `lib/step_files/andamiro_common.dart`, `lib/helpers/byte_helpers.dart`
