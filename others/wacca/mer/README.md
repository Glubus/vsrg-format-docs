# MER (`.mer`, WACCA / Mercury chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (space-separated columns, `#` metadata header, `#BODY` marker)

## Overview

`.mer` is the text chart format of WACCA's "Mercury" engine as handled by the community chart editors (BAKKA, then **MercuryMapper** by Yasu3D, a "forked from BAKKA-Avalonia" rewrite). Everything below is taken from MercuryMapper's `FormatHandler.cs`, `Note`/`Gimmick` code and enums, i.e. what that editor reads and writes; fields it ignores or does not model (e.g. the R-note extras) are marked. The editor also has two native dialects: `.map` (editor-saved Mercury text) and **SAT** ("Saturn"), a labelled format with `@COMMENTS` / `@GIMMICKS` / `@OBJECTS` sections and symbolic note types (format version "2").

Category: **others** — see [../README.md](../README.md).

## Container & encoding

Text, one record per line. Metadata lines start with `#`; the line `#BODY` separates metadata from content; content lines are whitespace-separated integers/floats (the writer pads them with `{,4}` widths). Reader: splits on spaces, requires ≥ 3 columns. Files carry no compression. UTF-8/ASCII.

## Structure / metadata

Header lines recognised by MercuryMapper (names with `EDITOR_` prefix are the editor's own copies, e.g. `#EDITOR_AUDIO`):

| Tag | Meaning |
|---|---|
| `#MUSIC_SCORE_ID`, `#MUSIC_SCORE_VERSION`, `#GAME_VERSION`, `#MUSIC_FILE_PATH` | written as `0`, `0`, empty, empty by the editor |
| `#OFFSET` | audio offset (seconds, 6 decimals) |
| `#MOVIEOFFSET` | background-video offset |
| `#AUDIO`, `#AUTHOR`, `#LEVEL`, `#CLEAR_THRESHOLD`, `#PREVIEW_TIME`, `#PREVIEW_LENGTH` | editor metadata (also as `#EDITOR_*`) |
| `#BODY` | end of header |

### Body lines

`measure tick objectId [arguments…]`, `measure ≥ 0`, `tick` in `[0, 1920)` (1920 ticks per measure = 4/4 beat grid, i.e. 480 per beat; the editor normalises `tick ≥ 1920` into the next measure).

| objectId | Meaning | Arguments |
|---|---|---|
| `1` | **note** | `noteTypeId noteIndex position size renderSegment [extra]` where the optional last column is `maskDirection` (masks 12/13) or `nextIndex` (hold start/segments) |
| `2` | BPM change | `bpm` |
| `3` | time signature | `upper lower` (old files may carry only the upper part, lower = 4) |
| `5` | hi-speed change | `speed` |
| `6` | reverse effect start | – |
| `7` | reverse effect end | – |
| `8` | reverse note end | – |
| `9` | stop start | – |
| `10` | stop end | – |
| `11` | end of chart (gimmick) | – (the editor writes the end marker as a note line `… 1 14 <noteCount> 0 60 1`) |

`position` is `0–59` (angular segment index, wraps modulo 60) and `size` `1–60` segments (editor clamps); `noteIndex` is a running id used to link multi-part notes: for a Hold start (9/25) and segments (10) the **last column is the index of the next hold part**; for masks (12/13) it is the mask direction `0` counter-clockwise, `1` clockwise, `2` centre. `renderSegment` (0/1) only matters for hold segments (type 10).

### Note type IDs (MER IDs)

| ID | Note (MercuryMapper enum) | Bonus |
|---|---|---|
| 1 | Touch | none |
| 2 | Touch | Bonus (effect) |
| 3 | Snap forward (`SnapForward`) | – |
| 4 | Snap backward (`SnapBackward`) | – |
| 5 | Slide clockwise | none |
| 6 | Slide clockwise | Bonus |
| 7 | Slide counter-clockwise | none |
| 8 | Slide counter-clockwise | Bonus |
| 9 | Hold start | – |
| 10 | Hold segment / point | – |
| 11 | Hold end | – |
| 12 | Mask add | – |
| 13 | Mask remove | – |
| 14 | End of chart marker | – |
| 16 | Chain | – |
| 20, 21, 22, 23, 24, 25, 26 | R-Note variants of Touch, Snap fwd, Snap back, Slide CW, Slide CCW, Hold start, Chain | R-Note |

(MercuryMapper additionally models "Damage" = 27 and "Trace" = 28 as editor-only types that are **not exported to MER**; 13–26 are "occupied by MER R-Note IDs".)

## Timing model

Position = `(measure, tick)` with 1920 ticks per measure (MercuryMapper's `FullTick = Measure·1920 + Tick`); BPM / time-signature / hi-speed / stop / reverse are objects on the same grid. Time follows from the BPM history (`#OFFSET` is the audio offset); how a non-4/4 time signature changes the measure's real length is not verified from the sources opened (MercuryMapper builds "metre events" and "time scales" from the gimmicks). `Stop` and `Reverse` gimmicks alter scroll/time mapping. No fractional ticks.

## Notes

Touch, snap (forward/backward), slides CW/CCW, hold (start + segments + end linked by indices, with `render` flag per segment), chain, masks (hide parts of the ring: add/remove, direction), bonus effect flag (even IDs 2/6/8), R-notes (IDs 20–26; meaning of "R-Note" not documented in the sources) and gimmicks. Simultaneous notes share (measure, tick). Width up to 60 = full ring.

## Audio & images

`#MUSIC_FILE_PATH` (empty in editor output), `#EDITOR_AUDIO`/`#AUDIO` (relative path), `#MOVIEOFFSET` for background video, preview via `#PREVIEW_TIME`/`#PREVIEW_LENGTH`.

## Versions & variants

- **MER** (game-like, numeric IDs).
- **MercuryMapper `.map`** (editor-saved Mercury text), **SAT v2** (`@COMMENTS`, `@GIMMICKS`, `@OBJECTS`; symbolic types; also supports comments and trace/damage notes).
- Official arcade data is not plaintext/accessible in the sources opened.

## Quirks & pitfalls

- `size`/`position` ranges: wrap modulo 60 and clamp 1–60.
- Hold links are by `noteIndex`; indices must be unique and the chain consistent (the editor repairs notes after load).
- Old files may lack the denominator in `3`.
- Reading requires `#BODY`; missing it returns without loading.
- The end-of-chart note (type 14) is stored as a note line but belongs to the gimmick list.
- Data not modelled by MercuryMapper (some R-note fields, unknown gimmicks) may be lost on round trip.

## Example

None taken verbatim from a source (no complete sample file was opened). Illustrative, hand-built from the writer code of MercuryMapper (`FormatHandler.WriteFile`):

```
#MUSIC_SCORE_ID 0
#MUSIC_SCORE_VERSION 0
#GAME_VERSION
#MUSIC_FILE_PATH
#OFFSET 0.000000
#MOVIEOFFSET 0.000000
#BODY
   0    0    2 120.000000
   0    0    3     4     4
   1    0    1    1    0    0   15    1
   2    0    1   14    1    0   60    1
```

(BPM 120, 4/4, one Touch at position 0 size 15 in measure 1, end-of-chart marker in measure 2.)

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [Yasu3D/MercuryMapper](https://github.com/Yasu3D/MercuryMapper) (C#/Avalonia; `Data/FormatHandler.cs`, `Enums/NoteType.cs`, `Enums/GimmickType.cs`, `Data/ChartElement.cs`)
- [WenqiOfficial/MercuryPlayerPlus](https://github.com/WenqiOfficial/MercuryPlayerPlus) (map player)
- BAKKA / BAKKA-Avalonia (earlier editors), Saturn (SAT) tools

## Sources

- <https://github.com/Yasu3D/MercuryMapper> (source files read: `FormatHandler.cs`, `ChartElement.cs`, `Chart.cs`, enum files)
- <https://github.com/WenqiOfficial/MercuryPlayerPlus> (search result)
- <https://en.wikipedia.org/wiki/Wacca_(video_game)> (hardware description)
