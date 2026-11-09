# Paradiddle

VR drum simulator by Emre Tanirgan (Steam/PC VR, Quest). The player hits a 3D drum kit with sticks; since the "note highway" update, songs are played like a drum rhythm game (hits scroll toward each drum). Songs are folders of audio plus one `.rlrr` file per difficulty, which can be authored with the open-source Paradiddle Song Creator (`ParadiddleUtilities`) from MIDI, and are shared on ParaDB (paradb.net) and converted from Clone Hero/YARG charts by community tools. The same `.rlrr` format also stores drum kit layouts and live recordings.

Category: **others**: the chart is a list of hits on named 3D instruments (each with its own position in a kit layout) played with VR controllers, not fixed lanes.

## Formats
| Folder | File | Status |
|---|---|---|
| [rlrr/](rlrr/README.md) | `.rlrr` | JSON (schema v0.7): instruments, timed hit events, BPM events, audio and metadata |

## Links
- Official custom song guide: https://paradiddleapp.com/custom-song-guide/
- ParadiddleUtilities (Song Creator, schema `docs/rlrrschema.json`, GPL-3): https://github.com/emretanirgan/ParadiddleUtilities
- ParaDB (community song database): https://paradb.net/instructions
- paradiddleTools (Clone Hero/YARG to RLRR, library manager): https://github.com/rrtrytcg/paradiddleTools
