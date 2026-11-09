# PJSK score maker chart (`.pjsk` / `.json` / `.json.gz`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg (12-lane vertical note highway) · Encoding: json (usually gzip + base64 wrapped)

## Overview

This is the **internal chart class of Project SEKAI: Colorful Stage! feat. Hatsune Miku's "score maker"** (the in-game custom-chart editor), as a JSON document: a list of **tempo/scroll/volume events** (`MusicScoreEventDataList`) and a flat list of **notes** (`NoteList`) in which slides are expressed as **doubly linked chains** (`previousConnectionId` / `nextConnectionId`). It is the closest thing to a "native" PJSK chart that tools can read or write; the community `.sus` ([`../sus`](../sus/README.md)) and `.usc` ([`../usc`](../usc/README.md)) formats are converted to and from it. No official documentation exists. The layout below is taken from the C++ loader/exporter of `UntitledCharts/rg_converters` (`cpp/src/converters/pjsk/`, a library by the UntitledCharts project that credits `susc-converter` as its base), which fully supports this format as "Fully Supported: `.pjsk/.json/.json.gz` - PJSK internal score maker class json". Fields not touched by the converter (e.g. `EventArray`, `FullComboDataHash`) are unknown.

## Container & encoding

- JSON (UTF-8). The converter's `load_raw` accepts three wrappers, tried in this order: **`base64(gzip(json))`** (the "server format" of the game), **raw gzip(json)**, or **plain JSON**. `detect` recognises a file as PJSK if it base64-decodes to a gzip stream (`1f 8b`) whose JSON contains both `NoteList` and `MusicScoreEventDataList`; plain-JSON files are therefore only detected by structure by other code paths [inference].
- The exporter writes `base64(gzip(json, level 9))` of a compact JSON (`dump(-1, true)`).
- Test files in the converter repo are named `<song>_append.pjsk.json`.

## Structure / metadata

Top-level object written by the exporter (and thus expected by the game):

| Key | Type | Meaning |
|---|---|---|
| `$id` | string | `"1"`; Json.NET reference id (the file is Json.NET-serialised C#: every object has `$id`). |
| `VersionCode` | int | `10000` in exports. |
| `MusicScoreEventDataList` | array | Events (below). |
| `EventArray` | array | Empty in exports (unknown content). |
| `NoteList` | array | Notes (below). |
| `MusicScoreTicksMax` | int | Largest note tick. |
| `MusicId` | int | Music id of the song this chart belongs to. |
| `FullComboDataHash` | null | `null` in exports. |

### Events (`MusicScoreEventDataList`)

Each event: `{ "$id", "id", "eventType", "ticks", "changeValue" }`.

| `eventType` | `changeValue` |
|---|---|
| 0 | BPM (float) |
| 1 | time scale / scroll speed multiplier (float; the loader gathers them into one time-scale group) |
| 2 | SE (sound effect) volume (float; the exporter adds a default `1.0` at tick 0 if none) |
| 3 | time signature string, e.g. `"4/4"` (exporter adds `4/4` at tick 0 if none; the loader does not read it) |

### Notes (`NoteList`)

Each note object:

| Key | Type | Meaning |
|---|---|---|
| `$id`, `id` | string, int | Reference id; unique note id (1-based counter). |
| `ticks` | int | Position in ticks; **480 ticks per beat**. |
| `laneStart`, `laneEnd` | int | Inclusive lane range `0..11`; width = `laneEnd - laneStart + 1`. Centre lane (converter convention) = `(laneStart + laneEnd)/2 - 5.5`, half-size = `(laneEnd - laneStart + 1)/2`. |
| `category` | int | Note kind (table below). |
| `type` | int | `1` = critical (gold) note; `0` = normal. |
| `speedRatio` | float | Per-note scroll ratio (default 1; non-positive or non-finite values are sanitised to 1). |
| `noteLineType` | int | Slide/guide segment shape: `0` linear, `1` ease-out, `2` ease-in. |
| `noteBaseType` | int | Base type enum: `Base=0, Normal=1, Long=2, Flick=3, FrictionFlick=4, Connection=5, HiddenConnection=6, LongHoldCombo=7, FrictionLong=8, FrictionHideLong=9, Guide=10, Friction=11, FrictionHide=12, GuideEnd=13, GuideHiddenConnection=14` (as commented in the exporter). |
| `previousConnectionId`, `nextConnectionId` | int | Linked chain; `-1` = none. |
| `direction` | int | Flick direction: `0` up, `1` left, `2` right. |
| `isSkip` | bool | Slide relay that adds a combo tick **without** changing the slide shape ("attach"). |
| `IsSingle`, `IsConnectedFirst`, `IsConnectedLast` | bool | Chain position flags (single = no links). |

`category` values (loader/exporter): `0` normal tap; `1` slide start / long end (normal long); `2` slide relay (visible connection); `3` flick; `4` trace (friction); `5` hidden trace end (FrictionHide); `6` trace slide start (FrictionLong); `7` hidden trace slide start (FrictionHideLong); `8` trace flick (FrictionFlick); `9` guide (start/end); `10` guide end; `11` guide hidden midpoint; `13` hidden slide relay (changes shape, no combo); `14` ignored by the loader.

## Timing model

Tick based: **480 ticks per beat** (`TICKS_PER_BEAT = 480`; the loader converts to beats with `ticks / 480`). BPM changes (`eventType 0`) and scroll multipliers (`eventType 1`) are events; time = integral of beats over BPM. Note `speedRatio` and time scale events give high-speed variations. There is **no offset field** in the chart: the audio offset is held elsewhere (the converter's metadata `waveoffset` defaults to 0).

## Notes

- Taps (`category 0`), critical (`type 1`), flicks (`3`, `direction`), traces/friction notes (`4`, `5`, `8`).
- Slides: a chain of notes linked by ids; head `IsConnectedFirst`, tail `IsConnectedLast`; start judge (`category 1` normal, `6` trace, `7` none), relays `2`/`13` (`isSkip` = attach), end `1/3/4/5/8`.
- Guides (`9`, `10`, `11`): coloured guide lines (green = normal, yellow = critical, according to the head's `type`).
- Wide notes: `laneStart..laneEnd` range.

## Audio & images

None in the chart. `MusicId` links to the game's music database.

## Versions & variants

- `VersionCode 10000` in exports; older/newer versions unknown.
- Related interchange: [`.sus`](../sus/README.md), [`.usc`](../usc/README.md), [`.mmws`](../mmws/README.md) and Sonolus LevelData (see [`../../../others/sonolus/level-data`](../../../others/sonolus/level-data/README.md)).

## Quirks & pitfalls

- Slides are not nested objects: reconstruct chains by following `nextConnectionId` from every note with `IsConnectedFirst`.
- `category 14` notes are dropped by the loader; Guide `type` colour comes from the head note.
- Lane width in the converter is `(laneEnd-laneStart+1)/2` (half-width); lane centre is offset by 5.5 so the 12 lanes centre on 0.
- Json.NET `$id`/`$ref` metadata appears in the file; reference ids in exports are strings counting from 2.
- Gzip + base64 is the transport format; do not try to read the raw string as JSON.

## Example

Illustrative, hand-built from the exporter's field list (one tap note and one BPM event; real files are gzip+base64 wrapped):

```json
{"$id":"1","VersionCode":10000,
 "MusicScoreEventDataList":[
  {"$id":"2","id":1,"eventType":0,"ticks":0,"changeValue":120.0},
  {"$id":"3","id":2,"eventType":3,"ticks":0,"changeValue":"4/4"},
  {"$id":"4","id":3,"eventType":2,"ticks":0,"changeValue":1.0}],
 "EventArray":[],
 "NoteList":[
  {"$id":"5","id":4,"ticks":480,"laneStart":5,"laneEnd":5,"category":0,"type":0,"speedRatio":1.0,
   "noteLineType":0,"noteBaseType":1,"previousConnectionId":-1,"nextConnectionId":-1,"direction":0,
   "isSkip":false,"IsSingle":true,"IsConnectedFirst":false,"IsConnectedLast":false}],
 "MusicScoreTicksMax":480,"MusicId":0,"FullComboDataHash":null}
```

## ROX support

Not read by ROX. It is a 12-lane layout with wide notes, flicks/traces, slides with ease curves, guides and per-note speed ratios; a conversion to ROX columns would be lossy (slides, guides, width and critical flags).

## Parsers & tools

- `rg-converters` (C++ core with Python bindings): https://github.com/UntitledCharts/rg_converters (`cpp/src/converters/pjsk/loader.cpp`, `exporter.cpp`, `detector.cpp`; PyPI `rg-converters`).
- `susc-converter` (credited base): https://github.com/Kyonkrnk/susc-converter

## Sources

- https://github.com/UntitledCharts/rg_converters (commit `673710dcc441aea97ac89e113f811d5c169763d4`): `README.md`, `cpp/src/converters/pjsk/*.cpp`, `cpp/include/rg/converters/pjsk.hpp`
