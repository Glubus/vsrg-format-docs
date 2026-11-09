# Pump It Up STX step file (`.stx`, header `STF4`)
Kind: chart

Doc status: partial (chart layout decoded; a few header/division fields skipped by the only parser) · ROX: no · Category: vsrg · Encoding: binary (little-endian, per-division zlib)

## Overview

`.stx` (magic `STF4`) is an Andamiro step file of the Pump It Up arcade series: one file per song holding all modes (Practice, Normal, Hard, Nightmare, Crazy, Freestyle, Half-Double, "Division", lightmap), each a sequence of zlib-compressed "divisions" of 13-byte step lines. No public specification; known from `STX2DM` (StepMania-AMX, C++, STX to `.ksf`) and `UCSConverterTool` (valius, Dart, STX to `.ucs`, `stx_file.dart` is the basis of this page). The sources do not say which Pump It Up version uses STF4.

## Container & encoding

- Binary, little-endian (`readUint32Bytes`: "STX uses little endian"), IEEE-754 float32.
- Fixed header, then one chart block per mode, each holding zlib streams. Files can be several hundred KB.
- Per-division compression: a `uint32` byte length, then that many bytes of a zlib stream (`zlib.decode`). STX2DM uses a fixed 16 MiB output buffer (`STX_UNCOMPRESSED = 16777216`).
- Text fields are 64-byte strings. The reference parser has `utf8.decode` commented out, so the charset is presumably UTF-8 or the Korean code page [inference].

## Structure / metadata

### File header

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | magic `STF4` (`53 54 46 34`) |
| 4 | 56 | not read (unknown) |
| 60 | 64 | title (string) |
| 124 | 64 | artist (string) |
| 188 | 64 | step author (string) |
| 252 | 9 x `uint32` | absolute file offsets of the nine charts, in this order |

Chart order (`ChartIndex`): 0 practice, 1 normal, 2 hard, 3 nightmare, 4 crazy, 5 freestyle (full double), 6 half-double, 7 division, 8 lightmap. Chart `i` spans `[offset[i], offset[i+1])`, the last one to end of file. Converters ignore the lightmap chart (stage-light data). STX2DM's UI lists the same modes: Practice, Normal, Hard, Nightmare, Crazy, Full Double, Half Double, Division, Lightmap.

### Chart block

| Offset | Size | Field |
|---|---|---|
| 0 | `uint32` | difficulty (meter; -1 if unset in the parser's default) |
| 4 | 50 x `uint32` | `divisionCount` per block (`maxBlocks = 50`); a count of 0 ends the chart |
| 204 | ... | for each block, for each division: `uint32 compressedLength` + zlib stream |

### Division (after zlib decompression)

| Offset | Size | Field |
|---|---|---|
| 0 | float32 | BPM |
| 4 | `uint32` | beats per measure (default 4) |
| 8 | `uint32` | beat split (steps per beat; UCS `:Split`) |
| 12 | `uint32` | delay (centiseconds; the UCS converter multiplies by 10 to get ms) |
| 16 | 20 x `uint32` (80 bytes) | "division sets" specific to Division Mode (not decoded; e.g. "Perfect 0 - 0, Great 1 - 1" per the source comment) |
| 96 | `uint32` | speed factor (default 1000) |
| 100 | 28 | padding |
| 128 | `uint32` | line count `N` |
| 132 | `N x 13` bytes | step lines |

### Step line (13 bytes)

Only the first `stepsPerBeat` bytes are used: 5 for Practice, Normal, Hard, Crazy and Division (single), 10 for Freestyle, Nightmare and Half-Double (double; "even though half double is only 6 steps in actuality, it is set up as a 10 step chart in data"). Panel order is left to right (1P: down-left, up-left, center, up-right, down-right [inference from the Pump layout]). Step codes:

| Byte | Meaning |
|---|---|
| 0 (or unknown) | empty |
| 1 | regular step |
| 10 | hold begin |
| 11 | hold body (continuing) |
| 12 | hold end |
| 2 | "groove" note |
| 3 | "wild" note |
| 4 | A step |
| 5 | B step |
| 6 | C step |

Codes 2..6 are special/gimmick steps used by Division and other modes. The UCS converter downgrades them to regular steps.

## Timing model

Each division carries its own BPM, beat split and delay, so tempo changes are divisions. A line is one step slot, `beatSplit` lines per beat. Time of line `k` inside a division = `delay/100 s + k / beatSplit * 60 / BPM` [inference from the UCS `:Delay`/`:Split`/`:BPM` semantics the converter maps these fields to]. `beatPerMeasure` is the measure length in beats. Division Mode branches: a chart is a list of blocks, each block may hold several alternative divisions, and the player's path selects one per block ("division sets" fields likely map judgements to branches). Non-Division modes have 1 division per block ("historically no STX has more than 1 division per block in non-Division modes", `stx_converter.dart`), so each block is a tempo segment. UCSConverterTool emits every path through a Division chart as a separate `.ucs`.

## Notes

Taps (1), holds (10 -> 11... -> 12), special steps (2-6, semantics unknown), 5-panel single (5 columns), double (10), half-double (10 columns, 6 used). No mines.

## Audio & images

Not in the file.

## Versions & variants

Header `STF4` (the "4" may be a format version [inference]). No other variants known.

## Quirks & pitfalls

- Stop at the first block with count 0; the chart address list is fixed length (9).
- Divisions can be large; STX2DM allocates 16 MiB.
- Special codes 2-6 collapse to regular steps in converters; keep them for lossless output.
- `delay` is in centiseconds, not ms.
- Half-double uses a 10-wide line though only 6 columns exist.

## Example

No sample in the repo. Header magic bytes: `53 54 46 34` ("STF4").

## ROX support

Not read by ROX. Needs a new decoder (zlib, per-division tempo, 13-byte lines); the `.sm` loader already handles `pump-single`/`pump-halfdouble`.

## Parsers & tools

- UCSConverterTool (Dart/Flutter; STX/SM/SSC/NOT5 -> UCS): https://github.com/valius/UCSConverterTool (`lib/step_files/stx_file.dart`, `lib/converters/stx_converter.dart`).
- STX2DM (C++/MFC; STX -> KSF / Direct Move): https://github.com/StepMania-AMX/STX2DM (`STXDlg.cpp`).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (PC disc image "Pump It Up: The Prex 3", archive.org item `prex-pc`, `STEP/*.STX`, 73 files, ISO 403 MB). [observed: `prex3-pc_101.STX`: header `STF4`, 56 zero bytes, 64-byte title at offset 60 (`Ignition Starts!`), ascending table of nine chart offsets at 252 (288, 547, 802, ...)]. Extract the rest with `7z x PREX_PC.ISO "STEP/*.STX"`. Later PIU PC/arcade data: archive.org has Pump It Up PRO/Infinity/Prime packs as multi-GB `.rar`/`.7z` (not inspected). Converters: [StepMania-AMX/STX2DM](https://github.com/StepMania-AMX/STX2DM), [valius/UCSConverterTool](https://github.com/valius/UCSConverterTool).

## Sources

- https://github.com/valius/UCSConverterTool (commit `bc9298390ace230499480a65ccdf8c2f3dc92ef0`): `README.md`, `lib/step_files/stx_file.dart`, `lib/step_files/andamiro_common.dart`, `lib/converters/stx_converter.dart`, `lib/helpers/byte_helpers.dart`
- https://github.com/StepMania-AMX/STX2DM (commit `10890ab97927ba7e861a09073d957dda915f8e40`): `STXDlg.cpp`
