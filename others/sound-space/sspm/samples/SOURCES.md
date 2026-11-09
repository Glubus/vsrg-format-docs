# Samples: Sound Space Plus map (.sspm)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-v1.sspm | hand-built from https://github.com/basils-garden/types/blob/4095da95def637822acef7403b8f16278226e169/sspm/v1.md | vsrg-format-docs | CC0 / public domain | synthetic SSPM v1: id/name/creator newline strings, medium difficulty, no cover, no audio, 6 notes mixing integer and quantum (float/negative) positions |
| synthetic-v2.sspm | hand-built from .../sspm/v2.md (hash layout checked against pysspm-rhythia writer) | vsrg-format-docs | CC0 / public domain | synthetic SSPM v2: no audio/cover, custom data (string, int8, array of uint32), one `ssp_note` marker definition, SHA-1 of definition+marker blocks, 6 notes int + quantum |

Both files were read back by an independent reader written from the spec (pointers, hash and all fields consistent). They hold no audio, so they are not playable in-game as is. `CC0` in the v2 mapper list and the custom field names are arbitrary test values.
