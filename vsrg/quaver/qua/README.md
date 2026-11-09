# Quaver map (`.qua`)
Kind: chart

Doc status: complete · ROX: reads/writes (only Keys4 and Keys7; many Quaver features dropped) · Category: vsrg · Encoding: text (YAML)

## Overview

`.qua` is the map file of **Quaver**, an open-source, community-driven, 4K/7K-centred VSRG (C#, MonoGame, on Steam; developers Swan and the Quaver team, 2017-). One `.qua` file is one difficulty. The format is plain YAML, written and read by the `Qua` class of the open-source `Quaver.API` library (MPL-2.0), which is the reference implementation. Quaver imports `.osz`, `.sm`, `.mcz`/`.mc` and `.qp` and converts them to `.qua` (`Quaver.Tools` has `ConvertOsuCommand`, `ConvertSmCommand`). Files are found inside `.qp` mapset archives ([../qp/README.md](../qp/README.md)), in Quaver's `Songs/` folder, on quavergame.com and in the Quaver.API test resources.

## Packaged in

- Packaged in [`qp`](../qp/).

## Container & encoding

- UTF-8 YAML (parsed with YamlDotNet; `Qua.Parse` decodes the bytes with `Encoding.UTF8` and deserializes with `IgnoreUnmatchedProperties()`, so unknown keys are ignored). A real test file in Quaver.API starts with two U+FEFF BOM characters; strip BOMs before handing the text to a strict YAML parser. [observed in `AutoMods/Resources/short-ln.qua`]
- Key names are PascalCase, exactly the C# property names. Enums are written by name (`Mode: Keys4`, `Signature: Triple`, `Type: Mine`, flags like `HitSound: Whistle, Finish` [inference: YamlDotNet's default for `[Flags]` enums]).
- The writer (`Qua.Serialize`) sorts the map, sets `QuaVersion` to the minimum needed, and writes default values as zero/null so that they are omitted ("Set default values to zero so they don't waste space"): `Signature` (4/4), `HitSound` (Normal), `Volume` (100), `TimingGroup` (`$Default`), empty `Bookmarks`, `ScrollSpeedFactors`, `TimingGroups` are not emitted; line endings `\r\n`. The reader restores the defaults (`RestoreDefaultValues`). A parser must therefore treat every missing key as its default.
- One file per difficulty; file name is free (often `<mapid>.qua`).
- Whole-file limit in ROX: 100 MiB.

## Structure / metadata

Top-level keys (from `Qua.cs`):

| Key | Type | Meaning |
|---|---|---|
| `QuaVersion` | int | 0 = no versioning, 1 = contains mines. The reader refuses a file whose version is greater than `CurrentQuaVersion` (= 1) with a `QuaVersionException` |
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
| `TimingGroups` | map | id -> group (tag `!ScrollGroup`); reserved ids `$Default` (not serialized, the top-level `SliderVelocities`/`ScrollSpeedFactors`/`InitialScrollVelocity` belong to it) and `$Global` (applies to every group; omitted when empty). A group has `ColorRgb`, `Hidden`, `InitialScrollVelocity`, `ScrollVelocities`, `ScrollSpeedFactors` |

`Qua.Validate()` (run by `Parse(..., checkValidity: true)`, which throws `ArgumentException` listing the errors): at least one hit object; at least one timing point; `Mode` must be a defined `GameMode`; each sound effect `Sample` in `[1, CustomAudioSamples.Count]` and `Volume` in 1..100; each long note `EndTime > StartTime`; each key sound `Sample` in `[1, Count]` and `Volume >= 1`.

## Timing model

- All times are milliseconds from the start of the audio. `HitObjects` `StartTime`/`EndTime` are ints, timing points / SVs / sound effects are floats. After loading, `Sort()` orders all lists by time.
- `TimingPoints`: `StartTime` (float ms), `Bpm` (float), `Signature` (`Quadruple` = 4/4, default and omitted; `Triple` = 3/4), `Hidden` (bool, editor-only). BPM = quarter notes per minute, beat length = `60000 / Bpm` ms (`MillisecondsPerBeat`). Several points may share a timestamp; the last one wins for the SV bookkeeping (`NormalizeSVs`).
- Position -> time is not needed: hit objects are in ms. Beats only matter for snapping and for the SV normalisation below.
- **Scroll velocity** (`SliderVelocities`): `Multiplier` changes scroll speed from `StartTime` until the next entry; this never changes hit timing, only the screen position of the notes. Two representations exist (`Qua.cs` comments):
  - `BPMDoesNotAffectScrollVelocity: false` (key absent: old maps, osu!/StepMania conversions) - "denormalized": the effective scroll multiplier is `SV multiplier * (currentBpm / baseBpm)`, where `baseBpm` is the most common BPM weighted by duration up to the last object (`GetCommonBpm`); every timing point resets the active SV multiplier to 1 unless an SV starts at the same time.
  - `true` - "normalized": the multiplier is used as is; `InitialScrollVelocity` is the multiplier before the first SV. `NormalizeSVs()` / `DenormalizeSVs()` convert between the two (infinite BPM is treated as a multiplier of 128).
- `ScrollSpeedFactors` (SSF) and `TimingGroups` give per-group, independent scrolling (hit objects reference a group with `TimingGroup`). `$Global` is applied on top of every group. Exact rendering formulas for SSF are not in the files consulted: Unknown.
- To convert to ROX the denormalized form must first be normalised as above; the ROX decoder does not do it (see ROX support).

## Notes

`HitObjects` entry (`HitObjectInfo`):

| Key | Type | Meaning |
|---|---|---|
| `StartTime` | int ms | |
| `Lane` | int | **1-based** lane (1 = leftmost). With `HasScratchKey` the scratch lane is `Lane == key count` (the last one) |
| `EndTime` | int ms | `0` / absent = tap; `> 0` = long note (`IsLongNote => EndTime > 0`); must be `> StartTime` |
| `HitSound` | flags | `Normal` 1, `Whistle` 2, `Finish` 4, `Clap` 8 (`Hitsounds.cs`); `Normal` is played when the value is 0 or 1; written as 0 when it is `Normal` |
| `Type` | enum | `Normal` (0) or `Mine` (1; hit = miss; makes `QuaVersion` 1) |
| `KeySounds` | list | `{ Sample: <1-based index into CustomAudioSamples>, Volume: <1-100, omitted = 100> }`; several key sounds per object are possible |
| `EditorLayer` | int | index into `EditorLayers` (0 = none), editor only |
| `TimingGroup` | string | scroll group id; omitted = `$Default` |

- Taps and long notes only (plus mines); no bursts/rolls. A long note's end is a separate judgement (`JudgementCount` 2); mines count 1 and are excluded from difficulty (`DifficultyContributingHitObjects`).
- Simultaneous notes are allowed (chords); objects are sorted by `StartTime` after loading.
- Key count: from `Mode` (Keys1..Keys10) plus 1 if `HasScratchKey` (`ModeHelper.ToKeyCount`); `FromKeyCount` is the inverse (1..10).
- `SoundEffects` play background samples at a time (`Sample` index 1-based into `CustomAudioSamples`); `UnaffectedByRate` samples keep their pitch/speed under rate mods.

## Audio & images

`AudioFile`, `BackgroundFile`, `BannerFile` are plain file names relative to the folder (the `.qp` root). `CustomAudioSamples[].Path` are relative sample files (wav/ogg/mp3). `SongPreviewTime` is in ms. Keysounds are referenced by index (1-based) into `CustomAudioSamples` from `HitObjects[].KeySounds` and `SoundEffects[]`.

## Versions & variants

- `QuaVersion` 0 -> original; 1 -> mines. `DetermineMinimumQuaVersion()` writes 1 only if a mine exists, so older clients still load maps without new features. A reader must reject `QuaVersion > 1` or ignore the unknown features.
- Newer keys (`TimingGroups`, `ScrollSpeedFactors`, `HasScratchKey`, `BPMDoesNotAffectScrollVelocity`, `LegacyLNRendering`, `Genre`) can be absent in older files.
- Maps converted from osu!/StepMania by Quaver use `BPMDoesNotAffectScrollVelocity` false and a long list of 1-ms-apart timing points (see the real test resource `Osu/Resources/Camellia - Backbeat Maniac (Evening) [Rewind VIP].qua`, which has thousands of `TimingPoints` entries).

## Quirks & pitfalls

- Lanes are 1-based; osu!/ROX columns are 0-based.
- `EndTime: 0` means tap, not a zero-length hold.
- Every value equal to its default is omitted by the writer.
- `Tags` is a single string; `Source`/`BackgroundFile` may be `''`.
- `Mode: Keys1/2/3/5/6/8/9/10` and `HasScratchKey` exist, though 4K/7K dominate.
- Floating-point `StartTime` of timing points/SVs vs integer `StartTime` of hit objects.
- Denormalized SV (default!) depends on BPM; an importer that reads `Multiplier` at face value gets the wrong scroll speed on maps with BPM changes (hit timing is still correct).
- The `Hidden` flag of timing points is editor-only.

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

ROX source `src/formats/qua` (parser: `serde_yaml`, UTF-8, 100 MiB):
- Read + write. Decode reads `AudioFile`, `SongPreviewTime`, `BackgroundFile`, `MapId`/`MapSetId` (only if > 0), `Mode`, `Title`, `Artist`, `Source`, `Tags` (split on whitespace), `Creator`, `DifficultyName`, `TimingPoints` (`Bpm` + `Signature` -> 4 or 3), `SliderVelocities`, `InitialScrollVelocity`, `HitObjects` (`StartTime`, `Lane` - 1, optional `EndTime`).
- Only `Mode: Keys4` and `Keys7` are accepted (`QuaMode` has two variants); any other `Mode` value makes the YAML deserialisation fail. A missing `Mode` is `Keys4`.
- `InitialScrollVelocity` (if finite and != 1) becomes an SV point at the start of the map (changelog 0.8.0). `SliderVelocities` become `TimingPoint::Sv` with the raw multiplier; `BPMDoesNotAffectScrollVelocity` is parsed but NOT used by the decoder, so denormalized maps are decoded with the wrong SV semantics (see Quirks).
- Dropped on read: `HitSound`, `KeySounds`, `Type: Mine` (an object with `Type: Mine` has no field in ROX's struct and is decoded as a normal tap), `EditorLayer`, `TimingGroup`/`TimingGroups`, `ScrollSpeedFactors`, `SoundEffects`, `CustomAudioSamples`, `Bookmarks`, `EditorLayers`, `HasScratchKey` (a scratch lane would exceed the key count and fail ROX validation `InvalidColumn`), `LegacyLNRendering`, `Hidden`, `Genre`, `Description`, `BannerFile`.
- A hold is decoded whenever `EndTime` is present, so an explicit `EndTime: 0` would give a hold of negative duration (validation error) [inference from `decoder.rs`: `if let Some(end) = ho.end_time { Note::hold(time, end - time, ..) }`].
- Encode: writes `AudioFile`, `SongPreviewTime`, `BackgroundFile`, `MapId`, `Title`, `Artist`, `Creator`, `DifficultyName`, `Source`, `Tags` (space-joined), `BPMDoesNotAffectScrollVelocity: true`, `InitialScrollVelocity: 1.0`, BPM points (signature omitted), SV points, hit objects (lane + 1, `EndTime` for holds). The encoder never sets `Mode` (ROX source `to_qua` uses the default), so a 7K chart is written as `Mode: Keys4` [from reading the source; not run]. Burst/Mine notes are written like taps/holds.

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

- **Committed** in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): 82 real and test maps: Quaver.API's test resources (MPL-2.0: `sample`, `keysounds`, `sound-effects`, SV regression and "normalized" pairs, `stable-sorting` with CRLF, `cheat`/`symphony` large maps, converted osu! maps `megalovania` 7K and `Camellia - Backbeat Maniac` with thousands of timing points, 29 AutoMod inputs including one with a UTF-8 BOM), Quaver's built-in maps (Offset Calibrator and the 8 Princess of Winter difficulties; CC-BY-NC 4.0) and two hand-written CC0 charts covering `HasScratchKey`, mines (`QuaVersion: 1`), `TimingGroups`/`ScrollSpeedFactors`, Keys10, layers and bookmarks (features the upstream test files here do not contain).
- **Manifest**: none for bare `.qua`; the three Quaver default `.qp` mapsets of the manifest (see [qp](../qp/README.md)) contain 4-6 real difficulties each.
- **How to get more**: Quaver's editor writes `.qua` into the Songs folder; every mapset on https://quavergame.com is a `.qp` (a ZIP, so unzip it); Quaver converts `.osz`, `.sm` and `.mcz` on import (`MapsetImporter.AcceptedMapType`), which also produces `.qua`; the Quaver repository ships 11 default `.qp` under `Quaver.Resources/Quaver.Resources/DefaultMaps/`. Newest features (scratch, mines, timing groups) only appear in recent community maps or in the current Quaver.API tests (the pinned a921d56 snapshot has none).

## Sources

- https://github.com/Quaver/Quaver.API/blob/master/Quaver.API/Maps/Qua.cs and `Maps/Structures/{HitObjectInfo,TimingPointInfo,SliderVelocityInfo,SoundEffectInfo,CustomAudioSampleInfo,KeySoundInfo,BookmarkInfo,EditorLayerInfo,ScrollGroup,ScrollSpeedFactorInfo,TimingGroup}.cs`, `Enums/{GameMode,HitObjectType,Hitsounds,TimeSignature}.cs`, `Helpers/ModeHelper.cs`
- https://github.com/Quaver/Quaver.API/tree/master/Quaver.API.Tests (test resources `.qua`)
- https://github.com/Quaver/Quaver/blob/master/Quaver.Shared/Database/Maps/MapsetImporter.cs
- https://wiki.quavergame.com/docs/faq (import of `.osz`, `.sm`, `.mcz`)
- ROX source: `src/formats/qua/{types,parser,decoder,encoder}.rs`, `CHANGELOG.md` (0.8.0)
