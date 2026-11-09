# Samples: Bemuse song metadata and music server index
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `bemuse-example-music-server-index.json` | https://github.com/bemusic/bemuse at `4bf3e7d98a44841b323741cc403ecb7b41618ade`, `bemuse/src/app/test-fixtures/example-music-server/index.json` | Bemuse contributors | AGPL-3.0 (repo `LICENSE`, read) | Real `index.json` shape with 13 songs: `id`/`path`, `artist_url`/`bms_url`/`song_url`/`long_url`, per-chart `file`, `md5`, `info` (title, subtitles, subartists, difficulty, level), `noteCount`, `scratch`, `keys` (5K/7K/14K), `bpm` (init/min/median/max); Japanese text; `.bms`/`.bme`/`.bml` chart names. |
| `derived-aoi-olivia-bemuse-song.json` | Derived by BmsAux from the first song of the file above by removing `id` and `path` (a `bemuse-song.json` has the song-object shape without them) and re-serialising with 2-space indentation; no real `bemuse-song.json` could be downloaded (the Bemuse server only exposes `index.json` for the songs checked). | BmsAux, from Bemuse contributors' data | AGPL-3.0 | Single-song metadata with 4 charts. |

Live, not hashable (removed from the manifest, URL not immutable): `bemuse-ninja_music_index.json`. See the fiche's Getting samples section for the live URLs.
