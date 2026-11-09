# DDR STEP data (1st-3rd Mix era, "DDR Utility" export)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: binary (little-endian)

## Overview

"STEP" is a name coined by SaxxonPike's `rhythm-game-formats` for "the format exported using DDR Utility", found in DDR 2nd Mix through 3rd Mix Plus, including Solo Bass Mix and Solo 2000 ("a slight variation in step panel configuration"). It precedes the chunked [SSQ](../ssq/README.md) (4th Mix on) and relates to [STEP2](../step2/README.md) (1st Mix only). The upstream page is a stub ("In a nutshell: TODO"); the layout below is the one RhythmCodex reads (`Charts.Step1`, MIT), checked on the three committed samples.

## Container & encoding

Chunks `{i32 length, length - 4 bytes}`, little-endian, back to back; a length below 4 ends the file (the samples end with a 0). The first chunk is the tempo, every other one a chart. RhythmCodex's heuristic: the file is a multiple of 4 bytes and at most 64 KiB, every chunk length is a positive multiple of 4 inside the file, the tempo chunk is at least 20 bytes and its ticks and times never go back.

## Structure / metadata

- Tempo chunk: pairs `{i32 measure tick, i32 time}`.
- Chart chunk: an `i32` code, then rows `{i32 tick, i32 panels}`; a row of `0` or `-1` is empty. Code low byte: `0` single (or a Solo chart), `1` couple, `2` double; next byte: `0`, `1`, `2` (RhythmCodex: Easy, Medium, Hard; the mixes call them Basic, Another, Maniac). The samples hold 3 x 3 charts (2nd Mix, Solo) or 3 x 2 (`picky`: single and double).
- No title, no audio name: the file holds steps and tempo only.

## Timing model

4096 ticks per measure (as SSQ); times are in 1/75 s. A tick's time is the linear interpolation between the tempo entries around it (two entries with the same tick are a stop), as for the SSQ tempo chunk. Observed: `2nd` has 2 entries (one tempo), `solo` 14.

## Notes

`panels` holds one nibble per panel: nibble `k` not 0 means panel bit `k` (8 bits: the low four player 1, the high four player 2: left, down, up, right). A single chart is written twice, once per player (both nibbles equal). Solo charts use bits 4 and 6 for up-left and up-right: 6 panels `L UL D U UR R` = bits `0 4 1 2 6 3`; the Solo mixes also have 3-panel charts (`UL D UR` = bits `4 1 6`). No freezes, no mines.

## Audio & images

None.

## Versions & variants

2nd Mix .. 3rd Mix Plus, Solo Bass Mix, Solo 2000.

## Quirks & pitfalls

- Singles are stored as a two-player chart with equal sides; compare the nibbles before calling a chart double or couple.
- `.step` is also the extension of pydance step files (text) and of CAD files: tell them by content.

## Example

`rhythmcodex_2nd.step` starts with the tempo chunk `14 00 00 00 | 00 00 00 00 2D 02 00 00 | 00 C0 02 00 98 18 00 00` (tick 0 at 557/75 s, tick 180224 at 6296/75 s: about 138 BPM).

## ROX support

Decode only, `rox::formats::ssq` (`StepDecoder`, `DetectedFormat::Step`; a `.step` is told by `looks_like_step`, RhythmCodex's heuristic). Each chart chunk is a variant except couples (skipped, as for `.ssq`/`.dwi`): a single chart (equal nibbles) is 4 columns, otherwise the smallest layout holding the panels used: Solo 3 (3 columns), Single (4), Solo (6), Double (8). Taps only; the tempo goes through the `.ssq` tempo map (1/75 s units).

## Parsers & tools

"DDR Utility" (original export tool); RhythmCodex and Scharfrichter have format-specific work for some of these games [inference].

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md) (RhythmCodex test fixtures, `Step1/` at commit `6c60e9b710150c6ca4adf9b7d93e51c2ad39b2ee`). Inspect them with a hex editor to fill the gaps. No other public source (searched GitHub parser repos and archive.org 2026-11-09). Otherwise use "DDR Utility" on your own 2nd Mix to 3rd Mix Plus / Solo data ([`ddr/step.md`](https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md)); RhythmCodex reads it.

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md
- https://zenius-i-vanisher.com/v5.2/thread?threadid=7564
