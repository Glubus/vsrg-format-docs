# FPS Plus chart JSON (`<song>.json` + `meta.json` + `events.json`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

FPS Plus (ThatRozebudDude, "FNF: FPS Plus") is an FNF engine/mod. The repository (ThatRozebudDude/FPS-Plus-Public, commit `8cc8ddac5f6f922686e8fd6741df8113e6249ad1`) now uses its own `fpsplus_1` format (`source/Chart.hx`), described under "Structure / metadata" [observed: synthetic-fpsplus-chart-normal.json and the manifest files]. Moonchart's `FNFFpsPlus` describes the older legacy-plus-sidecars layout, which the engine still reads for backward compatibility.

## Container & encoding

JSON, UTF-8. Per song: the legacy chart file (see [../legacy-json/README.md](../legacy-json/README.md)), a `meta` file and an `events` file (`formatFile` adds `meta` and `events` to the legacy file-name candidates).

## Structure / metadata

### `fpsplus_1` (current, `Chart.CURRENT_CHART_FORMAT`) [from `source/Chart.hx`; observed in the real `chart-normal.json`]

File `data/songs/<song>/chart-<difficulty>.json` (`Chart.chartFromSong`; with `BACKWARD_COMPATIBILITY` falls back to `<song>[-<difficulty>].json`). The loader trims trailing characters until the text ends with `}`.

- `meta`: `format` ("fpsplus_1"), `song`, `bpm` (ARRAY of `{ bpm, time }`: tempo map, time in ms), `player`, `opponent`, `speaker` (character names, capitalised in the shipped files: `Bf`, `Dad`, `Gf`), `stage`, `scroll` (float).
- `notes`: flat array of `{ time (ms), direction (0-3), length (int, in STEPS: the legacy converter uses `round(sustainMs / stepMs)`), tag (string, `""` or e.g. `alt`, `hey`, `censor`, `weekend-1-...`), player (bool: true = the player's strumline) }`. No sections, no `mustHitSection`.
- `events.json`: `{ meta: { format }, events: [ { time, lane, tag } ] }` (tag strings such as `camFocusDad;0;0`, `setBopFreq;bf;1`, `playAnim;bf;hey;false`).
- `meta.json` (observed): `name`, `artist`, `album`, `difficulties` (ints), `difficultySet`, `compatibleInsts`, `compatableInsts`, `mixName`.

### Legacy layout (Moonchart's description; still converted by `Chart.convertLegacyChart`)

- Chart: the legacy `{song: {...}}` object plus `stage` (string) and `gf` (character string) (typedef `FpsPlusJsonFormat = FNFLegacyFormat & { stage, gf }`).
- `meta.json` (`FpsPlusMetaJson`): `name`, `artist`, `album` (strings), `difficulties` (array of ints: ratings per difficulty, sorted easy, normal, hard, erect, nightmare), `compatableInsts` (array or null), `mixName`, `bfBeats` and `dadBeats` (arrays of ints: beats on which the characters bop), `pauseMusic`.
- `events.json` (`FpsPlusEventsJson`): `{ "events": { "events": [ event, ... ] } }`, each event an array `[section, time, ?, name, ...]` (accessors: index 0 = section number, 1 = time, 3 = name; index 2 and the value slots are undocumented in the sources read).
- Note types: `alt`, `censor`, `hey` (`FNFFpsPlusNoteType`) mapped to alt animation / censor / cheer.

## Timing model

As legacy: absolute ms, section BPM changes (`fpsplus_1`: `meta.bpm` tempo-map array).

## Notes

As legacy (`[time, lane, sustain]` plus type extras, lanes combined with `mustHitSection`). `fpsplus_1`: see the `notes` entry above.

## Audio & images

Unknown.

## Versions & variants

`fpsplus_1` is the only version string in the source (`Chart.hx`: "This is where you'd do version upgrading with new formats in the future"); a file without a `meta` key is treated as legacy and converted (`convertLegacyChart`: sections become a flat note list, `mustHitSection` becomes the `player` bool, `altAnim` becomes the tag `animSet;alt`, `changeBPM` sections become tempo-map entries).

## Quirks & pitfalls

As legacy. Moonchart's `findMeta` picks the meta file as the JSON that contains the word `name`.

## Example

See [samples/synthetic-fpsplus-chart-normal.json](samples/synthetic-fpsplus-chart-normal.json) (synthetic, `fpsplus_1`) and the real files listed in [samples/SOURCES.md](samples/SOURCES.md).

## ROX support

Not read. A `fpsplus_1` chart has no `song.notes[].sectionNotes`, so the legacy codec fails [inference]; only the legacy-layout variant decodes.

## Parsers & tools

- Moonchart `FNFFpsPlus` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFFpsPlus.hx
- FPS Plus: https://github.com/ThatRozebudDude/FPS-Plus-Public

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: the repository's `assets/data/songs/<song>/` (`chart-<diff>.json`, `events.json`, `meta.json`); its README allows non-commercial use only and forbids generative-AI use. Observed: the current format is `fpsplus_1`, not the legacy layout Moonchart describes.

## Sources

- https://raw.githubusercontent.com/ThatRozebudDude/FPS-Plus-Public/8cc8ddac5f6f922686e8fd6741df8113e6249ad1/source/Chart.hx and `source/Song.hx`

- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/legacy/FNFFpsPlus.hx
