# Arcaea songlist / packlist (`songlist`)
Kind: metadata

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview

`songlist` (no extension) is the JSON file in which Arcaea reads the metadata of its songs (and `packlist` the metadata of packs); community tools (ArcaeaChartRender, EtoileResurrection, arcfutil, the VS Code extension) read and write it. The JSON schemas of the VS Code extension (`songlist.json`, `songdata.json`, `packlist.json`, `packdata.json`, `unlockdata.json`, `unlocks.json`) are the best available description; only the outer schema of `songlist` was read: an object with a required `songs` array whose items follow `songdata.json`.

## Container & encoding

JSON file named `songlist` (and `packlist`) at the root of the songs directory.

## Structure / metadata

`{ "songs": [ <songdata>, ... ] }`. The `songdata` fields were not read here (see the schema file `json-schema/songdata.json` in the VS Code extension repository).

## Timing model

Not applicable.

## Notes

Not applicable.

## Audio & images

Song folders hold `base.ogg`, `base.jpg` and per-difficulty `.aff` (see `../aff/`).

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

<https://github.com/yojohanshinwataikei/vscode-arcaea-file-format> (JSON schemas), <https://github.com/Arcaea-Infinity/ArcaeaChartRender> (`fetch_song_info` from songlist).

## Getting samples

- **Committed**: 6 real `songlistadd.json` fragments from the Suhri archive in [`samples/`](samples/). Origin, author, date, sha256 and licence/terms of each file are in [`samples/SOURCES.md`](samples/SOURCES.md).
- **More samples**: `songlist` is part of the game's assets (not collected); fan song packs ship a `songlistadd.json` entry. JSON schemas: https://github.com/yojohanshinwataikei/vscode-arcaea-file-format (`json-schema/songlist.json`).

## Sources

- <https://raw.githubusercontent.com/yojohanshinwataikei/vscode-arcaea-file-format/master/json-schema/songlist.json>
- <https://github.com/Arcaea-Infinity/ArcaeaChartRender>
