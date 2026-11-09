# hololive Dream "holodori" SUS dialect (`.sus`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg (12-lane vertical highway, Project SEKAI-style) · Encoding: text

## Overview

**hololive Dream** (hololive production's mobile rhythm game, Project SEKAI-like) uses a **dialect of the Sliding Universal Score (SUS) text format** ([`../sus`](../sus/README.md)) for its charts. It keeps the SUS skeleton (`#MMMCC:data` lines, 12 lanes, bar lengths) but changes how each line's data is encoded and adds game-specific channels (hi-speed `NMS`, skill points, fever/charge sections, ghost notes). It is documented only by the loader of `UntitledCharts/rg_converters` (`cpp/src/converters/holodori_sus/loader.cpp`, described there as "a sekai-sus dialect decoded off the game's SusConverter"), which supports it as "Loading-Only". This page lists what that loader reads; behaviours the game has beyond it are unknown.

## Container & encoding

Plain text, one directive per line, lines starting with `#` are interpreted; leading/trailing whitespace stripped. Charset not stated (ASCII-compatible). The same `.sus` extension as the PJSK SUS: distinguish by the data cell syntax and the extra directives.

## Structure / metadata

### Directives

| Line | Meaning |
|---|---|
| `#MUSIC_ID <id>` | Song id (quotes stripped). |
| `#WAVEOFFSET <seconds>` | Audio offset (float). |
| `#BASEBPM <bpm>` | Default tempo used when a `#BPMxx` definition is missing (default 120). |
| `#SP_SKILL mmm num/den slot` | Legacy skill-point line: measure `mmm`, position `num/den` within the measure, deck slot number. |
| `#BPMxx <bpm>` | Tempo definition with 2-character id `xx` (the id is the two characters after `BPM`, used as a map key). |
| `#NMSxx <multiplier>` | **NMS (hi-speed) definition**: scroll multiplier with id `xx`. |
| `#COLORwwww <rgba>` | Colour definition (8 hex digits incl. alpha) for ghost notes; `wwww` = 4-hex id. |
| `#mmm02:<length>` | Bar length of measure `mmm` (beats; default 4), as in SUS. |

### Data lines

Header form `#mmmXY` + `:` + data, where `mmm` is the 3-digit measure, `X` the **event type** (hex/base-36 digit), `Y` the **lane character** (base-62 style, case-sensitive: `0-9`, `a-z` = 10-35, `A-Z` = 36-61).

| Event `X` (and header) | Meaning |
|---|---|
| `08` (`#mmm08`) | Tempo changes: each non-`00` cell is a `#BPMxx` id. |
| `0A` | Hi-speed changes: each non-`00` cell is a `#NMSxx` id. |
| `0B` | Skill activation: each cell is a deck slot number (1-5). |
| `0C` / `0D` | Fever sections: lane char `C` -> charge (`1` start, `2` end); lane char `D` -> fever (`1` start, `2` end). The game "drops the whole section unless it has exactly one of each point, in order" (chargeStart <= chargeEnd <= feverStart <= feverEnd). |
| `1l` | Tap channel for lane `l`. |
| `5l` | Directional channel for lane `l` (flicks and slide ease markers). |
| `3lc` (`#mmm3lc:`) | Long-note (slide) channel: lane `l`, channel `c` (base-36) which groups the segments of one slide. |
| `9lc` + 4-hex colour id | Ghost (decorative) notes with colour (header shape `mmm`, event char, lane char, channel char, 4 hex digits; the source comment says the event char is `9`). |

### Data encoding

A data string is a grid of **positions** within the measure. Two forms of token:

- A 2-character cell `kw` = `kind` (char 0) and `width` (char 1), each base-62; `kind == 0` means "empty". One cell advances the position by 1.
- `0x` + 2 characters (base-62, `d1*62 + d2`): a **run of that many empty positions** (compression). Total positions = final position count; a note's fractional position within the measure = `position / total`.

For the meta lines (`08`, `0A`, `0B`, `0C`, `0D`) the cell is read as a 2-char id/value (only `00` is empty; `05` is id 5), so they use a slightly different cell reading from note lines.

### Note kinds

Tap channel (`1l`): kind `1` normal tap; kind `2` = critical (as a co-located modifier or a standalone critical tap); kind `3` = "step ignore" marker (a relay marked this way is an `attach`, not a shape point); kind `6` also marks critical. Directional channel (`5l`): kind `1` flick up, `3` flick left, `4` flick right; `2`, `5`, `6` are **slide ease markers** (`2` ease-in; `5`/`6` ease-out). Long channel (`3lc`): kind `1` start, `2` end, `3` relay active (visible, combo), `4` bezier point, `5` relay deactivated (hidden, shape, no combo); a start is matched to the oldest open start ahead of its end (FIFO), relays between them are attached, unmatched ends are dropped, exact duplicate points removed (the dense encoding repeats points).

## Timing model

Positions are fractional (`position / total`) inside bars; ticks derive from bar lengths (`TICKS_PER_BEAT = 480` shared with the PJSK SUS code; "the file's ticks_per_beat is ignored"). Tempo from `#BPMxx` + channel `08`; hi-speed from `#NMSxx` + `0A` (a single hi-speed layer); audio offset from `#WAVEOFFSET`.

## Notes

Taps, critical taps, directional flicks, slides with relays and ease/bezier markers, ghost notes (decorative, colour from `#COLOR`), skill points, fever/charge sections. Lanes are positions on a 12-lane board (`MIN_LANE`..`MAX_LANE` of the shared SUS code).

## Audio & images

`#MUSIC_ID`, `#WAVEOFFSET` only.

## Versions & variants

Not applicable (single dialect known). The PJSK variant of SUS (`../sus`) uses its own `#MMMTL:` syntax; the converter selects the loader by option, not by file contents. [inference from separate loader entry points]

## Quirks & pitfalls

- Base-62 case-sensitive characters (`a-z` and `A-Z` differ).
- `0x` runs compress empties; a parser that treats `0x` as a note kind misreads them.
- Slides are split over several lines/channels; matching is by position, not by an explicit id.
- Bezier pull information is lost when converting to a PJSK-like model.
- The fever section is only accepted when complete and ordered.

## Example

Illustrative, hand-built from the cell rules above: measure 1, lane 5 tap channel, 8 positions, taps at positions 0 and 4:

```
#00115:110x03110x03
```

(cells `11` = kind 1 width 1; `0x03` = 3 empty positions; totals 1 + 3 + 1 + 3 = 8 positions.)

## ROX support

Not read by ROX. 12-lane board with wide notes, flicks, slides with eases/beziers, skill/fever events.

## Parsers & tools

`rg-converters` (C++/Python): https://github.com/UntitledCharts/rg_converters (`cpp/src/converters/holodori_sus/loader.cpp`, loading only).

## Sources

- https://github.com/UntitledCharts/rg_converters (commit `673710dcc441aea97ac89e113f811d5c169763d4`): `README.md`, `cpp/src/converters/holodori_sus/loader.cpp`, `cpp/include/rg/converters/sus_common.hpp`
