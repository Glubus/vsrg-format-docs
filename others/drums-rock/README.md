# Drums Rock

VR drumming game by Garage 51 (PC VR, Quest). Colored "enemies" (drum-shaped demons) arrive and the player hits them with drumsticks on a 6-drum kit in front of them; some are double hits or drum rolls that need several hits. Custom songs (one folder per difficulty: Easy, Medium, Hard, Extreme) are placed in `AppData/LocalLow/Garage 51/Drums Rock/CustomSongs` and published on the Steam Workshop. The official workflow is a Google Sheets template that exports `notes.csv`; community tools convert from MIDI and Editor on Fire.

Category: **others**: a VR game with a 3D drum kit (six drums with fixed colors), double hits and drum rolls; categorised with the other VR drum game (Paradiddle) rather than as lane-based vsrg. It is arguably a 6-lane game [judgement call: a ROX 6K decoder is feasible].

## Formats
| Folder | File | Status |
|---|---|---|
| [notes-csv/](notes-csv/README.md) | `notes.csv` + `info.csv` | CSV chart (time in seconds, enemy type, two drum colors) plus song info CSV |

## Links
- Official instructions: https://garage51.es/drumsrock/custom_songs.html
- Steam guide (workflow with Audacity, template and EoF): https://steamcommunity.com/sharedfiles/filedetails/?id=2989549859
- MIDI to CSV script (daredevil28): https://github.com/daredevil28/drumsrockmidiparser
- Editor on Fire (import/export Drums Rock): https://github.com/raynebc/editor-on-fire
