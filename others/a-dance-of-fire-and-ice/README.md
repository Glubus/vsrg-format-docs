# A Dance of Fire and Ice (ADOFAI)

One-button rhythm game by 7th Beat Games: two planets orbit alternately around the tiles of a path, and the player presses a key each time a planet lands on the next tile. Levels are made in the in-game editor and shared as `.adofai` files (Steam Workshop, community sites).

Category: others. The chart is a path of tiles, each defined by an absolute angle; timing comes from the angle between tiles and the BPM. No columns or lanes.

## Formats
| Folder | File | What |
|---|---|---|
| [adofai/](adofai/README.md) | `.adofai` | JSON level: `settings`, `angleData` (or legacy `pathData`), `actions`, `decorations` |

Same community tooling as [Rhythm Doctor](../rhythm-doctor/README.md) (the RhythmBase library reads both).

## Links
- ADOFAI Expansion docs: https://learn.modrift.org/libs/level-format
- ADOFAI-JS: https://github.com/adofaiex/ADOFAI-JS
- SharpFAI (C#): https://github.com/adofaiex/SharpFAI
- adofaipy (Python): https://github.com/M1n3c4rt/adofaipy
