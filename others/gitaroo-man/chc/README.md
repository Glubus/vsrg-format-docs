# Gitaroo Man stage chart (`.CHC`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary

## Overview
Each stage of Gitaroo Man and Gitaroo Man Lives! has one `.CHC` file (named so that characters 3-4 of the file name give the stage number, e.g. `ST03...`; the reader derives `stage` from `filename.substr(2, 2)`). It holds stage-level settings (win/lose animation frame ranges, 8 audio channel volumes/pans, gameplay speed, energy/damage factors), a list of **song sections**, and per section the branching conditions and one chart per player slot containing **trace lines**, **phrase bars** and **guard marks**. The layout below is reconstructed from the C++ reader/writer of Gitaroo Man File Reader (`CHC.cpp`, `CHC.h`), which can round-trip files. Several fields are "junk" (garbage RAM copied by the original tool, per the tool and TCRF) and are preserved as opaque bytes.

## Container & encoding
- Binary, **little-endian**, no compression. Magic `SNGS` at offset 0; section blocks tagged `CHLS`; chart blocks tagged `CHCH`.
- The reader throws if `SNGS`, `CHLS` or `CHCH` tags are missing, or if the energy factor table count is not 20.
- PS2 and PSP versions share the format; the 256-byte IMC path field is empty in PSP files ("Unused in PSP version"); `isPS2Compatible = imc[0] != 0`. Duet stages (stage numbers 11 and 12) have a swap-value convention.
- One file per stage; no companion index required beyond the game's audio (IMC) and SSQ animation files.

## Structure / metadata
Header (as written by `CHC::create`):

| Offset | Size | Field |
|---|---|---|
| 0 | 36 | header: `SNGS` tag, u32 at +4 = 6144 (+1 if "optimized"; reader: `6145` = optimized), rest unknown |
| 36 | 256 | IMC audio file path (C string) |
| 292 | 4 x 8 | four `SSQRange {float first, float last}` animation frame ranges: "Win A", "Win B", "Lose Pre", "Lose Loop" (names from the tool's text export) |
| 324 | 8 x 8 | 8 audio channels, each `{u32 volume (default 32767), u32 pan (default 16383)}` |
| 388 | 4 | `float speed` (gameplay speed) |
| 392 | 4 | `u32 count` of sections |
| then | count x 44 | cue records (below) |
| then | 4 | `u32 count` again |
| then | variable | `count` section blocks (`CHLS`) |
| then | 4 | `u32 20` (constant) |
| then | 20 x 32 | energy/damage factors: 4 players x 5 phase kinds, each 8 floats |

Cue record (44 bytes = `4 + 16 + 16 + 8 + 4`): `u32 index` (into the SSQ cue list), `char name[16]`, `char audio[16]` (audio section name), `SSQRange frames {float first, float last}` (SSQ animation frames), `u32 0`.

Energy/damage record (8 floats): `initialEnergy` (0.2), `chargeInitial` (0.01), `attackInitial` (0.015), `guardEnergy` (0.015), `attackMiss` (0.05), `guardMiss` (0.05), `chargeRelease` (0.025), `attackRelease` (0.025) (defaults of the tool's struct).

Section block (`CHLS`):

| Size | Field |
|---|---|
| 4 | tag `CHLS` |
| 4 | `u32 4864` (version/flags; older files store organized and swap bits here: `organized = v & 1`, `swapped = (v - 4864)/2`) |
| 4 | `u32 size` of the block |
| 4 | `u32 organized` (1 when the player charts are ordered correctly) |
| 4 | `u32 swapped` (player swap pattern: 0 none, 1 P2/P1/P4/P3, 2 P3/P4/P1/P2 (PS2) or P3/P2/P1/P4 (duet), 3 P4/P3/P2/P1; bit 4 = "Duet to PS2 conversion" marker) |
| 16 | junk |
| 4 | `u32 phase`: 0 INTRO, 1 CHARGE, 2 BATTLE, 3 FINAL_AG, 4 HARMONY, 5 END, >=6 FINAL_I |
| 4 | `float tempo` (BPM) |
| 4 | `u32 duration` (samples) |
| 4 | `u32 0` |
| 4 | `u32 conditionCount` |
| 16 x n | conditions `{u32 type, float argument, i32 trueEffect, i32 falseEffect}` |
| 4 | `u32 numPlayers` (always 4) |
| 4 | `u32 numCharts` (charts/subsections per player) |
| n x chart | `numPlayers * numCharts` chart blocks |

Condition types (tool text export): 0 unconditional, 1 left side energy below `argument`, 2 right side energy below `argument`, 3 random (true if rnd < argument), 4 left side unavailable (no player 3, versus only), 5 right side unavailable (no player 4), 6 left side energy < right side energy [more types may exist]. `trueEffect` / `falseEffect` select the next section / action (encoding not examined).

Chart block (`CHCH`, size `60 + 16 * (traces + guards + 2 * phrases)`):

| Size | Field |
|---|---|
| 4 | tag `CHCH` |
| 4 | `u32 4864` |
| 4 | `u32 size` (the reader ignores it: "the embedded value can be wrong") |
| 8 | zeros |
| 16 | junk |
| 4 | `i32 pivotTime` (center sample position all notes are relative to) |
| 4 | `i32 endTime` (optional transition time, unused in game) |
| 4 + 16 x n | traces: `u32 count`, then `Traceline` records |
| 4 + 32 x n | phrases: `u32 count`, then `Phrase` records |
| 4 + 16 x n | guards: `u32 count`, then `Guard` records |
| 4 | `u32 0` |

Note records (all begin with `i32 pivotAlpha`, a sample offset relative to the chart's `pivotTime`; start time in the section = `pivotTime + pivotAlpha`):
- `Traceline` (16 bytes): `i32 pivotAlpha`, `u32 duration` (samples), `float angle` (radians, the direction the line points, flipped 180 degrees), `u32 curve` (non-zero: the whole line is curved).
- `Phrase` (32 bytes): `i32 pivotAlpha`, `u32 duration`, `u32 start` (start cap flag), `u32 end` (end cap flag), `u32 animation` (character animation on hit when `start`), then 12 bytes: either 8 bytes junk + `u32 color` after the 8-byte marker `NOTECOLR` (color value used by the tool's Clone Hero export, 0 unused), or 12 junk bytes.
- `Guard` (16 bytes): `i32 pivotAlpha`, `u32 button` (0 square, 1 cross, 2 circle, 3 triangle; direction the mark appears from), 8 bytes zero.

## Timing model
- Time unit: **audio samples at 48 kHz** (`s_SAMPLES_PER_MIN = 2,880,000` = 48000 x 60). `samplesPerBeat = 2880000 / tempo`; Clone Hero export uses `ticks = samples * tempo * ticksPerBeat / 2880000`.
- Section duration in samples; tempo per section (float BPM), so tempo changes happen at section boundaries; sections can branch (conditions), so the song timeline is a graph rather than a list.
- All note times are relative to the chart's `pivotTime`, which is relative to the section start. A minimum gap `SAMPLE_GAP = 1800` samples is enforced between phrases by the editor.

## Notes
- Trace line: continuous curve segment that the player follows with the stick; angle and curve flag shape it; consecutive trace lines form the steering path of an attack phase.
- Phrase bar: sustained note (`duration`), with optional start/end caps; the player presses and holds the attack button.
- Guard mark: single press of one of four buttons, direction-coded.
- Each player slot (4 per section: P1, P2, P3, P4 / left and right "sides" with duet variants) has its own chart; `swapped` rearranges which chart goes to which player.
- Note counts and positions per chart are not bounded by the format; the PS2 and PSP builds assume organized order (sorted by `pivotAlpha`).

## Audio & images
Audio is in separate IMC files referenced by `imc` (PS2) and per-section audio names (`audio[16]`); animation is in SSQ files (frame ranges). No audio is stored in the CHC.

## Versions & variants
- PS2 (Gitaroo Man) versus PSP (Gitaroo Man Lives!): IMC path empty on PSP; "optimized" flag (header value 6145) set by the tool after minimal-glitch adjustments; "PSP to PS2" conversion available in the tool.
- Duet stages (11, 12) use different swap semantics.
- Tool sub-extensions: TAS (playback in a custom PCSX2 build) and Clone Hero `.chart` import/export.

## Quirks & pitfalls
- The chart block's stored `size` can be wrong; recompute it.
- Junk bytes (garbage from the original authoring tool) must be preserved for byte-exact round trips.
- Reader assumes sections are numbered by their appearance order, while `index` refers to the SSQ cue list.
- `pivotAlpha` can be negative.
- The `NOTECOLR` marker overlays the 8 junk bytes of a phrase; when absent the color is 0.

## Example
Not provided: no real CHC bytes were copied. The record layouts above are exact from the reader/writer. Illustrative, hand-built Guard record (16 bytes, little-endian): `pivotAlpha = 48000` (1 s), `button = 1`:
`80 BB 00 00  01 00 00 00  00 00 00 00 00 00 00 00`.

## ROX support
Not read by ROX. Stick-steered traces, branching sections and four player slots do not fit the column model; guard marks could map to four columns.

## Parsers & tools
- Gitaroo Man File Reader (C++, LGPL-3; CHC read/write/edit, Clone Hero and TAS export): https://github.com/sonicfind/Gitaroo-Man-File-Reader
- gitarootools (Python; other game files): https://github.com/boringhexi/gitarootools

## Getting samples

**Committed:** none. **Manifest:** none. No `.CHC` file is published in any open repository (Gitaroo-Man-File-Reader and gitarootools contain code and tool test data only, no CHC; checked at `a3bb1daf`/`22e6b0a5`), and the charts are commercial game data. The synthetic route was rejected because the header and junk fields cannot be verified without a real file.

**How to get one yourself**: own a copy of Gitaroo Man (PS2) or Gitaroo Man Lives! (PSP), unpack the game archives with gitarootools (`gm-xgmunpack` for XGM, `gm-pakunpack` for PAK of Gitaroo Man Lives; <https://github.com/boringhexi/gitarootools>), look for the per-stage `*.CHC` files (stage number in characters 3-4 of the file name, from `CHC.cpp`) and open them with Gitaroo Man File Reader (<https://github.com/sonicfind/Gitaroo-Man-File-Reader>, GPL-3; it can round-trip `.CHC` and export to Clone Hero `.chart`). Which archive holds the `.CHC` files is not stated in the sources read [inference: the game's data archives]. The Gitaroo Pals Discord linked from both READMEs is the community channel for help.

## Sources
- https://github.com/sonicfind/Gitaroo-Man-File-Reader (`README.md`, `GitarooFileReader/CHC/CHC.cpp`, `CHC.h`, `CH_Export.cpp`)
- https://github.com/boringhexi/gitarootools (README only)
