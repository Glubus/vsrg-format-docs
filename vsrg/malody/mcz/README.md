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
- Inside: `.mc` file(s) (JSON, may begin with a UTF-8 BOM, see the mc doc), audio (the `type:1` note's `sound`, typically `.ogg`), background (`meta.background`), optional video (`meta.video`), per-note keysound files. Directory layout: Malody Chart Forge's exports put everything in a folder `0/` (`0/<tier>--<difficulty>.mc`, `0/audio.ogg`, `0/background.png|jpg`) [observed in samples/forge-demo_toy-vwp.noaudio.mcz]; the PayToUse zips use a `<name>/` folder (one has a nested `<name>/<name>/`) [observed in samples/malody-custom-charts_bee.noaudio.mcz upstream listing]; other layouts may exist.
- The Store API (`/api/store/download`) returns, per chart, a list of `{name, hash, file}` items: file name, MD5 and URL; a client downloads these files individually and (as [inference]) can store them as a package. The server `sid`/`cid` identify song/chart; chart `.mc` `meta.id` / `meta.song.id` carry the same ids.

## Structure / metadata
No package-level manifest known [observed in the original forge-demo toy-vwp package, extracted to ../mc/samples/forge-demo_toy-vwp/: members `0/<tier>--<difficulty>.mc`, `0/audio.ogg`, `0/background.jpg`].

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

- **No archive is stored in this repository.** Real packages (5 Malody Chart Forge demo exports, 3 zips of PayToUse/malody-custom-charts) were downloaded and their `.mc` extracted: [`../mc/samples/`](../mc/samples/) (`forge-demo_*/` and `malody-custom-charts_*.mc`); provenance in the `Extracted from archives` section of its `SOURCES.md`. Observed layouts: Chart Forge puts `0/<tier>--<difficulty>.mc`, `0/audio.ogg`, `0/background.png|jpg` in a folder `0/`; the PayToUse zips use `<name>/` (one nested `<name>/<name>/`).
- The Malody store needs a login (`cgi/chart/download` answers `{"code":-1000}`), so no store package was fetched.
- **How to get more**: Malody's in-game store and its editor's export write `.mcz`; malody2osu accepts dragged `.mcz`/`.zip`. Unzip to see the real layout and keep only the `.mc`.


## Sources
- https://fileinfo.com/extension/mcz
- https://github.com/Jakads/malody2osu (convert.py)
- https://github.com/RhythmCodec/MorePracticeMalodyServer (Model/FileModel/McFile.cs)
- https://github.com/Mugzone/Malody_Store_API
- https://m.mugzone.net/page/175
