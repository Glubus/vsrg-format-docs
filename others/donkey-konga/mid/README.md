# Donkey Konga score MIDI (`.mid`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (Standard MIDI File)

## Overview

In *Donkey Konga 2* (and 1/3 by analogy; "Convert Donkey Konga 2 & 3 charts to TJA" confirms 2 and 3) the song charts ("scores") are plain **Standard MIDI files** stored in the game's `files/Score` directory, one per song/difficulty, referenced by the `FILENAME=` field of `/root/Resource/SongInfo.res` (e.g. `FILENAME=01predictable`, with variants `…_1e.mid` for single-player Easy as seen in a REAPER project name `01predictable_1e.mid`). Audio is a separate GameCube **DSP** stream (`files/stream/score/NN.dsp`, 01–35; 35 = tutorial). Information comes from modding guides; no deeper binary documentation was opened.

## Container & encoding

SMF (`MThd`/`MTrk`); the guide says **all notes must be on MIDI channel 10** when exporting; the file is loaded from `Score/`. Charts are reloaded when a song is entered from song select; changing `SongInfo.res` needs a full emulator restart.

## Structure / metadata

Song list (`SongInfo.res`, text, Shift-JIS): `#<id>` blocks with `SONGNAME`, `FILENAME` (score file prefix), `OFFSET` (delay before the song starts, used for timing the beats), `LENGTH` (180 s), `PRICE`, difficulty icons `1E 1H 1X` (single easy/normal/hard), `2E 2H 2X` (co-op), `4` (concert quartet), `B` (battle), `C` (concert share), `RUBY`, `COMMENT`, `GENRE`.

## Timing model

MIDI ticks/tempo map. The guide notes that **beats placed before the 2 second mark do not appear** (a 2 s lead-in must be left) and the song audio starts immediately (the editor adds 1–2 s of silence).

## Notes

| Input | MIDI note (REAPER names in the guide) |
|---|---|
| Left bongo | D#4 (note 63) |
| Right bongo | E4 (note 64) |
| Clap | D#2 (note 39) |

Other note numbers for both-bongo, rolls, etc. are not documented in the sources opened.

## Audio & images

`files/stream/score/NN.dsp`: GameCube DSP ADPCM, **stereo with a "Cstr" header** (created with Audacity-gcdspadpcm + `dkdsp`), sample rate 32 000 Hz in official tracks.

## Versions & variants

Only Donkey Konga 2 is documented in the guides opened (the KongaMidToTja tool title says "Donkey Konga 2 & 3 charts"); per-difficulty file suffixes (`_1e`, …) are inferred from a REAPER project item name in the guide.

## Quirks & pitfalls

Notes before 2 s are dropped; channel must be 10; offset in `SongInfo.res` shifts timing.

## Example

Example `SongInfo.res` entry from the guide:

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

Not read by ROX.

## Parsers & tools

[kongamidtotja](https://codeberg.org/hapaxant/kongamidtotja) (Donkey Konga 2/3 → TJA, C#), REAPER project templates, Dolphin (extraction), Konga Beat (custom track editor, ResetEra thread).

## Sources

- <https://gist.github.com/ImJustSpirit/67626bbc3844703c2cc202e54cffdcc9> (read)
- <https://codeberg.org/hapaxant/kongamidtotja> (search snippet; page content not retrievable)
