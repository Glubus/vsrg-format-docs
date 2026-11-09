# Samples: Rhythm Doctor level archive (`.rdzip`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rebuilt-internet-overdose-no-audio.rdzip` | BUILT HERE: a zip (deflate, entries dated 2024-01-01) containing only `main.rdlevel` = the file `../../rdlevel/samples/rd-nurse_internet_overdose.rdlevel` (from 0f-0b/rd-nurse, AGPL-3.0) | level authors credited inside the level; archive built by vsrg-format-docs (OthersC) | AGPL-3.0 (same as the level) | audio-less .rdzip: the container layout `main.rdlevel` at the zip root (name observed in two real archives, see manifest); the level refers to `music.ogg`, `preview.png`, `syringe.png` which are NOT included, so the level cannot be played from this archive |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `HyperHax_-_Corrupted.rdzip` | https://raw.githubusercontent.com/HyperHaxStudios/RD-Levels/5e6d8fc049498c4967b1e3c383e1a1f05a8b0b54/HyperHax%20-%20Corrupted.rdzip | No licence file in HyperHaxStudios/RD-Levels; level and music belong to the author | real .rdzip (zip with main.rdlevel, Album.jpg, Corrupt.ogg); not committed: audio inside, no licence |
| `HyperHax_-_Nowhere_(EDM_Remix).rdzip` | https://raw.githubusercontent.com/HyperHaxStudios/RD-Levels/5e6d8fc049498c4967b1e3c383e1a1f05a8b0b54/HyperHax%20-%20Nowhere%20(EDM%20Remix).rdzip | No licence file in HyperHaxStudios/RD-Levels; level and music belong to the author | real .rdzip (zip with main.rdlevel, Album.png and an .ogg); not committed: audio inside, no licence |

Notes: the two manifest archives were listed (`unzip -Z1`): `Album.jpg`/`Corrupt.ogg`/`main.rdlevel` and `Album.png`/`HyperHax - Nowhere (EDM Remix).ogg`/`main.rdlevel`, i.e. flat files at the zip root.
