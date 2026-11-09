# Samples: Rock Band `songs.dta`

## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| synthetic-songs.dta | Synthetic: written by script for this repository, built strictly from the fiche `rock-band/dta/README.md` (its keys and layout) | GuitarGames (ROX sample corpus) | CC0 1.0 / public domain (declared by the author of this file) | Two fictional entries (`synthetic_one`, `synthetic_two`) in the text DTA layout of the fiche: name, artist, master TRUE/FALSE, song_id, song_length, preview, game_origin, year_released, genre, vocal_gender, album_art, song(name, tracks with channel groups, pans, vols, cores, midi_file), `;` comment |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
| --- | --- | --- | --- |
| missing_song_data.dta | https://raw.githubusercontent.com/mtolly/onyx/d6c9cec8bec82bf14954f091d732b3436571c020/haskell/resources/missing_song_data.dta | Onyx repository: GPL-3.0 (haskell/LICENSE.txt). Contains metadata rows about commercial Rock Band songs, so it is not committed | 186,793 bytes of real DTA-style data (observed): quoted-symbol entries like `('21guns' ('song' ('vocal_parts' 3)) ('song_length' 327727) ('solo' ('guitar')) ('format' 10) ('game_origin' 'rb1_dlc') ...)`; partial entries (no tracks/midi_file) |
