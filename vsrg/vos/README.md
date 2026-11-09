# Virtual Orchestra Studio (VOS)

Freeware PC music game by the Korean company HanseulSoft (released 1999; last version 1.0P per a fan site), also played through CanMusic-style simulators and the Chinese "Mania" BMS-simulator platform (1.4.2+ reads `.vos`). Category: **vsrg** - seven piano-like keys with falling note blocks; the player performs the main melody of a MIDI song.

Distinguishing feature: a `.vos` file is essentially MIDI plus a note list, so each key press sends the matching MIDI note in real time (not pre-cut keysounds like BMS).

| Folder | Format | Status |
| --- | --- | --- |
| [`vos/`](vos/README.md) | `.vos` song file (note lists + embedded MIDI) | partial (one parser, VosDroid) |

Links: gpbeta VOS introduction (http://www.gpbeta.com/en/post/intro/vos-intro/), ReVanTis/VosDroid (https://github.com/ReVanTis/VosDroid), original README line: "`.vos`: Virtual Orchestra Studio and CanMusic chart, including 000, 001, 006, 022 versions".
