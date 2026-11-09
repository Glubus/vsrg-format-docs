# Pistol Whip Custom Levels folder (`level.pw`, `.pw_beat`, `.pw_koreo`, `.pw_sec`, `.pw_geo`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json (several files per level)

## Overview
The PWCL (Pistol Whip Custom Levels) mod by Givo loads levels from `./Custom Levels/<LevelName>/` next to the game. A level is a folder of JSON files: `level.pw` (metadata and global settings), then one set per difficulty named `Easy`, `Normal` or `Hard`: `<Diff>.pw_beat` (the actual gameplay chart: enemies and obstacles on beats), `<Diff>.pw_koreo` (a Koreographer tempo map and beat/event tracks), `<Diff>.pw_sec` (colour sections), `<Diff>.pw_geo` (track geometry: mesh chunks, props, decoration cubes), plus the audio (`songLocation`, e.g. `Assets/song.ogg`, only the file name is used) and an optional `poster.png`. The mod's C# model classes (`AllTheClasses.cs`) and a loader (`CustomLevels.cs`) deserialise them with Newtonsoft.Json; levels are authored in a Unity-based editor ("Pweditor"). The class definitions are the authority for field names; the PWCL structure doc page is still empty.

## Container & encoding
- JSON, UTF-8 (the files in the level repository are minified or indented). Levels are shared as `.zip` of the folder (sample: `10 Second Test Level.zip`: `Easy.pw_beat`, `Easy.pw_geo`, `Easy.pw_koreo`, `Easy.pw_sec`, `level.pw`, `poster.png`, `.ogg`).
- The `maps` array in `level.pw` lists which difficulties exist (`["Easy"]`, `["Hard"]`). Vectors are serialised with all derived members (e.g. `Vector2Int` has `x`, `y`, `magnitude`, `sqrMagnitude`; `Quaternion` includes `eulerAngles`).
- The official Pistol Mix tool uses `level.pw` (level info), `.pw_event` (events and BPM; values stored internally as audio samples, so the right sample rate for the `.ogg` must be set) and `.pw_art` (models) per mod.io's Geomancer guide; those files were not examined here.

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
- Gameplay times are **seconds**: `CustomBeat.time` goes straight into the game's `BeatData(time)` and the `beatTimes` list; `songLength` is in seconds. Sample: a one-enemy level at 69 BPM with `time` 4.902521 on a 10 s song.
- `.pw_koreo` defines the musical grid in audio **samples** (`samplesPerBeat = sampleRate * 60 / bpm`, e.g. 41739.13 at 48 kHz and 69 BPM); the `Beat` track holds one event per beat (start sample, end = start + 1). Koreography drives the rhythmic background (pulses, section changes); targets are placed by `time` seconds.
- `.pw_sec` `start`/`end` use whole-second positions in the sample (0..10 for a 10 s song). `colors[]` start/end are floats scaled by 1,000,000 by the loader [unit inference: seconds].
- Enemy sequences add durations (seconds); `fireTime` is relative to the sequence.

## Notes
- A "note" is a target (enemy) with `distance` and `placement`; shooting happens when the player aims at it on the beat; `bonusEnemy` targets do not count for rank. Obstacles (walls, limbo bars, side steps) have a lateral `placement` -3..3. Simultaneous enemies are several entries in `targets`.
- There are no holds. Enemy movement and firing are scripted with action sequences; some actions (Strafe, Instant, Animation) are commented out in the mod and thus unsupported.
- `moveMode` Stationary versus Moving changes whether the player travels.

## Audio & images
`songLocation` ogg, `poster.png` (level poster), `previewTime`. The mod's loader requests the audio with `UnityWebRequest` from the level folder.

## Versions & variants
- `version` 0.2 for `level.pw` and `.pw_beat`/`.pw_geo`.
- Official Pistol Mix files (mod.io) use `level.pw` plus `.pw_event`/`.pw_art`; their structure is not documented in sources opened here, so compatibility with the PWCL files is unknown.

## Quirks & pitfalls
- Derived Unity members are serialised (`magnitude`, `sqrMagnitude`, `eulerAngles`); parsers must ignore them.
- Enemy type names are enum names chosen by `enemySet`; using a name from another set throws on load (`Enum.Parse`).
- `bpm` fields appear in several files with different roles (tempo, samples per beat); `Tdata.sections[].bpm` was 2022.0 in the sample (a placeholder).
- Audio sample rate must match `mSampleRate`.

## Example
Real file, `Easy.pw_beat` from the PWCL repository sample "10 Second Test Level" (one enemy at 4.902521 s):
```json
{"version":0.2,"beatData":[{"time":4.902521,"targets":[{"type":"Enemy_Normal","distance":"Near",
 "placement":{"x":0,"y":0,"magnitude":0.0,"sqrMagnitude":0},
 "enemyOffset":{"position":{"x":0.0,"y":0.0,"z":0.0},"rotation":{"w":-4.371139E-08,"x":0.0,"y":1.0,"z":0.0,"eulerAngles":{"x":0.0,"y":180.0,"z":0.0}}},
 "enemySequence":[],"bonusEnemy":false,"shielded":false,"noGround":false,"noCarve":false,"playerActionLerp":0.0}],
 "obstacles":[],"dynamicObstacles":[]}],"beatTimes":[4.902521]}
```
(Line breaks added; origin: `levels/10 Second Test Level/10 Second Test Level.zip` in https://gitlab.com/pwcl/custom-levels.)

## ROX support
Not read by ROX. Target grid and enemy scripts do not map to columns; a decoder could keep only beat times plus x placement.

## Parsers & tools
- PWCL mod (C#, MelonLoader/Harmony, Newtonsoft.Json): https://gitlab.com/pwcl/mod
- PWCL editor (Unity project): https://gitlab.com/pwcl/editor
- Level library: https://gitlab.com/pwcl/custom-levels
- Official Pistol Mix and Geomancer (mod.io): https://mod.io/g/pistol-whip

## Sources
- https://gitlab.com/pwcl/mod (`Pistol Whip Custom Levels/AllTheClasses.cs`, `CustomLevels.cs`)
- https://gitlab.com/pwcl/custom-levels (`levels/*/level.pw`, the `10 Second Test Level` zip)
- https://pwcl.givo.xyz/ (docs: `home.md`, `editor/*.md`)
- https://mod.io/g/pistol-whip/r/geomancer and https://mod.io/g/pistol-whip/r/official-pistol-mix-how-to-guide (seen via search results; pages are JavaScript-rendered)
