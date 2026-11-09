# Smash Drums Indies package (`.indies`, `meta.json`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive (ZIP with JSON)

## Overview
A `.indies` file is a ZIP of one song: all four difficulty charts and metadata in `meta.json`, plus audio and menu art. The community Smash Drums Editor documents it (`docs/FILE_FORMATS.md`) and also imports/exports Clone Hero `.chart`, Paradiddle `.rlrr` and plain `meta.json`. Third-party description; `SongPhases` semantics and game-side behaviour are as that documentation reports.

## Contents
See the entries table in Container & encoding.

## Container & encoding
- ZIP archive (`.indies`) with these entries:

| File | Description |
|---|---|
| `meta.json` | metadata and all difficulty charts |
| `audio.ogg` | full song, must be real Ogg Vorbis (the editor transcodes non-Ogg sources on export) |
| `cover.png` | 500x500 album art |
| `preview.wav` | 12-second menu preview, 22050 Hz mono |

- Standalone `meta.json` embeds the charts; the audio is loaded separately and `FilePath` names the file.
- JSON, UTF-8. Keys are PascalCase except the lowercase `beat`/`timer` of timing anchors and `phase`/`power`/`phaseName`.
- Export needs at least one note on the Extreme difficulty and the full-song audio loaded.

## Structure / metadata
```json
{
  "NameArtist": "Artist", "NameSong": "Song Title", "NameCharter": "Charter",
  "FilePath": "audio.ogg",
  "SongOffsetSeconds": 0.0,
  "SongTiming": [{ "beat": 0, "timer": 0 }],
  "SongPhases": [],
  "ChartEasy": [], "ChartNormal": [], "ChartHard": [],
  "ChartExtreme": [{ "Beat": 4, "Id": 1, "Strength": 1 }]
}
```
- `SongPhases[]`: `{ beat, phase, power, phaseName }` section markers (phase beats may be fractional) [meaning of `phase`/`power` unknown; the editor labels them with `phaseName`].
- Charts: `ChartEasy`, `ChartNormal`, `ChartHard`, `ChartExtreme`.

## Timing model
- Each note has a `Beat` (fractional allowed, 1/16 grids and finer; the editor uses 480 ticks per beat internally).
- `SongTiming[]` is the tempo map: anchors `{ beat, timer }` mapping a whole beat number to seconds. `beat` must be an integer ("Smash `SongTimingItem.beat` is an `int`"); the game coerces fractional anchors and the audio drifts. A constant tempo is typically `{0,0}`, `{1, 60/BPM}`, `{endBeat, endBeat*60/BPM}` with integer `endBeat`. Between anchors time is interpolated linearly in beat (inference from "tempo map").
- `SongOffsetSeconds`: seconds of chart time before the audio starts; often baked into `SongTiming[0].timer` with the field set to 0.
- Note time: `t = timer_i + (Beat - beat_i) * (timer_{i+1} - timer_i) / (beat_{i+1} - beat_i)` between surrounding anchors [inference].

## Notes
Note object: `{ "Beat": number, "Id": 0..5, "Strength": 0..2 }`.

| Id | Instrument |
|---|---|
| 0 | Bass (blue kick drum) |
| 1 | Snare (red) |
| 2 | Cymbal (yellow) |
| 3 | Tom (green) |
| 4 | Hi-hat (pink) |
| 5 | Clapfire (orange) |

Left-to-right lane order on the editor highway: Hi-hat (4), Snare (1), Kick (0), Cymbal (2), Tom (3), Clapfire (5).

`Strength`: 0 Crystal (Arcade only), 1 Neutral, 2 Burning (Arcade only). Classic play ignores non-Neutral strengths, so classic-compatible charts keep Neutral.
The documented format has no holds or sustains. Simultaneous notes are several entries with the same `Beat`.

Clone Hero mapping in the editor: Smash Hi-hat to CH pad 2 (yellow cymbal, +64 flag), Snare to 1, Kick to 0, Cymbal to pad 3 (blue cymbal), Tom to pad 4 (green). Clapfire has no CH equivalent. CH cymbal notes are lane + 64.

## Audio & images
The editor accepts mp3, wav, ogg, flac, m4a, aac for manual loading; export writes the entries above.

## Versions & variants
- Clone Hero `.chart` (`[ExpertDrums]` etc., with `[SyncTrack]`), Paradiddle `.rlrr` and `.json` are editor import paths, not game formats.
- No version key observed. Real files may add `"anchored": true` to `SongTiming` entries [observed: indiesdb_Come_Out_And_Play_28034dfe/meta.json].

## Quirks & pitfalls
- `SongTiming.beat` is integer-only.
- `Strength` 0 and 2 only affect Arcade.
- Key case mixes PascalCase and lowercase.
- The editor requires the full song as audio, not the drum stem.

## Example
The schema example from the editor's `FILE_FORMATS.md` (https://github.com/JStillxSKS/SmashDrumsEditor):
```json
{
  "NameArtist": "Artist",
  "NameSong": "Song Title",
  "NameCharter": "Charter",
  "FilePath": "audio.ogg",
  "SongOffsetSeconds": 0.0,
  "SongTiming": [{ "beat": 0, "timer": 0 }],
  "SongPhases": [],
  "ChartEasy": [],
  "ChartNormal": [],
  "ChartHard": [],
  "ChartExtreme": [{ "Beat": 4, "Id": 1, "Strength": 1 }]
}
```

## ROX support
Not read by ROX. A decoder could map Ids 0..5 to six columns (BPM from `SongTiming`), tap-only.

## Parsers & tools
- Smash Drums Editor (TypeScript, read/write `.indies`, `meta.json`, `.chart`, `.rlrr`): https://github.com/JStillxSKS/SmashDrumsEditor
- Paradiddle-format cross-reference: [`../../paradiddle/rlrr/README.md`](../../paradiddle/rlrr/README.md), Clone Hero [`chart`](../../../vsrg/clone-hero/chart/README.md)

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (`<set>/meta.json` chart members only). [observed: indiesdb_*/meta.json] all four charts filled (108-1387 notes); ids 0-4 used (Clapfire 5 not seen); `Strength` 0/1/2 all occur; `SongTiming` has 1-4 anchors for constant tempo, hundreds in live-recorded songs (432 and 694); extra `"anchored": true` key possible; `SongOffsetSeconds` is 0 in all six.

More: Indies-DB (`https://indies-db.vercel.app`; public Supabase storage URLs follow `.../storage/v1/object/public/indies/maps/<mapper>/<id>.indies`) or the Smash Drums Editor export.

## Sources
- https://github.com/JStillxSKS/SmashDrumsEditor (`README.md`, `docs/FILE_FORMATS.md`)
