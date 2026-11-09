# DTXMania chart (`.dtx`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS or UTF-8, line-based, BMS-style)

## Overview
DTX is the chart format of DTXMania, a free GuitarFreaks/DrumMania simulator (see [README](../README.md)). It is a BMS dialect: header commands `#NAME: value`, resource tables `#WAVzz`, `#BPMzz`, `#AVIzz`, `#BMPzz`, and measure data lines `#mmmcc: <objects>`. One `.dtx` file is one chart (one difficulty, one or more instruments: drums, guitar, bass). Files are grouped into a song with [set.def](../set-def/README.md) or by folder. Archives hold the DTX files, audio (OGG/WAV/MP3/XA), banner/preview image, BGA video and `.score.ini` files ([samples listing](samples/README.md)). Editor: DTXCreator (`DTXCreator` in the DTXmaniaNX repo; writes `#DTXC_*` metadata). Chart library: http://files.pinoypercussionfreaks.com/.

## Container & encoding
- [observed: `dtxtopng_example_input_file_4.dtx`, DTXCreatorAL 010] A DTX may be UTF-16LE with BOM (`FF FE`). The BocuD fork loader detects UTF-8 BOM, UTF-16 LE/BE BOMs, valid UTF-8, else Shift_JIS (`ChartTextEncoding.cs`, https://github.com/BocuD/DTXmaniaNX). [observed: dtx2gp_test4.dtx] `#WAVzz` ids use base 36 beyond hex (`#WAV0G`, `#WAV0I`) and values may be followed by `;` comments.
- Lines end with `\n` (CRLF accepted). Of the sample files, 4 are plain ASCII/UTF-8-clean, 6 are not valid UTF-8 (Shift_JIS or similar), none has a BOM.
- Line grammar (from `t入力_コマンド文字列を抜き出す` etc.): optional spaces, `#`, command = text up to `:`, space, `;` or newline; optional spaces; parameter = text until newline or `;`. `;` starts a comment to end of line; a line starting with `;` is a comment. A command may be glued to its parameter (`#TITLE foo`, `#BPM 120`): `t入力_パラメータ食い込みチェック` splits a longer command name on the known prefix.
- Command names are case-insensitive. Matching uses `StartsWith`, so order matters: `PATH_WAV` before `PATH`, `BACKGROUND_GR` before `BACKGROUND`.
- Numbers use `.` or `,` as decimal point (custom `TryParse`).

## Structure / metadata
Header commands read by `CDTX.t入力_行解析` (DTXmaniaNX):

| Command | Meaning |
|---|---|
| `#TITLE`, `#ARTIST`, `#COMMENT`, `#GENRE` | free text |
| `#DLEVEL` / `#PLAYLEVEL`, `#GLEVEL`, `#BLEVEL` | drum / guitar / bass level, int 0..1000 clamped; value >= 100 is split as level = value/10 plus decimal digit (`#DLVDEC`, `#GLVDEC`, `#BLVDEC` hold the decimal part in newer versions; `#HIDDENLEVEL`) |
| `#BPM: x` | base/representative BPM (same as `#BPM00`); `x` > 0 |
| `#BASEBPM: x` | offset added to the BPM values of channel 03 and of `#BPMzz` (zz != 00) |
| `#DTXVPLAYSPEED: x` | speed factor of DTXViewer playback (>0) |
| `#PANEL` | text shown on the panel; if numeric it is treated as the EL panpot (ambiguity noted in source) |
| `#PREVIEW`, `#PREIMAGE`, `#PREMOVIE`, `#STAGEFILE`, `#BACKGROUND` / `#WALL`, `#BACKGROUND_GR`, `#RESULTIMAGE`, `#RESULTMOVIE`, `#RESULTSOUND` | preview audio/image/movie, loading-screen image, backgrounds, per-rank result media |
| `#SOUND_NOWLOADING`, `#SOUND_STAGEFAILED`, `#SOUND_FULLCOMBO`, `#SOUND_AUDIENCE` | sound overrides |
| `#PATH`, `#PATH_WAV` | base folder for resources |
| `#RANDOM n`, `#IF m`, `#ENDIF` | conditional blocks (random 1..n; up to 255 nesting) as in BMS |
| `#MIDIFILE`, `#MIDINOTE`, `#BLACKCOLORKEY`, `#FORCINGXG`, `#VOL7FTO64`, `#SUPRESSNOTEOFF_HIHAT/GUITAR/BASS`, `#BGMWAV` (DTXCreator output) | misc |
| `#DTXC_*` (e.g. `#DTXC_CHIPPALETTE`, `#DTXC_LANEBINDEDCHIP`, `#DTXC_WAVFORECOLOR`) | DTXCreator editor metadata |

Resource tables (index `zz` = 2 chars base 36, `00`..`ZZ`, at most 36*36 entries):
- `#WAVzz: file` (audio), `#VOLUMEzz: 0..100` (alias `#WAVVOLzz`), `#PANzz: -100..100` (alias `#WAVPANzz`; `#PANELzz`), `#SIZEzz` (chip display size).
- `#BPMzz: x` BPM table used by channel 08.
- `#AVIzz: file` / `#VIDEOzz`, `#AVIPANzz`, `#BMPzz`, `#BMPTEXzz`, `#BGAzz: bmp x1 y1 x2 y2 ox oy` (7 params), `#BGAPANzz`.
- `#00002:`-style lines are data lines, below.
- Forward references are allowed: the parser patches chips when the `#WAVzz` is defined ("無限管理"). A later redefinition of the same zz applies to the chips that follow.

## Timing model
- Data line: `#mmmcc: oooo...`. `mmm` = 3-char measure number: first char base-36 (`0-9A-Z`, value*100), next two decimal digits; `000`..`Z99` = 0..3599 (`CConversion.nConvert3DigitMeasureNumberToNumber`). `cc` = 2 hex digits = channel. The object string is a sequence of 2-char base-36 object ids (`00` = empty); `_` characters are ignored; an odd trailing char is dropped. Object k of n sits at `k/n` of the measure.
- Internal position: the parser adds one empty leading measure and uses 384 ticks per measure: `pos = (measure+1)*384 + (384*k)/n` (`(384*i)/n` integer division, resolution 1/384).
- Channel 02: measure length multiplier (real number, e.g. `#00002: 1.5`), whole line = one value. It applies to that measure only for BMS/BME and persists for DTX until changed [inference from `CDTX` timing loop: for BMS/BME `dbBarLength` is reset to 1.0 at the next measure, for DTX it is not].
- Channel 03: BPM change, objects are 2-digit hex values; BPM = `BASEBPM + value`.
- Channel 08: extended BPM, object = `zz` index into `#BPMzz`; BPM = `#BPMzz` value (plus `BASEBPM` unless zz = 00).
- Initial BPM: `#BPM`. If no BPM chip sits at position 0, the parser inserts one using the BPM (or 120 if undefined).
- Time of a chip: DTXmania `tComputeChipPlayTimeMs`: `t = t_anchor + 0x271 * (pos - pos_anchor) * barLength / bpm` ms (0x271 = 625; 625*384 = 240000, so a 384-tick measure of length 1 lasts 240000/bpm ms = 4 beats). The anchor resets at each BPM/bar length change. Mode 0 floors to ms.
- No stops, warps or scroll speed changes.

## Notes
Channel = 2 hex digits (`EChannel.cs`):

| Ch | Meaning |
|---|---|
| 01 | BGM (auto-play sample, WAV id) |
| 02 | bar length |
| 03 | BPM (hex) |
| 04, 07, 55-59, 60 | BGA layers 1, 2, 3-7, 8 (BMP id; `C4`, `C7`, `D5-D9`, `E0` = layer-swap variants of the same layers) |
| 05, 06, 09, 0A | unused/ reserved (ExObj, miss animation, BMS reserved) |
| 08 | extended BPM |
| 11 | hi-hat (close) |
| 12 | snare |
| 13 | bass drum |
| 14 | high tom |
| 15 | low tom |
| 16 | right crash (cymbal) |
| 17 | floor tom |
| 18 | hi-hat open |
| 19 | ride |
| 1A | left crash/cymbal |
| 1B | left pedal (HH pedal) |
| 1C | left bass drum |
| 1F | drum fill-in marker (`DrumsFillin`); 53 = FillIn |
| 20 | guitar open |
| 21-27 | guitar chords RGB: 21 B, 22 G, 23 GB, 24 R, 25 RB, 26 RG, 27 RGB (20 = none/open) |
| 28 | guitar wailing; 29 flow-speed (unused); 2C / 2D guitar / bass hold-note (DTXManiaAL); 2F wailing sound |
| 30 | flowspeed (drums, unused) |
| 31-3C | hidden drums (HH close, SD, BD, HT, LT, CY, FT, HH open, RD, LC, LP, LBD) |
| 4C-4F | bonus effects (`4F` appears in the samples) |
| 50 / 51 | bar line / beat line; 52 MIDI chorus; 54 movie; 5A full-screen movie |
| 61-69, 70-79, 80-89, 90-92 | sound effects SE01..SE32 (WAV ids; 61-69 = SE01-09, 70-79 = SE10-19, 80-89 = SE20-29, 90-92 = SE30-32) |
| 93-9F, A9-AF, D0-D3 | extended guitar combinations with Y (yellow) and P (pink) buttons (XG) |
| A0 | bass open; A1-A7 bass RGB combos (same pattern as 21-27); A8 bass wailing |
| C5, C6, C8-CF, DA-DF, E1-E8 | extended bass combinations |
| B1-BE | `*_NoChip` variants (`HiHatClose_NoChip` ... `LeftBassDrum_NoChip`; BA = guitar, BB = bass NoChip) |
| C1/C2 | beat line shift / display |
| EC, ED, EE, EF | click, first sound chip, mixer add / remove |

Channel numbers are the decimal values of the `EChannel` enum in `EChannel.cs` written in hex (e.g. `HiHatClose = 17` = `0x11`). Full extended guitar/bass tables: [Extended DTX Data Format wiki](https://github.com/limyz/DTXmaniaNX/wiki/Extended-DTX-Data-Format).
- Object value = base-36 WAV id of the keysound played when the chip is hit (and the sound id for auto-play).
- Hold notes: guitar/bass only, DTXManiaAL: channel 2C (guitar) / 2D (bass); `01` = start, other = end. Rules per wiki: start coincides with a press chip, end must not coincide with a press, nothing between, value not 00. No long notes for drums.
- Lane count: drums 10 channels (11-1C, minus 1D/1E), guitar/bass 3 colors in classic DTX (5 in XG) + open + wailing.
- Notes on the same lane at the same position overlap; chips need a WAV id (can be a rest sample).

## Audio & images
Audio is the `#WAVzz` table (OGG/WAV/MP3/XA). Background music is usually channel 01 chips (or `#BGMWAV zz` in DTXCreator output). Video: `#AVIzz` + chip channel 54 (`OceanAvenueMST.dtx` uses `#AVI01: bgv.avi` and `#00054: 000100...`). Images: `#BMPzz`/`#BGAzz` + channels 04/07/55-60.

## Versions & variants
- DTXMania (kairera0467 / yyagi lineage), DTXManiaXG (ver K adds XG lanes 1B/1C and Y/P guitar buttons), DTXManiaAL (hold notes 2C/2D), DTXManiaNX (limyz), BocuD/DTXmaniaNX, DTXMania 4.x (https://dtxmania.net/). The "Extended DTX Data Format" wiki documents XG/AL additions. The same parser class reads BMS/BME/MIDI.
- Arcade GITADORA charts circulate converted to DTX (e.g. GDAmania blog "Changed all format to DTX files").
- Older formats: [gda](../gda/README.md), [g2d](../g2d/README.md).

## Quirks & pitfalls
- Resource ids are base-36 but channel 03 BPM objects are hex.
- A `.dtx` may hold drums + guitar + bass (sample headers show `#GLEVEL`/`#BLEVEL` 0 in drum-only files).
- Bar length: per measure (BMS) vs persistent (DTX) [inference].

## Example
Excerpt from `samples/OceanAvenueMST.dtx` (first lines):

```
#TITLE: Ocean Avenue
#ARTIST: Yellowcard
#PREVIEW: pre.ogg
#PREIMAGE: banner.jpg
#BPM: 173.00
#DLEVEL: 76
#WAV01: METRO.OGG
#VOLUME01: 50
#WAV02: bgmoceanavenue.ogg
...
#BPM01: 119
#00002: 1.5
#00054: 000100000000000000000000
#00316: 0000001F
#00411: 0J0K0J0K0J0K0J0K
#00608: 0U
```
`#00608: 0U` = measure 6, channel 08 (ext. BPM), object `0U` = `#BPM0U: 178`. `#00411: 0J0K...` = measure 4, hi-hat (11), 8 slots, samples 0J/0K alternating.

## ROX support
Decode only (`rox::formats::dtx`, `DtxDecoder`: `variants`, `decode_variant`, `decode_with_report`, `decode_with_audio_plan`; `auto_decode_all` names the charts `Drums`, `Guitar`, `Bass`). One chart per instrument that has chips.
- Drums: columns `LC HH SD HT BD LT FT CY RD` as used; the left pedal / left bass drum lane folds onto the bass drum, open hi-hat onto hi-hat.
- Guitar/bass: `Open R G B` (4 columns) or `Open R G B Y P` (6); one note per button of a chord channel; holds from `2C`/`2D`.
- Dropped and counted: hidden chips, blank-hit settings, wailing, fill-ins, pictures, bar lines, unknown channels. Not handled: `.gda`/`.g2d`, `set.def`, `#DTXVPLAYSPEED`, pan.
- Timing follows the game (384 ticks, integer division, persistent bar length). The audio plan holds channel `01`, the effect channels and every chip's sound.
- Settled from `CDTX.cs`: hold pairing ignores the marker values, `#BPM00` is the FIRST one and takes no `#BASEBPM`, default BPM 120, bar length persists (the inference above is right), `#IF` before any `#RANDOM` reads 0.

## Parsers & tools
- DTXmaniaNX (C#): https://github.com/limyz/DTXmaniaNX (CDTX.cs parser; DTXCreator writer `DTXCreator/Code/00.App/CDTXInputOutput.cs`)
- DTXMania (official): https://dtxmania.net/ ; DTXMania Wiki (osdn): "DTX data format" (unreachable).
- BocuD fork: https://github.com/BocuD/DTXmaniaNX ; DTXmaniaNXPLUS: https://github.com/mee19mc/DTXmaniaNXPLUS ; DeepWiki: https://deepwiki.com/limyz/DTXmaniaNX
- Chart library: http://files.pinoypercussionfreaks.com/ (from original README)

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: community chart libraries (http://files.pinoypercussionfreaks.com/), the DTXMania download area (https://osdn.net/projects/dtxmania/releases/ and https://dtxmania.net/), YouTube channels with chart links (APPROVED DTX Gaming, Furukon Rhythm Gaming: named in the DTXmaniaNX README), the editors DTXCreator (in https://github.com/limyz/DTXmaniaNX) and DTXManiaXG Creator (https://drumgamer.weebly.com/tools2.html), and converters that write DTX: `seqtool.py` of https://github.com/fisyher/gitadora-customs (SQ3 to DTX, needs game data) and the DTX Charter viewer https://fisyher.github.io/dtxcharter. Most charts are fan transcriptions of commercial songs: check each author's terms. Search terms: "DTXMania dtx simfile", "DTXMania chart download", "ドラムマニア dtx".

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs , EChannel.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/FDK/Code/00.Common/CConversion.cs (`CConversion.cs`)
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs (`DTXCreator/CDTXInputOutput.cs`)
- https://github.com/limyz/DTXmaniaNX/wiki/Extended-DTX-Data-Format
- https://dtxmania.net/documents/create-setdef
- local samples in samples/
