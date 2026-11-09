# Quaver map (`.qua`)
Kind: chart

Doc status: complete · ROX: reads/writes (only Keys4 and Keys7; many Quaver features dropped) · Category: vsrg · Encoding: text (YAML)

## Overview
`.qua` is the YAML map file of Quaver (one file per difficulty). The `Qua` class of the open-source `Quaver.API` library (MPL-2.0) is the reference implementation. Quaver converts `.osz`, `.sm`, `.mcz`/`.mc` and `.qp` imports to `.qua` (`Quaver.Tools`: `ConvertOsuCommand`, `ConvertSmCommand`). Files live in `.qp` mapset archives (../qp/README.md), Quaver's `Songs/` folder, quavergame.com and the Quaver.API test resources.

## Packaged in

- `.qp` (zip of a Quaver mapset: one `.qua` per difficulty, audio, background, banner, hit samples).

## Container & encoding
- UTF-8 YAML (YamlDotNet). `Qua.Parse` deserializes with `IgnoreUnmatchedProperties()`, so unknown keys are ignored. A real Quaver.API test file starts with two U+FEFF BOM characters; strip them for strict YAML parsers. [observed: `AutoMods/Resources/short-ln.qua`]
- Keys are the PascalCase C# property names. Enums are written by name (`Mode: Keys4`, `Signature: Triple`, `Type: Mine`, flags like `HitSound: Whistle, Finish` [inference: YamlDotNet's default for `[Flags]` enums]).
- The writer (`Qua.Serialize`) sorts the map, sets `QuaVersion` to the minimum needed and omits defaults ("Set default values to zero so they don't waste space"): `Signature` (4/4), `HitSound` (Normal), `Volume` (100), `TimingGroup` (`$Default`), empty `Bookmarks`, `ScrollSpeedFactors`, `TimingGroups`. Line endings are `\r\n`. The reader restores defaults (`RestoreDefaultValues`), so treat every missing key as its default.
- File name is free (often `<mapid>.qua`). ROX limit: 100 MiB.

## Structure / metadata

Top-level keys (from `Qua.cs`):

| Key | Type | Meaning |
|---|---|---|
| `QuaVersion` | int | 0 = no versioning, 1 = contains mines. The reader refuses a version greater than `CurrentQuaVersion` (= 1) with a `QuaVersionException` |
| `AudioFile` | string | audio file name in the map folder |
| `SongPreviewTime` | int ms | preview start |
| `BackgroundFile` | string | |
| `BannerFile` | string | mapset banner |
| `MapId`, `MapSetId` | int | online ids; `-1` = not submitted |
| `Mode` | enum | `Keys4`, `Keys7`, `Keys1`, `Keys2`, `Keys3`, `Keys5`, `Keys6`, `Keys8`, `Keys9`, `Keys10` (C# numeric values 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in this order: Keys4 = 1, Keys7 = 2, Keys1 = 3, Keys2 = 4, Keys3 = 5, Keys5 = 6 ...; `GameMode.cs`) |
| `HasScratchKey` | bool | adds one scratch lane (the last) to the key count (5/8 key play: `Keys4`+scratch, `Keys7`+scratch) |
| `Title`, `Artist`, `Source`, `Tags`, `Creator`, `DifficultyName`, `Description`, `Genre` | string | `Tags` is a single string (comma or space separated by convention) |
| `LegacyLNRendering` | bool | old long note rendering (earliest/latest to start/end) |
| `BPMDoesNotAffectScrollVelocity` | bool | see Timing model |
| `InitialScrollVelocity` | float | initial SV multiplier before the first `SliderVelocities` entry; only meaningful when `BPMDoesNotAffectScrollVelocity: true` |
| `EditorLayers` | list | editor layers: `Name`, `Hidden`, `ColorRgb` (`"r,g,b"`) |
| `Bookmarks` | list | `StartTime` (int ms), `Note`, `ColorRgb` (default `255,255,0`) |
| `CustomAudioSamples` | list | `Path`, `UnaffectedByRate` (bool) |
| `SoundEffects` | list | `StartTime` (float ms), `Sample` (1-based index into `CustomAudioSamples`), `Volume` (1-100; omitted = 100) |
| `TimingPoints` | list | see Timing model |
| `SliderVelocities` | list | `StartTime` (float ms), `Multiplier` (float) |
| `ScrollSpeedFactors` | list | `StartTime`, `Multiplier`; scroll speed factors of the default group |
| `HitObjects` | list | see Notes |
| `TimingGroups` | map | id -> group (tag `!ScrollGroup`); reserved ids `$Default` (not serialized; the top-level `SliderVelocities`/`ScrollSpeedFactors`/`InitialScrollVelocity` belong to it) and `$Global` (applies to every group; omitted when empty). A group has `ColorRgb`, `Hidden`, `InitialScrollVelocity`, `ScrollVelocities`, `ScrollSpeedFactors` |

`Qua.Validate()` (run by `Parse(..., checkValidity: true)`, which throws `ArgumentException` listing the errors) requires: at least one hit object; at least one timing point; `Mode` a defined `GameMode`; each sound effect `Sample` in `[1, CustomAudioSamples.Count]` and `Volume` in 1..100; each long note `EndTime > StartTime`; each key sound `Sample` in `[1, Count]` and `Volume >= 1`.

## Timing model
- All times are ms from the audio start. `HitObjects` `StartTime`/`EndTime` are ints; timing points, SVs and sound effects are floats. `Sort()` orders all lists by time after loading.
- `TimingPoints`: `StartTime` (float ms), `Bpm` (float), `Signature` (`Quadruple` = 4/4, default and omitted; `Triple` = 3/4), `Hidden` (editor-only). Beat length = `60000 / Bpm` ms (`MillisecondsPerBeat`). Several points may share a timestamp; the last wins for SV bookkeeping (`NormalizeSVs`).
- Hit objects are in ms; beats matter only for snapping and SV normalisation.
- Scroll velocity (`SliderVelocities`): `Multiplier` changes scroll speed from `StartTime` until the next entry; it never changes hit timing. Two representations (`Qua.cs` comments):
  - `BPMDoesNotAffectScrollVelocity: false` (or absent: old maps, osu!/StepMania conversions), "denormalized": effective multiplier is `SV multiplier * (currentBpm / baseBpm)`, where `baseBpm` is the most common BPM weighted by duration up to the last object (`GetCommonBpm`). Every timing point resets the active SV multiplier to 1 unless an SV starts at the same time.
  - `true`, "normalized": the multiplier is used as is; `InitialScrollVelocity` applies before the first SV. `NormalizeSVs()` / `DenormalizeSVs()` convert between the two (infinite BPM counts as multiplier 128).
- `ScrollSpeedFactors` (SSF) and `TimingGroups` give independent per-group scrolling (objects reference a group with `TimingGroup`); `$Global` applies on top of every group. SSF rendering formulas: Unknown.
- Converting to ROX needs the denormalized form normalised first; the ROX decoder does not.

## Notes

`HitObjects` entry (`HitObjectInfo`):

| Key | Type | Meaning |
|---|---|---|
| `StartTime` | int ms | |
| `Lane` | int | 1-based lane (1 = leftmost). With `HasScratchKey` the scratch lane is `Lane == key count` (the last one) |
| `EndTime` | int ms | `0` / absent = tap; `> 0` = long note (`IsLongNote => EndTime > 0`); must be `> StartTime` |
| `HitSound` | flags | `Normal` 1, `Whistle` 2, `Finish` 4, `Clap` 8 (`Hitsounds.cs`); `Normal` plays when the value is 0 or 1; written as 0 when `Normal` |
| `Type` | enum | `Normal` (0) or `Mine` (1; hit = miss; makes `QuaVersion` 1) |
| `KeySounds` | list | `{ Sample: <1-based index into CustomAudioSamples>, Volume: <1-100, omitted = 100> }`; several per object allowed |
| `EditorLayer` | int | index into `EditorLayers` (0 = none), editor only |
| `TimingGroup` | string | scroll group id; omitted = `$Default` |

- Taps, long notes and mines only; no bursts/rolls. A long note's end is a separate judgement (`JudgementCount` 2); mines count 1 and are excluded from difficulty (`DifficultyContributingHitObjects`). Chords are allowed.
- Key count = `Mode` (Keys1..Keys10) plus 1 if `HasScratchKey` (`ModeHelper.ToKeyCount`); `FromKeyCount` is the inverse (1..10).
- `SoundEffects` play background samples; `UnaffectedByRate` samples keep pitch/speed under rate mods.

## Audio & images
`AudioFile`, `BackgroundFile`, `BannerFile` are file names relative to the `.qp` root; `CustomAudioSamples[].Path` are relative wav/ogg/mp3 files. `HitObjects[].KeySounds` and `SoundEffects[]` use 1-based indexes into `CustomAudioSamples`.

## Versions & variants
- `QuaVersion` 0 = original, 1 = mines. `DetermineMinimumQuaVersion()` writes 1 only if a mine exists. Reject `QuaVersion > 1` or ignore the unknown features.
- Older files lack `TimingGroups`, `ScrollSpeedFactors`, `HasScratchKey`, `BPMDoesNotAffectScrollVelocity`, `LegacyLNRendering`, `Genre`.
- osu!/StepMania conversions use `BPMDoesNotAffectScrollVelocity` false and long lists of 1-ms-apart timing points (test resource `Osu/Resources/Camellia - Backbeat Maniac (Evening) [Rewind VIP].qua`, thousands of `TimingPoints`).

## Quirks & pitfalls
- Lanes are 1-based; osu!/ROX columns are 0-based.
- `EndTime: 0` means tap, not a zero-length hold.
- `Tags` is one string; `Source`/`BackgroundFile` may be `''`.
- `StartTime` is float for timing points/SVs, int for hit objects.
- Denormalized SV is the default and depends on BPM: reading `Multiplier` at face value gives the wrong scroll speed on BPM-change maps (hit timing stays correct).

## Example

Real test resource of Quaver.API (`Quaver.API.Tests/Quaver/Resources/keysounds.qua`, MPL-2.0), complete file:

```yaml
Mode: Keys4
CustomAudioSamples:
- Path: hello.wav
- Path: world.mp3
  UnaffectedByRate: yes
TimingPoints:
- StartTime: 0
  Bpm: 88.5
HitObjects:
- StartTime: 500
  Lane: 2
  KeySounds:
  - Sample: 1
  - Sample: 2
    Volume: 50
- StartTime: 500
  Lane: 3
  KeySounds:
  - Sample: 2
- StartTime: 500
  Lane: 4
```

Three notes at 500 ms in lanes 2, 3 and 4; the first plays `hello.wav` at 100 % and `world.mp3` at 50 %.

## ROX support
ROX source `src/formats/qua` (`serde_yaml`, UTF-8, 100 MiB). Read + write.
- Reads `AudioFile`, `SongPreviewTime`, `BackgroundFile`, `MapId`/`MapSetId` (only if > 0), `Mode`, `Title`, `Artist`, `Source`, `Tags` (split on whitespace), `Creator`, `DifficultyName`, `TimingPoints` (`Bpm` + `Signature` -> 4 or 3), `SliderVelocities`, `InitialScrollVelocity`, `HitObjects` (`StartTime`, `Lane` - 1, optional `EndTime`).
- Only `Mode: Keys4` and `Keys7` (`QuaMode`); any other value fails deserialisation. Missing `Mode` is `Keys4`.
- `InitialScrollVelocity` (finite, != 1) becomes an SV point at map start (changelog 0.8.0). `SliderVelocities` become `TimingPoint::Sv` with the raw multiplier. `BPMDoesNotAffectScrollVelocity` is parsed but unused, so denormalized maps get wrong SV semantics.
- Dropped: `HitSound`, `KeySounds`, `Type: Mine` (decodes as a tap), `EditorLayer`, `TimingGroup`/`TimingGroups`, `ScrollSpeedFactors`, `SoundEffects`, `CustomAudioSamples`, `Bookmarks`, `EditorLayers`, `HasScratchKey` (the scratch lane would exceed the key count and fail validation `InvalidColumn`), `LegacyLNRendering`, `Hidden`, `Genre`, `Description`, `BannerFile`.
- A hold is decoded whenever `EndTime` is present, so an explicit `EndTime: 0` gives a negative-duration hold (validation error) [inference from `decoder.rs`: `if let Some(end) = ho.end_time { Note::hold(time, end - time, ..) }`].
- Encode writes `AudioFile`, `SongPreviewTime`, `BackgroundFile`, `MapId`, `Title`, `Artist`, `Creator`, `DifficultyName`, `Source`, `Tags` (space-joined), `BPMDoesNotAffectScrollVelocity: true`, `InitialScrollVelocity: 1.0`, BPM points (signature omitted), SV points, hit objects (lane + 1, `EndTime` for holds). It never sets `Mode` (`to_qua` uses the default), so a 7K chart is written as `Mode: Keys4` [from reading the source; not run]. Burst/Mine notes are written like taps/holds.

## Parsers & tools

| Name | Language | URL |
|---|---|---|
| Quaver.API (`Qua`, reference) | C# | https://github.com/Quaver/Quaver.API |
| Quaver (game, editor, importer) | C# | https://github.com/Quaver/Quaver |
| ROX `formats/qua` | Rust | vendored in this repository |
| map-parser (`QuaverMap`, `QuaverMapset`) | Rust | https://docs.rs/map-parser |
| qua3osu / qua2osu (Quaver -> osu!) | C# / Python | https://github.com/IceDynamix/qua3osu , https://github.com/IceDynamix/qua2osu |
| Moonchart (`Quaver`) | Haxe | https://github.com/MaybeMaru/moonchart |

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: Quaver's editor writes `.qua` into the Songs folder; every mapset on https://quavergame.com is a `.qp` (a ZIP); Quaver converts `.osz`, `.sm` and `.mcz` on import (`MapsetImporter.AcceptedMapType`); the Quaver repository ships 11 default `.qp` under `Quaver.Resources/Quaver.Resources/DefaultMaps/`. Scratch, mines and timing groups appear only in recent community maps or current Quaver.API tests (the pinned a921d56 snapshot has none).

## Sources

- https://github.com/Quaver/Quaver.API/blob/master/Quaver.API/Maps/Qua.cs and `Maps/Structures/{HitObjectInfo,TimingPointInfo,SliderVelocityInfo,SoundEffectInfo,CustomAudioSampleInfo,KeySoundInfo,BookmarkInfo,EditorLayerInfo,ScrollGroup,ScrollSpeedFactorInfo,TimingGroup}.cs`, `Enums/{GameMode,HitObjectType,Hitsounds,TimeSignature}.cs`, `Helpers/ModeHelper.cs`
- https://github.com/Quaver/Quaver.API/tree/master/Quaver.API.Tests (test resources `.qua`)
- https://github.com/Quaver/Quaver/blob/master/Quaver.Shared/Database/Maps/MapsetImporter.cs
- https://wiki.quavergame.com/docs/faq (import of `.osz`, `.sm`, `.mcz`)
- ROX source: `src/formats/qua/{types,parser,decoder,encoder}.rs`, `CHANGELOG.md` (0.8.0)
