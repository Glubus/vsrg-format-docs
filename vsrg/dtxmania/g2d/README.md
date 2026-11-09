# DTXMania older chart format (`.g2d`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text

## Overview
`.g2d` is the sibling of [`.gda`](../gda/README.md): DTXMania's `CDTX.tRead` maps the extension `.g2d` to `EType.G2D`, and in `tInput_LineAnalysis_ChipLocation` G2D and GDA share the same branch (GDA 2-letter channel names translated to DTX channels with the `STGDAPARAM` table). What distinguishes G2D from GDA (e.g. the game generation or a different header) is Unknown: no public specification found; the original README only says "older format" and links `CDTXInputOutput.cs`, where `GDA` and `G2D` are separate enum members (`E種別`) but share the same line analysis (`tDTX入力_行解析_チャンネル_GDAチャンネル文字列２桁をチャンネル番号にして返す`).

## Container & encoding
Text lines like DTX. [observed in samples/KAIRU_*.g2d, AOiRO_Manbow_Sky-on-grass__GDA.g2d] Same grammar as [gda](../gda/README.md): `#KEY value` headers (`#TITLE CLASSIC PARTY(BASIC)`, `#BPM ???` (literally; not a number), `#DLEVEL 52`, `#GLEVEL 89`, `#BLEVEL 61`), `#WAVzz file` tables (`#WAV01 01.XA` ... `.XA` samples), 2-letter data channels (`HH`, `BD`, `G1`..`G7`, `GW`, `B1`.., `TC`, `BL`), `;`/`*----- HEADER FIELD` comment lines; Shift_JIS or ASCII with CRLF; the extension may be upper case (`.G2D`). Editors named in the files: `;Created by GDA Creator Professional Ver.0.14b`, `;Created by GDA Creator Ver.1.25 Rev.Final`.

## Structure / metadata
Same channel-name table as GDA (see [gda](../gda/README.md)).

## Timing model
As DTX (384 ticks/measure, `TC` tempo, `BL` bar length).

## Notes
Same as GDA.

## Audio & images
Unknown.

## Versions & variants
Unknown.

## Quirks & pitfalls
No real sample; only DTXMania's loader as reference.

## Example
Five real files in [samples/](samples/SOURCES.md), e.g. samples/KAIRU_Drum3rd-Classic_Party_2_1_classic2_BAS.g2d (CP932, CRLF). What separates `.g2d` from `.gda` is not visible in them: [observed] the same text grammar (one pack, AOiRO_Manbow, even names its g2d `_GDA.g2d`).

## ROX support
Not read by ROX.

## Parsers & tools
DTXmaniaNX / DTXCreator: https://github.com/limyz/DTXmaniaNX

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): 5 real `.g2d` charts (KAIRU `CLASSIC PARTY` basic and `CLASSIC PARTY 2` BAS/ADV, AOiRO_Manbow `Sky on grass`, a DISCLAIMER chart) extracted from the packs of the archive.org item "Rare DTX&GDA Simfile Collection" (`raredtxgda`, `raredtxgda2`), plus one hand-written `synthetic-` file. Only 5 `.g2d` files were found in the ~95 smaller packs examined.
- **More**: other packs of the same items (RAR per charter: `https://archive.org/download/raredtxgda/<path>`, extract with `bsdtar`/`7z`); DTXmaniaNX (https://github.com/limyz/DTXmaniaNX) loads `.g2d` through `CDTX.tRead`.

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
