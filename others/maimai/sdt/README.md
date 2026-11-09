# SRT / SZT / SCT / SDT (maimai classic charts)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (comma-separated numbers; encrypted `S*B` counterparts)

## Overview

The original maimai (arcade, 2012–2019, "maimai classic": maimai to PLUS to GreeN to … to FiNALE) used four successive text chart formats: `.srt`, `.szt`, `.sct`, `.sdt`, plus encrypted variants `.srb/.szb/.scb/.sdb` ("S*T"/"S*B" is MaiConverter's naming). Source: donmai's blog post *The Four Chart Formats of Maimai Classic* (2020; corrected 2021) and MaiConverter. FiNALE uses another layout, deferred by the post to a follow-up (not found). The DX format is [ma2](../ma2/README.md). Category: others, see [../README.md](../README.md).

## Container & encoding

One line per note: seven comma-separated number columns (SRT, SZT), eight (SCT), nine (SDT), whitespace-padded, trailing comma on each line. No header, BPM or title. The engine looks up BPM and audio in external tables (hence MaiConverter's `--bpm` argument for sdt to ma2/simai). Encrypted variants (`.srb`, `.szb`, `.scb`, `.sdb`) are AES-encrypted containers of the same data; MaiConverter's `encrypt`/`decrypt` need the game key (not published here).

## Structure / metadata

No metadata. Columns:

| # | SRT / SZT | SCT adds | SDT adds |
|---|---|---|---|
| 1 | measure, whole part (integer written as float, first measure = 1) | | |
| 2 | measure, fractional part (0.000000–0.999999; SDT uses 4 decimals) | | |
| 3 | duration (hold/slide length in measures); for taps an unexplained constant like 0.0625 | | |
| 4 | button 0–7 (0 = button at 1 o'clock, then clockwise; button 7 is at the 11 o'clock position) | | |
| 5 | note type | | |
| 6 | slide id | | |
| 7 | slide pattern | | |
| 8 | – | slide amount (number of slides launched by a star) | |
| 9 | – | – | slide delay in measures (default one quarter note in older formats) |

### Note types (column 5)

| Value | SRT | SZT/SCT/SDT |
|---|---|---|
| 0 | tap | start slide |
| 1 | – | regular tap |
| 2 | hold | hold |
| 3 | – | break tap |
| 4 | break tap | star note |
| 5 | – | break star note |
| 128 | end slide | end slide |

SRT slides: a tap (0) + an end-slide (128) sharing a unique slide id and slide pattern. SZT+: a star note (4/5, slide id 0 and pattern 0) + a start slide (0, unique id, non-zero pattern) + an end slide (128, same id and pattern). Some Utage charts omit the star (and some replace all taps with stars).

### Slide patterns (column 7)

SRT: `0` straight, `1` along the ring clockwise, `2` along the ring counter-clockwise (ring slides limited to 3 places). SZT/SCT/SDT:

| Value | Shape | simai |
|---|---|---|
| 1 | straight (end must be ≥ 2 places away or defaults to 2 places CCW) | `-` |
| 2 | along the judgement ring CCW (full 360° allowed) | `<` `>` `^` |
| 3 | along the ring CW | `<` `>` `^` |
| 4 | arc around the centre CCW (table); the post's text labels this one `q` | `p` / `q` (inconsistent in the post) |
| 5 | arc around the centre CW | `q` / `p` |
| 6 | zigzag S | `s` |
| 7 | zigzag Z (end must be 180° from start, else it looks like `s`) | `z` |
| 8 | start to centre to end (straight) | `v` |
| 9 | start to centre (straight) to end (CCW arc) | `pp` |
| 10 | start to centre to end (CW arc) | `qq` (post says `pp`, apparently a typo) |
| 11 | start to two places CCW (straight) to end | `V` |
| 12 | start to two places CW to end | `V` |
| 13 | fan (always to the opposite button) | `w` |

## Timing model

Position = measure.fraction (float), duration in measures. No tempo, no offset: the engine takes the song BPM from a table, and BPM changes are not supported. Four decimals of precision suffice (the engine parses only four decimals in SDT). Slide delay (SDT) is in measures; before SDT it is a fixed quarter note. Time = `(measure_index − 1 + fraction) · 4 · 60/BPM` (inferred from "starting at measure 1.0000").

## Notes

Tap / break tap / hold / star / break star / slide (id, pattern, amount, delay). No touch (DX only). Simultaneous notes share the same time columns.

## Audio & images

None.

## Versions & variants

SRT (first), SZT (new note types, 3-note slides), SCT (slide amount), SDT (slide delay; used to the end of classic). FiNALE: other layout. maimai DX: `ma2`.

## Quirks & pitfalls

- First column looks like a float but is the integer measure.
- Pattern values 11/12 crash the game if start = end; bug if end lies between start and the second point.
- Ring slide numbering differs between SRT and SZT+ (1/2 swapped).
- No BPM in the chart: converters need an external BPM.
- MaiConverter has a naive touch to tap/hold conversion (`--convert_touch`).

## Example

From donmai's blog (SCT/SDT slide example, nine columns for SDT):

```
1.0000, 0.0000, 0.0625, 1,   1,   0,   0,   0,  0.0000,
1.0000, 0.5000, 0.0625, 1,   4,   0,   0,   2,  0.0000,
1.0000, 0.5000, 0.5000, 1,   0,   1,   1,   0,  0.2500,
1.0000, 0.5000, 0.5000, 1,   0,   2,   1,   0,  0.0000,
2.0000, 0.0000, 0.0000, 4, 128,   1,   1,   0,  0.0000,
2.0000, 0.0000, 0.0000, 6, 128,   2,   1,   0,  0.0000,
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

[donmai-me/MaiConverter](https://github.com/donmai-me/MaiConverter) (Python: parse/convert sdt, ma2, simai; AES encrypt/decrypt), sinmai-mods MoreChartFormats (loads srt/szt/sct/sdt in the DX game).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (synthetic only). No real classic chart is public (game data, encrypted; searched GitHub, MaiConverter, Neskol repos, gists). MaiConverter converts ma2/simai to sdt (`ma2tosdt`, `simaitosdt`). Write-up: <https://listed.to/@donmai/18173/the-four-chart-formats-of-maimai-classic>.

## Sources

- <https://listed.to/@donmai/18173/the-four-chart-formats-of-maimai-classic> (read in full)
- <https://github.com/donmai-me/MaiConverter> README (read)
- <https://gitea.tendokyu.moe/beerpsi/sinmai-mods/src/branch/trunk/README.md> (search snippet)
