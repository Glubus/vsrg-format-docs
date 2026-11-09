# Be-Music Source (`.bms`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice, charset not specified)

This is the reference page for the whole BMS text format. The sibling folders [`../bme`](../bme/README.md), [`../bml`](../bml/README.md) and [`../pms`](../pms/README.md) only document what is specific to their extension; the syntax, header commands, channels, timing and long-note rules below are shared by all of them. The JSON dialect is documented in [`../bmson`](../bmson/README.md).

## Overview

- BMS ("Be-Music Source", also read "Be-Music Script") is a plain-text chart format devised by Urao Yane (with NBK) in 1998 for BM98, a PC simulator of Konami's arcade game beatmania. The draft was shown on 1998-05-04, the official "BMS Format Specification" was published on 1998-11-26. Anyone may use the format freely (`hitkey` memo, section "minimum requirements").
- The format is *keysound based*: the chart is a timeline of references to `#WAVxx` audio files (one file per base-36 id). Every playable note, and every automatic background sound, triggers one of these files. There is no single audio track; songs are shipped as many stems/slices. Because of this a BMS song is usually a folder containing the chart(s), keysounds, optional BGA images/videos, banner and stage image.
- Today it is the format of the BMS community (BMS events such as "BMS of Fighters", the BMS Search database, difficulty tables, LR2IR / beatoraja IR). The de facto players are Lunatic Rave 2 (LR2, Windows, Japan) and beatoraja (cross-platform, Java/libGDX), plus Bemuse (web), Raindrop (VSRG engine), ruv-it! (Korea), uBMplay, Angolmois, Project OutFox/StepMania (parser for `be-mu`/`po-mu` game types). Editors: BMSE (BMx Sequence Editor), iBMSC, BMS Creator (BMSC), GDA Creator.
- Typical file extensions: `.bms`, `.bme`, `.bml`, `.pms` (identical syntax; the extension is a historical hint about the channel set, see below), also `.bmson` (a different, JSON-based format).
- Samples in this repo: [`samples/`](samples/) (7-key chart using channels 18/19 inside a `.bms`, `#STAGEFILE` empty, one MP3 as BGM on `#WAV03`) and [`../bme/samples/`](../bme/samples/).

## Container & encoding

- One chart per file; a "song" is a folder with several chart files (one per difficulty/play style, usually distinguished by file name and `#DIFFICULTY`/`#PLAYLEVEL`). No archive wrapper, no compression, no binary part.
- Lines beginning with `#` are commands. All other lines are comments/ignored (the sample uses lines like `*---------------------- HEADER FIELD`). Command names are case-insensitive, although some implementations are case-sensitive for particular values (e.g. `#LNOBJ XX`, see below).
- Two command kinds: *header sentences* `#NAME value` and *channel (main data) sentences* `#mmmCC:data`. File order is free ("BMS is compiled at runtime"): headers can appear after the data that uses them. Control flow (`#RANDOM` ... ) must be parsed before everything else.
- **Duplicates.** If the same header appears twice, the one nearest to EOF wins (exceptions listed in the memo: `#ExtChr`, `#STP`, `#WAVCMD`, `#OPTION`, control flow; and not guaranteed for `#SUBTITLE`, `#SUBARTIST`, `#COMMENT`, `#LNOBJ`). For channels: two lines for the same channel of the same measure are *merged* (non-`00` objects of the later line override earlier ones; `00` never overwrites), except channel `01` (BGM: several lines = several independent BGM lines), channel `02` (last line wins) and `A6` (`#CHANGEOPTION`). Example from the memo: `#00113:11111111` + `#00113:0022332255224400` + `#00113:0066` merges to `1122332266224400`. About half of the implementations do not merge; a robust parser should.
- **Line endings** may be CRLF, CR or LF, even mixed in the same file. The last line may lack a newline.
- **Delimiter.** Header: `#NAME` + one space (many parsers also accept tabs / several blanks / leading indent) + value. Channel: `#` + 3-digit measure + 2-char channel + `:` + data. bms-js uses `^#(\w+)(?:\s+(\S.*))?$` for headers and `^#(\d\d\d)(\S\S):(\S*)$` for channels after trimming each line.
- **Charset.** Not specified by the spec. Most Japanese files are Shift_JIS (CP932). Korean files are often EUC-KR. UTF-8 (with or without BOM) and UTF-16 exist; ruv-it!, iBMSC, IIDXv, HDX, Sonorous, BGAEncAdv, beatoraja... support Unicode. The obsolete ruv-it! `#CHARSET [EUC-KR|SHIFT-JIS|UTF-8]` header existed. bms-js documents a "Reader" stage that does charset detection; ruvit uses BOM first, otherwise guesses EUC-KR vs Shift_JIS from the frequency of lead bytes. ASCII is the only safe set for *file names*. Known pitfalls: yen/won sign, wave dash, `~` mapping. Note that a Shift_JIS sample in this repo (`samples/�l�g����.bms`) already has an undecodable file name in this checkout.
- **File names inside the chart** (`#WAVxx`, `#BMPxx`, ...) are relative to the chart's folder; path separators are inconsistent between files (`\` and `/`). Audio extension is often wrong: modern players do an *alternative search* (`foo.wav` → `foo.ogg`, `foo.flac`, ...).

## Structure / metadata

Syntax summary:

```
#TITLE  some title                  header sentence
#WAV01  kick.wav                    definition of key sound id 01
#00111:01000100                     channel sentence: measure 001, channel 11 (1P key 1), 4 slots of 2 chars
```

### Header commands

"Origin" is the program that introduced the command (from the `hitkey` memo); "common" means almost all modern players read it.

| Command | Meaning | Notes |
| --- | --- | --- |
| `#PLAYER n` | Play mode, 1..4. | `1` single (default), `2` couple (1P+2P, two gauges), `3` double (1P+2P played by one player), `4` battle. Origin BM98. Modern players (LR2, nanasi, ruvit, pomu2, beatoraja) ignore it and guess the mode from the channels used. PMS recommends `#PLAYER 3`. |
| `#GENRE s` | Genre text | BM98. |
| `#TITLE s` | Title | BM98. Many files append the difficulty, e.g. `[HYPER]`; "implicit subtitle" heuristics exist (text in brackets or after `-`) for bemaniaDX/DDR. |
| `#SUBTITLE s` | Explicit subtitle | nanasi. Sonorous allows several. |
| `#ARTIST s` | Artist | BM98. |
| `#SUBARTIST s` | Helpers (slicer, movie maker, chart author) | LR. May appear several times. |
| `#MAKER s` | Author of the data | bemaniaDX. |
| `#COMMENT "s"` | Text on selection screen | pomu. May appear several times. |
| `#BPM n` | Initial BPM | BM98. Default 130 per spec, but implementations differ (nanasi 150, nazo/BMSC/BMSE/iBMSC 120, fgt# / pomu2 / o2play 0, LR2 hangs on its BPM display). A decimal value is accepted by almost every modern player. Always write it. |
| `#BPMxx n` / `#EXBPMxx n` | Real-number BPM table used by channel `08` | bemaniaDX; `#EXBPM` is nanasi's alias to dodge a BMSC bug. Index range `01`..`ZZ` in modern players (older: `01`-`99`, `01`-`FF`). Negative value = reverse scroll in LR2, bemaniaDX, ruvit, Angolmois... (undefined by the spec). |
| `#BASEBPM n` | BPM used as reference for the automatic hi-speed | LR. |
| `#STOPxx n` | STOP table used by channel `09` | DDR. `n` is in units of 1/192 of a whole note in 4/4 (see Timing). |
| `#STP xxx.yyy zzzz` | Stop given by measure position and duration in ms | bemaniaDX, Angolmois, Sonorous, bms-js. |
| `#PLAYLEVEL n` | Declared level (integer, can be huge, e.g. `5000` in the repo sample) | BM98. nanasi allows a string. |
| `#DIFFICULTY n` | 1 Beginner, 2 Normal, 3 Hyper, 4 Another, 5 Insane | nanasi; read by LR2, iBMSC 3, Sonorous, beatoraja. |
| `#RANK n` | Judgment level: 0 VERY HARD, 1 HARD, 2 NORMAL, 3 EASY | BM98. LR2 windows: +-8 / 15 / 18 / 21 ms. nanasi adds `4` (VERY EASY); beatoraja documents `#RANK 4` as VERY EASY = 1.25x EASY. Default when omitted is implementation dependent (BM98 etc. 2, BMSE/iBMSC 3, nBMplay 0). |
| `#DEFEXRANK n` | Judgment width as a percentage of NORMAL (100 = NORMAL) | nanasi; beatoraja says it overrides `#RANK` (since 0.7.3 reference = NORMAL). |
| `#EXRANKxx n` | Table for channel `A0` (judge change during the song) | nanasi. |
| `#TOTAL n` | Gauge increase when all notes are hit perfectly | BM98. Omitted = implementation default (`200+NOTES` in BM98, 160 LR2/ruvit, 350 nanasi...). IIDX gauge formula quoted in the memo: `7.605*NOTES/(0.01*NOTES+6.5)`. Decimal values are accepted. Negative = gauge decreases in some players. |
| `#VOLWAV n` | Master volume of the keysounds (percent) | BM98. beatoraja: max 100. |
| `#LNTYPE n` | Long-note notation: `1` (default) channels 51-69 RDM type, `2` MGQ type (obsolete) | RDM. See "Notes". |
| `#LNOBJ xx` | Id of a keysound that marks the *end* of a long note | RDM 1.61. See "Notes". |
| `#LNMODE n` | beatoraja extension: 1 LN, 2 CN, 3 HCN (forces the long-note type) | beatoraja. |
| `#WAVxx file` | Keysound table, `xx` = base-36 id `01`..`ZZ` (`00` = landmine sound) | See Audio. |
| `#BMPxx file` | Image/video table, `00`..`ZZ` | See Audio. |
| `#EXBMPxx a,r,g,b file`, `#BGAxx`, `#@BGAxx`, `#POORBGA`, `#SWBGAxx`, `#ARGBxx`, `#VIDEOFILE`, `#VIDEOf/s`, `#MOVIE`, `#SEEKxx`, `#ExtChr` | BGA cropping / transparency / video extensions | bemaniaDX, BM98de, nanasi, DXEmu, BM98 (`#ExtChr`). See memo for exact argument lists. |
| `#STAGEFILE file` | Splash image (640x480) shown while loading | BM98k; very common. May be empty (as in the sample). |
| `#BACKBMP file` | Background image of the play screen | DDR; used by LR2 skins. |
| `#BANNER file` | Banner for the song list | nanasi; common. |
| `#PREVIEW file` | Preview audio in the song selection screen | beatoraja (if absent, beatoraja looks for `preview*.wav/ogg` in the folder). |
| `#SCROLLxx n` + channel `SC`, `#SPEEDxx n` + channel `SP` | Scroll-speed multiplier segments (negative = reverse) | Bemuse extension (from StepMania 5 SPEED/SCROLL); beatoraja implements `#SCROLLxx` / `#nnnSC:` as well, Raindrop planned them. |
| `#WAVCMD`, `#OPTION`, `#CHANGEOPTIONxx`, `#OCT/FP`, `#CHARFILE`, `#TEXTxx`, `#SONGxx`, `#CDDA`, `#MIDIFILE`, `#PATH_WAV`, `#MATERIALSWAV/BMP`, `#DIVIDEPROP`, `#CHARSET`, `%URL`, `%EMAIL` | Player- or editor-specific; documented individually in the memo. | Rarely needed by a chart reader. |
| `#EXT #mmmcc:...` | Bemuse "extension line" prefix (`#EXT` is removed from bms-rs for lack of specification) | |

### Control flow

Block statements, all evaluated before anything else (a parser must pre-process the file):

- `#RANDOM n` draws an integer in `1..n`; `#IF k` ... `#ENDIF` keeps its content only if the draw equals `k`. Optional: `#ELSEIF k`, `#ELSE` (IIDXv, nanasi), `#ENDRANDOM` (nanasi, required there for nested blocks), `#SETRANDOM n` (force the value, pomu2). `#SWITCH n` / `#SETSWITCH n`, `#CASE k`, `#SKIP`, `#DEF`, `#ENDSW` (nanasi) are the switch-style equivalent.
- Content outside `#IF` but inside `#RANDOM` is "orphaned": some players keep it (BM98, ruvit, uBMplay), some drop it (LR2, nazo, BMSE). Do not rely on it.
- Many players only support one nesting level (LR2, ruvit, bemaniaDX, ...); BM98, nanasi, pomu2, beatoraja-style engines nest. Headers (`#TITLE`, `#WAV`, `#BPMxx`) can be inside `#IF`.
- Typos found in the wild and accepted by some players: `#RONDAM`, `#END IF`, missing separator `#random5`. Players such as IIDXv/HDX default to `1` if no `#RANDOM` precedes `#IF`.
- bms-js implements it with a stack: `#RANDOM n` pushes `rng(n)`, `#IF k` pushes `skip = (top != k)`, `#ENDIF` pops; non-flow lines are dropped when the current skip flag is set. A fixed seed (or fixed values) is needed to get reproducible results.

### Main data field

`#mmmCC:ZZZZ...`

- `mmm`: 3 decimal digits, measure number `000`..`999` (`#000` is allowed by almost every modern player; LR2 inserts an empty measure before `#000` when it holds visible notes).
- `CC`: channel, 2 base-36 characters (see table).
- `ZZ...`: even-length string of 2-character *object ids*. The measure is divided into as many equal slots as there are pairs. Object `00` is a rest. Object ids are **base 36** (`0-9A-Z`) in modern files (1296 values, `00` unusable so 1295 usable), limited base-36 (`[0-9A-F][0-9A-Z]`, 576) or hexadecimal (256) in older ones. Case matters for some old players (`#LNOBJ`, uppercase is safer; nanasi and fgt++ do not match lowercase ids). In channel `03` (BPM) the pair is read as a *hexadecimal* number (`01`..`FF`) instead of an id; channels `0B`-`0E`, `97`, `98` also carry `01`..`FF` values per the memo's channel table.
- Invalid data is not specified. Cases found in the wild: odd length, non-alphanumerics, 500 000-character lines, trailing `;comment`, multi-byte chars inside the data. LR2/nazo/uBMplay try to recover; the recovery is undocumented.

### Channel table

From the `hitkey` channel mapping table (origin in the last column). `xx` below stands for a base-36 id.

| Channel | Meaning | Value | Origin |
| --- | --- | --- | --- |
| `01` | BGM (autoplay keysound). Several lines per measure are allowed and not merged. | `#WAVxx` | BM98 |
| `02` | Measure length multiplier. Only for that measure. `1` = 4/4, `0.75` = 3/4, `2` = 8/4. Real number (decimal point, not a base-36 pair). Last line wins. A length of 0 is used by some "kusofumen"; bms-rs treats it as a zero-length measure and keeps the objects at the same position. | float | BM98 |
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

Channel sets by "format" (from the `hitkey` KEYMAP table; *playable* lanes only; "16" is the scratch):

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

Key-mode inference: since `#PLAYER` is ignored, a reader counts used channels; a chart using only 16 can be 5K, 7K, 10K, 14K or PMS; use the file extension (PMS) and the presence of 18/19/21-29 to decide. IIDX-style 7K+scr is the commonly assumed layout (bms-js defines `IIDX_P1 = {11:1, 12:2, 13:3, 14:4, 15:5, 18:6, 19:7, 16:SC}`); Raindrop translates BME (`18`,`19`) to keys 6,7 and PMS with a dedicated mapper.

## Timing model

- Time is expressed as (measure number, fraction of measure). A measure is by default 4 quarter notes (4 beats); channel `02` multiplies its length (beats in measure *m* = `4 * len(m)`, `len` default 1). Position of a slot `i` out of `n` in measure `m`: `beat = sum_{k<m}(4*len(k)) + (i/n) * 4*len(m)`. This is exactly what bms-js `chart.measureToBeat` and Raindrop's `BeatForObj` do. There is no integer tick resolution; the finest representable position is limited only by the string length. A slot string that is e.g. 10 pairs long places objects at 1/10 of the measure.
- **BPM.** Initial `#BPM`; channel `03` sets an integer BPM (hex 1..255), channel `08` looks up `#BPMxx` / `#EXBPMxx` (real number, even above 255, even negative). When both `03` and `08` objects are at the same position the result is implementation dependent (BMSE/iBMSC warn). bms-js reads `03` as `parseInt(value,16)` and `08` as `+headers['bpm'+value]`; the initial BPM falls back to 60 when unparsable.
- **STOP.** Channel `09` + `#STOPxx n`. Unit: 1 = 1/192 of a whole note in 4/4, i.e. 1/48 of a beat; independent of channel `02`. Duration in seconds = `n/48 * 60/BPM` using the BPM *in effect at the stop*. bms-js: `stopBeats = value/48`; Raindrop: `Stops[ev]/48`. Order inside one position: notes sound first, then BPM change, then STOP (BPM change applied before the stop duration is computed). Negative STOP values: skipped by many, applied as -1 or 0 by others; decimal STOP values are truncated by LR2/Angolmois and kept by ruvit/nanasi/IIDXv.
- `#STP xxx.yyy zzzz` (bemaniaDX): a stop given by measure position (`xxx.yyy`) and a duration (`zzzz`); exact units were not verified here (see the memo section `#STP`). It is read by bms-js `Timing` ("STP commands") and by Angolmois/Sonorous.
- Converting to seconds (what bms-js `Timing.fromBMSChart` does): collect `bpm` and `stop` actions with their beat, sort by beat then (`bpm` before `stop`), walk accumulating `seconds += (beat - lastBeat) * 60 / bpm`; at a stop add `stopBeats * 60 / bpm`. A note placed at the stop position is hit at the *start* of the pause.
- **Offset.** BMS has no audio offset header: the audio is entirely made of keysounds placed on the timeline, so alignment is by construction. Players that use a single BGM file (e.g. `#WAV03 song.mp3` on channel 01 at `#00101:...03` like the repo sample) rely on that object being at the right time.
- **Scroll speed (SV).** Not in the original format. Bemuse `#SCROLLxx`/`#SPEEDxx`, beatoraja `#SCROLLxx`/`#nnnSC:` (multiplier on top of BPM-based speed, negative = reverse). Negative BPM/STOP are older ways to fake it.
- **Measure `#000`** / maximum measure: general implementations support `#000`..`#999`; some old ones fewer (BMSV 511, bemaniaDX 399, GALLI 399, BGAEnc 249).

## Notes

- **Visible note (tap).** Any object on a playable channel (`1x`/`2x`). Its id selects the keysound triggered when the player hits it. If the same keysound should play as BGM too, it is placed on channel `01`.
- **Invisible object** (`3x`/`4x`): never judged, never scored. A key press near it plays its keysound. Used for "ad-lib" and for easter eggs; placed under a visible note it can replace the keysound.
- **Landmine** (`Dx`/`Ex`): drawn as a hazard; when the key is held at the judgment time the gauge drops by `value/2` percent (`ZZ` fails the stage); the explosion sound is `#WAV00`.
- **Long notes** (three notations):
  1. `#LNTYPE 1` (RDM type #1, default, channels `51`..`69` for 1P and `61`..`6Z` for 2P): objects on an LN channel alternate *start*, *end*, *start*, *end* ... in time order; a non-`00` object opens an LN and the next non-`00` object on the same channel closes it. The sound of the start is played; the sound of the end is ignored (HDX/IIDXv/TechnicalGroove play the end id as the key-up sound when it differs from the start id). Example from the memo: `#00151:00220000` + `#06451:000000000033` is one LN from measure 001 to measure 064.
  2. `#LNOBJ xx` (RDM type #2, since RDM 1.61): the keysound id `xx` is a *terminator*; when an object with that id appears on a playable channel (`11`..`29`), the *previous visible object on the same channel* becomes the LN start. The terminator object is not a note. Players that do not support `#LNOBJ` display the terminator as an ordinary note; the extension `.bml` was proposed as a filter for that case. Use uppercase for `xx` (nanasi/fgt++ bug). Some players (RDM/ruvit) play the terminator keysound as BGM; most do not. TechnicalGroove allows several `#LNOBJ`.
  3. `#LNTYPE 2` (MGQ type, channels `51`..`8C`, obsolete): an LN is a run of non-`00` objects with the same lane; it ends at the first `00` (runs continue across bar lines if last of previous measure and first of next are both non-`00`).
  If both RDM-type channels and `#LNOBJ` are used in one file, the priority is unspecified.
  Counting rule (implementation-dependent): an LN counts as 1 note in most players, 2 in others. Whether the end must be released: per the memo, apps other than nanasi, HDX and Angolmois do not judge the end of a LN; beatoraja `#LNMODE`: 1 = LN, 2 = CN, 3 = HCN (the beatoraja wiki gives only these labels; CN = charge note, HCN = hell charge note in IIDX terminology). beatoraja's bmson field `t` (see [`../bmson`](../bmson/README.md)) is the equivalent.
- **Scratch/free zone.** `#xxx16` is the turntable lane; `#xxx17` (original BM98 free zone, one quarter note long, extended by a new object before it closes) is the foot pedal in nanasi/Angolmois, or a 9th key (PMS BME-type).
- **Simultaneous notes**: any number of channels can have an object at the same position. Two objects on the same channel at the same position cannot exist (one slot).
- **Counting notes** is the player's job: visible objects on the lanes of the detected mode, with the LN counting rule above.

## Audio & images

- `#WAVxx file`: `xx` base-36 `01`..`ZZ` (1295 ids; `00` is for landmines). Formats: WAV (PCM 8/16/24, IEEE float exist), OGG Vorbis (all modern players), MP3 (supported but discouraged; the bmson spec notes encoder delay shifts sounds up to ~20 ms). beatoraja plays wav (PCM and MP3 only), ogg, mp3, converting to 16-bit 44.1 kHz at decode. Modern players do "alternative search" on extensions. The same id can be defined twice in "multiplex" style (nested polyphony, see memo); by default polyphony is 1 per id.
- BGM can be a *single long file* triggered once on channel `01` or hundreds of slices.
- `#BMPxx file`: images (BMP/PNG/JPG) and, in LR2/beatoraja, **videos** (beatoraja detects mp4, wmv, m4v, webm, mpg, mpeg, m1v, m2v, avi in that priority order; any other file type ffmpeg can read is likely OK). Channel `04` base, `07` layer (black = transparent), `06` poor. `#BGAxx`/`#@BGAxx` define sub-rectangles of a BMP. In BM98k an *undefined* image id used in channels 04/06/07 displays a black 256x256.
- `#STAGEFILE`, `#BACKBMP`, `#BANNER`, `#PREVIEW` (see header table). The bmson spec says banners should be 15:4 (normally 600x160).

## Versions & variants

- **BM98 original** (1998): channels `01-06`, `11-17`, `21-27`, `31-36`, `41-46`; headers `#PLAYER #GENRE #TITLE #ARTIST #BPM #MIDIFILE #PLAYLEVEL #RANK #VOLWAV #WAVxx #BMPxx #TOTAL #RANDOM #IF #ENDIF #ExtChr`. Object ids hexadecimal.
- Extension timeline (hitkey memo): BM98k adds `#STAGEFILE` and BGA layer `07`; BM98de adds `#BGAxx`; Project2DX (pseudo-7K via `#ExtChr`), FlashTerminal (channels 18/19, 28/29, 38/39, 48/49), BME proposed by TIX for BMSC (2000s); bemaniaDX 0.72 (2000-07-15) adds `#BPMxx`+ch `08`, `#STP`, `#VIDEOFILE`; DDR (2001-12) adds `#STOPxx`+ch `09`, Ogg alternative search; MGQ (2001) adds channels `51-8C` + hex channels `1A-1F`..; RDM 1.21 (2001-09-29) RDM-notation LN on `51-69`; RDM 1.61 (2002-02-22) `#LNOBJ`; RDM 1.7 (2003-08-17) `#LNTYPE 1` default; nanasi adds `#SUBTITLE`, `#DIFFICULTY`, `#BANNER`, `#DEFEXRANK`, landmines, `#OPTION`, `#SWITCH`; pomu adds `#CHARFILE`, `#COMMENT`, `#TEXT`; LR adds `#SUBARTIST`, `#BASEBPM`, `#SEEK`; Bemuse adds base-36 channel names, `#SCROLL`, `#SPEED`; beatoraja adds `#PREVIEW`, `#LNMODE`, `#DEFEXRANK` semantics, `#VOLWAV` max 100, `#SCROLLxx`.
- **Extensions**: `.bms` (5K, original), `.bme` (7K), `.bml` (LN), `.pms` (9 buttons). All have identical syntax; modern players accept every channel in every extension except PMS (extension forces 9-button layout in LR2). Other historic extensions listed by the memo: `.mgq`/MGQ (24-key BMS with LN channels, KEYBOARDMANIA emulation), `.mbm` (MacBeat MOD, needs `#WAVCMD`), `.ems` (24-key, AngelicPianizm style, supported by KbMediaPlayer's `bmse.kpi`), `.kms` (24-key KeyMani style), `.bas` (BMS-2 format, BM-A4 / beat arranger extension), `.phx`, `.mgf`, `.bmb`, `.pmb`, `.d2b`, `.dee` (beatmaster variants, unknown details). `.mdm` is a BMS-like text file used by the fan "Muse Dash Melon Loader" custom-chart mod according to the Wikipedia BMS article; no spec was consulted. DTX/GDA/G2D are BMS-derived and have their own pages in this repo.
- The syntax is also the base of the DTX family. bms-js has a DTX mode: header `#NAME: value` (colon after the name) and channel `#mmmcc: data` with an optional space.

## Quirks & pitfalls

- Everything is implementation-defined beyond the minimum requirements; build a lenient parser: tolerant of CR/LF/CRLF mixes, missing EOF newline, lowercase commands, tabs, indent, leading `#EXT`.
- Header duplicates: last wins; channel duplicates: merge; channel 01: never merge.
- `#WAV` ids `00` is not a keysound (rest in data, landmine sound in header). A trailing `.wav` inside the file name may be doubled (`ura_63..wav` in a real file).
- Measure length and STOP: STOP is not scaled by `02`; BPM change position inside a shortened measure scales proportionally.
- Negative BPM, negative or decimal STOP, huge STOP (2147483647) exist in "kusofumen"; a decoder must not crash or loop.
- A chart with 6177 `#RANDOM` blocks and 400k lines exists (オートメーション工場); do not recurse naively.
- File name with Shift_JIS bytes inside Unicode file systems (see sample) can be unreadable.
- `#RANK`/`#TOTAL` defaults differ: charts that omit them play differently per engine.
- LN with `#LNOBJ` pointing to a keysound also used as a normal note makes that note disappear in LNOBJ-aware players.
- `#PLAYER` is unreliable; `#00111:` through `#001..` of 2P channels in a `#PLAYER 1` file are valid (used for jokes).
- Zero-length measure (`#xxx02:0`): objects of that measure all share one time position (bms-rs special case, PR 311).

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

Reading: measure 002 (the third measure, numbering starts at `#000`), channel 11 (1P key 1) has 2 slots with object `01` at 0 and 1/2 of the measure; channel 12 has 16 slots; channel 16 is the scratch; channels 18/19 are keys 6/7 (BME layout inside a `.bms`). The only keysound is `#WAV03`, a full MP3 triggered on channel 01 in measure 001 (`...03...` in `#00101`), and `01` objects on the lanes refer to the undefined `#WAV01`, i.e. they are silent.

Hand-built illustration of the long-note forms (illustrative, hand-built from the rules above, the first two are quoted from the hitkey memo):

```
#LNTYPE 1
#00151:00220000
#06451:000000000033     RDM type #1: LN from #001 to #064 on lane 1 (channel 51)

#LNOBJ ZZ
#00111:00220000
#06411:0000000000ZZ     RDM type #2: ZZ ends the LN started by the previous object of channel 11
```

## ROX support

Read by ROX since Prism's addition of `rox::formats::bms` (decode only: ROX does not write BMS). Source: `rhythm-open-exchange/src/formats/bms/` (documented in its module, tests in `bms/tests.rs`, hand-written charts `assets/bms/features.bms` and `assets/bms/nine.pms`).

- Extensions: `.bms`, `.bme`, `.bml` go to `BmsDecoder`, `.pms` to `PmsDecoder` (the extension is the only thing that says nine buttons). `auto_decode`, `auto_decode_bytes` and `auto_decode_variant` detect them; `auto_encode` refuses them.
- **Layout = the lanes the chart uses** (`#PLAYER` is ignored, like most players). One side: `[scratch] key1..key5` or `key1..key7` (keys 6 and 7 are channels `x8`/`x9`; the scratch column exists only when channel `x6`/`5x`/`6x` lanes use it) = 5, 6, 7 or 8 columns. Double play (1P and 2P lanes both used): `[scratch1] 1P keys | 2P keys [scratch2]` = 10, 12, 14 or 16 columns (a scratch column on both sides as soon as either side uses it). A chart with only 2P lanes is a single chart. PMS: nine columns, buttons `11 12 13 14 15 22 23 24 25`, or `11 12 13 14 15 18 19 16 17` (BME-type) when there is no 2P lane and channels 16-19 are used. Channel `x7` (free zone / foot pedal) and lanes outside the layout are dropped.
- **Time**: measure length (`02`), BPM (`03` hex, `08` through `#BPMxx`/`#EXBPMxx`; a non-positive or undefined BPM is ignored; at one position `03` then `08`), STOP (`09`, 1/48 beat units, not scaled by the measure length, computed with the BPM that follows a BPM change at the same position, a note on a STOP is at the start of the pause; stops are baked into the note times like `.sm`, ROX has no stop point). Missing `#BPM` = 130.
- **Long notes**: `#LNTYPE 1` channels (head/tail pairs; an odd last head is a tap), `#LNOBJ` (the terminator closes the previous note of the lane and is not a note; an orphan terminator is dropped), `#LNTYPE 2` runs (consecutive slots up to the first empty slot, across a bar line when the last and first slots are both filled). Mines `D1-E9` become ROX mines. Invisible objects (`3x`/`4x`) are ignored. A note inside a long note, or on the same time and column as the previous note, is dropped.
- **`#RANDOM`**: always 1 (reproducible); `#SETRANDOM n` forces `n`; `#IF`/`#ELSEIF`/`#ELSE`/`#ENDIF`/`#ENDRANDOM` nest; an `#IF` without `#RANDOM` is 1; content inside `#RANDOM` but outside `#IF` is kept. `#SWITCH` is not supported.
- **Keysounds and audio**: each playable note's `#WAVxx` goes to `chart.hitsounds` (file names with `\` become `/`, ids are case-insensitive base 36). Channel-01 background sounds are not part of a ROX chart. When the chart has exactly ONE defined background sound, that file is `metadata.audio_file` and every time is moved back by its position (earlier notes get negative times); otherwise `audio_file` is empty and Prism refuses the chart as "audio missing" (the sounds would have to be mixed into one track, not done).
- **File names**: `#WAVxx`, `#STAGEFILE` and `#BACKBMP` names that are absolute, have a drive letter, hold a NUL or contain a `..` component are read as undefined (counted in `BmsReport::unsafe_names`).
- **Text**: BOM UTF-8/UTF-16, else valid UTF-8, else Shift_JIS, else EUC-KR (`encoding_rs`).
- **Metadata**: `#TITLE`, `#ARTIST`, `#GENRE`, `#MAKER` (creator), `#PLAYLEVEL` (difficulty value), difficulty name from `#DIFFICULTY` (1-5: Beginner, Normal, Hyper, Another, Insane) else `#SUBTITLE` else `Normal`, background from `#STAGEFILE` (else `#BACKBMP`).
- **Audio plan**: `decode_with_audio_plan` also returns the sounds (every channel-01 object and the keysound of every playable object, at chart time) beside the chart; Prism mixes them into one Opus track when the chart has no single audio file (`docs/rendu-audio.md` in the Prism repo).
- Not handled: `#SCROLLxx`/`#SPEEDxx`, `#STP`, `#SWITCH`, `#CHARSET`, base-62 files, BGA, `#LNMODE`, `#EXRANKxx`, and the hexadecimal-letter channels `1A-1Z` (MGQ/pomu).
- Verification: the decoder agrees note for note (count, time, column, long notes) with Bemuse's `bms-js` (MIT) on the 21 sample charts of this repository (`bme/samples`, `bms/samples`), and by note count with `bms-rs` (Apache-2.0; it differs in time on the 8 of these 21 charts that use channel `02` or `03`, a difference not investigated further: for a shortened or lengthened measure it spaces the objects by the fraction of a 4/4 measure, where Bemuse and ROX use the fraction of the measure's own length). The sample charts are community files with no licence and are not shipped inside ROX; ROX's tests use the hand-written synthetic charts above.

## Parsers & tools

- bms-js / bemuse-notechart (JavaScript, Bemuse): https://github.com/bemusic/bms-js , https://github.com/bemusic/bemuse-notechart ; package `bemuse/packages/bms`.
- bms-rs (Rust, MikuroXina): https://github.com/MikuroXina/bms-rs (supports beatoraja and Bemuse extensions).
- StepMania C++ loader and writer: https://github.com/stepmania/stepmania/blob/5dad6a1c9a1caba66ebc1aa0feab9bc920399455/src/NotesLoaderBMS.cpp and `NotesWriterBMS.cpp`.
- Raindrop (C++): https://github.com/zardoru/raindrop/blob/master/src/NoteLoaderBMS.cpp
- beatoraja (Java): https://github.com/exch-bms2/beatoraja ; Lunatic Rave 2 (closed source); Angolmois / Sonorous (C / Rust, Kang Seonghoon): https://github.com/lifthrasiir/angolmois-rust , https://cosmic.mearie.org/f/sonorous/ ; Project OutFox parsers (see https://outfox.wiki/en/dev/mode-support/bms-pms-support).
- Editors: BMSE (https://github.com/dtinth/UCN-BMSE fork), iBMSC, BMS Creator, GDA Creator; converters bmx2wav, bme2wav, BMx Outliner (`#RANDOM` viewer).
- Ecosystem: BMS Search (https://bmssearch.net/ - Japanese database of songs, charts, artists and events), difficulty tables (GENOCIDE, etc.), BMS of Fighters, LR2IR/beatoraja IR, Bemuse (https://bemuse.ninja/), the English beatoraja guide https://wcko87.github.io/beatoraja-english-guide .

## Getting samples

Details and per-file licences: [`samples/SOURCES.md`](samples/SOURCES.md) (also covers the `.bme`, `.bml` and `.pms` samples in the sibling folders).

- **Committed** ([`samples/`](samples/)): the 11 community charts that came with the upstream repository (origin and licence unknown, Shift_JIS, 5K/7K+scratch, some with RDM long notes; two are byte-identical duplicates); real files from open-source repositories with a stated licence: Bemuse `#BASE 62` fixtures (AGPL-3.0 / MIT), bms-rs test charts (Apache-2.0: 7K charts with BOM, extended BPM/STOP, `#SCROLLxx`/`#SPEEDxx`), Angolmois's public-domain `invisible.bms`, rhythmus-emulator/rparser's MIT test charts (four "Angelico" charts and two "kusofumen"), Nekokan/be-music's MIT examples (`#PLAYER 3` double-play charts with 2P lanes 21-29 - `lane-order-test.bms`, `benchmark-command-mix-100.bms`, `four-measure-command-combo-test.bms` -, a pop'n 9-button chart in a `.bms`, `#LNMODE` 1/2/3 charts, `#RANDOM`, a real Shift_JIS file) and shuymn/tapestry's Shift_JIS title, `#LNTYPE 2`, mines and BPM/STOP charts; plus hand-written CC0 charts: double play 14K and 10K (`#PLAYER 3`), `#LNTYPE 2`, a CP932 + CRLF file with Japanese file names, decimal/negative BPM + STOP + measure lengths. The double-play files from the open-source repositories are small test files; full-length real DP songs are the `bemuse-*` files (next bullet).
- **Real Bemuse default songs** (committed, `bemuse-*` files): 59 `.bms` charts from https://github.com/bemusic/music at commit `472b0f3cc433c39b0a7e9849705b34af68bf5400` (the live site https://bemuse.ninja/music/ serves the same files), among them 17 real double-play charts (`#PLAYER 3`, 14K lanes 11-19 + 21-29, e.g. `bemuse-puru_toki-toki_hyper14.bms`, `bemuse-ice_l-L__DPA_.bms`, the `*_14*_YH.bms` anhedonia charts, `*14key*` Blooming charts, `*Dp*` Lyzoande charts), 18 Shift_JIS (CP932) charts, UTF-8 ones, `#RANDOM`, `#LNOBJ` and `#LNTYPE 1` charts, STOP and extended BPM, `SC`/`SP` scroll channels. The repository README says "Each song is copyrighted by respective author" (accepted-risk, chart files only). Seven tiny asdfghjkoiuy/iBMSCPP parser stubs (`ibmscpp-*`; mixed CR/CRLF/LF, UTF-8 BOM, CP932, nested `#RANDOM`, 10K/14K lane stubs) are committed too; that repository has no licence file. Per-file rows: [`samples/SOURCES.md`](samples/SOURCES.md).
- **Not found**: a real chart wider than 14K+2 scratches (24K, 48K): be-music's README lists "24 KEY SP" and "48 KEY DP" modes, but its example folder has no such chart; the `bemusic/music` index contains none either.
- **How to get more**: BMS Search (https://bmssearch.net/) finds a song and links the distribution page; BMS events (BMS of Fighters, https://manbow.nothing.sh/event/ - the Bemuse song READMEs link each song to its event page - and the event lists at https://hitkey.nekokan.dyndns.info/bmsevt.htm and https://bms.ms/bmsevtalt) publish packs, mostly with audio; starter packs recommended by the Bemuse FAQ (https://faq.bemuse.ninja/): GENOSIDE 2018 (http://nekokan.dyndns.info/~lobsak/genocide/grade.html), GENOSIDE (http://nekokan.dyndns.info/~lobsak/genoside/), the list at https://bms-community.github.io/resources/#starter-packs; pack archives at https://www.bmsworld.nz/ . Editors that write BMS: iBMSC (https://github.com/aqtq314/iBMSC), BMSE, BMS Creator, GDA Creator. Search terms: `BMS`, `BMS of Fighters`, `GENOSIDE`, `.bms .bme .bml` + song name. Packs are third-party works with their own terms; only the chart file (no `#WAV` audio) is kept here.

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
- Repo samples: `samples/`, `../bme/samples/`; original list: `ORIGINAL_README.md` (lines on `.bms/.bme/.bml`).
- Sample sources (see `samples/SOURCES.md`): bms-rs https://github.com/MikuroXina/bms-rs/tree/1eb789caa32a3e0851d274723468576de26a2d08/tests ; Bemuse https://github.com/bemusic/bemuse/tree/4bf3e7d98a44841b323741cc403ecb7b41618ade ; Angolmois https://github.com/lifthrasiir/angolmois/tree/625f8431556b8772b13a826d48a1becd228a8b1c/test ; rparser https://github.com/rhythmus-emulator/rparser/tree/d2efba4c36e5f74fda3da4b90f7e9119f1f62861/test ; Bemuse songs https://github.com/bemusic/music/tree/472b0f3cc433c39b0a7e9849705b34af68bf5400 ; Nekokan/be-music https://github.com/Nekokan/be-music/tree/a1b770446227c3e678e9a079078e8831edc8886c/examples/test ; shuymn/tapestry https://github.com/shuymn/tapestry/tree/cf1cc4b55deeffdd32fb43f47b89f550a92fb9a3/crates/bms-parser/tests/charts ; sappho192/BMSParser https://github.com/sappho192/BMSParser/tree/f90ae7cb7eed2d7738230283925c44a720e1664c/Resource
