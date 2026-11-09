# Malody chart package (`.mcz`)
Kind: package

Doc status: stub · ROX: no · Category: vsrg · Encoding: archive

## Overview
`.mcz` ("Malody Chart Zipped", developer Mugzone per fileinfo.com) is the package used to exchange and import Malody charts: a plain ZIP renamed to `.mcz` that holds one or more [`.mc`](../mc/README.md) chart files plus the audio, background image (and optionally video / keysound files) they reference. The Malody FAQ lists the import formats `.osu`, `.bms/.bme/.bml/.pms`, `.sm`, `.tja`, and `.mc`; the game also opens `.mcz` by drag-and-drop (Windows/Mac) or downloads the files from its chart store. No official specification of the package was found.

## Contents

- A plain ZIP with one or more charts plus the audio, background image and optionally video and keysounds they reference.
- Chart format inside: [`.mc`](../mc/README.md).

## Container & encoding
- ZIP archive (standard deflate/store). Evidence that it is a normal zip: malody2osu simply renames `.mcz` to `.zip` and calls Python `zipfile.ZipFile(...).extractall(...)`; MorePracticeMalodyServer opens a chart pack with .NET `ZipFile.OpenRead` and reads a named `.mc` entry.
- Inside: `.mc` file(s) (JSON, may begin with a UTF-8 BOM, see the mc doc), audio (the `type:1` note's `sound`, typically `.ogg`), background (`meta.background`), optional video (`meta.video`), per-note keysound files. Exact directory layout (flat vs one directory per chart) is Unknown; the samples seen name the files by id/timestamp.
- The Store API (`/api/store/download`) returns, per chart, a list of `{name, hash, file}` items: file name, MD5 and URL; a client downloads these files individually and (as [inference]) can store them as a package. The server `sid`/`cid` identify song/chart; chart `.mc` `meta.id` / `meta.song.id` carry the same ids.

## Structure / metadata
No package-level manifest known. Metadata is read from each `.mc` (`meta.song.title`, `artist`, `id`, `mode`, `version`, ...), see [mc](../mc/README.md). MorePractice's server additionally reads non-standard `meta.song.file` and `meta.song.bpm` fields from a server-side `.mc` (class `SongMeta`), which are not present in the downloaded sample `.mc` files in this repo.

## Timing model
Not applicable (see mc).

## Notes
Not applicable (see mc).

## Audio & images
Referenced by file name from the `.mc` inside the same archive; the audio entry is the `type:1` note with `sound`, `vol`, `offset`.

## Versions & variants
Unknown. `.mcz` is a rename of `.zip`; malody2osu accepts both `.mcz` and `.zip`.

## Quirks & pitfalls
- Entry names may contain non-ASCII characters; the archive may hold several difficulties (several `.mc`) for one song, or charts of different modes.
- A reader must skip the BOM of the `.mc` entry (the MorePractice server cuts 3 bytes).

## Example
Not applicable (binary archive). Extract with any unzip tool after renaming to `.zip`.

## ROX support
Not read by ROX (no archive support in `src/formats/`; ROX reads the extracted `.mc` only). Other file kinds: Malody has no other chart extension besides `.mc`/`.mcz` in the sources consulted; skins, plugins (Lua), `.msp` demo (Mugzone/Documents `Demo/tuturial.msp`) are non-chart files.

## Parsers & tools
- malody2osu (Python, unzips `.mcz`): https://github.com/Jakads/malody2osu
- MorePracticeMalodyServer (C#): https://github.com/RhythmCodec/MorePracticeMalodyServer
- Malody Store API (download items): https://github.com/Mugzone/Malody_Store_API

## Getting samples

- **Committed** in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): two audio-less packages built here with Python `zipfile`: `built-quaver-api-malody-audioless.mcz` (3 Key charts, MPL-2.0 sources) and `built-mc2tja-taiko-audioless.mcz` (2 Taiko charts, MIT sources). Their flat layout is an [inference]: no real `.mcz` could be downloaded.
- **Manifest**: none.
- **How to get more**: Malody's in-game store downloads and its editor's export write `.mcz`; malody2osu accepts dragged `.mcz`/`.zip` files and renames them to `.zip` (see Parsers & tools); the community also shares `.mcz` on the Malody forum and Discord [inference, not checked]. Since an `.mcz` is a ZIP, unzip it to see the real layout.

## Sources
- https://fileinfo.com/extension/mcz
- https://github.com/Jakads/malody2osu (convert.py)
- https://github.com/RhythmCodec/MorePracticeMalodyServer (Model/FileModel/McFile.cs)
- https://github.com/Mugzone/Malody_Store_API
- https://m.mugzone.net/page/175
