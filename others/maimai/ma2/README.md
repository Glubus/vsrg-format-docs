# MA2 (`.ma2`, maimai DX chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (tab-separated, tick-based)

## Overview

`.ma2` is the official chart format of maimai DX ("the game used Ver. 1.03 of this format before maimai DX FESTiVAL", which moved to 1.04.00; MaiLib: "a machine-readable pseudocode… records each note in chronological order"). Files sit in the game data (`…/music/musicNNNNNN/NNNNNN_0D.ma2`, `D` = difficulty index 0 BASIC … 4 Re:MASTER, 5 Utage-like variants [inference from lcebot's output naming `000000_00 … 000000_05`]) next to `Music.xml`. The game reloads charts on every play, which is how custom charts are tested. Source: Littlebluemoon/ma2Research (black-box testing, "no reverse-engineering of binary files") plus converter READMEs. maimai classic: [../sdt/](../sdt/README.md). Category: others, see [../README.md](../README.md).

## Container & encoding

- Tab-separated text, numbering from 0 everywhere. UTF-8 (assumed).
- The engine skips meaningless or erroneous definitions and ignores extra trailing arguments, but an impossible value (e.g. note position 8) crashes the game.
- Notes are sorted by time. Within one timing, line order sets stacking (earlier = frontmost), mostly relevant to slides.
- Whether `.ma2` files ship encrypted (like classic `S*B`) is not stated in the sources opened. This page describes plaintext.

## Structure / metadata

### Header

| Line | Fields |
|---|---|
| `VERSION` | `0.00.00  1.04.00`: second value = chart-engine version (1.03.00 pre-FESTiVAL) |
| `FES_MODE` | `0`/`1`: 1 = Utage chart (special Utage modifiers unknown) |
| `BPM_DEF` | 4 floats: starting BPM, mode BPM (most time), max BPM, min BPM (3 decimals) |
| `MET_DEF` | `lower upper`, lower part first; cosmetic |
| `RESOLUTION` | ticks per measure, default 384 |
| `CLK_DEF` | count-in: `CLK_DEF / (RESOLUTION/4)` ticks play at the starting BPM |
| `COMPATIBLE_CODE` | always `MA2` |

BPM values use 3 decimals and "follow how the computer understands tempo". To store BPM `b`: take `60000000 / b`, round down to an integer, take `60000000 /` that, round down to the third decimal. Example: 275.000 is stored as 275.001.

### Timing lines

`BPM measure tick bpm` (must start with measure 0 tick 0), `MET measure tick lower upper` (cosmetic: each measure is always four beats).

### Note lines

`<modifier><TYPE> measure tick …`. Modifiers prefixed to the type name: `NM` normal, `EX` EX (always CRITICAL PERFECT when hit), `BR` break (orange, 5× score), `BX` break-EX, `CN` (slides only: connected additional segment).

| Line | Fields |
|---|---|
| `[mod]TAP` | `measure tick position`; `position` 0–7 = buttons from 1 o'clock clockwise (1–8 in the game UI) |
| `[mod]HLD` | `measure tick position duration` (ticks; 0 or 1 ≈ tap with double score) |
| `[mod]STR` | `measure tick position`: star note (tap that announces a slide; may exist without slide and vice-versa for Utage) |
| `[mod][shape]` slide | `measure tick startPos delay duration endPos`: delay = ticks the star "forms" before moving (usually one beat), duration = travel time; `measure tick` equal to the star's |
| `NMTTP` | `measure tick numPos chrPos hanabi size`: touch; `numPos` 0–7, `chrPos` ∈ `A B C D E` (C: only `C0` = C1 is used), `hanabi` 1 = fireworks, `size` `M1` regular or `L1` big (Basic/Advanced) |
| `NMTHO` | `measure tick duration 0 C hanabi size`: touch hold (center sensor; since version 1.57 other sensors by replacing the `0`/`C`) |

Slide shapes (3-letter codes, with the modifier giving `NMSI_`, `BRSCL`…):

| Code | Shape | simai |
|---|---|---|
| `SI_` | straight, distance between ends must be > 1 | `-` |
| `SV_` | via centre | `v` |
| `SCR` / `SCL` | arc along the judgement ring clockwise / counter-clockwise | `>` / `<` |
| `SUR` / `SUL` | arc around the centre clockwise / counter-clockwise | `q` / `p` |
| `SXR` / `SXL` | big arc clockwise / counter | `qq` / `pp` |
| `SLR` / `SLL` | V through the button two steps away, cw / ccw (`endPos` constraint) | `V` |
| `SSL` / `SSR` | zigzag left / right (ends 4 apart) | `s` / `z` |
| `SF_` | fan between opposite buttons (ends 4 apart) | `w` |

Multiple slides from one star: several slide lines with the star's timing (the star becomes 10-sided and slides yellow). Connected slides: `CN` + shape lines inherit the first segment's modifier and start where the previous ended (`startPos` = previous `endPos`). Delay is 0, and star speed depends on the total duration.

### Footer

Statistics, not required to play: `T_REC_{TAP,BRK,XTP,BXX,HLD,XHO,BHO,BXH,STR,BST,XST,XBS,TTP,THO,SLD,BSL,ALL}`, `T_NUM_{TAP,BRK,HLD,SLD,ALL}`, `T_JUDGE_{TAP,HLD,SLD,ALL}` (one hold tick per `RESOLUTION/8` of duration, rounded up; zero-length hold = 1), `TTM_EACHPAIRS`, `TTM_SCR_{TAP,BRK,HLD,SLD,ALL,S}` (+ the SS threshold line, documented under the same key twice in ma2Research), `TTM_RAT_ACV`. Score per note: tap/touch 500, break 2600 (critical), hold/touch hold 1000, slide 1500.

## Timing model

`time = Σ over BPM segments (Δticks / RESOLUTION × 4 × 60/bpm)`, ticks relative to measure start; each measure = 4 beats irrespective of `MET`. Do not place notes before the count-in. No audio offset field (sync is handled by game data or tools, e.g. `&first=` in simai).

## Notes

Taps, holds, stars + slides, touch, touch hold; modifiers NM/EX/BR/BX/CN. EACH (yellow) is implicit: same measure+tick. No keysounds.

## Audio & images

Not in the chart.

## Versions & variants

`1.03.00` (maimai DX/DX PLUS/Splash/UNiVERSE…, pre-FESTiVAL), `1.04.00` (FESTiVAL: connected `CN` slides, touch `L1/M1` size field, touch hold parameters), post-`1.57` touch holds outside the centre.

## Quirks & pitfalls

- Position 8 or any out-of-range value crashes the game.
- `MET_DEF`/`MET` order is lower then upper.
- Store BPM with the 275.001-style rounding to match the game's integer-microsecond clock.
- Line order affects z-order. To change the overlap, shift timing by 1 tick (ma2Research's Apollo example: increase `BRSCL` duration, increase `CNSCR` tick by 1 and reduce its duration by 1).
- [observed: samples/OshamaDXBar6.ma2, samples/TanakaBar36.ma2] `1.03.00` files use unprefixed note names (`TAP`, `STR`, `SI_`, `BRK`, `HLD`, `XTP`, `XST`), `1.04.00` files the `NM`/`BR`/`EX`/`BX` prefixed names (`NMTAP`, `NMSTR`, `NMSCR`, `BRTAP`). Files may have no header at all (`samples/DXFestivalTestMa2.ma2`).
- 4 beats per measure; use `RESOLUTION` for subdivisions (a multiple of 3 and a power of 2, e.g. 384, recommended).

## Example

From ma2Research (examples inline in the documentation):

```
NMSTR	5	0	2
NMSI_	5	0	2	96	48	5
CNSUR	5	144	5	0	48	0
NMTTP	10	0	4	D	0	M1
```

Star at button 2; straight slide 2 to 5, delay 96 ticks, duration 48; connected clockwise centre arc 5 to 0; touch at D4.

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [Littlebluemoon/ma2Research](https://github.com/Littlebluemoon/ma2Research) (documentation)
- [donmai-me/MaiConverter](https://github.com/donmai-me/MaiConverter) (Python: ma2 <-> sdt <-> simai)
- [Neskol/MaiLib](https://github.com/Neskol/MaiLib), [MaichartConverter](https://github.com/Neskol/MaichartConverter) (C#)
- [lcebot/ma2-parser](https://github.com/lcebot/ma2-parser) (ma2 to simai), [lcebot/maidata-parser](https://github.com/lcebot/maidata-parser) (simai to ma2)
- MuNET-OSS/MaiChartManager (C#)

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Neskol/MaichartConverterUnitTest has about 15 more `.ma2`/`maidata` files in `MaichartConverterUnitTest/data/`. MaichartConverter and MaiConverter convert simai to ma2; ma2Research (Unlicense) has inline examples; official files are in game data (`.../music/musicNNNNNN/NNNNNN_0D.ma2`).

## Sources

- <https://raw.githubusercontent.com/Littlebluemoon/ma2Research/master/Charts.md> (read in full)
- <https://github.com/donmai-me/MaiConverter> README (read), <https://github.com/lcebot/maidata-parser>, <https://github.com/lcebot/ma2-parser> (read)
- <https://github.com/Neskol/MaiLib> (search snippet)
