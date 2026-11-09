# Smash Drums Indies package (`.indies`, `meta.json`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive (ZIP with JSON)

## Overview
A `.indies` file is a ZIP archive holding one song: its metadata, all four difficulty charts in a single `meta.json`, the audio and menu art. The structure is documented by the community Smash Drums Editor (`docs/FILE_FORMATS.md`), which also imports/exports Clone Hero `.chart`, Paradiddle `.rlrr` and plain `meta.json`. This is a third-party description (not from the game's developer); some fields (`SongPhases`) have unknown semantics, and the game-side behaviour noted below is as reported by that editor's documentation.

## Contents

- `meta.json`: metadata and all difficulty charts (also exists standalone with charts embedded).
- `audio.ogg`: full song (real Ogg Vorbis).
- `cover.png`: 500x500 album art.
- `preview.wav`: 12-second menu preview, 22050 Hz mono.

The chart format is described in this page (`meta.json`).

## Container & encoding
- ZIP archive (`.indies`) with these entries:

| File | Description |
|---|---|
| `meta.json` | metadata and all difficulty charts |
| `audio.ogg` | full song, must be real Ogg Vorbis (the editor transcodes non-Ogg sources on export) |
| `cover.png` | 500x500 album art |
| `preview.wav` | 12-second menu preview, 22050 Hz mono |

- `meta.json` also exists standalone with charts embedded; the audio is then loaded separately and `FilePath` names the file.
- JSON, UTF-8; keys are PascalCase except the lowercase `beat`/`timer` of timing anchors and `phase`/`power`/`phaseName`.
- Export requires at least one note on the Extreme difficulty and the full-song audio loaded.

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
- Charts: `ChartEasy`, `ChartNormal`, `ChartHard`, `ChartExtreme` (four difficulties).

## Timing model
- **Beats.** Each note has a `Beat` (fractional allowed, 1/16 grids and finer; the editor uses 480 ticks per beat internally).
- `SongTiming[]` is the tempo map: anchors `{ beat, timer }` mapping a whole beat number to a time in seconds. The `beat` field must be an integer ("Smash `SongTimingItem.beat` is an `int`"): fractional anchors are coerced by the game and the audio drifts. A constant tempo is typically `{0,0}`, `{1, 60/BPM}`, `{endBeat, endBeat*60/BPM}` with integer `endBeat`. Between anchors time is interpolated linearly in beat (inference from "tempo map").
- `SongOffsetSeconds`: seconds of chart time before the audio starts; often baked into `SongTiming[0].timer` with the field set to 0.
- Seconds for a note: `t = timer_i + (Beat - beat_i) * (timer_{i+1} - timer_i) / (beat_{i+1} - beat_i)` between surrounding anchors [inference].

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

`Strength`: 0 Crystal (Arcade only), 1 Neutral, 2 Burning (Arcade only); Classic play ignores non-Neutral strengths, so classic-compatible charts keep Neutral.
No holds or sustains exist in the documented format. Simultaneous notes are several entries with the same `Beat`.

Clone Hero mapping used by the editor: Smash Hi-hat to CH pad 2 (yellow cymbal, +64 flag), Snare to 1, Kick to 0, Cymbal to pad 3 (blue cymbal), Tom to pad 4 (green), Clapfire has no CH equivalent. CH cymbal notes are lane + 64.

## Audio & images
`audio.ogg`, `cover.png` (500x500), `preview.wav` (12 s, 22050 Hz mono). The editor accepts mp3, wav, ogg, flac, m4a, aac for manual loading.

## Versions & variants
- Native `.indies` versus standalone `meta.json`; Clone Hero `.chart` (`[ExpertDrums]` etc., with `[SyncTrack]`), Paradiddle `.rlrr` and `.json` are import paths of the editor, not game formats.
- No version key observed. Real files may add `"anchored": true` to `SongTiming` entries [observed in samples/indiesdb_Come_Out_And_Play_28034dfe/meta.json].

## Quirks & pitfalls
- Integer-only `SongTiming.beat`.
- `Strength` 0 and 2 are ignored in Classic mode and only affect Arcade.
- PascalCase and lowercase key mix.
- Do not feed the drum stem as song audio (the editor requires the full song).

## Example
Quoted from the editor's `FILE_FORMATS.md` (the schema example; origin: https://github.com/JStillxSKS/SmashDrumsEditor):
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

Committed in [`samples/`](samples/): six real community charts from the Indies-DB database (`<set>/meta.json`, the chart member of each `.indies` package; the audio, cover and preview of the packages are not kept, and no `.indies` archive is stored) plus one hand-written synthetic `synthetic-meta.json`. See [`samples/SOURCES.md`](samples/SOURCES.md) for every file's source URL, fetch date, sha256 and terms.

Observed in the real files [observed in samples/indiesdb_*/meta.json]: all four charts are filled (108-1387 notes); ids 0-4 used (Clapfire 5 not seen), `Strength` 0/1/2 all occur; `SongTiming` can hold hundreds of anchors (432 and 694 in two live-recorded songs) against 1-4 for constant-tempo songs; anchors may carry an extra `"anchored": true` key; `SongOffsetSeconds` is 0 in all six.

More: Indies-DB (`https://indies-db.vercel.app`; its public Supabase storage URLs follow `.../storage/v1/object/public/indies/maps/<mapper>/<id>.indies`) or the Smash Drums Editor export. `.indies` is a ZIP container (`meta.json`, `audio.ogg`, `cover.png`, `preview.wav`); only the chart member is kept here.

## Sources
- https://github.com/JStillxSKS/SmashDrumsEditor (`README.md`, `docs/FILE_FORMATS.md`)
