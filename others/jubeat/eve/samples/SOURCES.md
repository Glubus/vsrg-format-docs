# Samples: EVE (`.eve`, jubeat chart events)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-example.eve` | hand-written for this repository from the field list of `../README.md` (jubeatools `konami/commons.py` rules re-implemented in scratch: value ranges, LONG tail must stay on the 4x4 grid, three comma-separated fields, `{time:>8},{command:<8},{value:>8}` layout) | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | ASCII `.eve` with LF endings: two `TEMPO` events (400000 = 150 BPM, then 500000 = 120 BPM at tick 960), irregular beat spacing change in `HAKU`, `MEASURE` every 4 beats, taps on panels 0-15 incl. simultaneous ones, five `LONG` notes (tails right/up/left/down, lengths 1-3, durations 150-300 ticks), `END` at tick 2400 (1053 bytes) |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `jubeatools_Life_Without_You.eve` | https://raw.githubusercontent.com/Stepland/jubeatools/1aa4d33dd08760cb1b0c2a23a7d47a07c97d97a1/jubeatools/cli/tests/data/Life%20Without%20You.eve | No LICENSE file in the repository (checked tree at the pinned commit); public GitHub repo, so not committed | jubeatools CLI test fixture: 33 964 bytes, ASCII `time,command,value` lines, right-aligned fields; single `TEMPO 400000` (150 BPM), 89 `MEASURE`, 356 `HAKU`, 766 `PLAY`, one `END`, no `LONG`; origin of the chart not stated (possibly game-derived) (33964 bytes, sha256 `18b3e304bacf047a...`) |

