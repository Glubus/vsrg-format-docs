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

- Container only: this folder holds no archive. An `.rdzip` is a zip whose root holds `main.rdlevel` plus audio (`.ogg`) and images (observed by listing real archives: `main.rdlevel`, one `.ogg`, a cover image; two-player levels may add a second `.rdlevel`, e.g. `LosingYou 2P.rdlevel`).
- The real `main.rdlevel` files extracted from `.rdzip` levels are committed in [../rdlevel/samples/](../rdlevel/samples/) (each row there names the archive URL it came from).
- More: Rhythm Cafe level database (https://datasette.rhythm.cafe/, JSON API with `rdzip_url`), HyperHaxStudios/RD-Levels.

## Sources
- https://fileinfo.com/extension/rdzip
- https://raw.githubusercontent.com/RDCN-Community-Developers/RhythmToolkit/master/docs/Tutorial.md
- https://github.com/RDCN-Community-Developers/RhythmToolkit
