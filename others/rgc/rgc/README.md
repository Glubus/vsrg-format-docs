# RGC (Rhythm Game Chart) (`.rgc`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview

RGC is a game-agnostic JSON chart format whose spec follows the npm package `@rhythm-gaming/rgc` version. Goals: support many games, convert easily from/to other formats, enable prototyping. Non-goals: becoming "the standard", replacing KSON or bmson, a hashable canonical form. A chart is a header, metadata, timing (ticks, offset, BPM, time signature) and a map of lane groups holding notes. Note position dimension is game-defined (0 for Taiko/SDVX notes, 1 for SDVX lasers or camera angle, 2 for osu!).

## Container & encoding

UTF-8 JSON (no BOM recommended), usually `.rgc`. Top level is an object with no duplicated fields; `null` is forbidden unless stated. 64-bit integers may be base-10 strings; magnitudes are assumed < 2^53; non-finite floats are forbidden. Unknown fields may be ignored; where "custom fields allowed", preserve them.

## Structure / metadata

```text
RGC { header, meta, timing, chart: map<string, LaneGroup> }   // custom fields allowed
header   { version?: semver (no 'v'), editor?: "id semver", game?: "game[/mode]" (e.g. sdvx, ddr/dp) }
meta     { title?, music?, chart?, jacket?: { author?, path? } }
timing   { offset?: i32 ms, res?: u16, bpm?: [[tick, bpm]...], sig?: [[tick, [num, unit]]...] }
LaneGroup{ dim?: u8, lane: Note[][] }
Note     { t: Tick, id?: string, k?: string (kind), l?: Tick (length), v?: Pos (start), w?: Pos (end), p?: object }
```
`chart` keys are lane-group ids (may be empty string); every note of a lane group shares the same dimension; notes in a lane sorted by `t`. Level/difficulty are suggested as custom `meta` fields. `Pos` depends on `dim`: 0 = omitted or an empty array, 1 = a number or a one-element array, 2+ = an array of exactly `dim` numbers; `w` defaults to `v`. Notes may be written in a compact array form (`t`, `[k?, t, l?, p?]`, `[k?, t, [v, w?], l?, p?]`), which every reader must accept (spec, read in full).

## Timing model

Integer ticks: `res` ticks per quarter note (default 24 = 96 per 4/4 measure; `4*res` must be a multiple of every time-signature beat unit). `offset` (ms, may be negative) is the audio position of tick 0. BPM is quarter notes per 60 s; `bpm` entries `[tick, bpm]` are sorted with unique ticks and positive values (default 120). Time signatures default to 4/4 and the first must be at tick 0; no anacrusis (use two signatures). Seconds = integrate ticks via BPM, then add `offset`.

## Notes

A note has start tick `t`, optional length `l` (hold-like), optional start `v` and end `w` positions (tuples of the lane group's `dim` size), kind `k` (CSS-class-like id) and free properties `p`. Overlapping notes are allowed. Scroll-speed and camera angle changes are notes in lanes.

## Audio & images

`meta.music.path`, `meta.chart.path`, `meta.jacket.path` (optional paths + authors).

## Versions & variants

`header.version` follows the package semver. KSON (SDVX) and bmson inspired it.

## Quirks & pitfalls

`dim` is per lane group; kind and lane semantics are game-defined; JSON numbers beyond 2^53 are strings.

## Example

`calibration.rgc` of the rgc repository (MIT), complete ([samples/calibration.rgc](samples/calibration.rgc)): `{"header": {"version": "0.2.0", "game": "sdvx"}, "meta": {"title": "Calibration", "music": {"author": "HEXAGON", "path": "offset.ogg"}, "chart": {"author": "HEXAGON"}, "jacket": {"author": "HEXAGON", "path": "offset-1.png"}}, "timing": {"offset": 1000, "res": 1, "bpm": [[0, 120]], "sig": [[0, [4, 4]]]}, "chart": {"bt": {"dim": 0, "lane": [[0, 1, 2, 3, 16, 17, 18, 19, 32, 33, 34, 35, 48, 49, 50, 51], ...]}}}` [observed: calibration.rgc; three more `bt` lanes of the same shape follow]. Notes are written in the *compact note format* of the spec (a bare integer = a 0-dimensional note at that tick; `[k, t, l, p]` for 0-D notes with kind/length/property, `[k, t, [v, w], l, p]` for 1+D notes); the spec's own example of the same chart says `"version": "0.3.0"`, the sample file has `0.2.0`. [spec read in full in the rgc repository, `docs/spec.md`]


## ROX support

Not read by ROX.

## Parsers & tools

@rhythm-gaming/rgc (TypeScript library, `lib.md`): <https://github.com/rhythm-gaming/rgc>; rgchart (Rust/WASM): <https://github.com/R2O3/rgchart>.

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). No other public `.rgc` collection found (the rgc repo has only `test/chart/sdvx/calibration.rgc`; R2O3's rgchart has test maps in other formats). The library `@rhythm-gaming/rgc` and converters write the format.

## Sources

- <https://raw.githubusercontent.com/rhythm-gaming/rgc/main/docs/spec.md> (read in full; commit 724560c47a12fd2d13170370f1e2b8074d482951 for the sample)
- <https://rgc.readthedocs.io/en/latest/> (listed in search)
