# PhiCommonChart (PhiFanmade interchange model) (`.json / protobuf`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: mixed

## Overview

PhiFanmade's "PhiCommonChart" is a common chart model for Phigros fan tools with a documented JSON form and an accompanying protobuf schema (`package PhiCommonChart.ChartStructs`). Its judge line model has `XMoveEvents`, `YMoveEvents`, `RotateEvents`, `AlphaEvents`, `SpeedEvents`, `Notes`, `FatherIndex`, `RotateWithFather`, `IsCover`, `AttachUi`, `Anchor`, `BpmFactor`, `ZOrder`, `ExtendedEvents`, `TextureData`/`TexturePath` and a per-field "compatibility level".

## Container & encoding

JSON and protobuf (proto3, `message JudgeLine` with explicit field numbers 1-16 and 100).

## Structure / metadata

Judge line (field numbers): 1 `TextureData` (bytes), 2 `IsGifTexture`, 3 `XMoveEvents`, 4 `YMoveEvents`, 5 `RotateEvents`, 6 `AlphaEvents`, 7 `SpeedEvents`, 8 `Notes`, 9 `FatherIndex` (-1 none), 10 `RotateWithFather` (default true), 11 `IsCover` (default true), 12 `AttachUi` enum (None, Pause, ComboNumber, ComboText, Score, ProgressBar, Name, Level), 13 `Anchor` (float[], default 0.5), 14 `BpmFactor` (effective BPM = global / factor), 15 `ZOrder`, 16 `ExtendedEvents`, 100 `TexturePath`. Event lists are sorted by `StartBeat`, must not overlap; defaults when empty: X/Y/Rotate 0, Alpha 0, Speed 10. Other messages (root, event, note) were not read.

## Timing model

Beat based (`StartBeat`/`EndBeat`); root/BPM structure not read.

## Notes

Not read (Note message not consulted).

## Audio & images

Unknown.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

Documentation site: <https://docs.nuanr-mxi.com/en/>.

## Sources

- <https://docs.nuanr-mxi.com/en/chart_format/judge_line.html>
