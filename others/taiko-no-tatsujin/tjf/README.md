# TJF (`.tjf`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: text

## Overview

`.tjf` is the chart format of **Taikosan** (太鼓さん太郎, "Taikosan Tarou", VIL, public release 2007-07-06; re-released 2009-01-16 with **TJF EDIT**, whose first version dates to 2004-05-08, when the program was still called 日曜太鼓 "Sun(day) Taiko"). It is the direct ancestor of [TJA](../tja/README.md) (toach's TaikoJiro readme: "tja is a format based on tjf which also attempts to incorporate a bms-like feel"); TaikoJiro 1 can also read TJF.

## Container & encoding

Plain text. Comments (`//`) never existed in TJF. Line-initial whitespace before headers/commands is not allowed. Non-newline whitespace inside note lines is significant in TJF (TaikoJiro ignores it for TJA).

## Structure / metadata

Only what the TJAPlayer3 article says is documented here; the authoritative description is Taikosan's `Readme.txt` (linked from that article, not opened):

- header `BPM:<int>` (integer only in TJF, floats arrived with TaikoJiro v1.29 for TJA);
- note digits `0` to `7` where each symbol is **one 1/16 note** (no `,` measure separator exists);
- no `8` terminator: a roll/balloon's duration is written by repeating its head symbol, the last repeat corresponds to TJA `8` (TJF `5555` = TJA `5558`);
- command `#GOMUSIC` starts the music at that position (there is no `OFFSET`; the author states offsets must be adjusted with `#GOMUSIC` and BPM changes — similar to the absence of `GAP` in DWI/MSD).

Unknown: full header list, complete command set, difficulty/course handling.

## Timing model

Beat-grid based: each symbol = 1/16 note at the current BPM; `#GOMUSIC` marks the audio start (replaced by `OFFSET:` in TJA).

## Notes

`0` blank, `1`–`7` as TJA `1`–`7` (don, ka, big don, big ka, roll, big roll, balloon) per the TJAPlayer3 article ("Inspired by TJF format (`0` to `7`)").

## Audio & images

Unknown (external audio started with `#GOMUSIC`).

## Versions & variants

Superseded by TJA after 2008-12-08. Related Taikosan-era tool: TJF EDIT.

## Quirks & pitfalls

Unknown beyond the differences listed above (no comments, no `,`, no `8`, integer BPM).

## Example

Illustrative, hand-built from the rules above (not a real file): `BPM:120` then a line of 16 symbols such as `1020102010201020` is one 4/4 measure of 1/16 notes (don/ka alternating).

## ROX support

Not read by ROX.

## Parsers & tools

TaikoJiro (reads `.tjf`), Taikosan, TJF EDIT; no open-source parser identified.

## Sources

- <https://iepiweidieng.github.io/TJAPlayer3/tja> (formats table, "About TJA", "Notechart Formats Inspiring TJA", "Note Symbols in Taiko Mode")
- Taikosan `Readme.txt` and TaikoJiro readme, mirrored at `iepiweidieng.github.io/TJAPlayer3/taiko-sim-readmes/` (linked from the above, not opened)
