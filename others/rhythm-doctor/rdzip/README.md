# Rhythm Doctor level archive (`.rdzip`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive

## Overview
`.rdzip` is the custom level package of Rhythm Doctor (developer 7th Beat Games per FileInfo). It is a ZIP that wraps an [`.rdlevel`](../rdlevel/README.md) plus its assets (audio, sprites). Created by the in-game editor's export, shared on Rhythm Cafe and Discord.

## Contents

- A ZIP wrapping one level plus its audio and sprites.
- Chart format inside: [`.rdlevel`](../rdlevel/README.md).

## Container & encoding
ZIP archive (RhythmBase treats `.rdzip` and `.zip` as the same archive family: "Archive: `.rdzip` `.zip`"; default read mode `ZipProcessingMode.AllEntries` extracts all entries to a temporary directory and loads the level). Internal layout beyond "contains an `.rdlevel` and its resources" is Unknown from the sources read.

## Structure / metadata
See rdlevel. No archive-level metadata file known.

## Timing model / Notes
Not applicable.

## Audio & images
Resources extracted next to the level file; referenced by name from the rdlevel.

## Versions & variants
Same as rdlevel.

## Quirks & pitfalls
Extract to a temporary directory and clean up (RhythmBase `GlobalSettings.CachePath`, `ClearCache()`).

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
- RhythmBase (C#): `Level.FromFile("x.rdzip")`, `SaveToZip`: https://github.com/RDCN-Community-Developers/RhythmToolkit

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): `rebuilt-internet-overdose-no-audio.rdzip`, an audio-less package BUILT from an AGPL-3.0 level: a zip with only `main.rdlevel` at its root (the level refers to `music.ogg` and two images that are not included).
- Manifest (`samples.manifest.json`): two real `.rdzip` files of HyperHaxStudios/RD-Levels (pinned commit): `HyperHax_-_Corrupted.rdzip` (4.8 MB) and `HyperHax_-_Nowhere_(EDM_Remix).rdzip` (3 MB). [observed by listing them: `main.rdlevel`, one `.ogg` and one cover image (`Album.jpg` / `Album.png`), all at the zip root]
- More: custom levels from the Rhythm Cafe database or the in-game level browser/Steam Workshop [inference]; "Export" in the level editor produces the zip.

## Sources
- https://fileinfo.com/extension/rdzip
- https://raw.githubusercontent.com/RDCN-Community-Developers/RhythmToolkit/master/docs/Tutorial.md
- https://github.com/RDCN-Community-Developers/RhythmToolkit
