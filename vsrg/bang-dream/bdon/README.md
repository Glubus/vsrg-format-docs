# BDON - BanG Dream! Our Notes chart (`.bdon` / `.json` / `.json.gz`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg (lane/board-based vertical highway) · Encoding: json (optionally gzip)

## Overview

**BDON** is the JSON chart format of **BanG Dream! Our Notes**, as understood by the converter library `rg-converters` (UntitledCharts), whose README lists it as "Loading-Only Support: `.bdon/.json/.json.gz` - BDON (BanG Dream! Our Notes) chart json". Charts are a list of notes on a **24-unit-wide board**, with taps, flicks, traces, long (slide) notes made of nodes with easing, guides, and tempo/skill/fever events. The game's own documentation is not public; this page is reconstructed from the validating loader `cpp/src/converters/bdon/loader.cpp`, which rejects documents that do not match the schema ("expected an array", "expected one of a fixed set of values" ...). Anything not read by that loader is unknown. It is a different format from the older BanG Dream! (Bestdori) ones documented in [`../bestdori-json`](../bestdori-json/README.md) and [`../txt`](../txt/README.md).

## Container & encoding

- A single JSON object. The loader transparently gunzips the input when it starts with `1f 8b` (so `.json.gz` is accepted); otherwise it parses plain JSON text (UTF-8). Invalid gzip/JSON or a non-object root are errors.

## Structure / metadata

```json
{ "score": { "notes": [ <note>, ... ], "events": { "bpm": [...], "skill": [...], "fever": [...] } } }
```

`score` must be an object; `score.notes` an array (absent = empty); `score.events` an object (absent/null = empty).

### Events (`score.events`)

| Key | Item | Meaning |
|---|---|---|
| `bpm` | `{ "t": tick, "bpm": number }` | Tempo changes; `bpm` default 120, valid range 0.001..100000; sorted by `t`; if the first change is after tick 0 (or none), a 120 BPM point is inserted at tick 0. |
| `skill` | tick (integer) | Skill activation times; the n-th entry is skill slot n (1-based). |
| `fever` | `[startTick, endTick]` | Fever sections (`end >= start` required). |

### Notes (`score.notes`)

Each item has `type` in `tap` (default), `flick`, `trace`, `long`, `guide`, `node`. Single notes and the **nodes** of long/guide notes share these fields:

| Field | Type | Meaning |
|---|---|---|
| `t` | integer >= 0 | Tick. |
| `pos` | number or `"auto"` | Left edge on the 24-unit board; `"auto"` = interpolate between neighbouring nodes. |
| `size` | number | Width in board units, default **6**. |
| `crit` | bool | Critical (gold) note, default false. |
| `visible` | bool | Default true; `false` = hidden (no judgement). |
| `ease` | `"linear"`, `"in"`, `"out"` or a 2-element array `[left, right]` | Edge easing towards the next node (default linear). |
| `dir` | `"left"`, `"up"`, `"right"` | Flick direction, default up. |
| `alpha` | `"none"`, `"fadeIn"`, `"fadeOut"` | Fade of guide start/end, default none. |

`long` and `guide` notes carry `node`: an array of node objects (the note's own `t`, if present, is the first node); at least **two nodes** are required. Slides: node 0 = start (judge: `visible` + `trace`), last = end (flick/trace possible), intermediate = relays (`"auto"` positions become "attach" relays). Guides: coloured line (yellow if any node is `crit`, green otherwise), with fade derived from the first/last node `alpha`.

## Timing model

Tick based; the loader uses **480 ticks per beat** (`TICKS_PER_BEAT = 480`) and converts `beat = tick / 480`. Tempo from `events.bpm`. No offset or audio information appears in the schema (the converter sets `waveoffset` to 0, so the audio offset lives elsewhere).

## Notes

- Tap, flick (with `dir`), trace (hold-free "friction" type), long (slide with nodes), guide (decorative line, optionally judged via converter option `guide_traces`).
- A flick that overlaps a long note body within 4 ticks and overlapping horizontal range is treated as a trace by the converter (`flick_body_collide`).
- Horizontal geometry: `lane = (left + width/2 - 12) * 0.5`, `size = width * 0.25` in the converter's 12-lane score units (board 24 units mapped onto 12).

## Audio & images

None.

## Versions & variants

Unknown; only the current schema as implemented by the converter is known.

## Quirks & pitfalls

- Strict validation: unknown `type`/`ease`/`dir`/`alpha` strings are errors, not ignored.
- `pos: "auto"` must be resolved by interpolation between the nearest non-auto neighbours (the first/last auto node copies the first node's left/width).
- Ticks must be non-negative integers (fractions rejected).
- Heavily dependent on interpretation (flick-on-slide-body collision) when converting to PJSK-like models.

## Example

Illustrative, hand-built from the loader's field list (not a real chart):

```json
{ "score": {
  "events": { "bpm": [ { "t": 0, "bpm": 150 } ], "skill": [ 1920 ], "fever": [ [3840, 5760] ] },
  "notes": [
    { "type": "tap", "t": 480, "pos": 9, "size": 6 },
    { "type": "flick", "t": 960, "pos": 12, "dir": "right" },
    { "type": "long", "node": [ { "t": 1440, "pos": 6 }, { "t": 1920, "pos": "auto" }, { "t": 2400, "pos": 12 } ] }
  ] } }
```

## ROX support

Not read by ROX. The model (wide free-position notes on a 24-unit board, slides with eased edges, guides) does not fit ROX columns; only taps would convert cleanly.

## Parsers & tools

`rg-converters` (C++/Python): https://github.com/UntitledCharts/rg_converters (`cpp/src/converters/bdon/loader.cpp`, loading only; options `guide_traces`, `trace_ends`, `flick_body_collide`).

## Getting samples

- Committed in [`samples/`](samples/): 6 real score files (4 JP, 2 Intl) from https://github.com/haneoka-gakuen/ournotes-charts (byte-exact `original/*.bytes`, which are plain JSON). Everything is listed with origin, date and sha256 in [`samples/SOURCES.md`](samples/SOURCES.md).
- Observed [observed in samples/ournotes-jp_0003_02.json]: besides `score.notes` and `score.events.{bpm,skill,fever}` described above, the files hold `meta.version` (100), `events.sig` (`{"t":0,"sig":[4,4]}`) and `events.call` (`{"t":0,"timing":[0,1,0,1]}`); notes without `type` are taps (`t`, `pos`, `size`), long/guide notes have `node` arrays; ticks are in 1/480-beat units [matches fiche]; chart file names are `<4-digit music id>_<2-digit difficulty>`. Compact JSON, no BOM, no gzip.
- More: the same repository has 20 `original/` and `scores/` (pretty-printed) files per server plus `tables/` with MasterLiveMusic; `ryougishiiki/our-notes-chartdb` builds a normalised database; the official CDN is the source.

## Sources

- https://github.com/UntitledCharts/rg_converters (commit `673710dcc441aea97ac89e113f811d5c169763d4`): `README.md`, `cpp/src/converters/bdon/loader.cpp`, `cpp/include/rg/converters/bdon.hpp`
