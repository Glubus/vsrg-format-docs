# DTXMania older chart format (`.g2d`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text

## Overview
`.g2d` is the sibling of [`.gda`](../gda/README.md): DTXMania's `CDTX.tRead` maps the extension `.g2d` to `EType.G2D`, and in `tInput_LineAnalysis_ChipLocation` G2D and GDA share the same branch (GDA 2-letter channel names translated to DTX channels with the `STGDAPARAM` table). What distinguishes G2D from GDA (e.g. the game generation or a different header) is Unknown: no public specification found; the original README only says "older format" and links `CDTXInputOutput.cs`, where `GDA` and `G2D` are separate enum members (`E種別`) but share the same line analysis (`tDTX入力_行解析_チャンネル_GDAチャンネル文字列２桁をチャンネル番号にして返す`).

## Container & encoding
Text lines like DTX; charset Unknown.

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
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
DTXmaniaNX / DTXCreator: https://github.com/limyz/DTXmaniaNX

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
