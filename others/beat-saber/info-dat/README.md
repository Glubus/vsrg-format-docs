# Beat Saber Info file (`Info.dat`, legacy `info.json`)
Kind: metadata

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview
`Info.dat` is the entry point of a Beat Saber custom level. It carries song metadata, the audio and cover filenames, environment/color-scheme choices and the list of difficulty files (one beatmap per characteristic + difficulty). Written by the Official Editor, ChroMapper, MMA2 etc.; read by the game, SongCore and BeatSaver. Schema versions: v1 (legacy `info.json`, game < 1.0 era), v2 (since 1.0.0, root keys prefixed with `_`), v4 (since 1.34.5, no prefix, no beatmap sets). There is no v3 Info (v3 only exists for beatmap files); [BeatSaber-Deno](https://github.com/KivalEvan/BeatSaber-Deno/blob/main/BEATMAP.md) lists Info versions v1 (1.0.0), v2 (2.1.0) and v4 (4.0.1). The base game accepts older schemas through an internal compatibility layer, but BSMG recommends targeting the newest.

## Packaged in

- Packaged in [`beatsaver-zip`](../beatsaver-zip/).

## Container & encoding
- JSON text (UTF-8). All metadata files are JSON; any extension may be used for them, **except the info file, which must be named exactly `Info.dat`** (BSMG, map-format).
- All filename references are relative to the directory containing `Info.dat`.
- Since 1.34.5 the game's own OST/DLC metadata files are gzip-deflated; the game also accepts such deflated files for custom levels (BSMG), editors usually do not write them.
- Defaulted properties: since 1.31.0 omitted fields take defaults; v4 additionally treats missing arrays as empty. `{ "version": "4.0.0" }` is a valid v4 beatmap.
- One Info file per map set; difficulties are separate files (see [../dat/](../dat/README.md)).

## Structure / metadata
### v2 (`_version` `2.0.0` / `2.1.0`)
Sample (BSMG): `_version`, `_songName`, `_songSubName`, `_songAuthorName`, `_levelAuthorName`, `_beatsPerMinute`, `_songTimeOffset`, `_shuffle`, `_shufflePeriod`, `_previewStartTime`, `_previewDuration`, `_songFilename`, `_coverImageFilename`, `_environmentName`, `_allDirectionsEnvironmentName`, `_difficultyBeatmapSets`; 2.1.0 adds `_environmentNames` (array), `_colorSchemes`.

| Field | Meaning |
|---|---|
| `_songName`, `_songSubName`, `_songAuthorName` | Title, subtitle (collaborators/alt arrangement), artist |
| `_levelAuthorName` | Single mapper string, applies to all difficulties |
| `_beatsPerMinute` | Grid BPM: how the beat grid aligns to the audio |
| `_songTimeOffset` (s) | Delays audio start vs. beatmap. Deprecated, unstable, unsupported from v4 |
| `_shuffle`, `_shufflePeriod` | "Swing" timing across all beatmaps. Deprecated, unsupported from v4 |
| `_previewStartTime`, `_previewDuration` | Preview window of the song (s) |
| `_songFilename` | Audio file (ogg recommended for BeatSaver; wav works in the Official Editor) |
| `_coverImageFilename` | png/jpeg/jpg, square, >= 256 px advised for BeatSaver |
| `_environmentName` | Base environment; `_allDirectionsEnvironmentName` for 360/90 degree beatmaps |
| `_environmentNames` (2.1.0) | Environment collection indexed by `_environmentNameIdx`; takes priority over the top-level one |
| `_colorSchemes` (2.1.0) | Array of `{useOverride, colorScheme{colorSchemeId, saberAColor, saberBColor, environmentColor0/1, obstaclesColor, environmentColor0Boost/1Boost}}`; colors are `{r,g,b,a}` floats 0..1 |
| `_difficultyBeatmapSets` | Array of `{_beatmapCharacteristicName, _difficultyBeatmaps[]}` |

`_difficultyBeatmaps[]` entry: `_difficulty`, `_difficultyRank`, `_beatmapFilename`, `_noteJumpMovementSpeed` (NJS), `_noteJumpStartBeatOffset`; 2.1.0 adds `_beatmapColorSchemeIdx` (-1 = inherit environment colors), `_environmentNameIdx`.

Characteristics: `Standard`, `NoArrows`, `OneSaber` (left/red saber disabled), `360Degree`, `90Degree` (rotation behaviours), `Legacy`. SongCore adds `Lightshow`, `Lawless` (not valid on an unmodded game). Difficulty names / ranks: Easy 1, Normal 3, Hard 5, Expert 7, Expert+ 9 (`ExpertPlus` in files).

Per-beatmap color scheme / environment on v2.0.0 relies on SongCore/PinkCore (BSMG).

### v4 (`version` `4.0.0`)
Sample (BSMG):
```
version, song{title,subTitle,author},
audio{songFilename,songDuration,audioDataFilename,bpm,lufs,previewStartTime,previewDuration},
songPreviewFilename, coverImageFilename, environmentNames[], colorSchemes[],
difficultyBeatmaps[{characteristic,difficulty,beatmapAuthors{mappers[],lighters[]},
  environmentNameIdx,beatmapColorSchemeIdx,noteJumpMovementSpeed,noteJumpStartBeatOffset,
  beatmapDataFilename,lightshowDataFilename}]
```
- No beatmap sets: characteristic is a per-beatmap string.
- `audio.songDuration` (s) caches the length (v3 and earlier: only SongCore/PinkCore show it).
- `audio.audioDataFilename` points to the BPM/LUFS file (`BPMInfo.dat`), see [../dat/](../dat/README.md#audio-data-bpminfodat--audiodatadat).
- Two audio files: primary (`audio.songFilename`, used for play, BPM and LUFS) and preview (`songPreviewFilename`).
- Colors are hex `RRGGBBAA` strings (`"C81414FF"`), `colorSchemeName` instead of id.
- Authors per beatmap: `beatmapAuthors.mappers` / `lighters`.
- Deprecated time offset and shuffle are gone.

### v1 legacy `info.json`
Not on BSMG. From the conversion table in the gist [Beat Saber 1.0 level format conversion](https://gist.github.com/MCJack123/892b936ef0d18da43ab2764ba97402be): keys `songName`, `songSubName`, `authorName`, `beatsPerMinute`, `previewStartTime`, `previewDuration`, `coverImagePath`, `environmentName`, `oneSaber`, `difficultyLevels[]` with `characteristic`, `difficulty`, `difficultyRank`, `audioPath`, `offset`, `jsonPath`, `oldOffset`, `chromaToggle`, `customColors`, `difficultyLabel`; `_noteJumpSpeed`, `_shuffle`, `_shufflePeriod` live in the difficulty json. Fields the gist marks "custom mod": `contributors`, `customEnvironment`, `customEnvironmentHash`. The song loader README (https://github.com/xyonico/BeatSaberSongLoader) confirms `info.json` and that difficulty files are named by `jsonPath`. v1 has no environment list, no color schemes, no author-per-beatmap (BeatSaber-Deno table).

## Timing model
- Beatmap objects are in **beats**; seconds = beats x 60 / BPM (BPM from `_beatsPerMinute` / v4 `audio.bpm`) when BPM never changes; BPM changes are carried by beatmap BPM events (v3 `bpmEvents`, v2 events of type 100, see [../dat/](../dat/README.md)) or by BPM regions in the audio data file.
- `_songTimeOffset` shifts the audio (seconds, deprecated). `_noteJumpMovementSpeed` / `_noteJumpStartBeatOffset` do not change judgement time; they control how early/far objects spawn (note jump metadata).

## Notes
Not applicable at this level (see dat doc). Info only selects characteristic (`OneSaber` disables the left saber) and difficulty.

## Audio & images
`_songFilename` / `audio.songFilename`, `songPreviewFilename` (v4), `_coverImageFilename` / `coverImageFilename`; v4 `audio.audioDataFilename`; v4 `lightshowDataFilename` per beatmap. If a v2/v3 beatmap is referenced, the lightshow file is ignored (lighting is inside the beatmap) (BSMG).

## Versions & variants
- v1 info.json (legacy) -> v2 Info.dat (1.0.0) -> v4 Info.dat (1.34.5). No Info v3. BeatSaber-Deno schema versions: Info v4.0.1, v2.1.0, v1.0.0.
- A v2 Info can load v2 and v3 beatmaps; a v4 Info can load v2, v3 and v4 beatmaps (BeatSaber-Deno BEATMAP.md). A v4 beatmap needs v4 audio data from a v4 Info.
- `customData` / `_customData` blocks (Chroma, Noodle Extensions, SongCore, Cinema, ...) are mod extensions, not part of the vanilla schema.

## Quirks & pitfalls
- File name case: the Info must be `Info.dat` (some Linux tools see `info.dat`; [inference] accept both when parsing).
- Do not rely on `_levelAuthorName` per beatmap in v2; per-beatmap authors exist only in v4.
- Unset color-scheme colors become `null` colors in-game (BSMG).
- `_difficulty` string for the last tier is `ExpertPlus` while the BSMG rank table labels it `Expert+`.
- Mods add characteristics; filter unknown ones.

## Example
Excerpt of the BSMG sample (Magic, v2):
```json
{
  "_version": "2.0.0",
  "_songName": "Magic", "_songSubName": "ft. Meredith Bull",
  "_songAuthorName": "Jaroslav Beck", "_levelAuthorName": "Freeek",
  "_beatsPerMinute": 208, "_songTimeOffset": 0, "_shuffle": 0, "_shufflePeriod": 0,
  "_previewStartTime": 0, "_previewDuration": 0,
  "_songFilename": "Magic.wav", "_coverImageFilename": "cover.png",
  "_environmentName": "WeaveEnvironment",
  "_allDirectionsEnvironmentName": "GlassDesertEnvironment",
  "_difficultyBeatmapSets": [ { "_beatmapCharacteristicName": "Standard",
    "_difficultyBeatmaps": [ { "_difficulty": "Easy", "_difficultyRank": 1,
      "_beatmapFilename": "Easy.dat", "_noteJumpMovementSpeed": 10, "_noteJumpStartBeatOffset": 0 } ] } ]
}
```
Origin: https://bsmg.wiki/mapping/map-format/info.html (trimmed to one difficulty).

## ROX support
Not read by ROX (no Beat Saber codec in `src/formats/`: auto, fnf, mc, osu, qua, rox_native, sm, taiko, jrox, yrox).

## Parsers & tools
- BeatSaber-Deno / `bsmap` (TypeScript, Deno/Bun/Node): https://github.com/KivalEvan/BeatSaber-Deno (Info v1/v2/v4, converters)
- ChroMapper (C#/Unity): https://github.com/Caeden117/ChroMapper
- Official Beat Saber Editor (in game)
- MediocreMapAssistant2: https://git.bsmg.dev/Top_Cat/MediocreMapAssistant2
- SongCore (mod): https://github.com/Kylemc1413/SongCore
- SimSaber (Python interpretMapFiles): https://github.com/MetaGuard/SimSaber/blob/main/interpretMapFiles.py (seen in search results only, not opened)

## Sources
- https://bsmg.wiki/mapping/map-format.html
- https://bsmg.wiki/mapping/map-format/info.html
- https://raw.githubusercontent.com/KivalEvan/BeatSaber-Deno/main/BEATMAP.md
- https://raw.githubusercontent.com/KivalEvan/BeatSaber-Deno/main/README.md
- https://gist.github.com/MCJack123/892b936ef0d18da43ab2764ba97402be
- https://github.com/xyonico/BeatSaberSongLoader (search result)
