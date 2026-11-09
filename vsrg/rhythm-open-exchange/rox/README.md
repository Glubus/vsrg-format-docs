# ROX native binary (`.rox`)
Kind: chart

Doc status: complete · ROX: reads/writes (native) · Category: vsrg (README index: interchange) · Encoding: binary

## Overview

Compact native file of Rhythm Open Exchange 0.8.1: one chart, one key count, no archive. A 50K-note mania chart is about 133 KB (vs ~3 MB as `.osu`) and decodes in ~21 ms (ROX wiki, v0.7.0 benchmark). Written by `RoxNativeCodec` (`src/formats/rox_native`); the model is in `src/model`. The Rust code (rkyv `Archive` derives) defines the format; no written spec exists.

## Container & encoding

```
offset 0   : 4 bytes   magic  52 4F 58 00   ("ROX\0")   (ROX_MAGIC)
offset 4   : N bytes   one zstd frame (level 3 when written by the native encoder)
inflated   : an rkyv 0.8 archive of RoxChart (root object at the end of the buffer, as rkyv does)
```

- Encode (`encoder.rs`): `chart.validate()`, clone, **delta-encode the note times** (`notes[i].time_us := notes[i].time_us - notes[i-1].time_us`, first note relative to 0), `rkyv::to_bytes`, zstd level 3 (`COMPRESSION_LEVEL = 3`), prepend the magic.
- Decode (`decoder.rs`): require length >= 4 and the magic (`Invalid ROX file: missing magic bytes`); refuse files over 100 MiB (`MAX_FILE_SIZE`); inflate into a 16-byte aligned buffer capped at 64 MiB (`MAX_DECOMPRESSED`, anti zstd-bomb, `InvalidFormat`); validate the archive with `bytecheck` (`rkyv::access`, errors become `RoxError::Deserialize`); `check_counts`; deserialize; delta-decode the notes with wrapping addition; `chart.validate()`.
- No unchecked path (0.8.1 security fix, CHANGELOG: `from_bytes_unchecked` was used on unbounded input before).
- WASM builds: `compress` returns the raw rkyv bytes without zstd and the decoder reads the bytes after the magic as a raw archive. A `.rox` from a wasm32 build is not a zstd frame and a native build cannot read it, and vice versa [from the `#[cfg(target_arch = "wasm32")]` branches].
- Byte order / pointer width: `rkyv` is enabled with `default-features = false, features = ["alloc", "bytecheck"]` (Cargo.toml), so rkyv 0.8 defaults apply [inference: native endianness (little-endian on all supported targets), 32-bit relative pointers]. Read a `.rox` with the Rust crate or an rkyv reader built from the types below.
- Named `*.rox`, one per difficulty; detected by extension (`auto/detect.rs`: `"rox" => Rox`) or by the magic.

## Structure / metadata

### Model types

`RoxChart` (`src/model/chart.rs`), fields in archive order:

| Field | Type | Meaning |
|---|---|---|
| `version` | `u8` | format version, `ROX_VERSION = 3` |
| `key_count` | `u8` | number of columns (>= 1) |
| `metadata` | `Metadata` | see below |
| `timing_points` | `Vec<TimingPoint>` | BPM and SV points |
| `notes` | `Vec<Note>` | sorted by `time_us` |
| `hitsounds` | `Vec<Hitsound>` | keysound table |

`Metadata` (`src/model/metadata.rs`), all strings are `CompactString`:

| Field | Type | Default |
|---|---|---|
| `chart_id` | `Option<u64>` | None |
| `chartset_id` | `Option<u64>` | None |
| `title`, `artist`, `creator` | string | `""` |
| `difficulty_name` | string | `"Normal"` |
| `difficulty_value` | `Option<f32>` | None (OD, difficulty rating, ...) |
| `audio_file` | string (relative path) | `""` |
| `background_file` | `Option<string>` | None |
| `audio_offset_us` | `i64` | 0 |
| `preview_time_us` | `i64` | 0 |
| `preview_duration_us` | `i64` | 15 000 000 (15 s) |
| `source`, `genre`, `language` | `Option<string>` | None |
| `tags` | `Vec<string>` | empty |
| `is_coop` | `bool` | false (requires an even `key_count`) |

`key_count` sits on `RoxChart` because it is a gameplay property (wiki).

`TimingPoint` (`timing.rs`), enum, two variants:

| Variant | Fields |
|---|---|
| `Bpm` | `time_us: i64`, `bpm: f32`, `signature: u8` (numerator of the time signature, 4 for 4/4) |
| `Sv` | `time_us: i64`, `scroll_speed: f32` (multiplier; does not change timing) |

`Note` (`note.rs`):

| Field | Type | Meaning |
|---|---|---|
| `time_us` | `i64` | start time in microseconds (delta-encoded inside `.rox`) |
| `note_type` | `NoteType` | `Tap`, `Hold { duration_us: i64 }`, `Burst { duration_us: i64 }` (roll / rapid tapping), `Mine` |
| `hitsound_index` | `Option<u16>` | index into `hitsounds` (up to 65 535 samples) |
| `column` | `u8` | 0-indexed column |

`Hitsound` (`hitsound.rs`): `file: CompactString` (relative path), `volume: Option<u8>` (0-100; `with_volume` clamps to 100).

### Limits (decoder)

| Constant | Value |
|---|---|
| `MAX_FILE_SIZE` | 100 MiB (`rox_native/mod.rs`) |
| `MAX_DECOMPRESSED` | 64 MiB |
| `MAX_NOTES` | 4 000 000 |
| `MAX_TIMING_POINTS` | 1 000 000 |
| `MAX_HITSOUNDS` | 1 000 000 |

## Timing model

Microsecond `i64` timestamps everywhere. `Bpm` points give tempo (`bpm: f32`, `signature` for bar lines); `Sv` points scale scroll speed only. Times are absolute; beats derive from the BPM points (`analysis::bpm`). Validation (`src/codec/validate.rs`, run by `encode` and `decode`, in this order, first error wins):

1. `key_count != 0`; if `is_coop`, `key_count` must be even.
2. Timing points sorted by `time_us`; if there are notes: at least one `Bpm` point and the first `Bpm` point must be at or before the first note.
3. Notes sorted by `time_us`.
4. `column < key_count`.
5. No overlap: per column, a note must not start before the previous note of that column ended (`end_time_us = time_us + duration_us`).
6. `Hold`/`Burst` `duration_us > 0`.

## Notes

Mapping from other formats (ROX wiki "Notes"): StepMania `1`/`2`,`3`/`4`/`M`; osu!mania circle/hold; Quaver tap/LN (the Quaver decoder maps no mines); FNF notes; osu!taiko don/kat. `RoxChart::remove_unsupported_notes` drops mines and bursts for games that cannot play them.

## Audio & images

Names only: `audio_file`, `background_file` (relative paths); times `audio_offset_us`, `preview_time_us`, `preview_duration_us`. Keysounds: `hitsounds` table + `hitsound_index`.

## Versions & variants

- `ROX_VERSION = 3`. CHANGELOG 0.7.0: "`.rox` binary format v3: Files encoded with version 2 are rejected with `RoxError::UnsupportedVersion(2)`. The `TimingPoint` enum has a different rkyv binary layout than the old struct."
- In 0.8.1 the `version` byte is stored and `RoxError::UnsupportedVersion` exists, but nothing in `src/` compares it on decode [inference from grep: `ROX_VERSION` is used only as the constant and in `RoxChart::new`]; an old file fails at archive validation.
- No content hash is stored. `analysis::hash` (feature `analysis`) computes `xxh3_128` over the rkyv bytes of the chart (`hash`, 32 hex chars), the notes (`notes_hash`), the timing points (`timings_hash`), the first 16 hex chars (`short_hash`), and a rate-independent `normalized_notes_hash(chart, target_bpm)` (note times scaled so the dominant BPM equals `target_bpm`, truncating toward zero). The README says "BLAKE3 content hashing" but the code uses xxHash3-128 (no blake3 dependency in Cargo.toml) [observed discrepancy].

## Quirks & pitfalls

- Stored note times are deltas; skipping `delta_decode_notes` gives wrong times. Writers must sort notes first.
- wasm32 and native files differ (raw vs zstd).
- The archive layout depends on the exact type definitions and rkyv version; field order or enum layout changes break files (as the 0.7.0 `TimingPoint` change did).
- Decoding runs semantic validation: a structurally fine file with overlapping notes is rejected.
- Hitsound index is `Option<u16>`; strings are `CompactString` in the archive.

## Example

Binary, no bytes shown. The codec's unit test (`rox_native/decoder.rs`: `RoxChart::new(4)`, one `TimingPoint::bpm(0, 180.0)`, `Note::tap(1_000_000, 0)`, `Note::hold(2_000_000, 500_000, 1)`) has a logical equivalent in the JSON form in [../jrox/README.md](../jrox/README.md).

## ROX support

Reference implementation (`RoxNativeCodec`, extensions `["rox"]`): read + write, checked decoding, detected by extension.

## Parsers & tools

- `rhythm-open-exchange` (Rust, crate `rox`): https://github.com/Glubus/rhythm-open-exchange ; vendored in this repository.
- C# bindings `RhythmOpenExchange` (NuGet 0.5.0 per README).
- rkyv: https://rkyv.org/ ; zstd: https://github.com/facebook/zstd

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (all 4K; no genuine non-4K file was available). To make more, decode any supported chart and re-encode it: `let chart = auto_decode(path)?; auto_encode(&chart, "output.rox")?;` (crate `rhythm-open-exchange` 0.8.1, library `rox`; the repo's `examples/auto_conversion.rs`). Upstream `Glubus/rhythm-open-exchange` ships no `.rox`. Layout checked on the samples [observed]: the zstd payload is an rkyv root at the end of the buffer (200 bytes for `RoxChart`: `version`, `key_count`, `Metadata` at offset 8, the three vector headers last); notes are 32-byte records with delta-encoded `time_us`.

## Sources

- `rhythm-open-exchange/src/formats/rox_native/{mod,encoder,decoder}.rs`, `src/model/{chart,metadata,note,timing,hitsound}.rs`, `src/codec/{traits,validate}.rs`, `src/analysis/hash.rs`, `src/error.rs`, `Cargo.toml`, `CHANGELOG.md`, `wiki.wiki/{Notes,Timing-Points,Metadata,Hitsounds,Performance-Optimizations}.md`, `README.md`
