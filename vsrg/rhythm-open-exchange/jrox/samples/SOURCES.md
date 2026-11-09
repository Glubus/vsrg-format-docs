# Samples: ROX JSON (.jrox)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-4k-features.jrox` | Hand-written by BmsAux from the serde model of ROX 0.8.1 (`src/model/{chart,metadata,note,timing,hitsound}.rs`, `src/formats/jrox.rs`, MIT, owner's crate vendored in `prism/vendor/rhythm-open-exchange`) and its validation rules (`src/codec/validate.rs`). Never run through the Rust codec. | BmsAux (synthetic) | CC0 / public domain | 4K, all four note types (Tap, Hold, Burst, Mine), chords, hitsound indexes with a `volume` override, BPM change with a 3/4 signature, two SV points, fully populated metadata (ids, difficulty value, negative audio offset, tags). 20 notes. |
| `synthetic-7k-minimal.jrox` | same | BmsAux (synthetic) | CC0 / public domain | 7K, default metadata values (`Normal`, 15 s preview, empty strings, nulls), one BPM point, 7 taps. |
| `synthetic-8k-coop.jrox` | same | BmsAux (synthetic) | CC0 / public domain | `is_coop: true` with an even key count (8), two-player columns 0-3 / 4-7, holds and a mine. |

The three files describe the same charts as the `.yrox` samples (identical model data); they were checked by parsing the YAML and JSON with independent parsers (equal results) and by re-implementing the validation rules (sorted notes and timing points, BPM before the first note, columns < key_count, no overlapping notes per column, positive hold/burst durations).
