# BanG! Simulator chart (`.txt`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes; Prism's addition) · Category: vsrg · Encoding: text

## Overview
The `.txt` "BanG Dream!" chart of the original format list is the line-based text chart read by **BanG! Simulator** (thtl1999, extended by loader3229 to v2.0), a desktop simulator for BanG Dream! Girls Band Party. Charts are obtained and converted from official/Bestdori sources with BanGConverter. rmstZ also reads/writes a `.txt` BanG Dream style (it lists it as supported). The file is described in the simulator's `Bang info.txt`.

## Container & encoding
Plain text, one entry per line, fields separated by `/`. Score file name: `[musicnamecode]ex.txt`; special score: `xxxsp.txt`; music `bgm[musicnamecode].ogg` (also mp3 per changelog). Encoding: Unknown (ASCII numerics).

## Structure / metadata
Layout:
```
<note offset>       (line 1, int)
<song bpm>          (line 2, number)
<beat>/<type>/<lane>   (lines 3..)
```
Each note line is `beat/notetype/lanenumber`; `beat` may be fractional (`8.5`). Lane is 1-based in the example (`8/1/3` = normal note at beat 8 on the 3rd lane).

Note types: 0 music start (`0/0/0` = music starts at beat 0); 1 normal; 2 flick; 3/4/5 slide A start/among/end; 6/7/8 slide B start/among/end; 10 fever single; 11 skill; 12 slide A end flick; 13 slide B end flick; 20 BPM change (`5/20/160` = BPM 160 at beat 5); 21 long note start, 25 long note end, 26 long note end with flick; v1.30: 31 long start with skill, 32 long end with skill, 33/34 slide A start/end with skill, 35/36 slide B start/end with skill; v2.00: 41/42 slide A/B among hidden; 51-57 directional flick left width 1..7; 61-67 directional flick right width 1..7.

## Timing model
Beats are real numbers (`beat`), one global BPM (line 2) plus type-20 lines for changes; `note offset` in the first line (default 46 in the simulator, ms [inference: unit of the setting.ini Offset is not stated]). Notes are time-based in v2.0 ("note movement now based on time instead of tick").

## Notes
Taps (1), flicks (2), long notes (21 ... 25/26), slides in two interleaved chains A and B (3-5 / 6-8) with "among" nodes, skill/fever variants, hidden slide nodes, directional flicks with width. Notes at the same time should be sequentially ordered. Beat not divisible by 0.5 renders gray (display only).

## Audio & images
`bgm<code>.ogg/mp3` beside the chart; resources from BandoriDatabase/bangdream-data-viewer.

## Versions & variants
beta .. 1.11 (original), 1.20 / 1.30 / 2.0 by loader3229 (new note types for the JP server v5.0); Bestdori v1/v2 JSON are separate ([bestdori-json](../bestdori-json/README.md)).

## Quirks & pitfalls
Lane numbering 1-based; the official game's own score files are converted by tools (broken BMS notes exist); first line offsets.

## Example
From `Bang info.txt` (BanG! Simulator):
```
46
131
0/0/0
8/1/3
8.5/1/6
8.75/1/6
9.25/1/1
```

## ROX support
Read by ROX since Prism's addition of `rox::formats::bandori` (decode only): `SimulatorDecoder` (`decode`, `decode_with_report` giving a `BandoriReport`, `decode_with_title`, `decode_file`; `DetectedFormat::BangSimulator`). ONE chart per file, always **7 columns**, lane 1..7 -> column 0..6 (outside 1..7 or not whole: dropped, counted). Types: 1 Tap; 2, 10, 11 and 51..57 / 61..67 Taps whose flick, fever (`charge`), skill and directional flags are counted and dropped; 21/31 .. 25/26/32 a long note paired by its LANE (`BanGConverter`'s `out/bestdori.js`), 3/33 .. 4/41 .. 5/12/34 slide chain A, 6/35 .. 7/42 .. 8/13/36 chain B, each ONE Hold from its first note to its last on the first note's lane (the `among` notes are dropped and counted); 71..77 (not in the notes above: `BanGConverter` writes them for a third overlapping slide, as `beat/type/number/lane`) the same by their number; 20 a BPM change (the BPM is in the lane field); 0 `0/0/0` the beat at which the music starts (the origin of the times; a note before it is dropped and counted); other types are counted. Lines are read sorted by beat (file order at one beat). The first line (the note offset, 46 in every file `BanGConverter` writes) is read and NOT applied: no unit (milliseconds is an inference) and no sign in the notes. The line 2 BPM is the tempo from beat 0; no BPM events after it is a constant tempo.

**Detection**: ROX never claims `.txt` by extension (`detect` says nothing of it); `auto_decode*` reads a `.txt` as a score only when its content is one (`rox::formats::looks_like_simulator`: a number, a positive number, then nothing but `beat/type/lane` lines over the first 4 KiB). The music is `bgm<code>.ogg|mp3` next to a score named `<code>ex.txt` / `<code>sp.txt` (this fiche): Prism plays the audio file with the chart's name (`game_core::dance_audio`), else that `bgm<code>` file, else the first of the folder, else silence. Read by Prism (`docs/game.md` "BanG Dream"), playable on the 7K layout. Sources read: the simulator's `Bang info.txt` (no licence file: facts only), `BanGConverter` (MIT); nothing copied, no real score was decoded.

## Parsers & tools
BanG! Simulator (Python): https://github.com/thtl1999/BanG-simulator · BanGConverter (JS): https://github.com/loader3229/BanGConverter · rmstZ.

## Sources
https://github.com/thtl1999/BanG-simulator (Bang info.txt) · https://github.com/loader3229/BanGConverter · https://lrfasd.github.io/rmstZ/WHATSNEW.html
