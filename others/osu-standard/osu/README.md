# osu!standard beatmap (`.osu`, `Mode: 0`)
Kind: chart

Doc status: partial · ROX: no (refused) · Category: others · Encoding: text

Container, sections, metadata, `[Events]`, `[TimingPoints]` and the generic hit-object line are described once in the canonical page [vsrg/osu-mania/osu/README.md](../../../vsrg/osu-mania/osu/README.md). This page covers what is specific to osu!standard (`Mode: 0`, also the default when `Mode` is missing).

## Overview

osu!standard is the original osu! game mode (`Mode: 0`). Circles, sliders and spinners are placed in a 512x384 "osu!pixel" playfield (`x` 0-512, `y` 0-384; lazer clamps both to 0..512). The player clicks circles at the right time (approach circle), follows slider bodies and spins spinners.

## Packaged in

- Packaged in [`osz`](../../../vsrg/osu-mania/osz/).

## Container & encoding

As in the canonical page. The mode-specific data is in `[General]`, `[Difficulty]`, `[Colours]`, `[HitObjects]`.

## Structure / metadata

Keys that matter only in standard:

- `[General]`: `StackLeniency` (0-1, default 0.7; the time window in which close objects are stacked), `OverlayPosition`, `SkinPreference`, `UseSkinSprites`, `Mode: 0`.
- `[Difficulty]`: `CircleSize` (circle radius, 0-10), `ApproachRate` (0-10; if missing it equals `OverallDifficulty` in old files), `OverallDifficulty`, `HPDrainRate`, `SliderMultiplier` (hundreds of osu!pixels per beat at SV 1.0; lazer clamps 0.4-3.6), `SliderTickRate` (ticks per beat; lazer clamps 0.5-8).
- `[Colours]`: `Combo1..` additive combo colours (`R,G,B`), `SliderTrackOverride`, `SliderBorder`.

## Timing model

Absolute milliseconds. Uninherited points define BPM (`60000/beatLength`) and meter; inherited points (`beatLength < 0`) define the slider velocity multiplier `SV = 100 / -beatLength` (e.g. `-50` = 2x faster sliders). A slider's duration is not stored; one pass lasts

```
length / (SliderMultiplier * 100 * SV) * beatLength        (ms; beatLength of the active uninherited point)
```

(osu-wiki), and the full slider lasts `slides` times that. Sample set / volume / custom index come from the timing point unless the object's `hitSample` overrides them; kiai is `effects` bit 0.

## Notes

### Hit circle

`x,y,time,type,hitSound,hitSample` - `type` bit 0; bit 2 = starts a new combo; bits 4-6 = combo colours to skip (only meaningful with the new-combo bit). lazer forces the first object of the map and the object after a spinner to start a new combo, and the first object after a break as well (`postProcessBreaks`).

### Slider

`x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample` (`type` bit 1).

| Field | Meaning |
|---|---|
| `curveType` | `B` bezier, `C` centripetal Catmull-Rom, `L` linear, `P` perfect circle (arc through 3 points) (wiki). lazer: an unknown letter is read as Catmull (`convertPathType` default); `B<n>` with a degree is a B-spline in lazer's own extension |
| `curvePoints` | pipe separated `x:y` list; the first point of the curve is the object's own `x,y`, so the list starts at the second point |
| `slides` | number of passes (repeat count + 1); lazer rejects `> 9000` and stores `slides - 1` as repeats |
| `length` | visual length of the path in osu!pixels (the path is cut or extended with a straight line to this length); 0 or missing = use the curve's own length in lazer |
| `edgeSounds` | pipe list of `hitSound` flags for each edge (head, each repeat, tail): `slides + 1` entries |
| `edgeSets` | pipe list of `normalSet:additionSet` for each edge |
| `hitSample` | as in the canonical doc (applies to the body sound / default for edges) |

- Bezier: arbitrary degree; several bezier curves can be chained by repeating a point (a "red anchor"); two equal consecutive points start a new segment, as in lazer's `convertPoints`.
- Perfect circle: needs exactly 3 points including the head; with more points the type becomes bezier. Stable turns collinear perfect curves into linear paths; lazer (version 128) keeps them as perfect curves (`ConvertHitObjectParser.convertPoints`).
- Catmull: legacy catmull sliders do not support several segments, adjacent segments are merged (stable behaviour kept for versions < 128).
- Slider sounds: edges play their `edgeSounds`; the body loops `<set>-slidernormal` / `-sliderwhistle` (only normal and whistle) while the follow circle is active (wiki).
- Version 3 files list the head point as the first curve point (osu-file-parser drops it); see the canonical version table.

### Spinner

`x,y,time,type,hitSound,endTime,hitSample` (`type` bit 3); `x,y` are ignored and set to the centre `256,192` (lazer: `new Vector2(512,384)/2`); duration = `endTime - time` (never negative).

### Combo colours and stacking

Combo number resets at each new-combo object. Stacking (objects at the same place within `StackLeniency * preempt` are drawn offset) is computed at load time by the client, and its algorithm depends on the format version (version >= 6 uses the newer algorithm, lazer `OsuBeatmapProcessor.ApplyStacking`); it is not stored in the file.

## Audio & images

As in the canonical page. Hit samples follow the `<set>-hit<name><index>.wav` convention; `Combo` colours and skin sprites are optional.

## Versions & variants

All `.osu` versions (3-14 stable, 128 lazer) can hold standard maps; see the version table of the canonical page. Standard-specific: version < 6 stacking, version 3 curve points, lazer v128 keeps float coordinates (below 128 positions are truncated to integers), and lazer's parser accepts a letter in the middle of the point list to start a new path segment of another type (`B|1:1|2:2|L|3:3`, documented in the parser's comment as "explicit segments"; whether stable writes it is not established).

## Quirks & pitfalls

- Missing `Mode` means standard: a mania-only decoder must check it (ROX does, and refuses).
- Slider length 0 / missing and `slides` of 0 exist in broken maps; lazer tolerates them.
- Curve points can be non-integer in lazer files (>= v128), integers before.
- `x,y` are clamped to 0..512 by lazer (maps with offscreen objects exist).
- `edgeSounds`/`edgeSets` may be shorter than `slides + 1`; missing entries take the object's own sound/set.

## Example

Real documentation example (osu-wiki `.osu` page, "Hit objects / Examples", 3 lines):

```
256,192,11000,21,2
256,192,11200,8,12,12000,3:0:0:80:
100,100,12600,6,1,B|200:200|250:200|250:200|300:150,2,310.123,2|1|2,0:0|0:0|0:2,0:0:0:0:
```

hit circle at the centre, whistle, new combo with 1 colour skip; spinner from 11200 to 12000 ms; compound bezier slider (red anchor at `250:200`) with 2 slides, length 310.123, edge sounds 2|1|2.

## ROX support

Not read by ROX: `OsuDecoder` calls `peek_mode` on the header and returns `InvalidFormat("Not a mania beatmap (mode=0, expected 3)")` before parsing the objects. A missing `Mode:` is read as 0, so such files are refused too.

## Parsers & tools

- osu!lazer (C#), the reference: https://github.com/ppy/osu/tree/master/osu.Game.Rulesets.Osu and `osu.Game/Rulesets/Objects/Legacy/ConvertHitObjectParser.cs`
- osu-file-parser, libosu (Rust); osu-parsers (TypeScript) https://github.com/kionell/osu-parsers [listed from the wider ecosystem; not opened]
- Parsers of the repository's original README: see the canonical page.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osu_(file_format)/en.md
- https://github.com/ppy/osu/blob/master/osu.Game/Rulesets/Objects/Legacy/ConvertHitObjectParser.cs
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Osu/Beatmaps/OsuBeatmapProcessor.cs
- https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/Formats/LegacyBeatmapDecoder.cs
- https://docs.rs/osu-file-parser/1.1.0/ (hitobjects module)
- ROX source: `src/formats/osu/decoder.rs` (`peek_mode`, `refuse_other_mode`)
