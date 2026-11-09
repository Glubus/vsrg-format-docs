# FPS Plus chart JSON (`<song>.json` + `meta.json` + `events.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

FPS Plus (ThatRozebudDude, "FNF: FPS Plus") is a FNF engine/mod that keeps the legacy chart JSON and adds sidecar files. Everything known here comes from Moonchart's implementation (`FNFFpsPlus`), not from the FPS Plus source, which was not read.

## Container & encoding

JSON, UTF-8. Per song: the legacy chart file (see [../legacy-json/README.md](../legacy-json/README.md)), a `meta` file (`formatFile` adds `meta` and `events` to the legacy file-name candidates) and an `events` file.

## Structure / metadata

- Chart: the legacy `{song: {...}}` object plus two fields: `stage` (string) and `gf` (string; character) (typedef `FpsPlusJsonFormat = FNFLegacyFormat & { stage, gf }`).
- `meta.json` (`FpsPlusMetaJson`): `name`, `artist`, `album` (strings), `difficulties` (array of ints: ratings per difficulty, sorted easy, normal, hard, erect, nightmare), `compatableInsts` (array or null), `mixName`, `bfBeats` and `dadBeats` (arrays of ints: beats on which the characters bop), `pauseMusic`.
- `events.json` (`FpsPlusEventsJson`): `{ "events": { "events": [ event, ... ] } }`, each event an array `[section, time, ?, name, ...]` (accessors: index 0 = section number, 1 = time, 3 = name; index 2 and the value slots are not described in the sources read).
- Note types: `alt`, `censor`, `hey` (`FNFFpsPlusNoteType`) mapped to alt animation / censor / cheer.

## Timing model

As legacy: absolute ms notes, section BPM changes.

## Notes

As legacy (`[time, lane, sustain]` plus note type extras), lanes combined with `mustHitSection`.

## Audio & images

Not specified here.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown beyond the legacy ones; `findMeta` in Moonchart picks the meta file as the JSON that contains the word `name`.

## Example

None (no real FPS Plus file inspected).

## ROX support

Not read as FPS Plus; the chart file alone decodes with the legacy rule (`song.notes[].sectionNotes`).

## Parsers & tools

- Moonchart `FNFFpsPlus` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFFpsPlus.hx
- FPS Plus: https://github.com/ThatRozebudDude/FPS-Plus-Public

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/legacy/FNFFpsPlus.hx
