# A Dance of Fire and Ice (ADOFAI)

One-button rhythm game by 7th Beat Games. Two planets (fire and ice) orbit alternately around the tiles of a path; the player presses a key each time a planet should land on the next tile. Levels are authored in the in-game level editor and shared as `.adofai` files (Steam Workshop, community sites).

Category: **others**. The "chart" is a geometric path of tiles (each tile defined by an absolute angle), not notes on lanes; timing derives from the angle between tiles and the BPM. Not column-based, no vertical lane scrolling.

## Formats
| Folder | File | What |
|---|---|---|
| [adofai/](adofai/README.md) | `.adofai` | JSON level: `settings`, `angleData` (or legacy `pathData`), `actions`, `decorations` |

Same developer and community tooling as [Rhythm Doctor](../rhythm-doctor/README.md) (RhythmBase library reads both).

## Links
- ADOFAI Expansion docs: https://learn.modrift.org/libs/level-format
- ADOFAI-JS: https://github.com/adofaiex/ADOFAI-JS
- SharpFAI (C#): https://github.com/adofaiex/SharpFAI
- adofaipy (Python): https://github.com/M1n3c4rt/adofaipy
