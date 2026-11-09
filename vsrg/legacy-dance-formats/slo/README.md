# SLOEDIT chart (`.slo`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown (probably text)

## Overview

`.slo` is the file of SLOEDIT ("SLO chart editor"), companion of the D2R chart editor D2REDIT on the Japanese site "D2R譜面サーチ" (paramax.hypermart.net). SLOEDIT reads and writes `*.slo` only: it shows colour-coded arrows, has a minimum unit of 1/16, supports tempo changes and offers a one-hand editing environment ("片手編集環境"). D2REDIT also writes `*.slo` (it reads `*.d2r`, `*.sul`, `*.msd`, `*.ddr`; writes `*.d2r`, `*.ddr`, `*.slo`). StepMania's `misc.txt` lists "[D2R, SLO] Obscure old Japanese formats". No grammar for `.slo` was found.

## Container & encoding

Unknown.

## Structure / metadata

The definition part uses `KEY=value` lines; SLOEDIT's template `slohead.txt` lists the keys `ORDER= PLAYMODE= TITLE= ARTIST= MUSIC= SHORTCUT= TEMPO10= DELAYTIME= BGBMP= TITLEBMP= WAKUBMP= CDTRACK= CDTRACKFROM= CDTRACKTO= CDDELAYTIME= START=` [observed in `sloedit.zip:slohead.txt`, Wayback 2003-12-19 copy of http://paramax.hypermart.net/sloedit.zip]. The readme says the definition part follows D2R2's (documented in [d2r](../d2r/README.md): `TITLE`, `ARTIST`, `MUSIC`, `SHORTCUT`, `TEMPO10`, `START` match; `ORDER`, `PLAYMODE`, `DELAYTIME`, `BGBMP`, `TITLEBMP`, `WAKUBMP` are new here). The chart grammar itself is Unknown.

## Timing model

Unknown. SLOEDIT's minimum unit is 1/16 (same as D2REDIT) and it supports tempo changes.

## Notes

Unknown. "One-hand editing" suggests a single-hand variant (keys for one hand) [inference].

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

SLOEDIT (~200 KB, from the chart-search site; no longer hosted).

## Getting samples

No sample: no `.slo` file or specification was found. [observed: sloedit.zip] https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/sloedit.zip (176,632 bytes, read 2026-11-09): `slohead.txt` is the template of definition-part keys: `ORDER= PLAYMODE= TITLE= ARTIST= MUSIC= SHORTCUT= TEMPO10= DELAYTIME= BGBMP= TITLEBMP= WAKUBMP= CDTRACK= CDTRACKFROM= CDTRACKTO= CDDELAYTIME= START=`. The readme says the definition part follows D2R2 style ("most D2R2 definitions can be used as-is"), notes are placed with keys `4 7 2 8 9 6 ; p : @ [ ]`, the arrow colours at 1/16 are "yellow, grey, blue, grey", and the editor autosaves. To make a file, run SloEdit.exe (Windows) from that archive, choose a play mode, place arrows, and save.

## Sources

- http://web.archive.org/web/20031219024931/http://paramax.hypermart.net/editor.html
- https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/sloedit.zip (`readme.txt`, `slohead.txt`)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt
