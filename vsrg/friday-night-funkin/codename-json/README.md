# Codename Engine chart JSON (`charts/<difficulty>.json` + `meta.json`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview

Codename Engine (FNF-CNE-Devs) is a FNF engine with its own chart editor and a song folder layout with per-difficulty charts and meta files. Its chart format is not section based: notes live in a list of **strumlines**, each with its own characters, key count and notes. It also reads and converts Psych and legacy charts at load, and V-Slice charts in its editor only. Source: `source/funkin/backend/chart/ChartData.hx`, `Chart.hx` (main branch).

## Container & encoding

- UTF-8 JSON. Per song folder `songs/<song>/`:
  - `charts/<difficulty>.json` (default variant) or `charts/<variant>/<difficulty>.json`: the chart (`Paths.chart(song, difficulty, variant)`; saving writes `'$songPath/$chartFolder/${difficulty}.json'`).
  - `meta.json`, optionally `meta-<difficulty>.json`, `meta-<variant>.json`, `meta-<variant>-<difficulty>.json` (`loadChartMeta` tries them in this order of specificity).
  - optional `events.json` / `events-<variant>.json`: global events merged into the chart's `events` (`loadEventsJson`).
- The parser detects the format of a chart file (`detectChartFormat`: `CODENAME`, `PSYCH_NEW`, `VSLICE`, `LEGACY`): Psych/legacy charts are converted at load (`PsychParser`, `FNFLegacyParser`), V-Slice is refused at runtime ("must be imported and converted in the new song editor window").

## Structure / metadata

`ChartData`:

| Field | Type | Meaning |
|---|---|---|
| `strumLines` | array of `ChartStrumLine` | |
| `events` | array of `ChartEvent` | |
| `meta` | `ChartMetaData` | filled from `meta.json` |
| `codenameChart` | bool | `true` marks the Codename layout (used by `detectChartFormat`) |
| `stage` | string | |
| `scrollSpeed` | float | |
| `noteTypes` | array of string | names of custom note types, indexed by `ChartNote.type - 1` |
| `bookmarks` | array, optional | `{ time, name, color }` |
| `chartVersion` | string, optional | |

`ChartStrumLine`: `characters` (array of strings), `type` (0 = opponent, 1 = player, 2 = additional/CPU always), `notes` (array of `ChartNote`), `position` (string: `dad`, `boyfriend`, `girlfriend`), optional `visible`, `strumPos` ([x, y]), `strumScale`, `strumSpacing`, `scrollSpeed` (per strumline), `vocalsSuffix`, `keyCount` (default 4), `strumLinePos` (legacy 0-1 horizontal position).

`ChartNote`: `{ time (ms), id (lane in the strumline), type (int), sLen (sustain length in ms) }`.

`ChartEvent`: `{ name, time, params: [...], global? }`. Old charts used `type` ints (-1 HScript Call, 0 Unknown, 1 Camera Movement, 2 BPM Change, 3 Alt Animation Toggle), converted to names at load.

`ChartMetaData` (`meta.json`): `name`, optional `variant`, `displayName`, `bpm`, `beatsPerMeasure`, `stepsPerBeat`, `difficulties`, `variants`, `customValues`, `icon`, `color`, `coopAllowed`, `opponentModeAllowed`, `instSuffix`, `vocalsSuffix`, `needsVoices`.

## Timing model

- Notes and events in absolute milliseconds. Tempo: `meta.bpm` (initial) plus events named `BPM Change` (param: the BPM) in `events`; `stepsPerBeat` (default 4) and `beatsPerMeasure` (default 4) from `meta.json`.
- Scroll speed: `scrollSpeed` per chart and optionally per strumline; `Scroll Speed Change` events exist in the engine [inference; not read in the files consulted].
- No sections: camera focus is an event (`Camera Movement`, param = strumline index).

## Notes

- A note belongs to the strumline that lists it. `id` is the lane inside the strumline (0..keyCount-1), so there is no `mustHitSection` and no 0-7 lane space. `keyCount` allows strumlines with other than 4 keys (default 4) - the only FNF variant here with a variable key count.
- `sLen` > 0 = hold of that length in ms.
- `type`: `0` = default note; `n >= 1` = `noteTypes[n - 1]` (`Chart.addNoteType` returns `index + 1` and `0` for the default note).
- Strumline `type` decides who plays it: `0` opponent (CPU, player in opponent mode), `1` player, `2` additional (always CPU).
- No mines (note types are scripted), no keysounds.

## Audio & images

`meta.instSuffix` / `vocalsSuffix` and strumline `vocalsSuffix` choose the audio files (e.g. `Voices_Opponent.ogg`); the chart itself has none.

## Versions & variants

- `chartVersion` optional. Per-difficulty meta and "variants" (`charts/<variant>/...`, `meta-<variant>.json`) are first-class.
- Conversion of legacy/Psych charts happens at load; the editor also imports V-Slice.

## Quirks & pitfalls

- Several charts with other key counts per strumline break "4 lanes per side" assumptions.
- `events.json` is a separate global file that must be merged.
- Old `events[].type` int is replaced by names.
- Chart-level `scrollSpeed` and strumline-level `scrollSpeed` both exist.

## Example

Illustrative, hand-built from the `ChartData` typedefs above (the MeguminBOT engine-differences page gives a similar example; not copied):

```json
{
  "codenameChart": true, "stage": "stage", "scrollSpeed": 2.0, "noteTypes": [],
  "strumLines": [
    { "type": 0, "position": "dad", "characters": ["dad"], "visible": true,
      "notes": [ { "time": 0, "id": 0, "type": 0, "sLen": 0 } ] },
    { "type": 1, "position": "boyfriend", "characters": ["bf"], "visible": true,
      "notes": [ { "time": 500, "id": 2, "type": 0, "sLen": 250 } ] }
  ],
  "events": [ { "name": "Camera Movement", "time": 0, "params": [0] } ]
}
```

## ROX support

Not read by ROX: the `.json` extension is routed to the legacy FNF codec, which expects `song.notes[].sectionNotes`; a Codename chart has no `song` object and fails parsing. A decoder would map each `strumLine` to a group of `keyCount` columns (an 8-column chart for two 4K strumlines).

## Parsers & tools

- Codename Engine (Haxe): https://github.com/FNF-CNE-Devs/CodenameEngine (`source/funkin/backend/chart/`)
- Moonchart `FNFCodename` (Haxe): https://github.com/MaybeMaru/moonchart

## Sources

- https://raw.githubusercontent.com/FNF-CNE-Devs/CodenameEngine/main/source/funkin/backend/chart/ChartData.hx
- https://raw.githubusercontent.com/FNF-CNE-Devs/CodenameEngine/main/source/funkin/backend/chart/Chart.hx
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (community comparison)
