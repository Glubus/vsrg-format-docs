# Samples: O2Jam sample bank (`.ojm`)

Synthetic containers only (84-168 bytes), no real audio: M30 samples hold a 5-byte payload starting `OggS` then counting bytes, named `sample`; OJM ones hold filler bytes.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `m30-flag-0.seed`, `m30-flag-16.seed`, `m30-flag-32.seed` (96 B each) | https://github.com/djzmo/render-ojn/tree/d2c3c81910b6e37e6190caec39a52241cae366ed/fuzz/corpus/ojm (`fuzz/corpus/ojm/`) | djzmo (render-ojn) | GPL-3.0 | **M30** containers (`M30\0` signature) with encryption flag 0 (plaintext Ogg payload), 16 (`nami` XOR-obfuscated payload) and 32 (plaintext payload). |
| `m30-nami-partial-tail.seed` (90 B) | same | djzmo | GPL-3.0 | M30 `nami` payload with a trailing partial 0-3 byte group left untouched. |
| `m30-codec-0.seed` (96 B) | same | djzmo | GPL-3.0 | M30 sample with codec code 0 (accepted into the background bank per the corpus README). |
| `m30-codec-invalid.seed`, `m30-flag-unsupported.seed`, `m30-not-ogg.seed` (96 B each), `unsupported-m30-codec.m30` (84 B) | same | djzmo | GPL-3.0 | Malformed M30 on purpose: codec code 1, flag 8, decoded payload without `OggS`, unsupported codec in a `.m30` file. |
| `sparse-pcm-slot.ojm` (149 B) | same | djzmo | GPL-3.0 | **`OJM\0`** variant (`4f 4a 4d 00`) whose PCM directory has a zero-length slot (names `pcm0`, `pcm1`): the slot is skipped, positional ids. |
| `trailing-empty-ogg.ojm` (168 B) | same | djzmo | GPL-3.0 | `OJM\0` container with an OGG directory (entry `ogg0` with a 4-byte `OggS` payload, then entries `trailing0`..`trailing2` with zero-byte payloads). |

No `OMC\0` example.
