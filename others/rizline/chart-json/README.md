# Rizline chart (`chart.json`, game asset `Chart_<DIFF>_<n>.json`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview
One JSON document per difficulty. The official game stores charts as Unity assets (`Chart_EZ_64.json` style names in rizlib's test data), extracted from the app's asset bundles. The PC version publishes custom charts on the Steam Workshop (`Steam/steamapps/workshop/content/2272590/<workshop_item_id>/`) as a folder with `chart.json`, `metadata.json` and `song.ogg`. The field list is from the Rhythm Game Wiki page "Rizline:Chart", cross-checked against rizlib's serde structs and a real chart (`test_data/chart/Chart_EZ_64.json`: 230 lines, 13 canvases).

## Container & encoding
- UTF-8 JSON, one chart per file. Official files may be pretty-printed; the Workshop `metadata.json` is minified.
- Workshop folder: `chart.json`, `metadata.json`, `song.ogg` (Ogg audio).
- No compression or encryption known. Fields are camelCase except `bPM` (sic).

## Structure / metadata
Root object:

| Key | Type | Meaning |
|---|---|---|
| `fileVersion` | int | usually 0; 1 in some charts (e.g. Tempest IN) [wiki: verify] |
| `songsName` | string | usually empty; unused leftover from the charting software |
| `themes[]` | `{colorsList: [color x3]}` | two themes: 0 default, 1 Riztime; colors: background, note, particle |
| `challengeTimes[]` | `{checkPoint, start, end, transTime}` | Riztime periods; `start`/`end` in beats; `checkPoint` purpose unknown; `transTime` transition time, unit unknown |
| `bPM` | float | initial BPM |
| `bpmShifts[]` | key points | tempo changes, `value` is a **multiplier** of `bPM` (1.5 at 120 gives 180); instant, `easeType` ignored |
| `offset` | float | audio/chart offset; always 0.0 in known charts, unit unknown |
| `lines[]` | Line | all lines (the bulk of the file) |
| `canvasMoves[]` | `{index, xPositionKeyPoints[], speedKeyPoints[]}` | one entry per canvas; `index` equals the array index; x keyframes give the absolute x of the canvas center; speed keyframes in meters/second, instant |
| `cameraMove` | `{scaleKeyPoints[], xPositionKeyPoints[]}` | camera zoom and x position |

Line: `linePoints[]`, `notes[]`, `judgeRingColor[]` (color key points), `lineColor[]` (color key points).
- LinePoint: `time` (beats), `xPosition` (screen fraction: -0.5 left edge, 0 center, 0.5 right edge; may exceed the range), `color` (vertex color for gradients, also gives alpha), `easeType` (int), `canvasIndex` (which canvas moves it), `floorPosition` (float, meters).
- Note: `type` (0 Tap, 1 Catch (drag), 2 Hold), `time` (beats), `floorPosition` (meters), `otherInformations[]`: empty except for Hold notes where `[0]` = end time in beats, `[1]` = canvas index of the tail (float, whole number), `[2]` = floor position of the tail (meters).
- Key point: `time` (beats), `value`, `easeType`, `floorPosition`.
- Color: `{r,g,b,a}` ints 0-255.
- Color key point (`lineColor`, `judgeRingColor`): `startColor`, `endColor`, `time`; always linear: `t = (now - prev.time)/(next.time - prev.time)`, `color = (1-t)*prev.startColor + t*prev.endColor`.
- Ease type enum: 0 Linear, 1 InQuad, 2 OutQuad, 3 InOutQuad, 4 InCubic, 5 OutCubic, 6 InOutCubic, 7 InQuart, 8 OutQuart, 9 InOutQuart, 10 InQuint, 11 OutQuint, 12 InOutQuint, 13 Zero, 14 One, 15 InCirc, 16 OutCirc, 17 OutSine, 18 InSine.

`metadata.json` (Workshop custom chart): `title`, `composer`, `difficulty` (0 Easy; 1 Hard?, 2 Insane?, 3 Another? per wiki), `level` (1-15), `maxHit`, `maxScore`, `previewTime` (float).

## Timing model
- All times (`time`, `start`, `end`, `otherInformations[0]`) are in **beats**. Seconds: integrate tempo from `bPM` and the `bpmShifts` step function: `sec_per_beat = 60 / (bPM * multiplier(t))`, multiplier piecewise constant (a shift is instant).
- A note's scroll position is `floorPosition` = meters from the judgement line at level start: the integral over time of the canvas speed (m/s, negative speeds allowed, instant changes) from the `speedKeyPoints` of its canvas. BPM shifts do not change floor positions. The in-game scroll-speed setting multiplies them at runtime. The game stores them to speed up loading; they can be recomputed from the speed key points.
- Example from the wiki: with a constant canvas speed of 1.0 m/s and 120 BPM, a note at beat 2 has floor position 1.0 m.
- `offset` is 0 everywhere; audio sync is handled by the audio file itself [inference].

## Notes
- Tap (0): tap at `time`. Catch (1): drag/catch note, no tap needed but the finger must be on the line [inference from the name]. Hold (2): press from `time` to `otherInformations[0]`; the tail can be on a different canvas.
- A note belongs to a line; its horizontal position is the line's x at that time (interpolated between `linePoints` with their `easeType`) plus the canvas x. A line may have zero notes (decorative or guiding).
- Simultaneous notes are multiple notes with the same `time`, usually on different lines.

## Audio & images
Audio is outside the JSON: `song.ogg` for Workshop charts; official audio is in separate asset files (the wiki has pages for audio files, asset lists and the `Catalog_catalog.json` asset catalog). No offset or preview fields in `chart.json`; the preview start is `previewTime` in custom `metadata.json`.

## Versions & variants
- `fileVersion` 0 and 1. Newer official charts add `__isSample` / `__easeMark {startValue, easeType}` objects inside speed key points (editor leftovers without gameplay effect, per the wiki).
- Workshop custom charts use the same chart schema plus `metadata.json`.

## Quirks & pitfalls
- Times are in beats but scroll geometry uses precomputed `floorPosition`: recompute or keep it.
- `otherInformations` is a bare float array `[end, canvasIndex, tailFloorPosition]`; the canvas index is a float.
- Colors alpha: `lineColor` alpha acts as blend weight; the drawn alpha comes from `linePoint` (wiki section "Interactions between linePoint colors and lineColor key points").
- Key point `value` means different things: absolute x (canvas/camera), meters per second (speed), multiplier (BPM).

## Example
Header of a real chart, from rizlib `test_data/chart/Chart_EZ_64.json` (trimmed):
```json
{"fileVersion":0,"songsName":"",
 "themes":[{"colorsList":[{"r":255,"g":255,"b":255,"a":255},{"r":185,"g":229,"b":255,"a":255},{"r":115,"g":162,"b":225,"a":255}]}, "..."],
 "challengeTimes":[{"checkPoint":131.0,"start":131.0,"end":195.0,"transTime":0.5}],
 "bPM":150.0,
 "bpmShifts":[{"time":0.0,"value":1.0,"easeType":0,"floorPosition":0.0}],
 "offset":0.0, "lines":["..."], "canvasMoves":["..."], "cameraMove":{"scaleKeyPoints":["..."],"xPositionKeyPoints":["..."]}}
```
A Hold note from the same file: `{"type":2,"time":132.0,"floorPosition":52.8,"otherInformations":[134.0,2.0,53.6]}`.

## ROX support
Not read by ROX. Conversion to fixed columns would be lossy (free-form lines, moving canvases); BPM shifts and note times convert directly.

## Parsers & tools
- rizlib (Rust, serde structs for chart, catalog, asset lists, game config): https://gitlab.com/TadeLn/rizlib (crates.io `rizlib`)
- Rhythm Game Wiki documentation: https://rgwiki.stary.pc.pl/wiki/Rizline:Chart

## Getting samples
Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: Steam Workshop custom charts (folder `Steam/steamapps/workshop/content/2272590/<workshop_item_id>/` with `chart.json`, `metadata.json`, `song.ogg`; needs Steam). Official charts are extracted from the game's asset bundles (rgwiki guide "Extracting asset files from an Android device"). No public chart collection was found on GitHub.

## Sources
- https://rgwiki.stary.pc.pl/wiki/Rizline:Chart
- https://rgwiki.stary.pc.pl/wiki/Rizline:Chart_file
- https://rgwiki.stary.pc.pl/wiki/Rizline:Custom_charts
- https://rgwiki.stary.pc.pl/wiki/Rizline:Custom_chart_metadata
- https://gitlab.com/TadeLn/rizlib (`src/chart/*.rs`, `test_data/chart/Chart_EZ_64.json`)
- https://docs.rs/rizlib/latest/rizlib/
