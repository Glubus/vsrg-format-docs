# Synth Riders map (`.synth`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive

## Overview

A `.synth` file is a ZIP written by the Synth Riders Beatmap Editor: one map set (several difficulties) with a large JSON `beatmap.meta.bin`, a small `track.data.json` summary, the audio and the cover. The structure is reverse-engineered by the community tool `synth_mapping_helper` (`synth_format.py`), which reads and writes it; no official spec was found and several field semantics are unknown.

## Contents

See Container & encoding.

## Container & encoding

- ZIP (deflate). Entries: `beatmap.meta.bin`, `track.data.json`, audio (`AudioName` in the JSON, original format kept), cover image (`Artwork`; the editor stores a PNG copy).
- `beatmap.meta.bin` is JSON text in UTF-8 with BOM and CRLF line endings.
- `track.data.json` is JSON in UTF-16LE with BOM.
- One file holds all difficulties: `Easy`, `Normal`, `Hard`, `Expert`, `Master`, `Custom`.

## Structure / metadata
### `beatmap.meta.bin` keys (from the writer)
`Name`, `Author` (the song artist), `Artwork` (cover filename), `ArtworkBytes` (base64 PNG), `AudioName`, `AudioData` (null), `AudioFrecuency` (sic), `AudioChannels`, `BPM`, `Offset` (ms), `Track` (notes), `Effects`, `Bookmarks.BookmarksList[{time,name}]`, `Jumps`, `Crouchs`, `Slides`, `Lights`, `Squares`, `Triangles`, `DrumSamples`, `FilePath`, `IsAdminOnly`, `EditorVersion`, `Beatmapper` (mapper name), `CustomDifficultyName`, `CustomDifficultySpeed`, `UsingBeatMeasure`, `UpdatedWithMovementPositions`, `ProductionMode`, `Tags`, `BeatConverted`, `BeatModified`, `ModifiedTime` (unix s), `Explicit`. Collections `Track`, `Effects`, `Jumps`, `Crouchs`, `Slides`, `Lights`, `Squares`, `Triangles` are dictionaries keyed by difficulty name.
`Crouchs`, `Squares`, `Triangles` only exist in the beta editor files (older files lack them).

### `track.data.json`
`name`, `artist`, `duration` ("mm:ss"), `coverImage`, `audioFile`, `supportedDifficulties[]` (name or ""), `bpm`, `mapper`.

### Note objects (`Track[diff]`)
Dictionary: key = time index (as integer or float, in **1/64 beat** units), value = list of notes at that time:
`{ "Id": "Note_<time><TypeString><n>", "ComboId": -1, "Position": [x, y, z], "Segments": null | [[x,y,z], ...], "Type": 0..3, "Direction": 0 }`
- `Type`: 0 RightHanded, 1 LeftHanded, 2 OneHandSpecial, 3 BothHandsSpecial (strings `RightHanded`, `LeftHanded`, `OneHandSpecial`, `BothHandsSpecial`).
- `Segments` non-null = **rail**: head `Position` followed by successive node positions (each [x, y, z]).
- Only one note of each type per time index.

### Walls
- `Slides[diff][]`: `{ "time": ticks(1/64 beat), "slideType": 0..4, "position": [x,y,z], "zRotation": degrees, "initialized": true }`. slideType 0 right wall, 1 left wall, 2 angle right, 3 center, 4 angle left.
- `Crouchs[diff][]`, `Squares[diff][]`, `Triangles[diff][]` (no `slideType`; crouch has no zRotation).
- `Lights[diff]`, `Effects[diff]`: arrays of times (1/64 beat).

## Timing model
- Time index/ticks are in **1/64 of a beat** ("bookmarks are stored in steps of 64 per beat (regardless of BPM)"; INDEX_SCALE = 64). Beat = tick / 64; the common non-power-of-two fractions 1/48 are also used (the tool rounds to 1/64 or 1/48).
- Seconds = beat x 60 / `BPM`; `Offset` (ms) shifts the audio. A single BPM per map set (no BPM change events found in the writer).
- The note's z coordinate is a world position along the track: `z = seconds x 20` (TIME_SCALE = 20 units per second); x, y are world positions: `xy = grid x 0.1365 (+ editor offsets 0.002 / 0.0012)` (GRID_SCALE). So time is stored twice (index and z) [inference; the tool derives beats from z: `(coord[2] / 20)` seconds].

## Notes

Taps are hand-colored (left/right) or "special" (one hand either, both hands). Rails (`Segments`) are continuous paths. Walls (slides, crouch, square, triangle) must be dodged. Lights/effects are cosmetic. Position is a continuous 2D position around the player (multiples of 0.1365 world units), not a lane.

## Audio & images

Audio named by `AudioName`; cover by `Artwork`/`ArtworkBytes`. `DrumSamples` unknown.

## Versions & variants

`EditorVersion` varies; the beta editor adds Crouch/Square/Triangle lists. The editor's clipboard JSON (`BPM`, `startMeasure`, `startTime`, `lenght` (sic), `notes`, `effects`, `jumps`, `crouchs`, `squares`, `triangles`, `slides`, `lights`) has the same structure and is what the helper edits. Flags `BeatConverted` (converted from other games) and `BeatModified` exist.

## Quirks & pitfalls

- Files downloaded from synthriderz.com are AES-encrypted ZIPs (compression method 99); plain ZIP tools and the helper cannot read them [observed on 40 downloads from https://synthriderz.com/api/beatmaps].
- Misspellings are real keys (`AudioFrecuency`, clipboard `lenght`, `Crouchs`).
- Time keys can be floats (strings in JSON); positions carry small editor snap offsets.
- The editor may refuse duplicate note types at the same time.
- Keys marked "?" in the helper must be preserved on round trip.

## Example
Illustrative, hand-built from the writer code (not from a real map):
```json
{ "BPM": 120.0, "Offset": 0, "Track": { "Expert": {
   "64": [ { "Id": "Note_64RightHanded0", "ComboId": -1, "Position": [0.002, 0.0012, 10.0],
             "Segments": null, "Type": 0, "Direction": 0 } ] } } }
```
(`64` = beat 1, z = 10 world units = 0.5 s at 120 BPM.)

## ROX support
Not read by ROX.

## Parsers & tools
- synth_mapping_helper (Python): https://github.com/adosikas/synth_mapping_helper (read/write `.synth`, GUI)
- Synth Riders Beatmap Editor (official).

## Getting samples

No `.synth` could be committed. Downloads from <https://synthriderz.com> (`GET /api/beatmaps` lists maps; `download_url` redirects to the file) are AES-encrypted ZIPs (`beatmap.meta.bin` and `track.data.json` use zip method 99, flag bit 1; checked on 40 files), so neither chart nor audio can be extracted without the key. Unencrypted `.synth` files come only from their mappers [Synth_Riders_Kinematics README: "choose an unencrypted .synth file provided by its mapper. Encrypted downloads are unsupported"]. Save a map from the Synth Riders Beatmap Editor (writes an unencrypted file) or ask a mapper; `adosikas/synth_mapping_helper` reads/writes them.

## Sources
- https://raw.githubusercontent.com/adosikas/synth_mapping_helper/main/src/synth_mapping_helper/synth_format.py
- https://github.com/adosikas/synth_mapping_helper
- https://en.wikipedia.org/wiki/Synth_Riders
