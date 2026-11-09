# EVE (`.eve`, jubeat chart events)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text (ASCII, `time,command,value` lines)

## Overview

`.eve` is the plain-text event list the jubeat arcade game uses for charts (one file per difficulty, named after the difficulty, e.g. `bsc.eve`, `adv.eve`, `ext.eve`). It has no header: it is a flat sequence of timed commands. The format is read/written by **jubeatools** (Stepland) — whose `konami/commons.py` and `eve/load.py` are the main source here — and by `Jubeat-MemonEveConverter` (C), enabling F.E.I.S/memon charts to be used on arcade-compatible jubeat setups. The compiled binary equivalent is [jbsq](../jbsq/README.md).

## Container & encoding

ASCII text (jubeatools reads `ascii`), split on `\n`, blank lines ignored. Each line has **exactly three comma-separated fields**: `time, command, value`; whitespace around fields is trimmed (jubeatools writes them right-aligned: `{time:>8},{command:<8},{value:>8}`). Folder loader globs `*.eve`; the difficulty is guessed from the file stem (`BSC`/`ADV`/`EXT`), default EXTREME.

## Structure / metadata

| Field | Meaning |
|---|---|
| `time` | integer tick; **300 ticks per second** |
| `command` | one of `END`, `MEASURE`, `HAKU`, `PLAY`, `LONG`, `TEMPO` |
| `value` | integer; meaning depends on command |

| Command | Value | Meaning |
|---|---|---|
| `TEMPO` | non-zero int `v` | set tempo; `BPM = 6·10⁷ / v` (v = µs per beat). Several lines possible; the first is at time 0 |
| `MEASURE` | 0 | marks a measure line |
| `HAKU` | 0 | marks a beat ("haku", 拍) line; irregular sequences allowed |
| `PLAY` | 0–15 | tap note on the panel index (4×4 grid; 16 panels; row-major order 0 = top-left … 15 = bottom-right is the usual convention [inference from `NotePosition.from_index`, not opened]) |
| `LONG` | packed int | long note (see below) |
| `END` | 0 | end of the chart (time of the last required event) |

### LONG value

`value = (duration << 8) | (length << 6) | (direction << 4) | position` where
- `position` (4 bits) = starting panel 0–15,
- `direction` (2 bits) = tail direction: `0` down, `1` up, `2` right, `3` left,
- `length` (2 bits) = tail length in panels, 1–3,
- `duration` = hold length in ticks (300 Hz), ≥ 0.
The tail tip must stay on the grid; only straight (horizontal/vertical) tails exist in `.eve` (diagonal tails cannot be represented).

## Timing model

Absolute time: `seconds = ticks / 300`. Tempo events are for display/beat markers and converters (the notes are placed in absolute time, not beats). To get beats, integrate `TEMPO` segments. The audio offset is not in the file (the first event time already includes it).

## Notes

Only two note kinds: `PLAY` (tap) and `LONG` (hold with a directional tail). No holds with release timing windows in the file. Simultaneous notes = identical `time`. `MEASURE`/`HAKU` are guide lines, not notes. The markers' animation timing (when a marker appears before its hit time) is a game constant.

## Audio & images

Not referenced.

## Versions & variants

Arcade jubeat `.eve` (this page); the same events in binary form in `.jbsq`. jubeat plus/jukebeat store them as `seq_bas/seq_adv/seq_ext` files inside `.jbt` zip packages (encrypted, see the Reflec Beat/iOS page).

## Quirks & pitfalls

- `TEMPO` value is the inverse of BPM: a zero value is invalid; jubeatools truncates the BPM to enough digits to recover the original value.
- Parsers must accept any order but lines are normally time-sorted; ties sorted by (time, command, value).
- `HAKU` lines can be irregular; jubeatools detects a regular 4/4 pattern and then drops them.
- The numeric command ids of the binary [`.jbsq`](../jbsq/README.md) (PLAY=1, END=2, MEASURE=3, HAKU=4, TEMPO=5, LONG=6) are **not** the same as the order in which jubeatools' `Command` enum lists the `.eve` commands (END=1, MEASURE=2, HAKU=3, PLAY=4, LONG=5, TEMPO=6); the text form uses names, so only matters when sorting events.
- Tail overflow outside the 4×4 grid is invalid.

## Example

Illustrative, hand-built from the rules above (not from a real chart): 

```
       0,TEMPO   ,  500000
       0,MEASURE ,       0
       0,HAKU    ,       0
     150,PLAY    ,       5
     300,HAKU    ,       0
     300,LONG    ,   76965
    1200,END     ,       0
```

(`500000` µs per beat = 120 BPM; a tap on panel 5 at 0.5 s; at 1.0 s a long note on panel 5 going right, tail length 2, duration 300 ticks = 1 s: `(300<<8) | (2<<6) | (2<<4) | 5 = 76800 + 128 + 32 + 5 = 76965`; END at 4 s.)

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [Stepland/jubeatools](https://github.com/Stepland/jubeatools) (Python; `formats/konami/eve`, `konami/commons.py`)
- [fishguy6564/Jubeat-MemonEveConverter](https://github.com/fishguy6564/Jubeat-MemonEveConverter) (C)

## Sources

- <https://raw.githubusercontent.com/Stepland/jubeatools/master/jubeatools/formats/konami/commons.py>, `.../konami/eve/load.py`, `.../konami/load_tools.py` (read)
- <https://github.com/fishguy6564/Jubeat-MemonEveConverter> (search snippet)
