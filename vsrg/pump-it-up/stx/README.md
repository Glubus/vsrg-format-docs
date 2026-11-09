# Pump It Up STX step file (`.stx`, header `STF4`)
Kind: chart

Doc status: partial (chart layout decoded; a few header/division fields skipped by the only parser) · ROX: no · Category: vsrg · Encoding: binary (little-endian, per-division zlib)

## Overview

`.stx` is an **Andamiro step file for the Pump It Up arcade series**: one file per song, holding **all difficulty modes** (Practice, Normal, Hard, Nightmare, Crazy, Freestyle, Half-Double, "Division" and a lightmap chart), each as a sequence of zlib-compressed "divisions" made of 13-byte step lines. Its magic is the ASCII string `STF4`. The format has no public specification from Andamiro; the community knows it from converters: `STX2DM` (StepMania-AMX, Windows/C++, converts STX to Kick It Up / Direct Move `.ksf`) and `UCSConverterTool` (valius, Dart/Flutter, STX to `.ucs`), whose `stx_file.dart` is the reader this page is based on (its README lists `.STX files` as supported input). [The Pump It Up game series/version that uses STF4 is not stated in the sources consulted.]

## Container & encoding

- Binary, **little-endian** (`readUint32Bytes`: "STX uses little endian"), IEEE-754 float32.
- File = fixed header + one chart block per mode + (inside each chart) zlib streams. Files can be several hundred KB.
- Per-division compression: a `uint32` byte length followed by that many bytes of a **zlib stream** (`zlib.decode`). STX2DM uses a fixed 16 MiB output buffer (`STX_UNCOMPRESSED = 16777216`) for decompression.
- Text fields: 64-byte strings (the reference parser has `utf8.decode` for them commented out, so the charset is presumably UTF-8 or the Korean code page [inference]).

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

Chart order (`ChartIndex`): 0 practice, 1 normal, 2 hard, 3 nightmare, 4 crazy, 5 freestyle (full double), 6 half-double, 7 division, 8 lightmap. Chart `i` spans `[offset[i], offset[i+1])`, the last one to end of file. The lightmap chart (stage-light data) is ignored by converters. STX2DM's UI exposes the same modes: Practice, Normal, Hard, Nightmare, Crazy, Full Double, Half Double, Division, Lightmap.

### Chart block

| Offset | Size | Field |
|---|---|---|
| 0 | `uint32` | difficulty (meter; -1 if unset in the parser's default) |
| 4 | 50 x `uint32` | `divisionCount` per block (`maxBlocks = 50`); a count of **0 ends the chart** |
| 204 | ... | for each block, for each division: `uint32 compressedLength` + zlib stream |

### Division (after zlib decompression)

| Offset | Size | Field |
|---|---|---|
| 0 | float32 | BPM |
| 4 | `uint32` | beats per measure (default 4) |
| 8 | `uint32` | beat split (steps per beat; UCS `:Split`) |
| 12 | `uint32` | delay (**centiseconds**; the UCS converter multiplies by 10 to get ms) |
| 16 | 20 x `uint32` (80 bytes) | "division sets" specific to Division Mode (not decoded; e.g. "Perfect 0 - 0, Great 1 - 1" per the source comment) |
| 96 | `uint32` | speed factor (default 1000) |
| 100 | 28 | padding |
| 128 | `uint32` | line count `N` |
| 132 | `N x 13` bytes | step lines |

### Step line (13 bytes)

Only the first `stepsPerBeat` bytes are used (the rest are not interpreted): **5** for Practice, Normal, Hard, Crazy and Division (single), **10** for Freestyle, Nightmare and Half-Double (double; "even though half double is only 6 steps in actuality, it is set up as a 10 step chart in data"). Panel order is left to right (1P: down-left, up-left, center, up-right, down-right [inference from the Pump layout]). Step codes:

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

Codes 2..6 are special/gimmick step types used by Division/other modes; the UCS converter downgrades them to regular steps.

## Timing model

Each division carries **its own BPM, beat split and delay**, so tempo changes are divisions. A line is one step slot: **`beatSplit` lines per beat**; time of line `k` inside a division = `delay/100 s + k / beatSplit * 60 / BPM` [inference from the UCS `:Delay`/`:Split`/`:BPM` semantics that the converter maps these fields to]. `beatPerMeasure` is the measure length in beats. Division Mode (a branching mode): a chart is a list of **blocks**; each block may contain several alternative divisions, and the player's path selects one division per block ("division sets" fields likely map judgements to branches). Non-Division modes have 1 division per block ("historically no STX has more than 1 division per block in non-Division modes", `stx_converter.dart`), so each block is simply a tempo segment. UCSConverterTool emits every path through a Division chart as a separate `.ucs`.

## Notes

Taps (1), holds (10 -> 11... -> 12), special steps (2-6, semantics unknown), 5-panel single (5 columns) and double (10 columns), half-double (10 columns with 6 used). No mines (UCS has none either).

## Audio & images

Not in the file (separate game data).

## Versions & variants

Header `STF4` (the "4" may be a format version [inference]). No other variants known to the parsers.

## Quirks & pitfalls

- Block/division counts: stop at the first block with count 0; chart address list is fixed length (9).
- Decompression buffer size: divisions can be large; STX2DM allocates 16 MiB.
- Special step codes 2-6 collapse to regular steps in converters; keep them if lossless.
- `delay` is in centiseconds, not ms.
- Panel columns: half-double uses a 10-wide line even though only 6 columns exist.

## Example

No sample in the repo (binary, no public sample). Header magic bytes: `53 54 46 34` ("STF4").

## ROX support

Not read by ROX. Pump `pump-single` 5-column charts map to ROX (the `.sm` loader already supports `pump-single`/`pump-halfdouble`); STX would need a new decoder (zlib, per-division tempo, 13-byte lines).

## Parsers & tools

- UCSConverterTool (Dart/Flutter; STX/SM/SSC/NOT5 -> UCS): https://github.com/valius/UCSConverterTool (`lib/step_files/stx_file.dart`, `lib/converters/stx_converter.dart`).
- STX2DM (C++/MFC; STX -> KSF / Direct Move): https://github.com/StepMania-AMX/STX2DM (`STXDlg.cpp`).

## Sources

- https://github.com/valius/UCSConverterTool (commit `bc9298390ace230499480a65ccdf8c2f3dc92ef0`): `README.md`, `lib/step_files/stx_file.dart`, `lib/step_files/andamiro_common.dart`, `lib/converters/stx_converter.dart`, `lib/helpers/byte_helpers.dart`
- https://github.com/StepMania-AMX/STX2DM (commit `10890ab97927ba7e861a09073d957dda915f8e40`): `STXDlg.cpp`
