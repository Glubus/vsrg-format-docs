# Clone Hero and the guitar-game chart ecosystem

Clone Hero (CH, by srylain; free fan game, ~2016+) plays custom charts in the style of Guitar Hero / Rock Band: 5 colored lanes (green, red, yellow, blue, orange; plus open notes) scroll toward a strike line and the player strums or taps frets. It also plays drums (4-lane, 4-lane pro, 5-lane), 6-fret GHL guitar and keys. YARG (Yet Another Rhythm Game, open source) reads the same files. Phase Shift, FoFiX / Frets on Fire, Moonscraper (editor, writes `.chart`), Feedback Editor, Editor on Fire, REAPER (MIDI authoring) and Onyx (converter) belong to the same ecosystem.

Category: **vsrg**. Notes fall along fixed lanes toward a strike line, key count/column based. Beyond the VSRG column model are only guitar-specific mechanics (HOPO/strum/tap forcing, open notes, star power, solos) and secondary tracks (vocals, pro guitar, pro keys).

Folders (all in this game folder unless noted):
- [`chart`](chart/README.md): the Feedback/Moonscraper `.chart` text format (GH1/2 era; what Clone Hero reads most).
- [`mid`](mid/README.md): the Rock Band-style `notes.mid` Standard MIDI chart (also used by GH1/2, Phase Shift, FoFiX, YARG, Rock Band).
- [`ini`](ini/README.md): `song.ini` metadata companion file.
- [`../rock-band/dta`](../rock-band/dta/README.md): Rock Band `songs.dta` database (S-expressions).
- [`../dj-hero/xmk`](../dj-hero/xmk/README.md): DJ Hero `.xmk` (stub).

Dialects: Guitar Hero 1/2 and Rock Band use MIDI (`.mid`) internally. Modern `.mid` charts follow Rock Band's layout, with extensions from Phase Shift (SysEx modifiers, real drums, dance track) and Clone Hero (note-based tap/open markers, 6-fret). Feedback Editor (Turkeyman) invented `.chart`; Guitar Hero Three Control Panel (GHTCP) imported it; Moonscraper and Clone Hero made it the dominant fan format. FoFiX/Frets on Fire reads `song.ini` + `notes.mid` (+ `.chart` in later versions [inference from the TheNathannator docs naming FoFiX as an implementation]). The dialects share the folders above; each format page documents its differences.

Main reference: TheNathannator's GuitarGame_ChartFormats (CC0): https://github.com/TheNathannator/GuitarGame_ChartFormats , rendered at https://thenathannator.github.io/GuitarGame_ChartFormats/ .
