# Pistol Whip Custom Levels folder (`level.pw`, `.pw_beat`, `.pw_koreo`, `.pw_sec`, `.pw_geo`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json (several files per level)

## Overview

The PWCL (Pistol Whip Custom Levels) mod by Givo loads levels from `./Custom Levels/<LevelName>/`. A level is a folder of JSON files: `level.pw` (metadata, global settings) and per difficulty (`Easy`, `Normal` or `Hard`) `<Diff>.pw_beat` (the gameplay chart: enemies and obstacles on beats), `<Diff>.pw_koreo` (Koreographer tempo map and event tracks), `<Diff>.pw_sec` (colour sections) and `<Diff>.pw_geo` (track geometry: mesh chunks, props, decoration cubes), plus the audio (`songLocation`, e.g. `Assets/song.ogg`, only the file name is used) and an optional `poster.png`. The mod's C# classes (`AllTheClasses.cs`, `CustomLevels.cs`) deserialise them with Newtonsoft.Json; levels are authored in the Unity editor "Pweditor". The class definitions are the authority for field names; the PWCL structure doc page is empty.

## Container & encoding

- UTF-8 JSON, minified or indented. Levels ship as a `.zip` of the folder (sample `10 Second Test Level.zip`: `Easy.pw_beat`, `Easy.pw_geo`, `Easy.pw_koreo`, `Easy.pw_sec`, `level.pw`, `poster.png`, `.ogg`).
- `maps` in `level.pw` lists the difficulties (`["Easy"]`, `["Hard"]`). Vectors carry derived members (`Vector2Int`: `x`, `y`, `magnitude`, `sqrMagnitude`; `Quaternion`: `eulerAngles`).
- The official Pistol Mix tool uses `level.pw`, `.pw_event` (events and BPM, stored as audio samples, so set the right `.ogg` sample rate) and `.pw_art` (models) per mod.io's Geomancer guide; not examined.

## Structure / metadata
`level.pw` (`LevelInfo`):

| Field | Type | Meaning |
|---|---|---|
| `version` | float | 0.2 in samples |
| `sceneDisplayName` | string | e.g. `"Lily ~ Who knows~Me"` (song ~ artist~mapper) |
| `songDisplayName`, `songArtist`, `mapper`, `description` | string | metadata |
| `songLocation` | string | path to audio; only the final path component is used, file in the level folder |
| `songLength` | float | seconds |
| `tempo` | float | BPM (informational; timing comes from `.pw_koreo` and beat times) |
| `previewTime` | float | preview start, seconds |
| `maps` | string[] | difficulties present |
| `obstacleSet` | enum | `Normal` 0, `Spooky` 1, `Pipes` 2, `Rocks` 3, `AirDrop` 4, `Colony` 5, `Tower` 6, `EarthCracker` 7, `Crates` 8, `Train` 9 |
| `materialPropertiesSet` | enum | `Default`, `Heartbreaker`, `AlienPlanet_2089`, `Arbiter_2089`, `RobotFacilities_2089`, `StrangeCreatures_2089`, `Cave_AP2`, `Desert_AP2`, `WesternTown`, `OldWestTrain` |
| `enemySet` | enum | `Normal` 0, `Robots` 1, `Outlaws` 2 (selects which enemy names `type` accepts) |
| `moveMode` | enum | `Moving` 0, `Stationary` 1 (appears in samples) |
| `moveSpeed` | float | default 3 |
| `timingWindowSize` | float | default 150 (ms) [inference] |
| `customMainMenuColor` | `{Main, Fog, Glow, Enemy}` each `{a,r,g,b}` floats | menu colours |

`.pw_beat` (`BeatFile`): `{ "version": float, "beatData": [CustomBeat...], "beatTimes": [float...] }` where `beatTimes` repeats each beat's `time`.
- `CustomBeat`: `time` (float, seconds), `targets[]`, `obstacles[]`, `dynamicObstacles[]` (empty class in the mod).
- `CustomTargetData`: `type` (string, enum name of the enemy set: `Enemy_Normal`, `Enemy_Tough`, `Enemy_ChuckNorris`, `Enemy_2089_Minigun`, `Enemy_Shield`, `Enemy_2089_SentyGun`, `Enemy_HorseRider` for set 0; set 1 uses `Enemy_2089_1Shot`, `_2Shot`, `_4Shot`, ... `Enemy_AP2_HorseRider`; set 2 `Enemy_AP2_1Shot`..), `distance` (`Near`, `Middle`, `Far`), `placement` (`Vector2Int` x, y on the target grid), `enemyOffset` (`WorldPoint`: `position` vec3 + `rotation` quaternion), `enemySequence[]`, `bonusEnemy` (ignored for level rank), `shielded`, `noGround`, `noCarve`, `playerActionLerp`.
- `CustomEnemyAction`: `enemyAction` (0 Wait, 1 Move, 2 AimStart, 3 AimAndFire, 4 Fire, 5 AimStop, 7 StopFiring, 8 Despawn, 9 FacePlayerStart, 10 FacePlayerStop, 11 AimWithoutFacing) and `properties` (`duration`, `destination` WorldPoint, `isOverrideAnimationSpeed`, `animationSpeedOverride`, `facing`, `fireTime`, `stopFacingOnExit`, `stopLookingOnExit`, `action`, `triggerHash` [role unknown]). Actions run sequentially; `duration` accumulates into the sequence length.
- `CustomObstacleData`: `placement` (-3 EvenMoreLeft .. 3 EvenMoreRight, 0 Center) and `type` (0 Sidestep, 1 LimboTall, 2 LimboShort, 3 Wall).

`.pw_koreo` (`KoreographyBaseC`, Koreographer data): `mSampleRate` (48000 in the sample, default 44100), `mTempoSections[] {sectionName, startSample, samplesPerBeat, beatsPerMeasure, bStartNewMeasure}` (the sample file also has a `bpm` key per section that the mod ignores), `mTracks[] {mEventID, mEventList[] {mStartSample, mEndSample}}` with track IDs `Beat`, `NoBeat`, ... [others unknown].

`.pw_sec` (`Tdata`): `sections[] {name, start, end, bpm, beat, colorHue, colorSaturation, colorValue, fogColor, glowColor, mainColor, enemyColor, customEnemyColor}` and `colors[] {start, end, colors}` (color shifts; start/end converted with `*1000000` into the game's integer units).

`.pw_geo` (`Geoset`): `version`, `chunksForSlices[] {id, chunks[]}`, `chunks[] {id (Vector3Int), tris[] (indices), verts[] (vec3)}`, `decCubes[]`, `staticProps[] {pos, rot, scale, name, path}`, `dynamicProps[] {pos, rot, scale, Start, End, name}`, `spropNames[]`, `dpropNames[]`.

## Timing model

- Gameplay times are seconds: `CustomBeat.time` goes into the game's `BeatData(time)` and `beatTimes`; `songLength` is seconds. Sample: one enemy at `time` 4.902521 in a 10 s, 69 BPM song.
- `.pw_koreo` holds the musical grid in audio samples (`samplesPerBeat = sampleRate * 60 / bpm`, e.g. 41739.13 at 48 kHz and 69 BPM); the `Beat` track has one event per beat (start sample, end = start + 1). It drives background pulses and section changes; targets use `time` seconds.
- `.pw_sec` `start`/`end` are whole seconds in the sample (0..10). `colors[]` start/end are floats scaled by 1,000,000 by the loader [unit inference: seconds].
- Enemy sequences add durations (seconds); `fireTime` is relative to the sequence.

## Notes

- A note is a target (enemy) with `distance` and `placement`; `bonusEnemy` targets do not count for rank. Obstacles (walls, limbo bars, side steps) have a lateral `placement` -3..3. Simultaneous enemies are several `targets` entries.
- No holds. Enemy movement and firing are scripted with action sequences; the actions Strafe, Instant, Animation are commented out in the mod (unsupported).
- `moveMode` Stationary or Moving sets whether the player travels.

## Audio & images

`songLocation` ogg (loaded with `UnityWebRequest` from the level folder), `poster.png`, `previewTime`.

## Versions & variants

`version` 0.2 for `level.pw`, `.pw_beat`, `.pw_geo`. Official Pistol Mix files (`level.pw`, `.pw_event`, `.pw_art`) are undocumented here; compatibility with PWCL files is unknown.

## Quirks & pitfalls

- Ignore the serialised Unity members (`magnitude`, `sqrMagnitude`, `eulerAngles`).
- Enemy `type` names come from `enemySet`; a name from another set throws on load (`Enum.Parse`).
- `bpm` appears in several files with different roles; `Tdata.sections[].bpm` was 2022.0 in the sample (placeholder).
- The audio sample rate must match `mSampleRate`.

## Example

Real `Easy.pw_beat` of the PWCL sample "10 Second Test Level" (one enemy at 4.902521 s; line breaks added; origin `levels/10 Second Test Level/10 Second Test Level.zip` in https://gitlab.com/pwcl/custom-levels):

```json
{"version":0.2,"beatData":[{"time":4.902521,"targets":[{"type":"Enemy_Normal","distance":"Near",
 "placement":{"x":0,"y":0,"magnitude":0.0,"sqrMagnitude":0},
 "enemyOffset":{"position":{"x":0.0,"y":0.0,"z":0.0},"rotation":{"w":-4.371139E-08,"x":0.0,"y":1.0,"z":0.0,"eulerAngles":{"x":0.0,"y":180.0,"z":0.0}}},
 "enemySequence":[],"bonusEnemy":false,"shielded":false,"noGround":false,"noCarve":false,"playerActionLerp":0.0}],
 "obstacles":[],"dynamicObstacles":[]}],"beatTimes":[4.902521]}
```

## ROX support

Not read by ROX. The target grid and enemy scripts do not map to columns; a decoder could keep beat times plus x placement.

## Parsers & tools
- PWCL mod (C#, MelonLoader/Harmony, Newtonsoft.Json): https://gitlab.com/pwcl/mod
- PWCL editor (Unity project): https://gitlab.com/pwcl/editor
- Level library: https://gitlab.com/pwcl/custom-levels
- Official Pistol Mix and Geomancer (mod.io): https://mod.io/g/pistol-whip

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md) (levels from gitlab.com/pwcl/custom-levels; no `.ogg`, no posters, `.pw_geo` over 20 MB skipped). More: the PWCL editor (https://gitlab.com/pwcl/editor) and docs (https://pwcl.givo.xyz/). Official Pistol Mix levels (`level.pw` + `.pw_event` + `.pw_art`) are on mod.io (JavaScript-rendered; not examined).

## Sources
- https://gitlab.com/pwcl/mod (`Pistol Whip Custom Levels/AllTheClasses.cs`, `CustomLevels.cs`)
- https://gitlab.com/pwcl/custom-levels (`levels/*/level.pw`, the `10 Second Test Level` zip)
- https://pwcl.givo.xyz/ (docs: `home.md`, `editor/*.md`)
- https://mod.io/g/pistol-whip/r/geomancer and https://mod.io/g/pistol-whip/r/official-pistol-mix-how-to-guide (seen via search results; pages are JavaScript-rendered)
