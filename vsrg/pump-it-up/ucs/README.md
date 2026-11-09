# Pump It Up User Custom Step (`.ucs`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (ASCII, CRLF)

## Overview

`.ucs` is the chart file of Pump It Up's **User Custom Step** system: players author a chart for an official song (the song's audio is not in the file), upload it (piugame.com "UCS Share", contests such as "The 6th U.C.S. Contest"), and the arcade cabinet plays it from a USB drive. It is a small line-oriented text format: a two-line header, then **blocks** `:BPM= :Delay= :Beat= :Split=` each followed by note rows of `5` (single) or `10` (double) characters. The official editor is Andamiro's "StepEdit Lite" (PIU Forge calls its web editor "much better than StepEdit Lite"); third-party editors: [VainUCS](https://piuforge.com/tools/vain-ucs) (web), [infhyroyage/PIUUCSMaker](https://github.com/infhyroyage/PIUUCSMaker) (React/TypeScript; its upload/download hooks are the real parser/serializer used below). There is **no official specification**; the description below is read from the PIUUCSMaker source (`useUploadingUCS.tsx`, `useDownloadingUCS.tsx`, `types/ucs.ts`, `services/validations.ts`). Per a NamuWiki snippet, UCS support was extended to all songs of the PHOENIX version.

## Container & encoding

- Text; **CRLF line breaks required** (the PIUUCSMaker validator rejects a file without `\r\n`: "Line break code is not CRLF"). ASCII only; no BOM known.
- One chart per file. The song is chosen outside the file (by the UCS system; the filename/upload target).
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
- Line 2 `:Mode=`: `Single` (5 columns), `Double` (10 columns), `S-Performance` (5, "single performance" = co-op style chart split by player) or `D-Performance` (10). (Performance = Pump's `routine` style: column count is the same as the base mode.)
- Then one or more **blocks**; each block header is exactly 4 lines in this order: `:BPM=`, `:Delay=`, `:Beat=`, `:Split=`. Every block must have at least one note row.

| Header | Type / range (editor validation) | Meaning |
|---|---|---|
| `:BPM=` | float, 0.1 .. 999, at most 7 significant digits | tempo of the block |
| `:Delay=` | float ms, -999999 .. 999999 (7 digits max) | start delay in milliseconds; the editor "Ignore[s] value and assume[s] 0 automatically except 1st block" (so only the first block's delay shifts the chart relative to the audio); in playback code a positive first delay delays the chart start, a negative one delays the music |
| `:Beat=` | integer 1 .. 64 | beats per measure (time signature numerator) [inference from the name and the editor's measure display] |
| `:Split=` | integer 1 .. 128 | number of rows per beat ("split") in this block |

## Timing model

- Each block is a stretch of rows at a fixed BPM. A row lasts `60 / BPM / Split` seconds (the editor draws each row `1/split` of a beat tall and scrolls at `bpm/60000` per ms) [inference from `usePlaying.tsx`]. A measure holds `Beat * Split` rows [inference]. A BPM change is simply a new block; there are no stops/warps (a stop would need an extra block with a huge `Split` or the `Delay`, which is ignored after the first block).
- Time of a row = `Delay0/1000 +` sum over previous rows of `60/bpm_block/split_block`, i.e. a plain accumulation per block [inference].
- No explicit beat numbers: position = index of the row.

## Notes

Each note row has exactly `5` (Single/S-Performance) or `10` (Double/D-Performance) characters, one per panel (a panel order of down-left, up-left, centre, up-right, down-right per pad is the Pump convention [inference]):

| Char | Meaning (PIUUCSMaker `Note.type`) |
|---|---|
| `.` | empty |
| `X` | single (tap) note |
| `M` | start point of a hold |
| `H` | "setting point" of a hold (a body/intermediate row of the hold) |
| `W` | end point of a hold |

A hold = `M` on its first row, `H` on every row between (in the same column), `W` on its last row (the editor writes a `H` for each row of the hold; "setting point of hold"). Any other character is rejected by the editor's validator. Several columns in one row = a jump/hand. There are no mines, rolls, lifts or fakes.

## Audio & images

None. Audio is the official song (the PIUUCSMaker preview takes an `.mp3` you provide, purely for editing).

## Versions & variants

- `:Format=1` is the only version seen. `Single`/`Double` are ordinary step types; `S-Performance`/`D-Performance` are co-op ("Performance") charts.
- The "UCS Base List" (Pump Pro+) hosts "base" files for songs (BPM/delay skeletons) to author on.

## Quirks & pitfalls

- CRLF is mandatory for at least one editor; LF-only files fail there.
- `:Delay=` of later blocks is ignored by that editor (value kept in the model).
- Hold bodies are explicit (`H` rows), not implied by head/tail only.
- `:Split=` up to 128 and `:Beat=` up to 64 allow nonstandard grids.
- The format carries no song identity; matching to the song is a UCS-system step.

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

(a block of 8 rows at 2 rows per beat: tap on the down-left panel at row 0, tap on the centre at row 2, a hold on the down-right panel from row 4 to row 6.)

## ROX support

Not read by ROX. A decoder would map `Single` -> 5 columns (ROX has 5-column pump support) and `Double` -> 10 columns (no ROX step type; ROX has no 10-key StepMania support), Hold from `M..H..W`, per-block BPM/Split.

## Parsers & tools

- [infhyroyage/PIUUCSMaker](https://github.com/infhyroyage/PIUUCSMaker) (TypeScript, MIT; GitHub Pages editor), [VainUCS](https://piuforge.com/tools/vain-ucs) (web), Andamiro StepEdit Lite (official), [piulin/piured](https://github.com/piulin/piured) (web-based PIU simulator, not verified to read UCS).

## Getting samples

Committed in [`samples/`](samples/SOURCES.md): eight real `.ucs` files from [StepMania-AMX/micro](https://github.com/StepMania-AMX/micro) (commit `fae7828e7e7e5f20fea67060d0bc5d6fef8a415e`; `step/1001/` and `step/1002/`: Single and Double charts, levels 3-24, `DP`/`SP` performance-style charts; `:Format=1`, CRLF). The same repository holds 3,124 `.ucs` files for 549 song ids (names like `S12_12.ucs`, `D14_14.ucs`, `DP50_2PEOPLE.ucs`); no licence file there.

More: the remaining files in that repository; the official UCS sites (e.g. https://xx.piugame.com/bbs/board.php?bo_table=ucs, https://www.pumpproplus.com/ucs-base-list.aspx: user-made charts for Andamiro songs; log-in/terms were not tested); editors that write `.ucs`: StepEdit Lite (official), [PIUUCSMaker](https://github.com/infhyroyage/PIUUCSMaker), converters [valius/UCSConverterTool](https://github.com/valius/UCSConverterTool) and [rilegoat/Step2UCS](https://github.com/rilegoat/Step2UCS). StepMania AMX reads `.ucs` directly.

## Sources

- https://piuforge.com/ (tool descriptions: VainUCS "create, edit, and export .ucs step charts")
- https://xx.piugame.com/bbs/board.php?bo_table=ucs (UCS Share / contests), https://www.pumpproplus.com/ucs-base-list.aspx
- https://en.namu.wiki/w/펌프 잇 업 PHOENIX (search snippet: UCS expanded to all songs)
- https://github.com/infhyroyage/PIUUCSMaker (src/hooks/useUploadingUCS.tsx, useDownloadingUCS.tsx, src/types/ucs.ts, src/services/validations.ts, usePlaying.tsx, src/components/workspace/Chart.tsx: a hold is built as `M` on the first row, `H` on each row between and `W` on the last row)
