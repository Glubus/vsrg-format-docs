# D2R legacy chart (`.sul`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text (probably)

## Overview

`.sul` is the chart format of the **earlier version of Dazzle Dazzle Realization** (before 2ndMIX). The D2R format page says the single-character duration symbols are "the symbols used by the previous version's charts (`*.sul`). They can still be used in the new version, but should not be used much". D2REDIT (D2R chart editor) can read `*.sul` files. The ORIGINAL_README entry for `.sul` is the root URL of that site (`paramax.hypermart.net`, archived 2004-02-05). Nothing else is documented.

## Container & encoding

Unknown (likely a text format like [`.d2r`](../d2r/README.md)).

## Structure / metadata

Unknown.

## Timing model

The duration symbols inherited by `.d2r` are known: `P` (quarter), `p` (eighth), `Q` (sixteenth), `8.` (32nd) and `T` (triplet, sets of three), e.g. `P:L   :    :`; the full `.d2r` table is in [d2r](../d2r/README.md#timing-model). Whether `.sul` lines have the same `length:1P:2P:option` shape is an inference.

## Notes

Probably the same `L D U R` 4-character arrow fields (space = none) [inference from the `.d2r` page].

## Audio & images

Unknown.

## Versions & variants

Pre-2ndMIX D2R.

## Quirks & pitfalls

Not applicable (not documented).

## Example

Not available.

## ROX support

Not read by ROX.

## Parsers & tools

D2REDIT reads it (closed, not hosted anymore).

## Getting samples

No sample and no grammar: `.sul` was the chart format of the earlier D2R (before 2ndMIX). D2REDIT reads `.sul` (its Japanese readme: "files that load normally are the D2R chart files (`*.d2r` / `*.sul`)") and the D2R official site offered a `d2r2sul` converter (named in the same readme). To get real files: run D2REDIT from the Wayback archive https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/d2redit.zip (224,948 bytes) and a `.d2r` through `d2r2sul` (not found online), or find old D2R charts; both unverified here. The one-character duration symbols of `.sul` are listed in [`d2r`](../d2r/README.md).

## Sources

- http://web.archive.org/web/20030807133410/http://paramax.hypermart.net/d2r.html
- http://web.archive.org/web/20031219024931/http://paramax.hypermart.net/editor.html
- http://web.archive.org/web/20040205071612/http://paramax.hypermart.net/
