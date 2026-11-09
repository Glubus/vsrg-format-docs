# Sliding Universal Score (SUS) (`.sus`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text

## Overview

SUS (Sliding Universal Score; originally "SeaUrchin Score", the proprietary format of the Seaurchin player) is a plain-text, BMS-inspired chart format. This page documents the **Project SEKAI dialect** as described by YumYummity's "SUS Format Specification for PJSK" gist (based on testing, "somewhat inaccurate") and the sus-io library keywords (pjsekai, chunithm, seaurchin). The generic SUS 2.7 spec (waki285's gist) could not be fetched, so note types used only by Chunithm/Seaurchin (for example hold and air notes) are not described. Used by: PJSK custom chart editors (MikuMikuWorld, MMW4CC, UntitledChartingStudio), Chart Cyanvas, Sonolus converters, hololive Dream (own extended SUS).

## Container & encoding

Plain text, UTF-8, CRLF or LF; extension `.sus`. Lines starting with `#` are data; everything else is a comment. Strings use double quotes. One file = one difficulty.

## Structure / metadata

Metadata lines (ignored by PJSK; the game takes metadata from its master data) `#TITLE "..."`, `#ARTIST "..."`, `#DESIGNER "..."`, and `#REQUEST "ticks_per_beat 480"` (the only one that matters: sets ticks per beat, default 480).

Data lines: `#mmmcxy: data` (some without `y`, some with a 2-char base-36 `zz` special number):

| Part | Meaning |
|---|---|
| `mmm` | measure number, 000.. (numeric = general data; non-numeric = special data) |
| `c` | note type digit (`1` tap-like, `3` slide, `5` directional, `9` guide, `0` special) |
| `x` | leftmost lane of the note: `0`..`9`, `a`..`z` (base 36, case-insensitive) |
| `y` | channel (`0`..`z`); notes of the same channel are connected; absent for some types |
| `zz` | special number, base-36 `01`..`zz` |
| data | pairs of characters; the measure is split into `len/2` slots; first char of a pair = note kind (0 = none), second char = width `1`..`z` (1..35); `00` = empty |

Maximum divisions: at least 512 slots (1024 chars) must be supported.

Special data lines: `#mmm02: <beats>` beats in the measure (PJSK requires exactly `#mmm02: 4`); `#BPMzz: <float>` define a BPM, `#mmm08: <zz...>` place BPM changes referencing definitions (the `zz` after `BPM` must be **uppercase**); `#ATRzz: "rh:<float>, h:<float>, pr:<int>"` attribute sets + `#ATTRIBUTE zz` / `#NOATTRIBUTE`; `#TILzz: "meas'tick:speed, ..."` hi-speed definitions + `#HISPEED zz` / `#NOSPEED`; `#MEASUREHS zz`.

## Timing model

Measures divided into data slots; ticks per beat from `#REQUEST` (default 480, so a 4/4 measure = 1920 ticks). A slot position in the measure is `slot_index / slots_per_measure`. BPM changes via `#BPMzz` + `#mmm08`. Hi-speed (`#TIL`) is a note-scroll speed map in `measure'tick:speed` form (negative speeds allowed), applied to notes following `#HISPEED`. PJSK supports a single time signature (4/4).

## Notes

Tap family `#mmm1x:` kinds in the first char of each pair: `1` Tap, `2` Critical tap, `3` Flick (only used to attach slide relays), `4` Skill activation (damage note; lane 0, width 1), `5` Trace, `6` Critical trace, `7` Elaser (hides slide start/end judgment), `8` Critical elaser. Fever start/end: normal/critical tap on lane `f`, width 1.

Slides `#mmm3xy:` (same channel `y` connects): `1` start, `2` end, `3` relay (visible), `4` Bezier control (not verified for PJSK), `5` relay (invisible). Widths can change per point.

Directionals `#mmm5x:` placed on top of another note: `1` up, `2` down, `3` left-up, `4` right-up, `5` left-down, `6` right-down (several unverified for PJSK).

Guides `#mmm9xy:` (decorative slides): `1` start, `2` end, `5` relay (invisible).

Overlaps: other objects stacked on the same lane (by left-most lane) set attributes - directionals give flick direction; tap overlaps give critical/trace/none judge types on slides; a directional `RIGHT_DOWN` gives ease-out and `DOWN` gives ease-in on slide steps (no directional = linear), plus a tap `1` on relay points; a flick+tap overlap makes a slide attach relay; guide colour is yellow when each guide step has a critical elaser, green with plain elaser. Overlapped tap notes that are not on slides/guides produce misses.

## Audio & images

None (metadata only; PJSK takes audio from master data; offset lives outside the SUS or via editor).

## Versions & variants

- SUS 2.7 generic (Seaurchin/Chunithm) vs PJSK dialect (post 3rd anniversary, per the gist).
- hololive Dream uses a unique SUS dialect (rg_converters: loading only).
- `rg_converters` supports `.sus` with "some extensions"; also `.mmws`, `.ccmmws`, `.unchmmws` (editor formats).
- Sonolus USC conversion: `susToUSC` in sonolus-pjsekai-engine.

## Quirks & pitfalls

- Measure numbers are 3 digits: measures >= 1000 impossible.
- `#BPMzz` index is case-sensitive uppercase for BPM only.
- Overlap semantics (flick/critical/ease via stacked notes) are positional: only the left-most lane is compared, even for different note types.
- Overlapped tap notes (not meant as overlaps) cause misses even in autoplay.
- Elaser notes hide the judgement of slide ends/starts.

## Example

From the PJSK spec gist (each line below appears in its examples/sections):

```text
#REQUEST "ticks_per_beat 480"
#00002: 4
#BPM01: 140.0
#00008: 01
#00010: 2414141434141414
```
Reading the last line with the rules above: measure 000, tap-family type 1 at lane 0, 8 slots; each pair is kind+width, e.g. `24` = critical tap of width 4, `14` = tap of width 4, `34` = flick of width 4.

## ROX support

Read by ROX since Prism's addition of `rox::formats::sekai` (decode only: ROX does not write SUS): `SusDecoder` (`decode`, `decode_with_report` giving a `SekaiReport`, `decode_with_title`, `decode_file`; `DetectedFormat::Sus`). ONE chart per file, always **12 columns** (SUS lanes `x = 2..=13` are the columns 0..=11; lanes 0, 1, 14 and 15 are off the stage, `f` with width 1 is the fever marker). A wide note is ONE note on its leftmost column. Tap and critical tap are taps (the critical flag is dropped and counted); a tap with a directional overlapped on it is a tap counted as a flick; a slide (`#mmm3xy`, points paired by channel `y` and cut after each end) is ONE hold from its first point to its last on the first point's column, the points between and the overlaps on them (critical, trace, elaser, flick-attach, easing) dropped and counted; traces, skill activations (kind `4`), fever markers, guides (`#mmm9xy`) and overlays with nothing under them are dropped and counted, never taps. Timing: the measure is divided by the number of 2-character slots, `#mmm02` sets the measure length (4 before the first), `#BPMzz` / `#mmm08` the tempo (the id is case-sensitive; the first BPM also holds before it), `#MEASUREBS` adds to the measure numbers, `#REQUEST "ticks_per_beat n"` (480 by default) does not change the times. `#WAVEOFFSET s` (SUS 2.7: a positive value makes the chart start first) moves every time by `-s`. Metadata from `#TITLE`, `#ARTIST`, `#DESIGNER`, `#DIFFICULTY`, `#PLAYLEVEL` (`+` adds 0.5), `#GENRE`, `#BACKGROUND`, `#WAVE`. The generic SUS 2.7 holds (`#mmm2xy`) and slides 2 of Chunithm are counted, not read. Decisions: `rox::formats::sekai` `mod.rs`; tests (every file built by hand): `sekai/tests.rs`.

Read by Prism (`docs/game.md` "Project SEKAI"): the scan keeps a `.sus` only when its first bytes are text with a `#` line (`rox::formats::looks_like_sus`; a Chunithm `.sus` passes and is read as a Project SEKAI chart); the sound is `#WAVE`, else the audio file with the chart's own name, else the first of the folder; no sound: the chart is kept, marked as missing its audio and played silent. **No 12-column layout exists in the catalog yet**: the chart is refused by the scan as `Unsupported layout: 12K` (like a BMS double play) until one does.

Sources read for this: the SUS 2.7 specification (kb10uy's gist, in Japanese, and its English copy by waki285: `#WAVE`, `#WAVEOFFSET`, `#MEASUREBS`, `#DIFFICULTY`, `#PLAYLEVEL`), `sonolus-pjsekai-engine` `lib/src/sus/{analyze,convert}.ts` (MIT), `sus-js` `sus-parse` (MIT). No real `.sus` was decoded.

## Parsers & tools

- sus-io / sus-stringify (TypeScript): <https://github.com/mkpoli/sus-js>, <https://www.npmjs.com/package/sus-io>; sus-io (Python): <https://pypi.org/project/sus-io/>
- Sonolus PJSekai engine `susToUSC` (TypeScript): <https://github.com/NonSpicyBurrito/sonolus-pjsekai-engine>
- rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>
- susc-converter: <https://github.com/Kyonkrnk/susc-converter/>

## Sources

- <https://gist.github.com/YumYummity/49935bf74367712b6ba240474cb7ce22> (raw markdown fetched: sus-specification-pjsk.md)
- <https://www.npmjs.com/package/sus-io>
- <https://github.com/UntitledCharts/rg_converters>
- <https://gist.github.com/waki285/dafa254a9de56ba43d177ae0913d4263> (SUS 2.7; listed in search, content not retrievable)
