# RIQ (`.riq`, Rhythm Heaven Studio remix)
Kind: package

Doc status: stub (container known, entity schema partial) · ROX: no · Category: others · Encoding: archive (zip) containing JSON + audio

## Overview

`.riq` is the project/chart container of **Rhythm Heaven Studio** (RHeavenStudio): a zip archive with metadata, one or more **charts** (lists of timed *entities* = minigame events), and the song audio. The format is implemented by the open-source **Jukebox** library ("Parser and Serializer for the RIQ rhythm game chart format", Unity package). The current structure version is **201** (older "V1" RIQs held `remix.json` + `song.bin`). It is not an official Nintendo format.

## Contents

- `.meta`: JSON metadata (`RiqMetadata`: `version`, `origin`, hashed key/value entries).
- `Charts/<name>.json`: `RiqBeatmap` JSON, one or more charts indexed from 0. The chart format is described in this page.
- `Music/song<index>.<ext>`: audio for chart `index`.
- `Resources/`: extra assets referenced by the remix.

## Container & encoding

- A normal **zip** (written with `ZipFile.CreateFromDirectory`, optimal compression) with extension `.riq`. Extracted layout (Jukebox cache tree `Current/`):
  - `.meta` — JSON metadata file (`RiqMetadata`: `version`, `origin` (name of the authoring program) + hashed key/value entries).
  - `Charts/<name>.json` — JSON `RiqBeatmap` (several charts allowed, indexed from 0).
  - `Music/song<index>.<ext>` — audio for chart `index` (extension kept from the imported file).
  - `Resources/` — extra assets (textures, audio clips, asset bundles) referenced by the remix.
- V1 layout: `remix.json` + `song.bin` at the archive root (Jukebox's `UpgradeOldStructure` converts it; needs the `JUKEBOX_V1` define).

## Structure / metadata

A `RiqBeatmap` holds: `Version` (201), `Offset` (seconds), `SongName`, and `Entities`. Each `RiqEntity` has: a **datamodel** (hashed string key, e.g. `"gameName/eventName"`), a `Type` (default `"riq__Entity"`), `Version`, a `Guid`, and a dictionary of **dynamic properties** keyed by hashed names (`beat` (double), `length` (float), plus event-specific parameters). The JSON on disk is produced by custom converters (`RiqBeatmapConverter`, `RiqEntityConverter`, `RiqMetadataConverter`); the exact JSON key names are not documented in the sources opened.

## Timing model

Beat-based: `beat` and `length` are in beats; the song audio is aligned by the beatmap `Offset` (seconds). Tempo/volume/scroll changes are themselves entities (not verified).

## Notes

There are no notes in the VSRG sense: each entity is a cue/event for a minigame (e.g. a bop, a hit prompt, a tempo change). Interpretation depends on the game datamodel registry of Rhythm Heaven Studio.

## Audio & images

`Music/song<N>.<ext>` plus `Resources/` for custom assets.

## Versions & variants

V1 (`remix.json`, `song.bin`) → V2 (`.meta`, `Charts/`, `Music/`, `Resources/`, structure version 201).

## Quirks & pitfalls

Unknown beyond: property keys are hashed (stored as dictionary of int hash → value with the key list kept for round-trip); GUIDs are random per entity; a cache directory must be locked while a RIQ is open.

## Example

Not applicable (no sample opened).

## ROX support

Not read by ROX 0.8.1; RIQ is an event timeline, not a lane chart.

## Parsers & tools

[RHeavenStudio/Jukebox](https://github.com/RHeavenStudio/Jukebox) (C#, Unity), Rhythm Heaven Studio editor.

## Sources

- <https://github.com/RHeavenStudio/Jukebox> (README; `Assets/Scripts/Jukebox/RiqFileHandler.cs`, `RiqBeatmap.cs`, `RiqEntity.cs`, `RiqMetadata.cs` read)
