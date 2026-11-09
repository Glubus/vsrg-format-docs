# ROX YAML (`.yrox`)
Kind: chart

Doc status: complete · ROX: reads/writes (native) · Category: vsrg (README index: interchange) · Encoding: text (YAML)

## Overview

YAML serialisation of the ROX model (`RoxChart`): the same data as [`.jrox`](../jrox/README.md) and [`.rox`](../rox/README.md), easier to edit by hand. Source: `src/formats/yrox.rs` (`YroxDecoder`, `YroxEncoder`, extension `yrox`), `serde_yaml` 0.9.

## Container & encoding

- UTF-8 YAML, one document per file. Encoder: `serde_yaml::to_string(chart)` bytes; decoder: `serde_yaml::from_slice` (`YROX parse error: ...`). 100 MiB limit.
- `chart.validate()` runs on `encode` and `decode`, as in the other native formats. No delta encoding, no `version` check.

## Structure / metadata

Model: [../rox/README.md](../rox/README.md#model-types). The serde structure is that of [../jrox/README.md](../jrox/README.md#structure--metadata), as YAML mappings and sequences. Top-level keys: `version`, `key_count`, `metadata`, `timing_points`, `notes`, `hitsounds`. The enums `TimingPoint` and `NoteType` use adjacent tagging (`type` + `data`), which serde_yaml 0.9 writes as a mapping with those two keys (no YAML `!tag`s): `type: Bpm` then `data: {time_us, bpm, signature}`; unit variants (`Tap`, `Mine`) have only `type`.

## Timing model

As in `.rox` / `.jrox` (microseconds, absolute note times).

## Notes

As in `.rox`.

## Audio & images

As in `.rox`.

## Versions & variants

`version: 3` (`ROX_VERSION`), not checked on decode.

## Quirks & pitfalls

- YAML quirks apply: strings that look like numbers/booleans (a title like `1999`, `yes`) are quoted by the serialiser; hand-edited files must quote them or serde reports a type error [general YAML 1.2/serde_yaml behaviour, not tested here].
- Non-`Option` fields of `Metadata` are required (no serde defaults; `Option` fields may be omitted) [inference from the derives].
- Large for big charts (one mapping per note).

## Example

Hand-built from the structure above (same chart as the `.jrox` example; `serde_yaml` scalar quoting not reproduced by running it):

```yaml
version: 3
key_count: 4
metadata:
  chart_id: null
  chartset_id: null
  title: Test
  artist: ''
  creator: ''
  difficulty_name: Normal
  difficulty_value: null
  audio_file: ''
  background_file: null
  audio_offset_us: 0
  preview_time_us: 0
  preview_duration_us: 15000000
  source: null
  genre: null
  language: null
  tags: []
  is_coop: false
timing_points:
- type: Bpm
  data:
    time_us: 0
    bpm: 180.0
    signature: 4
notes:
- time_us: 1000000
  note_type:
    type: Tap
  hitsound_index: null
  column: 0
hitsounds: []
```

## ROX support

`YroxDecoder`/`YroxEncoder`, auto-detected by extension (`"yrox" => Yrox`), read + write.

## Parsers & tools

- Any YAML library; ROX `formats/yrox.rs` (Rust, serde_yaml).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: convert any supported chart with the ROX crate and write it with `YroxEncoder`.

## Sources

- `rhythm-open-exchange/src/formats/yrox.rs`, `src/model/*.rs`, `src/formats/auto/detect.rs`
