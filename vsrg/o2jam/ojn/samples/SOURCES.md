# Samples: O2Jam note file (`.ojn`)

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `o2ma2420.ojn`, `o2ma2626.ojn`, `o2ma2906.ojn`, `o2ma2968.ojn`, `o2ma3308.ojn`, `o2ma3383.ojn`, `o2ma3772.ojn`, `o2ma3904.ojn`, `o2ma3933.ojn`, `o2ma4069.ojn` | from upstream repository, origin and licence unknown (`README.md` in this folder: "randomly chosen from the _Server Two Music Pack Unofficial Songs OJM 2001-6000+_") | Unknown | Unknown | Real community OJN files (full 300-byte header, three difficulty sections, embedded cover JPEG/BMP); kept as they were. `o2ma2906.ojn` has CP949 artist/noter strings (see the fiche). |
| `README.md` | upstream repository | Unknown | Unknown | Provenance note quoted above (not a chart). |
| `exact-five-way.seed` (328 B), `measure-fraction.seed` (324 B), `bpm-channel-order.seed` (348 B), `count-mismatch.seed` (312 B), `truncated-header.seed` (5 B) | https://github.com/djzmo/render-ojn/tree/d2c3c81910b6e37e6190caec39a52241cae366ed/fuzz/corpus/ojn (`fuzz/corpus/ojn/`) | djzmo (render-ojn) | GPL-3.0 (render-ojn `LICENSE`); the corpus README states "Add only redistributable malformed or synthetic OJN inputs here" | Synthetic, minimal OJN files (`songid` 42, signature `ojn\0`, `encode_version` 0.0, genre 2 (Dance), BPM 120, only the third (hard) section holds 1-2 events, `cover_offset` = end of file, i.e. **no cover**). Per the corpus README: `exact-five-way` = non-divisible five-way note subdivision; `measure-fraction` = channel-0 (measure fraction) normalisation; `bpm-channel-order` = channel-order backtracking around a BPM change; `count-mismatch` = declared event count differs from the section's real content; `truncated-header` = header shorter than 300 bytes (invalid on purpose). |
| `new-wrapper.seed` (320 B), `new-wrapper-block4.seed` (320 B), `new-wrapper-zero-block.seed` (40 B), `new-wrapper-truncated.seed` (6 B), `new-wrapper-wrong-key.seed` (320 B) | same | djzmo | GPL-3.0 | The **encrypted "new" OJN wrapper** (starts with ASCII `new`, then block size, primary/middle/initial keys; payload read in reverse and XORed, see the fiche "Versions & variants"): a valid wrapper with block size 11, one with block size 4 and different keys, a zero block size (divide-by-zero trap), a file shorter than the 8-byte key header, and a well-formed container whose payload does not decrypt to an OJN. First bytes of `new-wrapper.seed`: `6e 65 77 0b 46 e1 85 00 ...` (`new`, block size 0x0B). |

The corpus names end in `.seed` (fuzzer seeds) although the bytes are OJN data; copy them to `.ojn` to feed a parser that dispatches by extension.

Real encrypted retail OJN files are not provided (Getting samples).
