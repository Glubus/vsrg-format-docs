# OhShape level (`.yml`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (YAML 1.1)

## Overview
An OhShape map is a single YAML file that references an `.ogg` song (`clip`) and lists, per level (difficulty layer), a sequence of timed objects (`second`, `obj`, `track`, `position`, `length`). The structure comes from the editor's C# model `DeserializedSong` (deserialised with YamlDotNet, camelCase naming, unmatched properties ignored) and the bundled example `ice-flow-by-kevin-macleod.yml` (354 lines). The meaning of the compact object codes is taken from the editor's `WallsUtils.cs`; some codes (hand pose digits) are only enumerated, not explained.

## Container & encoding
- Text file starting with `%YAML 1.1` and `---`, UTF-8 (the editor reads with `FileManager.ReadYaml`). Keys are camelCase (`vOffset`, `audioTime`).
- Files go in `My Documents/OhShape/Songs`; sub-folders make albums. One `.yml` per difficulty ("Easy, Medium and Hard" per the official wiki: the difficulty is part of the file name when making several) with the same `.ogg`.
- The video (`video`, `.mp4`) is editor-only reference in the example.

## Structure / metadata
Top-level keys (`DeserializedSong`):

| Key | Type | Meaning |
|---|---|---|
| `title` | string | song title |
| `clip` | string | audio file name without extension (`.ogg`) |
| `icon`, `source` | string | cover and source (optional) |
| `speed` | int | wall approach speed (30 in the example) |
| `offset` | float | audio offset (0 in the example) |
| `author` | string | song author (artist) |
| `difficulty` | string | e.g. `medium` |
| `preview` | float | preview start, seconds |
| `genere` | string | genre (sic) |
| `audioTime` | float | audio duration in seconds |
| `grid`, `gridBpm`, `gridOffset` | bool/float/float | editor snapping grid settings |
| `scenario` | int | scenery |
| `forceDebug` | bool | debug flag |
| `video`, `vOffset` | string, float | reference video file and offset |
| `levels[]` | `{level: int, sequence: []}` | objects per level; the editor loads level 0 |
| `poses[]` | `{pose, x, y, ang}` | named poses [role not documented] |
| `offsetHorizontal`, `offsetVertical` | float | calibration offsets |
| `objects[]` | `{id, type, head{X,Y,Z}, leftHand, rightHand, position, size, life}` | definitions of custom walls (`WC.<id>`) [only the C# model was read] |

`sequence[]` item (`LevelSequence`): `second` (float seconds), `obj` (string code), `track` (int, 0 in the example), `position` (int), `length` (float).

## Timing model
`second` is an absolute time in seconds from the start of the audio. There are no BPM/beat fields in the gameplay data: `grid`, `gridBpm`, `gridOffset` only drive the editor grid. The editor rounds times to 0.01 s (`Mathf.Round(time * 100)`). The `length` of avoid walls (e.g. `WA.L.30`) is part of the id string; its unit is not stated [inference: hundredths of a second, because the check `CheckAvoidWall` requires 2..100000].

## Notes
Object code `obj` = `TYPE.<payload>`, with TYPE from `WallsUtils.Walltype` (`NONE, WP, WA, WH, WC, CN, EV`):
- `WP.<6 chars>` pose wall. Chars: [1] torso offset `C`/`R`/`L`, [2] and [3] hand poses from `1-9,0,A,B` (left and right), [4] torso offset `C`/`R`/`L`, [5] height `U`/`D`, [6] legs `L`/`C`/`R`. Special ids `WP.28RDO` and `WP.82LDO`. Invalid combinations are removed (`CleanInvalidWalls`). Example in the sample: `WP.C18CUC`, `WP.C81CUC`, `WP.CAACUC`.
- `WH.<3 chars>` hit wall: torso offset `C`/`R`/`L`, hand `L`/`R`/`B` (both), height `U`/`D`. Example `WH.CRU`.
- `WA.<dir>.<len>` avoid (dodge) wall: dir in `U`, `L`, `R`, `RI`, `LI`; `len` number (30, 40 in the sample).
- `CN.<x>.<y>` coin at x in -10..10, y in 0..13 (e.g. `CN.0.6`, `CN.-3.6`).
- `WC.<id>` custom wall defined in `objects[]`; `EV.<...>` event [semantics unknown].
- Mirroring in the editor swaps `L` and `R` characters (and swaps characters 2 and 3 of `WP` ids; for coins negates x).
- Simultaneous events are separate entries with the same or close `second`. There are no holds apart from avoid-wall length.

## Audio & images
`clip` `.ogg` file in the same folder; optional `icon` image, `video` mp4 (editor). `preview` seconds.

## Versions & variants
Editor built with Unity 2017.4.30f1 (README). No format version key exists in the file. The model contains `scenario`, `grid*`, `icon`, `source` that the bundled example does not use; unknown keys are tolerated (`IgnoreUnmatchedProperties`).

## Quirks & pitfalls
- `genere` misspelling, `speed` integer, ids are case-insensitive in the editor (upper-cased on load).
- The editor only loads `levels[0]`.
- Hand-pose digits are a closed set; ids outside the generated set are invalid.
- The `second` key is a float but the editor writes two decimals.

## Example
Real excerpt from the bundled example `examples/ice-flow-by-kevin-macleod.yml` (first lines):
```yaml
%YAML 1.1
---
title: Ice Flow
clip: ice-flow-by-kevin-macleod
speed: 30
author: Kevin MacLeod
difficulty: medium
preview: 6.8
audioTime: 74
levels:
  - level: 0
    sequence:
      - second: 2.36
        obj: CN.0.6
        track: 0
      - second: 2.59
        obj: WP.C18CUC
        track: 0
```

## ROX support
Not read by ROX. Pose walls cannot be expressed in key columns.

## Parsers & tools
- OhShape Level Editor (C#, YamlDotNet): https://github.com/OddersLab/OhShapeEditor
- OhShape-SimpleSongInfo (overlay mod, reads current song data): https://github.com/Shadnix-was-taken/OhShape-SimpleSongInfo

## Getting samples

**Committed** ([`samples/`](samples/SOURCES.md)): 8 real levels: the official demo (GPL-3, OddersLab/OhShapeEditor) and 7 community maps from the OhShapes site (`ohshapes-*.yml`, extracted from the zips; audio and cover dropped). More: <http://ohshapes.com> (BeatSaver-style API: `/api/maps/latest/<page>`, downloads at `/api/download/key/<key>`), the OhShape Discord; maps are written by the official Level Editor.

## Sources
- https://github.com/OddersLab/OhShapeEditor (`Readme.md`, `examples/ice-flow-by-kevin-macleod.yml`, `src/Assets/Scripts/WallDanceVR/YamlDeserializer.cs`, `src/Assets/Scripts/Utils/WallsUtils.cs`, `src/Assets/Scripts/Manager/SongManager.cs`)
- https://ohshape.fandom.com/wiki/Editor (via search snippet)
