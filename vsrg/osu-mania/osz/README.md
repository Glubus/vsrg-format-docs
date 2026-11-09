# osu! beatmap archive (`.osz`)
Kind: package

Doc status: complete · ROX: no · Category: vsrg (osu!mania mapsets; the same archive also carries osu!standard/taiko/catch difficulties) · Encoding: archive (ZIP)

## Overview

`.osz` is the **distribution package of an osu! beatmap set**: one song (audio, background, optional video/storyboard/hitsounds) and one or more difficulties (`.osu` files, one per difficulty, each in its own game mode). Mapsets are downloaded from osu.ppy.sh/mirrors and by the in-game downloader as `.osz`; the editor's *File > Export package...* writes one into the `Exports` folder. The osu! wiki says: ".osz is an overall file archive, containing beatmaps and any additional resources such as skin or hitsounds." and lists the MIME type `x-osu-beatmap-archive`. Sibling extensions: `.osk` (skin archive), `.osr` (replay), `.osb` (shared storyboard, see [`../osb`](../osb/README.md)), `.osu` ([`../osu`](../osu/README.md)); osu!lazer additionally accepts `.olz` as an archive extension of its own export. It is a plain ZIP, no encryption, no manifest.

## Contents

- One beatmap set: audio, background, optional video, storyboard (`.osb`) and hitsounds, plus one `.osu` file per difficulty.
- Chart formats inside: [`.osu`](../osu/README.md) (osu!mania, mode 3). Other game modes use their own `.osu` pages: [osu!standard](../../../others/osu-standard/osu/README.md), [osu!taiko](../../../others/osu-taiko/osu/README.md), [osu!catch](../../../others/osu-catch/osu/README.md).

## Container & encoding

- Standard ZIP (deflate). Create it by zipping the files and renaming `.zip` to `.osz` (osu! wiki, "Using an archiver"); the osu! wiki states that `.osz` contents are extracted into the `Songs` directory and `.osk` into `Skins`.
- Entries should be at the **root** of the archive (no wrapper folder). The lazer importer is tolerant: it strips the archive-wide common directory prefix when it ends with `/` or `\` (`getShortenedFilenames`), converts paths to its standard form, and **rejects** an archive containing two entries that differ only by case ("Multiple files with the name ... (ignoring case) are present").
- File-name encoding: archives created by osu!stable write entry names in **Shift-JIS (code page 932)** rather than UTF-8; osu!lazer forces CP932 as the default entry encoding when reading (`ZipArchiveReader.DEFAULT_ENCODING`, with the comment that the future plan is to set the ZIP UTF-8 flag on export). A reader should honour the ZIP UTF-8 flag when present and otherwise try CP932.
- lazer skips directory entries and filters OS junk files through an `ExcludeSystemFileNames()` helper (its exact list was not verified here).
- lazer refuses single entries larger than 200 MiB (`ZipArchiveReader.MaximumEntrySize`).
- Charset inside the `.osu` files is UTF-8 (see the `.osu` doc).

## Structure / metadata

Typical content of a mapset archive:

| Entry | Role |
|---|---|
| `*.osu` | One file per difficulty; a single set may mix modes (`Mode: 0/1/2/3`). Naming convention `Artist - Title (Mapper) [Difficulty].osu`; the name is not parsed (the `[Metadata]` section is). |
| `*.osb` | Optional set-wide storyboard (difficulty-specific storyboard events live inside each `.osu` under `[Events]`). |
| audio (`.mp3`, `.ogg`, `.wav`) | Referenced by `AudioFilename:` in each `.osu` `[General]` section (a set may use different files per difficulty). |
| image (`.jpg`, `.png`) | Background, referenced by the `0,0,"file",x,y` event in `[Events]`. |
| video (`.mp4`, `.avi`, `.flv`, ...) | Referenced by a `Video,offset,"file"` event. |
| hitsound samples (`.wav`, `.ogg`) | Custom samples looked up by name from `[General]`/hitobject sample fields. |
| other skin-like images | Storyboard sprites, etc. |

There is no index inside the archive: the metadata (title, artist, mapper, difficulty names, set/beatmap IDs) comes **only** from the contained `.osu` files.

Identity/hashing used by clients:
- osu!stable identifies each difficulty by the **MD5 of its `.osu` file** [inference: widely stated, e.g. by fileformat sites; lazer's `BeatmapInfo.MD5Hash` stores it].
- lazer computes the set hash as the **SHA-2 hash of the concatenation of all `.osu` file contents sorted by file name** (`HashableFileTypes = ".osu"`, `ComputeHash` / `computeHashFast`); an archive with no `.osu` falls back to hashing its name. Importing a set whose hash matches an existing one is a duplicate; an update with the same online set ID replaces the old set and transfers scores for unchanged difficulties (`ImportAsUpdate`).

## Timing model

Not applicable (container); timing is in the `.osu` files (milliseconds, uninherited/inherited timing points).

## Notes

Not applicable; see [`../osu`](../osu/README.md) for mania columns (`CircleSize` = key count, `x` position -> column), hold notes, etc.

## Audio & images

All resources are plain files addressed by file name from the `.osu`/`.osb`; names are matched case-insensitively by lazer (a model with two names differing only by case is rejected, see above), but stable on Windows is case-insensitive by nature of the file system.

## Versions & variants

- `.osz` (osu!stable and lazer export). lazer additionally handles `.olz` (`BeatmapImporter.HandledExtensions = { ".osz", ".olz" }`). `.olz` is a distinct extension: lazer's own export, see [`../olz`](../olz/README.md); lazer can still export legacy-compatible `.osz` (`LegacyBeatmapExporter`, `FileExtension = ".osz"`, ppy/osu @ bb37f05). [observed in samples/ppy-osu_japanese-filename.osz] a real `.osz` may contain 0-byte audio entries. The archive format itself did not change; the `.osu` inside has `osu file format v14` currently (see the `.osu` doc for the version history).
- The old online variant **osz2** (an encrypted/streamed package used by the stable updater and `osu!direct`) is not an `.osz`; it is outside this page. [inference: mentioned from general knowledge, not from the sources consulted]

## Quirks & pitfalls

- Wrapper folders and case-colliding names break strict importers.
- Non-ASCII file names written by stable in CP932 look corrupted when decoded as UTF-8/CP437.
- Mixed-mode sets: an osu!mania importer must filter `.osu` files by `Mode: 3` itself; the archive has no per-mode index.
- The archive can also be a skin-less partial set (e.g. only `.osu` files, referencing an audio file that is absent); importers differ in tolerance.

## Example

Real audio-less archives are in [`samples/`](samples/). Illustrative, hand-built listing of a typical mania set (names invented):

```
Artist - Title (Mapper) [4K Easy].osu
Artist - Title (Mapper) [4K Hard].osu
audio.mp3
bg.jpg
```

## ROX support

Not read by ROX: ROX opens an individual `.osu` file (mode 3 only, see [`../osu`](../osu/README.md)); the mapset ZIP must be unpacked first.

## Parsers & tools

- osu!lazer (C#): [`BeatmapImporter.cs`](https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/BeatmapImporter.cs), [`ZipArchiveReader.cs`](https://github.com/ppy/osu/blob/master/osu.Game/IO/Archives/ZipArchiveReader.cs), [`RealmArchiveModelImporter.cs`](https://github.com/ppy/osu/blob/master/osu.Game/Database/RealmArchiveModelImporter.cs).
- Any ZIP library. Converters that emit `.osz`: [`brd`](https://github.com/sbruder/brd) (`ddr2osu` writes DDR SSQ+XWB into an `.osz` container, Rust).

## Getting samples

- **Committed** in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): an audio-less real mapset pair from Prelude's tests (5 and 10 mania 4K difficulties), lazer's 816-byte `japanese-filename.osz` (0-byte audio entries, CP932 entry-name test), and `built-mania-key-counts-audioless.osz`, built here (CC0 container) from MIT lazer test maps (4K/7K/10K + a v5 slider file + an `.osb`).
- **Manifest**: three lazer test archives (two tiny ones with `.ogg`/`.png`, and `241526 Soleily - Renatus_virtual_quick.osz` with 12 difficulties of all four modes plus a jpg and `__MACOSX` entries), pinned to ppy/osu @ bb37f05.
- **How to get more**: download from https://osu.ppy.sh/beatmaps or mirrors; osu!stable *File > Export package...* writes into `Exports`, lazer exports `.osz` (legacy-compatible, `LegacyBeatmapExporter`, Shift-JIS entry names) or [`.olz`](../olz/README.md) (lazer-native). The osu! installer also bundles mapsets, listed in `BundledBeatmapDownloader.cs` (names such as `241526 Soleily - Renatus.osz`, served from `assets.ppy.sh/client-resources/bundled/<id>.osz`; not fetched here). A mapset only needs to be unzipped to get its charts; audio and images in it are copyrighted and must not be redistributed.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/en.md
- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osz_(file_format)/en.md
- https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/BeatmapImporter.cs
- https://github.com/ppy/osu/blob/master/osu.Game/IO/Archives/ZipArchiveReader.cs
- https://github.com/ppy/osu/blob/master/osu.Game/Database/RealmArchiveModelImporter.cs
- https://github.com/sbruder/brd (README, `ddr2osu`)
