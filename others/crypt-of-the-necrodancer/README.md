# Crypt of the NecroDancer

Rhythm roguelike by Brace Yourself Games (2015, PC and consoles). The player moves and acts on the beat of the music while exploring dungeons; the beat is a metronome-like stream of beat events (the "beat bars" at the bottom). With the Custom Music feature the player replaces a zone's soundtrack with their own MP3/OGG file; the game then needs a list of beat positions for that file, which it generates automatically (essentia-based beat tracker) or from manual tapping.

Category: **others**: there are no notes or lanes; the "chart" is just the beat grid of a song, and gameplay happens on a 2D tile map.

## Formats
| Folder | File | Status |
|---|---|---|
| [beatmap-txt/](beatmap-txt/README.md) | `<song file name>.txt` in `data/custom_music/` | plain-text list of beat positions (seconds in current builds; milliseconds in a 2017 forum sample) |

## Links
- Official FAQ (Custom Music section): https://braceyourselfgames.com/crypt-of-the-necrodancer/faq/
- necrodancer-custom-music (CLI importing music, writes beatmaps): https://github.com/Supinic/necrodancer-custom-music
- toofz-necrodancer-core (.NET parser for `necrodancer.xml`, replays, saves): https://github.com/leonard-thieu/toofz-necrodancer-core
