# StepMania JSON song/chart (`.json`, "StepMania Micro")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview

Two things share this name:

1. StepMania's JSON (de)serializer (`NotesWriterJson::WriteSong/WriteSteps`, `NotesLoaderJson::LoadFromJsonFile`): a full dump of a `Song` (metadata, song timing, background changes, keysounds, lyrics, every chart with note data) as one JSON object, plus the matching loader (`*.json` in a song folder). The schema below is read from those two files.
2. StepMania Micro's data files (JS game `smjs-0.3`): `songs/<Name>/steps.js` holds `var steps = { noteData: [ [beat, track, {tapnote}], ... ] }`, the `noteData` array of `NotesWriterJson` in a JS assignment, and `song.js` holds `var song = { bpm: 148, addToMusicPosition: -0.03 }` (single BPM, offset in seconds). Only these two files were retrieved; that SM Micro data is a StepMania JSON export is inferred from the identical tuple shape (`[18.50, 0, {}]`, `[64.0, 0, {"Duration": 132, "SubType": 0, "Type": 2}]`) and the original README's links.

## Container & encoding

- JSON text (jsoncpp, `Json::Value`; `JsonUtil::WriteFile(root, file, false)` writes compactly) on the C++ side; JavaScript source (`var x = {...};`) for SM Micro.
- One file per song (`WriteSong`) or per chart (`WriteSteps`). StepMania lists `*.json` as a loader file type (`NotesLoaderJson::GetApplicableFiles`), but `NotesLoader::LoadFromDir` does not include it, so only tools and the Micro build use it [inference from the loader list].

## Structure / metadata

Song object (`WriteSong`; keys exactly as written):

| Key | Type | Meaning |
|---|---|---|
| `SongDir`, `GroupName` | string | |
| `Title`, `SubTitle`, `Artist`, `TitleTranslit`, `SubTitleTranslit`, `Genre`, `Credit` | string | |
| `Banner`, `Background`, `LyricsFile`, `CDTitle`, `Music` | string | file names |
| `Offset` | float seconds | StepMania `#OFFSET` (beat 0 at `-Offset` s) |
| `SampleStart`, `SampleLength` | float | preview, seconds |
| `Selectable` | `"YES"` / `"NO"` | |
| `FirstBeat`, `LastBeat` | float | (written, not read) |
| `SongFileName`, `HasMusic`, `HasBanner`, `MusicLengthSeconds` | string/bool/float | cache-like fields |
| `DisplayBpmType` | string | `"*"` => random display; otherwise specified |
| `SpecifiedBpmMin`, `SpecifiedBpmMax` | float | when display BPM is specified |
| `TimingData` | object | `{ "BpmSegments": [{Beat, BPM}], "StopSegments": [{Beat, Seconds}] }`: **only BPMs and stops are serialized**; the loader ignores every other segment type ("The rest are unused") |
| `LyricSegments` | array | `{StartTime, Lyric, Color}` |
| `BackgroundChanges` | array of arrays (one per layer) | `{Def: {Effect, File1, File2, Color1}, StartBeat, Rate, Transition}` |
| `ForegroundChanges` | array | same shape |
| `KeySounds` | array of strings | |
| `Charts` | array | one object per non-autogen chart |

Chart object (`Serialize(Steps)`): `StepsType` (string e.g. `dance-single`), `NoteData` (array), `Hash`, `Description`, `Difficulty` (`Beginner`..`Edit`), `Meter` (int), `RadarValues` (object keyed by `RadarCategory` names).

## Timing model

Beats are floats in tuples and segments; `Beat` in `BpmSegments`/`StopSegments`; offset in `Offset`. Rows are `lrint(beat*48)` on load. Semantics identical to `.sm` ([timing](../../stepmania/sm/README.md#timing-model)): BPM from its beat, stop after the beat. Warps/delays/speeds/scrolls are not preserved. SM Micro itself ignores all but a single `bpm` and an `addToMusicPosition` (the game computes `beat = (musicSec + addToMusicPosition) * bpm / 60`).

## Notes

`NoteData` is an array of 3-element arrays, one per note, ordered by track then row:

```
[ beat (float), track (int, 0-based column), { tapnote fields } ]
```

Tapnote object keys (omitted when default): `Type` (`TapNoteType` int, omitted for a plain Tap = 1), `SubType` (hold head only: 0 hold, 1 roll), `AttackModifiers`, `AttackDurationSeconds`, `KeysoundIndex` (omitted when -1), `Duration` (**rows**, 48 per beat; hold/roll length), `PlayerNumber`. `TapNoteType` ints: 0 Empty, 1 Tap, 2 HoldHead, 3 HoldTail, 4 Mine, 5 Lift, 6 Attack, 7 AutoKeysound, 8 Fake. A hold is **one** note with `Duration` (no tail note). Track = column index as in `.sm` for the step type.

## Audio & images

File name strings (`Music`, `Banner`, `Background`, ...). SM Micro: `songs/<Name>/<Name>.mp3` + `.ogg` (HTML5 audio `<source>` pair) and `background.png`.

## Versions & variants

- C++ JSON: no version field.
- SM Micro 0.3: `steps.js`/`song.js` JavaScript wrappers (`var steps = {noteData: [...]}`); 4 columns at fixed x positions with rotations `90, 0, 180, -90`; judgment windows `[0.05, 0.1, 0.15, 0.25, 0.3]` s; the score table shows Marvelous, Perfect, Great, Good, Boo, Miss.

## Quirks & pitfalls

- ROX maps `.json` to the Friday Night Funkin' decoder (`detect.rs`: `"json" => Fnf`), so a StepMania JSON file would be misdetected.
- `Duration` is in rows, not beats or ms.
- The loader's `Deserialize(TapNote)` reads `root["Type"]` only `if root.isInt()` (a bug: tapnotes are objects), so `Type` may load wrong; trust the writer more than the loader [source reading].
- Only BPM and stop segments survive; negative stops (warps) become stops of negative duration.

## Example

Real fragments from SM Micro 0.3's `steps.js` (Wayback copy):

```js
var steps = {
    noteData: [
        [18.50, 0, {}],
        [25.0, 0, {}],
        [64.0, 0, { "Duration": 132, "SubType": 0, "Type": 2 }],
        [68.0, 0, {}]
    ]
};
var song = { bpm: 148, addToMusicPosition: -0.03 };
```

(a hold of 132 rows = 2.75 beats on column 0 at beat 64; plain taps have `{}`.)

## ROX support

Not read by ROX, on purpose (2026-11-10): no real `.json` written by `NotesWriterJson` exists (the two samples are StepMania Micro `.js` files with one BPM, no step type and no metadata), so a reader would rest on the C++ writer alone with nothing to check it against. `.json` is routed to the FNF decoder: it would also need its own detection.

## Parsers & tools

- StepMania [NotesLoaderJson.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderJson.cpp), [NotesWriterJson.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterJson.cpp) (C++, jsoncpp); SM Micro `smjs-0.3` (JavaScript).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md): the two SM Micro 0.3 data files for the song *Lost* (Wayback snapshot `20150110120332` of the original Dropbox host: `steps.js` 11,723 bytes, `song.js` 64 bytes: `bpm: 148`, `addToMusicPosition: -0.03`), JavaScript wrappers.

No file written by `NotesWriterJson` (whole-song `.json`) was found. To produce one, build StepMania (writer in `src/NotesWriterJson.cpp`) and call it from code. [StepMania-AMX/micro](https://github.com/StepMania-AMX/micro) is a JS player derived from StepMania Micro that loads `.ucs` steps, not JSON.

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderJson.cpp, NotesWriterJson.cpp, NoteTypes.h (`TapNoteType`, `TapNoteSubType`)
- https://web.archive.org/web/20150110063934/http://old.stepmania.com/wiki/StepMania_Micro
- https://web.archive.org/web/20150110120332if_/https://dl.dropboxusercontent.com/u/2963913/smjs-0.3/index.html and its `js/steps.js`, `js/song.js`, `js/stepmania.js`
- ROX source: `rhythm-open-exchange/src/formats/auto/detect.rs`
