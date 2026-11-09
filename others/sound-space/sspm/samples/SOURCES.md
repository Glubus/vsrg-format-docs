# Samples: Sound Space Plus map (.sspm)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-v1.sspm | hand-built from https://github.com/basils-garden/types/blob/4095da95def637822acef7403b8f16278226e169/sspm/v1.md | vsrg-format-docs | CC0 | synthetic SSPM v1: id/name/creator newline strings, medium difficulty, no cover, no audio |
| synthetic-v2.sspm | hand-built from .../sspm/v2.md (hash layout checked against pysspm-rhythia writer) | vsrg-format-docs | CC0 | synthetic SSPM v2: no audio/cover, custom data (string, int8, array of uint32) |

Both files were read back by an independent reader written from the spec (pointers, hash and all fields consistent). They hold no audio, so they are not playable in-game as is. `CC0` in the v2 mapper list and the custom field names are arbitrary test values.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `rhythia_4333_v1.sspm` | https://static.rhythia.com/rhythia-legacy-3c623566938eb0ec93157fdbedb50303033f327270bfbbafa959c11e62de0439.sspm | 2026-11-09 | 3c623566938eb0ec93157fdbedb50303033f327270bfbbafa959c11e62de0439 | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v1, audio and cover stripped; sha256 is of the original 877775-byte download |
| `rhythia_14778_v2.sspm` | https://static.rhythia.com/rhythia-90322-1782857055467.sspm | 2026-11-09 | eacd62194bb05986f4b4af46f7902ea2f99a4ee80cbebf7aad7885d0d7444e9c | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v2, audio and cover stripped; sha256 is of the original 6730255-byte download |
| `rhythia_11892_v2.sspm` | https://static.rhythia.com/rhythia-dfc6eaa7-6205-46f1-a17d-cb34b6fb50b4-1774615908775.sspm | 2026-11-09 | af95659dfd04c885787ea898402fb61796fc8c528dab57f6ab02efb3991fb29e | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v2, audio and cover stripped; sha256 is of the original 6387336-byte download |
| `rhythia_4288_v1.sspm` | https://static.rhythia.com/rhythia-legacy-f10635bc49b876c8ec130b9f4208de98b86dcc9f07580de938c208436a8903da.sspm | 2026-11-09 | f10635bc49b876c8ec130b9f4208de98b86dcc9f07580de938c208436a8903da | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v1, audio and cover stripped; sha256 is of the original 2468396-byte download |
| `rhythia_4915_v1.sspm` | https://static.rhythia.com/rhythia-legacy-6adc9a4938e54a86e37abff4e2bc4021effe737ef727607b44670df9d0f71418.sspm | 2026-11-09 | 6adc9a4938e54a86e37abff4e2bc4021effe737ef727607b44670df9d0f71418 | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v1, audio and cover stripped; sha256 is of the original 2446-byte download |
| `rhythia_11871_v2.sspm` | https://static.rhythia.com/rhythia-e8bd1a72-c466-4d10-b779-d0c2b214302d-1774496396692.sspm | 2026-11-09 | 1fdb130245e57556b06d95f40e854e303767056d2a41882448f5ea8da39493b6 | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v2, audio and cover stripped; sha256 is of the original 4278255-byte download |
| `rhythia_8565_v2.sspm` | https://static.rhythia.com/rhythia-73040926-c9c7-4eb2-9675-6ab49695666f-1740924430844.sspm | 2026-11-09 | b33750ed4f02c4f44ce112158a0db6e1fceb438412a7b803493405078fef236d | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v2, audio and cover stripped; sha256 is of the original 2133905-byte download |
| `rhythia_4256_v1.sspm` | https://static.rhythia.com/rhythia-legacy-7c0cd967ce329abc8b61e40f83d5370321aa26f5220c5146d53be6769cab4878.sspm | 2026-11-09 | 7c0cd967ce329abc8b61e40f83d5370321aa26f5220c5146d53be6769cab4878 | unknown (Rhythia/SS+ community mapper | community upload on Rhythia | real SSPM v1, audio and cover stripped; sha256 is of the original 4987-byte download |
