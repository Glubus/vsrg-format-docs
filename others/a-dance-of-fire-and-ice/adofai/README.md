# ADOFAI level (`.adofai`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview
`.adofai` is the level file of "A Dance of Fire and Ice" (7th Beat Games). It is JSON-like text with five top-level members: `settings`, `angleData` (or legacy `pathData`), `actions`, `decorations`. Each tile of the path is one hit. Official format documentation does not exist in the sources found; everything here comes from community libraries and docs (ADOFAI Expansion, ADOFAI-JS, adofaipy, RhythmBase). Level counts are large (Steam Workshop and community); great chart volume but no vsrg structure.

## Container & encoding
- Text file, **non-strict JSON**: parsers must handle trailing commas (`,]`, `,}`), raw newlines inside strings and a UTF-8 BOM (ADOFAI-JS StringParser handles "trailing commas, raw newlines in strings"; BufferParser strips the BOM; ADOFAI_auto reads with `utf-8-sig` and removes `,]`, `,}` and `,,`; its pre-pass also inserts a missing comma between `]` and the next key).
- Very large levels exist (ADOFAI-JS LargeFileParser thresholds at 50 MB / 100 MB); `angleData` is a long numeric array.
- One file per level; assets (audio, images, videos) are referenced by filename in the same folder; `.zip` packages are mentioned by RhythmBase ("Archive: `.zip`").

## Structure / metadata
```
{ "angleData": [ ... ],   // or "pathData": "RUL..."
  "settings": { ... },
  "actions": [ {"floor": n, "eventType": "...", ...}, ... ],
  "decorations": [ {...}, ... ] }
```
(ADOFAI-JS README: `{ angleData, settings, actions, decorations }`; ADOFAI Expansion also lists `pathData`.)

### `settings` (JSON key names confirmed from sources: `bpm`, `pitch`, `offset`, `countdownTicks`, `songFilename`, `volume`, `hitsound`, `hitsoundVolume`; other keys follow RhythmBase `Settings.cs`, where JSON name = lowerCamelCase of the C# property [inference])
| Key | Meaning | RhythmBase default |
|---|---|---|
| `version` | Format version | DefaultVersion |
| `artist`, `song`, `author` | Artist, song name, level author | "" |
| `songFilename` | Audio file | "" |
| `bpm` | Base BPM | 100 |
| `volume` | Music volume | 100 |
| `offset` | Audio offset in ms | 0 |
| `pitch` | Playback speed percent | 100 |
| `hitsound`, `hitsoundVolume` | Hit sound name, volume | Kick, 100 |
| `countdownTicks` | Count-in ticks before start | 4 |
| `separateCountdownTime`, `previewImage`, `previewIcon`, `previewIconColor`, `previewSongStart`, `previewSongDuration`, `seizureWarning`, `levelDesc`, `levelTags`, `artistLinks`, `speedTrialAim`, `difficulty`, `requiredMods` | Selection screen metadata | |
| `tileShape`, `trackColorType`, `trackColor`, `secondaryTrackColor`, `trackColorAnimDuration`, `trackColorPulse`, `trackPulseLength`, `trackStyle`, `trackTexture`, `trackTextureScale`, `trackGlowIntensity`, `trackAnimation`, `beatsAhead`, `trackDisappearAnimation`, `beatsBehind` | Track appearance | |
| `backgroundColor`, `showDefaultBGIfNoImage`, `showDefaultBGTile`, `defaultBGTileColor`, `defaultBGTileShapeType`, `defaultBGShapeColor`, `bgImage`, `bgImageColor`, `parallax`, `bgDisplayMode`, `imageSmoothing`, `lockRot`, `loopBG`, `bgVideo`, `loopVideo`, `vidOffset` | Background | |
| `relativeTo`, `position`, `rotation`, `zoom`, `pulseOnFloor`, `scalingRatio` | Camera | |
| `floorIconOutlines`, `stickToFloors`, `planetEase`, `planetEaseParts`, `planetEasePartBehavior`, `customClass`, `defaultTextColor`, `defaultTextShadowColor`, `congratsText`, `perfectText`, `legacyFlash`, `legacyCamRelativeTo`, `legacySpriteTiles`, `legacyTween`, `disableV15Features` | Misc and legacy flags | |

### `angleData` / `pathData`
- `angleData`: array of numbers, one per tile after the start tile. Each value is the direction of the path from the previous tile to this one, in degrees: 0 = right, 90 = up (adofaipy: "0 degrees is facing right, 90 degrees is facing upwards"). `999` marks a **midspin** tile (ADOFAI_auto/adofaipy/ADOFAI-JS: "999 (endpoint)" in the ADOFAI Expansion table). ADOFAI_auto prepends 0 as the angle of the (implicit) start tile (tile 0, floor 0).
- `pathData` (legacy, older versions): a string, one character per tile. Absolute table (ADOFAI Expansion): R 0, p 15, J 30, E 45, T 60, o 75, U 90, q 105, G 120, Q 135, H 150, W 165, L 180, x 195, N 210, Z 225, F 240, V 255, D 270, Y 285, B 300, C 315, M 330, A 345, `!` = 999 (midspin). Relative offset characters: `5` +72, `6` -72, `7` +52, `8` -52, `9` -30, `h` +120, `j` -120, `t` +60, `y` +300 (added to the previous angle). (ADOFAI_auto uses negative equivalents for D, C, Z, N, F, B, M, V, A, i.e. same angle mod 360.) Unknown characters: keep the current angle.

### `actions[]` (events)
Each: `{"floor": <tile index>, "eventType": "<Name>", ...fields}`. `floor` 0 is the start tile. Known `eventType` values (ADOFAI-JS 57 interfaces): `SetSpeed`, `Twirl`, `Checkpoint`, `MoveCamera`, `CustomBackground`, `ChangeTrack`, `ColorTrack`, `AnimateTrack`, `RecolorTrack`, `MoveTrack`, `SetText`, `Flash`, `SetHitsound`, `SetFilter`, `SetFilterAdvanced`, `SetPlanetRotation`, `HallOfMirrors`, `ShakeScreen`, `MoveDecorations`, `PositionTrack`, `RepeatEvents`, `Bloom`, `Hold`, `SetHoldSound`, `SetConditionalEvents`, `ScreenTile`, `ScreenScroll`, `EditorComment`, `Bookmark`, `CallMethod`, `AddComponent`, `PlaySound`, `MultiPlanet`, `FreeRoam`, `FreeRoamTwirl`, `FreeRoamRemove`, `Pause`, `AutoPlayTiles`, `Hide`, `ScaleMargin`, `ScaleRadius`, `Multitap`, `TileDimensions`, `KillPlayer`, `ScalePlanets`, `SetFloorIcon`, and decoration-related ones (`AddDecoration`, `AddText`, `AddObject`, `SetObject`, ...; list truncated in the source).
Timing-relevant ones (fields seen in sources):
- `SetSpeed`: `speedType` (`Multiplier` or BPM), `bpmMultiplier`, `beatsPerMinute`; the example in ADOFAI-JS also shows `speed`.
- `Twirl`: `{ "floor": 10, "eventType": "Twirl" }` reverses rotation direction (the Expansion example also shows a `twirl: true` flag).
- `Pause`, `Hold`, `MultiPlanet`, `Multitap`, `FreeRoam*`, `SetPlanetRotation`, `AutoPlayTiles`: change timing or input semantics; fields Unknown here (see ADOFAI-JS event interfaces).
- `Checkpoint`, `SetHitsound`, ... gameplay support events.

### `decorations[]`
Free-form decoration objects (sprites, texts, objects) with `floor` or fixed positions. Not documented here.

## Timing model
- Beat length (seconds) = 60 / (bpm) x (100 / pitch). In ADOFAI_auto: `delay = 100 * degree / bpm / pitch / 3`, i.e. `(100/pitch) * (60/bpm) * degree/180`, so **180 degrees of rotation = one beat**, no matter the tile.
- The time between tile i and tile i+1 = (rotation angle between them) / 180 beats. The rotation angle: `interior = 180 + angleData[i-1]` (the planet enters tile i from the opposite direction of the incoming path), `rot = normalize(spin * (angleData[i] - interior))` in (0, 360] with `spin = +1/-1` (ADOFAI_auto: initial spin -1, flipped at every `Twirl` on the tile, `normalize_degree` maps 0 to 360). For the first tile the previous angle is 0 (implicit start). A midspin tile (999) is skipped: its predecessor angle is reused and no hit is made on it.
- BPM changes: `SetSpeed` on a tile changes bpm from that tile on (`Multiplier` multiplies the current bpm, otherwise absolute `beatsPerMinute`).
- Start: `countdownTicks * 60 / bpm * 100/pitch + offset/1000` seconds before the first hit (ADOFAI_auto `play()`); `offset` (ms) shifts the audio.
- Hit times are therefore a cumulative sum; there is no explicit time field. Events other than SetSpeed/Twirl/Pause/Hold/Multitap/FreeRoam do not affect timing.

## Notes
Every tile (except midspins) = one tap in time with the planet landing. `Hold` events make a held tile; `Multitap` requires several presses; `Pause` inserts a pause; `MultiPlanet` adds planets; `FreeRoam` events add free-movement sections. Details Unknown here. For a vsrg-like conversion: the tile sequence maps to a one-key chart with times computed as above; geometry (angles, camera, tile positions) is lost.

## Audio & images
`songFilename`, `bgImage`, `bgVideo`, `previewImage`, `previewIcon`, `trackTexture` + sprite filenames in decorations; all relative to the level file.

## Versions & variants
- `pathData` (old) vs `angleData` (current); both supported by ADOFAI-JS and ADOFAI_auto. `settings.version` is the format version; `legacy*` flags and `disableV15Features` keep old behaviour of earlier versions. Exact version history Unknown.
- Modded levels may carry extra keys/events (custom filters, `CallMethod`, `AddComponent`).

## Quirks & pitfalls
- Trailing commas and raw newlines inside strings break strict JSON parsers.
- `floor` indexes the start tile as 0, but `angleData[0]` describes tile 1.
- `angleData` may contain floating values, negative values (pathData conversion of `D` gives -90 in ADOFAI_auto) and 999.
- Event order inside `actions` is not guaranteed to be by floor.
- Huge files (tens of MB).
- Twirl state is cumulative along the path.

## Example
From the ADOFAI Expansion docs (https://learn.modrift.org/libs/level-format): the event
```json
{ "floor": 10, "eventType": "Twirl", "twirl": true }
```
and `pathData` `"REJW"` converts to `angleData` `[0, 45, 30, 165]`.

## ROX support
Not read by ROX.

## Parsers & tools
- ADOFAI-JS (TypeScript): https://github.com/adofaiex/ADOFAI-JS
- SharpFAI (C#): https://github.com/adofaiex/SharpFAI
- RhythmBase.Adofai (C#): https://github.com/RDCN-Community-Developers/RhythmToolkit
- adofaipy (Python): https://github.com/M1n3c4rt/adofaipy
- ADOFAI_auto (Python, autoplay script): https://github.com/UminChoi/ADOFAI_auto
- adofai-lib (npm): https://npm.io/package/adofai-lib
- ADOFAI Music Converter (MIDI/WAV to level): https://maicy0609.github.io/ADOFAI_Converter

## Sources
- https://learn.modrift.org/libs/level-format
- https://raw.githubusercontent.com/adofaiex/ADOFAI-JS/main/README.md
- https://raw.githubusercontent.com/UminChoi/ADOFAI_auto/master/adofaiAuto_module.py
- https://raw.githubusercontent.com/RDCN-Community-Developers/RhythmToolkit/master/RhythmBase.Adofai/Adofai/Components/Settings.cs
- https://raw.githubusercontent.com/M1n3c4rt/adofaipy/main/README.md
- https://github.com/RDCN-Community-Developers/RhythmToolkit
