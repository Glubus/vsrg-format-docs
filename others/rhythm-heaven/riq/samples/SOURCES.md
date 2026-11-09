# Samples: RIQ (`.riq`, Rhythm Heaven Studio remix)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-no-audio.riq` | BUILT HERE from the serialisation code of RHeavenStudio/Jukebox (`RiqBeatmapConverter.cs`, `RiqEntityConverter.cs`, `RiqMetadataConverter.cs`, `RiqFileHandler.cs`, commit 565eba7037208033bc30ef9c96a544df2d119343) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` zip with two entries (dated 2024-01-01): `.meta` (`version` 201, `origin`, `data`) and `Charts/chart0.json` (`version` 201, `offset`, `songname` `song0`, 4 entities with `type`/`version`/`model`/`data`, `models` and `types` index tables). No `Music/song0.*` is included (Jukebox only warns "Chart has no music"); the datamodel names (`demo/intro`, ...) are placeholders, not Rhythm Heaven Studio games |

Notes: the JSON key names (`version`, `offset`, `songname`, `entities`, `models`, `types`, per entity `type`/`version`/`model`/`data`; metadata `version`/`origin`/`data`) are read from the Jukebox converters (MIT). The file was not opened in Heaven Studio. Real remixes exist (for instance on https://kitsting.com/misc/remixes/, a live personal site, not hashable and containing music) but were not downloaded.
