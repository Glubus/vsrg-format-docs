# Be-Music Source (`.bms`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice, charset not specified)

Reference page for the whole BMS text format; [`../bme`](../bme/README.md), [`../bml`](../bml/README.md) and [`../pms`](../pms/README.md) cover only what their extension adds. The JSON dialect is in [`../bmson`](../bmson/README.md).

## Overview

BMS ("Be-Music Source") is a plain-text chart format devised by Urao Yane (with NBK) in 1998 for BM98, a PC simulator of Konami's beatmania (draft 1998-05-04, specification 1998-11-26; free to use per the `hitkey` memo). A chart is a timeline of references to `#WAVxx` keysounds (one file per base-36 id); there is no single audio track. A song is a folder with chart(s), keysounds, optional BGA media, banner and stage image. Extensions `.bms`, `.bme`, `.bml`, `.pms` share the syntax and hint at the channel set; `.bmson` is a JSON dialect. Players: Lunatic Rave 2 (LR2), beatoraja, Bemuse, Raindrop, ruv-it!, uBMplay, Angolmois, Project OutFox/StepMania (`be-mu`/`po-mu`). Editors: BMSE, iBMSC, BMS Creator (BMSC), GDA Creator. Samples: [`samples/`](samples/) (7K chart with channels 18/19 inside a `.bms`, empty `#STAGEFILE`, one MP3 as BGM on `#WAV03`) and [`../bme/samples/`](../bme/samples/).

## Container & encoding

- One chart per file; a song folder holds one file per difficulty/play style. No archive, compression or binary part.
- Lines starting with `#` are commands; the rest are comments (the sample uses `*---------------------- HEADER FIELD`). Command names are case-insensitive; some implementations are case-sensitive for values (e.g. `#LNOBJ XX`).
- Header sentences `#NAME value` and channel sentences `#mmmCC:data`. Order is free ("BMS is compiled at runtime"): headers can follow their use. Control flow (`#RANDOM` ...) is parsed first.
- Duplicate header: the one nearest EOF wins (memo exceptions: `#ExtChr`, `#STP`, `#WAVCMD`, `#OPTION`, control flow; not guaranteed for `#SUBTITLE`, `#SUBARTIST`, `#COMMENT`, `#LNOBJ`). Duplicate channel lines in one measure merge (non-`00` objects of the later line override; `00` never overwrites), except channel `01` (several independent BGM lines), `02` (last wins) and `A6` (`#CHANGEOPTION`). Memo example: `#00113:11111111` + `#00113:0022332255224400` + `#00113:0066` merges to `1122332266224400`. Half of the implementations do not merge.
- Line endings: CRLF, CR or LF, even mixed; the last line may lack a newline.
- Delimiter: `#NAME` + one space (many parsers accept tabs, several blanks, indent) + value; `#` + 3-digit measure + 2-char channel + `:` + data. bms-js trims each line and uses `^#(\w+)(?:\s+(\S.*))?$` for headers and `^#(\d\d\d)(\S\S):(\S*)$` for channels.
- Charset: unspecified. Most Japanese files are Shift_JIS (CP932), Korean ones often EUC-KR; UTF-8 (with or without BOM) and UTF-16 exist (ruv-it!, iBMSC, IIDXv, HDX, Sonorous, BGAEncAdv, beatoraja support Unicode). The obsolete ruv-it! `#CHARSET [EUC-KR|SHIFT-JIS|UTF-8]` header existed. bms-js has a "Reader" stage that detects the charset; ruvit uses the BOM, else guesses EUC-KR vs Shift_JIS from lead-byte frequency. Pitfalls: yen/won sign, wave dash, `~` mapping. Use ASCII for file names; the Shift_JIS sample `samples/�l�g����.bms` has an undecodable name in this checkout.
- Chart file references (`#WAVxx`, `#BMPxx`, ...) are relative to the chart folder, with `\` and `/` mixed. The audio extension is often wrong, so players try alternatives (`foo.wav` to `foo.ogg`, `foo.flac`, ...).

## Structure / metadata

Syntax summary:

```
#TITLE  some title                  header sentence
#WAV01  kick.wav                    definition of key sound id 01
#00111:01000100                     channel sentence: measure 001, channel 11 (1P key 1), 4 slots of 2 chars
```

### Header commands

Notes give the origin program (`hitkey` memo); "common" = read by almost all modern players.

| Command | Meaning | Notes |
| --- | --- | --- |
| `#PLAYER n` | Play mode, 1..4. | `1` single (default), `2` couple (1P+2P, two gauges), `3` double (1P+2P played by one player), `4` battle. Origin BM98. Modern players (LR2, nanasi, ruvit, pomu2, beatoraja) ignore it and guess the mode from the channels used. PMS recommends `#PLAYER 3`. |
| `#GENRE s` | Genre text | BM98. |
| `#TITLE s` | Title | BM98. Many files append the difficulty, e.g. `[HYPER]`; "implicit subtitle" heuristics exist (text in brackets or after `-`) for bemaniaDX/DDR. |
| `#SUBTITLE s` | Explicit subtitle | nanasi. Sonorous allows several. |
| `#ARTIST s` | Artist | BM98. |
| `#SUBARTIST s` | Helpers (slicer, movie maker, chart author) | LR. May repeat. |
| `#MAKER s` | Author of the data | bemaniaDX. |
| `#COMMENT "s"` | Text on selection screen | pomu. May repeat. |
| `#BPM n` | Initial BPM | BM98. Default 130 per spec, but implementations differ (nanasi 150, nazo/BMSC/BMSE/iBMSC 120, fgt# / pomu2 / o2play 0, LR2 hangs on its BPM display). A decimal value is accepted by almost every modern player. Always write it. |
| `#BPMxx n` / `#EXBPMxx n` | Real-number BPM table used by channel `08` | bemaniaDX; `#EXBPM` is nanasi's alias to dodge a BMSC bug. Index `01`..`ZZ` in modern players (older: `01`-`99`, `01`-`FF`). Negative value = reverse scroll in LR2, bemaniaDX, ruvit, Angolmois... (undefined by the spec). |
| `#BASEBPM n` | BPM used as reference for the automatic hi-speed | LR. |
| `#STOPxx n` | STOP table used by channel `09` | DDR. `n` is in 1/192 of a whole note in 4/4 (see Timing). |
| `#STP xxx.yyy zzzz` | Stop given by measure position and duration in ms | bemaniaDX, Angolmois, Sonorous, bms-js. |
| `#PLAYLEVEL n` | Declared level (integer, can be huge, e.g. `5000` in the repo sample) | BM98. nanasi allows a string. |
| `#DIFFICULTY n` | 1 Beginner, 2 Normal, 3 Hyper, 4 Another, 5 Insane | nanasi; read by LR2, iBMSC 3, Sonorous, beatoraja. |
| `#RANK n` | Judgment level: 0 VERY HARD, 1 HARD, 2 NORMAL, 3 EASY | BM98. LR2 windows: +-8 / 15 / 18 / 21 ms. nanasi adds `4` (VERY EASY); beatoraja documents `#RANK 4` as VERY EASY = 1.25x EASY. Default when omitted depends on the implementation (BM98 etc. 2, BMSE/iBMSC 3, nBMplay 0). |
| `#DEFEXRANK n` | Judgment width as a percentage of NORMAL (100 = NORMAL) | nanasi; beatoraja says it overrides `#RANK` (since 0.7.3 reference = NORMAL). |
| `#EXRANKxx n` | Table for channel `A0` (judge change during the song) | nanasi. |
| `#TOTAL n` | Gauge increase when all notes are hit perfectly | BM98. Omitted = implementation default (`200+NOTES` in BM98, 160 LR2/ruvit, 350 nanasi...). IIDX gauge formula quoted in the memo: `7.605*NOTES/(0.01*NOTES+6.5)`. Decimals accepted. Negative = gauge decreases in some players. |
| `#VOLWAV n` | Master volume of the keysounds (percent) | BM98. beatoraja: max 100. |
| `#LNTYPE n` | Long-note notation: `1` (default) channels 51-69 RDM type, `2` MGQ type (obsolete) | RDM. See "Notes". |
| `#LNOBJ xx` | Id of a keysound that marks the end of a long note | RDM 1.61. See "Notes". |
| `#LNMODE n` | beatoraja extension: 1 LN, 2 CN, 3 HCN (forces the long-note type) | beatoraja. |
| `#WAVxx file` | Keysound table, `xx` = base-36 id `01`..`ZZ` (`00` = landmine sound) | See Audio. |
| `#BMPxx file` | Image/video table, `00`..`ZZ` | See Audio. |
| `#EXBMPxx a,r,g,b file`, `#BGAxx`, `#@BGAxx`, `#POORBGA`, `#SWBGAxx`, `#ARGBxx`, `#VIDEOFILE`, `#VIDEOf/s`, `#MOVIE`, `#SEEKxx`, `#ExtChr` | BGA cropping / transparency / video extensions | bemaniaDX, BM98de, nanasi, DXEmu, BM98 (`#ExtChr`). Exact argument lists are in the memo. |
| `#STAGEFILE file` | Splash image (640x480) shown while loading | BM98k; very common. May be empty (as in the sample). |
| `#BACKBMP file` | Background image of the play screen | DDR; used by LR2 skins. |
| `#BANNER file` | Banner for the song list | nanasi; common. |
| `#PREVIEW file` | Preview audio in the song selection screen | beatoraja (if absent, it looks for `preview*.wav/ogg` in the folder). |
| `#SCROLLxx n` + channel `SC`, `#SPEEDxx n` + channel `SP` | Scroll-speed multiplier segments (negative = reverse) | Bemuse extension (from StepMania 5 SPEED/SCROLL); beatoraja implements `#SCROLLxx` / `#nnnSC:` too, Raindrop planned them. |
| `#WAVCMD`, `#OPTION`, `#CHANGEOPTIONxx`, `#OCT/FP`, `#CHARFILE`, `#TEXTxx`, `#SONGxx`, `#CDDA`, `#MIDIFILE`, `#PATH_WAV`, `#MATERIALSWAV/BMP`, `#DIVIDEPROP`, `#CHARSET`, `%URL`, `%EMAIL` | Player- or editor-specific; each documented in the memo. | Rarely needed by a chart reader. |
| `#EXT #mmmcc:...` | Bemuse "extension line" prefix (`#EXT` is removed from bms-rs for lack of specification) | |

### Control flow

Evaluated before anything else (pre-process the file).

- `#RANDOM n` draws an integer in `1..n`; `#IF k` ... `#ENDIF` keeps its content if the draw equals `k`. Optional: `#ELSEIF k`, `#ELSE` (IIDXv, nanasi), `#ENDRANDOM` (nanasi, required there for nesting), `#SETRANDOM n` (pomu2). `#SWITCH n` / `#SETSWITCH n`, `#CASE k`, `#SKIP`, `#DEF`, `#ENDSW` (nanasi) are the switch equivalent.
- Content outside `#IF` but inside `#RANDOM` is kept by BM98, ruvit, uBMplay and dropped by LR2, nazo, BMSE.
- Many players nest one level only (LR2, ruvit, bemaniaDX, ...); BM98, nanasi, pomu2, beatoraja-style engines nest. Headers (`#TITLE`, `#WAV`, `#BPMxx`) can be inside `#IF`.
- Typos accepted by some: `#RONDAM`, `#END IF`, `#random5`. IIDXv/HDX default to `1` without a preceding `#RANDOM`.
- bms-js keeps a stack: `#RANDOM n` pushes `rng(n)`, `#IF k` pushes `skip = (top != k)`, `#ENDIF` pops; lines are dropped while skip is set. Reproducible output needs a fixed seed.

### Main data field

`#mmmCC:ZZZZ...`

- `mmm`: measure `000`..`999` (`#000` allowed by almost every modern player; LR2 inserts an empty measure before `#000` when it holds visible notes).
- `CC`: channel, 2 base-36 characters.
- `ZZ...`: even-length string of 2-character object ids; the measure splits into as many equal slots as pairs; `00` is a rest. Ids are base 36 (`0-9A-Z`; 1296 values, 1295 usable) in modern files, limited base-36 (`[0-9A-F][0-9A-Z]`, 576) or hexadecimal (256) in older ones. Some old players are case-sensitive (`#LNOBJ`: use uppercase; nanasi and fgt++ do not match lowercase ids). Channel `03` pairs are hexadecimal (`01`..`FF`); channels `0B`-`0E`, `97`, `98` also carry `01`..`FF`.
- Invalid data (odd length, non-alphanumerics, 500 000-character lines, trailing `;comment`, multi-byte chars) is unspecified; LR2/nazo/uBMplay try to recover.

### Channel table

From the `hitkey` channel mapping table (origin in the last column). `xx` stands for a base-36 id.

| Channel | Meaning | Value | Origin |
| --- | --- | --- | --- |
| `01` | BGM (autoplay keysound). Several lines per measure are allowed and not merged. | `#WAVxx` | BM98 |
| `02` | Measure length multiplier, for that measure only. `1` = 4/4, `0.75` = 3/4, `2` = 8/4. Real number (decimal point, not a base-36 pair). Last line wins. A length of 0 is used by some "kusofumen"; bms-rs treats it as a zero-length measure and keeps the objects at the same position. | float | BM98 |
| `03` | BPM change, integer `01..FF` hex (1..255). | hex pair | BM98 |
| `04` | BGA base layer | `#BMPxx` | BM98 |
| `05` | Extended object (`#ExtChr`, BM98 only) / SEEK object (LR) | | BM98 / LR |
| `06` | BGA "poor" layer shown on a miss | `#BMPxx` | BM98 |
| `07` | BGA layer, black pixels (RGB 000000) are transparent, over channel 04 | `#BMPxx` | BM98k |
| `08` | Extended BPM change | `#BPMxx` (`#EXBPMxx`) | bemaniaDX |
| `09` | STOP | `#STOPxx` | DDR |
| `0A` | BGA layer 2 | `#BMPxx` | nanasi |
| `0B`-`0E` | Opacity of BGA base / layer / layer 2 / poor | `01..FF` | nanasi |
| `11`-`19` (`11`..`1Z`) | 1P visible notes (BM98: 11-17; FlashTerminal: 18-19; MGQ: 1A-1F; pomu: 1G-1Z) | `#WAVxx` | |
| `21`-`29` (`21`..`2Z`) | 2P visible notes | `#WAVxx` | |
| `31`-`39` (`31`..`3Z`) | 1P invisible objects (not drawn, not judged; sound on key press only) | `#WAVxx` | |
| `41`-`49` (`41`..`4Z`) | 2P invisible objects | `#WAVxx` | |
| `51`-`59` (`51`..`5Z`) | 1P long notes (RDM notation, `#LNTYPE 1`) | `#WAVxx` | MGQ/pomu |
| `61`-`69` (`61`..`6Z`) | 2P long notes | `#WAVxx` | MGQ/pomu |
| `70`-`96` | reserved | | |
| `97` / `98` | BGM volume / KEY volume change (`01..FF`) | | forgetalia |
| `99` | Text change (`#TEXTxx`) | | pomu |
| `A0` | Judge rank change | `#EXRANKxx` | nanasi |
| `A1`-`A4` | ARGB of BGA base / layer / layer 2 / poor | `#ARGBxx` | nanasi |
| `A5` | BGA key-bound (switch on key press) | `#SWBGAxx` | nanasi |
| `A6` | Option change (multi-line) | `#CHANGEOPTIONxx` | nanasi |
| `D1`-`D9` | 1P landmines | base-36 pair = damage; gauge loses value/2; `ZZ` = instant fail; sound = `#WAV00` | nanasi |
| `E1`-`E9` | 2P landmines | same | nanasi |
| `SC`, `SP` | scroll / speed segments | `#SCROLLxx` / `#SPEEDxx` | Bemuse (base-36 channel names) |

Channel sets by format (`hitkey` KEYMAP table; playable lanes only; "16" is the scratch):

| Layout | Lanes in order (left to right) | Channels |
| --- | --- | --- |
| BMS 5K (+scratch) | scratch, 1..5 (free zone `17`) | 16 11 12 13 14 15 (17) ; 2P: 21..25, 26 (27) |
| BME 7K+scr | scratch, 1..7 | 16 11 12 13 14 15 18 19 ; 2P: 21 22 23 24 25 28 29 26 |
| Project2DX (pseudo 7K, historical) | scratch, 1..7 | 16 11 12 13 14 15 21 22 |
| PMS 9 buttons (standard) | 1..9 | 11 12 13 14 15 22 23 24 25 |
| PMS BME-type 9 buttons | 1..9 | 11 12 13 14 15 18 19 16 17 |
| PMS 18 (BME-DP) | 1P 1..9 + 2P 1..9 | 11 12 13 14 15 18 19 16 17 / 21 22 23 24 25 28 29 26 27 |
| nanasi/Angolmois foot pedal | extra lane on `17` (and `27`) | |
| DDR (Delight Delight Reduplication) 4/8 | left, down, up, right | 11 13 15 16 (+21 23 25 26) |

Key mode is inferred from used channels, since `#PLAYER` is ignored: a chart using only 16 can be 5K, 7K, 10K, 14K or PMS (use the extension and the presence of 18/19/21-29). IIDX-style 7K+scr is the commonly assumed layout (bms-js defines `IIDX_P1 = {11:1, 12:2, 13:3, 14:4, 15:5, 18:6, 19:7, 16:SC}`); Raindrop translates BME (`18`,`19`) to keys 6,7 and PMS with a dedicated mapper.

## Timing model

- Position = (measure, fraction). A measure is 4 beats times `len(m)` (channel `02`, default 1). Slot `i` of `n` in measure `m`: `beat = sum_{k<m}(4*len(k)) + (i/n) * 4*len(m)` (bms-js `chart.measureToBeat`, Raindrop `BeatForObj`). No tick resolution: 10 pairs place objects at 1/10 of the measure.
- BPM: initial `#BPM`; `03` sets an integer BPM (hex 1..255); `08` looks up `#BPMxx` / `#EXBPMxx` (real, above 255, even negative). `03` and `08` at one position: implementation dependent (BMSE/iBMSC warn). bms-js: `parseInt(value,16)` for `03`, `+headers['bpm'+value]` for `08`; initial BPM falls back to 60 when unparsable.
- STOP: `09` + `#STOPxx n`; 1 = 1/192 whole note in 4/4 = 1/48 beat, independent of `02`. Seconds = `n/48 * 60/BPM` at the BPM in effect. bms-js `stopBeats = value/48`, Raindrop `Stops[ev]/48`. Order at one position: notes, BPM change, STOP (BPM applies before the duration). Negative STOP: skipped by many, applied as -1 or 0 by others. Decimal STOP: truncated by LR2/Angolmois, kept by ruvit/nanasi/IIDXv.
- `#STP xxx.yyy zzzz` (bemaniaDX): stop at measure position `xxx.yyy` for duration `zzzz`; units not verified (memo section `#STP`). Read by bms-js `Timing`, Angolmois, Sonorous.
- Seconds (bms-js `Timing.fromBMSChart`): collect `bpm` and `stop` actions by beat, sort by beat then (`bpm` before `stop`), `seconds += (beat - lastBeat) * 60 / bpm`, at a stop add `stopBeats * 60 / bpm`. A note at the stop position is hit at the pause start.
- Offset: none; keysounds sit on the timeline. A single BGM file (e.g. `#WAV03 song.mp3` at `#00101:...03` in the repo sample) must be placed at the right time.
- Scroll speed: Bemuse `#SCROLLxx`/`#SPEEDxx`, beatoraja `#SCROLLxx`/`#nnnSC:` (multiplier, negative = reverse); negative BPM/STOP are older hacks.
- Measure range: `#000`..`#999`; some old players fewer (BMSV 511, bemaniaDX 399, GALLI 399, BGAEnc 249).

## Notes

- Visible note: any object on `1x`/`2x`; its id is the keysound. Place the same keysound on channel `01` to play it as BGM too.
- Invisible object (`3x`/`4x`): never judged or scored; a key press near it plays its keysound (ad-libs, easter eggs, keysound replacement under a visible note).
- Landmine (`Dx`/`Ex`): when the key is held at judgment the gauge drops by `value/2` percent (`ZZ` fails the stage); sound `#WAV00`.
- Long notes:
  1. `#LNTYPE 1` (RDM type #1, default; `51`..`69` for 1P, `61`..`6Z` for 2P): objects alternate start, end, start, end ...; the start sound plays and the end sound is ignored (HDX/IIDXv/TechnicalGroove play the end id as key-up sound when it differs). Memo example: `#00151:00220000` + `#06451:000000000033` is one LN from measure 001 to 064.
  2. `#LNOBJ xx` (RDM type #2, since RDM 1.61): id `xx` is a terminator; on a playable channel (`11`..`29`) it makes the previous visible object of that channel the LN start, and is not a note. Players without `#LNOBJ` show it as a note (`.bml` was proposed as a filter). Use uppercase (nanasi/fgt++ bug). RDM/ruvit play the terminator keysound as BGM, most do not. TechnicalGroove allows several `#LNOBJ`.
  3. `#LNTYPE 2` (MGQ type, channels `51`..`8C`, obsolete): a run of non-`00` objects in one lane; it ends at the first `00` (runs continue across bar lines if the previous measure's last slot and the next measure's first are both non-`00`).
  Priority is unspecified when RDM channels and `#LNOBJ` mix. An LN counts as 1 note in most players, 2 in others. Per the memo, only nanasi, HDX and Angolmois judge the LN end. beatoraja `#LNMODE`: 1 = LN, 2 = CN, 3 = HCN (labels only in its wiki; charge note, hell charge note). The bmson field `t` ([`../bmson`](../bmson/README.md)) is the equivalent.
- Scratch/free zone: `#xxx16` is the turntable; `#xxx17` (BM98 free zone, one quarter note long, extended by a new object before it closes) is the foot pedal in nanasi/Angolmois or a 9th key (PMS BME-type).
- Any number of channels can hold an object at one position; one channel holds one object per slot. Counting notes is the player's job.

## Audio & images

- `#WAVxx file`: `xx` base-36 `01`..`ZZ` (1295 ids; `00` is for landmines). WAV (PCM 8/16/24, IEEE float exist), OGG Vorbis (all modern players), MP3 (discouraged; the bmson spec notes encoder delay shifts sounds up to ~20 ms). beatoraja plays wav (PCM and MP3 only), ogg, mp3, converting to 16-bit 44.1 kHz at decode. One id can be defined twice in "multiplex" style (nested polyphony, see memo); polyphony is 1 per id by default.
- BGM is one long file triggered once on channel `01`, or hundreds of slices.
- `#BMPxx file`: BMP/PNG/JPG and, in LR2/beatoraja, videos (beatoraja tries mp4, wmv, m4v, webm, mpg, mpeg, m1v, m2v, avi in that order; other ffmpeg-readable types likely work). Channel `04` base, `07` layer (black = transparent), `06` poor. `#BGAxx`/`#@BGAxx` define sub-rectangles. BM98k shows a black 256x256 for an undefined id in channels 04/06/07.
- `#STAGEFILE`, `#BACKBMP`, `#BANNER`, `#PREVIEW`: see the header table. The bmson spec wants banners at 15:4 (normally 600x160).

## Versions & variants

- BM98 (1998): channels `01-06`, `11-17`, `21-27`, `31-36`, `41-46`; headers `#PLAYER #GENRE #TITLE #ARTIST #BPM #MIDIFILE #PLAYLEVEL #RANK #VOLWAV #WAVxx #BMPxx #TOTAL #RANDOM #IF #ENDIF #ExtChr`; hexadecimal ids.
- Timeline (hitkey memo): BM98k `#STAGEFILE`, BGA layer `07`; BM98de `#BGAxx`; Project2DX (pseudo-7K via `#ExtChr`), FlashTerminal (channels 18/19, 28/29, 38/39, 48/49), BME by TIX for BMSC (2000s); bemaniaDX 0.72 (2000-07-15) `#BPMxx`+ch `08`, `#STP`, `#VIDEOFILE`; DDR (2001-12) `#STOPxx`+ch `09`, Ogg alternative search; MGQ (2001) channels `51-8C` + hex channels `1A-1F`..; RDM 1.21 (2001-09-29) RDM-notation LN on `51-69`; RDM 1.61 (2002-02-22) `#LNOBJ`; RDM 1.7 (2003-08-17) `#LNTYPE 1` default; nanasi `#SUBTITLE`, `#DIFFICULTY`, `#BANNER`, `#DEFEXRANK`, landmines, `#OPTION`, `#SWITCH`; pomu `#CHARFILE`, `#COMMENT`, `#TEXT`; LR `#SUBARTIST`, `#BASEBPM`, `#SEEK`; Bemuse base-36 channel names, `#SCROLL`, `#SPEED`; beatoraja `#PREVIEW`, `#LNMODE`, `#DEFEXRANK` semantics, `#VOLWAV` max 100, `#SCROLLxx`.
- Extensions: `.bms` (5K, original), `.bme` (7K), `.bml` (LN), `.pms` (9 buttons). Modern players accept every channel in every extension except PMS (LR2 forces 9 buttons). Historic (memo): `.mgq` (24-key, LN channels, KEYBOARDMANIA emulation), `.mbm` (MacBeat MOD, needs `#WAVCMD`), `.ems` (24-key, AngelicPianizm style, KbMediaPlayer's `bmse.kpi`), `.kms` (24-key KeyMani style), `.bas` (BMS-2, BM-A4 / beat arranger), `.phx`, `.mgf`, `.bmb`, `.pmb`, `.d2b`, `.dee` (beatmaster variants, details unknown); `.mdm` (Muse Dash Melon Loader mod, per Wikipedia). DTX/GDA/G2D derive from BMS (own pages); bms-js has a DTX mode (`#NAME: value`, `#mmmcc: data`).

## Quirks & pitfalls

- Beyond the minimum, everything is implementation-defined: parse leniently (CR/LF/CRLF mixes, missing EOF newline, lowercase commands, tabs, indent, leading `#EXT`).
- `#WAV` id `00` is no keysound (rest in data, landmine sound in header). A doubled `.wav` exists (`ura_63..wav`).
- STOP is not scaled by `02`; a BPM change inside a shortened measure scales proportionally.
- "Kusofumen" use negative BPM, negative or decimal STOP, STOP 2147483647: do not crash or loop. One chart has 6177 `#RANDOM` blocks and 400k lines (オートメーション工場): do not recurse naively.
- `#RANK`/`#TOTAL` defaults differ per engine.
- An `#LNOBJ` id also used as a normal note makes that note disappear in LNOBJ-aware players.
- `#PLAYER` is unreliable; 2P channels in a `#PLAYER 1` file are valid.
- Zero-length measure (`#xxx02:0`): its objects share one time position (bms-rs special case, PR 311).

## Example

First lines of the repo sample [`samples/beginner.bms`](samples/beginner.bms) (Shift_JIS, 7-key chart in a `.bms`, shown re-encoded; the file continues with `#00201`... lines for the other measures):

```
*---------------------- HEADER FIELD

#PLAYER 1
#GENRE STEINS;GATE
#TITLE 刻司ル十二ノ盟約
#ARTIST 榊原ゆい　obj.よねすけ
#BPM 108
#PLAYLEVEL 9
#RANK 3
#STAGEFILE 

#WAV03 刻司ル十二ノ盟約.mp3

#DIFFICULTY 1

*---------------------- MAIN DATA FIELD

#00211:0101
#00212:00000000000000000100000000000001
#00216:0101
#00218:00010100010100010001000000000100
```

Measure 002 (numbering starts at `#000`): channel 11 (1P key 1) has 2 slots, channel 12 has 16, 16 is the scratch, 18/19 are keys 6/7. The only keysound is `#WAV03` (a full MP3 in `#00101`); the lane `01` objects point to the undefined `#WAV01` and are silent.

Long-note forms (hand-built; the first two quoted from the hitkey memo):```
#LNTYPE 1
#00151:00220000
#06451:000000000033     RDM type #1: LN from #001 to #064 on lane 1 (channel 51)

#LNOBJ ZZ
#00111:00220000
#06411:0000000000ZZ     RDM type #2: ZZ ends the LN started by the previous object of channel 11
```

## ROX support

Decode only (`rox::formats::bms`, `rhythm-open-exchange/src/formats/bms/`; tests `bms/tests.rs`, charts `assets/bms/features.bms`, `assets/bms/nine.pms`). `.bms`, `.bme`, `.bml` go to `BmsDecoder`, `.pms` to `PmsDecoder`; `auto_decode`, `auto_decode_bytes`, `auto_decode_variant` detect them, `auto_encode` refuses them.

- Layout follows the lanes used (`#PLAYER` ignored). One side: `[scratch] key1..key5` or `key1..key7` (keys 6/7 are channels `x8`/`x9`; scratch column only if `x6`/`5x`/`6x` lanes use it) = 5, 6, 7 or 8 columns. Double play: `[scratch1] 1P keys | 2P keys [scratch2]` = 10, 12, 14 or 16 columns (scratch on both sides once either uses it). A 2P-only chart is single. PMS: nine columns, `11 12 13 14 15 22 23 24 25`, or `11 12 13 14 15 18 19 16 17` (BME-type) with no 2P lane and channels 16-19 used. Channel `x7` and out-of-layout lanes are dropped.
- Time: `02`, `03` (hex), `08` via `#BPMxx`/`#EXBPMxx` (non-positive or undefined BPM ignored; at one position `03` then `08`). STOP `09` in 1/48 beat units, not scaled by measure length, uses the BPM after a same-position change; a note on a STOP is at the pause start. Stops are baked into note times like `.sm`. Missing `#BPM` = 130.
- Long notes: `#LNTYPE 1` pairs (odd last head is a tap), `#LNOBJ` (terminator closes the lane's previous note, is not a note; orphan dropped), `#LNTYPE 2` runs (up to the first empty slot, across a bar line if last and first slots are filled). Mines `D1-E9` become mines. `3x`/`4x` ignored. A note inside an LN or at the same time and column as the previous note is dropped.
- `#RANDOM` is always 1; `#SETRANDOM n` forces `n`; `#IF`/`#ELSEIF`/`#ELSE`/`#ENDIF`/`#ENDRANDOM` nest; `#IF` without `#RANDOM` is 1; content in `#RANDOM` outside `#IF` is kept. `#SWITCH` unsupported.
- Audio: each playable note's `#WAVxx` goes to `chart.hitsounds` (`\` becomes `/`, ids case-insensitive base 36). Channel-01 sounds are not in the chart. With exactly ONE background sound, it is `metadata.audio_file` and all times shift back by its position (negative times possible). Otherwise `audio_file` is empty and Prism refuses the chart as "audio missing" unless `decode_with_audio_plan` is used: it returns every channel-01 object and playable keysound at chart time, and Prism mixes them into one Opus track (`docs/rendu-audio.md` in the Prism repo).
- File names: `#WAVxx`, `#STAGEFILE`, `#BACKBMP` names that are absolute, have a drive letter, hold a NUL or contain `..` are read as undefined (counted in `BmsReport::unsafe_names`).
- Text: BOM UTF-8/UTF-16, else UTF-8, else Shift_JIS, else EUC-KR (`encoding_rs`).
- Metadata: `#TITLE`, `#ARTIST`, `#GENRE`, `#MAKER` (creator), `#PLAYLEVEL`, difficulty name from `#DIFFICULTY` (1-5: Beginner, Normal, Hyper, Another, Insane) else `#SUBTITLE` else `Normal`, background `#STAGEFILE` (else `#BACKBMP`).
- Not handled: `#SCROLLxx`/`#SPEEDxx`, `#STP`, `#SWITCH`, `#CHARSET`, base-62 files, BGA, `#LNMODE`, `#EXRANKxx`, channels `1A-1Z` (MGQ/pomu).
- Verified note for note (count, time, column, long notes) against Bemuse's `bms-js` (MIT) on the 21 sample charts of `bme/samples` and `bms/samples`; by note count against `bms-rs` (Apache-2.0), which differs in time on the 8 charts using channel `02` or `03` (not investigated; it spaces objects of a shortened or lengthened measure by the fraction of a 4/4 measure, Bemuse and ROX by the fraction of the measure's own length). The sample charts have no licence and are not shipped in ROX; ROX tests use synthetic charts.

## Parsers & tools

- bms-js / bemuse-notechart (JavaScript): https://github.com/bemusic/bms-js , https://github.com/bemusic/bemuse-notechart ; package `bemuse/packages/bms`.
- bms-rs (Rust, supports beatoraja and Bemuse extensions): https://github.com/MikuroXina/bms-rs
- StepMania loader and writer: https://github.com/stepmania/stepmania/blob/5dad6a1c9a1caba66ebc1aa0feab9bc920399455/src/NotesLoaderBMS.cpp and `NotesWriterBMS.cpp`.
- Raindrop (C++): https://github.com/zardoru/raindrop/blob/master/src/NoteLoaderBMS.cpp
- beatoraja (Java): https://github.com/exch-bms2/beatoraja ; LR2 (closed source); Angolmois / Sonorous (Kang Seonghoon): https://github.com/lifthrasiir/angolmois-rust , https://cosmic.mearie.org/f/sonorous/ ; Project OutFox: https://outfox.wiki/en/dev/mode-support/bms-pms-support
- Editors: BMSE (https://github.com/dtinth/UCN-BMSE fork), iBMSC, BMS Creator, GDA Creator; bmx2wav, bme2wav, BMx Outliner (`#RANDOM` viewer).
- Community: BMS Search (https://bmssearch.net/), difficulty tables (GENOCIDE, etc.), LR2IR/beatoraja IR, Bemuse (https://bemuse.ninja/), beatoraja English guide https://wcko87.github.io/beatoraja-english-guide

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (covers `.bme`, `.bml`, `.pms` samples too). Bemuse default songs: https://github.com/bemusic/music at `472b0f3cc433c39b0a7e9849705b34af68bf5400` (https://bemuse.ninja/music/ serves the same files). No real chart wider than 14K+2 scratches (24K, 48K) was found: be-music's README lists "24 KEY SP" and "48 KEY DP" modes, but its example folder and the `bemusic/music` index have none.

More: BMS Search (https://bmssearch.net/) links each song's distribution page. BMS events (BMS of Fighters, https://manbow.nothing.sh/event/, whose pages the Bemuse song READMEs link; event lists https://hitkey.nekokan.dyndns.info/bmsevt.htm and https://bms.ms/bmsevtalt) publish packs, mostly with audio. Starter packs from the Bemuse FAQ (https://faq.bemuse.ninja/): GENOSIDE 2018 (http://nekokan.dyndns.info/~lobsak/genocide/grade.html), GENOSIDE (http://nekokan.dyndns.info/~lobsak/genoside/), https://bms-community.github.io/resources/#starter-packs; archives at https://www.bmsworld.nz/. Editors: iBMSC (https://github.com/aqtq314/iBMSC), BMSE, BMS Creator, GDA Creator. Search terms: `BMS`, `BMS of Fighters`, `GENOSIDE`, `.bms .bme .bml` + song name. Packs have their own terms; keep the chart file only (no `#WAV` audio).

## Sources

- hitkey "BMS command memo": https://hitkey.nekokan.dyndns.info/cmds.htm (main source of this page; Japanese version https://hitkey.nekokan.dyndns.info/cmdsJP.htm)
- Original spec by Urao Yane: http://bm98.yaneu.com/bm98/bmsformat.html (referenced)
- bms-rs README: https://raw.githubusercontent.com/MikuroXina/bms-rs/main/README.md
- bms-js (README, `compiler/index.js`, `timing/index.js`, `notes/channels.js`): https://github.com/bemusic/bms-js
- Bemuse BMS extensions: https://bemuse.ninja/project/docs/bms-extensions/
- beatoraja wiki (楽曲製作者向け資料): https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- Raindrop `NoteLoaderBMS.cpp`: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
- Wikipedia "Be-Music Source": https://en.wikipedia.org/wiki/Be-Music_Source
- BMS Search: https://bmssearch.net/
- Repo samples: `samples/`, `../bme/samples/`; original list: the upstream `README.md` at commit `503382a` (lines on `.bms/.bme/.bml`).
- Sample sources (see `samples/SOURCES.md`): bms-rs https://github.com/MikuroXina/bms-rs/tree/1eb789caa32a3e0851d274723468576de26a2d08/tests ; Bemuse https://github.com/bemusic/bemuse/tree/4bf3e7d98a44841b323741cc403ecb7b41618ade ; Angolmois https://github.com/lifthrasiir/angolmois/tree/625f8431556b8772b13a826d48a1becd228a8b1c/test ; rparser https://github.com/rhythmus-emulator/rparser/tree/d2efba4c36e5f74fda3da4b90f7e9119f1f62861/test ; Bemuse songs https://github.com/bemusic/music/tree/472b0f3cc433c39b0a7e9849705b34af68bf5400 ; Nekokan/be-music https://github.com/Nekokan/be-music/tree/a1b770446227c3e678e9a079078e8831edc8886c/examples/test ; shuymn/tapestry https://github.com/shuymn/tapestry/tree/cf1cc4b55deeffdd32fb43f47b89f550a92fb9a3/crates/bms-parser/tests/charts ; sappho192/BMSParser https://github.com/sappho192/BMSParser/tree/f90ae7cb7eed2d7738230283925c44a720e1664c/Resource
