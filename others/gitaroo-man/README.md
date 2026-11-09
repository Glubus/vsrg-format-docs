# Gitaroo Man

Rhythm action game by iNiS (PS2 2001, as "Gitaroo Man"; PSP 2006 as "Gitaroo Man Lives!"). In "attack" phases the player follows a curved trace line with the analog stick while pressing a button on phrase bars; in "guard" phases the player presses the face button shown by a mark arriving from a direction; each stage is a series of sections whose chart files decide the flow (energy conditions branch between sections). Chart data of a stage lives in a `.CHC` file. The community tool "Gitaroo Man File Reader" (sonicfind, C++) reads, edits and writes CHC files and converts them to Clone Hero `.chart` and to TAS files; "gitarootools" (boringhexi, Python) handles other game files.

Category: **others**: trace lines with continuous angle/curve and phrase bars (stick-steered), guard marks from four directions; not column-based.

## Formats
| Folder | File | Status |
|---|---|---|
| [chc/](chc/README.md) | `.CHC` | reverse-engineered binary chart/stage file (partial: field layout complete from the tool's reader/writer, some values junk or unknown) |

## Links
- Gitaroo Man File Reader (C++): https://github.com/sonicfind/Gitaroo-Man-File-Reader
- gitarootools (Python): https://github.com/boringhexi/gitarootools
- TCRF note that chart files contain RAM garbage: https://tcrf.net/Gitaroo_Man/Development_Text (not opened)
