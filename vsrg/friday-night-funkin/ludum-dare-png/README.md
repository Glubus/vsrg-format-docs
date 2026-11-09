# FNF Ludum Dare chart (one PNG per section + `<song>.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: mixed (PNG bitmaps + JSON)

## Overview

Earliest FNF data layout (the game-jam build; Moonchart: "FNF (Ludum Dare)", tag `1.0.0` of FunkinCrew/Funkin, "This was a mistake."). Each section of a song is a small PNG whose pixels mark notes. Source: Moonchart's `FNFLudumDare.hx`, `BitmapFile.hx`; the original game files were not read.

## Container & encoding

A folder: `<song>.json` plus `<song>_section<N>.png` for N = 1..`sections` (`formatSection`: `song.toLowerCase() + "_section" + (index + 1) + ".png"`). One difficulty ("supportsDiffs: false"), no events.

## Structure / metadata

`<song>.json`: `{ "song": <string>, "bpm": <int>, "sections": <int> }` (`FNFLudumDareMeta`).

Each PNG is 8 pixels wide and `height` = number of steps in the section (16 in Moonchart's writer, 12 in the real `bopeebo` files of tag 1.0.0 [observed by decoding the manifest PNGs]; sections with more rows are 8 beats long). Pixel value 1 ("tile 1" after the engine's CSV conversion) is black (`0xFF000000`) on white (`0xFFFFFFFF`) in Moonchart's writer.

## Timing model

One BPM from the JSON. Row `y` is step `y`; `stepCrochet = 60000 / bpm / 4`. Moonchart reads each section list twice (opponent, then player) with `time = step * stepCrochet + crochet * 8 * totalLength + crochet * sectionBeats * i`, `i = 0` opponent, `1` player. Images alternate "dad, boyfriend"; each pair spans 8 beats (4 + 4). Rows are 16 steps = 4 beats; sections of 5-8 beats count as 8 beats [as implemented in Moonchart's `getNotes`; not verified].

## Notes

Columns 0-3 of the 8-pixel row are tap notes of the four lanes (decoded `column + 1`); columns 4-7 mean "sustain of lane (column - 3)" (decoded as negative numbers). Moonchart's lane mapping (`1 -> 2, 2 -> 3, 3 -> 1, other -> 0`) reorders the stored lanes to left/down/up/right. At most one note per row (`dopeArray.push` once per row); a negative value after a note extends it by one step.

## Audio & images

Not in the chart.

## Versions & variants

Single historical variant; later builds use the legacy JSON ([../legacy-json/README.md](../legacy-json/README.md)).

## Quirks & pitfalls

Needs a PNG decoder. One note per row, so no chords. Holds are multiples of a step. The dad/bf section interleave must be reproduced.

## Example

See [samples/SOURCES.md](samples/SOURCES.md) (tag 1.0.0) and the synthetic PNGs in [samples/](samples/). Real PNGs: 8-bit RGB, white background, black (0,0,0) note pixels, holds in columns 4-7.

## ROX support

Not read.

## Parsers & tools

- Moonchart `FNFLudumDare` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/FNFLudumDare.hx
- FNF repository tag `1.0.0` (cited by Moonchart): https://github.com/FunkinCrew/Funkin/tree/1.0.0 [not opened]

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). Source: https://github.com/FunkinCrew/Funkin/tree/1.0.0/assets/data (`assets/data/<song>/`, no licence file; chart bitmaps without artwork). Observed in `bopeebo` and `fresh`: PNGs are 8 pixels wide and 12 rows high (not 16), at most one black pixel per row, columns 0-3 notes, 4-7 hold continuations (note column + 4); `bopeebo.json` is `{"song": "Bopeebo", "bpm": 100, "sections": 15}`, 4-space indentation, no trailing newline [observed by decoding the PNGs].

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/FNFLudumDare.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/parsers/_internal/BitmapFile.hx
