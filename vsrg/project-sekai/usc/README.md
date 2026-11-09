# Universal Sekai Chart (USC) (`.usc`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: json

## Overview

JSON score model of NonSpicyBurrito's `sonolus-pjsekai-engine` (Sonolus recreation of the Project SEKAI engine), which converts SUS to USC (`susToUSC`) and USC to Sonolus Level Data (`uscToLevelData`). `rg_converters` calls `.usc` "the old Sonolus standard (DEPRECATED FORMAT)", superseded by Next SEKAI LevelData. MMW4CC and similar editors export it. The structure below is the TypeScript type definition in `sonolus-pjsekai-engine@1.9.0`.

## Container & encoding

JSON (UTF-8). Editors may wrap or extend the object (not verified); the engine expects the bare `{offset, objects}` shape. Sonolus level data derived from it is gzip-JSON (see `../../../others/sonolus/level-data/`).

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

Beat-based (`beat` floats). `bpm` objects change tempo, `timeScale` objects change scroll speed. Beats convert to seconds via the `bpm` objects; `offset` shifts the BGM.

## Notes

Single notes map to Sonolus archetypes (from `usc/convert.js`): `NormalTapNote`, `CriticalTapNote`, `NormalFlickNote`, `CriticalFlickNote`, `NormalTraceNote`, `CriticalTraceNote`, `NormalTraceFlickNote`, `CriticalTraceFlickNote`; direction values: left -1, up 0, right 1; eases: out -1, linear 0, in 1. Slides become connected entities (joints, attaches, ends) with `lane`/`size` data. Simultaneous notes get `SimLine` entities automatically.

## Audio & images

None (BGM is part of the Sonolus level item).

## Versions & variants

Superseded by Next SEKAI LevelData (`.nsld`); per rg_converters the Chart Cyanvas and Untitled SEKAI LevelData variants are deprecated. rg_converters converts SUS <-> USC.

## Quirks & pitfalls

Slide `connections` start with start/ignore and end with end/ignore. hidden/attach have no lane or size. lane/size may be non-integer.

## Example

Hand-built from the TypeScript types above:

```json
{"offset":0,"objects":[
 {"type":"bpm","beat":0,"bpm":120},
 {"type":"single","beat":4,"lane":0,"size":1,"trace":false,"critical":false}]}
```

## ROX support

Decode only, `rox::formats::sekai` (`UscDecoder`, `DetectedFormat::Usc`). One chart per file, always 12 columns: leftmost lane `lane - size + 6` (`susToUSC` writes `lane = x - 8 + width / 2`, `size = width / 2`), rounded when within 1e-4 of a whole lane, else floored and counted; notes not entirely on the stage are dropped and counted.

- Accepts bare `{offset, objects}` or `{"usc": {...}, "version": 1|2}` (version 2 adds `damage`, `guide`, `skill`, `feverChance`, `feverStart`, `timeScaleGroup`).
- A `single` is a tap (`direction` counted as a flick; `critical` and `trace` dropped and counted). An active `slide` is one hold from first to last connection on the first column; its middle connections are dropped and counted. Guides, `damage`, `skill`, fever and scroll objects are counted and ignored.
- `bpm` in beats (last of a beat wins; first BPM also holds before it; none valid is an error). `offset` (seconds, `-#WAVEOFFSET` of the source SUS) shifts every time. Title is the file stem; sound is found in the folder. Limit 16 MiB.
- Prism (`docs/game.md` "Project SEKAI"): the scan keeps a `.usc` only if it starts as a JSON object with an `"objects"` key (`rox::formats::looks_like_usc`), then refuses it as `Unsupported layout: 12K` (no 12-column layout in the catalog).

Decisions: `rox::formats::sekai` `mod.rs`; tests `sekai/tests.rs`. Read for this: `sonolus-pjsekai-engine` `lib/src/usc/{index,convert}.ts`, `lib/src/sus/convert.ts` (MIT); `rg_converters` (GPL-3.0; wrapper, version-2 types, `offset` sign only; nothing copied). No real `.usc` was decoded.

## Parsers & tools

sonolus-pjsekai-engine (TypeScript): <https://github.com/NonSpicyBurrito/sonolus-pjsekai-engine> (superseded by <https://github.com/Next-SEKAI/sonolus-next-sekai-engine>); rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

- [observed: susc-converter_ccmmw.usc] the editors' file is wrapped as `{"usc":{"objects":[...]}}` (compact, keys alphabetical), has a `timeScaleGroup` object (`{"changes":[{"beat","timeScale"}],"type":"timeScaleGroup"}`), and every note carries `timeScaleGroup` (index) next to `lane`, `size`, `critical`, `trace`.
- More: convert any SUS with rg-converters or `susToUSC`. Sonolus servers serve LevelData, not USC. No public repository with raw `.usc` charts exists besides susc-converter's tests.

## Sources

- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/index.d.ts>
- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/convert.js>
- <https://github.com/UntitledCharts/rg_converters>
