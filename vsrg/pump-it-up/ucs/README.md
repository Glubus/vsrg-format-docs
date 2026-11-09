# Pump It Up User Custom Step (`.ucs`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (ASCII, CRLF)

## Overview

`.ucs` is the chart file of Pump It Up's User Custom Step system: players author a chart for an official song, upload it (piugame.com "UCS Share", contests such as "The 6th U.C.S. Contest") and play it from a USB drive. Line-oriented text: a two-line header, then blocks `:BPM= :Delay= :Beat= :Split=` each followed by note rows of `5` (single) or `10` (double) characters. Editors: Andamiro's "StepEdit Lite", [VainUCS](https://piuforge.com/tools/vain-ucs) (web; PIU Forge calls it "much better than StepEdit Lite"), [infhyroyage/PIUUCSMaker](https://github.com/infhyroyage/PIUUCSMaker) (React/TypeScript). No official specification; this page is read from the PIUUCSMaker source (`useUploadingUCS.tsx`, `useDownloadingUCS.tsx`, `types/ucs.ts`, `services/validations.ts`). Per a NamuWiki snippet, UCS was extended to all songs of PHOENIX.

## Container & encoding

- Text; CRLF line breaks required (the PIUUCSMaker validator rejects a file without `\r\n`: "Line break code is not CRLF"). ASCII only; no BOM known.
- One chart per file. The UCS system picks the song (filename/upload target).
- Extension `.ucs` (PIUUCSMaker checks `name.split(".").pop() === "ucs"`).

## Structure / metadata

```
:Format=1
:Mode=<Single|Double|S-Performance|D-Performance>
:BPM=<float>
:Delay=<float>
:Beat=<int>
:Split=<int>
<note rows...>
:BPM=...        (next block)
:Delay=...
:Beat=...
:Split=...
<note rows...>
```

- Line 1 must be exactly `:Format=1`.
- Line 2 `:Mode=`: `Single` (5 columns), `Double` (10 columns), `S-Performance` (5, "single performance", co-op chart split by player) or `D-Performance` (10). Performance is Pump's `routine` style; the column count equals the base mode.
- Then one or more blocks. Each block header is exactly 4 lines in this order: `:BPM=`, `:Delay=`, `:Beat=`, `:Split=`. Every block needs at least one note row.

| Header | Type / range (editor validation) | Meaning |
|---|---|---|
| `:BPM=` | float, 0.1 .. 999, at most 7 significant digits | tempo of the block |
| `:Delay=` | float ms, -999999 .. 999999 (7 digits max) | start delay in milliseconds; the editor "Ignore[s] value and assume[s] 0 automatically except 1st block", so only the first block's delay shifts the chart relative to the audio. In playback code a positive first delay delays the chart start, a negative one delays the music |
| `:Beat=` | integer 1 .. 64 | beats per measure (time signature numerator) [inference from the name and the editor's measure display] |
| `:Split=` | integer 1 .. 128 | rows per beat in this block |

## Timing model

- Each block is a stretch of rows at a fixed BPM. A row lasts `60 / BPM / Split` seconds (the editor draws each row `1/split` of a beat tall and scrolls at `bpm/60000` per ms) [inference from `usePlaying.tsx`]. A measure holds `Beat * Split` rows [inference]. A BPM change is a new block. There are no stops/warps (a stop would need an extra block with a huge `Split` or the `Delay`, which is ignored after the first block).
- Time of a row = `Delay0/1000 +` sum over previous rows of `60/bpm_block/split_block` [inference].
- No explicit beat numbers: position = row index.

## Notes

Each note row has exactly `5` (Single/S-Performance) or `10` (Double/D-Performance) characters, one per panel (Pump order down-left, up-left, centre, up-right, down-right per pad [inference]):

| Char | Meaning (PIUUCSMaker `Note.type`) |
|---|---|
| `.` | empty |
| `X` | single (tap) note |
| `M` | start point of a hold |
| `H` | "setting point" of a hold (a body/intermediate row of the hold) |
| `W` | end point of a hold |

A hold is `M` on its first row, `H` on every row between (same column), `W` on its last row. Any other character is rejected by the editor's validator. Several columns in one row form a jump/hand. No mines, rolls, lifts or fakes.

## Audio & images

None (the official song is used; the PIUUCSMaker preview takes an `.mp3` you provide).

## Versions & variants

`:Format=1` is the only version seen. The "UCS Base List" (Pump Pro+) hosts base files (BPM/delay skeletons) for songs.

## Quirks & pitfalls

- CRLF is mandatory for at least one editor; LF-only files fail there.
- That editor ignores `:Delay=` of later blocks (value kept in the model).
- Hold bodies are explicit (`H` rows).
- `:Split=` up to 128 and `:Beat=` up to 64 allow nonstandard grids.
- No song identity in the file.

## Example

Constructed from the serializer of `useDownloadingUCS.tsx` (illustrative; not a real UCS file):

```
:Format=1
:Mode=Single
:BPM=140
:Delay=0
:Beat=4
:Split=2
X....
.....
..X..
.....
....M
....H
....W
.....
```

A block of 8 rows at 2 rows per beat: tap on the down-left panel at row 0, tap on the centre at row 2, a hold on the down-right panel from row 4 to row 6.

## ROX support

Not read by ROX. `Single` maps to 5 columns (ROX has 5-column pump support); `Double` has no ROX step type.

## Parsers & tools

- [infhyroyage/PIUUCSMaker](https://github.com/infhyroyage/PIUUCSMaker) (TypeScript, MIT; GitHub Pages editor), [VainUCS](https://piuforge.com/tools/vain-ucs) (web), Andamiro StepEdit Lite (official), [piulin/piured](https://github.com/piulin/piured) (web-based PIU simulator, not verified to read UCS).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) ([StepMania-AMX/micro](https://github.com/StepMania-AMX/micro), commit `fae7828e7e7e5f20fea67060d0bc5d6fef8a415e`, `step/1001/`, `step/1002/`). That repository holds 3,124 `.ucs` files for 549 song ids (names like `S12_12.ucs`, `D14_14.ucs`, `DP50_2PEOPLE.ucs`); no licence file. Official UCS sites: https://xx.piugame.com/bbs/board.php?bo_table=ucs, https://www.pumpproplus.com/ucs-base-list.aspx (log-in/terms not tested). Converters: [valius/UCSConverterTool](https://github.com/valius/UCSConverterTool), [rilegoat/Step2UCS](https://github.com/rilegoat/Step2UCS). StepMania AMX reads `.ucs` directly.

## Sources

- https://piuforge.com/ (tool descriptions: VainUCS "create, edit, and export .ucs step charts")
- https://xx.piugame.com/bbs/board.php?bo_table=ucs (UCS Share / contests), https://www.pumpproplus.com/ucs-base-list.aspx
- https://en.namu.wiki/w/펌프 잇 업 PHOENIX (search snippet: UCS expanded to all songs)
- https://github.com/infhyroyage/PIUUCSMaker (src/hooks/useUploadingUCS.tsx, useDownloadingUCS.tsx, src/types/ucs.ts, src/services/validations.ts, usePlaying.tsx, src/components/workspace/Chart.tsx: a hold is built as `M` on the first row, `H` on each row between and `W` on the last row)
