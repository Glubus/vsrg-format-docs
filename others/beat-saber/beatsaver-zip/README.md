# Beat Saber custom level package (BeatSaver `.zip`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive

## Overview
Custom Beat Saber levels are shared as a ZIP archive containing a map folder: `Info.dat`, the difficulty `.dat` files, the audio file, the cover image and optional extras. BeatSaver (https://beatsaver.com/) is the main distribution site; uploaded maps are validated against the schemas described in the [info](../info-dat/README.md) and [dat](../dat/README.md) docs (BSMG: "these schemas are also enforced when uploading your map to BeatSaver"). Installed maps live in a folder per level inside the game's `Beat Saber_Data/CustomLevels` (PC) [inference from the song-loader plugin docs: custom songs are folders containing `info.json`]. The archive has no wrapper format of its own.

## Contents

- A map folder in a ZIP: `Info.dat`, one difficulty `.dat` per difficulty, audio, cover and optional extras.
- Chart format inside: [`.dat`](../dat/README.md); metadata: [`Info.dat`](../info-dat/README.md).

## Container & encoding
Standard ZIP. Contents: files referenced by Info with names relative to `Info.dat`'s directory (BSMG: "All filename references are assumed to be located in the same relative directory as the info file"). The Info file must be named `Info.dat`. Recommended audio `ogg`; cover png/jpg, square, >= 256 px for BeatSaver (BSMG). No top-level mandatory folder structure documented in the sources read; Unknown beyond that.

## Structure / metadata
Unknown / not applicable beyond the files listed. BeatSaver stores its own metadata (id, hash, stats) in its API, not in the package.

## Timing model / Notes
Not applicable (see dat doc).

## Audio & images
Audio file and cover image referenced from Info.dat.

## Versions & variants
Follows the Info/beatmap schema versions (v1 legacy `info.json` packages in the early era, v2, v4). Quest/PC use the same package.

## Quirks & pitfalls
- Info.dat name case.
- Mod-only characteristics may be present and be dropped by vanilla.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
- BeatSaber-Deno: https://github.com/KivalEvan/BeatSaber-Deno
- ChroMapper exports/imports BeatSaver zips: https://github.com/Caeden117/ChroMapper [inference]
- Song loader plugin (legacy, folder layout `info.json`): https://github.com/xyonico/BeatSaberSongLoader

## Sources
- https://bsmg.wiki/mapping/map-format.html
- https://bsmg.wiki/mapping/map-format/info.html
- https://github.com/xyonico/BeatSaberSongLoader
