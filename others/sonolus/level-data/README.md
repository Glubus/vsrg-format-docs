# Sonolus Level Data (`.json (gzip)`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview

Level Data is the JSON resource a Sonolus engine uses to populate entities for a level. It is the interchange target of USC, SUS and many converters (rg_converters, sonolus-level-converters, `dcToLevelData` of the Deemo engine, `uscToLevelData` of the PJSekai engine). Specification: Sonolus Wiki "Level Data" and "Level Data Entity" pages and the `@sonolus/core` type definitions (7.16.0).

## Container & encoding

JSON that **must be GZip-compressed** (`.json` is the only supported format; the file served as the level's `data` resource is gzip JSON).

## Structure / metadata

```ts
type LevelData = { bgmOffset: number; entities: LevelDataEntity[] }
type LevelDataEntity = {
  name?: string
  archetype: EngineArchetypeName | string
  data: ({ name: string; value: number } | { name: string; ref: string })[]
}
```

- `bgmOffset` (seconds): offset applied to the BGM.
- `entities[]`: each entity names an archetype (a string) of the engine; engines ignore archetypes they do not implement, so metadata can be stored as extra entities.
- `data[]`: named values; `value` = number, `ref` = the `name` of another entity (used to link slide points, `SimLine` pairs, etc.).
- Entity `name` is optional and only needed as a `ref` target.

Special engine-independent names (`@sonolus/core`): archetypes `#BPM_CHANGE`, `#TIMESCALE_CHANGE`; data names `#BEAT`, `#BPM`, `#TIMESCALE`, `#JUDGMENT`, `#ACCURACY`.

Older wiki revisions used numeric archetype indexes and `data: { index, values }` (an older revision of the format) [from a search summary of the old NonSpicyBurrito wiki; the current wiki uses names].

Level item (server side `LevelItem`, not part of the file): `name`, `version: 1`, `rating`, `title`, `artists`, `author`, `tags`, `engine`, `useSkin`/`useBackground`/`useEffect`/`useParticle` (default or item), and resource links `cover`, `bgm`, `preview?`, `data`.

## Timing model

Time is expressed by the engine's own data: BPM via `#BPM_CHANGE` entities (`#BEAT` + `#BPM`), scroll speed via `#TIMESCALE_CHANGE` (`#BEAT` + `#TIMESCALE`), then any entity's `#BEAT` is converted to seconds by Sonolus using the BPM changes. Engines may instead store raw seconds in a custom data field (the Sonolus.js guide first uses a `time` field then refactors to `#BEAT`).

## Notes

Notes are engine archetypes; names and data are defined by each engine. Examples from real converters:

- Deemo engine (`dcToLevelData`): `Initialization`, `Stage`, `#BPM_CHANGE` (`#BEAT`, `#BPM`), `TapNote`/`SlideNote` with `#BEAT`, `lane`, `size`.
- PJSekai engine (`uscToLevelData`): `NormalTapNote`, `CriticalFlickNote`, slide joints, `SimLine` (data `a`, `b` as `ref`) with `#BEAT`, `lane`, `size`, `direction`, `ease`.

## Audio & images

BGM, cover and preview are separate Sonolus resources of the level item (not in LevelData).

## Versions & variants

Older engines/level data used index-based archetype and entity layouts; `@sonolus/core` 7.x uses names. SCP (collection package) format versions 0.5.13 and 0.6.0 differ (see `../scp/`). Next SEKAI LevelData (`.nsld`, `.json.gz`) is an engine profile with extended lanes, guide colours, fades, fake notes, timescale groups, dynamic stages.

## Quirks & pitfalls

- Must be gzip-compressed JSON.
- `ref` targets are entity names: names must be unique and defined.
- Unknown archetypes are silently ignored (not an error).
- The same container holds very different games; a decoder must know the engine to interpret archetype/data names.

## Example

From `sonolus-deemo-engine`'s `dcToLevelData` output shape (illustrative instance built from its converter code):

```json
{"bgmOffset":0,"entities":[
 {"archetype":"Initialization","data":[]},
 {"archetype":"Stage","data":[]},
 {"archetype":"#BPM_CHANGE","data":[{"name":"#BEAT","value":0},{"name":"#BPM","value":60}]},
 {"archetype":"TapNote","data":[{"name":"#BEAT","value":1.0},{"name":"lane","value":-2},{"name":"size","value":1}]}]}
```

## ROX support

Not read by ROX.

## Parsers & tools

- `@sonolus/core` (TypeScript types): <https://www.npmjs.com/package/@sonolus/core>
- rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>
- sonolus-level-converters (old): <https://github.com/UntitledCharts/sonolus-level-converters>
- sonolus-core-go (Go): <https://pkg.go.dev/github.com/WindowsSov8forUs/sonolus-core-go/core/resource>
- Sonolus.py: <https://sonolus.py.qwewqa.xyz/>

## Getting samples

Committed: one synthetic gzip LevelData and its plain JSON twin ([`samples/`](samples/)). No real level data was found in a licensed open repository (Sonolus engine/template repos checked ship no levels; `UntitledCharts/sonolus-level-converters` test files are `.sus` charts of Project SEKAI songs under GPL-3.0 but are copyrighted charts, not committed). To obtain real ones: any Sonolus server serves a level's `data` resource (gzip JSON; the level item JSON gives its URL), the sonolus-level-converters / rg_converters tools convert USC/SUS to LevelData, and the Sonolus.py/Sonolus.js guides build a test level.

## Sources

- <https://wiki.sonolus.com/level-specs/resources/level-data>
- <https://wiki.sonolus.com/level-specs/resources/level-data-entity>
- <https://wiki.sonolus.com/sonolus.js-guide/play/07> and `/08`
- <https://cdn.jsdelivr.net/npm/@sonolus/core@7.16.0/dist/common/core/level/data/data.d.ts>, `entity.d.ts`, `level/item.d.ts`, `engine/archetypeName/archetypeName.d.ts`, `engine/archetypeDataName/archetypeDataName.d.ts`
- <https://cdn.jsdelivr.net/npm/sonolus-deemo-engine@1.6.4/dist/dc/convert.js>
- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/convert.js>
