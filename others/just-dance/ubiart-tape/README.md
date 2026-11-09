# Just Dance UbiArt tape (`.dtape.ckd`, `.ktape.ckd`, `.tape.ckd`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json (binary for Just Dance 2015)

## Overview
In the UbiArt Framework versions of Just Dance (2015/2016 onward), the choreography of a map is a **tape**: a timeline with a list of *clips*. A map normally has a dance tape (`<map>_tml_dance.dtape.ckd`: motion, pictogram and gold-effect clips), a karaoke tape (`<map>_tml_karaoke.ktape.ckd`: lyric clips with pitch) and a cinematics tape (`*.tape.ckd`: camera, FX, UI and other clips). "ckd" means "cooked" (the game's packaged form). From Just Dance 2016 on, a cooked tape is a plain JSON document with a trailing NUL byte; Just Dance 2015 used a binary layout. The format is known through reverse engineering by the modding community (Ferris Dancing parser, json2tape generator); there is no official documentation.

## Container & encoding
- File: UTF-8 JSON text terminated by one `0x00` byte (parser `clean_buffer_json` requires the last byte be 0 unless lax). Parsed as a `Tape` object.
- Stored inside the game's cooked file tree / `.ipk` bundles (Ferris Dancing has an `ipk` module); community tools (e.g. KtapeTool) convert to readable JSON and back to "weird null-terminated JSON".
- File naming (json2tape, Ferris Dancing notes): `<map>_tml_dance.dtape.ckd`, `<map>_tml_karaoke.ktape.ckd` under `world/maps/<map>/timeline/`; moves in `timeline/moves/<name>.msm`; pictograms in `timeline/pictos/<name>.png|tga`; music track `<map>_musictrack.tpl.ckd`.
- One tape per map and kind (dance, karaoke, cinematics).

## Structure / metadata
`Tape` (PascalCase keys, from Ferris Dancing `ubiart_toolkit::cooked::tape`):

| Key | Type | Meaning |
|---|---|---|
| `__class` | string | `"Tape"` |
| `Clips` | array | clips (below) |
| `TapeClock` | u32 | usually 0 (sometimes missing in mods) |
| `TapeBarCount` | u32 | usually 1 (default 1 if missing) |
| `FreeResourcesAfterPlay` | u32 | 0 |
| `MapName` | string | map identifier |
| `SoundwichEvent` | string | optional (not in the Switch 2017 files) |

Every clip has `__class` (`"MotionClip"`, `"PictogramClip"`, `"GoldEffectClip"`, `"KaraokeClip"`, ...), `Id` (u32), `TrackId` (u32; may be missing in mods), `IsActive` (1), `StartTime` (int; some mods write floats), `Duration` (int), and for many types `ActorIndices` / `TargetActors`.

| Clip class | Extra keys |
|---|---|
| `MotionClip` | `ClassifierPath` (path of the `.msm` move), `GoldMove` (0/1), `CoachId` (also `CoachID` in mods), `MoveType`, `Color` ([r,g,b,a] floats), `MotionPlatformSpecifics` (map of platform name such as `X360`, `ORBIS`, `DURANGO` to `{__class:"MotionPlatformSpecific", ScoreScale, ScoreSmoothing, ScoringMode, LowThreshold?, HighThreshold?}`; thresholds not used from 2019 on) |
| `PictogramClip` | `PictoPath`, `MontagePath` and `AtlIndex` (only 2017-2018; atlas montage), `CoachCount` (default 0xFFFFFFFF = all) |
| `GoldEffectClip` | `EffectType` |
| `KaraokeClip` | `Pitch` (float), `Lyrics` (string), `IsEndOfLine` (0/1), `ContentType`, `StartTimeTolerance`, `EndTimeTolerance`, `SemitoneTolerance` |

Other clip classes defined by the parser (cinematics and UI): `ActorEnableClip`, `AlphaClip` (`Curve`), `CameraFeedClip`, `ColorClip`, `CommunityDancerClip`, `FXClip`, `GameplayEventClip`, `HideUserInterfaceClip`, `MaterialGraphic*Clip`, `ProportionClip`, `Proportion3DClip`, `RotationClip`, `SizeClip`, `SlotClip`, `SpawnActorClip`, `SoundSetClip`, `SoundwichClip`, `TapeLauncherClip`, `TapeReferenceClip`, `TextClip`, `TextAreaSizeClip`, `TranslationClip`, `VibrationClip` and three clips named by hash (`Unknown59FCC733Clip`, `UnknownCBB7C029Clip`, `Unknown5C944B01Clip`).

## Timing model
- `StartTime` and `Duration` are **tape ticks**, 24 ticks per beat: json2tape maps beat `i` to tick `24*i` (`BeatsMap24`) and interpolates linearly between beat times of the source map to convert millisecond times (`ubiArtTime`). It adds 24 ticks (one beat) to a gold move's start for its `GoldEffectClip` and gives it duration 24.
- The beat grid is not in the tape: it is in the music track template (`MusicTrackStructure`): `markers` = sample positions of every beat on a 48 kHz timebase (json2tape writes `beat_ms * 48`; [inference: 48 samples per ms]), `signatures[] {marker, beats, comment?}` for the time signature (beats per bar), `sections[] {marker, sectionType, comment}`, `startBeat` (may be negative), `endBeat`, `fadeStartBeat`, `useFadeStartBeat`, `fadeEndBeat`, `useFadeEndBeat`, `videoStartTime` (float, seconds), `previewEntry`, `previewLoopStart`, `previewLoopEnd` (beat indices), `volume`, `fadeInDuration`/`fadeInType`/`fadeOutDuration`/`fadeOutType`, `entryPoints`. `path` and `url` of `MusicTrackData` name the audio. So tempo may vary: the marker spacing is the tempo map.
- Seconds for tick `t`: beat index = `t / 24`; interpolate between `markers[floor]` and `markers[ceil]` (divide by 48000 for seconds if markers are 48 kHz samples). [inference from json2tape]

## Notes
- A "note" in the rhythm sense does not exist. Gameplay is: (1) `MotionClip`s cue the **move** (`.msm` movement-space file) that the player's controller/camera motion is compared to, with `GoldMove` marking gold moves; (2) `PictogramClip`s show the matching icons on the scrolling timeline (json2tape emits one per entry of the source map's pictogram list); (3) `GoldEffectClip` triggers the gold effect; (4) `KaraokeClip` gives sing-along syllables with pitch and tolerances.
- Coaches: `CoachId` selects which coach a move belongs to (duet, trio, quatro maps); `CoachCount` on pictograms is used for multi-coach icons that require cropping from the montage.
- Move scoring parameters (`ScoreScale`, `ScoreSmoothing`, `ScoringMode`) differ per console platform.
- Moves themselves are `.msm` ("movement space move") binary files with 2D data points `(f32, f32)` per sample, name, map and device (Ferris Dancing `msm` module: version 7 and others; several fields unknown); on PS4 `.gesture` files are used.

## Audio & images
`musictrack.tpl.ckd` `MusicTrackData.path` and `url` (e.g. `jmcs://jd-contents/<Map>/<Map>.ogg` in json2tape output); videos are `.webm`; pictograms are PNG/TGA textures (cooked `.tga.ckd` in games); a `montage.png` atlas is used in 2017-2018 maps. Audio is `.wav.ckd` (binary) in the games.

## Versions & variants
- Just Dance 2015: binary tape layout (Ferris Dancing `Tape::deserialize_with` for `Game::JustDance2015`). 2016 and later: JSON. Per-game differences: `SoundwichEvent` absent in 2017 Switch; `MontagePath`/`AtlIndex` only 2017-2018; `LowThreshold`/`HighThreshold` removed from 2019. Mods may omit `TrackId`, `IsActive`, `TapeClock` or write floats for ints.
- Just Dance Now / "Bluestar engine": separate JSON maps with times in milliseconds (`moves`, `pictos`, `lyrics`, `beats`); converted to tapes by json2tape and BlueStar, and back by tape2json.
- 2022 and later (Unity) tapes exist and are converted to UbiArt format by `Unity2UbiArt` (found by search, not opened).

## Quirks & pitfalls
- Trailing NUL byte; JSON may contain floats in integer fields (`StartTime`) and key case variants (`CoachID`).
- Clip `Id` and `TrackId` are random 32-bit values generated by tools; uniqueness matters only inside a tape.
- Gold effect times cannot be derived from a JDN map: json2tape places them 24 ticks after each gold move.
- Tick-to-ms needs the beat markers of the music track, which is a different file.

## Example
Shape produced by json2tape for one move and one karaoke syllable (from its source `j2t.js`; keys quoted, values trimmed):
```json
{"__class":"Tape","Clips":[
 {"__class":"MotionClip","Id":123456,"TrackId":654321,"IsActive":1,"StartTime":384,"Duration":48,
  "ClassifierPath":"world/maps/<map>/timeline/moves/<move>.msm","GoldMove":0,"CoachId":0,"MoveType":0,
  "Color":[1,0.5,0.5,0.500001],
  "MotionPlatformSpecifics":{"X360":{"__class":"MotionPlatformSpecific","ScoreScale":1.4,"ScoreSmoothing":0,"ScoringMode":0}}}],
 "TapeClock":0,"TapeBarCount":1,"FreeResourcesAfterPlay":0,"MapName":"<map>"}
```
Numeric values 384/48 are illustrative (16 beats in, one beat long). `KaraokeClip` shape: `{"__class":"KaraokeClip","Id":1,"TrackId":2,"IsActive":1,"StartTime":0,"Duration":24,"Pitch":7.000001,"Lyrics":"la","IsEndOfLine":0,"ContentType":0,"StartTimeTolerance":4,"EndTimeTolerance":4,"SemitoneTolerance":5}`.

## ROX support
Not read by ROX. A clip timeline of scored full-body moves; at most the beat grid could be exported, no columns.

## Parsers & tools
- Ferris Dancing / `ubiart_toolkit` (Rust, parse+write tapes, ipk, tpl, msm): https://github.com/Kriskras99/ferris_dancing
- json2tape (JavaScript): https://github.com/matty0004/json2tape
- BlueStar (Python): https://github.com/MZommer/BlueStar
- tape2json (tapes to Just Dance Now JSON): https://github.com/ibratabian17/tape2json
- KtapeTool, IpkTool (nkrapivin): https://github.com/nkrapivin/JustDanceModTools
- JD Timeline Studio: https://github.com/MaximJDTOOLS/Just-dance-2017-timeline-studio
- OpenDance (GameMaker recreation): https://github.com/WodsonKun/OpenDance

## Getting samples

**Committed** ([`samples/`](samples/SOURCES.md)): `synthetic_tml_dance.dtape.ckd` and `synthetic_tml_karaoke.ktape.ckd` (hand-written from the documented fields, CC0). **Manifest:** none. No real tape could be redistributed: Ferris Dancing's real test files live in a private submodule (`ubiart_toolkit_test_files`), tape2json's `input/*.json` are empty `{}` placeholders, json2tape is PolyForm Strict, and real tapes are Ubisoft data.

**How to get real ones**: from a game install (Just Dance 2016 and later use JSON tapes with a trailing NUL), extract the `.ipk` bundles with IpkTool (<https://github.com/nkrapivin/JustDanceModTools>) or Ferris Dancing's `ipk` module (<https://github.com/Kriskras99/ferris_dancing>); the tapes are under `world/maps/<map>/timeline/` as `<map>_tml_dance.dtape.ckd` and `<map>_tml_karaoke.ktape.ckd` (paths from the README sources). Just Dance Now JSON maps can be turned into tapes with json2tape (<https://github.com/matty0004/json2tape>) or BlueStar (<https://github.com/MZommer/BlueStar>); `tape2json` converts back. Fan-made tapes for JD 2017 are edited with JD Timeline Studio.

## Sources
- https://github.com/Kriskras99/ferris_dancing (`ubiart_toolkit/src/cooked/tape/mod.rs`, `ubiart_toolkit/src/utils/json.rs`, `ubiart_toolkit/src/cooked/tpl/types.rs`, `ubiart_toolkit/src/msm/types.rs`, `scratchpad.md`)
- https://github.com/matty0004/json2tape (`j2t.js`)
- https://github.com/nkrapivin/JustDanceModTools
- https://github.com/MZommer/BlueStar
- https://github.com/ibratabian17/tape2json, https://github.com/MaximJDTOOLS/Just-dance-2017-timeline-studio, https://github.com/Itaybl14/Unity2UbiArt (read via search snippets only)
