# Cytus 1 chart ("Rayark v2 modified") (`.txt`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text

## Overview

Text chart of the original **Cytus** (Rayark, 2012), in the dialect the Cytoid wiki calls **"Rayark v2 modified"**: Cytus' own `VERSION 2` text format plus a custom `OFFSET` parameter. It is the only format the early Cytoid supported, loaded by Cytoid and edited with Cytunity and PCtyx; the community also calls it the "C1 chart format" (deprecated in favour of the JSON C2 format, `../c2-json/`). The original repository README lists `.txt` for "Cytus chart, including original and Version2": the "Version2" in that line is this `VERSION 2` dialect; the pre-v2 ("original") layout is not described by any consulted source.

## Packaged in

- Packaged in [`cytoidlevel`](../cytoidlevel/).

## Container & encoding

Plain text, one record per line, one chart per file (extension `.txt`; PCtyx saving as `.txt` exports C2/Cytoid format since v200). Fields separated by a single space or tab (the wiki sample uses tabs in `NOTE` lines). Distributed inside Cytoid level archives (see `../cytoidlevel/`) or alone.

## Structure / metadata

Header (4 lines) then `NOTE` lines then `LINK` lines:

| Record | Format | Meaning |
|---|---|---|
| `VERSION` | `VERSION {0}` | format version used internally by Cytus (`2`); Cytoid does not read it |
| `BPM` | `BPM {0}` | music BPM, used by Cytus for visual-effect timing; no effect in Cytoid (as of its Beta 2) |
| `PAGE_SHIFT` | `PAGE_SHIFT {0}` | shift of the first page, in seconds |
| `PAGE_SIZE` | `PAGE_SIZE {0}` | duration of one page in seconds (the scanner sweep time); smaller = faster scanner. The CrowFX guide gives `240 / BPM` for the editor-generated value (e.g. BPM 402 -> 0.597015) |
| `NOTE` | `NOTE {id} {timing} {x} {duration}` | `id` identifies the note (Cytus requires chronological ids; Cytoid accepts any order); `timing` seconds when the note is touched; `x` in 0..1 (0 left, 1 right); `duration` > 0 makes it a Hold |
| `LINK` | `LINK {id 1} {id 2} ...` | note chain (Drag): the listed ids are chained in order |
| `OFFSET` | `OFFSET {0}` | **custom** (Cytoid): shifts all note times, seconds; positive delays notes, negative advances them |

## Timing model

Absolute seconds, no tempo map: `NOTE` timing and duration are in seconds from the start of the music; tempo changes are baked into the times. `PAGE_SIZE` sets the page (scan sweep) length and `PAGE_SHIFT` the first page's shift, so the page of a note is derived from `timing`, `PAGE_SHIFT` and `PAGE_SIZE` [inference: the exact page-boundary formula is not stated]. The scanner reverses direction at each page boundary.

## Notes

Types are derived: every `NOTE` is a Click; `duration > 0` makes it a Hold (may span pages); an id listed in a `LINK` line becomes a Drag in that chain. No Flick or Long Hold in this format. No sibling flag: simultaneity is implicit.

## Audio & images

Not referenced by the chart (music and background live in the Cytoid level description or the game's assets).

## Versions & variants

- `VERSION 2` = Cytus format; "Rayark v2 modified" adds `OFFSET` (Cytoid).
- Superseded by the JSON C2 format (`../c2-json/`) in Cytoid, which adds tempo list, explicit pages, flicks and long holds.
- Converters: TigerHix's gist converts a Cytus chart to a Cytus II chart; `ky-reflection/cyl_package_tool` converts Cytus 2 JSON/txt to Cytus 1 `.converted.txt`; Cytofu converts Cytoid charts to osu! beatmaps.

## Quirks & pitfalls

- Cytus itself requires chronological note ids; Cytoid does not.
- Link breaks: LINK ids that do not match a NOTE make Cytoid misbehave and Cytunity report "Link Break"; Cytunity may allocate new ids on edits and fail to update LINK lines.
- Times are plain seconds (no minutes); the editor-generated PAGE_SIZE is derived from BPM.
- Fields are whitespace separated; parsers should accept both tabs and spaces.

## Example

From the Cytoid wiki (sample chart file, shortened):

```text
VERSION 2
BPM 402.000000
PAGE_SHIFT 0.800000
PAGE_SIZE 0.597015
NOTE	0	1.588880	0.800000	0.000000
NOTE	1	2.782910	0.600000	0.000000
NOTE	3	5.170969	0.600000	0.298508
LINK 26 27 28 29
```

## ROX support

Not read by ROX.

## Parsers & tools

- Cytoid (Unity, C#): <https://github.com/Cytoid/Cytoid>
- PCtyx editor: <https://github.com/XionUzuki/PCtyx>; Cytunity (editor)
- Converters: <https://gist.github.com/TigerHix/edf9933ce98da7ce92b9a70364ba4935> (Cytus -> Cytus II), <https://github.com/ky-reflection/cyl_package_tool> (C2 -> C1), <https://github.com/CenTdemeern1/Cytofu> (-> osu!)
- Make_Cytus2: <https://github.com/we684123/Make_Cytus2>

## Sources

- <https://raw.githubusercontent.com/wiki/Cytoid/Cytoid/b.-Chart-formats.md> (Cytoid wiki "b. Chart formats": VERSION, BPM, PAGE_SHIFT, PAGE_SIZE, NOTE, LINK, OFFSET)
- <https://sites.google.com/site/cytoidcommunity/charting/chart-format/c1-chart-format> (CrowFX guide)
- <https://cytoid.wiki/en/reference/chart/c1-format> (WIP stub page)
