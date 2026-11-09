# UGC (`.ugc`, UMIGURI Chart v8)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text (UTF-8, LF or CRLF, tab-separated header lines)

## Overview

`.ugc` ("UMIGURI Chart") is the native chart format of **UMIGURI**, a free CHUNITHM simulator by inonote (Windows, closed source) and of its chart editor **Margrete** (it "outputs UMIGURI Chart format (*.ugc)"). It is the most documented CHUNITHM-style format: the author publishes a specification gist ("Umiguri Chart v8 仕様"). A UGC file contains **one chart** (one difficulty) with its own metadata, audio/jacket references, BPM/beat/speed definitions and note lines. UMIGURI also reads `.sus` (see [../sus/](../sus/README.md)) with limitations.

## Container & encoding

- Extension `.ugc`, UTF-8, LF or CRLF. **One line = one command or one note.** Lines that do not start with `@` or `#` are ignored; lines with missing parameters are ignored; comment lines start with `'`.
- `@` lines are header commands, parameters separated by **horizontal tabs**. `#` lines are notes: `#BarTick:` followed by a compact note code (see below).
- Time is written `Bar'Tick` ("BarTick format"), e.g. bar 0, tick 240 → `0'240`.
- Files sit in `data/music/<Genre>/<Song folder>/` next to the audio (WAV, MP3, OGG, M4A recommended, FLAC, WebM) and jacket (PNG/BMP/JPEG/GIF/DDS 400×400 recommended).

## Structure / metadata

Header commands (all `@NAME<TAB>params`; parameters in order):

| Command | Parameters / meaning |
|---|---|
| `VER` | version, always `8` |
| `EXVER` | extension version 0/1; `1` = behaves as if `FLAG:EXLONG TRUE` (always 1 in UMIGURI NEXT) |
| `TITLE`, `SORT`, `ARTIST`, `GENRE`, `DESIGN` | title; sort key (uppercase, katakana, no symbols…); artist; genre (default = parent folder name); chart designer |
| `DIFF` | BASIC 0, ADVANCED 1, EXPERT 2, MASTER 3, WORLD'S END 4, ULTIMA 5 |
| `LEVEL` | play level text (star count for World's End), `WEATTR` World's End attribute (one kanji/fullwidth symbol), `CONST` chart constant |
| `SONGID`, `RLDATE` | song id (shared across difficulties except WE), release date `YYYYMMDD` |
| `BGM`, `BGMOFS`, `BGMPRV` | audio file; **offset in seconds (positive = delay playback, negative = advance)**; preview start/end seconds |
| `JACKET`, `BGIMG`, `BGSCENE`, `BGMODE`, `FLDCOL`, `FLDSCENE` | jacket, background image/video (MP4/AVI), 3D background scene id, background mode (`PASSIVE TRUE/FALSE`), field separator colour index (−1 auto … 8 purple), field scene |
| `TICKS` | time resolution, always 480 |
| `MAINBPM`, `MAINTIL`, `CLKCNT` | reference BPM, reference timeline id (0), count-in clicks (default = numerator of first bar) |
| `FLAG` | `DIFFTTL` (tutorial, keep FALSE), `SOFFSET` (insert one empty bar at start), `CLICK`, `EXLONG`, `BGMWCMP`, `HIPRECISION` (high-resolution AIR) with `TRUE/FALSE` |
| `BPM` | `BarTick  bpm` |
| `BEAT` | `Bar  Numer  Denom` |
| `TIL` | `TimelineId  BarTick  Speed` — timeline-wide scroll speed (soflan) |
| `SPDMOD` | `BarTick  Speed` — note speed definition |
| `SPDDEF` (v2.01) | `SpdId  OffsetTick  Speed` — note-speed definition (Ex) |
| `SPDFLD` (v2.01) | `SpdId  BarTick  X  Width  Length` — apply speed definition to a field area |
| `USETIL` | `TimelineId` — special: following note lines belong to that timeline |

## Timing model

Position is `Bar'Tick`; `BEAT` defines the meter per bar and `BPM` the tempo from a given BarTick, so absolute time = integrate bar lengths with the active BPM. `TICKS` is 480; with 4/4 a bar is 1920 ticks (the converter mgxc2s uses 1920 ticks per measure) [inference: ticks per beat = 480, per bar = 480·4·numer/denom]. The audio offset is `BGMOFS` (the author recommends keeping it at 0 and adjusting the audio file instead). `FLAG:SOFFSET` shifts everything by one bar. `TIL`/`SPDMOD`/`SPDDEF` change drawing speed only (soflan), not judgement times; `USETIL` assigns subsequent notes to a timeline so that different notes can scroll at different speeds.

## Notes

Notes are `#BarTick:<type><x><width>[extra]` where `x` (lane, 0-based) and `width` are written in **base 36**. Parent notes use `BarTick`; child notes (hold ends, slide points…) use `#OffsetTick:` relative to their parent.

| Type char | Note | Syntax |
|---|---|---|
| `c` | click (count-in sound) | `#BarTick:c` |
| `t` | TAP | `#BarTick:txw` |
| `x` | ExTAP | `#BarTick:txwd` with effect `U D C A W L R I` (up, down, centre, clockwise, counter-clockwise, left, right, inside/outside) |
| `f` | FLICK | `#BarTick:txwd` with auto-play effect direction `A`uto, `L`, `R` |
| `d` | DAMAGE (mine) | `#BarTick:txw` |
| `h` | HOLD | parent `#BarTick:txw`; child end `#OffsetTick:s` |
| `s` | SLIDE | parent `#BarTick:txw`; children: `#OffsetTick:txw` with type `s` = relay/end node, or type `c` = control point |
| `a` | AIR | `#BarTick:txwddc` — `dd` ∈ `UC UL UR DC DL DR`; colour `N` normal (up green / down pink) or `I` inverted; needs a parent note |
| `H` | AIR-HOLD | `#BarTick:txwc`; children: `#OffsetTick:s` relay/end, `#OffsetTick:c` end without AIR-ACTION |
| `S` | AIR-SLIDE | `#BarTick:txwhhc`; `hh` = height ×10 in two base-36 digits; children `#OffsetTick:txwhh` type `s` (relay/end) or `c` (control / end without AIR-ACTION) |
| `C` | AIR-CRUSH (also decoration-only AIR-TRACE) | `#BarTick:txwhhc,{interval}` — `c` colour `0` normal `1` red `2` orange `3` yellow `4` yellow-green `5` green `6` aqua `7` sky `8` heaven `9` blue `A` blue-purple `Y` magenta `B` pink `C` white `D` black `Z` transparent; `{interval}` decimal tick spacing of combo-producing points (`0` = no combo notes, pure AIR-TRACE decoration; `$` = only the start generates combo); children `#OffsetTick:txwhh` type `c` |

Simultaneous notes share a BarTick. There are 16 lanes (x 0–15) in CHUNITHM; the spec states only base-36 for `x`/`w`. Overtaking ("追い越し") notes are supported by Margrete.

## Audio & images

`BGM`, `BGMOFS`, `BGMPRV`, `JACKET`, `BGIMG` (video allowed), `BGSCENE`/`FLDSCENE` 3D scenes. No keysounds.

## Versions & variants

Spec title "v8" (`VER 8`); `EXVER`, `SPDDEF`/`SPDFLD` appeared with UMIGURI v2.01; UMIGURI NEXT forces EXLONG. Margrete's own container is `.mgxc` (converted by Margrete2S/mgxc2s; the text dump read by mgxc2s uses `BEGIN META` / `BEGIN HEADER` / `BEGIN NOTES` blocks with keys `TITLE ARTIST DESIGNER DIFFICULTY PLAYLEVEL SONGID BGM BGMOFFSET JACKET MAINBPM EXLONG`, header lines `BPM`, `BEAT`, `TIL`, `SPDMOD`, and 10-column note lines with dotted nesting `t`, `e`, `f`, `d`, `h`, `s`, `a`, `H`, `S`, `C`). Not to be confused with the c2s dialect ([../c2s/](../c2s/README.md)).

## Quirks & pitfalls

- Header values are tab-separated; note codes are base-36 (case?) — spec does not say; assume lowercase digits.
- Missing parameters → line silently ignored.
- AIR/AIR-HOLD/AIR-SLIDE/AIR-CRUSH need a parent note; orphan AIRs are dropped (when loaded from SUS in UMIGURI).
- `hh` heights are ×10.
- `{interval}` in `C` is decimal while other fields are base 36.
- `BGMOFS` sign: positive delays the audio.
- UMIGURI forces SUS-loaded FLICK/AIR widths to the nearest of 1, 2, 3, 4, 6, 8, 16 and ignores AIR-HOLD height/AIR-ACTION position.

## Example

None of the primary sources contains a complete UGC example; the following is illustrative, hand-built from the rules above (not a real file):

```
@VER	8
@TICKS	480
@MAINBPM	140
@BPM	0'0	140
@BEAT	0	4	4
#0'0:t0g
#0'480:h44
#960:s
```

(`t0g` = TAP at lane 0, width `g` = 16 in base 36, i.e. all 16 lanes; `h44` = HOLD at lane 4, width 4, starting at bar 0 tick 480; the child line `#960:s` is its end, 960 ticks after the parent [relative-offset semantics inferred from the `#OffsetTick:` notation].)

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- UMIGURI (inonote, closed) and **Margrete** (editor): <https://umgr.inonote.jp/en/margrete/intro>, <https://margrete.inonote.jp>
- Margrete2S / [mgxc2s](https://github.com/sbga-tech/mgxc2s) (C#): `.mgxc` text → c2s
- [MuNET-OSS/ChuChartManager](https://github.com/MuNET-OSS) (UGC ↔ C2S)
- [mkpoli/sus-io](https://github.com/mkpoli/sus-io) (SUS only)

## Getting samples

- **Committed**: 4 file(s) in [`samples/`](samples/) (see samples/SOURCES.md for origin, author and licence of each).
- **Manifest**: none.
- **More samples**: UGC files are written by the Margrete editor (the header comment of every committed file says "Created with Margrete vX"); MuConvert (LGPL-3.0) keeps example UGC files in `tests/chu/testset/自制谱/`; the UMIGURI documentation (https://umgr.inonote.jp/) explains how songs and charts are added. Charts are shared by the CHUNITHM simulator community [inference].

## Sources

- <https://gist.github.com/inonote/5c01e73781cab17765a1d93641d52298> ("Umiguri Chart v8 仕様", read in full)
- <https://umgr.inonote.jp/en/docs/user-content/add-songs>, <https://umgr.inonote.jp/docs/others/chart-sus>, <https://umgr.inonote.jp/en/margrete/intro>
- <https://github.com/sbga-tech/mgxc2s> (`Parser.cs`, `Notes.cs`)
