# Samples: Rizline chart (`chart.json`, game asset `Chart_<DIFF>_<n>.json`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-chart.json` | hand-written from the Rizline:Chart fiche; key set cross-checked with the real `Chart_EZ_64.json` of rizlib (MIT) key by key | vsrg-format-docs (OthersC) | CC0 | `synthetic`: `bPM` 120, two `bpmShifts` (1.0, then 1.5 at beat 24), one `challengeTimes` entry |

Notes: the synthetic chart is pretty-printed with 2 spaces and a final newline. It was not loaded in the game or in rizlib.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `Chart_EZ_64.json` | https://gitlab.com/TadeLn/rizlib/-/raw/4643e1c3e89b83956420e632454a22200111bcd3/test_data/chart/Chart_EZ_64.json | 2026-11-09 | 3e24d5cf94987a65add3dd19aa5bc031cb102b583982d7afdc04f428c9a958b5 | see source | rizlib code MIT; chart is an official Rizline asset (Pigeon Games) [inference from file name Chart_EZ_64.json] | real official chart: 230 lines, 13 canvases, 1 challengeTime, bPM 150, pretty-printed (377 KB) |
