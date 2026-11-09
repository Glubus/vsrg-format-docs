# Gadvia chart (JSON asset)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
Gadvia charts are JSON text assets stored in the game's Unity asset bundles (32-character hexadecimal bundle names inside `split_UnityDataAssetPack.apk`, e.g. `assets/bin/Data/293c9b06cc505f448949507b64e7a17c`). The only public description is the "Gadvia:Chart file" page of the Rhythm Game Wiki, which lists field names and types without semantics. No parser or editor was found.

## Container & encoding
- JSON. Extraction: `adb pull` the APKs, rename to `.zip`, open the bundle containing the chart in AssetRipper with File > Open File (a folder open does not extract chart files), then Export. Song list and lyrics assets cannot be extracted cleanly (cause unknown).
- One chart per difficulty is presumed (Neritic, Photic, Bathyal). [inference; not stated by the wiki]

## Structure / metadata
Root fields (names and types as listed by the wiki):

| Field | Type |
|---|---|
| `TrackTypeSetting` | array of integers |
| `SongName` | string |
| `Compose` | string (composer) |
| `Length` | float |
| `BPM` | float |
| `beatMax` | integer |
| `GridOffset` | float |
| `SaveMode` | int |
| `NoteDatas` | array of note objects |
| `BgNoteDatas` | array of note objects |
| `BPMNoteDatas` | array of note objects |
| `FallNoteDatas` | array of note objects |
| `NoUseNoteDatas` | array |
| `SpeedNoteDatas` | array |
| `CheckLineDatas` | array of note objects |
| `CameraDatas` | array |

Note object: `time` (float), `Pos` {`x`, `y`, `z`} (floats), `trackPos` (int), `Type` (int), `NoteValue` (float), `SPValue` {`x`, `y`, `z`} (floats), `word` (string, the lyric word displayed on top of the note), `isEndTip` (bool), `TipStartMode` (int).

## Timing model
Unknown. `BPM`, `beatMax`, `GridOffset`, `Length` and `BPMNoteDatas` suggest a beat-grid with tempo-change notes; the unit of `time` (beats, seconds or milliseconds) is not documented. [inference only]

## Notes
Unknown semantics of `Type`, `NoteValue`, `SPValue`, `trackPos` and the several note arrays. Score rule from the wiki's Sing mode page: each note scores `1000000 / totalNotes` times a judgement factor (Gold Perfect 100% + 0.0001, Perfect 100%, Great 80%, Good 50%, Miss 0%).

## Audio & images
Not described in the chart page; audio and lyrics are separate assets (a "lyrics file" and a "song list file" exist).

## Versions & variants
Not documented.

## Quirks & pitfalls
- Chart files do not extract with AssetRipper when opening a whole folder.
- The game is offline-only since 2025-01-15, so no new assets will appear.

## Example
None: no real chart sample was available. The schema above is the complete public information.

## ROX support
Not read by ROX.

## Parsers & tools
None known. Extraction: AssetRipper, adb.

## Getting samples

**Committed:** none. **Manifest:** none. No Gadvia chart is published anywhere I could reach (the Rhythm Game Wiki page lists only field names and types), and the game is commercial; inventing a file from a field list without semantics (`Type`, `NoteValue`, `SPValue`, `time` unit) would not be a real chart, so no synthetic file was written.

**How to get one yourself** (Rhythm Game Wiki, *Gadvia:Guides/Extracting game files*, <https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files>): install the Android game (`com.hgca.uma`), enable USB debugging, run `adb shell pm path com.hgca.uma`, `adb pull` the three APKs (`base.apk`, `split_UnityDataAssetPack.apk`, `split_config.arm64_v8a.apk`), rename `split_UnityDataAssetPack.apk` to `.zip` and unzip it. The charts are in asset bundles with 32-hex-character names under `assets/bin/Data/` (e.g. `293c9b06cc505f448949507b64e7a17c`); find the bundle containing the song name by text search, then open that single bundle in AssetRipper with *File > Open File* (not *Open Folder*) and *Export > Export all Files*. The game's servers stopped on 2025-01-15 and it is offline-only, so an already installed copy is the practical source.

## Sources
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Chart_file
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Gadvia
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Sing_mode
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files
