# osu!standard beatmap (`.osu`, `Mode: 0`)
Kind: chart

Doc status: partial · ROX: no (refused) · Category: others · Encoding: text

Container, sections, metadata, `[Events]`, `[TimingPoints]` and the generic hit-object line are in the canonical page [vsrg/osu-mania/osu/README.md](../../../vsrg/osu-mania/osu/README.md). This page covers osu!standard only (`Mode: 0`, also the default when `Mode` is missing).

## Overview
Original osu! mode. Circles, sliders and spinners sit in a 512x384 "osu!pixel" playfield (`x` 0-512, `y` 0-384; lazer clamps both to 0..512).

## Packaged in

- `.osz` (zip of a beatmap set: one `.osu` per difficulty, audio, background, optional video, `.osb` storyboard, hitsounds).

## Container & encoding
As in the canonical page; mode-specific data is in `[General]`, `[Difficulty]`, `[Colours]`, `[HitObjects]`.

## Structure / metadata

Keys that matter only in standard:

- `[General]`: `StackLeniency` (0-1, default 0.7; the time window in which close objects stack), `OverlayPosition`, `SkinPreference`, `UseSkinSprites`, `Mode: 0`.
- `[Difficulty]`: `CircleSize` (circle radius, 0-10), `ApproachRate` (0-10; in old files equals `OverallDifficulty` if missing), `OverallDifficulty`, `HPDrainRate`, `SliderMultiplier` (hundreds of osu!pixels per beat at SV 1.0; lazer clamps 0.4-3.6), `SliderTickRate` (ticks per beat; lazer clamps 0.5-8).
- `[Colours]`: `Combo1..` additive combo colours (`R,G,B`), `SliderTrackOverride`, `SliderBorder`.

## Timing model

Absolute milliseconds. Uninherited points define BPM (`60000/beatLength`) and meter. Inherited points (`beatLength < 0`) define the slider velocity multiplier `SV = 100 / -beatLength` (e.g. `-50` = 2x faster sliders). The file stores no slider duration; one pass lasts

```
length / (SliderMultiplier * 100 * SV) * beatLength        (ms; beatLength of the active uninherited point)
```

(osu-wiki), and the full slider lasts `slides` times that. Sample set / volume / custom index come from the timing point unless the object's `hitSample` overrides them. Kiai is `effects` bit 0.

## Notes

### Hit circle

`x,y,time,type,hitSound,hitSample`: `type` bit 0; bit 2 = new combo; bits 4-6 = combo colours to skip (only with the new-combo bit). lazer forces a new combo on the first object of the map, the object after a spinner, and the first object after a break (`postProcessBreaks`).

### Slider

`x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample` (`type` bit 1).

| Field | Meaning |
|---|---|
| `curveType` | `B` bezier, `C` centripetal Catmull-Rom, `L` linear, `P` perfect circle (arc through 3 points) (wiki). lazer: an unknown letter is read as Catmull (`convertPathType` default); `B<n>` with a degree is a B-spline in lazer's own extension |
| `curvePoints` | pipe separated `x:y` list; the curve's first point is the object's own `x,y`, so the list starts at the second point |
| `slides` | number of passes (repeat count + 1); lazer rejects `> 9000` and stores `slides - 1` as repeats |
| `length` | visual path length in osu!pixels (the path is cut or extended with a straight line to this length); 0 or missing = the curve's own length in lazer |
| `edgeSounds` | pipe list of `hitSound` flags per edge (head, each repeat, tail): `slides + 1` entries |
| `edgeSets` | pipe list of `normalSet:additionSet` per edge |
| `hitSample` | as in the canonical doc (body sound / default for edges) |

- Bezier: arbitrary degree. Repeating a point (a "red anchor") chains several bezier curves; two equal consecutive points start a new segment, as in lazer's `convertPoints`.
- Perfect circle: needs exactly 3 points including the head; with more points the type becomes bezier. Stable turns collinear perfect curves into linear paths; lazer (version 128) keeps them as perfect curves (`ConvertHitObjectParser.convertPoints`).
- Catmull: legacy catmull sliders do not support several segments, so adjacent segments are merged (stable behaviour kept for versions < 128).
- Slider sounds: edges play their `edgeSounds`; the body loops `<set>-slidernormal` / `-sliderwhistle` (only normal and whistle) while the follow circle is active (wiki).
- Version 3 files list the head point as the first curve point (osu-file-parser drops it); see the canonical version table.

### Spinner

`x,y,time,type,hitSound,endTime,hitSample` (`type` bit 3). `x,y` are ignored and set to the centre `256,192` (lazer: `new Vector2(512,384)/2`). Duration = `endTime - time` (never negative).

### Combo colours and stacking

The combo number resets at each new-combo object. The client computes stacking (objects at the same place within `StackLeniency * preempt` are drawn offset) at load time; the file does not store it. The algorithm depends on the format version (version >= 6 uses the newer one, lazer `OsuBeatmapProcessor.ApplyStacking`).

## Audio & images
As in the canonical page. Hit samples follow `<set>-hit<name><index>.wav`.

## Versions & variants
All `.osu` versions (3-14 stable, 128 lazer) hold standard maps; see the canonical table. Standard-specific: version < 6 stacking, version 3 curve points, lazer v128 float coordinates (positions truncated to integers below 128). lazer's parser accepts a letter mid point list to start a new segment of another type (`B|1:1|2:2|L|3:3`, "explicit segments"; stable support not established).

## Quirks & pitfalls
- Missing `Mode` means standard: a mania-only decoder must check it (ROX does).
- Broken maps can have slider length 0 / missing or `slides` 0; lazer tolerates them.
- Curve points are non-integer in lazer files (>= v128), integer before; lazer clamps `x,y` to 0..512 (offscreen objects exist).
- `edgeSounds`/`edgeSets` may be shorter than `slides + 1`; missing entries take the object's own sound/set.

## Example

osu-wiki `.osu` page, "Hit objects / Examples", 3 lines:

```
256,192,11000,21,2
256,192,11200,8,12,12000,3:0:0:80:
100,100,12600,6,1,B|200:200|250:200|250:200|300:150,2,310.123,2|1|2,0:0|0:0|0:2,0:0:0:0:
```

Hit circle at the centre, whistle, new combo with 1 colour skip; spinner from 11200 to 12000 ms; compound bezier slider (red anchor at `250:200`) with 2 slides, length 310.123, edge sounds 2|1|2.

## ROX support
Not read: `OsuDecoder` checks `peek_mode` and returns `InvalidFormat("Not a mania beatmap (mode=0, expected 3)")`. A missing `Mode:` reads as 0 and is refused too.

## Parsers & tools

- osu!lazer (C#), the reference: https://github.com/ppy/osu/tree/master/osu.Game.Rulesets.Osu and `osu.Game/Rulesets/Objects/Legacy/ConvertHitObjectParser.cs`
- osu-file-parser, libosu (Rust); osu-parsers (TypeScript) https://github.com/kionell/osu-parsers [listed from the wider ecosystem; not opened]
- Parsers of the repository's original README: see the canonical page.

## Getting samples
Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: any osu! mapset (`.osz`, zip of `.osu` + audio) holds `.osu` files named `Artist - Title (Creator) [Difficulty].osu`; download needs an account [inference: anonymous visitors see "Sign In To Proceed"]. Respect https://osu.ppy.sh/wiki/en/Rules/Content_usage_permissions. Fixture repositories: MaxOhn/rosu-map `resources/`, ekgame/beatmap-analyzer `test_maps/osu/`.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osu_(file_format)/en.md
- https://github.com/ppy/osu/blob/master/osu.Game/Rulesets/Objects/Legacy/ConvertHitObjectParser.cs
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Osu/Beatmaps/OsuBeatmapProcessor.cs
- https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/Formats/LegacyBeatmapDecoder.cs
- https://docs.rs/osu-file-parser/1.1.0/ (hitobjects module)
- ROX source: `src/formats/osu/decoder.rs` (`peek_mode`, `refuse_other_mode`)
