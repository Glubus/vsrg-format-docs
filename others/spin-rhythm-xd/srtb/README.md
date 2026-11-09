# Spin Rhythm XD track bundle (`.srtb`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview
`.srtb` ("Spin Rhythm Track Bundle") is the chart container written by the Spin Rhythm XD in-game editor. The official editor guide says it holds "the note types and timings, the audio clip edits (bpm, time signature, cue points, difficulty types etc)". It is a Unity `ScriptableObject` dump serialized to JSON. Community tools (SRTBEditor, Chronomia, SpinShare) read and write it; no official specification exists, so the field list below is taken from real files (templates in the SRTBEditor repository, including a 5-difficulty full-album chart) and from the editors' source code. Meaning of some note fields is not documented (marked unknown).

## Container & encoding
- Outer file: UTF-8 JSON (single line by default). It is a registry: `unityObjectValuesContainer.values[]` lists objects, `largeStringValuesContainer.values[]` holds their payloads, `clipInfoCount` is the number of ClipInfo objects.
- Each payload `val` is itself a **JSON string** (double-encoded). Parse the outer JSON, then `JSON.parse` every `val` (SRTBEditor `convertToJSON`); stringify them back to save (`convertToSRTB`).
- Entries (all keys fixed):

| `unityObjectValuesContainer.values[]` (`key` / `jsonKey` / `fullType`) | Payload object |
|---|---|
| `TrackInfo` / `SO_TrackInfo_TrackInfo` / `TrackInfo` | song metadata |
| `TrackData_<n>` / `SO_TrackData_TrackData_<n>` / `TrackData` | notes of one difficulty (n = 0..4 in observed files) |
| `ClipInfo_<n>` / `SO_ClipInfo_ClipInfo_<n>` / `ClipInfo` | audio clip, BPM and time signature markers, cue points |

- `largeStringValuesContainer.values[]` entries: `{ "key": "<jsonKey>", "val": "<JSON string>", "loadedGenerationId": 1 }`.
- Companion files: `AlbumArt/<name>.png` and `AudioClips/<name>.ogg|mp3` under the game's `Custom` folder (`%USERPROFILE%/AppData/LocalLow/Super Spin Digital/Spin Rhythm XD/Custom`). A `.zip` backup (SpinShare download) contains the `.srtb`, `AlbumArt*` and audio files (SRTBEditor load code). The game also keeps `.bak` copies in the temp directory.

## Structure / metadata
### TrackInfo (keys seen)
`trackOrder`, `trackId`, `albumArtReference {bundle, assetName, m_guid}`, `backgroundId {backgroundId}`, `backgroundColoring {id}`, `artistName`, `featArtists`, `title`, `subtitle`, `trackLabel`, `charter`, `description`, `titleTextColor`, `subtitleTextColor`, `titleOffsetY`, `spotifyLink`, `appleMusicLink` (older files), `countdownOffset`, `difficultyRating`, `difficultyRatings`, `difficulties[] { bundle: "CUSTOM", assetName: "TrackData_<n>", m_guid, _active, _difficulty, _compatibilityVersion }`, `platformFilter` (-1), `trackType` (1), `editorFunction`, `allowCustomLeaderboardCreation`.

### TrackData (one per difficulty)
| Field | Meaning |
|---|---|
| `difficultyType` | 2 Easy, 3 Normal, 4 Hard, 5 Expert, 6 XD, 7 RemiXD (SRTBEditor `diffTypeNames`; the editor stores `index + 2`) |
| `difficultyRating` | numeric rating (e.g. 20, 30, 50 in a real chart) |
| `noteSerializationFormat` | 0 = floating-point notes in `notes`; 2 = binary-style integer ticks in `binaryNotes`; other values unknown/compressed (`notesCompressed`) |
| `notes` | format 0 note list (below) |
| `binaryNotes` | format 2 note list: `{tk, tp, c, p, s}` |
| `previewLoopBars {min,max}` | preview bar range |
| `goBeatOffsetFromFirstNote` | beats before the first note where "GO" is shown (template default -4) |
| `clipData[] {clipIndex, startBar, endBar, transitionIn, transitionInValue, transitionInOffset, transitionOut, transitionOutValue, transitionOutOffset}` | which ClipInfo clip plays over which bars |
| `clipInfoAssetReferences[] {bundle, assetName, m_guid}` | points at `ClipInfo_<n>` |
| `backgroundId`, `background`, `groundSettingsToUse`, `groundSettingsOverTime`, `splinePath`, `splinePathData` | scenery and track shape (splines for the twisty track) |
| `tutorialObjects`, `rewindSections`, `references {version, RefIds}`, `lastEditedOnDate`, `revisionVersion`, `compatibilityVersion`, `isTutorial`, `tutorialTitleTranslation` | misc |

### ClipInfo
`timeSignatureMarkers[] {startingBeat, ticksPerBar, tickDivisor, beatLengthType, beatLengthDotted}`, `bpmMarkers[] {beatLength, clipTime, type}`, `cuePoints[] {name, time}`, `clipAssetReference {bundle, assetName, m_guid}` (audio clip file name, no extension), and optionally `lyrics`.

## Timing model
- Notes carry **absolute seconds** on the audio clip, not beats: format 0 `time` is a float in seconds (verified: the last note of a 74-minute album chart is at 4472.5 s; ClipInfo markers reach 4466 s). Format 2 `tk` = `round(time * 100000)` (SRTBEditor `changeNoteEncodings`), i.e. units of 10 microseconds.
- `bpmMarkers[i].beatLength` is **seconds per beat** (60/BPM; Chronomia writes `60/bpm`); `clipTime` is the second at which this tempo starts. Tempo changes are piecewise constant. `type` is 0 in all observed files (other values unknown).
- `timeSignatureMarkers[].startingBeat` is a beat index counted from the clip start (negative = before the audio start); `ticksPerBar` / `tickDivisor` give the signature (4/4 default). `beatLengthType` and `beatLengthDotted` select the beat unit (6/8 workaround in the guide shows the editor cannot express some fractions).
- Beat positions are only needed for editors and for `goBeatOffsetFromFirstNote`; playback uses the stored seconds.

## Notes
Format 0 note: `{ "time": float seconds, "type": int, "colorIndex": int, "column": int, "m_size": int }`. Format 2 note: `{ "tk", "tp", "c", "p", "s" }` with the same meaning in order (`time`, `type`, `colorIndex`, `column`, `m_size`).

| `type` | Name (SRTBEditor diagnostics) |
|---|---|
| 0 | match note |
| 1 | beat note |
| 2 | right spin |
| 3 | left spin |
| 4 | slider (hold start); a following type 5 is the slider end |
| 5 | note endpoint / slider end |
| 8 | tap |
| 11 | beat-hold end |
| 12 | scratch |

- `colorIndex`: 0 = blue, 1 = red; higher values 2/3 appear as invisible (off-track) notes (SRTBEditor `calculateBalance`: "invis" counts for c >= 2).
- `column`: signed lane position on the wheel. In a real chart, match/tap notes use -4..4 (mostly -2, 0, 2); 0 is the center. Slider and beat-hold notes also use it. `m_size`: size/shape value of unclear meaning (0..5 observed; type 5 with `m_size` 2 marks a slider release in SRTBEditor logic). [unknown]
- Notes within 50 ticks (0.5 ms) of each other are treated as one stack by SRTBEditor (stacked matches must all be hit together).
- Sliders: type 4 start, optional intermediate type 4/5 points (each with its own `column` and `m_size`), final type 5. Beat-hold: type 1 start plus type 11 end.
- Mutual constraints (misaligned stacks, "unmissable" notes) are a gameplay issue; see SRTBEditor `diagnostics-checker.js`.

## Audio & images
- Audio: `ClipInfo.clipAssetReference.assetName` names a file in `Custom/AudioClips` (.ogg Vorbis or MP3 per the guide). Several ClipInfo entries (several audio files) are possible; each TrackData selects via `clipInfoAssetReferences` / `clipData[].clipIndex` (SRTBEditor says multi-clip charts are not fully supported).
- Cover art: `TrackInfo.albumArtReference.assetName`, file in `Custom/AlbumArt` (1024x1024 recommended by the guide).
- Backgrounds are referenced by GUID-like `backgroundId` strings, not user files (the guide says custom backgrounds are not editable).

## Versions & variants
- `revisionVersion` / `compatibilityVersion` per TrackData (0 in observed files); `noteSerializationFormat` 0 (float) versus 2 (binary ticks) is the main format break; SRTBEditor can migrate 0 -> 2. Very old files ("ancient .srtb formats") and charts with missing/out-of-order fields are reported to break SRTBEditor.
- Official tracks use the same container; `bundle` values other than `CUSTOM` refer to game asset bundles.

## Quirks & pitfalls
- Double-encoded JSON: payloads must be parsed twice and re-stringified without extra whitespace on save.
- Key names mix camelCase (`colorIndex`) and Unity-style `m_size`/`m_guid`.
- Time units differ between note formats (seconds float vs 10 us ints).
- Difficulty slots and `difficultyType` numbering start at 2; slot index != difficulty.
- Unknown fields must be preserved when round-tripping (many Unity-only fields).

## Example
Real skeleton, quoted from `chronomia/converters/srtb.js` (container only, payloads are the embedded JSON strings):
```json
{"unityObjectValuesContainer":{"values":[
  {"key":"TrackInfo","jsonKey":"SO_TrackInfo_TrackInfo","fullType":"TrackInfo"},
  {"key":"TrackData_0","jsonKey":"SO_TrackData_TrackData_0","fullType":"TrackData"},
  {"key":"ClipInfo_0","jsonKey":"SO_ClipInfo_ClipInfo_0","fullType":"ClipInfo"}]},
 "largeStringValuesContainer":{"values":[
  {"key":"SO_TrackInfo_TrackInfo","val":"{...TrackInfo JSON...}","loadedGenerationId":1},
  {"key":"SO_TrackData_TrackData_0","val":"{...TrackData JSON...}","loadedGenerationId":1},
  {"key":"SO_ClipInfo_ClipInfo_0","val":"{...ClipInfo JSON...}","loadedGenerationId":1}]},
 "clipInfoCount":1}
```
A decoded format-0 note list from the SRTBEditor template `CUTIEMARKS (And the Things That Bind Us).srtb`, difficulty 0, first entries:
`{"time":1308.2274,"type":0,"colorIndex":0,"column":2,"m_size":0}`, `{"time":1308.4580,"type":4,"colorIndex":0,"column":2,"m_size":3}`, `{"time":1308.6164,"type":5,"colorIndex":0,"column":-2,"m_size":0}`.

## ROX support
Not read by ROX. Wheel positions and spins do not map to columns; a decoder would have to project `column` to lanes and drop spins/scratches.

## Parsers & tools
- SRTBEditor (JavaScript web editor, load/save/diagnostics): https://github.com/plushproto/SRTBEditor
- Chronomia (JavaScript converters osu!/sm/chart/BMS/KSH to SRTB): https://github.com/LavenderTheGreat/chronomia
- SpinShare API/site (zip downloads): https://spinsha.re
- In-game editor (official).

## Sources
- https://www.spinrhythmgame.com/editor-guide
- https://github.com/plushproto/SRTBEditor (scripts `main.js`, `chart-loading.js`, `charter-utils.js`, `diagnostics.js`, `diagnostics-checker.js`, templates `*.srtb`)
- https://github.com/LavenderTheGreat/chronomia (`converters/srtb.js`)
- https://steamcommunity.com/sharedfiles/filedetails/?id=2994362851 (multiple audio tracks guide; ClipInfo duplication; not opened, found via search)
