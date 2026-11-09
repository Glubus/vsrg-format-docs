# K-Shoot MANIA JSON chart (`.kson`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview
KSON is the JSON successor of [`ksh`](../ksh/README.md), specified by the K-Shoot MANIA project (spec v1.0.2, `format_version: 1`, CC0). It stores everything on an absolute **pulse** grid instead of text measures, supports graphs with curves (camera, scroll speed, laser), and can embed KSH-only leftovers in `compat`. Used by KSM v2 development, Unnamed SDVX Clone (Rust rewrite, `kson-rs`) and editors. This page covers the structure fields that matter for charts; audio-effect tables (lines 235-656 of the spec: `audio.audio_effect`, parameter types/lists) and camera details are only summarized.

## Container & encoding
JSON, UTF-8 **without BOM**, LF line endings, `.kson` extension, no `null` values; undefined values take their defaults; unsupported "(OPTIONAL SUPPORT)" parameters must be ignored. One file = one difficulty.

## Structure / metadata
Top level: `format_version` (uint), `meta`, `beat`, optional `gauge`, `note`, `audio`, `camera`, `bg`, `editor`, `compat`, `impl`.

- `meta`: `title`, `title_translit?`, `title_img_filename?`, `artist`, `artist_translit?`, `artist_img_filename?`, `chart_author`, `difficulty` (uint 0-3 = light/challenge/extended/infinite, or a name; KSM ignores names -> 3), `level` (1-20), `disp_bpm` (string), `std_bpm?`, `jacket_filename?`, `jacket_author?`, `icon_filename?`, `information?`.
- `gauge.total` (0 = auto).
- `audio.bgm`: `filename`, `vol` (1.0), `offset` (ms, 0), `preview` {`offset` ms 0, `duration` ms 15000}, `legacy.fp_filenames` (prerendered FX/laser variants).
- `audio.key_sound` (`fx`, `laser`: chip FX samples, slam sounds) and `audio.audio_effect` (`fx`, `laser` definitions and events: see the spec).
- `camera` (`tilt`, `cam.body`, `cam.pattern`), `bg` (`legacy.bg`, `layer`, `movie`), `compat.ksh_unknown` (KSH options without a kson counterpart), `editor`, `impl`.

## Timing model
- Pulse `y` resolution: **240 per beat = 960 per measure (4/4)**.
- `beat.bpm`: `ByPulse<double>[]` = `[[y, bpm], ...]`.
- `beat.time_sig`: `ByMeasureIdx<TimeSig>[]` = `[[measure_idx, [num, den]], ...]`, default `[[0,[4,4]]]`.
- `beat.scroll_speed`: GraphPoint[] default `[[0,1.0]]`; `beat.stop`: `[[y, duration_pulses]]` (equal to scroll speed 0 for a duration; stop has priority).
- Time of pulse y: integrate BPM over pulses (1 beat = 240 pulses); time-signature changes only change where measure lines fall (measure length in pulses = 960 * num/den [inference from the unit definitions]).

## Notes
`note`: `bt: (uint|ButtonNote)[][4]`, `fx: (uint|ButtonNote)[][2]`, `laser: LaserSection[][2]`. Notes of one lane must not overlap.
- `ButtonNote` = `[y, length]` (`length` 0 = chip, > 0 = long); a bare uint `y` is a chip note.
- `LaserSection` = `[y, points, w]`: `points` = array of GraphSectionPoint `[ry, v | [v, vf], curve?]` (relative pulse, position 0.0-1.0 (vf = second value for an immediate change = slam), optional curve control point `[a, b]` default `[0,0]`); `w` = x-axis scale 1 or 2 (wide laser), default 1.
- GraphPoint (whole-chart graphs) = `[y, v | [v, vf], curve?]`.

## Audio & images
`audio.bgm.filename`, `meta.jacket_filename`, `bg` section; paths relative to the chart file.

## Versions & variants
`format_version` 1 (spec 1.0.0 -> 1.0.2). KSH `ver=200` marks charts converted from kson. Unknown/unsupported KSH options are preserved in `compat.ksh_unknown`.

## Quirks & pitfalls
- [observed in samples/oracle.kson, samples/effects.kson] Files written by the VOXL4DD3R converter's dialect deviate from the spec text read here: `meta.difficulty` as an object `{"idx":2,"name":"exhaust"}` (spec: `uint|string`), a 3-element `ButtonNote` `[0,480,"r"]` and a 4-element `LaserSection` `[0,[...],1,{"effect":"hp"}]` (spec: sizes 2 and 2-3). A strict reader may reject them; they are not KSM reference output.
No nulls; defaults for missing keys; graphs use `[v, vf]` immediate-change pairs; relative pulses inside laser sections; `difficulty` may be a string.

## Example
Real and synthetic files are in [samples/](samples/SOURCES.md) (`Gram_ex.kson` is a complete real chart; `oracle.kson` is a small synthetic one with BPM/time-signature changes, stop, slams and camera graphs). The spec has no complete sample chart in the sections consulted. Shape (illustrative, hand-built from the field tables above):
```json
{"format_version":1,"meta":{"title":"T","artist":"A","chart_author":"me","difficulty":3,"level":15,"disp_bpm":"140"},
 "beat":{"bpm":[[0,140.0]],"time_sig":[[0,[4,4]]]},
 "note":{"bt":[[0,[960,480]],[],[],[]],"fx":[[],[]],"laser":[[[0,[[0,0.0],[480,1.0]]]],[]]}}
```

## ROX support
Not read by ROX.

## Parsers & tools
libkson (C++): https://github.com/kshootmania/libkson · kson (Rust): https://lib.rs/crates/kson · kshoot (TS): https://www.npmjs.com/package/kshoot · ksm2sdvx (KSON -> VOX v13): https://github.com/Foahh/ksm2sdvx · VOXL4DD3R (KSH/KSON -> VOX v13): https://github.com/ooznon/VOXL4DD3R

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): `Gram_ex.kson` (a complete real chart converted by libkson) and four small synthetic fixtures from the VOXL4DD3R converter (BPM/time-signature changes, stop, scroll-speed curves, slam events, camera graphs, audio-effect definitions).
- Also committed: `kson-rs_Gram_ex.json` (the same real chart serialised by the Rust `kson` crate, MIT) and three tiny synthetic fixtures of `Foahh/ksm2sdvx` (`ksm2sdvx_minimal.kson`, `_notes`, `_camera`; that repository has no licence file).
- **More**: convert any KSH chart with libkson's `tool/ksh2kson.cpp` (https://github.com/kshootmania/libkson) or the `ksh2kson` example of https://github.com/Drewol/kson-rs (`kson/examples/ksh2kson.rs`, MIT); `kson-rs` also contains a KSON chart editor and game. KSM v2 (https://github.com/kshootmania/ksm-v2) is the reference player; the format site is https://kson.dev/. [inference] KSON charts found in the wild are almost all conversions of `.ksh`, so the KSH sources in [ksh](../ksh/README.md#getting-samples) apply.

## Sources
https://github.com/kshootmania/ksm-chart-format (`kson_format.md`) · https://kson.dev/
