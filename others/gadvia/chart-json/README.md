# Gadvia chart (JSON asset)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview

Gadvia charts are JSON text assets in the game's Unity asset bundles (32-hex-character bundle names inside `split_UnityDataAssetPack.apk`, e.g. `assets/bin/Data/293c9b06cc505f448949507b64e7a17c`). The only public description is the Rhythm Game Wiki page "Gadvia:Chart file" (field names and types, no semantics). No parser or editor found.

## Container & encoding

- JSON. Extraction: `adb pull` the APKs, rename to `.zip`, open the bundle with the chart in AssetRipper via File > Open File (opening a folder does not extract charts), then Export. Song list and lyrics assets do not extract cleanly (cause unknown).
- One chart per difficulty (Neritic, Photic, Bathyal) [inference; not stated by the wiki].

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

Unknown. `BPM`, `beatMax`, `GridOffset`, `Length` and `BPMNoteDatas` suggest a beat grid with tempo-change notes; the unit of `time` (beats, seconds or ms) is undocumented [inference].

## Notes
Unknown semantics of `Type`, `NoteValue`, `SPValue`, `trackPos` and the several note arrays. Score rule from the wiki's Sing mode page: each note scores `1000000 / totalNotes` times a judgement factor (Gold Perfect 100% + 0.0001, Perfect 100%, Great 80%, Good 50%, Miss 0%).

## Audio & images

Separate assets (a "lyrics file" and a "song list file" exist).

## Versions & variants

Unknown.

## Quirks & pitfalls

- AssetRipper does not extract charts when opening a whole folder.
- The game is offline-only since 2025-01-15, so no new assets will appear.

## Example

None: no real chart sample was available.

## ROX support
Not read by ROX.

## Parsers & tools
None known. Extraction: AssetRipper, adb.

## Getting samples

No sample committed: no Gadvia chart is public (searched GitHub and the wiki, which has field names only), and one was not synthesised because `Type`, `NoteValue`, `SPValue` and the `time` unit are undocumented. To extract one (Rhythm Game Wiki, [Gadvia:Guides/Extracting_game_files](https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files)): install the Android game (`com.hgca.uma`), run `adb shell pm path com.hgca.uma`, `adb pull` the APKs, rename `split_UnityDataAssetPack.apk` to `.zip` and unzip; charts are in 32-hex-named bundles under `assets/bin/Data/` (e.g. `293c9b06cc505f448949507b64e7a17c`); open that bundle in AssetRipper with *File > Open File*, then *Export > Export all Files*.

## Sources
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Chart_file
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Gadvia
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Sing_mode
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files
