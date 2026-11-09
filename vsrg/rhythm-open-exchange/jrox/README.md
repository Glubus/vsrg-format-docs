# ROX JSON (`.jrox`)
Kind: chart

Doc status: complete · ROX: reads/writes (native) · Category: vsrg (README index: interchange) · Encoding: json

## Overview

JSON serialisation of the ROX model (`RoxChart`) for debugging, diffing and tools that skip the binary codec. Same fields and validation as [`.rox`](../rox/README.md), but absolute note times and no compression. Source: `src/formats/jrox.rs` (`JroxDecoder`, `JroxEncoder`, extension `jrox`).

## Container & encoding

- UTF-8 JSON, one document, one chart per file. The encoder uses `serde_json::to_vec_pretty` (2-space indentation, field order = struct order); the decoder uses `serde_json::from_slice` on the whole input (`JROX parse error: ...` on failure).
- 100 MiB limit (`MAX_FILE_SIZE`; larger input is refused before parsing).
- `Encoder::encode` validates the chart before writing and `Decoder::decode` after parsing (rules in [../rox/README.md](../rox/README.md#timing-model)). Unlike `.rox`, a `.jrox` is not delta-encoded, not hash-checked, and `version` is not checked.

## Structure / metadata

Model types: [../rox/README.md](../rox/README.md#model-types). Serde mapping (derives `serde::Serialize/Deserialize`, no renames except the enum tagging):

- `RoxChart`: object `{ "version": u8, "key_count": u8, "metadata": {...}, "timing_points": [...], "notes": [...], "hitsounds": [...] }`.
- `Metadata`: object with snake_case keys `chart_id`, `chartset_id` (number or `null`), `title`, `artist`, `creator`, `difficulty_name`, `difficulty_value` (number or `null`), `audio_file`, `background_file` (string or `null`), `audio_offset_us`, `preview_time_us`, `preview_duration_us`, `source`, `genre`, `language` (string or `null`), `tags` (array of strings), `is_coop` (bool). serde does not apply the Rust `Default` impl (no `#[serde(default)]` on `Metadata`/`RoxChart`): non-`Option` fields must be present; `Option` fields may be omitted (a missing `Option` is `None`) [serde derive behaviour; not run].
- `TimingPoint` and `NoteType` use adjacent tagging `#[serde(tag = "type", content = "data")]`: `{"type": "Bpm", "data": {"time_us": 0, "bpm": 180.0, "signature": 4}}`, `{"type": "Sv", "data": {"time_us": 15000000, "scroll_speed": 0.5}}`, `{"type": "Tap"}`, `{"type": "Hold", "data": {"duration_us": 500000}}`, `{"type": "Burst", "data": {...}}`, `{"type": "Mine"}`.
- `Note`: `{ "time_us": i64, "note_type": <NoteType>, "hitsound_index": u16|null, "column": u8 }`.
- `Hitsound`: `{ "file": string, "volume": u8|null }`.

## Timing model

Identical to `.rox`: microsecond `i64` times, `Bpm`/`Sv` points, absolute note times.

## Notes

Tap, Hold, Burst, Mine as in `.rox`; columns 0-based.

## Audio & images

Names only (`audio_file`, `background_file`), as in `.rox`.

## Versions & variants

`version` is `3` in files written by 0.8.1 (`ROX_VERSION`); the decoder ignores it. Hand-edited files must keep notes and timing points sorted and BPM-first, or validation fails.

## Quirks & pitfalls

- A missing non-`Option` field of `RoxChart`/`Metadata`/`Note` fails the load (no serde defaults) [inference from the derives; not run].
- `bpm` and `scroll_speed` are `f32`, written in serde_json's shortest form (e.g. `180.0`).
- Key order is not significant on read.
- Decoding re-validates, so unsorted notes are refused.
- 50K notes ~ several MB of pretty JSON; use `.rox` for large charts.

## Example

Hand-built from the type definitions and serde attributes above (the content of the codec's round-trip unit test: 4K, title `Test`, BPM 180 at 0, one tap at 1 s on column 0); `to_vec_pretty` whitespace not reproduced:

```json
{
  "version": 3,
  "key_count": 4,
  "metadata": {
    "chart_id": null,
    "chartset_id": null,
    "title": "Test",
    "artist": "",
    "creator": "",
    "difficulty_name": "Normal",
    "difficulty_value": null,
    "audio_file": "",
    "background_file": null,
    "audio_offset_us": 0,
    "preview_time_us": 0,
    "preview_duration_us": 15000000,
    "source": null,
    "genre": null,
    "language": null,
    "tags": [],
    "is_coop": false
  },
  "timing_points": [
    { "type": "Bpm", "data": { "time_us": 0, "bpm": 180.0, "signature": 4 } }
  ],
  "notes": [
    { "time_us": 1000000, "note_type": { "type": "Tap" }, "hitsound_index": null, "column": 0 }
  ],
  "hitsounds": []
}
```

## ROX support

`JroxDecoder`/`JroxEncoder` (`src/formats/jrox.rs`), auto-detected by extension (`"jrox" => Jrox`), read + write, validated both ways.

## Parsers & tools

- Any JSON library; ROX `formats/jrox.rs` (Rust, serde_json).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: convert any supported chart with the ROX crate and write it with `JroxEncoder` or `auto_encode(&chart, "x.jrox")` [inference: extension picks the codec].

## Sources

- `rhythm-open-exchange/src/formats/jrox.rs`, `src/model/*.rs`, `src/codec/traits.rs`, `src/formats/auto/detect.rs`, `wiki.wiki/*.md`
