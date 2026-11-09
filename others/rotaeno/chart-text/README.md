# Rotaeno chart text (as read by RotaenoChartTool) (`.txt`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview
Sectioned plain-text chart format read and written by RotaenoChartTool (C++, adashi521; time shift, rotation, trail generation, note conversion). Whether it equals the game's own chart text is not established; the tool writes a `# Version 2` header. No spec exists (also zznyjidi/rotaeno-tools, OBS stabilisers).

## Container & encoding

Plain text lines. Sections start with header lines `# BPM`, `# Tag`, `# Speed`, `# Note`; the tool reads each section until an empty line. Output starts with `# Version 2`, a blank line, then `# BPM`, `# Speed`, `# Note`. Data lines are comma-separated numbers (parsed with `stod`).

## Structure / metadata

Per-line number lists (from `Chart.h` comments and `readInfo`):

| Section | Line format |
|---|---|
| `# BPM` | `time,BPM` |
| `# Speed` | `time,speed,smooth` (`smooth` is a boolean 0/1) |
| `# Note` | first number = note type, then type-specific values (below) |
| `# Tag` | ignored by the reader |

Note lines (type id: fields): `0` tap: `time,degree`; `1` flick: `time,degree`; `2` slide: `time,degree,slidetype,end_degree,snap,amount,prev_curv,next_curv`; `4` rotate: `time,degree,delta,prev_curv,next_curv`; `5` catch: `time,degree`; `11` trail: `time,degree,delta,prev_curv,next_curv`. Any other id is read as a "Custom" note `time,degree` (the code also has a Bomb class, `time,degree`, with no reader id; ids 3, 6-10 are therefore Custom). `SlideType`: Tap, Flick, SmallSlide, BigSlide.

## Timing model

`time` per record (unit not stated in the code read; likely seconds [inference]). BPM and speed are separate timelines. The tool integrates speed to a note "distance" (speed_distance); trails use curvature parameters.

## Notes
Angles are degrees on the dial. Bomb exists in code only (see Structure).

## Audio & images

Unknown.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example
Hand-written from the reader: [samples/synthetic-all-note-types.txt](samples/synthetic-all-note-types.txt) starts `# Version 2`, a blank line, `# BPM`, `0,120`, `32,150`, ... then `# Note` with lines such as `0,1,0` (tap at time 1, degree 0) and `2,3,270,2,315,1,1,0,0` (slide).

## ROX support

Not read by ROX.

## Parsers & tools

RotaenoChartTool (C++): <https://github.com/adashi521/RotaenoChartTool>; rotaeno-tools: <https://github.com/zznyjidi/rotaeno-tools>.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). No open source holds a real chart. Checked: RotaenoChartTool (no licence file), zznyjidi/rotaeno-tools (parser code), chogang/rotaeno-song-database (metadata and extraction tools, no charts). How the game's files map to this text format is Unknown.

## Sources

- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/include/Chart.h>
- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/src/Chart.cpp>
- <https://cdn.jsdelivr.net/gh/adashi521/RotaenoChartTool@main/include/ChartDetails/Notes/Note.h>
