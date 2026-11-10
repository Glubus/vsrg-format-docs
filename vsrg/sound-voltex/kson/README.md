# K-Shoot MANIA JSON chart (`.kson`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: json

## Overview
KSON is the JSON successor of [`ksh`](../ksh/README.md), specified by the K-Shoot MANIA project (spec v1.0.2, `format_version: 1`, CC0). Notes sit on an absolute pulse grid; graphs support curves (camera, scroll speed, laser); KSH-only leftovers go in `compat`. Used by KSM v2 development, Unnamed SDVX Clone (`kson-rs`) and editors. Audio-effect tables (spec lines 235-656: `audio.audio_effect`, parameter types/lists) and camera details are only summarized.

## Container & encoding
JSON, UTF-8 without BOM, LF line endings, `.kson` extension, no `null` values. Undefined values take their defaults; unsupported "(OPTIONAL SUPPORT)" parameters must be ignored. One file = one difficulty.

## Structure / metadata
Top level: `format_version` (uint), `meta`, `beat`, optional `gauge`, `note`, `audio`, `camera`, `bg`, `editor`, `compat`, `impl`.

- `meta`: `title`, `title_translit?`, `title_img_filename?`, `artist`, `artist_translit?`, `artist_img_filename?`, `chart_author`, `difficulty` (uint 0-3 = light/challenge/extended/infinite, or a name; KSM ignores names -> 3), `level` (1-20), `disp_bpm` (string), `std_bpm?`, `jacket_filename?`, `jacket_author?`, `icon_filename?`, `information?`.
- `gauge.total` (0 = auto).
- `audio.bgm`: `filename`, `vol` (1.0), `offset` (ms, 0), `preview` {`offset` ms 0, `duration` ms 15000}, `legacy.fp_filenames` (prerendered FX/laser variants).
- `audio.key_sound` (`fx`, `laser`: chip FX samples, slam sounds) and `audio.audio_effect` (`fx`, `laser` definitions and events: see the spec).
- `camera` (`tilt`, `cam.body`, `cam.pattern`), `bg` (`legacy.bg`, `layer`, `movie`), `compat.ksh_unknown` (KSH options without a kson counterpart), `editor`, `impl`.

## Timing model
- Pulse `y` resolution: 240 per beat = 960 per measure (4/4).
- `beat.bpm`: `ByPulse<double>[]` = `[[y, bpm], ...]`.
- `beat.time_sig`: `ByMeasureIdx<TimeSig>[]` = `[[measure_idx, [num, den]], ...]`, default `[[0,[4,4]]]`.
- `beat.scroll_speed`: GraphPoint[] default `[[0,1.0]]`; `beat.stop`: `[[y, duration_pulses]]` (equal to scroll speed 0 for a duration; stop has priority).
- Time of pulse y: integrate BPM over pulses (1 beat = 240 pulses). Time-signature changes only move measure lines (measure length in pulses = 960 * num/den [inference from the unit definitions]).

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
- [observed: oracle.kson, effects.kson] Files from the VOXL4DD3R converter deviate from the spec text: `meta.difficulty` as an object `{"idx":2,"name":"exhaust"}` (spec: `uint|string`), a 3-element `ButtonNote` `[0,480,"r"]` and a 4-element `LaserSection` `[0,[...],1,{"effect":"hp"}]` (spec: sizes 2 and 2-3). A strict reader may reject them; they are not KSM reference output.
- No nulls; defaults for missing keys; graphs use `[v, vf]` immediate-change pairs; relative pulses inside laser sections; `difficulty` may be a string.

## Example
Hand-built from the field tables (real files: [samples/](samples/SOURCES.md); the spec has no complete sample chart in the sections consulted):
```json
{"format_version":1,"meta":{"title":"T","artist":"A","chart_author":"me","difficulty":3,"level":15,"disp_bpm":"140"},
 "beat":{"bpm":[[0,140.0]],"time_sig":[[0,[4,4]]]},
 "note":{"bt":[[0,[960,480]],[],[],[]],"fx":[[],[]],"laser":[[[0,[[0,0.0],[480,1.0]]]],[]]}}
```

## ROX support
Decode only (`rox::formats::kson::KsonDecoder`, by the `.kson` extension). 6 columns as the `.ksh` reader: `note.bt[0..4]` BT A-D, `note.fx[0..2]` FX-L/FX-R; lasers dropped and counted. Pulses (240 a beat) to time through `beat.bpm`; `audio.bgm.offset` moves every time (as the ksh `o`; libkson copies one to the other); `time_sig` only sets the signature of the BPM points; `scroll_speed` and `stop` (scroll only) are counted. A 3-element `ButtonNote` or a 4-element `LaserSection` (converter output) is read by its first entries. 20 of the 23 `.kson` decode; the 3 others have no button note (camera, minimal and speed-curve fixtures). `kson-rs_Gram_ex.json` (a KSON chart saved as `.json` by `kson-rs`) is not read: the extension is `.kson`, and a `.json` goes to the FNF/Bestdori/BDON content checks.

## Parsers & tools
libkson (C++): https://github.com/kshootmania/libkson · kson (Rust): https://lib.rs/crates/kson · kshoot (TS): https://www.npmjs.com/package/kshoot · ksm2sdvx (KSON -> VOX v13): https://github.com/Foahh/ksm2sdvx · VOXL4DD3R (KSH/KSON -> VOX v13): https://github.com/ooznon/VOXL4DD3R

## Getting samples
Committed: see [samples/SOURCES.md](samples/SOURCES.md).
- Convert any KSH chart with libkson's `tool/ksh2kson.cpp` (https://github.com/kshootmania/libkson) or the `ksh2kson` example of https://github.com/Drewol/kson-rs (`kson/examples/ksh2kson.rs`, MIT). KSM v2 (https://github.com/kshootmania/ksm-v2) is the reference player; the format site is https://kson.dev/. [inference] KSON charts in the wild are almost all conversions of `.ksh`, so the KSH sources in [ksh](../ksh/README.md#getting-samples) apply.
- Nautica (https://ksm.dev): the public API https://ksm.dev/app/songs?page=N (JSON, 10 songs per page, `cdn_download_url` = zip on the CDN) lists ~7 400 songs; 91 of the 400 newest scanned (about 1 in 4) contained a `.kson` member. Zips support HTTP range requests, so the zip directory and one member can be read without the audio.

## Sources
https://github.com/kshootmania/ksm-chart-format (`kson_format.md`) · https://kson.dev/
