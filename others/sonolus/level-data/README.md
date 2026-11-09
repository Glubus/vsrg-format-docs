# Sonolus Level Data (`.json (gzip)`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview

Level Data is the JSON resource a Sonolus engine uses to populate entities for a level, and the interchange target of USC, SUS and many converters (rg_converters, sonolus-level-converters, `dcToLevelData` of the Deemo engine, `uscToLevelData` of the PJSekai engine). Spec: Sonolus Wiki "Level Data" and "Level Data Entity" pages and the `@sonolus/core` type definitions (7.16.0).

## Container & encoding

GZip-compressed JSON (`.json` is the only supported format; the level's `data` resource is gzip JSON).

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

Time comes from engine data: BPM via `#BPM_CHANGE` entities (`#BEAT` + `#BPM`), scroll speed via `#TIMESCALE_CHANGE` (`#BEAT` + `#TIMESCALE`); Sonolus converts any entity's `#BEAT` to seconds from the BPM changes. Engines may store raw seconds in a custom field instead (the Sonolus.js guide first uses `time`, then refactors to `#BEAT`).

## Notes

Notes are engine archetypes with engine-defined names and data. Real converters:

- Deemo engine (`dcToLevelData`): `Initialization`, `Stage`, `#BPM_CHANGE` (`#BEAT`, `#BPM`), `TapNote`/`SlideNote` with `#BEAT`, `lane`, `size`.
- PJSekai engine (`uscToLevelData`): `NormalTapNote`, `CriticalFlickNote`, slide joints, `SimLine` (data `a`, `b` as `ref`) with `#BEAT`, `lane`, `size`, `direction`, `ease`.

## Audio & images

BGM, cover and preview are separate resources of the level item.

## Versions & variants

Older engines/level data used index-based archetype and entity layouts; `@sonolus/core` 7.x uses names. SCP (collection package) format versions 0.5.13 and 0.6.0 differ (see `../scp/`). Next SEKAI LevelData (`.nsld`, `.json.gz`) is an engine profile with extended lanes, guide colours, fades, fake notes, timescale groups, dynamic stages.

## Quirks & pitfalls

- Must be gzip-compressed JSON.
- `ref` targets are entity names: unique and defined.
- Unknown archetypes are silently ignored.
- A decoder needs the engine to interpret archetype/data names.

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

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (UntitledCharts Sonolus server: `https://untitledcharts.com/sonolus/levels/<name>` gives the item, whose `data.url` is the gzip JSON; only `data` was downloaded). Real NextRUSH+ data uses `#BPM_CHANGE`, `#TIMESCALE_GROUP`, `#TIMESCALE_CHANGE`, `NormalTapNote`, `CriticalFlickNote`, `AnchorNote`, `Connector`, `SimLine`, `Initialization` [observed: untitledcharts_*.json.gz]. Any Sonolus server serves levels the same way; `sonolus-level-converters` / `rg_converters` convert USC/SUS to LevelData.

## Sources

- <https://wiki.sonolus.com/level-specs/resources/level-data>
- <https://wiki.sonolus.com/level-specs/resources/level-data-entity>
- <https://wiki.sonolus.com/sonolus.js-guide/play/07> and `/08`
- <https://cdn.jsdelivr.net/npm/@sonolus/core@7.16.0/dist/common/core/level/data/data.d.ts>, `entity.d.ts`, `level/item.d.ts`, `engine/archetypeName/archetypeName.d.ts`, `engine/archetypeDataName/archetypeDataName.d.ts`
- <https://cdn.jsdelivr.net/npm/sonolus-deemo-engine@1.6.4/dist/dc/convert.js>
- <https://cdn.jsdelivr.net/npm/sonolus-pjsekai-engine@1.9.0/dist/usc/convert.js>
