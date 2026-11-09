# Troll Engine chart JSON (`<song>.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

Troll Engine (riconuts, "FNF-Troll-Engine") is a Psych-derived FNF engine aimed at modcharting and extra note kinds. Everything known here comes from Moonchart's implementation (`FNFTroll extends FNFPsychBasic<TrollJsonFormat>`); the engine's own source was not read.

## Container & encoding

JSON, UTF-8, same file layout as Psych ([../psych-json/README.md](../psych-json/README.md)); Moonchart marks a Troll file by the presence of the keys `tracks`, `hudSkin` or `keyCount`.

## Structure / metadata

`TrollJsonFormat = PsychJsonFormat & { hudSkin?: string, info?: string[], metadata?: { songName?, artist?, charter?, modcharter?, extraInfo?: string[] }, offset?: float, tracks?: { inst: string[], player?: string[], opponent?: string[] }, keyCount?: int, extraTracks?: string[] (deprecated) }`. `keyCount` gives the number of keys per side (Moonchart sets it to `max(lanes, 8) / 2`).

## Timing model

As Psych: absolute ms, section BPM changes; `offset` is a chart offset (ms).

## Notes

As Psych; note types `Mine` and `Roll` exist (`FNFTrollNoteType`), mapped by Moonchart to its mine and roll types. Lane semantics follow the Psych variant used by the engine (not established here).

## Audio & images

`tracks.inst`, `tracks.player`, `tracks.opponent` list audio file names (e.g. `Inst`, `Voices-bf`).

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

None (no real Troll Engine file inspected).

## ROX support

Not read as Troll (legacy codec reads `song.notes[].sectionNotes` only; mines/rolls are note types and would decode as taps).

## Parsers & tools

- Moonchart `FNFTroll`: https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFTroll.hx
- Troll Engine: https://github.com/riconuts/FNF-Troll-Engine

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/legacy/FNFTroll.hx
