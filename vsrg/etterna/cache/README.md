# Etterna chart cache (`<chartkey>.cache`, `songdata.cache`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (+ SSC text companion)

## Overview

Etterna can export a song pack in a *pre-digested* form: for each song a cache `.ssc` text file, and for each chart a binary `.cache` file that holds only the tap timings. The code lives in two places of the Etterna source (commit `2d706147cc4bcf95a8ceb24dc4f4129be207f803`):

- `SongManager::GenerateCachefilesForGroup(pack)` writes, inside every song folder of the pack, `songdata.cache` (the song's `.ssc` text written by `NotesWriterSSC::Write(..., bSavingCache = true)` through a temporary `Cache/tmp_<pack>.ssc`) and one `<chartkey>.cache` per chart, then zips the pack folder into `Cache/<pack>.zip` and removes the generated `.cache` files again ("Zipping song directory...", "Removing cache files that were generated...").
- `ScreenInstallOverlay` (pack installer overlay) has an equivalent path that writes `<chartkey>.cache` into a note-data output directory, `<songkey>.ssc` (songkey = hex SHA-1 of the concatenated chart keys) and copies banner, CD title and background images next to it.

The purpose (inference from the code, no spec exists) is to let the online side read chart data without parsing `.sm`/`.ssc`. The `.cache` files are **chart data**, but only a reduced model: taps and hold heads as a bitmask per row, without hold ends, mines, lifts, fakes or keysounds.

## Packaged in

Zipped with the song folders in `Cache/<pack>.zip` (`GenerateCachefilesForGroup`).

## Container & encoding

`<chartkey>.cache`: no header, no magic number: the raw bytes of a C++ `std::vector<NoteInfo>` (`file.write(&serializednd[0], size * sizeof(NoteInfo))`). The only read-back in the source is a debug re-read in `ScreenInstallOverlay.cpp` that computes `size = file_length / sizeof(NoteInfo)` records; no production reader is in the Etterna source (it is presumably on the online side) [inference]. Byte order and layout are those of the machine that wrote it (little-endian on x86) [inference].

`songdata.cache` / `<songkey>.ssc`: text, see [`.ssc`](../../stepmania/ssc/README.md) plus the cache tags below.

## Structure / metadata

`NoteInfo` (`Models/NoteData/NoteDataStructures.h`):

```c++
struct NoteInfo { unsigned int notes; float rowTime; };   // 8 bytes, no padding on common ABIs
```

- `notes`: bit `t` (`1 << t`) is set when track `t` has a *note* on that row (`TapNote::IsNote()`), in `NoteData::SerializeNoteData`. Rows without any note are dropped.
- `rowTime`: seconds of the row **minus the time of the first non-empty row** (`etaner[i] - etaner[0]`; the comment "see note in serialize 2 about zeroing out element 0"); a `float`.
- Records are in row order. A second serializer (`SerializeNoteData2`) uses the value `128` (bit 7) in `notes` for rows that carry only non-tap objects when building chart keys; it is not the one written to the cache files [inference from `NoteData.cpp`].

Text companion tags (written between `// cache tags:` and `// end cache tags` of the `.ssc`): `#FIRSTSECOND #LASTSECOND #SONGFILENAME #HASMUSIC #HASBANNER #MUSICLENGTH`; per chart `#MSDVALUES` and `#CHARTKEY` (see [Etterna](../README.md)).

## Timing model

Absolute seconds per row (already resolved through the chart's timing data: `td->BuildAndGetEtaner(nerv)` gives the elapsed time of each non-empty row). Times are relative to the first note.

## Notes

Column count is the chart's track count (bit width of `notes`); there is no key-count field, so a reader must get it from `#STEPSTYPE` in the companion `.ssc`.

## Audio & images

None in the `.cache`; the pack zip may carry the audio (preference `CacheZipsContainAllAssets`) and the installer path copies banner/CD title/background images.

## Versions & variants

No version field. Two writers (pack builder, installer overlay) with the same record layout.

## Quirks & pitfalls

- Headerless, so the file cannot be validated; a size that is not a multiple of 8 is corrupt.
- Hold tails are not stored: hold length is lost.
- Times are relative to the first note, so absolute audio sync information is only in the companion `.ssc`.
- The installer overlay path reads the file back using `sizeof(NoteData)` for the read length in one place (`ScreenInstallOverlay.cpp`) [observed; looks like a bug in a debug read-back, not part of the format].

## Example

None committed (see Getting samples). Layout of two records for a chord on columns 0 and 3 on the first row, then a tap on column 1 0.5 s later (little-endian, hand-computed from the struct, not from a file):

```
09 00 00 00 | 00 00 00 00      notes=0b1001  rowTime=0.0   (first row)
02 00 00 00 | 00 00 00 3F      notes=0b0010  rowTime=0.5
```

## ROX support

Not read by ROX.

## Parsers & tools

Etterna C++ only (`SongManager.cpp`, `ScreenInstallOverlay.cpp`, `NoteData.cpp`). EtternaOnline consumes these packs on the server side (not open source) [inference].

## Getting samples

None committed or in the manifest: these files are generated artefacts of Etterna's pack tooling and are not stored in any repository checked. How to produce one: in a stock Etterna build, open the pack-export action that calls `SongManager::GenerateCachefilesForGroup` (the code path creates `Songs/<pack>/<song>/songdata.cache` and `<chartkey>.cache`, then `Cache/<pack>.zip`) [inference: the menu entry/Lua binding that calls it was not traced]. Alternatively compute a record array yourself from a committed chart (for example `../../stepmania/ssc/samples/Springtime.ssc`) with the rules above.

## Sources

- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Singletons/SongManager.cpp (`GenerateCachefilesForGroup`)
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Screen/Others/ScreenInstallOverlay.cpp
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteData/NoteData.cpp (`SerializeNoteData`)
- https://github.com/etternagame/etterna/blob/2d706147cc4bcf95a8ceb24dc4f4129be207f803/src/Etterna/Models/NoteData/NoteDataStructures.h
