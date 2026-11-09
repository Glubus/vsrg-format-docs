# Fumen (`.bin`, official Taiko no Tatsujin chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (little- or big-endian, fixed-size records, no compression/encryption at this level)

## Overview

"Fumen" (譜面, chart) is the binary chart format used by the official Bandai Namco games: arcade (Taiko no Tatsujin AC, PC-generation boards), console ports (Wii/PS2/PS3/PS4/Switch), and the PC game "Taiko no Tatsujin: The Drum Master" (Steam, `TDMX`). One file = **one difficulty** (and, for diverge charts, the three branches inside the same file). Files are named `<songid>_<course>.bin` with course letters `e` Easy, `n` Normal, `h` Hard, `m` Oni, `x` Ura (Edit), plus `_1`/`_2` style suffixes for 2-player/Double variants (see `COURSE_IDS` in tja2fumen; the `_n_2.bin` example appears in the TaikoMods README). In console/PC builds the `.bin` files are normally stored inside encrypted/packed archives; only the **plaintext/unencrypted** `.bin` is described here. The format was reverse engineered by the community (KatieFrogs' `fumen-tools`, then vivaria's **tja2fumen**; OpenLibTaiko documents the "Ver2" layout).

Category: **others** — same reasoning as [TJA](../tja/README.md): one horizontal track, two drum colours, scroll-speed gimmicks, branches.

## Container & encoding

- Fixed layout: `520`-byte header, then `measure_count` measures; each measure = 40-byte measure header + **three** branch blocks (Normal, Professional, Master) each = 8-byte branch header + `N` note records. A non-branching chart stores the notes in the Normal block and empty (0-note) Professional/Master blocks (the header flag below says whether branches exist).
- **Endianness**: both byte orders exist in the wild; parsers autodetect: read the `u32` at offset 512 (measure count) as little and big endian and take the smaller value (tja2fumen); OpenLibTaiko probes `0..300` as plausible and prefers little-endian. Which platform uses which order is not stated in the sources opened. tja2fumen's `FumenHeader.order` defaults to `<` (little-endian) when writing.
- Times are **float32 milliseconds**, BPM is float32. No time signature field exists: measure length is derived from BPM and, for non-4/4 or sub-measures, is baked into the next measure's offsets.
- No magic number, no checksum. One known official file runs out of data early (AC11 `deo_n.bin`); tja2fumen zero-pads.

## Structure / metadata

### Header (520 bytes, `0x208`)

| Offset | Type | Field (tja2fumen name) |
|---|---|---|
| 0–431 | 108 × f32 | timing windows: 36 triples (GOOD, OK, BAD) in ms. Easy/Normal triple = `41.7083, 108.4417, 125.125`; Hard/Oni = `25.025, 75.075, 108.4417` (tja2fumen writes the triple 36 times) |
| 432 | i32 | has_branches flag |
| 436 | i32 | `hp_max` (default 10000) |
| 440 | i32 | `hp_clear` (soul threshold; tja2fumen: Easy 6000, Normal/Hard 7000, Oni 8000) |
| 444 / 448 / 452 | i32 | `hp_gain_good`, `hp_gain_ok`, `hp_loss_bad` (defaults 10, 5, −20; tja2fumen looks them up per note count/level) |
| 456 / 460 / 464 | i32 | `normal_normal_ratio`, `normal_professional_ratio`, `normal_master_ratio` (default 65536 = 1.0 in 16.16) |
| 468 / 472 / 476 | i32 | branch points GOOD / OK / BAD (defaults 20, 10, 0) |
| 480 | i32 | branch points per drumroll hit (default 1) |
| 484 / 488 | i32 | branch points GOOD-big / OK-big (20, 10) |
| 492 | i32 | branch points per big drumroll hit (1) |
| 496 / 500 | i32 | branch points balloon / kusudama (30, 30) |
| 504 | i32 | branch points "unknown" (20) |
| 508 | i32 | dummy (12345678 in tja2fumen) |
| 512 | i32 | **number of measures** |
| 516 | i32 | unknown |

OpenLibTaiko's field names for the same bytes: `0x000–0x1AF` 108 timing floats, `0x1B0` branch-present flag, `0x1B4` HP max, `0x1B8` clear threshold, `0x1BC/0x1C0/0x1C4` Good/OK/Bad gauge change, `0x1C8/0x1CC/0x1D0` Normal/Professional/Master ratio, `0x1D4–0x1FB` ten BranchPoint values, `0x1FC` dummy, `0x200` measure count, `0x204` unknown.

### Measure (40-byte header)

`f32 bpm; f32 offset (ms); u8 gogo; u8 barline; u16 padding; i32 branch_info[6]; i32 padding` (struct `ffBBHiiiiiii`).

- `offset` is the measure start in ms, **biased backwards by one full 4/4 measure at the current BPM**: `play_start = offset + 240000 / bpm` (OpenLibTaiko) — equivalently tja2fumen sets the first measure's offset to `−OFFSET·1000 − 240000/bpm` and later ones to `prev.end + delay + 240000/prev.bpm − 240000/bpm`.
- `gogo`: Go-Go Time active; `barline`: show the bar line (official files contain empty measures used only for visual bar lines).
- `branch_info[6]`: three pairs (for the Normal, Professional, Master branch respectively) = thresholds in "branch points" to move to Professional and to Master from that branch. Conventions used by tja2fumen: `999` = unreachable (also used for `#LEVELHOLD`: Normal `[999,999]`, Professional `[0,999]`, Master `[0,0]`), `0` = always passes; `#BRANCHSTART p,a,b` → `int(total_points·a)` etc. (percentages ≤ 1), `#BRANCHSTART r` → raw drumroll-hit counts.
- Measure length in time = `240000/bpm` for a 4/4 measure; tja2fumen scales it by `n/d` for `#MEASURE n/d` and by the fraction of the measure covered for sub-measures created by mid-measure commands.

### Branch block (8 bytes) then notes

`u16 total_notes; u16 padding; f32 speed` (struct `HHf`). `speed` is the scroll multiplier (`#SCROLL`) of that measure/branch.

### Note record (24 bytes; struct `ififHHf`)

| Offset | Type | Meaning |
|---|---|---|
| 0 | i32 | note type (table below) |
| 4 | f32 | position inside the measure, ms from measure start (`measure_duration × position ratio`) |
| 8 | i32 | "item" (unknown; present in all notes) |
| 12 | f32 | padding |
| 16 | u16 | `score_init` for ordinary notes; **hit count** for balloon (0xA) and kusudama (0xC) |
| 18 | u16 | `score_diff × 4` (tja2fumen divides by 4); padding for balloons |
| 20 | f32 | duration in ms for rolls/balloons (tja2fumen truncates to int) |

Types `0x06`, `0x09` and `0x62` (drumroll-like) are followed by **8 extra bytes** (`drumroll_bytes`), making their record 32 bytes (OpenLibTaiko: types `0x06`, `0x09`, `0x62`; "known types").

### Note types

| Value | Meaning (tja2fumen `FUMEN_NOTE_TYPES`) |
|---|---|
| `0x01` | Don (ドン) |
| `0x02` | Don2 (ド) |
| `0x03` | Don3 (コ) |
| `0x04` | Ka (カッ) |
| `0x05` | Ka2 (カ) |
| `0x06` | Drumroll |
| `0x07` | DON (big) |
| `0x08` | KA (big) |
| `0x09` | DRUMROLL (big) |
| `0x0A` | Balloon |
| `0x0B` | DON2 (hands, multi-player) |
| `0x0C` | Kusudama |
| `0x0D` | KA2 (hands) |
| `0x0E`, `0x0F`, `0x10`–`0x19`, `0x22`, `0x62` | unknown: `0x0E, 0x10, 0x11, 0x13, 0x15, 0x16, 0x22` seen in some Wii1 songs; `0x0F, 0x14, 0x18, 0x19` PS4; `0x12, 0x17` Wii4; `0x62` "Drumroll2 (?)" |

The don/ka *variants* (`0x01`–`0x03`, `0x04`–`0x05`) differ only in the voice ("note phoneticization", e.g. ド/コ/ドン) — which TJA expresses with `#SENOTECHANGE`. OpenLibTaiko's grouping for gameplay: Don = `0x01,0x02,0x03,0x07`; Ka = `0x04,0x05,0x08`; roll = `0x06,0x09`; balloon-family = `0x0A,0x0C`; factory-supported IDs `0x01..0x1E`.

## Timing model

Time-in-measure floats in ms, absolute time of a note = `measure.offset + 240000/measure.bpm + note.pos` (equivalently `play_start + pos`). BPM changes are expressed by giving each measure its own BPM; a `#BPMCHANGE` in the middle of a TJA measure forces tja2fumen to split it into sub-measures (with `barline=false` for non-initial pieces). `#DELAY` is folded into the next measure's offset. There are no stops/warps. Branch blocks share the same time frame.

## Notes

Don/Ka/DON/KA (0x01–0x08, 0x0B, 0x0D), rolls (0x06/0x09 with duration), balloons (0x0A) and kusudama (0x0C) with hit counts. No keysounds. Branch variations are different note lists in the three branch blocks of the same measure. TJA letters `C`–`I` have no direct fumen equivalent in tja2fumen (replaced by normal notes/rolls).

## Audio & images

Not in the chart. Audio is a separate resource (NUS3BANK in older games, CRIWARE ACB/HCA in the PC game; TakoTako/TJAConvert produce unencrypted HCA-in-ACB). Song metadata (title, stars, genre) lives in separate databases (`musicinfo`, `wordlist`) of the games [not opened].

## Versions & variants

- OpenLibTaiko calls the described layout "Ver2" (`CFumen::Parse`, reconstructed core of an official engine). Older/other console layouts are not documented in the sources opened.
- Unknown note types differ by platform (Wii, PS4...), suggesting additional types for minigames/Taiko Tower; they are preserved by tja2fumen but not interpreted.

## Quirks & pitfalls

- Detect endianness first; the measure count is the discriminator.
- Do not rely on `total_notes` bounds across file end (official file truncation).
- Roll records are longer (32 bytes) — mandatory when skipping unknown notes.
- `score_diff` is stored ×4; balloon hit counts reuse the score field.
- Offsets are *biased by one measure*; ignoring it shifts the chart by `240000/bpm` ms.
- Empty measures carry only a barline.
- Per-note timing already has measure length baked in: no time-signature field to read.
- The tja2fumen repository moved to <https://gitea.tendokyu.moe/vivaria/tja2fumen> (GitHub copy archived) after DMCA concerns around Bandai Namco modding tools; the code deals only with unencrypted files.

## Example

No byte dump is reproduced (official files are copyrighted). Layout of the smallest valid chart as implied by the structs above (illustrative, hand-built from the rules above): 520 header bytes with `measure_count = 1` at offset 512, then 40 bytes of measure header, then three 8-byte branch headers (`HHf` = 0 notes for Professional/Master) and, in the Normal block, one 24-byte note record `type=1, pos=0.0, item=0, pad=0.0, score_init, score_diff*4, duration=0.0`.

## ROX support

Not read by ROX 0.8.1 (no fumen codec in `src/formats`).

## Parsers & tools

- [vivaria/tja2fumen](https://github.com/vivaria/tja2fumen) / [Tendokyu mirror](https://gitea.tendokyu.moe/vivaria/tja2fumen) — Python; `parse_fumen`, `write_fumen`, `convert_tja_to_fumen` (MIT)
- [KatieFrogs/fumen-tools](https://github.com/KatieFrogs/fumen-tools) — Python `fumen2osu.py` (`readFumen()`), original parser tja2fumen is based on
- [cainan-c/OpenLibTaiko](https://github.com/cainan-c/OpenLibTaiko) — `docs/FUMEN_FORMAT.md`, C++ `CFumen::Parse`
- [Fluto/TakoTako](https://github.com/Fluto/TakoTako) (BepInEx mod for the PC game, includes TJAConvert + `tja2bin`), [goaaats/TaikoMods](https://github.com/goaaats/TaikoMods)

## Getting samples

Committed in [`samples/`](samples/): 30 real fumen `.bin` files in four sets (`tja2fumen_butou5`, `_hol6po`, `_linda`, `_senpac`), extracted from the zips of the tja2fumen test data (no archive kept). The matching `.tja` files are in [`../tja/samples/`](../tja/samples/). See [`samples/SOURCES.md`](samples/SOURCES.md) for every file's source URL, fetch date, sha256 and terms. Filenames follow `<id>_<e|n|h|m|x>[_1|_2].bin` (easy/normal/hard/oni/ura; `_1`/`_2` per player) [observed in samples/]. More: dump the official game data (see Parsers) or run `tja2fumen` on a `.tja`.

## Sources

- <https://github.com/vivaria/tja2fumen> (README, `src/tja2fumen/parsers.py`, `classes.py`, `constants.py`, `converters.py` — read)
- <https://raw.githubusercontent.com/cainan-c/OpenLibTaiko/main/docs/FUMEN_FORMAT.md> (read)
- <https://github.com/goaaats/TaikoMods> (search snippet: file names `[MUSIC_ID]_n_2.bin`, `[MUSIC_ID]_x.bin`)
- <https://iepiweidieng.github.io/TJAPlayer3/tja> (formats table: `.bin` "Proprietary format, first release 2001-02-21 (AC1)")
