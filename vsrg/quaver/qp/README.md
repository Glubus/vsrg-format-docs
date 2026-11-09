# Quaver mapset package (`.qp`)
Kind: package

Doc status: partial · ROX: no (ROX does not open archives; the `.qua` files inside are read) · Category: vsrg · Encoding: archive (ZIP)

## Overview

A `.qp` file is a Quaver mapset: "It contains an MP3 file and one or more QUA files" and is what the editor produces on export and what quavergame.com serves for download (FileInfo.com, "Quaver Mapset"). It bundles every difficulty (`.qua`, see [../qua/README.md](../qua/README.md)) of one mapset with its audio, background, banner and hit-sample files. Quaver imports it by dragging the file onto the game.

## Contents

- One Quaver mapset: an MP3, one or more difficulties, background, banner and hit-sample files.
- Chart format inside: [`.qua`](../qua/README.md).

## Container & encoding

- A ZIP-style archive with the extension `.qp`. Quaver opens it with SharpCompress's generic `ArchiveFactory.Open(fileName)` (so any supported archive type would load) and extracts every non-directory entry with `ExtractFullPath = true, Overwrite = true` into a temporary folder (`MapsetImporter.ExtractQuaverMapset`). The Rust crate `map-parser` reads it with the `zip` crate. In practice it is a ZIP (the Quaver ecosystem treats it as renamed zip) [inference from the above, no format magic is checked in the sources read].
- Layout: flat; `.qua` files at the archive root plus the files they reference by name (`AudioFile`, `BackgroundFile`, `BannerFile`, `CustomAudioSamples[].Path`). On extraction failure of a `.qua` entry at the root, Quaver retries with an MD5-of-name file name (`CryptoHelper.StringToMd5(path) + ".qua"`), which means any `.qua` name is acceptable and other files must keep their names (they are referenced by name).
- After extraction every `*.qua` found recursively (`SearchOption.AllDirectories`) in the folder is parsed and inserted into the map database (`InsertAndUpdateSelectedMap`).
- Accepted import extensions in `MapsetImporter.AcceptedMapType`: `.qp`, `.osz`, `.sm`, `.mcz`, `.mc`. A `.zip` or `.qpl` (Quaver playlist: a ZIP plus a `metadata.json`) is treated as a batch archive of maps.
- Path-traversal entries are rejected by the extraction call (see Quaver issue #1200 "Entry is trying to write a file outside of the destination directory").

## Structure / metadata

There is no manifest: the mapset is defined by the set of `.qua` files (each carries `MapSetId`, `Title`, `Artist`, ...). File names inside are free; the usual contents are `<difficulty>.qua` files, `audio.mp3` (or other audio), `bg.jpg`/`banner.jpg`, and optional sample files. Exact file-name conventions of the exporter are not documented in the sources consulted: Unknown.

## Timing model

Not applicable (see `.qua`).

## Notes

Not applicable.

## Audio & images

Everything referenced by name from each `.qua`; one audio file normally shared by all difficulties (it may differ per `.qua` via `AudioFile`).

## Versions & variants

No format version of its own. `.qpl` playlists (ZIP with `metadata.json`) are a related batch container (MapsetImporter), not a map package.

## Quirks & pitfalls

- Entries with `..` or absolute paths are unsafe; extract with path checks.
- Duplicate `.qua` names, or `.qua` files in sub-folders, are accepted by Quaver (recursive search).
- Uploaded mapsets can contain only the audio (Quaver issue #1200 mentions an upload whose `.qp` held only the mp3); an importer must tolerate "no `.qua`".

## Example

Not applicable (binary archive). Illustrative layout, hand-built from the rules above:

```
mymapset.qp
  audio.mp3
  bg.jpg
  1234.qua      (Mode: Keys4, DifficultyName: Hard)
  1235.qua      (Mode: Keys7, DifficultyName: Insane)
```

## ROX support

Not read by ROX: unzip first and pass each `.qua` to the `.qua` codec.

## Parsers & tools

- Quaver `MapsetImporter` (C#): https://github.com/Quaver/Quaver/blob/master/Quaver.Shared/Database/Maps/MapsetImporter.cs
- map-parser `QuaverMapset::from_path` (Rust): https://docs.rs/map-parser/0.1.5/map_parser/struct.QuaverMapset.html
- qua3osu (`.qp`/`.qua` -> `.osz`/`.osu`, C#): https://github.com/IceDynamix/qua3osu

## Sources

- https://fileinfo.com/extension/qp
- https://github.com/Quaver/Quaver/blob/master/Quaver.Shared/Database/Maps/MapsetImporter.cs
- https://docs.rs/map-parser/0.1.5/src/map_parser/qp.rs.html
- https://github.com/Quaver/Quaver/issues/1200
- https://github.com/IceDynamix/qua3osu
