# ArcCreate package / project (`.arcpkg`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive

## Overview

`.arcpkg` is the package format of **ArcCreate** (community Arcaea editor/player by Arcthesia). It is a zip archive that bundles one or more Arcaea charts with audio, jacket, background and a project description so that charts can be shared and played by ArcCreate (desktop editor, Android/iOS player). Details come from ArcCreate's export code and the EtoileResurrection README; nothing else was read.

## Contents

- A ZIP bundling one or more Arcaea charts with audio, jacket, background and a project description.
- Chart format inside: Arcaea chart; see [`.aff`](../aff/README.md) [inference].

## Container & encoding

Zip archive. The exporter writes an `index.yml` at the root listing import entries (`directory`, `identifier` as `publisher.package`, `settingsFile`, `version`, `type` = `level`), then the project folder with `*.arcproj` (YAML) and the files referenced by its charts (chart `.aff`, audio, jacket, background, video, hitsound waveforms).

## Structure / metadata

`.arcproj` (YAML, camelCase keys; from ArcCreate's `ProjectSettings` / `ChartSettings` classes): top-level `lastOpenedChartPath`, `charts` (list), `editorSettings` (stripped on export). Each chart: `chartPath`, `audioPath`, `jacketPath`, `baseBpm`, `bpmText`, `syncBaseBpm`, `backgroundPath`, `videoPath`, `title`, `composer`, `charter`, `alias`, `illustrator`, `difficulty`, `chartConstant`, `difficultyColor`, `skin`, `colors`, `lastWorkingTiming`, `previewStart`, `previewEnd`, `searchTags`.

## Timing model

Inside the contained `.aff` (see `../aff/`). `previewStart`/`previewEnd` are timing values (presumably ms) [inference].

## Notes

Not applicable.

## Audio & images

Referenced by `audioPath`, `jacketPath`, `backgroundPath`, `videoPath` relative to the project.

## Versions & variants

`index.yml` entry `version` int per package; EtoileResurrection converts between `.arcpkg` and the official Arcaea layout (songlist/packlist + `.aff` files) with commands `pack`, `export`, `combine`, `convert`.

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

ArcCreate (C#): <https://github.com/Arcthesia/ArcCreate> (`Compose/Project/Export/Exporter.cs`, `Data/ProjectSettings.cs`, `Data/ChartSettings.cs`, `Storage/ImportInformation.cs`); EtoileResurrection (archived): <https://github.com/freeze-dolphin/EtoileResurrection>; Etoile.Lite is the successor named in its README.

## Sources

- <https://github.com/Arcthesia/ArcCreate>
- <https://github.com/freeze-dolphin/EtoileResurrection>
