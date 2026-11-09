# ROX YAML (`.yrox`)
Kind: chart

Doc status: complete · ROX: reads/writes (native) · Category: vsrg (README index: interchange) · Encoding: text (YAML)

## Overview

`.yrox` is the YAML serialisation of the ROX model (`RoxChart`): the same data as [`.jrox`](../jrox/README.md) and [`.rox`](../rox/README.md), in a form easier to edit by hand. Source: `src/formats/yrox.rs` (`YroxDecoder`, `YroxEncoder`, extension `yrox`), `serde_yaml` 0.9.

## Container & encoding

- UTF-8 YAML, one document per file. Encoder: `serde_yaml::to_string(chart)` bytes; decoder: `serde_yaml::from_slice` (`YROX parse error: ...`). 100 MiB limit.
- Validation on `encode` and `decode` as in the other native formats (`chart.validate()`); no delta encoding, no `version` check.

## Structure / metadata

The model is the one of [../rox/README.md](../rox/README.md#model-types); the serde structure is the same as in [../jrox/README.md](../jrox/README.md#structure--metadata), expressed as YAML mappings and sequences: top-level keys `version`, `key_count`, `metadata`, `timing_points`, `notes`, `hitsounds`. The enums `TimingPoint` and `NoteType` use adjacent tagging (`type` + `data`), which serde_yaml 0.9 writes as a mapping with those two keys (not as YAML `!tag`s): `type: Bpm` then `data: {time_us, bpm, signature}`; unit variants (`Tap`, `Mine`) have only `type`.

## Timing model

As in `.rox` / `.jrox` (microseconds, absolute note times).

## Notes

As in `.rox`.

## Audio & images

As in `.rox`.

## Versions & variants

`version: 3` (`ROX_VERSION`), not checked on decode.

## Quirks & pitfalls

- YAML quirks apply: strings that look like numbers/booleans (a title like `1999`, `yes`) are quoted by the serialiser; hand-edited files must quote them or serde will complain about the type [general YAML 1.2/serde_yaml behaviour, not tested here].
- Non-`Option` fields of `Metadata` are required (no serde defaults; `Option` fields may be omitted) [inference from the derives].
- Pretty large for big charts (one mapping per note).

## Example

Illustrative, hand-built from the structure above (same chart as the `.jrox` example; the exact scalar quoting of `serde_yaml` was not reproduced by running it):

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

- **Committed** ([`samples/`](samples/), see [`SOURCES.md`](samples/SOURCES.md)): six real charts written as `.yrox` (decoded from the real `.rox` samples by a Python script emulating `serde_yaml`; scalar quoting may differ from the Rust output) plus three hand-written synthetic files.
- **More**: convert any supported chart with the ROX crate and write it with `YroxEncoder`.

## Sources

- `rhythm-open-exchange/src/formats/yrox.rs`, `src/model/*.rs`, `src/formats/auto/detect.rs`
