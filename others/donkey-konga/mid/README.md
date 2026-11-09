# Donkey Konga score MIDI (`.mid`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (Standard MIDI File)

## Overview

Donkey Konga 2 song charts ("scores") are plain Standard MIDI files in the game's `files/Score` directory, one per song/difficulty, referenced by the `FILENAME=` field of `/root/Resource/SongInfo.res` (e.g. `FILENAME=01predictable`; a REAPER project name `01predictable_1e.mid` shows the `_1e` single-player Easy suffix). Konga 3 works the same way ("Convert Donkey Konga 2 & 3 charts to TJA"). Audio is a separate GameCube DSP stream (`files/stream/score/NN.dsp`, 01-35; 35 = tutorial). Source: modding guides only.

## Container & encoding

SMF (`MThd`/`MTrk`), loaded from `Score/`. All notes must be on MIDI channel 10 when exporting. Charts reload when a song is entered from song select; changing `SongInfo.res` needs a full emulator restart.

## Structure / metadata

Song list (`SongInfo.res`, text, Shift-JIS): `#<id>` blocks with `SONGNAME`, `FILENAME` (score file prefix), `OFFSET` (delay before the song starts, used for beat timing), `LENGTH` (180 s), `PRICE`, difficulty icons `1E 1H 1X` (single easy/normal/hard), `2E 2H 2X` (co-op), `4` (concert quartet), `B` (battle), `C` (concert share), `RUBY`, `COMMENT`, `GENRE`.

## Timing model

MIDI ticks/tempo map. Beats before the 2 second mark do not appear, so leave a 2 s lead-in; the song audio starts immediately (the editor adds 1-2 s of silence).

## Notes

| Input | MIDI note (REAPER names in the guide) |
|---|---|
| Left bongo | D#4 (note 63) |
| Right bongo | E4 (note 64) |
| Clap | D#2 (note 39) |

Notes for both-bongo, rolls etc.: Unknown.

## Audio & images

`files/stream/score/NN.dsp`: GameCube DSP ADPCM, stereo with a "Cstr" header (made with Audacity-gcdspadpcm + `dkdsp`), 32 000 Hz in official tracks.

## Versions & variants

Only Donkey Konga 2 is documented in the guides (KongaMidToTja says "2 & 3"). The `_1e` suffixes come from a REAPER item name.

## Quirks & pitfalls

Notes before 2 s are dropped; the channel must be 10; `OFFSET` in `SongInfo.res` shifts timing.

## Example

`SongInfo.res` entry from the guide:

```
#1
SONGNAME=Predictable
FILENAME=01predictable
OFFSET=1
LENGTH=180
PRICE=1500
1E=7
1H=8
1X=6
```

## ROX support

Not read.

## Parsers & tools

[kongamidtotja](https://codeberg.org/hapaxant/kongamidtotja) (Donkey Konga 2/3 to TJA, C#), REAPER project templates, Dolphin (extraction), Konga Beat (custom track editor, ResetEra thread).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Konga Beat/Launcher (https://kongabeat.com) say custom tracks are shared on GameBanana; its Donkey Konga 2 game page (https://gamebanana.com/games/23415) listed only one track mod. Official charts are `files/Score/*.mid` in a dumped game image (guide: https://gist.github.com/ImJustSpirit/67626bbc3844703c2cc202e54cffdcc9).

## Sources

- <https://gist.github.com/ImJustSpirit/67626bbc3844703c2cc202e54cffdcc9> (read)
- <https://codeberg.org/hapaxant/kongamidtotja> (search snippet; page content not retrievable)
