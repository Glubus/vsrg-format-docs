# SLOEDIT chart (`.slo`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown (probably text)

## Overview

`.slo` is the file of **SLOEDIT**, "SLO chart editor", a companion of the D2R chart editor (D2REDIT) on the Japanese site "D2R譜面サーチ" (paramax.hypermart.net). Per the editor page: SLOEDIT reads and writes `*.slo` only; features: edit while seeing the actual arrows (arrows colour-coded), minimum unit 1/16, tempo changes inside a song, and a **one-hand editing environment** ("片手編集環境"). D2REDIT can also *write* `*.slo` (it reads `*.d2r`, `*.sul`, `*.msd`, `*.ddr`; writes `*.d2r`, `*.ddr`, `*.slo`). StepMania's `misc.txt` lists "[D2R, SLO] Obscure old Japanese formats". No grammar for `.slo` was found anywhere.

## Container & encoding

Unknown.

## Structure / metadata

The definition part uses `KEY=value` lines; SLOEDIT's template `slohead.txt` lists the keys `ORDER= PLAYMODE= TITLE= ARTIST= MUSIC= SHORTCUT= TEMPO10= DELAYTIME= BGBMP= TITLEBMP= WAKUBMP= CDTRACK= CDTRACKFROM= CDTRACKTO= CDDELAYTIME= START=` [observed in `sloedit.zip:slohead.txt`, Wayback 2003-12-19 copy of http://paramax.hypermart.net/sloedit.zip]. Its readme says the definition part follows D2R2's (documented in [d2r](../d2r/README.md): `TITLE`, `ARTIST`, `MUSIC`, `SHORTCUT`, `TEMPO10`, `START` match; `ORDER`, `PLAYMODE`, `DELAYTIME`, `BGBMP`, `TITLEBMP`, `WAKUBMP` are new here). The chart grammar itself is Unknown.

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

## Getting samples

No sample: no `.slo` file or specification was found. Observed in the SLOEDIT archive (https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/sloedit.zip, 176,632 bytes; read 2026-11-09): `slohead.txt` is the editor's template of **definition-part keys**: `ORDER= PLAYMODE= TITLE= ARTIST= MUSIC= SHORTCUT= TEMPO10= DELAYTIME= BGBMP= TITLEBMP= WAKUBMP= CDTRACK= CDTRACKFROM= CDTRACKTO= CDDELAYTIME= START=` (so `TITLE`, `ARTIST`, `MUSIC`, `SHORTCUT`, `TEMPO10`, `START` resemble [`.d2r`](../d2r/README.md); `ORDER`, `PLAYMODE`, `DELAYTIME`, `BGBMP`, `TITLEBMP`, `WAKUBMP` are new). The readme says the definition part follows the D2R2 style ("most D2R2 definitions can be used as-is"), notes are placed with keys `4 7 2 8 9 6 ; p : @ [ ]`, the arrow colours at 1/16 are "yellow, grey, blue, grey", and the editor autosaves. To get a file: run SloEdit.exe (Windows) from that archive, choose a play mode, place arrows, and save.

## Sources

- http://web.archive.org/web/20031219024931/http://paramax.hypermart.net/editor.html
- https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/sloedit.zip (`readme.txt`, `slohead.txt`)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt
