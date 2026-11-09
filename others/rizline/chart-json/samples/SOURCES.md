# Samples: Rizline chart (`chart.json`, game asset `Chart_<DIFF>_<n>.json`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-chart.json` | hand-written from the Rizline:Chart fiche; key set cross-checked with the real `Chart_EZ_64.json` of rizlib (MIT) key by key | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic`: `bPM` 120, two `bpmShifts` (1.0, then 1.5 at beat 24), one `challengeTimes` entry, 2 themes, 2 lines with `linePoints`/`judgeRingColor`/`lineColor`, a Tap, a Catch (type 1) and a Hold (type 2 with `otherInformations` = end beat, tail canvas, tail floor), one canvas with two speed key points (1.0 -> 2.0 m/s at beat 16) and `cameraMove`; floor positions computed from the canvas speed at the base BPM (the fiche says BPM shifts do not change them) |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `Chart_EZ_64.json` | https://gitlab.com/TadeLn/rizlib/-/raw/4643e1c3e89b83956420e632454a22200111bcd3/test_data/chart/Chart_EZ_64.json | rizlib code is MIT; the chart is an extracted official Rizline game asset (copyright Pigeon Games / owner of Rizline) [inference from the file name Chart_EZ_64.json] | real official chart: 230 lines, 13 canvases, 1 challengeTime, bPM 150, pretty-printed (377 KB); not committed: commercial game asset |

Notes: the synthetic chart is pretty-printed with 2 spaces and a final newline. It was not loaded in the game or in rizlib.
