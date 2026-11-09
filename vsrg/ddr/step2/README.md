# DDR STEP2 data (1st Mix, "DDR Utility" export)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview

"STEP2" is, like [STEP](../step/README.md), a name coined by SaxxonPike's `rhythm-game-formats`: "the format exported using DDR Utility. It is featured **only in 1st Mix** and **can quantize to 1/64**." No further description exists upstream (the page says "In a nutshell: TODO").

## Container & encoding

Unknown.

## Structure / metadata

Unknown.

## Timing model

Unknown; only the statement that it quantizes to 1/64 (so a 64-division grid per measure or beat) is known.

## Notes

Unknown.

## Audio & images

Unknown.

## Versions & variants

DDR 1st Mix only.

## Quirks & pitfalls

Not applicable (not documented).

## Example

Not available.

## ROX support

Not read by ROX.

## Parsers & tools

Unknown ("DDR Utility" exported it).

## Getting samples

Committed in [`samples/`](samples/SOURCES.md): three real STEP2 files from the RhythmCodex test suite (`single.step2` 3,088 bytes, `double.step2` 5,620, `couple.step2` 5,620; commit `6c60e9b710150c6ca4adf9b7d93e51c2ad39b2ee`, `Step2/`; extracted from the fixture zips). They are tiny: ideal to reverse the layout. No other public source was found.

More: the format occurs only in DDR 1st Mix (upstream note in [SaxxonPike/rhythm-game-formats `ddr/step2.md`](https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step2.md)); get it from your own 1st Mix data via "DDR Utility".

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/step2.md
