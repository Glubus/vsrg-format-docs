# Samples: Rock Band `songs.dta`

## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| synthetic-songs.dta | Synthetic, scripted from [`dta/README.md`](../README.md) | GuitarGames (ROX sample corpus) | CC0 1.0 | Two fictional entries (`synthetic_one`, `synthetic_two`) with every documented key, plus a `;` comment |

## Downloaded (fetched 2026-11-09)
| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `missing_song_data.dta` | https://raw.githubusercontent.com/mtolly/onyx/d6c9cec8bec82bf14954f091d732b3436571c020/haskell/resources/missing_song_data.dta | 2026-11-09 | f27f04cc97a05d1277d46f5a47ced2ddf054f283625017b6da921f38cd56fbba | mtolly/onyx contributors | GPL-3.0 (haskell/LICENSE.txt) | quoted-symbol dialect, partial entries (`'song_length'`, `'solo'`, `'format'`, `'game_origin'`, `'extra_authoring'`, `'preview'`, `'vocal_parts'`), no tracks/midi_file; 186793 bytes, 9257 lines, ~1140 entries |
| `rock-band-3-deluxe_songs.dta` | https://raw.githubusercontent.com/hmxmilohax/rock-band-3-deluxe/HEAD/_ark/songs/songs.dta (repo HEAD was c64e3a7792a424b104b3468ee835b920c0e4385f when fetched) | 2026-11-09 | 584fe44bc79ba007c67c99058455df84c6f99569413f90457dabec3db294ad82 | Harmonix / hmxmilohax | none found | full RB3 `songs.dta`: `#ifndef`/`#define` blocks, `(rank ...)`, `(drum_solo (seqs ...))`; 173962 bytes, 6217 lines |
| `rock-band-3-deluxe_songs_dx.dta` | https://raw.githubusercontent.com/hmxmilohax/rock-band-3-deluxe/HEAD/_ark/songs/songs_dx.dta (repo HEAD was c64e3a7792a424b104b3468ee835b920c0e4385f when fetched) | 2026-11-09 | 49cbde5335d886b5d3572aa6984e92b3208138760223a16f4cd218114e1916cc | hmxmilohax | none found | `(tracks_count ...)`, `(tracks ((drum (0 1)) ...))`, `;` header (calibration song); 3144 bytes, 128 lines, ~2 entries |
| `rock-band-3-deluxe_rb1_songs.dta` | https://raw.githubusercontent.com/hmxmilohax/rock-band-3-deluxe/HEAD/_ark/songs/rb1_songs.dta (repo HEAD was c64e3a7792a424b104b3468ee835b920c0e4385f when fetched) | 2026-11-09 | 859175cfde31032caebf5e60d0b724ac6135d9fe8fd3f0fbe809e304b561e141 | Harmonix / hmxmilohax | none found | Rock Band 1 entries; 63667 bytes, 2460 lines, ~58 entries |
| `gh2-customs_songs.dta` | https://raw.githubusercontent.com/Milohax-archive/gh2-customs/HEAD/GH2CUSTOMSREPO/config/songs.dta (repo HEAD d6515c6e0c3e88ae5a0df0ce9eab090a83080691) | 2026-11-09 | 8b8658c1e6626e9c75e7a111c398ceef5caf0f15ddd92f385418bad258eff044 | Milohax-archive GH2 customs (fan authors, e.g. `$author "mariteaux"`) | none stated | GH2: `{do {set $songalbum ...}}` blocks in `(artist ...)`, `(caption performed_by)`, `(tracks ((guitar (2 3)) (bass 4)))` [observed]; 53557 bytes, 2088 lines, ~55 entries |
