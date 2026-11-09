# osu!taiko beatmap (`.osu`, `Mode: 1`)
Kind: chart

Doc status: partial · ROX: decode only (`TaikoDecoder`, converted to a 4K layout; not reached by extension auto-detection) · Category: others · Encoding: text

Everything about the file container, sections, `[General]`/`[Metadata]`/`[Difficulty]`, `[Events]`, `[TimingPoints]` and the generic hit-object line is in the canonical page [vsrg/osu-mania/osu/README.md](../../../vsrg/osu-mania/osu/README.md). This page only covers what is specific to `Mode: 1`.

## Overview

osu!taiko is the osu! mode inspired by Taiko no Tatsujin: a horizontal scroll from the right to a fixed target circle on the left; the player hits "centre" (don, red) and "rim" (kat, blue) with two pairs of keys. The beatmap file is the ordinary `.osu` with `Mode: 1`. Maps are either made natively in taiko or are auto-converted from osu!standard / mania maps by the client at load time (the conversion is not stored in the file).

## Packaged in

- Shipped in: `.osz` (zip of a beatmap set: one `.osu` per difficulty, audio, background, optional video, `.osb` storyboard, hitsounds).

## Container & encoding

Identical to the canonical doc: UTF-8 text, one file per difficulty, `osu file format vN`, `.osz` set archive.

## Structure / metadata

Same sections. Mode-relevant keys:

- `[General] Mode: 1`. `SampleSet` / hit sounds drive the object colour (below).
- `[Difficulty]`: `OverallDifficulty` (hit windows and swell requirement), `SliderMultiplier` and `SliderTickRate` (drum roll length and tick rate; a drum roll is a slider line), `HPDrainRate`. `CircleSize` and `ApproachRate` are unused.
- `[Colours]`: combo colours unused.

## Timing model

- Absolute milliseconds, as in all `.osu` files.
- BPM = uninherited point `60000/beatLength`. The time signature of uninherited points drives bar lines; `effects` bit 3 ("omit first barline in osu!taiko and osu!mania") is honoured.
- Scroll speed: inherited points (`beatLength < 0`) set a scroll speed multiplier `-100/beatLength` (lazer assigns it to `EffectControlPoint.ScrollSpeed` for rulesets 1 and 3). It also scales drum roll duration via the slider formula below.
- Taiko applies a hidden constant `VELOCITY_MULTIPLIER = 1.4` to slider length / velocity (osu source `TaikoBeatmapConverter`, comment: never exposed to the player).

## Notes

Object lines are the generic ones (`x,y,time,type,hitSound,objectParams,hitSample`); `x`, `y`, combo bits and combo colours are ignored in taiko. Per the osu-wiki `.osu` page and lazer's taiko code:

| `.osu` object | Taiko object | Rule |
|---|---|---|
| hit circle (`type & 1`) | **Hit** (don or kat) | `hitSound` has whistle (2) or clap (8) -> **kat** (rim, blue); otherwise **don** (centre, red). `finish` (4) -> **strong / large** version of either (`IsStrong`). So `0` don, `2`,`8`,`10` kat, `4` big don, `6`,`12`,`14` big kat. Lazer: rim if the samples contain clap or whistle (`Hit.getRimSamples`); strong if samples contain finish (`TaikoStrongableHitObject`) |
| slider (`type & 2`) | **Drum roll** (yellow bar, tick hits) | only `length`, `slides` and the timing points matter; `curveType`/`curvePoints` are used by the editor only. Duration of one pass = `length / (SliderMultiplier * 100 * SV) * beatLength` (wiki formula, `SV` = inherited multiplier), times `slides` for the whole drum roll (lazer: `distance = length * 1.4 * spans`, `taikoVelocity = 100 * SliderMultiplier * 1.4`, `duration = distance / taikoVelocity * (beatLength / SV)`, truncated to an integer ms). Finish on the slider -> strong drum roll. Tick spacing: `beatLength / TickRate` with `TickRate = 3` if `SliderTickRate == 3`, else 4 (`DrumRoll.cs`) |
| spinner (`type & 8`) | **Swell** (denden / "shaker") | duration = `endTime - time`; `RequiredHits = max(1, duration/1000 * hitMultiplier)` with `hitMultiplier = DifficultyRange(OD, 3, 5, 7.5) * 1.65` (lazer `RequiredSwellHitsPerSecond`) |
| mania hold (`type & 128`) | not defined for taiko | lazer's converter turns mania objects of the same time into strong hits (`GroupBy StartTime`), that is a conversion, not a native encoding |

Native taiko files (`Mode: 1`, `isForCurrentRuleset`) keep sliders as drum rolls. When osu!standard maps are converted to taiko, short sliders can be split into repeated hits (`shouldConvertSliderToHits`: tick spacing `min(beatLength / SliderTickRate, duration / spans)`, only if `distance / osuVelocity * 1000 < 2 * beatLength`; in versions < 8 the speed-adjusted beat length is used, from 8 on the raw one: `beatmap.BeatmapVersion >= 8`). That conversion is client behaviour, not file content.

Simultaneous objects: two objects at the same time are possible (stacked don/kat); in the client mania->taiko conversion they become a strong hit.

## Audio & images

As in the canonical doc. Taiko uses the `taiko-` prefixed sample sets of the skin (`taiko-normal-hitnormal.wav` etc.) [inference: skinning convention, not read in a source for this page]; per-object `hitSample` custom files also apply.

## Versions & variants

Same version line as the other modes. Version 8 changes the slider->hits conversion rule (see above). Gameplay-affecting differences between stable and lazer (scroll speed handling of inherited points) are not stored in the file.

## Quirks & pitfalls

- A taiko map's `x,y` are meaningless; do not use them.
- A drum roll's end time is not stored: it must be computed from `length`, `slides`, `SliderMultiplier`, the inherited multiplier and the beat length at the slider's start.
- Strong/big is encoded in the sound bit `finish`, colour in the whistle/clap bits.
- `curvePoints` must still parse (a slider line is a slider line) even though they are unused.

## Example

Illustrative, hand-built from the rules above (not a real file; lines follow the syntax of the wiki's example):

```
[General]
Mode: 1
[HitObjects]
256,192,1000,1,0,0:0:0:0:        <- don
256,192,1500,1,8,0:0:0:0:        <- kat (clap)
256,192,2000,1,4,0:0:0:0:        <- big don (finish)
256,192,2500,2,0,L|356:192,1,100 <- drum roll, one pass, length 100
256,192,4000,12,0,6000,0:0:0:0:  <- swell until 6000 (type 8 + new combo bit 4)
```

## ROX support

ROX source `src/formats/taiko`:
- `TaikoDecoder` is a separate decoder that parses the `.osu` with the same parser as mania, requires `Mode: 1` (else `InvalidFormat("Not a taiko beatmap (mode=N, expected 1)")`), and builds a **4-column** chart. The extension auto-detection (`auto/detect.rs`: `osu -> DetectedFormat::Osu`) and `auto/dispatch.rs` only know the mania decoder, so taiko decoding needs an explicit call.
- Mapping: spinners (type bit 3) are skipped. Every other object (including sliders, which therefore become a single tap at the slider start, NOT a roll) becomes tap(s): kat if whistle or clap, don otherwise; `finish` -> big: two columns at the same time. Small notes alternate between the two columns of their colour, big ones use both. Column layouts (`ColumnLayout`): `Dkkd` (default) don = columns 0 and 3, kat = 1 and 2; `Dkdk` don = 0,2, kat = 1,3; `Kddk` don = 1,2, kat = 0,3. `AlternationState` can be supplied to continue the alternation.
- Timing: only uninherited points become BPM points (with meter); SV points are dropped; if there is no BPM point, 120 BPM at 0 is inserted. Metadata: title/artist (Unicode preferred), creator, version, ids, audio, background, `AudioLeadIn` and `PreviewTime`.
- Not read: drum roll length, swell, scroll speed, editor/colours. Burst/hold notes are never generated. Encoding to taiko is not provided.

## Parsers & tools

- osu!lazer taiko ruleset (C#): https://github.com/ppy/osu/tree/master/osu.Game.Rulesets.Taiko
- osu-file-parser, libosu (Rust): see the canonical doc.
- ROX `TaikoDecoder` (Rust), vendored in this repository.
- Taiko no Tatsujin charts (`.tja`) are a different format: [../../taiko-no-tatsujin/tja/](../../taiko-no-tatsujin/tja/).

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): 15 `Mode: 1` charts (v9, v12, v14; Kantan to Inner Oni difficulties of one song; drum rolls; swells; one hand-written mini map) from kionell/osu-taiko-stable (MIT), ekgame/beatmap-analyzer (GPL-3.0), MaxOhn/rosu-pp (MIT), ppy/osu (MIT), N0zoM1z0/osu-reverse-engineering (MIT).
- More: any osu! mapset (`.osz`) with taiko difficulties has `.osu` files with `Mode: 1`; converted maps (standard -> taiko) are not stored as taiko files (the client converts at load time). Fixture folders: kionell/osu-taiko-stable `tests/Files/Taiko/Beatmaps`, ekgame/beatmap-analyzer `test_maps/taiko`.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osu_(file_format)/en.md (osu!taiko section)
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Taiko/Beatmaps/TaikoBeatmapConverter.cs
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Taiko/Objects/{Hit,Swell,DrumRoll,TaikoStrongableHitObject}.cs
- https://github.com/ppy/osu/blob/master/osu.Game/Rulesets/Objects/Legacy/LegacyRulesetExtensions.cs (`GetPrecisionAdjustedBeatLength`)
- ROX source: `src/formats/taiko/{decoder,types}.rs`, `src/formats/auto/{detect,dispatch}.rs`
