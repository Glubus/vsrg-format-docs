# Samples: Universal Sekai Chart (USC)

## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-12lane.usc` | hand-written for this repository | vsrg-format-docs | CC0 / public domain | `synthetic`: bare `{offset, objects}` form; `bpm` (3 changes), `timeScale`, `single` taps (normal, critical, trace, `direction` up/left, non-integer `lane`/`size` = 2.5/1.5), an active critical `slide` with `start`/`tick` (ease `out`)/`hidden`/`end` (direction right) and an inactive `slide` with an `attach` node. `lane` is the note centre from the stage centre and `size` its half width (12-lane board, lanes -6..6). Built strictly from `../README.md` (TypeScript types of sonolus-pjsekai-engine 1.9.0); not run through any parser. |

## Notes
No real `.usc` file with a licence permitting redistribution was found: sonolus-pjsekai-engine (MIT, commit `0f6f37fc9b512b9d156ec4c00d998fe3916b157d`) ships only Sonolus LevelData (`shared/src/level/data/append.json`, 1.2 MB, a converted chart whose origin is not stated) and rg_converters' test files are SUS and PJSK JSON.
