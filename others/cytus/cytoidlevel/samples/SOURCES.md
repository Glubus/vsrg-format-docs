# Samples: Cytoid level package (`.cytoidlevel`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `chovvy.test.noaudio.cytoidlevel` | BUILT here from https://github.com/CatalinTermure/Cytoid-Chart-Editor/blob/fc36b7a0acce5062ab50cc4f1742d91c4f72446d/Assets/Editor/Resources/chovvy.test/level.json and https://github.com/CatalinTermure/Cytoid-Chart-Editor/blob/fc36b7a0acce5062ab50cc4f1742d91c4f72446d/Assets/Editor/Resources/chovvy.test/chart-extreme.json (flat zip with the two files; music, preview and background are NOT included) | chovvy (files); package assembled by OthersA | GPL-3.0 (repo LICENSE); chart written by the repo author "chovvy" | level package layout: flat zip with `level.json` (schema_version 2, id, title, artist + artist_source, charter, illustrator, storyboarder, music/music_preview/background paths, `charts[]` with type extreme, difficulty 0, name, path) and one C2 chart; the referenced media files are absent |
| `cytoid-chart-editor_chovvy.test_level.json` | https://github.com/CatalinTermure/Cytoid-Chart-Editor/blob/fc36b7a0acce5062ab50cc4f1742d91c4f72446d/Assets/Editor/Resources/chovvy.test/level.json | chovvy | GPL-3.0 (repo LICENSE); chart written by the repo author "chovvy" | loose `level.json` as stored in the editor test level (2-space JSON, keys sorted alphabetically) |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `cytoid_io.cytoid.8bit_adventurer.cytoidlevel` | https://raw.githubusercontent.com/Cytoid/Cytoid/bd4eb6eea8accf7c832e4c9a957eafe27f1ef4cf/engines/unity/Assets/StreamingAssets/Levels/io.cytoid.8bit_adventurer.cytoidlevel | GPL-3.0 repo, but README limits it to source code (graphical assets excluded) and the level embeds mp3 + images by third parties; not committed | 9.7 MB Cytoid level zip bundled with the game: level.json (schema_version 2) + 3 charts ez.txt/hd.txt/ex.txt that actually contain C2-style JSON (format_version 0, start_offset_time) + storyboard JSON + music + images (9691323 bytes) |
