# Troll Engine chart JSON (`<song>.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

Troll Engine (riconuts, "FNF-Troll-Engine") is a Psych-derived FNF engine for modcharting and extra note kinds. This page follows Moonchart's `FNFTroll extends FNFPsychBasic<TrollJsonFormat>`.

## Container & encoding

UTF-8 JSON, same layout as Psych ([../psych-json/README.md](../psych-json/README.md)). Moonchart detects Troll by the keys `tracks`, `hudSkin` or `keyCount`.

## Structure / metadata

`TrollJsonFormat = PsychJsonFormat & { hudSkin?: string, info?: string[], metadata?: { songName?, artist?, charter?, modcharter?, extraInfo?: string[] }, offset?: float, tracks?: { inst: string[], player?: string[], opponent?: string[] }, keyCount?: int, extraTracks?: string[] (deprecated) }`. `keyCount` is keys per side (Moonchart sets `max(lanes, 8) / 2`).

## Timing model

As Psych; `offset` is a chart offset (ms).

## Notes

As Psych. Note types `Mine` and `Roll` (`FNFTrollNoteType`) map to Moonchart's mine and roll types. Lane semantics follow the engine's Psych variant (not established).

## Audio & images

`tracks.inst`, `tracks.player`, `tracks.opponent` list audio file names (e.g. `Inst`, `Voices-bf`).

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

None.

## ROX support

Not read as Troll; mines and rolls decode as taps through the legacy codec (`song.notes[].sectionNotes`).

## Observed in real files

`keyCount` (4), `hudSkin`, `tracks`, `extraTracks: []`, `splashSkin`, `arrowSkin`, `path`; some charts add `metadata` (`songName`, `artist`, `charter`) and `offset`. Note arrays have a 4th element `''` for untyped notes [observed: troll_bopeebo.json, troll_darnell.json].

## Parsers & tools

- Moonchart `FNFTroll`: https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFTroll.hx
- Troll Engine: https://github.com/riconuts/FNF-Troll-Engine

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: the repository's `default_content/base-game/songs/...` and `example_content/...` folders (no LICENSE file); the engine's chart editor.

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/legacy/FNFTroll.hx
