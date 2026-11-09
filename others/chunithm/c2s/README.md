# C2S (`.c2s`, CHUNITHM chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (UTF-8, tab-separated lines)

## Overview

`.c2s` is the plain-text chart format read by the CHUNITHM arcade engine ("c2s" = chuni 2 score [inference]). It is found in the game data tree `app/data/AXXX/music/musicXXXX/` (one `.c2s` per difficulty: Basic/Advanced/Expert/Master/World's End/Ultima), next to `Music.xml` which holds title/level/difficulty. The format is not publicly documented by SEGA; the descriptions below come from reverse-engineering notes (Suprnova's Chunithm-Research, a HackMD page) and from converter source code (Margrete2S/mgxc2s). The game **reloads `.c2s` files on song selection**, which makes custom-chart debugging easy.

Category: **others** — see [../README.md](../README.md): 16 variable-width cells, slides with changing width, air plane.

## Container & encoding

- Plain text, "standard unicode" (UTF-8; Japanese creator names are written directly), one record per line, **fields separated by a horizontal tab**. In an existing chart the game ignores a note line unless it is formatted exactly; using spaces instead of tabs in a modified line was reported not to work (Suprnova, in Notepad++).
- Block order: header, BPM/meter (and soflan) lines, notes, footer statistics, and the file ends with empty lines (HackMD: "All charts end with 2 empty lines").
- One file per difficulty. Index/title/level are *not* in the file for recent versions (`MUSIC 0`, `DIFFICULT 00`, `LEVEL 0.0` are placeholders; older versions stored the music id and difficulty).

## Structure / metadata

### Header (each once, in this order)

| Line | Fields | Notes |
|---|---|---|
| `VERSION` | `<ver> <ver>` | e.g. `1.08.00`; Margrete2S writes `1.11.00 1.11.00`; "version of the c2s handler" [inference] |
| `MUSIC` | int | music id in old versions, else 0 |
| `SEQUENCEID` | int | 0 |
| `DIFFICULT` | int | difficulty number (old) or 0/00 (3 = Master…) |
| `LEVEL` | float | 0.0 in recent files |
| `CREATOR` | string | chart author; shown on the song card unless difficulty is Basic/Advanced |
| `BPM_DEF` | 4 floats | **display** BPMs: first = initial BPM; second = most used other BPM (mirrors 1st if none); 3rd/4th mirror 2nd/1st (Suprnova) |
| `MET_DEF` | two ints | display meter (Margrete2S writes `4 4`); cosmetic. Field order: see the `MET` line |
| `RESOLUTION` | int | ticks per measure, **384** (96 per beat) |
| `CLK_DEF` | int | click (count-in) resolution, 384 |
| `PROGJUDGE_BPM` | float | 240.000 (affects number of hold-judgement ticks: "proportional to hold judgement count") |
| `PROGJUDGE_AER` | float | 0.999 |
| `TUTORIAL` | int | 1 for tutorial tracks |

### Timing lines

| Line | Fields |
|---|---|
| `BPM` | `measure tick bpm` — real tempo change (first must be measure 0 tick 0) |
| `MET` | `measure tick a b` — meter change, cosmetic only (it only changes where the thin measure lines are drawn). **Order caveat**: HackMD documents `METER_HIGH METER_LOW` (numerator first); Suprnova documents the columns as "Second Value, First Value" and stresses that "the values for the time signature are in reverse"; the mgxc2s fork of Margrete2S states that "in c2s, numerator should be placed in front of denominator" and writes `MET measure tick numerator denominator`. Treat the first value as numerator unless a real file contradicts it |
| `SFL` | `measure tick duration multiplier` — scroll-speed ("soflan") multiplier with 6 decimals, negative allowed (board moves backwards); purely visual |
| `DCM` | `measure tick duration speed` — per-note drop-speed segment written by Margrete2S for `SPDMOD` (used in newer charts) |

### Note lines

Common prefix: `TYPE measure tick cell width` where `measure` ≥ 0, `tick` in `[0, RESOLUTION)`, `cell` 0–15 = leftmost cell, `width` 1–16 cells to the right (`cell+width ≤ 16`).

| Type | Extra fields | Meaning |
|---|---|---|
| `TAP` | – | tap |
| `CHR` | `effect` (`UP`, `DW`, `CE`; Margrete2S also `LC RC LS RS BS`) | EX-TAP ("ex-note") with effect direction |
| `FLK` | `L` | flick (always `L`, direction-agnostic) |
| `MNE` | – | mine / damage |
| `HLD` / `HXD` | `length` [ `effect` ] | hold (`HXD` = EX hold in newer versions, `HLD` normal) |
| `SLD` / `SLC` (also `SXD`, `SXC` for EX slides) | `length endCell endWidth` [ `SLD` ...] | slide segment: `SLD` = visible node (draws a note), `SLC` = control segment (no extra note); a slide starting with a straight segment begins with `SLD`, one starting in motion with `SLC`; **a slide ends at an `SLD` located where another slide currently is with nothing following**; width interpolates start→end width |
| `AIR`, `AUR`, `AUL`, `ADW`, `ADR`, `ADL` | `target` | air notes (up / up-right / up-left / down / down-right / down-left); `target` = note type of the parent at the same time/cell (`TAP`,`CHR`,`HLD`,`SLD`,`FLK`…) |
| `AHD` (`AHX` for no-action end) | `target length` | air-hold; ends with an automatic down |
| `ASD` / `ASC` | `target height length endCell endWidth endHeight color` | air-slide node / control (newer versions; Margrete2S output) |
| `ALD` | `dense height length endCell endWidth endHeight color` | air-crush / air-trace lines |

Ticks and lengths are all expressed in `RESOLUTION` parts per measure (length = duration in ticks). Offsets for sub-beat positions: `tick = beat_index·(R/4) + fraction·(R/4)`; with R = 384 a beat is 96 ticks, a 1/16 is 24 ticks. Air notes must be placed at the same measure/tick/cell/width as their parent note ("leech"); the Margrete2S writer enforces it. `AIR`s should be placed at note ends rather than mid-slide, which official charts sometimes do anyway.

### Footer

Statistics, ignored by the game (Suprnova: "do not seem to influence the functionality"): `T_REC_{TAP,CHR,FLK,MNE,HLD,SLD,AIR,AHD,ALL}`, `T_NOTE_*`, `T_NUM_*` (+ `T_NUM_AAC`), `T_CHRTYPE_{UP,DW,CE}`, `T_LEN_{HLD,SLD,AHD,ALL}` (ms), `T_JUDGE_*` (unknown), `T_FIRST_MSEC/T_FIRST_RES`, `T_FINAL_MSEC/T_FINAL_RES`, `T_PROG_00 … T_PROG_95` (20 values, step 5, unknown).

## Timing model

Position = (measure, tick) with `RESOLUTION` ticks per measure (384; always 4 beats per measure regardless of `MET`). Tempo from `BPM measure tick bpm` lines; convert with `time = Σ segments (Δticks / R · 4 · 60/bpm)`. `MET` and `BPM_DEF`/`MET_DEF` are cosmetic. `SFL`/`DCM` only change drawing speed, never judgement time. There is **no audio offset** in the file (audio sync is handled by the game data / `Music.xml`, simulators add `BGMOFS`).

## Notes

See the table above. Simultaneous notes: same measure/tick on different cells. Slides are chains of lines sharing the end position of one segment as the start of the next; air/air-hold lines are dependants. Mines are `MNE`. There are no keysounds.

## Audio & images

Not referenced: audio, jacket, title and levels are in the game's `Music.xml`/asset tree. For simulators the `.ugc`/`.sus` formats include `BGM`, `JACKET` fields.

## Versions & variants

`VERSION` lines seen: `1.08.00`, `1.11.00` (Margrete2S output), with additions between (EX hold/slide `HXD/SXD`, air-slide `ASD/ASC`, `ALD`, `DCM`). The hackmd page describes an older dialect: `AIR` family with `TYP MASTER` (target), `AHD TYP MASTER LENGTH`, `SLC` "slide chain", `CHR [DIRECTION]`, and `DIFFUCLT` (sic) header spelling.

## Quirks & pitfalls

- Fields must be tab-separated; trailing `PROGJUDGE_AER` has two leading spaces in output (`  0.999`) in Margrete2S — whitespace is not meaningful but tabs are.
- Suprnova's example uses `RESOLUTION 386` in prose (typo for 384).
- `MET` argument order is described inconsistently by the sources (see the table).
- `SFL` multiplier must have six decimals (Suprnova). For per-note speed (`DCM`) mgxc2s notes the game cannot take speed `0`; use e.g. `0.00001`.
- Every `AIR`/`AHD` must have a parent at the same position, otherwise the note is ignored or the game may refuse the chart [inference from the "leech" description].
- Charts must satisfy CHUNITHM regulations (Margrete has an automatic regulation checker per its docs); `cell+width` > 16 is invalid [inference].

## Example

From Suprnova's Chunithm-Research ("recreation of the MASTER chart of Cyaegha", excerpt; fields tab-separated in the original):

```
TAP	8	0	6	4
TAP	8	0	12	4
SLC	8	96	4	4	7	3	4
TAP	8	96	10	4
SLC	8	103	3	4	10	2	4
SLD	8	148	0	4	236	0	4
AHD	9	0	0	4	SLD	192
CHR	9	0	4	8	CE
AIR	9	0	4	8	CHR
```

## ROX support

Not read by ROX 0.8.1 (no chunithm codec). Mapping to ROX would need a 16-column model with width collapsed to column ranges; slides/air are not representable.

## Parsers & tools

- [AsakuraMizu/mgxc2s](https://github.com/AsakuraMizu/mgxc2s) / [sbga-tech/mgxc2s](https://github.com/sbga-tech/mgxc2s) (C#, writes c2s; source of the newer note IDs)
- Margrete2S / Margrithm (<https://margrithm.girlsband.party/>)
- MuNET-OSS ChuChartManager (UGC ↔ C2S, C#)
- UMIGURI + Margrete (inonote) for `.ugc`; Suprnova research notes; adzen/chu2view (score viewer, not a parser)

## Getting samples

- **Committed**: 3 file(s) in [`samples/`](samples/) (see samples/SOURCES.md for origin, author and licence of each).
- **Manifest**: 4 entries in `samples.manifest.json` (downloaded by `tools/fetch-samples.sh` into `samples-local/`; listed in [`samples/SOURCES.md`](samples/SOURCES.md))
- **More samples**: official `.c2s` files sit in the CHUNITHM data (not collected); MuNET-OSS/MuConvert (LGPL-3.0) keeps a test set with four official charts (listed in the manifest) and three community-made ones (committed), including a UTF-16LE-with-BOM file (VERSION 1.08.00) and versions 1.10.01, 1.11.00 and 1.14.00. UMIGURI/Margrete (`.ugc`/`.mgxc`) charts can be converted to c2s with MuConvert or Margrete2S (see Parsers & tools).

## Sources

- <https://github.com/Suprnova/Chunithm-Research/blob/main/Charting.md> (read)
- <https://hackmd.io/@BBk8NLCQRziqXVLr1VX_qA/HkJocOmdX> (read)
- <https://github.com/sbga-tech/mgxc2s> README + `Margrete2S/Parser.cs`, `Notes.cs` (read)
- <https://github.com/MuNET-OSS> (search snippet)
