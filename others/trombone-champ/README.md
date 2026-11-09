# Trombone Champ

Rhythm game by Holy Wow Studios (2022, PC/Switch/consoles). The player moves the mouse (or a stick) vertically to set the trombone pitch and holds a button to blow, following a pitched note ribbon that scrolls right to left. Official tracks are compiled into the game; custom tracks are loaded by the BepInEx plugin TrombLoader (and BaboonAPI) from a folder containing `song.tmb`, `song.ogg` and an optional background.

Category: **others**: notes are horizontal ribbons positioned on a continuous pitch axis (slides and microtonal pitches); there are no fixed lanes or columns.

## Formats
| Folder | File | Status |
|---|---|---|
| [tmb/](tmb/README.md) | `song.tmb` | JSON chart (beat-based, one tempo, notes as `[bar, length, startPitch, deltaPitch, endPitch]` arrays) |

## Links
- TrombLoader (custom track loader, source of the loader-side schema): https://github.com/NyxTheShield/TrombLoader
- TromboneCharter (GDScript editor): https://github.com/towai/TromboneCharter
- Midi2TromboneChamp / TmbToMidi (converters): https://github.com/NyxTheShield/Midi2TromboneChamp, https://github.com/Gloomhonk/TmbToMidi
- Trombone Champ modding wiki: https://trombone.wiki/
