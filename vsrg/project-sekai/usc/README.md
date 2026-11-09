# Universal Sekai Chart (USC) (`.usc`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: json

## Overview

USC (Universal Sekai Chart) is the JSON score model used by NonSpicyBurrito's `sonolus-pjsekai-engine` (a Sonolus recreation of the Project SEKAI engine); the package converts SUS to USC (`susToUSC`) and USC to Sonolus Level Data (`uscToLevelData`). The `rg_converters` README calls `.usc` "the old Sonolus standard (DEPRECATED FORMAT)", superseded by Next SEKAI LevelData. Editors such as MMW4CC export USC. The structure below is the TypeScript type definition shipped in `sonolus-pjsekai-engine@1.9.0`.

## Container & encoding

JSON (UTF-8). A chart editor may wrap or extend the object (not verified); the engine expects the bare `{offset, objects}` shape. Sonolus level data derived from it is gzip-JSON (see `../../../others/sonolus/level-data/`).

## Structure / metadata

Root: `{ "offset": number, "objects": USCObject[] }` (`offset` becomes `bgmOffset`).

Every object has `beat` (number). Types:

| `type` | Fields |
|---|---|
| `bpm` | `bpm` |
| `timeScale` | `timeScale` (scroll speed multiplier) |
| `single` | `lane`, `size`, `trace` (bool), `critical` (bool), `direction?` (`left`/`up`/`right`) |
| `slide` | `active` (bool), `critical` (bool), `connections` (array, see below) |

`slide.connections` is an ordered list: first element `start` or `ignore`, then any of `ignore`, `tick`, `hidden`, `attach`, last element `end` or `ignore`. Connection elements:

| `type` | Fields |
|---|---|
| `start` | `beat`, `lane`, `size`, `trace`, `critical`, `ease` (`out`/`linear`/`in`) |
| `ignore` | `beat`, `lane`, `size`, `ease` |
| `tick` | `beat`, `lane`, `size`, `trace`, `critical`, `ease` |
| `hidden` | `beat` |
| `attach` | `beat`, `critical` |
| `end` | `beat`, `lane`, `size`, `trace`, `critical`, `direction?` |

## Timing model

Beat-based (`beat` floats); BPM changes by `bpm` objects, scroll speed by `timeScale` objects. Conversion: beats -> seconds via the `bpm` objects; `offset` shifts the BGM.

## Notes

Single notes map to Sonolus archetypes (from `usc/convert.js`): `NormalTapNote`, `CriticalTapNote`, `NormalFlickNote`, `CriticalFlickNote`, `NormalTraceNote`, `CriticalTraceNote`, `NormalTraceFlickNote`, `CriticalTraceFlickNote`; direction values: left -1, up 0, right 1; eases: out -1, linear 0, in 1. Slides become connected entities (joints, attaches, ends) with `lane`/`size` data; simultaneous notes get `SimLine` entities generated automatically.

## Audio & images

None (BGM is part of the Sonolus level item).

## Versions & variants

Superseded by Next SEKAI LevelData (`.nsld`) and by Chart Cyanvas / Untitled SEKAI LevelData variants (per rg_converters: Chart Cyanvas and Untitled SEKAI formats are deprecated). SUS <-> USC conversions available in rg_converters.

## Quirks & pitfalls

Slide `connections` must start with start/ignore and end with end/ignore; hidden/attach have no lane or size; lane/size are numbers (can be non-integer).

## Example

Illustrative, hand-built from the TypeScript types above:

```json
{"offset":0,"objects":[
 {"type":"bpm","beat":0,"bpm":120},
 {"type":"single","beat":4,"lane":0,"size":1,"trace":false,"critical":false}]}
```

## ROX support

Read by ROX since Prism's addition of `rox::formats::sekai` (decode only): `UscDecoder` (`decode`, `decode_with_report` giving a `SekaiReport`, `decode_with_title`, `decode_file`; `DetectedFormat::Usc`). ONE chart per file, always **12 columns**, from `lane` (the CENTRE of the note from the centre of the stage) and `size` (HALF its width), as `susToUSC` writes them (`lane = x - 8 + width / 2`, `size = width / 2`): the leftmost lane is `lane - size + 6`, the column is that value (rounded when within 1e-4 of a whole lane, else floored and counted); a note not entirely on the stage is dropped and counted. The document may be bare (`{offset, objects}`) or wrapped in `{"usc": {...}, "version": 1|2}` (the editors' files, read from `rg_converters`; version 2 adds `damage`, `guide`, `skill`, `feverChance`, `feverStart` and `timeScaleGroup` objects). A `single` is a tap (`direction` is a flick, counted; `critical` dropped and counted; `trace` dropped and counted), a `slide` with `active` (true or absent) is ONE hold from its first connection to its last on the first connection's column, the connections between dropped and counted; a `slide` with `active: false` and a `guide` object are guides (dropped and counted); `damage`, `skill`, `feverChance`, `feverStart` and the scroll speeds (`timeScale`, `timeScaleGroup`) are counted and ignored. `bpm` objects are in beats (the last of a beat wins; the first BPM also holds before it; no valid BPM is an error); `offset` (seconds, `-#WAVEOFFSET` of the SUS it came from) moves every time by itself. A `.usc` has no title and no audio name: the title is the file stem, the sound is found in the folder. Limit 16 MiB. Decisions: `rox::formats::sekai` `mod.rs`; tests (every file built by hand): `sekai/tests.rs`.

Read by Prism (`docs/game.md` "Project SEKAI"): same as the `.sus`; the scan keeps a `.usc` only when it starts as a JSON object with an `"objects"` key (`rox::formats::looks_like_usc`). No 12-column layout exists in the catalog yet: refused by the scan as `Unsupported layout: 12K` until one does.

Sources read for this: `sonolus-pjsekai-engine` `lib/src/usc/{index,convert}.ts` and `lib/src/sus/convert.ts` (MIT), and `rg_converters` (GPL-3.0, read for the wrapper, the version-2 object types and the sign of `offset` only; nothing copied). No real `.usc` was decoded.

## Parsers & tools

sonolus-pjsekai-engine (TypeScript): <https://github.com/NonSpicyBurrito/sonolus-pjsekai-engine> (superseded by <https://github.com/Next-SEKAI/sonolus-next-sekai-engine>); rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>.

## Sources

- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/index.d.ts>
- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/convert.js>
- <https://github.com/UntitledCharts/rg_converters>
