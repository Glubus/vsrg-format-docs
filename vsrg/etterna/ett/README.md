# Etterna song file (`.ett`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (CRLF)

## Overview

`.ett` is the extension Etterna gives to an SSC-derived song file written by `NotesWriterETT::Write` (`src/Etterna/Models/NoteWriters/NotesWriterETT.cpp`; header comment: "Writes a Song to a .ETT file"). `Song::SaveToETTFile` sets the extension (`SetExtension(sPath, "ett")`), copies an existing file to `<name>.ett.old` first, and marks the saved steps. In the Etterna source at commit `2d706147cc4bcf95a8ceb24dc4f4129be207f803`:

- the loader is a stub: `NotesLoaderETT.cpp`/`.h` contain only an `#include` and an empty include guard, and `NotesLoader::LoadFromDir` does not list ETT (order: SSC, SMA, SM, DWI, BMS, KSF, OSU);
- `Song::SaveToETTFile` has **no call site** in `src/Etterna` (a search for `SaveToETTFile` finds only its definition and declaration).

So `.ett` is, as far as the source shows, a write-only, never-invoked experiment [inference: from the absence of readers and callers]. No `.ett` file has been seen in the wild.

## Packaged in

Not packaged; would sit next to the song's `.sm`/`.ssc`.

## Container & encoding

Plain text, MSD syntax (`#TAG:value;`), lines joined with CRLF (`JoinLineList` uses `\r\n`), values escaped with `SmEscape`. Encoding Unknown (UTF-8 as in StepMania 5).

## Structure / metadata

Same layout as [`.ssc`](../../stepmania/ssc/README.md) (`NotesWriterSSC` was the template):

1. Global tags: `#VERSION:<STEPFILE_VERSION_NUMBER %.2f>;`, `#TITLE #SUBTITLE #ARTIST #TITLETRANSLIT #SUBTITLETRANSLIT #ARTISTTRANSLIT #GENRE #ORIGIN #CREDIT #BANNER #BACKGROUND #PREVIEWVID #JACKET #CDIMAGE #DISCIMAGE #LYRICSPATH #CDTITLE #MUSIC #PREVIEW #INSTRUMENTTRACK #OFFSET #SAMPLESTART #SAMPLELENGTH #SELECTABLE #DISPLAYBPM`, song timing (`#BPMS #STOPS #DELAYS #WARPS #TIMESIGNATURES #TICKCOUNTS #COMBOS #SPEEDS #SCROLLS #FAKES #LABELS`), `#LASTSECONDHINT`, `#BGCHANGES`, `#FGCHANGES`, `#KEYSOUNDS`.
2. A **cache block is always written** (unlike `.ssc`, where it is only for cache files): `// cache tags:` `#FIRSTSECOND #LASTSECOND #SONGFILENAME #HASMUSIC #HASBANNER #MUSICLENGTH` `// end cache tags`.
3. One block per chart (only charts whose chart key is non-empty): `//---------------<stepstype> - <description>----------------`, `#NOTEDATA:;`, `#CHARTNAME #STEPSTYPE #DESCRIPTION #CHARTSTYLE #DIFFICULTY #METER`, **`#MSDVALUES:`** (per-skillset ratings; `MSDToString2`: each value truncated to 5 characters, values of one rate separated by `,`, rates separated by `:`), **`#CHARTKEY:`**, `#MUSIC`, `#RADARVALUES`, `#CREDIT`, optional chart timing (`#OFFSET` + timing tags), `#DISPLAYBPM`, then `#NOTES:` (or `#NOTES2:` when the song has keysounds) and the note data.

## Timing model

As [`.ssc`](../../stepmania/ssc/README.md#timing-model): 48 rows per beat, 4 beats per measure, song-wide timing with optional per-chart overrides.

## Notes

`NoteDataUtil::GetETTNoteDataString` writes a compact encoding **for 4-column charts only** (`if (in.GetNumTracks() != 4)` the string is empty):

- One measure per segment, segments separated by `,`. Each segment starts with the numeric value of the smallest note type of that measure (`std::to_string(nt)`), then one symbol per row at that spacing, then a newline.
- A row is first spelled with one letter per column: `E` empty, `T` tap, `H` hold head, `R` roll head, `J` hold tail, `*` mine, `^` lift, `V` fake.
- Tap-only/empty rows are then replaced by one letter: `EEEE`=`?`, `TTEE`=`M`, `EETT`=`W`, `TEEE`=`L`, `ETEE`=`D`, `EETE`=`U`, `EEET`=`Y`, `TEET`=`B`, `ETTE`=`Z`, `ETET`=`G`, `TETE`=`K`, `TTTE`=`U` (the same letter as `EETE`: ambiguous in the source), `ETTT`=`I`, `TETT`=`O`, `TTET`=`P`. Rows that contain holds, rolls, mines, lifts, fakes, or are `TTTT` keep their four letters.
- Runs of empty rows are then run-length shrunk by pairwise replacement: `??`->`~`, `~~`->`|`, `||`->`!`, `!!`->`-`, `--`->`` ` ``, ` `` `->`.`.

## Audio & images

By file name in the header, as `.sm`/`.ssc`.

## Versions & variants

`#VERSION` is the Etterna `STEPFILE_VERSION_NUMBER`. Related Etterna artefacts: [`.cache`](../cache/README.md).

## Quirks & pitfalls

- No reader exists: a file cannot be loaded back by Etterna.
- The note encoding is lossy for ambiguous letters (`U`) and, because the row symbols are replaced by blind string search, a letter sequence can be re-merged across measures [inference from the replace loops starting at offset 0].
- Only 4-key charts have note data.

## Example

None: no real file, and a hand-built one would be pure inference (see Getting samples).

## ROX support

Not read by ROX.

## Parsers & tools

Etterna C++ (writer only): [NotesWriterETT.cpp](https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteWriters/NotesWriterETT.cpp), [NoteDataUtil.cpp `GetETTNoteDataString`](https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteData/NoteDataUtil.cpp), [Song.cpp `SaveToETTFile`](https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/Songs/Song.cpp).

## Getting samples

No `.ett` file is committed or in the manifest: none exists in any repository checked (Etterna, ITGmania, StepMania, parser fixtures), and the only way to produce one is to build Etterna from source and call `Song::SaveToETTFile(path, false)` from code, since no menu, Lua binding or other caller was found [inference from a source search at commit `2d706147cc4bcf95a8ceb24dc4f4129be207f803`]. Useful starting points to obtain real data of the same family: the `#CHARTKEY`/`#MSDVALUES` tagged `.ssc` cache files (see [`cache`](../cache/README.md)) produced by stock Etterna.

## Sources

- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteWriters/NotesWriterETT.cpp
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteLoaders/NotesLoaderETT.cpp
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteLoaders/NotesLoader.cpp
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteData/NoteDataUtil.cpp
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/Songs/Song.cpp
