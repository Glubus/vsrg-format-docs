# Paradiddle

VR drum simulator by Emre Tanirgan (Steam/PC VR, Quest). The player hits a 3D drum kit with sticks; since the "note highway" update, hits scroll toward each drum. Songs are folders of audio plus one `.rlrr` per difficulty, authored from MIDI with the open-source Song Creator (`ParadiddleUtilities`), shared on ParaDB (paradb.net) and converted from Clone Hero/YARG charts by community tools. The same `.rlrr` also stores kit layouts and live recordings.

Category: others (hits on named 3D instruments, each with its own kit position, played with VR controllers; no fixed lanes).

## Formats
| Folder | File | Status |
|---|---|---|
| [rlrr/](rlrr/README.md) | `.rlrr` | JSON (schema v0.7): instruments, timed hit events, BPM events, audio and metadata |

## Links
- Official custom song guide: https://paradiddleapp.com/custom-song-guide/
- ParadiddleUtilities (Song Creator, schema `docs/rlrrschema.json`, GPL-3): https://github.com/emretanirgan/ParadiddleUtilities
- ParaDB (community song database): https://paradb.net/instructions
- paradiddleTools (Clone Hero/YARG to RLRR, library manager): https://github.com/rrtrytcg/paradiddleTools
