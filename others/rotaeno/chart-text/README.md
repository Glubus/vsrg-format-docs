# Rotaeno chart text (as read by RotaenoChartTool) (`.txt`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview

A sectioned plain-text chart format read and written by the open-source **RotaenoChartTool** (C++, by adashi521), a toolkit that transforms Rotaeno charts (time shift, rotation, trail generation, note conversion...). Whether it is identical to the game's own chart text is not established by the sources; the tool treats it as the chart it edits (it writes a `# Version 2` header). Other Rotaeno tooling exists (zznyjidi/rotaeno-tools; OBS stabilisers) but no spec.

## Container & encoding

Plain text, lines; sections introduced by header lines `# BPM`, `# Tag`, `# Speed`, `# Note` (the tool reads each section until an empty line); output starts with `# Version 2` followed by a blank line, then `# BPM`, `# Speed`, `# Note`. Data lines are comma-separated numbers (parsed with `stod`).

## Structure / metadata

Per-line number lists (from `Chart.h` comments and `readInfo`):

| Section | Line format |
|---|---|
| `# BPM` | `time,BPM` |
| `# Speed` | `time,speed,smooth` (`smooth` is a boolean 0/1) |
| `# Note` | first number = note type, then type-specific values (below) |
| `# Tag` | ignored by the reader |

Note lines (type id: fields): `0` tap: `time,degree`; `1` flick: `time,degree`; `2` slide: `time,degree,slidetype,end_degree,snap,amount,prev_curv,next_curv`; `4` rotate: `time,degree,delta,prev_curv,next_curv`; `5` catch: `time,degree`; `11` trail: `time,degree,delta,prev_curv,next_curv`; any other id is read as a "Custom" note `time,degree` (the code also has a Bomb class, `time,degree`, but the reader has no id for it; ids 3, 6-10 are therefore treated as Custom). `SlideType`: Tap, Flick, SmallSlide, BigSlide.

## Timing model

`time` per record (unit not stated in the code read; likely seconds [inference]); BPM and speed tracks are separate timelines; the tool integrates speed to a note "distance" (speed_distance) and trails use curvature parameters.

## Notes

Tap (0), Flick (1), Slide (2, with start/end angle, snap/amount and curvature), Rotate (4, dial rotation instruction), Catch (5), Bomb, Trail (11, angle path with curvature). Angles in degrees on the dial.

## Audio & images

Unknown.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

Hand-written from the tool's reader (no game-exported file was available): [samples/synthetic-all-note-types.txt](samples/synthetic-all-note-types.txt) starts `# Version 2`, a blank line, `# BPM`, `0,120`, `32,150`, ... and then `# Note` with lines such as `0,1,0` (tap at time 1, degree 0) and `2,3,270,2,315,1,1,0,0` (slide).


## ROX support

Not read by ROX.

## Parsers & tools

RotaenoChartTool (C++): <https://github.com/adashi521/RotaenoChartTool>; rotaeno-tools: <https://github.com/zznyjidi/rotaeno-tools>.

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): `synthetic-all-note-types.txt` (hand-written from RotaenoChartTool's reader, CC0).
- Manifest: nothing. No game-exported chart is available from an open source: RotaenoChartTool (no licence file) and zznyjidi/rotaeno-tools (parser code only: `src/main.py`, `src/parser/*`, `utils/constant_extractor/extractor.py`) contain no sample charts.
- How a person could get one: charts are game data of Rotaeno; how the game's files map to the text described here is Unknown. Search terms: "Rotaeno chart extract", "RotaenoChartTool" [inference].

## Sources

- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/include/Chart.h>
- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/src/Chart.cpp>
- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/include/ChartDetails/Notes/Note.h>
