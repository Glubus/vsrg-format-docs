# TJF (`.tjf`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: text

## Overview

`.tjf` is the chart format of Taikosan (太鼓さん太郎, VIL, public release 2007-07-06; re-released 2009-01-16 with TJF EDIT, first version 2004-05-08 under the name 日曜太鼓 "Sun(day) Taiko"). It is the direct ancestor of [TJA](../tja/README.md) (toach's TaikoJiro readme: "tja is a format based on tjf which also attempts to incorporate a bms-like feel"). TaikoJiro 1 can read TJF.

## Container & encoding

Plain text. TJF has no `//` comments. Whitespace before headers/commands is not allowed. Non-newline whitespace inside note lines is significant (TaikoJiro ignores it for TJA).

## Structure / metadata

Only what the TJAPlayer3 article documents; the authoritative description is Taikosan's `Readme.txt` (linked from that article, not opened):

- header `BPM:<int>` (integer only in TJF; floats came with TaikoJiro v1.29 for TJA);
- note digits `0` to `7`, each symbol one 1/16 note (no `,` measure separator);
- no `8` terminator: a roll/balloon's duration is written by repeating its head symbol, the last repeat corresponds to TJA `8` (TJF `5555` = TJA `5558`);
- command `#GOMUSIC` starts the music at that position. There is no `OFFSET`; the author states offsets are adjusted with `#GOMUSIC` and BPM changes (like the absence of `GAP` in DWI/MSD).

Per the Taikosan readme: headers `TITLE`, `LEVEL` (1-10), `BPM`, `WAVE`; chart between `#START` and `#END`; digit `7` (gekirenda/balloon) shows graphics only; commands `#GOMUSIC`, `#BPMCHANGE n`, `#ONESYOSETU` (next line is one measure whatever its length) [observed in https://iepiweidieng.github.io/TJAPlayer3/taiko-sim-readmes/utf-8/Readme-taikosan-plusedit.txt].

Unknown: full header list, complete command set, difficulty/course handling.

## Timing model

Each symbol is a 1/16 note at the current BPM; `#GOMUSIC` marks the audio start (TJA: `OFFSET:`).

## Notes

`0` blank, `1`-`7` as TJA (don, ka, big don, big ka, roll, big roll, balloon), per the TJAPlayer3 article ("Inspired by TJF format (`0` to `7`)").

## Audio & images

Unknown (external audio started with `#GOMUSIC`).

## Versions & variants

Superseded by TJA after 2008-12-08. Related tool: TJF EDIT.

## Quirks & pitfalls

Unknown beyond the differences above.

## Example

Hand-built from the rules above (not a real file): `BPM:120` then `1020102010201020` is one 4/4 measure of 1/16 notes (don/ka alternating).

## ROX support

Not read by ROX.

## Parsers & tools

TaikoJiro (reads `.tjf`), Taikosan, TJF EDIT (writes `.tjf`); no open-source parser identified.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (`taikosan_syatyou.tjf`, VIL's sample chart from the Taikosan plusedit package, MediaFire link on https://w.atwiki.jp/laser_bm/pages/72.html; exe, mp3 and docs not kept). Observed [observed: samples/taikosan_syatyou.tjf]: Shift-JIS text, headers `TITLE`, `LEVEL`, `BPM`, `WAVE`, a blank line, `#START`, 16-symbol measure lines and the `#THREERENPU-GO` hidden command (deprecated per the readme). No other real `.tjf` was found: getuploader archives answer 403 and a Wayback/archive.org search found nothing.

## Sources

- <https://iepiweidieng.github.io/TJAPlayer3/tja> (formats table, "About TJA", "Notechart Formats Inspiring TJA", "Note Symbols in Taiko Mode")
- Taikosan `Readme.txt` and TaikoJiro readme, mirrored at `iepiweidieng.github.io/TJAPlayer3/taiko-sim-readmes/` (linked from the above, not opened)
