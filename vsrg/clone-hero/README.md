# Clone Hero and the guitar-game chart ecosystem

Clone Hero (CH, by srylain; free fan game, ~2016+) plays custom charts in the style of Guitar Hero / Rock Band: 5 colored lanes (green, red, yellow, blue, orange; plus open notes) scroll toward a strike line; the player strums or taps frets. It also plays drums (4-lane, 4-lane pro, 5-lane), 6-fret GHL guitar and keys. YARG (Yet Another Rhythm Game, open source) reads the same files; Phase Shift, FoFiX / Frets on Fire, Moonscraper (editor, writes `.chart`), Feedback Editor, Editor on Fire, REAPER (MIDI authoring) and Onyx (converter) belong to the same ecosystem.

Category: **vsrg**. Notes fall along fixed lanes toward a strike line, key count/column based; the only things beyond the VSRG column model are guitar-specific mechanics (HOPO/strum/tap forcing, open notes, star power, solos) and secondary tracks (vocals, pro guitar, pro keys).

Folders (all in this game folder unless noted):
- [`chart`](chart/README.md): the Feedback/Moonscraper `.chart` text format (GH1/2 era; what Clone Hero reads most).
- [`mid`](mid/README.md): the Rock Band-style `notes.mid` Standard MIDI chart (also used by GH1/2, Phase Shift, FoFiX, YARG, Rock Band).
- [`ini`](ini/README.md): `song.ini` metadata companion file.
- [`sng`](sng/README.md): `.sng` single-file package.
- [`../rock-band/dta`](../rock-band/dta/README.md): Rock Band `songs.dta` database (S-expressions).
- [`../yarg/yargsong`](../yarg/yargsong/README.md): YARG `.yargsong` package (stub).
- [`../dj-hero/xmk`](../dj-hero/xmk/README.md): DJ Hero `.xmk` (stub).

How the game dialects relate: Guitar Hero 1/2 and Rock Band use MIDI (`.mid`) internally; Rock Band's layout is what modern `.mid` charts follow, with extensions from Phase Shift (SysEx modifiers, real drums, dance track) and Clone Hero (note-based tap/open markers, 6-fret). Feedback Editor (Turkeyman) invented `.chart`; Guitar Hero Three Control Panel (GHTCP) imported it; Moonscraper and Clone Hero made it the dominant fan format. FoFiX/Frets on Fire reads `song.ini` + `notes.mid` (+ `.chart` in later versions [inference from the TheNathannator docs naming FoFiX as an implementation]). These share the folders above; per-dialect differences are documented inside each format page (a separate folder per game was not needed).

Main reference: TheNathannator's GuitarGame_ChartFormats (CC0): https://github.com/TheNathannator/GuitarGame_ChartFormats , rendered at https://thenathannator.github.io/GuitarGame_ChartFormats/ .
