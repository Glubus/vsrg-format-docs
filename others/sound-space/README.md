# Sound Space / Sound Space Plus / Rhythia

Mouse-aim rhythm game family. Notes appear in a 3 x 3 grid in front of the camera and fly toward the player, who moves the cursor over each note at the right time (no click). Lineage:

1. Sound Space (Roblox game): plain text note lists ([txt](txt/README.md)).
2. Sound Space Plus (SS+, standalone Godot 3 game, repository `Rhythia/sound-space-plus`): adds the `.sspm` package ([sspm](sspm/README.md)), v1 then v2.
3. Rhythia (rename of SS+ by NaN Studios; same `.sspm`): [../rhythia/](../rhythia/README.md).
4. Vulnus (separate game, JSON maps, importable into SS+): [../vulnus/](../vulnus/README.md).

Category: others. Notes sit at free positions (3 x 3 grid, "quantum" notes with float x/y); there are no lanes or columns, and the player aims a cursor instead of pressing keys.

## Formats
| Folder | File | Status |
|---|---|---|
| [sspm/](sspm/README.md) | `.sspm` v1, v2 | binary package: metadata, audio, cover, notes (+ custom markers) |
| [txt/](txt/README.md) | `.txt` (Sound Space Roblox) | comma/pipe text note list |

## Links
- SS+ file type docs: https://basils-garden.github.io/types/
- SS+ source: https://github.com/Rhythia/sound-space-plus
- pysspm-rhythia: https://github.com/David-Jed/pysspm-rhythia
