# SLOEDIT chart (`.slo`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown (probably text)

## Overview

`.slo` is the file of **SLOEDIT**, "SLO chart editor", a companion of the D2R chart editor (D2REDIT) on the Japanese site "D2R譜面サーチ" (paramax.hypermart.net). Per the editor page: SLOEDIT reads and writes `*.slo` only; features: edit while seeing the actual arrows (arrows colour-coded), minimum unit 1/16, tempo changes inside a song, and a **one-hand editing environment** ("片手編集環境"). D2REDIT can also *write* `*.slo` (it reads `*.d2r`, `*.sul`, `*.msd`, `*.ddr`; writes `*.d2r`, `*.ddr`, `*.slo`). StepMania's `misc.txt` lists "[D2R, SLO] Obscure old Japanese formats". No grammar for `.slo` was found anywhere.

## Container & encoding

Unknown.

## Structure / metadata

Unknown. Related D2R definitions (title, artist, tempo, delay...) are documented in [d2r](../d2r/README.md); whether `.slo` shares that syntax is Unknown.

## Timing model

Unknown. SLOEDIT's stated minimum unit is 1/16 (the same as D2REDIT) and it supports tempo changes.

## Notes

Unknown. "One-hand editing": notes are likely a single-hand/lane variant (e.g. keys for one hand) [inference].

## Audio & images

Unknown.

## Versions & variants

Companion to D2R 2ndMIX tooling (late 1990s).

## Quirks & pitfalls

Not applicable (not documented).

## Example

Not available.

## ROX support

Not read by ROX.

## Parsers & tools

SLOEDIT (~200 KB, from the chart-search site; no longer hosted).

## Sources

- http://web.archive.org/web/20031219024931/http://paramax.hypermart.net/editor.html
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt
