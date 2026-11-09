# Re:PhiEdit chart (RPEJSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

Chart format of **Re:PhiEdit (RPE)**, the community Phigros chart editor by cmdysj; it is the de-facto standard for fan-made Phigros charts and is read by Phira, phi-chart-render, PhiZone Player and others. Much richer than the official format: global BPM list, several event layers per line, bezier/easing curves, parent lines, textures, text, colour and UI-bound lines. Documented in Chinese by the Phira team; the page below is a faithful English summary of fields that were read. Written against RPE 1.4.1 per the source; older "added in" versions are mostly unknown.

## Packaged in

- Packaged in [`pez`](../pez/).

## Container & encoding

- JSON, UTF-8, one file per chart (often named by the editor as `<id>.json`); a chart folder also holds the music, illustration and optional line textures/hitsounds referenced by relative paths in `META`.
- Phira's loader ignores the file extension and detects the format via `info.yml` `format` or by content.

## Structure / metadata

Root:

| Field | Type | Meaning |
|---|---|---|
| `BPMList` | array of `{bpm, startTime}` | tempo map; `startTime` is a beat triple |
| `META` | object | `RPEVersion` (int, 100..160), `background` (path), `charter`, `composer`, `id`, `illustration` (added 141), `level`, `name`, `offset` (int, **ms**), `song` (path) |
| `judgeLineList` | array | lines |
| `judgeLineGroup` | string[] | editor only |
| `chartTime` | double | editing time in s (added 141), editor only |
| `multiLineString`, `multiScale`, `timeTags`, `xybind` | | editor-only state |

Judge line fields: `Group` (int), `Name`, `Texture` (path, default `line.png`), `anchor` (float[2], added 142), `eventLayers` (array, 1..5 layers; missing events omitted), `extended` (special events, see below), `father` (parent index, `-1` none), `isCover` (1 = lines mask notes behind them), `notes`, `numOfNotes` (includes fake notes, excludes Holds), `zOrder`, `attachUI` (`pause`, `combonumber`, `combo`, `score`, `bar`, `name`, `level`), `isGif` (added 150), `posControl`, `sizeControl`, `skewControl`, `yControl`, `alphaControl` (per-note keyframe controls by distance `x`), `bpmfactor` (effective BPM = `nowBpm / bpmfactor`), `rotateWithFather` (bool, added 163; treat missing as false).

Event layer: arrays `moveXEvents`, `moveYEvents`, `rotateEvents`, `alphaEvents`, `speedEvents`. Layer values add up (position, rotation); alpha as combined by the editor.

Event (all but speed): `startTime`/`endTime` (beat triples), `start`/`end` (float; alpha 0..255; rotation degrees; colour events use `[r,g,b]`, text events strings), `easingType` (1..29), `easingLeft`/`easingRight` (0..1 sub-range), `bezier` (0/1) + `bezierPoints` (float[4]), `linkgroup`. Speed events have only `startTime`, `endTime`, `start`, `end`, `linkgroup`; since 162 they accept easings (no bezier); 1.7.0 reverted to easing the speed value itself.

Easing ids: 1 Linear, 2 OutSine, 3 InSine, 4 OutQuad, 5 InQuad, 6 InOutSine, 7 InOutQuad, 8 OutCubic, 9 InCubic, 10 OutQuart, 11 InQuart, 12 InOutCubic, 13 InOutQuart, 14 OutQuint, 15 InQuint, 16 OutExpo, 17 InExpo, 18 OutCirc, 19 InCirc, 20 OutBack, 21 InBack, 22 InOutCirc, 23 InOutBack, 24 OutElastic, 25 InElastic, 26 OutBounce, 27 InBounce, 28 InOutBounce, 29 InOutElastic (not usable on speed events).

Special events (`extended`): `colorEvents`, `scaleXEvents`, `scaleYEvents`, `textEvents`, `paintEvents`, `gifEvents`, `inclineEvents`; absent when unused (except inclineEvents). Field-level detail was not read [partial].

## Timing model

- Beat triple `[a, b, c]` = `a + b/c` beats (integer part, numerator, denominator).
- Single BPM: `seconds = 60 / BPM * beat`. Multi-BPM: integrate piecewise over `BPMList`, using `BPM / line.bpmfactor` as the effective tempo (Phira docs give `beat2sec`/`sec2beat` reference code).
- `META.offset` is in **milliseconds**: negative = music starts `-offset` ms before the chart; positive = after.
- Coordinate system: origin at screen centre, X in -675..675, Y in -450..450 (so normalised x = `(x+675)/1350`, y = `1-(y+450)/900`).
- Between events the previous end value is kept; Phira's reference code pads gaps with constant events and adds a sentinel until beat 31250000.

## Notes

Note fields: `above` (1 = falls on the front, otherwise back), `alpha` (0..255, default 255), `startTime`/`endTime` (beat triples; equal unless Hold), `isFake` (1 = fake: no judgement, no hit effect/sound, not counted), `positionX` (relative to line centre), `size` (width multiplier, default 1), `speed` (default 1), `type`, `visibleTime` (s, default 999999), `yOffset` (effective offset `yOffset * speed`), `hitsound` (path, added 142), `judgeArea` (added 170), `tint`/`color` (int[3], added 170; field was renamed color -> tint in beta, accept both), `tintHitEffects` (int[3]?).

Note `type`: 1 Tap, 2 **Hold**, 3 **Flick**, 4 **Drag** (differs from the official format where 2 = Drag, 3 = Hold, 4 = Flick). Default Tap.

## Audio & images

`META.song`, `META.background` are paths relative to the chart folder; per-line `Texture` and per-note `hitsound` likewise. RPE can also embed textures through control fields not documented here.

## Versions & variants

- `META.RPEVersion` 100..160 but stays `150` for RPE 1.5.0 - 1.6.0 (alpha included) and `160` for 1.6.1 (field not bumped); do not use it to gate features.
- Fields have "added in" versions (141, 142, 150, 162, 163, 170); older charts omit them.
- A `bpmfactor` quirk: the editor cannot edit it; the divisor semantics (`/` not `*`) is easy to get wrong.
- Converters: PEC <-> RPE (`../pec/`), official <-> RPE.

## Quirks & pitfalls

- Negative `alpha` hides the line **and all its notes** (deprecated/illegal but still works).
- Negative speed makes notes fly upward; a Hold is fully drawn when its tail appears (not like the original game).
- Empty layers: `null` in older versions, omitted in later (>= 143 at least).
- `isCover` only masks notes on the back side of the line.
- `speed`/`yOffset` interplay: `yOffset` is scaled by `speed`, so speed 0 cancels it.

## Example

Illustrative, hand-built from the field tables above (not extracted from a real chart):

```json
{"BPMList":[{"bpm":120.0,"startTime":[0,0,1]}],
 "META":{"RPEVersion":160,"name":"demo","charter":"x","composer":"y","level":"IN Lv.1","id":"1","offset":0,"song":"music.ogg","background":"bg.png"},
 "judgeLineList":[{"Name":"Untitled","Texture":"line.png","father":-1,"isCover":1,"zOrder":0,
  "eventLayers":[{"speedEvents":[{"startTime":[0,0,1],"endTime":[1,0,1],"start":10.0,"end":10.0,"linkgroup":0}]}],
  "notes":[{"type":1,"above":1,"startTime":[1,0,1],"endTime":[1,0,1],"positionX":0.0,"size":1.0,"speed":1.0,"alpha":255,"isFake":0,"yOffset":0.0,"visibleTime":999999.0}]}]}
```

## ROX support

Not read by ROX.

## Parsers & tools

- Phira (Rust) loader and docs: <https://github.com/TeamFlos/phira>, <https://github.com/TeamFlos/phira-docs>
- phi-chart-render (JS): <https://github.com/MisaLiu/phi-chart-render>
- Phichain (Rust, converts RPE <-> Phichain/official): <https://github.com/Ivan-1f/phichain>
- PhiFanmade common chart docs: <https://docs.nuanr-mxi.com/en/>

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): three synthetic RPE charts (`RPEVersion` 113, 160, 170) from the MIT-licensed `rpechart` fixtures: layered events, extended events, father lines, fake notes, all four note types.
- Manifest (`samples.manifest.json`): nothing. A real `.pez` zip with an RPE chart is in [../pez/samples/](../pez/samples/).
- More: Re:PhiEdit writes `chart.json`; Phira imports it inside a `.pez`; `rpechart` can generate charts from a small `spec.json` (https://github.com/kamilhzn/rpechart).

## Sources

- <https://github.com/TeamFlos/phira-docs/tree/main/src/chart-standard/chart-format/rpe> (root, beat, judgeLine, event, extend, extendEvent, controls, note pages; raw markdown)
- <https://docs.nuanr-mxi.com/en/chart_format/judge_line.html> (PhiCommonChart model, for the cross-reference)
