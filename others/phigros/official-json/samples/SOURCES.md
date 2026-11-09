# Samples: Phigros official chart (`.json`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-v3.json` | hand-written for this repository, built from the fiche tables (see Notes below) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic`, `formatVersion` 3: 2 judge lines at 120 BPM; Tap, Drag, Hold (`holdTime` 32, tail `speed` 1.5), Flick; one note on `notesBelow`; speed events with `floorPosition` 0 then 1.0 and a 2.0 segment; v3 move events (`start`/`end` = X, `start2`/`end2` = Y), rotate and disappear events; `floorPosition` of notes computed from the speed events |
| `synthetic-v1.json` | hand-written for this repository, built from the fiche tables (see Notes below) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic`, `formatVersion` 1: legacy `numOfNotes`/`numOfNotesAbove`/`numOfNotesBelow` counters, move events packed as `1000*x + y` integers (x scaled by 880, y by 520), no speed-event `floorPosition` |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `Introduction_Legacy.json` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/Introduction_Legacy/Introduction_Legacy.json | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); chart content (c) Pigeon Games | official chart, formatVersion 1 (numOfNotes counters, packed move events); not committed: commercial game data, unclear licence |
| `Christmas_SP.json` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/Christmas/Christmas_SP.json | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); chart content (c) Pigeon Games | official special chart, formatVersion 1; not committed: commercial game data, unclear licence |
| `Rubbish_Sorting_SP.json` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/Rubbish_Sorting_SP/Rubbish%20Sorting_SP.json | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); chart content (c) Pigeon Games | official special chart, formatVersion 3, minified single-line JSON, speed events with value 1000 and 0; not committed: commercial game data, unclear licence |

Notes: the two `synthetic-*` files follow the field tables of the fiche (unit T = 1.875 / BPM seconds, X/Y units). They were written by hand/script and were not loaded in Phigros or Phira; real charts of the game are listed in the manifest section. The packed-move scale factors follow the 880/520 convention quoted in the fiche (one of two conventions given there).
