# ROX native binary (`.rox`)
Kind: chart

Doc status: complete · ROX: reads/writes (native) · Category: vsrg (README index: interchange) · Encoding: binary

## Overview

`.rox` is the compact native file of Rhythm Open Exchange 0.8.1: one chart, one key count, no archive. A 50K-note mania chart is about 133 KB (vs ~3 MB as `.osu`) and decodes in ~21 ms (ROX wiki, v0.7.0 benchmark). Files are produced by `RoxNativeCodec` (`src/formats/rox_native`), the model is in `src/model`. The format is defined by the Rust code (rkyv `Archive` derives) rather than by a written spec; this page derives it from the source.

## Container & encoding

```
offset 0   : 4 bytes   magic  52 4F 58 00   ("ROX\0")   (ROX_MAGIC)
offset 4   : N bytes   one zstd frame (level 3 when written by the native encoder)
inflated   : an rkyv 0.8 archive of RoxChart (root object at the end of the buffer, as rkyv does)
```

- Encode (`encoder.rs`): `chart.validate()` first (trait template), then clone the chart, **delta-encode the note times** (`notes[i].time_us := notes[i].time_us - notes[i-1].time_us`, first note relative to 0), serialise with `rkyv::to_bytes`, compress with zstd level 3 (`COMPRESSION_LEVEL = 3`), prepend the magic.
- Decode (`decoder.rs`): check length >= 4 and the magic (`Invalid ROX file: missing magic bytes`); refuse a file larger than 100 MiB (`MAX_FILE_SIZE`); inflate the zstd frame into a 16-byte aligned buffer with a hard cap of 64 MiB (`MAX_DECOMPRESSED`, anti zstd-bomb, `InvalidFormat`); validate the archive with `bytecheck` (`rkyv::access`, errors become `RoxError::Deserialize`); check counts (`check_counts`); deserialize to `RoxChart`; delta-decode the notes with wrapping addition; finally `chart.validate()`.
- No unchecked path (0.8.1 security fix, CHANGELOG: before, `from_bytes_unchecked` was used on unbounded input).
- WASM builds: `compress` returns the raw rkyv bytes without zstd, and the wasm decoder reads the bytes after the magic as a raw archive. So a `.rox` written by a wasm32 build is NOT a zstd frame and is not readable by a native build, and vice versa [from the `#[cfg(target_arch = "wasm32")]` branches].
- Byte order / pointer width of the rkyv archive: ROX enables `rkyv` with `default-features = false, features = ["alloc", "bytecheck"]` (Cargo.toml); no explicit endianness or pointer-width feature is selected, so rkyv 0.8's defaults apply [inference: native endianness (little-endian on all supported targets), 32-bit relative pointers]. The authoritative way to read a `.rox` is the Rust crate (or a rkyv-compatible reader built from the same type definitions below).
- File naming: `*.rox`, one per difficulty; detection by extension (`auto/detect.rs`: `"rox" => Rox`). The magic is also a reliable signature.

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

`key_count` is on `RoxChart`, not on `Metadata`, because it is a gameplay property (wiki).

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

Microsecond `i64` timestamps for everything (notes, durations, timing points, offsets). `Bpm` points give the tempo (`bpm: f32`, `signature` for bar lines); `Sv` points scale scroll speed only. Position -> time is trivial (times are absolute); beat positions are derived from the BPM points (`analysis::bpm`). Validation rules (`src/codec/validate.rs`, run by `encode` and `decode`, in this order, first error wins):

1. `key_count != 0`; if `is_coop`, `key_count` must be even.
2. Timing points sorted by `time_us`; if there are notes: at least one `Bpm` point and the first `Bpm` point must be at or before the first note.
3. Notes sorted by `time_us`.
4. `column < key_count`.
5. No overlap: per column, a note must not start before the previous note of that column ended (`end_time_us = time_us + duration_us`).
6. `Hold`/`Burst` `duration_us > 0`.

## Notes

See the model table. Tap/Hold/Burst/Mine map from other formats as in the ROX wiki "Notes": StepMania `1`/`2`,`3`/`4`/`M`; osu!mania circle/hold; Quaver tap/LN (mines are not mapped by the Quaver decoder); FNF notes; osu!taiko don/kat. `RoxChart::remove_unsupported_notes` drops mines and bursts for games that cannot play them.

## Audio & images

Only names: `audio_file`, `background_file` (relative paths); times `audio_offset_us`, `preview_time_us`, `preview_duration_us`. Keysounds: `hitsounds` table + `hitsound_index`.

## Versions & variants

- `ROX_VERSION = 3`. CHANGELOG 0.7.0: "`.rox` binary format v3: Files encoded with version 2 are rejected with `RoxError::UnsupportedVersion(2)`. The `TimingPoint` enum has a different rkyv binary layout than the old struct."
- In the 0.8.1 source the `version` byte is stored and `RoxError::UnsupportedVersion` exists, but no code in `src/` compares it on decode [inference from grep: the only uses of `ROX_VERSION` are the constant and `RoxChart::new`]; an old file fails at archive validation instead.
- Content hashes are NOT stored in the file. `analysis::hash` (feature `analysis`) computes `xxh3_128` over the rkyv bytes of the whole chart (`hash`, 32 hex chars), of the notes only (`notes_hash`), of the timing points only (`timings_hash`), the first 16 hex chars (`short_hash`), and a rate-independent `normalized_notes_hash(chart, target_bpm)` (note times scaled so that the dominant BPM equals `target_bpm`, truncation toward zero). The README says "BLAKE3 content hashing", but the code uses xxHash3-128 (no blake3 dependency in Cargo.toml): the README is outdated [observed discrepancy].

## Quirks & pitfalls

- Stored note times are deltas: a reader that skips `delta_decode_notes` gets wrong times. A writer must sort notes first (validation guarantees it).
- wasm32 / native files differ (zstd vs raw).
- `rkyv` archive layout depends on the exact type definitions and rkyv version: field order and enum layout change break files (as the 0.7.0 `TimingPoint` change did).
- Decoding also runs semantic validation: a structurally fine file with overlapping notes is rejected.
- `Option<u16>` hitsound index; strings stored as `CompactString` in the archive.

## Example

Not shown as bytes (binary, generated by the Rust codec). Equivalent logical content for the unit test of the codec (`rox_native/decoder.rs` tests: `RoxChart::new(4)`, one `TimingPoint::bpm(0, 180.0)`, `Note::tap(1_000_000, 0)`, `Note::hold(2_000_000, 500_000, 1)`): see the JSON form in [../jrox/README.md](../jrox/README.md).

## ROX support

This is the reference implementation (`RoxNativeCodec`, extensions `["rox"]`): read + write, checked decoding, auto-detected by extension.

## Parsers & tools

- `rhythm-open-exchange` (Rust, crate `rox`): https://github.com/Glubus/rhythm-open-exchange ; vendored in this repository.
- C# bindings `RhythmOpenExchange` (NuGet 0.5.0 per README).
- rkyv: https://rkyv.org/ ; zstd: https://github.com/facebook/zstd

## Getting samples

- **Committed**: none. `.rox` is an rkyv archive inside a zstd frame; it can only be produced by the Rust codec, and building anything was not allowed for this corpus, so no file was fabricated by hand. The upstream repository `Glubus/rhythm-open-exchange` (MIT) ships no `.rox` fixture either (checked at commit `cbceffbc3bf2987170f412992cc43c5ee9b62c00`: its `assets/` folder holds `.osu`, `.qua`, `.sm`, `.fnf`/`.json`, `.bms/.bme/.pms/.bmson` sources only).
- **How to get one**: decode any supported chart and re-encode it. With the crate (`rhythm-open-exchange` 0.8.1, library name `rox`): `let chart = auto_decode(path)?; auto_encode(&chart, "output.rox")?;` (this is the repo's `examples/auto_conversion.rs`, using `assets/osu/mania_7k.osu`). The text twins [`.jrox`](../jrox/) and [`.yrox`](../yrox/) of the same model have committed samples in their folders, and hold the same data (a `.rox` is the same `RoxChart`).
- Note: the Prism repository keeps `.rox` files as test fixtures, but they come from community maps (their metadata names third-party packs), so they are not redistributable here.

## Sources

- `rhythm-open-exchange/src/formats/rox_native/{mod,encoder,decoder}.rs`, `src/model/{chart,metadata,note,timing,hitsound}.rs`, `src/codec/{traits,validate}.rs`, `src/analysis/hash.rs`, `src/error.rs`, `Cargo.toml`, `CHANGELOG.md`, `wiki.wiki/{Notes,Timing-Points,Metadata,Hitsounds,Performance-Optimizations}.md`, `README.md`
