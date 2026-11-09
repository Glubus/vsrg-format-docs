# Phigros official chart (`.json`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview

The native chart format of Phigros (Pigeon Games). The game stores one JSON file per difficulty (e.g. extracted `Chart_IN.json`); the reverse-engineered documentation calls the numeric schema `formatVersion` 1 (legacy, early releases) and 3 (current). Third-party players (phi-chart-render, prpr, Phira, Phichain) read it and many fan tools export it. How the game packs these files in its asset bundles is not covered by the documents consulted; community tools consume the extracted JSON (see e.g. the decrypted-assets mirror <https://github.com/SonolusHaniwa/phigros-decrypted-data>).

## Packaged in

- Shipped in: `.pez` (Phira / PhiZone zip: a chart file, music, illustration, `info.yml`).

## Container & encoding

- Plain JSON, UTF-8, one file per difficulty. No archive, no compression in the file itself.
- The file has no metadata (title, composer, music file); those live in the game's own info tables (or `info.yml` / `info.txt` in fan packages, see `pez/`).

## Structure / metadata

Root object:

| Field | Type | Meaning |
|---|---|---|
| `formatVersion` | int | `1` or `3`; currently only changes how judge-line move events are decoded |
| `offset` | float | seconds; >= 0 means the music starts immediately and the chart is delayed by `offset` s |
| `judgeLineList` | array | judge lines |
| `numOfNotes` | int | old versions only (total notes); removed in game v2.5.0 |

Judge line object (`JudgeLine`):

| Field | Type | Meaning |
|---|---|---|
| `bpm` | float | BPM of **this line**; defines the line's time unit T |
| `notesAbove` / `notesBelow` | array of Note | notes on the front / back side of the line |
| `speedEvents` | array | note flow speed events |
| `judgeLineDisappearEvents` | array | opacity events |
| `judgeLineMoveEvents` | array | position events |
| `judgeLineRotateEvents` | array | rotation events (degrees, counter-clockwise) |
| `numOfNotes`, `numOfNotesAbove`, `numOfNotesBelow` | int | old versions; ignored on load; removed in 2.5.0 |

Note object:

| Field | Type | Meaning |
|---|---|---|
| `type` | int | `1` Tap, `2` Drag, `3` Hold, `4` Flick; other values are invisible/unjudgeable |
| `time` | int | judgement time in T units |
| `positionX` | float | X offset from the line centre, in X units (1 X = 0.05625 of screen width = 108 px at 1920x1080) |
| `holdTime` | int | Hold length in T; 0 for non-hold notes (always > 0 for official Holds) |
| `speed` | float | note speed multiplier; for Holds the head speed is always 1 and `speed` is the multiplier applied to the tail |
| `floorPosition` | float | initial vertical offset in Y units (1 Y = 0.6 screen height = 648 px at 1080p); normally equals the line's accumulated floor position at `time` |

Events: `startTime`/`endTime` (int, T units) plus:

| Event | Fields |
|---|---|
| speed | `value` (Y per second); v3 files also have `floorPosition` (cumulative position at `startTime`, recomputed by the game, removed in 2.5.0) |
| disappear (opacity) | `start`, `end` (<= 0 transparent, >= 1 opaque) |
| rotate | `start`, `end` (degrees, counter-clockwise) |
| move, `formatVersion` 3 | `start`, `end` = X; `start2`, `end2` = Y; origin at bottom-left, top-right is (1, 1) |
| move, `formatVersion` 1 | `start`, `end` = `1000*x + y` packed integers; origin bottom-left, x in 0..880, y in 0..520 per lchzh (Phichain's page uses 880 and 530 as scale factors: `start = round(x*880)*1000 + y*530`) |

## Timing model

- Time unit `T = 1.875 / BPM` seconds, i.e. 1/32 of a beat (a "128th note" in the source's wording), using the **line's own** `bpm`. All `time`, `holdTime`, `startTime`, `endTime` of a line are integers in T. `seconds = t * 1.875 / line.bpm`, then add `offset` (see above for sign).
- There is **no global BPM list**: tempo changes are baked into each line by authoring events/notes at different T values with a constant `bpm` (lines in one chart usually share the same `bpm`).
- Vertical distance of a note from its line: derived from the integral of `speedEvents.value` (floor position). Hold length on screen: `d = speed * holdTime * 1.875/bpm` Y (per lchzh).
- Events interpolate linearly between `start` and `end`; between events the previous end value holds [inference from the standard player implementations; not stated verbatim in the pages read].

## Notes

- Tap (1), Drag (2: hit by holding at judgement time, no tap needed), Hold (3), Flick (4: flick in any direction).
- A note's side: `notesAbove` falls onto the front of the line, `notesBelow` onto the back.
- There are no keysounds. No fake notes in the official format (the RPE format adds `isFake`).
- Simultaneous notes are just notes with equal `time` on any line; the game highlights them (not stored).

## Audio & images

Not referenced by the chart. Music/illustration are in the game's asset bundle (or `info.yml` for fan packages).

## Versions & variants

- `formatVersion` 1 vs 3: the only semantic change documented is the move event encoding. Version 3 charts of old game versions also carry `numOf*` counters and speed-event `floorPosition`, dropped in 2.5.0.
- Phichain exports always version 3 and treats `time` as a beat-scaled float on export (`time = beat * 1.875 / 60.0`); this contradicts "int" in lchzh's description and is a tool convention [unverified].
- Other formats that cover the same ideas: RPE JSON (`../rpe/`), PEC (`../pec/`).

## Quirks & pitfalls

- Units are non-obvious: X/Y units are fractions of screen dimensions, T units are per-line.
- `holdTime` is read as an integer even if written `120.0`.
- Notes whose `type` is outside 1..4 must be ignored, not rejected.
- `floorPosition` may be stale/redundant; players recompute from speed events.
- Negative `offset` has never been used by official charts.

## Example

Illustrative, hand-built from the field tables above (not an extracted official chart): one line, two notes.

```json
{"formatVersion":3,"offset":0.0,
 "judgeLineList":[{"bpm":120.0,
  "notesAbove":[{"type":1,"time":32,"positionX":0.0,"holdTime":0,"speed":1.0,"floorPosition":0.0},
                {"type":3,"time":64,"positionX":2.0,"holdTime":32,"speed":1.0,"floorPosition":0.0}],
  "notesBelow":[],
  "speedEvents":[{"startTime":0,"endTime":9999999,"value":1.0}],
  "judgeLineDisappearEvents":[{"startTime":0,"endTime":9999999,"start":1.0,"end":1.0}],
  "judgeLineMoveEvents":[{"startTime":0,"endTime":9999999,"start":0.5,"end":0.5,"start2":0.5,"end2":0.5}],
  "judgeLineRotateEvents":[{"startTime":0,"endTime":9999999,"start":0.0,"end":0.0}]}]}
```
With `bpm` 120 one T is 15.625 ms, so the Tap is at 0.5 s and the Hold at 1.0 s lasting 0.5 s.

## ROX support

Not read by ROX.

## Parsers & tools

- phi-chart-render (JS): <https://github.com/MisaLiu/phi-chart-render> (official conversion in `src/chart/convert/official.js`).
- prpr / Phira (Rust): <https://github.com/Mivik/prpr>, <https://github.com/TeamFlos/phira>.
- Phichain (Rust/Bevy editor, imports/exports official): <https://github.com/Ivan-1f/phichain>.
- phi_reversed analysis docs: <https://github.com/Hxjjxg/phi_reversed>.

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): 6 real official charts (formatVersion 1 and 3: `Introduction_Legacy`, `Christmas_SP`, `Rubbish_Sorting_SP`, `Anomaly_EZ`, `Destination_EZ`, `Winter_Cube_SP`; from the fan-site repository yuameshi/phigros-charts-repo) and two hand-written `synthetic-*` files.
- More: official charts are extracted from the game's asset bundles by community tools; public mirrors exist (the fiche cites https://github.com/SonolusHaniwa/phigros-decrypted-data) and auto-updating dump repositories (e.g. MEMZ-Chrome/phigros-chart-tracker); fan tools export the same format (Phichain, https://github.com/Ivan-1f/phichain). Phira chart packages hold either this format or RPE (see [../rpe/](../rpe/)).

## Sources

- <https://github.com/Hxjjxg/phi_reversed/blob/master/Analysis%20docs/EN_Chart_format(from%20lchzh).md>
- <https://ivan-1f-phichain.mintlify.app/formats/official>
- <https://github.com/TeamFlos/phira-docs/tree/main/src/chart-standard/chart-format/phi>
- <https://github.com/Hxjjxg/phi_reversed/blob/master/Analysis%20docs/EN_Chart_Loading_Analysis.md> (listed in search, not read in full)
