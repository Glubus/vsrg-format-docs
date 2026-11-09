# DTXMania older chart format (`.g2d`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: text

## Overview
`.g2d` is the sibling of [`.gda`](../gda/README.md): `CDTX.tRead` maps `.g2d` to `EType.G2D`, and `tInput_LineAnalysis_ChipLocation` handles G2D and GDA in one branch (GDA 2-letter channel names translated with `STGDAPARAM`). What distinguishes G2D from GDA is Unknown. The original README only says "older format" and links `CDTXInputOutput.cs`, where `GDA` and `G2D` are separate enum members (`E種別`) with the same line analysis (`tDTX入力_行解析_チャンネル_GDAチャンネル文字列２桁をチャンネル番号にして返す`).

## Container & encoding
Text lines like DTX. [observed: KAIRU_*.g2d, AOiRO_Manbow_Sky-on-grass__GDA.g2d] Same grammar as [gda](../gda/README.md): `#KEY value` headers (`#TITLE CLASSIC PARTY(BASIC)`, `#BPM ???` (literally, not a number), `#DLEVEL 52`, `#GLEVEL 89`, `#BLEVEL 61`), `#WAVzz file` tables (`#WAV01 01.XA` ... `.XA` samples), 2-letter data channels (`HH`, `BD`, `G1`..`G7`, `GW`, `B1`.., `TC`, `BL`), `;`/`*----- HEADER FIELD` comment lines. Shift_JIS or ASCII with CRLF; the extension may be upper case (`.G2D`). Editors named in the files: `;Created by GDA Creator Professional Ver.0.14b`, `;Created by GDA Creator Ver.1.25 Rev.Final`.

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
Only DTXMania's loader serves as reference.

## Example
[observed] e.g. samples/KAIRU_Drum3rd-Classic_Party_2_1_classic2_BAS.g2d (CP932, CRLF) shows the same text grammar as `.gda`; the AOiRO_Manbow pack even names its g2d `_GDA.g2d`.

## ROX support
Decode only, as a [`.gda`](../gda/README.md) (`GdaDecoder`, `DetectedFormat::Gda`). The 6 committed `.g2d` decode, each with drums, guitar and bass. `#BPM ???` (a literal, in the KAIRU files) gives no BPM: 120 until the first `TC` line.

## Parsers & tools
DTXmaniaNX / DTXCreator: https://github.com/limyz/DTXmaniaNX

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: other packs of the archive.org items `raredtxgda` and `raredtxgda2` (RAR per charter: `https://archive.org/download/raredtxgda/<path>`, extract with `bsdtar`/`7z`). Only 5 `.g2d` files turned up in the ~95 smaller packs examined.

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
