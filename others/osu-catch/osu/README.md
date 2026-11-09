# osu!catch beatmap (`.osu`, `Mode: 2`)
Kind: chart

Doc status: partial · ROX: no (refused) · Category: others · Encoding: text

The container, sections, timing points and generic hit-object line are in the canonical page [vsrg/osu-mania/osu/README.md](../../../vsrg/osu-mania/osu/README.md). This page only lists what is specific to `Mode: 2`. The slider line syntax (curve types, `slides`, `length`, edge sounds) is documented in [../../osu-standard/osu/README.md](../../osu-standard/osu/README.md).

## Overview

osu!catch (osu!ctb) is the catching mode of osu!: fruits fall from the top, the player slides a catcher left/right. The file is the usual `.osu` with `Mode: 2`; catch maps are either mapped natively or converted at load time from osu!standard maps (a standard map has all the data a catch map needs: x positions, sliders, spinners), so a very large share of `Mode: 2` files are conversions made by the mapper.

## Packaged in

- Packaged in [`osz`](../../../vsrg/osu-mania/osz/).

## Container & encoding

As in the canonical page (UTF-8 text, one file per difficulty, `.osz` set archive).

## Structure / metadata

`[Difficulty]`: `CircleSize` (fruit size), `ApproachRate` (fall speed), `OverallDifficulty`, `HPDrainRate`, `SliderMultiplier`, `SliderTickRate` (juice-stream droplets). The exact gameplay use of each value is client behaviour and is not described in the sources consulted. Everything else as standard.

## Timing model

Absolute milliseconds; BPM from uninherited points, slider velocity from inherited points (`SV = 100 / -beatLength`). Juice stream duration uses the standard slider formula: velocity `100 * SliderMultiplier / adjustedBeatLength` osu!pixels per ms, where `adjustedBeatLength = beatLength * clamp(100/SV, 10, 1000) / 100` for catch (`GetPrecisionAdjustedBeatLength`, ruleset `fruits`, i.e. `beatLength / SV` within the clamp); tick distance is `velocity * beatLength / SliderTickRate * TickDistanceMultiplier`. Before format version 8 the tick distance multiplier was `1 / SV` of the active inherited point, from 8 on it is 1 (comment in `CatchBeatmapConverter`: "prior to v8, speed multipliers don't adjust for how many ticks are generated over the same distance").

## Notes

The playfield is one-dimensional: `x` in `0..512` (`CatchPlayfield.WIDTH = 512`) is the horizontal position; `y` is not used for gameplay (lazer stores it as `LegacyConvertedY`, default `DEFAULT_LEGACY_CONVERT_Y = 192`; what it is used for was not established from the files read). Per the osu-wiki `.osu` page and lazer's `CatchBeatmapConverter`:

| `.osu` object | Catch object | Notes |
|---|---|---|
| hit circle (`type & 1`) | **Fruit** | at `x`; combo bit/skip give the fruit variety (colour) |
| slider (`type & 2`) | **Juice stream** | a fruit at each slider node (head, every repeat, tail) and droplets (ticks, at `x + path x offset`) along the way; "tiny droplets" are inserted between events more than 80 ms apart, halved until <= 100 ms. Only the horizontal component of the path matters, but vertical space in the curve can be used to make the stream move horizontally with acceleration after flattening (wiki) |
| spinner (`type & 8`) | **Banana shower** | bananas spaced by `duration` halved until <= 100 ms, from `time` to `endTime` (int-truncated); their x offsets are random (seeded) at load time, they are not stored |
| mania hold (`type & 128`) | not defined | |

Not in the file, computed by the client: hyper-dash (dash chains), fruit x offsets for Hard Rock, banana randomness (`RNG_SEED = 1337` for the position offsets in `CatchBeatmapProcessor`), the number of droplets.

## Audio & images

As in the canonical page. Hit sounds: the usual `hitSound`/`hitSample` fields; droplets use `slidertick`.

## Versions & variants

Format version 8 changes the juice-stream tick distance rule (above). The usual version table of the canonical page applies. Lazer v128 stores float positions.

## Quirks & pitfalls

- Slider paths are flattened to 1D: only the x extent of the curve counts.
- A converted map keeps standard semantics in `x` values; maps near the playfield edge are clamped to `0..512` (`EffectiveX`).
- `Mode: 2` is easy to confuse with the default 0: check `[General]`.

## Example

Illustrative, hand-built from the rules above (not a real file):

```
[General]
Mode: 2
[HitObjects]
256,192,1000,1,0,0:0:0:0:                  <- fruit at x=256
100,192,2000,2,0,L|300:192,1,200           <- juice stream, x 100 -> 300, one pass
256,192,4000,8,0,5000,0:0:0:0:             <- banana shower 4000..5000 ms
```

## ROX support

Not read by ROX: `OsuDecoder` returns `InvalidFormat("Not a mania beatmap (mode=2, expected 3)")` from the header peek.

## Parsers & tools

- osu!lazer catch ruleset (C#): https://github.com/ppy/osu/tree/master/osu.Game.Rulesets.Catch (`Beatmaps/CatchBeatmapConverter.cs`, `Objects/JuiceStream.cs`, `Objects/BananaShower.cs`)
- osu-file-parser / libosu (Rust) parse the generic lines.

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): 21 `Mode: 2` charts (ppy/osu catch tests, kionell/osu-taiko-stable, MaxOhn/rosu-pp); format v14 only. Standard maps used to test conversion to catch are in [../../osu-standard/osu/samples/](../../osu-standard/osu/samples/).
- More: any osu! mapset (`.osz`) with catch difficulties has `.osu` files with `Mode: 2`; download from osu.ppy.sh needs an account [inference]. Fixture folders: ppy/osu `osu.Game.Rulesets.Catch.Tests/Resources/Testing/Beatmaps`, kionell/osu-taiko-stable `tests/Files/Catch/Beatmaps`.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osu_(file_format)/en.md (osu!catch section)
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Catch/Beatmaps/CatchBeatmapConverter.cs, `CatchBeatmapProcessor.cs`
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Catch/Objects/{JuiceStream,BananaShower,CatchHitObject}.cs, `UI/CatchPlayfield.cs`
- https://github.com/ppy/osu/blob/master/osu.Game/Rulesets/Objects/Legacy/LegacyRulesetExtensions.cs
- ROX source: `src/formats/osu/decoder.rs`
