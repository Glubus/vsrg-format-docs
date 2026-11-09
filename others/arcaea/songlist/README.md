# Arcaea songlist / packlist (`songlist`)
Kind: metadata

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
`songlist` (no extension) is the JSON file Arcaea reads song metadata from (`packlist` for packs). Best description: the VS Code extension's JSON schemas (`songlist.json`, `songdata.json`, `packlist.json`, `packdata.json`, `unlockdata.json`, `unlocks.json`). Only the outer schema of `songlist` was read: an object with a required `songs` array of `songdata.json` items.

## Container & encoding

JSON file named `songlist` (and `packlist`) at the root of the songs directory.

## Structure / metadata

`{ "songs": [ <songdata>, ... ] }`. The `songdata` fields were not read (see `json-schema/songdata.json` in the VS Code extension repository).

## Timing model

Unknown.

## Notes

Unknown.

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
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). `songlist` is game data (not collected); fan song packs ship a `songlistadd.json` entry. Schema: https://github.com/yojohanshinwataikei/vscode-arcaea-file-format (`json-schema/songlist.json`).

## Sources

- <https://raw.githubusercontent.com/yojohanshinwataikei/vscode-arcaea-file-format/master/json-schema/songlist.json>
- <https://github.com/Arcaea-Infinity/ArcaeaChartRender>
