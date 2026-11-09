# OGKR (`.ogkr`, ONGEKI chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (tab-separated records)

## Overview

`.ogkr` is the chart file of the arcade game ONGEKI. It is a text file of one command per line listing every object (taps, holds, flicks, bells, bullets, beams, walls, lane segments, enemy waypoints, timing and speed changes). The format was documented in Chinese by **MikiraSora** (OngekiFumianDescription, covering "refresh 1.50", ".ogkr parsing → 85%"), who also wrote the editor **OngekiFumenEditor**; **fairywreath/ogkr** (Rust) parses it ("with reference to MikiraSora's description"). All names below come from the `ongeki.md` page; items marked `(?)` there are uncertain.

Category: **others** — see [../README.md](../README.md).

## Container & encoding

Text, line-based; each line = command name followed by arguments (tab-separated in the example snippets). Numbers: ints and floats. Not compressed. Example lines in the description use tabs: `TAP\t217\t3\t0\t0\t0` [format of the snippet in `description.md`].

## Structure / metadata

### Header commands

| Command | Arguments |
|---|---|
| `VERSION` | `major minor release` (e.g. `1 3 1`) |
| `CREATOR` | chart author |
| `BPM_DEF` | `first common minimum maximum` |
| `MET_DEF` | `numerator(bunshi) denominator(bunbo)` |
| `TickResolution` / `RESOLUTION` | `resT` = 1920 (ticks per `tUnit`) |
| `XResolution` / `XRESOLUTION` | `resX` = 4096 (horizontal resolution) |
| `CLK_DEF` | count-in click resolution (1920) |
| `TUTORIAL` | unused |
| `BULLET_DAMAGE`, `HARDBULLET_DAMAGE`, `DANGERBULLET_DAMAGE`, `BEAM_DAMAGE` | damage values (1, 2, 4, 2 in the example) |
| `T_TOTAL`, `T_TAP`, `T_HOLD`, `T_SIDE`, `T_SHOLD`, `T_FLICK`, `T_BELL` | judgement counts (`T_TOTAL = T_TAP + T_HOLD + T_SIDE + T_SHOLD + T_FLICK`; platinum score = `T_TOTAL × 2`) |
| `PROGJUDGE_BPM` | proportional to number of hold-tick judgements (≤ 1.00001 → forced 240) |
| `BPL` | **bullet palette** entries: `strID shooter placeOffsetX target speed size type randDiffPos` |
| `BTP` | unused |

Bullet palette enums: shooter `UPS` (from the bullet's target-head x position), `ENE` (enemy position, with `ENS` lane), `CEN` (centre, X[0,0]); target `PLR` (aimed at the player's position when spawned), `FIX` (fixed field position); size `N` normal, `L` large (×1.4); type `CIR` circle, `NDL` needle, `SQR` square.

### Time and position grid

- **TGrid** `T[tUnit, tGrid]` with `ResT = 1920`: `tGrid = tUnit × 1920`, so `T[1,0] = T[0,1920]`. It is beat-relative: absolute time needs the BPM history. One `tUnit` = one drawn semi-transparent line = **one beat** [inference from "one tUnit equals one translucent line" and ResT=1920; the `MET` fields define the beat grouping].
- **XGrid** `X[xUnit, xGrid]` with `ResX = 4096`; horizontal positions in `xUnit` (e.g. walls default to X[−24,0]/X[24,0]).

### Timing / structure commands

| Command | Arguments |
|---|---|
| `BPM` | `tUnit tGrid bpm` |
| `MET` | `tUnit tGrid numerator denominator` |
| `CLK` | `tUnit tGrid` — click sound |
| `ISF` | `tUnit tGrid xUnit tGridLength areaWidth pattern` — force the speed-group of objects in an area |
| `SFL` | `tUnit tGrid tGridLength speedMultiplier groupId` — soflan; negative → reverse; groups like Arcaea timing groups |
| `EST` | `tUnit tGrid tag` (`WAVE1`, `WAVE2`, `BOSS`) — enemy set / boss phase marker |

### Object commands

Chains use **Start/Next/End** triplets sharing a `GroupId`/`RecordId`: walls `WLS/WLN/WLE` (left), `WRS/WRN/WRE` (right), lanes `LLS/LLN/LLE` (red), `LCS/LCN/LCE` (green), `LRS/LRN/LRE` (blue), `CLS/CLN/CLE` (coloured lane: `colorID` 0–19, `brightnessID` offset +3), enemy path `ENS/ENN/ENE`; each takes `GroupId tUnit tGrid xUnit` and the Start line an `isTransparent` flag. `LDP`/`LBK` (lane display / lane block): `GroupId Fore.tUnit Fore.tGrid Fore.xUnit Fore.xGrid Rear.tUnit Rear.tGrid Rear.xUnit Rear.xGrid`.

| Command | Arguments |
|---|---|
| `TAP` / `CTP` (= `XTP`, critical tap) | `laneGroupId tUnit tGrid xUnit xGrid` (the lane group only gives the colour/type; walls are lanes too, so wall taps use the wall's id) |
| `HLD` / `CHD` (= `XHD`) | `laneGroupId Fore.tUnit Fore.tGrid Fore.xUnit Fore.xGrid Rear.tUnit Rear.tGrid Rear.xUnit Rear.xGrid` |
| `FLK` / `CFK` | `tUnit tGrid xUnit direction` (`L` or `R`) |
| `BEL` | `tUnit tGrid xUnit bulletPaletteId` (`--` = none; with a palette the bell moves like a bullet) |
| `BLT` | `strId tUnit tGrid xUnit type` — bullet using palette `strId`; type `NML` normal, `STR` hard, `DNG` danger damage |
| `BMS/BMN/BME` | beam start/next/end: `recordId tUnit tGrid xUnit widthId`; `widthId` 1–5 → judge width 4/6/8/16/24, draw width 2/3/4/12/20 |
| `OBS/OBN/OBE` | oblique beam: same + `shootPosXUnitOffset` (only the Start's value counts) |

Bullets/bells with `target = PLR` ignore soflan (treated as speed 1).

## Timing model

Beat-relative like BMS: `time = integrate(BPM)` over `tUnit + tGrid/1920`. `MET` is cosmetic grouping. Bullet spawn time before impact (ms) from the description: `(40 − 7.5) / (max(0.2·(1+(6−1)·0.27), 0.2·UserSpeed) · BulletSpeed) · 16.6666`. There is no audio offset in the chart (handled outside).

## Notes

Tap/Hold (lane-bound, colour from lane), side-wall tap/hold, Flick (L/R), Bell, Bullet (aimed or fixed), Beam (straight/oblique, 5 widths), enemy markers; simultaneous objects share the time. Holds carry a Fore (head) and Rear (tail) point so hold tails can move horizontally.

## Audio & images

Not referenced by the chart.

## Versions & variants

`VERSION 1 3 1`-style; the doc tracks "refresh 1.50". Older/other game versions may differ.

## Quirks & pitfalls

- Lane groups must be defined before notes referencing them; `LBK` lasts only within its wall's display range.
- `isTransparent > 0` hides the lane drawing.
- Positions are free xUnit (not discrete columns); conversion to fixed columns is lossy.
- The spec itself is partially uncertain (`(?)` marks).
- The OngekiFumianDescription author asks not to discuss the project on other public sites (fairywreath README notice).

## Example

From OngekiFumianDescription `description.md` (original snippets):

```
TAP	217	3	0	0	0
TAP	74	3	960	-8	0
WLS	4	15	0	0
WLN	4	15	480	-24
WLE	4	16	0	-24
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [fairywreath/ogkr](https://github.com/fairywreath/ogkr) (Rust)
- [MikiraSora/OngekiFumenEditor](https://github.com/MikiraSora/OngekiFumenEditor) (C#, editor)
- MuNET-OSS tool "OGKR parse/generate" (C#) (search snippet)

## Sources

- <https://raw.githubusercontent.com/MikiraSora/OngekiFumianDescription/master/ongeki.md> and `description.md` (read)
- <https://github.com/fairywreath/ogkr> README (read)
