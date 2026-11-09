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

**Committed:** none; no Gadvia chart exists in any public place I could reach (searched GitHub repositories, the Rhythm Game Wiki page, which has field names only). Not synthesised, because `Type`, `NoteValue`, `SPValue` and the `time` unit are undocumented.

**How to get one yourself** (Rhythm Game Wiki, *Gadvia:Guides/Extracting game files*, <https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files>): install the Android game (`com.hgca.uma`), `adb shell pm path com.hgca.uma`, `adb pull` the APKs, rename `split_UnityDataAssetPack.apk` to `.zip` and unzip; charts sit in 32-hex-named asset bundles under `assets/bin/Data/` (e.g. `293c9b06cc505f448949507b64e7a17c`); open that single bundle in AssetRipper with *File > Open File*, then *Export > Export all Files*. The servers closed on 2025-01-15; the game is offline-only.

## Sources
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Chart_file
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Gadvia
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Sing_mode
- https://rgwiki.stary.pc.pl/wiki/Gadvia:Guides/Extracting_game_files
