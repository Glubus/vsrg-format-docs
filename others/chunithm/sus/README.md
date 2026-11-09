# SUS (`.sus`, Sliding Universal Score)
Kind: chart

Doc status: partial · ROX: decode only, as a Project SEKAI chart · Category: others · Encoding: text (UTF-8, CRLF or LF)

## Overview

SUS ("Sliding Universal Score", originally "SeaUrchin Score", the proprietary format of the Seaurchin CHUNITHM-like simulator) is a plain-text, BMS-inspired, measure-grid chart format with **channel lines** (`#mmmcxy: data`). It is the *lingua franca* of the CHUNITHM fan scene: charts made with ched / Seaurchin tooling, read by UMIGURI ("SUS Format rev2"), and later adopted by tooling for Project Sekai (`sus-io`, PJSK engine). SUS has no tab-separated header; it looks like BMS: a few `#KEY "value"` metadata lines and then `#<measure><channel>: <2-digit tokens>` data lines. Spec versions seen: **v2.7 (rev2)** (waki285 gist, no longer retrievable at the time of writing — HTTP 404) and a PJSK-specific derivative by YumYummity.

Category: **others** — same lane/width/air model as [c2s](../c2s/README.md); see [../README.md](../README.md).

## Container & encoding

- Plain text, all printable characters, extension `.sus`, EOL CRLF or LF, **UTF-8**.
- Only lines starting with `#` carry data; every other line is a comment. Strings use double quotes.
- Metadata commands are `#NAME` with no space between `#` and the name; "ASCII" fields cannot contain non-ASCII characters, "UTF-8" fields can.
- One file = one chart.

## Structure / metadata

Metadata (v2.7, as reflected in the PJSK variant): `#TITLE "…"`, `#ARTIST "…"`, `#DESIGNER "…"` (all UTF-8), `#REQUEST "ticks_per_beat 480"` (the only effective one in PJSK; sets the number of ticks per beat), plus (v2.7 family, per UMIGURI's "unsupported syntax" list) `#SUBTITLE`, `#GENRE`, `#BASEBPM`, `#ATR`/`#ATTRIBUTE`/`#NOATTRIBUTE`, `#NOSPEED`, and `#REQUEST` keys `enable_priority`, `enable_moving_lane`, `segments_per_second`.

Chart data lines: `#<mmm><c><x><y>[zz]: <data>` — `mmm` = 3-digit **measure number** from 0 (so 0–999); if it is not numeric the line is special data (e.g. `#BPM01: 140.0`, `#ATR01: "pr:100"`, `#TIL01: "0'0:1.0, 0'960:2.0"`); `c` = note type; `x` = leftmost lane (0-9a-z, case-insensitive); `y` = channel (0-z) for note types that need it; `zz` = base-36 special number. The **data part is a list of 2-character tokens**; the measure is divided equally into as many slots as there are tokens (`1111111111` = quarter notes in 4/4... in the PJSK spec's wording: five slots). The first character of a token is type-specific (`0` = nothing), **the second is the note width** (1–z = 1–35). Positions without a note are `00`. Parsers must support at least 512 slots (1024 chars).

### Special lines

| Line | Meaning |
|---|---|
| `#mmm02: n` | measure length in beats from measure `mmm` on (decimal allowed; PJSK requires exactly 4) |
| `#BPMzz: x` and `#mmm08: zz` | define BPM `zz` (uppercase base 36 — case-sensitive), and switch to it at the slots set in `#mmm08` |
| `#ATRzz: "rh:..,h:..,pr:.."` + `#ATTRIBUTE zz` / `#NOATTRIBUTE` | note attributes (roll speed, height, priority) applied to following data |
| `#TILzz: "meas'tick:speed, ..."` + `#HISPEED zz` / `#NOSPEED` | hi-speed (soflan) definitions applied to following notes (`meas'tick:speed`, 480 ticks per beat by default) |
| `#MEASUREHS zz` | bar-line speed definition (same format as `TIL`) |

### Note channels (PJSK spec; CHUNITHM semantics noted in the spec)

| Prefix | Notes |
|---|---|
| `#mmm1x` | single taps: `1?` tap, `2?` critical tap, `3?` flick (used to attach slide relays), `4?` skill activation (= CHUNITHM damage/mine; must be lane 0, width 1 to count), `5?` trace, `6?` critical trace, `7?`/`8?` "elaser" (hides slide start/end, removes judgement) |
| `#mmm3xy` | slides: `1?` start, `2?` end, `3?` visible relay, `4?` Bézier control, `5?` invisible relay; same channel `y` connects points |
| `#mmm5x` | directional (flick/air): `1?` up, `2?` down, `3?` left-up, `4?` right-up, `5?` left-down, `6?` right-down; must overlap another note to set direction |
| `#mmm9xy` | guide (decorative slide): `1?` start, `2?` end, `5?` relay |

Other channels used by CHUNITHM SUS charts (hold `2xy`, air-hold, air-action…) are **not covered by the sources I could open** (the v2.7 gist was unavailable). Overlap rules: notes of different types on the same leftmost lane at the same slot are "overlaps" that attach attributes (direction, critical, easing) to the underlying note; an overlapped tap that is not meant as an attribute causes a miss.

## Timing model

BMS-like: measure number + slot index inside the measure; each measure is divided by the number of 2-character tokens of the line; measure length defaults to 4 beats (`#mmm02`), BPM from `#BPMzz`/`#mmm08`. `ticks_per_beat` (default 480) gives the resolution for `TIL`/`MEASUREHS` ticks (1920 ticks per 4/4 measure). The PJSK spec has no audio-offset field (not verified for v2.7).

## Notes

See channel table. Width is the second digit of every token (1–z). Slides are chains of tokens linked by their `y` channel digit; relays carry their own width so a slide can widen/narrow.

## Audio & images

Not referenced in the chart (PJSK: "none of these metadata lines do anything"); simulators locate audio by file name next to the chart.

## Versions & variants

- **v2.7 rev2** (Seaurchin/ched): the reference for CHUNITHM-style notes.
- **PJSK variant** (YumYummity, "post 3rd anniversary"): defines taps/critical, traces, guides, easing via overlapped directional notes, and mandates 4/4.
- UMIGURI (rev2) limitations: FLICK and AIR widths snapped to 1, 2, 3, 4, 6, 8 or 16; AIR attached to an AIR-HOLD is forced to up-AIR; AIR-HOLD height / AIR-ACTION position and width ignored; AIR without a parent note not loaded; unsupported lines listed above; Bézier slides are supported but deprecated.

## Quirks & pitfalls

- `#BPMzz` index must be uppercase.
- Measure numbers cap at 999.
- A tap overlapping a slide end/start without being an attribute marker will miss (PJSK).
- Width 0 does not exist; the token second character is the width.
- Metadata can be absent entirely; BMS-style parsing (ignore everything not starting with `#`) is the safe approach.

## Example

Illustrative, hand-built from the PJSK spec rules above (not a real file):

```
#TITLE "demo"
#REQUEST "ticks_per_beat 480"
#BPM01: 120
#00008: 01
#00010: 1414141414141414
```

## ROX support

Read by ROX as a Project SEKAI chart (`rox::formats::sekai::SusDecoder`, see [`../../../vsrg/project-sekai/sus`](../../../vsrg/project-sekai/sus/README.md)): a CHUNITHM `.sus` is the same text format, and ROX cannot tell the two dialects apart from the first bytes. It is read on the 12 lanes of Project SEKAI (`x = 2..=13`); the notes on the lanes of the 16 outside them, the holds (`#mmm2xy`) and the slides 2 (`#mmm4xy`) of CHUNITHM are dropped and counted (`SekaiReport`), never played as taps; an air note (`#mmm5x`) is read as a directional (a flick counted on the note under it, else a stray overlay, counted). The real CHUNITHM layout (16 cells, air plane) is not modelled.

## Parsers & tools

[mkpoli/sus-io](https://github.com/mkpoli/sus-io) (Python + npm `sus-io`, `sus-parse`, `sus-stringify`), ched (Windows editor), Seaurchin, UMIGURI, Project Sekai charting tools.

## Getting samples

- **Committed**: 6 real SUS files written by Ched (Project Sekai dialect): one from sonolus-pjsekai-engine-extended (MIT) and five fixtures from sonolus-level-converters (GPL-3.0; CR CR LF line endings). Origin, author, date, sha256 and licence/terms of each file are in [`samples/SOURCES.md`](samples/SOURCES.md).
- **More samples**: Ched writes SUS; UMIGURI can import it (https://umgr.inonote.jp/docs/others/chart-sus); UntitledCharts/chart-downloader fetches PJSK charts. No CHUNITHM-specific licensed `.sus` was found.

## Sources

- <https://gist.github.com/YumYummity/49935bf74367712b6ba240474cb7ce22> (read; derivative of the v2.7 spec by waki285)
- <https://gist.github.com/waki285/dafa254a9de56ba43d177ae0913d4263> (listed in search results; fetch failed)
- <https://umgr.inonote.jp/docs/others/chart-sus> (UMIGURI limitations; read)
- <https://pypi.org/project/sus-io/0.2.1> (read)
