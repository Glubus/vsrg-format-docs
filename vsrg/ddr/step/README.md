# DDR STEP data (1st-3rd Mix era, "DDR Utility" export)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview

"STEP" is a name coined by SaxxonPike's `rhythm-game-formats` for "the format exported using DDR Utility", found in DDR 2nd Mix through 3rd Mix Plus, including Solo Bass Mix and Solo 2000 ("a slight variation in step panel configuration"). It precedes the chunked [SSQ](../ssq/README.md) (4th Mix on) and relates to [STEP2](../step2/README.md) (1st Mix only). The upstream page is a stub ("In a nutshell: TODO").

## Container & encoding

Unknown (extension, header, endianness, quantization).

## Structure / metadata

Unknown.

## Timing model

Unknown. The ZIv "DDR Research Master Thread" describes the PRE-MAX engine's in-RAM edit mode layout (one byte per beat, a nibble per player), probably the same data family but not a file specification.

## Notes

Solo mixes use a different panel configuration (6 panels: the ZIv thread lists UL/UR bytes for solo edit data). Nothing else is known.

## Audio & images

Unknown.

## Versions & variants

2nd Mix .. 3rd Mix Plus, Solo Bass Mix, Solo 2000.

## Quirks & pitfalls

Unknown.

## Example

None.

## ROX support

Not read by ROX.

## Parsers & tools

"DDR Utility" (original export tool); RhythmCodex and Scharfrichter have format-specific work for some of these games [inference].

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md) (RhythmCodex test fixtures, `Step1/` at commit `6c60e9b710150c6ca4adf9b7d93e51c2ad39b2ee`). Inspect them with a hex editor to fill the gaps. No other public source (searched GitHub parser repos and archive.org 2026-11-09). Otherwise use "DDR Utility" on your own 2nd Mix to 3rd Mix Plus / Solo data ([`ddr/step.md`](https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md)); RhythmCodex reads it.

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md
- https://zenius-i-vanisher.com/v5.2/thread?threadid=7564
