# PhiEdit Chart (PEC) (`.pec`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview

PEC (PhiEdit Chart) is the plain-text chart format of the older Phigros chart editor **PhiEdit** (by the same community as RPE). It does not store metadata (title, composer...). The Phira docs state the format is no longer updated; PhiEdit allows at most 30 judgement lines and no X/Y split. Still read by Phira and several players.

## Packaged in

- Packaged in [`pez`](../pez/).

## Container & encoding

Plain text, one record per line; the first line is the offset; note records are followed by modifier lines starting with `#` (speed) and `&` (width). Charset not stated in the page (UTF-8/ASCII in practice [inference]). Phira loads it with `format: pec` in `info.yml`.

## Structure / metadata

Line 1: offset in **ms** (integer). The doc says the real offset is `value - 175` ms (a fixed, unexplained 175 ms shift).

Record types (fields separated by spaces; times are in beats, floats):

| Record | Fields | Meaning |
|---|---|---|
| `bp <beat> <bpm>` | | BPM change |
| `n1 <line> <beat> <x> <side> <fake>` | `side`: 1 above, 2 below; `fake`: 1 = fake | Tap |
| `n2 <line> <startBeat> <endBeat> <x> <side> <fake>` | | Hold |
| `n3 ...` | same as `n1` | Flick |
| `n4 ...` | same as `n1` | Drag |
| `# <speed>` | after a note line | note speed multiplier |
| `& <width>` | after a note line | note width multiplier |
| `cv <line> <beat> <value>` | | instantaneous speed event (default speed 10.0; speed has no easing) |
| `cp <line> <beat> <x> <y>` | | instantaneous move |
| `cd <line> <beat> <angle>` | | instantaneous rotation |
| `ca <line> <beat> <alpha>` | | instantaneous alpha (0..255; -1 hides all notes on the line) |
| `cm <line> <startBeat> <endBeat> <x> <y> <easing>` | | eased move to (x, y) |
| `cr <line> <startBeat> <endBeat> <angle> <easing>` | | eased rotation |
| `cf <line> <startBeat> <endBeat> <alpha>` | | alpha change, always linear (no easing field) |

Easing numbers are the same table as RPE (`../rpe/`). Eased events start from the line's current value at the start beat.

## Timing model

Beats are floats (e.g. `0.500`); `bp` lines give the tempo map (`bp 0.000 180.000`). Coordinates in the file: origin at the bottom-left, centre at (1024, 700), range X 0..2048, Y 0..1400, angles **clockwise positive** (the editor UI uses centre origin and counter-clockwise positive). Convert beat to seconds by integrating the BPM list and applying the offset shift above.

## Notes

Types by prefix: `n1` Tap, `n2` Hold, `n3` Flick, `n4` Drag (same numbering as RPE). Modifier lines (`#`, `&`) bind to the preceding note line. Fake notes via the last field. 30-line limit.

## Audio & images

Not stored in PEC; supply them through the container (`info.yml` / `info.txt` for Phira).

## Versions & variants

Frozen; superseded by RPE JSON. No version marker in the file.

## Quirks & pitfalls

- The 175 ms constant is easy to forget.
- Angles are clockwise, unlike the RPE/editor UI convention.
- Speed (`cv`) events cannot be eased; alpha (`cf`) neither.
- Field order for `n2` differs from the other note types (two beats).

## Example

From the Phira docs (note and BPM examples; the note lines are verbatim, the BPM line is the doc's own sample):

```text
bp 0.000 180.000
n1 0 0.500 -40.000 1 0
# 1.00
& 1.00
n2 0 0.250 2.000 -320.000 1 0
# 1.00
& 1.00
```

## ROX support

Not read by ROX.

## Parsers & tools

Phira (Rust): <https://github.com/TeamFlos/phira>; prpr (`format: pec`): <https://github.com/Mivik/prpr>; Phichain converts PEC.

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): `synthetic-all-records.pec` (hand-written from the record table above, CC0).
- Manifest (`samples.manifest.json`): three real fan charts of yuameshi/phigros-charts-repo (`TSLove_chart.pec`, `All_the_time.pec`, `Tempestissimo.pec`), no licence file, hence not committed. [observed in the files: the first line is the offset (150, -50, -80), then `bp` lines, then `n1` records each followed by `#` and `&` lines]
- More: that repository holds more `.pec` charts (`grievousLady`, `materializeAnything`, `ouroVoros`, `terrasphere`, `theRailway`, ... by file name); PhiEdit is the editor that writes the format; Phira loads it with `format: pec` in `info.yml`.

## Sources

- <https://github.com/TeamFlos/phira-docs/tree/main/src/chart-standard/chart-format/pe> (basic, event, note pages)
- <https://github.com/Mivik/prpr> (README, `info.yml` formats `rpe`, `pgr`, `pec`)
