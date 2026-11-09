# RIQ (`.riq`, Rhythm Heaven Studio remix)
Kind: package

Doc status: stub (container known, entity schema partial) · ROX: no · Category: others · Encoding: archive (zip) containing JSON + audio

## Overview

`.riq` is the project/chart container of **Rhythm Heaven Studio** (RHeavenStudio): a zip archive with metadata, one or more **charts** (lists of timed *entities* = minigame events), and the song audio. The format is implemented by the open-source **Jukebox** library ("Parser and Serializer for the RIQ rhythm game chart format", Unity package). The current structure version is **201** (older "V1" RIQs held `remix.json` + `song.bin`). It is not an official Nintendo format.

## Contents

- `.meta`: JSON metadata (`RiqMetadata`: `version`, `origin`, hashed key/value entries).
- `Charts/chart<index>.json`: `RiqBeatmap` JSON, one or more charts indexed from 0 (`RiqFileHandler` opens `chart{index}.json`). The chart format is described in this page.
- `Music/song<index>.<ext>`: audio for chart `index`.
- `Resources/`: extra assets referenced by the remix.

## Container & encoding

- A normal **zip** (written with `ZipFile.CreateFromDirectory`, optimal compression) with extension `.riq`. Extracted layout (Jukebox cache tree `Current/`):
  - `.meta` — JSON metadata file (`RiqMetadata`: `version`, `origin` (name of the authoring program) + hashed key/value entries).
  - `Charts/chart<index>.json` — JSON `RiqBeatmap` (several charts allowed, indexed from 0).
  - `Music/song<index>.<ext>` — audio for chart `index` (extension kept from the imported file).
  - `Resources/` — extra assets (textures, audio clips, asset bundles) referenced by the remix.
- V1 layout: `remix.json` + `song.bin` at the archive root (Jukebox's `UpgradeOldStructure` converts it; needs the `JUKEBOX_V1` define).

## Structure / metadata

A `RiqBeatmap` holds: `Version` (201), `Offset` (seconds), `SongName`, and `Entities`. Each `RiqEntity` has a **datamodel** (string such as `"gameName/eventName"`), a `Type` (default `"riq__Entity"`), a `Version`, and a dictionary of dynamic properties (`beat` (double), `length` (float), plus event-specific parameters). On disk (Jukebox converters `RiqBeatmapConverter`, `RiqEntityConverter`, `RiqMetadataConverter`, read): the chart is `{"version": 201, "offset": <seconds>, "songname": "song0", "entities": [{"type": <index into types>, "version": <int>, "model": <index into models>, "data": {<property>: <value>, ...}}], "models": {"0": "<datamodel>", ...}, "types": {"0": "<type>", ...}}`; a chart without `songname` is read as `song0` (and version 2 as 201); `.meta` is `{"version": 201, "origin": "<authoring program>", "data": {<key>: <value>, ...}}` (version 2 is read as 201). Property keys are plain strings on disk; the hashing is internal to the library.

## Timing model

Beat-based: `beat` and `length` are in beats; the song audio is aligned by the beatmap `Offset` (seconds). Tempo/volume/scroll changes are themselves entities (not verified).

## Notes

There are no notes in the VSRG sense: each entity is a cue/event for a minigame (e.g. a bop, a hit prompt, a tempo change). Interpretation depends on the game datamodel registry of Rhythm Heaven Studio.

## Audio & images

`Music/song<N>.<ext>` plus `Resources/` for custom assets.

## Versions & variants

V1 (`remix.json`, `song.bin`) → V2 (`.meta`, `Charts/`, `Music/`, `Resources/`, structure version 201).

## Quirks & pitfalls

Property keys are hashed in memory (dictionary of int hash -> value with the key list kept for round-trip) but stored as strings; per-entity GUIDs are random; a cache directory must be locked while a RIQ is open. Source discrepancy: `Assets/Scripts/Jukebox/_v2FileStructure.txt` lists the audio folder as `Audio/`, while `RiqFileHandler.cs` reads `Music/`.

## Example

Hand-written from the Jukebox converters (no real remix was opened): [samples/synthetic-no-audio.riq](samples/synthetic-no-audio.riq), whose `Charts/chart0.json` is `{"version":201,"offset":0.0,"songname":"song0","entities":[{"type":0,"version":0,"model":0,"data":{"beat":0.0,"length":4.0}},{"type":0,"version":0,"model":1,"data":{"beat":4.0,"length":1.0,"type":0}}, ...],"models":{"0":"demo/intro","1":"demo/hit","2":"demo/bop"},"types":{"0":"riq__Entity"}}` and whose `.meta` is `{"version":201,"origin":"synthetic (hand-written)","data":{"title":"Synthetic RIQ","author":"vsrg-format-docs"}}` (the datamodel names are placeholders).

## ROX support

Not read by ROX 0.8.1; RIQ is an event timeline, not a lane chart.

## Parsers & tools

[RHeavenStudio/Jukebox](https://github.com/RHeavenStudio/Jukebox) (C#, Unity), Rhythm Heaven Studio editor.

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): `synthetic-no-audio.riq`, a zip with `.meta` and `Charts/chart0.json` built from the Jukebox serialisation code (MIT), CC0; no audio.
- Manifest: nothing: real remixes contain their music, and the places that host them are live personal sites or Discord (e.g. https://kitsting.com/misc/remixes/, listed in search results; not hashable).
- More: the Heaven Studio editor (https://rheavenstudio.itch.io/heaven-studio) saves `.riq`; its Discord "level-showcase" forum and video descriptions link remix files (search results); Jukebox has code to extract and pack `.riq`.

## Sources

- <https://github.com/RHeavenStudio/Jukebox> (README; `Assets/Scripts/Jukebox/RiqFileHandler.cs`, `RiqBeatmap.cs`, `RiqEntity.cs`, `RiqMetadata.cs` read)
