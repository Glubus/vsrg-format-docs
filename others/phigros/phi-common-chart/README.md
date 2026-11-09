# PhiCommonChart (PhiFanmade interchange model) (`.json / protobuf`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: mixed

## Overview

PhiFanmade's "PhiCommonChart" is a common chart model for Phigros fan tools, with a documented JSON form and a protobuf schema (`package PhiCommonChart.ChartStructs`). The judge line model has `XMoveEvents`, `YMoveEvents`, `RotateEvents`, `AlphaEvents`, `SpeedEvents`, `Notes`, `FatherIndex`, `RotateWithFather`, `IsCover`, `AttachUi`, `Anchor`, `BpmFactor`, `ZOrder`, `ExtendedEvents`, `TextureData`/`TexturePath` and a per-field "compatibility level".

## Container & encoding

JSON and protobuf (proto3, `message JudgeLine` with explicit field numbers 1-16 and 100).

## Structure / metadata

Judge line (field numbers): 1 `TextureData` (bytes), 2 `IsGifTexture`, 3 `XMoveEvents`, 4 `YMoveEvents`, 5 `RotateEvents`, 6 `AlphaEvents`, 7 `SpeedEvents`, 8 `Notes`, 9 `FatherIndex` (-1 none), 10 `RotateWithFather` (default true), 11 `IsCover` (default true), 12 `AttachUi` enum (None, Pause, ComboNumber, ComboText, Score, ProgressBar, Name, Level), 13 `Anchor` (float[], default 0.5), 14 `BpmFactor` (effective BPM = global / factor), 15 `ZOrder`, 16 `ExtendedEvents`, 100 `TexturePath`. Event lists are sorted by `StartBeat`, must not overlap; defaults when empty: X/Y/Rotate 0, Alpha 0, Speed 10. Other messages (root, event, note) not read.

## Timing model

Beat based (`StartBeat`/`EndBeat`). Root/BPM structure not read.

## Notes

Unknown.

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

## Getting samples
Committed: nothing. The docs site (https://docs.nuanr-mxi.com/en/) shows JSON fragments only (e.g. the default judge line object in `judge_line.html`) and a proto3 definition (`package PhiCommonChart.ChartStructs`); no repository with sample charts exists. PhiFanmade tools (listed on the docs site, not opened) should produce one [inference].

## Sources

- <https://docs.nuanr-mxi.com/en/chart_format/judge_line.html>
