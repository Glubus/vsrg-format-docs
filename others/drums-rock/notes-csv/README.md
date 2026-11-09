# Drums Rock custom song (`notes.csv`, `info.csv`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text (CSV)

## Overview
A Drums Rock custom song is a folder with `song.ogg`, `preview.ogg`, `notes.csv` (the chart) and `info.csv` (song information), plus `album.jpg` for the Steam Workshop. One folder holds one difficulty. Implementations: Editor on Fire's `dr.c` (export and import with validation) and the community `drumsrockparser.py` (MIDI to CSV). The official Google Sheets template produces the same CSV.

## Container & encoding
- CSV with a header row, `,` separator, `\n` line endings (EoF writes `\n`). Quotes inside names are doubled `""`. Commas and `+` are not allowed in the song and artist fields of `info.csv` (EoF strips them).
- Folder: `CustomSongs/<SongName>/` (names without spaces recommended for compatibility). Start from the shipped `TemplateSong` folder. Workshop items are copied to `.../Drums Rock/Workshop/<folder>` with a `Metadata.cfg` (below).
- One difficulty per folder: Easy, Medium, Hard, Extreme (EoF also names an "Extreme+" slot; `info.csv` difficulty values 0-3 are accepted on import).

## Structure / metadata
`info.csv` (EoF export, header exactly):
```
Song Name,Author Name,Difficulty,Song Duration in seconds,Song Map
```
Second line: title, artist (`Author Name` is the song artist in EoF), difficulty number (0 Easy, 1 Medium, 2 Hard, 3 Extreme), duration in whole seconds, `Song Map` = `0` as written by EoF [meaning not documented; real community files carry 0 or 2, observed in samples/*_info.csv].

`notes.csv` header (the official/community headers differ slightly in spelling):
```
Time [s],Enemy Type,Aux Color 1,Aux Color 2,No Enemies,interval,Aux
```
(`drumsrockparser.py` writes `Nº Enemies` for the fifth column.)

| Column | Meaning |
|---|---|
| `Time [s]` | hit time in seconds, decimal with 2 digits (EoF `%.2f`; the parser floors to 0.01 s) |
| `Enemy Type` | 1 single drum note, 2 double note (two drums at once), 3 drum roll |
| `Aux Color 1` | first drum 1..6 (colors below) |
| `Aux Color 2` | second drum (equals Color 1 for singles and drum rolls). `drumsrockparser.py` orders the pair so Color 1 <= Color 2; EoF writes the two gems in its lane-scan order (orange, blue, yellow, red, green, purple) |
| `No Enemies` | number of enemies in this row; always 1 in the tools; ignored by EoF import |
| `interval` | for drum rolls: number of hits required (EoF writes the hit count, default 3, max 100); empty otherwise |
| `Aux` | derived from `Aux Color 1`: 1 to 6, 2 to 7, 3 to 5, 4 to 8, 5 to 5, 6 to 8; the role is unknown ("probably position for double notes", per the parser comment), ignored on import |

Drum colors/lanes: 1 yellow = snare, 2 red = kick, 3 orange = high tom, 4 purple = low tom, 5 blue = crash cymbal, 6 green = ride cymbal (EoF release note and `drumsrockparser.py` MIDI mapping). Left-to-right order of the lanes in game differs from the numbering (EoF comment).

`Metadata.cfg` (Workshop packaging written by EoF): `title=<artist> - <title>` and `description=Song:  ... | Artist:  ... | Genre:  ... | Charter:  ... | Difficulty:  <name> | Average BPM:  <n> | Total notes:  <n> | ...`.

## Timing model
Absolute seconds from the start of `song.ogg`, resolution 0.01 s, ascending order. No tempo, beat grid or offset field: tempo changes are baked in (the template requires constant tempo; the MIDI script accumulates MIDI delta times with tempo changes). Drum roll duration is not stored, only the hit count (`interval`).

## Notes
- Single (type 1): one drum. Double (type 2): two different drums at once (EoF limits a chord to two gems and drops a third; chords of more than two drums cannot be encoded). Drum roll (type 3, "fat demon"): one drum, hit `interval` times; start time only.
- EoF import: timestamp times 1000 plus 0.5 ms, length 1 ms; drum rolls become notes named with the hit count.

## Audio & images
`song.ogg`, `preview.ogg` (Ogg Vorbis required), `album.jpg` for the Workshop. Duration is in `info.csv`.

## Versions & variants
- Header spelling differs (`No Enemies` vs `Nº Enemies`). EoF 1.8RC12 and later write/read the files; the Google Sheets template's `enemyData` sheet is the layout's origin.

## Quirks & pitfalls
- Commas and `+` in title/artist break the info line (EoF strips them).
- EoF import rejects a drum roll without `interval`; export defaults to 3 hits.
- `.` is the decimal separator; spreadsheet exports with `,` decimals break parsing.
- Gem numbering does not follow lane order.

## Example
Illustrative, hand-built from the column rules above (not a real chart): a snare hit at 1.50 s, a kick plus high tom at 2.00 s, and a 5-hit crash roll at 3.25 s.
```
Time [s],Enemy Type,Aux Color 1,Aux Color 2,No Enemies,interval,Aux
1.5,1,1,1,1,,6
2,2,2,3,1,,7
3.25,3,5,5,1,5,5
```

## ROX support
Not read by ROX. A decoder could map the 6 drum colors to 6 columns (doubles as chords, drum rolls as a hold or burst) with an assumed constant BPM.

## Parsers & tools
- Editor on Fire (C; export/import, `src/dr.c`): https://github.com/raynebc/editor-on-fire
- drumsrockmidiparser (Python, mido; MIDI notes 60..65 to colors): https://github.com/daredevil28/drumsrockmidiparser
- Official Google Sheets template (Demons March Hard) linked from the instructions page.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Observed: the header uses `Nº Enemies` and `info.csv` `Song Map` is 0 or 2 (the fiche says EoF writes 0). The Steam guide https://steamcommunity.com/sharedfiles/filedetails/?id=3284235843 ("Direct song downloads") links ~140 Google Drive folders and files of community songs; the official template is on https://garage51.es/drumsrock/custom_songs.html; Editor on Fire exports the format.

## Sources
- https://garage51.es/drumsrock/custom_songs.html
- https://steamcommunity.com/sharedfiles/filedetails/?id=2989549859
- https://github.com/raynebc/editor-on-fire (`src/dr.c`, `src/dr.h`)
- https://github.com/daredevil28/drumsrockmidiparser (`drumsrockparser.py`, `README.MD`)
