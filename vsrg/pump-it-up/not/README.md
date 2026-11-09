# Pump It Up NOT / NOT5 step file (`.not`, `.not5`)
Kind: chart

Doc status: partial (step data and tempo fields decoded; title/other header fields skipped by the only parser) · ROX: no · Category: vsrg · Encoding: binary (little-endian; NOT4 step data XOR-obfuscated)

## Overview

`.not` ("NOT4", older) and `.not5` ("NOT5", header string `pump 5.0`) are **per-chart step files of Andamiro's Pump It Up arcade series** (UCSConverterTool's README calls the older ones ".NOT files (pre-NOT5)"). One file holds **one chart** (single or double). The tool converts them to the text-based `.ucs` User Custom Step format, which per its README can express everything NOT5 does ("The UCS format supports all NOT5 features fully", UCSConverterTool README). There is no public specification; this page is derived from the Dart reader `lib/step_files/not_file.dart` and its converter `not_converter.dart` in UCSConverterTool, which also encodes the "official converter" quirks. [Which arcade versions ship NOT4 versus NOT5 is not stated in the sources.]

## Container & encoding

- Binary, **little-endian**, float32 BPMs.
- Detection: if the first 8 bytes are ASCII `pump 5.0` (`70 75 6D 70 20 35 2E 30`) the file is **NOT5**, otherwise it is parsed as **NOT4**.
- NOT4 step data is obfuscated with a repeating **256-byte XOR key**: `key[i] = (0xD2 + 0x95 * i) & 0xFF` (the key table in the source starts `D2 67 FC 91 26 BB 50 E5 ...`; verified here to equal this arithmetic progression for all 256 entries); decrypted byte = `data[i] ^ key[i % 256]`.
- Single vs double is **not stored** in the header used by the converter: the converter decides from the file name (`_XD` or `_DB` in the name = double, otherwise single). Step lines are always 10 columns wide.
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
| 0xD8 (216) | `N x 2` bytes | **step array** |
| +`2N` | `N x 2` bytes | **hold-begin array** |
| +`4N` | `N x 2` bytes | **hold-end array** |

Each line `i` has three 2-byte values (one in each array): `mask = ((b[1] & 3) << 8) | b[0]`, a 10-bit panel mask. Bit `j` (0..9) is a panel, with bit 0 = the right-most panel of 2P and bit 9 = the left-most panel of 1P ("we go from the right step of 2P all the way to left step of 1P"); the parser reverses so that column 0 = 1P left. A panel with a bit in the step mask is a step; if the same bit is set in the hold-begin mask it starts a hold, if set in the hold-end mask it ends it; between a begin and an end, steps of that panel are hold bodies. The parser rejects begin+end together, begin while already holding and end while not holding.

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
| 0x88 (136) | ... | XOR-obfuscated **sparse step records** |

After XOR decryption, step records are 4 bytes: `uint16 stepIndex` (line number, 1-based: padding lines inserted so that the new line becomes index `stepIndex - 1`), then `uint16 mask` (`b[3] << 8 | b[2]`) with **bits 6..15** the ten panels (bit 6 = right-most 2P ... bit 15 = left-most 1P; the low 6 bits are lightmap/padding). Lines with no record are empty. NOT4 has **no holds**: every set bit is a regular step. A truncated last record is dropped; the line count pads the chart's end.

## Timing model

`beat split` = lines per beat. The BPM table is combined with **bunki** values: a bunki is a **time (in centiseconds) at which the next BPM from the table takes over** (a bunki of 0 ends the list; repeated bunkis are ignored: "common on official charts where a bunki and bpm would be repeated 2x"). The converter derives line indices with: `rawLines = (bunki - startTime) * (BPM / 6000) * beatSplit` (BPM/6000 beats per centisecond), exit line = floor, enter line = ceil, with fractional centisecond remainders carried into the next block's start time (adjusted by 16 cs for NOT4 and 14 cs for NOT5 "or the chart will be out of sync"). Start times are in centiseconds (the UCS `:Delay` = start time x 10 ms). NOT4 files get one empty line inserted at the beginning "to emulate official converters".

## Notes

Taps (all versions), holds (NOT5 only; begin/body/end by the three arrays), 5 columns (single) or 10 (double), 10-bit masks. No mines, no special steps.

## Audio & images

Not in the file (separate game data; NOT4 contains a title field the parser skips).

## Versions & variants

NOT4 (no magic, XOR obfuscation, 3 BPM entries, 2 bunkis, no holds) and NOT5 (`pump 5.0`, 10 BPM/start/bunki entries, hold arrays, plain data). UCS is the text format the converter targets.

## Quirks & pitfalls

- Single vs double comes from the file name convention, not the header.
- NOT4 sparse records vs NOT5 dense arrays.
- The converter's sync adjustments (16 / 14 cs) are empirical.
- Centisecond start times, not ms.
- Bit order is right-to-left (bit 0 = 2P right).

## Example

No sample in the repo (binary). Header magic of a NOT5 file: `70 75 6D 70 20 35 2E 30` (`pump 5.0`).

## ROX support

Not read by ROX. Pump 5-column charts map to ROX columns; a decoder needs the bunki/tempo logic and the NOT4 XOR step.

## Parsers & tools

UCSConverterTool (Dart/Flutter): https://github.com/valius/UCSConverterTool (`lib/step_files/not_file.dart`, `lib/converters/not_converter.dart`). Its README lists NOT5 as supported and plans NOT (pre-NOT5), KSF, SMA, SEE and NX (NX10) support.

## Getting samples

No `.not`/`.not5` file is committed or in the manifest: the only open code that reads them ([valius/UCSConverterTool](https://github.com/valius/UCSConverterTool), commit `bc9298390ace230499480a65ccdf8c2f3dc92ef0`) has no fixtures in its tree (a search for `.not`, `.stx`, `.ucs`, `sample`, `test` finds only Flutter boilerplate), and real files are Andamiro game data. Exactly how: the files are the per-chart step files of Pump It Up arcade/PC data (the converter's README calls the older ones ".NOT files (pre-NOT5)"); extract them from the data folder of a Pump It Up installation you own (exact path/archive layout is Unknown here), then check the header: `pump 5.0` = NOT5, anything else = NOT4 (XOR-obfuscated). Convert with UCSConverterTool to `.ucs` to compare with the [`.ucs` manifest samples](../ucs/samples/SOURCES.md).

## Sources

- https://github.com/valius/UCSConverterTool (commit `bc9298390ace230499480a65ccdf8c2f3dc92ef0`): `README.md`, `lib/step_files/not_file.dart`, `lib/converters/not_converter.dart`, `lib/step_files/andamiro_common.dart`, `lib/helpers/byte_helpers.dart`
