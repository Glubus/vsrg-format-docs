# Sliding Universal Score (SUS) (`.sus`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text

## Overview

SUS (Sliding Universal Score; originally "SeaUrchin Score", the format of the Seaurchin player) is a plain-text, BMS-inspired chart format. This page covers the Project SEKAI dialect, from YumYummity's "SUS Format Specification for PJSK" gist (from testing, "somewhat inaccurate") and the sus-io keywords (pjsekai, chunithm, seaurchin). The generic SUS 2.7 spec (waki285's gist) could not be fetched, so Chunithm/Seaurchin-only note types (hold, air) are missing. Used by PJSK custom chart editors (MikuMikuWorld, MMW4CC, UntitledChartingStudio), Chart Cyanvas, Sonolus converters and hololive Dream (own extended SUS).

## Container & encoding

Plain text, UTF-8, CRLF or LF; extension `.sus`. Lines starting with `#` are data; everything else is a comment. Strings use double quotes. One file = one difficulty.

## Structure / metadata

Metadata lines (ignored by PJSK, which takes metadata from its master data): `#TITLE "..."`, `#ARTIST "..."`, `#DESIGNER "..."`, and `#REQUEST "ticks_per_beat 480"` (the only one that matters: ticks per beat, default 480).

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

Special data lines: `#mmm02: <beats>` beats in the measure (PJSK requires exactly `#mmm02: 4`); `#BPMzz: <float>` define a BPM, `#mmm08: <zz...>` place BPM changes referencing definitions (the `zz` after `BPM` must be uppercase); `#ATRzz: "rh:<float>, h:<float>, pr:<int>"` attribute sets + `#ATTRIBUTE zz` / `#NOATTRIBUTE`; `#TILzz: "meas'tick:speed, ..."` hi-speed definitions + `#HISPEED zz` / `#NOSPEED`; `#MEASUREHS zz`.

## Timing model

Measures are divided into data slots. Ticks per beat come from `#REQUEST` (default 480, so a 4/4 measure = 1920 ticks). A slot position in the measure is `slot_index / slots_per_measure`. BPM changes use `#BPMzz` + `#mmm08`. Hi-speed (`#TIL`) is a note-scroll speed map in `measure'tick:speed` form (negative speeds allowed), applied to notes following `#HISPEED`. PJSK supports one time signature (4/4).

## Notes

- Tap family `#mmm1x:` (first char of each pair): `1` Tap, `2` Critical tap, `3` Flick (only to attach slide relays), `4` Skill activation (damage note; lane 0, width 1), `5` Trace, `6` Critical trace, `7` Elaser (hides slide start/end judgment), `8` Critical elaser. Fever start/end: normal/critical tap on lane `f`, width 1.
- Slides `#mmm3xy:` (same channel `y` connects): `1` start, `2` end, `3` relay (visible), `4` Bezier control (not verified for PJSK), `5` relay (invisible). Widths can change per point.
- Directionals `#mmm5x:` sit on top of another note: `1` up, `2` down, `3` left-up, `4` right-up, `5` left-down, `6` right-down (several unverified for PJSK).
- Guides `#mmm9xy:` (decorative slides): `1` start, `2` end, `5` relay (invisible).
- Overlaps (other objects on the same left-most lane) set attributes: directionals give flick direction; tap overlaps give critical/trace/none judge types on slides; `RIGHT_DOWN` gives ease-out and `DOWN` ease-in on slide steps (none = linear), plus a tap `1` on relay points; flick+tap makes a slide attach relay; guide colour is yellow when each guide step has a critical elaser, green with plain elaser. Overlapped tap notes outside slides/guides produce misses.

## Audio & images

None. PJSK takes audio from master data; the offset lives outside the SUS or in the editor.

## Versions & variants

- SUS 2.7 generic (Seaurchin/Chunithm) vs the PJSK dialect (post 3rd anniversary, per the gist).
- hololive Dream has its own dialect (rg_converters: loading only). `rg_converters` reads `.sus` "with some extensions", plus `.mmws`, `.ccmmws`, `.unchmmws`. `susToUSC` converts to USC.

## Quirks & pitfalls

- Measure numbers are 3 digits: measures >= 1000 impossible.
- The `#BPMzz` index is case-sensitive uppercase, for BPM only.
- Overlap semantics (flick/critical/ease via stacked notes) compare only the left-most lane, even for different note types.
- Overlapped tap notes (not meant as overlaps) cause misses even in autoplay.
- Elaser notes hide the judgement of slide ends/starts.

## Example

From the PJSK spec gist:

```text
#REQUEST "ticks_per_beat 480"
#00002: 4
#BPM01: 140.0
#00008: 01
#00010: 2414141434141414
```
Last line: measure 000, tap-family type 1 at lane 0, 8 slots; each pair is kind+width, e.g. `24` = critical tap of width 4, `14` = tap of width 4, `34` = flick of width 4.

## ROX support

Decode only, `rox::formats::sekai` (`SusDecoder`, `DetectedFormat::Sus`). One chart per file, always 12 columns: SUS lanes `x = 2..=13` are columns 0..=11, lanes 0, 1, 14, 15 are off the stage, `f` with width 1 is the fever marker. A wide note is one note on its leftmost column.

- Tap and critical tap are taps (critical dropped and counted); a tap with a directional overlapped is a counted flick.
- A slide (`#mmm3xy`, points paired by channel `y`, cut after each end) is one hold from first to last point on the first column; middle points and their overlaps (critical, trace, elaser, flick-attach, easing) are dropped and counted.
- Traces, skill activations (kind `4`), fever markers, guides (`#mmm9xy`) and bare overlays are dropped and counted, never taps. SUS 2.7 holds (`#mmm2xy`) and Chunithm slides 2 are counted, not read.
- Timing: `#mmm02` sets the measure length (4 before the first); `#BPMzz` / `#mmm08` the tempo (case-sensitive id; the first BPM also holds before it); `#MEASUREBS` adds to measure numbers; `#REQUEST "ticks_per_beat n"` does not change times; `#WAVEOFFSET s` (positive makes the chart start first) shifts times by `-s`.
- Metadata: `#TITLE`, `#ARTIST`, `#DESIGNER`, `#DIFFICULTY`, `#PLAYLEVEL` (`+` adds 0.5), `#GENRE`, `#BACKGROUND`, `#WAVE`.
- Prism (`docs/game.md` "Project SEKAI"): the scan keeps a `.sus` when its first bytes are text with a `#` line (`rox::formats::looks_like_sus`; a Chunithm `.sus` passes and reads as Project SEKAI). Sound: `#WAVE`, else the audio named like the chart, else the first in the folder, else silent and marked missing audio. Refused as `Unsupported layout: 12K` (no 12-column layout in the catalog).

Decisions: `rox::formats::sekai` `mod.rs`; tests `sekai/tests.rs`. Read for this: SUS 2.7 spec (kb10uy's gist, Japanese; English copy by waki285: `#WAVE`, `#WAVEOFFSET`, `#MEASUREBS`, `#DIFFICULTY`, `#PLAYLEVEL`), `sonolus-pjsekai-engine` `lib/src/sus/{analyze,convert}.ts` (MIT), `sus-js` `sus-parse` (MIT). No real `.sus` was decoded.

## Parsers & tools

- sus-io / sus-stringify (TypeScript): <https://github.com/mkpoli/sus-js>, <https://www.npmjs.com/package/sus-io>; sus-io (Python): <https://pypi.org/project/sus-io/>
- Sonolus PJSekai engine `susToUSC` (TypeScript): <https://github.com/NonSpicyBurrito/sonolus-pjsekai-engine>
- rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>
- susc-converter: <https://github.com/Kyonkrnk/susc-converter/>

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

- Official PJSK charts: `https://storage.sekai.best/sekai-jp-assets/music/music_score/<4-digit id>_01/<easy|normal|hard|expert|master|append>.txt` (also `-en-`, `-kr-`, `-tc-`, `-cn-` region prefixes in `chart-downloader`'s `sb.py`). Fan charts: Chart Cyanvas / Untitled Charts (untitledcharts.com, via UntitledCharts/chart-downloader). Editors: MikuMikuWorld and forks, Ched.
- [observed: ournotes-jp_performance_music_expert.sus] BanG Dream! Our Notes development SUS adds `#LANECOUNT 24` (28 in the `short_music_*` files) and channels such as `#00177: 11` / `#001sk: 11`. The 12-lane assumption holds only for Project SEKAI.
- [observed: sekaibest_0001_01_easy.sus] sekai.best files carry empty `#TITLE ""` metadata and `#TIL00: ""`.

## Sources

- <https://gist.github.com/YumYummity/49935bf74367712b6ba240474cb7ce22> (raw markdown fetched: sus-specification-pjsk.md)
- <https://www.npmjs.com/package/sus-io>
- <https://github.com/UntitledCharts/rg_converters>
- <https://gist.github.com/waki285/dafa254a9de56ba43d177ae0913d4263> (SUS 2.7; listed in search, content not retrievable)
