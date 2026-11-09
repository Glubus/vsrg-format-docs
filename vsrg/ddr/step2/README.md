# DDR STEP2 data (1st Mix, "DDR Utility" export)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview

"STEP2" is a SaxxonPike `rhythm-game-formats` name, like [STEP](../step/README.md): "the format exported using DDR Utility. It is featured only in 1st Mix and can quantize to 1/64." The layout below is the one RhythmCodex reads (`Charts.Step2`, MIT).

## Container & encoding

One file = one chart. An `i32` header length `H` (a multiple of 4, `(H - 4)` a multiple of 20), then `(H - 4) / 20` block descriptors of five `i32`: offset of the block from the file start, length in 4-byte words, reserved, next block of player 1, next block of player 2 (the last two as `4 + 20 x index`). The step data follows the header.

## Structure / metadata

Each player's steps are the chain of blocks from descriptor 0 following `next 1P` (or `next 2P`) until a block points at itself. Each byte of the chain is one 1/64-measure slot.

## Timing model

Slots of 1/64 measure, from the start. **There is no tempo in the file**: the BPM and the offset live in the game's own song table.

## Notes

A byte's bits are panels: `0x01` left, `0x08` down, `0x04` up, `0x02` right (RhythmCodex's mapper: bits 0, 3, 2, 1 are columns 0, 1, 2, 3). Equal chains for both players = a single chart; otherwise a double (player 2's columns after player 1's). The `couple` sample is byte-identical to `double` in size; RhythmCodex calls every non-single STEP2 a double.

## Audio & images

None.

## Versions & variants

DDR 1st Mix only.

## Quirks & pitfalls

No tempo: a reader can place the notes on a grid but not in time without the game's BPM.

## Example

See the three committed RhythmCodex fixtures (`single`, `double`, `couple`).

## ROX support

Not read by ROX: the file has no tempo, so no note has a time. A reader would need the 1st Mix song table (BPM and offset per song).

## Parsers & tools

RhythmCodex (`Charts.Step2`, MIT) reads the steps; "DDR Utility" exported them.

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md) (RhythmCodex fixtures, `Step2/` at commit `6c60e9b710150c6ca4adf9b7d93e51c2ad39b2ee`; tiny, good for reverse engineering). No other public source. Get it from your own 1st Mix data via "DDR Utility" ([`ddr/step2.md`](https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step2.md)).

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step2.md
