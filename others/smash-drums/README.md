# Smash Drums

VR drumming game (Quest and PC VR, smashdrums.com). The player smashes approaching drum-colored objects with sticks on a drum kit. Six instruments (kick, snare, cymbal, tom, hi-hat, clapfire); per-note "strength" modes (Crystal, Neutral, Burning, used in Arcade mode). Custom songs ("Indies") are `.indies` ZIP packages. No official format spec exists; the only public description is the documentation of the community chart editor "Smash Drums Editor" (JStillxSKS), which reads and writes them.

Category: **others**: a VR game on a 3D drum kit with stick strokes, treated like the other VR drum games, though the highway has six fixed instrument lanes (judgement call; a 6-column projection is straightforward).

## Formats
| Folder | File | Status |
|---|---|---|
| [indies/](indies/README.md) | `.indies` (ZIP with `meta.json`) | JSON chart in a ZIP; documented through a third-party editor (partial) |

## Links
- Game site: https://smashdrums.com/
- Smash Drums Editor (React/TypeScript/Electron, docs `docs/FILE_FORMATS.md`): https://github.com/JStillxSKS/SmashDrumsEditor
