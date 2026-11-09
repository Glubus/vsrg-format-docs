# FNF Ludum Dare chart (one PNG per section + `<song>.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: mixed (PNG bitmaps + JSON)

## Overview

The earliest FNF data layout (the game-jam build, referenced by Moonchart as "FNF (Ludum Dare)", pointing to the tag `1.0.0` of FunkinCrew/Funkin; Moonchart's description: "This was a mistake."). Notes are not stored as text: each section of a song is a small PNG image whose pixels mark notes, loaded as a tilemap. Everything below is taken from Moonchart's implementation (`FNFLudumDare.hx`, `BitmapFile.hx`), a third-party reverse implementation; the original game files and source tag were not read.

## Container & encoding

A folder: `<song>.json` (metadata) plus `<song>_section<N>.png` for N = 1..`sections` (lower-cased song name; `formatSection`: `song.toLowerCase() + "_section" + (index + 1) + ".png"`). Charts have one difficulty ("supportsDiffs: false") and no events.

## Structure / metadata

`<song>.json`: `{ "song": <string>, "bpm": <int>, "sections": <int> }` (`FNFLudumDareMeta`).

Each PNG is 8 pixels wide and `height` = number of steps in the section (16 in Moonchart's writer, 12 in the real `bopeebo` files of tag 1.0.0 [observed by decoding the manifest PNGs];  sections with more rows are 8 beats long). Pixel value 1 ("tile 1" after the engine's CSV conversion) is black (`0xFF000000`) on a white (`0xFFFFFFFF`) background in Moonchart's writer.

## Timing model

BPM from the JSON (a single value, no changes). Row `y` of a section is step `y`; `stepCrochet = 60000 / bpm / 4`. Section start: the sections of the two sides alternate: Moonchart reads each section list twice (opponent then player) with `time = step * stepCrochet + crochet * 8 * totalLength + crochet * sectionBeats * i` where `i = 0` for the opponent and `1` for the player, so section images alternate "dad, boyfriend" and each pair spans 8 beats (4 + 4). Rows count as 16 steps = 4 beats; sections of 5-8 beats are treated as 8 beats. [as implemented in Moonchart's `getNotes`; not independently verified]

## Notes

Columns of the 8-pixel row: columns 0-3 are tap notes of the four lanes (decoded `column + 1`), columns 4-7 mean "sustain of lane (column - 3)" (decoded as negative numbers). The Moonchart lane mapping (`1 -> 2, 2 -> 3, 3 -> 1, other -> 0`) reorders the stored lane numbers to FNF's usual left/down/up/right. One note per row at most (`dopeArray.push` once per row); a negative value after a note extends it by one step.

## Audio & images

Not in the chart.

## Versions & variants

Single historical variant; later builds moved to the legacy JSON ([../legacy-json/README.md](../legacy-json/README.md)).

## Quirks & pitfalls

Image decoding needs a PNG decoder (no text); one note per row means chords are impossible; hold lengths are multiples of a step; the section interleave (dad/bf alternate) must be reproduced.

## Example

Real files: see [samples/SOURCES.md](samples/SOURCES.md) (tag 1.0.0) and the synthetic section PNGs in [samples/](samples/). Observed in the real PNGs: 8-bit RGB, white background, black (0,0,0) note pixels, hold pixels in columns 4-7.

## ROX support

Not read.

## Parsers & tools

- Moonchart `FNFLudumDare` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/FNFLudumDare.hx
- FNF repository tag `1.0.0` (cited by Moonchart): https://github.com/FunkinCrew/Funkin/tree/1.0.0 [not opened]

## Getting samples

- Committed ([samples/](samples/) and [samples/SOURCES.md](samples/SOURCES.md)): the real Ludum Dare build data from tag `1.0.0` of FunkinCrew/Funkin (`assets/data/<song>/`): `bopeebo.json` + 15 section PNGs and `fresh.json` + 16 PNGs (the tag has no licence file; the PNGs are 8-pixel-wide chart bitmaps without artwork), plus a synthetic 4-section set.
- Observed in those files: the PNGs are 8 pixels wide and 12 rows high (not 16), white background with black pixels, at most one black pixel per row, columns 0-3 notes and 4-7 hold continuations (hold pixel = note column + 4); `bopeebo.json` is `{"song": "Bopeebo", "bpm": 100, "sections": 15}` with 4-space indentation and no trailing newline [observed by decoding the PNGs].
- More: https://github.com/FunkinCrew/Funkin/tree/1.0.0/assets/data.

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/FNFLudumDare.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/parsers/_internal/BitmapFile.hx
