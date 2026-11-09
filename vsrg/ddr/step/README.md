# DDR STEP data (1st-3rd Mix era, "DDR Utility" export)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview

"STEP" is not an official name: SaxxonPike's `rhythm-game-formats` uses it for "the format exported using DDR Utility" and found in **Dance Dance Revolution 2nd Mix through 3rd Mix Plus, including Solo Bass Mix and Solo 2000**. The Solo mixes have "a slight variation in step panel configuration". It precedes the chunked [SSQ](../ssq/README.md) format (first used in 4th Mix) and is related to, but distinct from, [STEP2](../step2/README.md) (1st Mix only). The upstream page is a stub ("In a nutshell: TODO").

## Container & encoding

Unknown (binary; extension, header, endianness, quantization are not documented upstream).

## Structure / metadata

Unknown.

## Timing model

Unknown. (The ZIv "DDR Research Master Thread" describes the PRE-MAX engine's *in-RAM edit mode* layout, one byte per beat with a nibble per player, which is probably the same data family but is not a file specification.)

## Notes

Unknown beyond: Solo mixes use a different panel configuration (6 panels: the ZIv thread lists UL/UR bytes for solo edit data).

## Audio & images

Unknown.

## Versions & variants

2nd Mix .. 3rd Mix Plus, Solo Bass Mix, Solo 2000.

## Quirks & pitfalls

Not applicable (not documented).

## Example

Not available.

## ROX support

Not read by ROX.

## Parsers & tools

"DDR Utility" (original export tool); RhythmCodex and Scharfrichter have format-specific work for some of these games [inference].

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step.md
- https://zenius-i-vanisher.com/v5.2/thread?threadid=7564
