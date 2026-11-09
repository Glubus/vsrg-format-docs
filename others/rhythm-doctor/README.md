# Rhythm Doctor

One-button rhythm game by 7th Beat Games (Steam release December 2025 per Wikipedia). The player presses one key on the 7th beat of each pulse sequence ("rows" of patients). The built-in level editor (also standalone "RDLE") writes custom levels.

Category: others. Gameplay is a timeline of rows, beats and heavy visual events with no key lanes. A level file is mostly an event list (sound, VFX, rows, decorations, rooms).

## Formats
| Folder | File | What |
|---|---|---|
| [rdlevel/](rdlevel/README.md) | `.rdlevel` | The level: JSON with `settings`, `rows`, `decorations`, `events`, `conditionals`, `bookmarks`, `colorPalette` |

## Links
- Wiki: https://wiki.rhythm.cafe/
- Level editor tutorial: https://rd-editor-docs.github.io/intro
- JSON schema: https://github.com/0f-0b/rd-schema
- RhythmBase (C#): https://github.com/RDCN-Community-Developers/RhythmToolkit
