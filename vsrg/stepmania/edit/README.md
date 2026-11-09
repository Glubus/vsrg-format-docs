# StepMania edit file (`.edit`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text

## Overview

A `.edit` file is a single-chart simfile fragment: `.sm`/`.ssc` syntax with a `#SONG` tag naming the target song, then one chart. StepMania (3.9 on, and ITG, Etterna, ITGmania, OutFox) loads it from the profile's `Edits/` folder and from the song folder. No real `.edit` sample is in the repo; the `.ssc` sample [`../ssc/samples/Tokimeki Experience.ssc`](../ssc/samples/Tokimeki%20Experience.ssc) has an inline `Edit` chart (`#DESCRIPTION:terstedit STRING lolol .,-.a;`).

## Container & encoding

- Text, same tokenizer as [`.sm`](../sm/README.md#container--encoding), read with unescape on. One file = one chart.
- Locations (StepMania `SongManager::LoadStepEditsFromProfileDir`, `Song::LoadEditsFromSongDir`): `<profile>/Edits/*.edit` (flat, old style: the `#SONG` tag names the song), `<profile>/Edits/<Group>/<Song folder>/*.edit` (new style: `#SONG` may be omitted, the song is inferred from the path), and `*.edit` next to the song's simfile (loaded with the song as context).
- Loader order: StepMania tries the `.ssc`-style loader first and the `.sm`-style loader on failure, so both layouts below are valid.
- Limits: `MAX_EDIT_STEPS_SIZE_BYTES` per file (larger edits are refused: "unreasonably large"), `MAX_EDITS_PER_SONG_PER_PROFILE` per song and `MAX_EDIT_STEPS_PER_PROFILE` per profile.
- File naming (writer `NotesWriterSSC::GetEditFileName`): `<translit full title> - <description>.edit`, with ` (doubles)` appended for `dance-double`; characters illegal on FAT are stripped.

## Structure / metadata

SSC-style (what StepMania 5 writes, `NotesWriterSSC::GetEditFileContents`):

```
#SONG:<Group>/<Song folder>;
//---------------dance-single - <description>----------------
#NOTEDATA:;
#CHARTNAME:...;
#STEPSTYPE:dance-single;
#DESCRIPTION:<edit name>;
#DIFFICULTY:Edit;
#METER:<n>;
#RADARVALUES:...;
#CREDIT:...;
[optional chart timing tags: #OFFSET/#BPMS/#STOPS/...]
#NOTES:
<measures>
;
```

SM-style (older, still loaded): `#SONG:<Group>/<Song folder>;` then one `#NOTES:` tag with the six `.sm` parameters (`stepstype:description:difficulty:meter:radar:notedata`).

| Tag | Meaning |
|---|---|
| `#SONG` | `Group/Song folder` path below `Songs/` (backslashes converted to `/`); resolved with `SongManager::FindSong`. If the song is missing the edit is refused ("requires a song ... that isn't present"). Ignored on a second occurrence. |
| rest | the `#NOTES` / `#NOTEDATA` chart syntax of [`.sm`](../sm/README.md) / [`.ssc`](../ssc/README.md) |

The loader forces `Difficulty_Edit` whatever the file says. For `.ssc`-style edits, chart-level timing tags are honoured regardless of `#VERSION` (`for_load_edit`). An edit identical to one already loaded ("duplicate") is refused. Only the first chart of a file is used ("Only allow one Steps per edit file!").

## Timing model

Edits reuse the target song's timing (offset, BPMs, stops, ...); the file normally carries only notes. Beats and rows are as in `.sm` (48 rows/beat, 4 beats/measure). An `.ssc`-style edit may define its own timing tags (split timing), which replace the song timing for that chart.

## Notes

Same as [`.sm` notes](../sm/README.md#notes): column count and order from `#STEPSTYPE` (a step type the song's game supports), chars `0 1 2 3 4 M L F K`.

## Audio & images

None: all assets belong to the target song.

## Versions & variants

- `.edit` in a song folder or profile; in the arcade-oriented ITG builds edits are stored on memory cards. `.sm`-style layout is the SM 3.9/4 era; `.ssc`-style is SM5.
- A lone `.sm` file renamed to `.edit` is handled specially by the `.sm` note loader (`LoadNoteDataFromSimfile`: "HACK?: If this is a .edit fudge the edit difficulty").

## Quirks & pitfalls

- Without the target song installed the file is useless; a converter must resolve `#SONG` itself.
- Titles in the file name are transliterated, so names can collide ("isn't guaranteed" unique).
- A file with several charts silently keeps the first.
- Metadata (title/artist/audio) is not in the file: ROX or any importer needs the song's own `.sm`/`.ssc`.

## Example

Hand-built from the writer's layout above (illustrative, not a real file):

```
#SONG:Example Pack/Example Song;
#NOTEDATA:;
#STEPSTYPE:dance-single;
#DESCRIPTION:my edit;
#DIFFICULTY:Edit;
#METER:5;
#NOTES:
1000
0100
0010
0001
;
```

## ROX support

ROX reads `.edit` through `rox::formats::sm_edit` (decode only). `EditDecoder::song_path` normalises `#SONG` (`Group/Song folder` or `Song folder`) and refuses absolute paths, drives, `.`/`..` parts, more than two parts and control characters; the first `#SONG` counts. `decode_for_song` / `decode_for_header` / `decode_for_song_file` lay the chart over the song's `.sm`/`.ssc` header (title, artist, `#OFFSET`, `#BPMS`, `#STOPS`, `#DELAYS`, `#WARPS`, `#FAKES`, `#MUSIC` relative to the song folder), or use the chart's own timing in an `.ssc`-style edit.

- Both layouts read (`#NOTEDATA` before the first `#NOTES` = `.ssc` style, else six-parameter `#NOTES`). Difficulty forced to `Edit`, chart named by `#DESCRIPTION`, first chart only.
- Step types are those of the `.sm` decoder (`dance-single`, `dance-solo`, `dance-double`, `pump-single`, `pump-halfdouble`, `kb7-single`); others fail with the reason.
- Files over 60 KiB (`MAX_EDIT_STEPS_SIZE_BYTES`) are refused.
- `auto_decode` of an `.edit` path fails with `InvalidFormat("edit needs its song")`; finding the song (`Songs/<Group>/<Song folder>` or the edit's own folder) is the caller's job.
- Source: `rhythm-open-exchange/src/formats/sm_edit/` (`mod.rs`, `tests.rs`) and `sm/song_header.rs`. Tests build their files in memory from the layouts above.

Prism (`docs/game.md` "Formats de danse"): the scan finds the song in `<library root>/<Group>/<Song folder>` and `<library root>/Songs/<Group>/<Song folder>` of every enabled root (folder name, any case; a one-part `#SONG` in `<root>/<Song folder>` and `<root>/Songs/<Song folder>`; never by title), using its `.ssc` else its `.sm`. Audio is the song's (absolute path); the song's background is not shown; the MP3 is timed like the song's. A missing song gives the reason `editSongMissing`. Every scan rereads every `.edit`.

## Parsers & tools

- StepMania: [NotesLoaderSM.cpp `LoadEditFromFile/LoadEditFromMsd`](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp), [NotesLoaderSSC.cpp `LoadEditFromMsd`](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSSC.cpp), [NotesWriterSSC.cpp `GetEditFileContents`](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSSC.cpp), [SongManager.cpp `LoadStepEditsFromProfileDir`](https://github.com/stepmania/stepmania/blob/master/src/SongManager.cpp), [Song.cpp `LoadEditsFromSongDir`](https://github.com/stepmania/stepmania/blob/master/src/Song.cpp) (C++).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (Drano edits from archive.org item `StepManiaDranoEdits`, `edits_full (Drano).zip` with 440 edits, old SM layout only; synthetic files do not count as real). No real SSC-layout (`#NOTEDATA`) `.edit` was found.

More: the rest of the Drano zip; `AstrosEditsDanceDanceRevolution` (archive.org, 38 MB, DDR edit packs, not inspected); your own profile's `Edits/` folder after saving an edit in StepMania 5's Edit mode (`NotesWriterSSC::GetEditFileContents` writes `<translit title> - <description>.edit`).

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSSC.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSSC.cpp
- https://github.com/stepmania/stepmania/blob/master/src/SongManager.cpp
- https://github.com/stepmania/stepmania/blob/master/src/Song.cpp
- https://github.com/stepmania/stepmania/blob/master/src/Profile.cpp (`EDIT_STEPS_SUBDIR = "Edits/"`)
- ROX source: `rhythm-open-exchange/src/formats/sm/mod.rs`
