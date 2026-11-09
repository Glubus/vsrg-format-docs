# Drums Rock

VR drumming game by Garage 51 (PC VR, Quest). Drum-shaped demons arrive and the player hits them with sticks on a 6-drum kit; some are double hits or drum rolls. Custom songs (one folder per difficulty: Easy, Medium, Hard, Extreme) go in `AppData/LocalLow/Garage 51/Drums Rock/CustomSongs` and on the Steam Workshop. The official workflow is a Google Sheets template exporting `notes.csv`; community tools convert from MIDI and Editor on Fire.

Category: others (VR game with a 3D drum kit of six fixed-color drums, doubles and drum rolls; grouped with Paradiddle). It is arguably a 6-lane game [judgement call: a ROX 6K decoder is feasible].

## Formats
| Folder | File | Status |
|---|---|---|
| [notes-csv/](notes-csv/README.md) | `notes.csv` + `info.csv` | CSV chart (time in seconds, enemy type, two drum colors) plus song info CSV |

## Links
- Official instructions: https://garage51.es/drumsrock/custom_songs.html
- Steam guide (workflow with Audacity, template and EoF): https://steamcommunity.com/sharedfiles/filedetails/?id=2989549859
- MIDI to CSV script (daredevil28): https://github.com/daredevil28/drumsrockmidiparser
- Editor on Fire (import/export Drums Rock): https://github.com/raynebc/editor-on-fire
