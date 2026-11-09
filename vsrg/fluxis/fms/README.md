# fluXis mapset package (`.fms`)
Kind: package

Doc status: partial · ROX: no · Category: vsrg · Encoding: archive (ZIP)

## Overview

`.fms` is the **distribution/import package of a fluXis mapset**: a ZIP archive containing one or more [`.fsc`](../fsc/README.md) difficulty files plus everything they reference (audio, background, cover, video, [`.ffx`](../ffx/README.md) effects, `.fsb` storyboards, custom hitsounds). `.fms` is the only extension the native importer (`FluXisImport.FileExtensions`) accepts and the one the desktop app registers as a file association (`FileExtensionHelper.cs`, Android intent filter on `.*\.fms`). The other importers (osu!, Quaver, StepMania) convert external maps into a temporary folder and then call `CreatePackage` to build an `.fms` that is fed to the same importer. Skins use a separate `.fsk` ZIP. The format is defined only by code.

## Contents

- One or more `.fsc` difficulties plus everything they reference (audio, background, video, hit sounds).
- Chart format inside: [`.fsc`](../fsc/README.md). Effects: [`.ffx`](../ffx/README.md).

## Container & encoding

- ZIP archive (`System.IO.Compression.ZipFile`); entries are extracted as-is, with `\` replaced by the OS path separator, to a per-set folder.
- File naming on export: `"{Title} - {Artist} [{Mapper}].fms"` (`MapStore.cs`); converters name it after the source file.
- No manifest or index: the set is defined by the `.fsc` files found in the archive (every entry ending in `.fsc` is a difficulty).
- Hash per difficulty = hash of the `.fsc` entry (`GetHash(entry)`), audio hash = xxHash of the audio entry referenced by `AudioFile`.

## Structure / metadata

| Entry | Role |
|---|---|
| `*.fsc` | One map (difficulty) each; metadata (`title`, `artist`, `mapper`, `difficulty`, `tags`...) is read from inside. |
| audio file | `AudioFile` of each `.fsc` (can differ per difficulty). |
| `BackgroundFile`, `CoverFile`, `VideoFile` | Images/video referenced by name. |
| `*.ffx` | Effects (`EffectFile`). |
| `*.fsb` | Storyboard (`StoryboardFile`). |
| hitsound samples | Named from `hitsound` fields of objects. |

On import the importer, for every `.fsc`: parses it, computes length (max of `time` (+ `holdtime`)), key count (`ceil(maxLane / (split ? 2 : 1))`, raised to the largest lane-switch `count` of its `.ffx`), min/max BPM, extracts an accent colour from the background if the map has none, and looks the hash up on the online API to attach the online set/map id, rating, status, dates. A set whose online id is already installed is imported as an **update** of the existing set (files moved over the old ones).

## Timing model

Not applicable (container).

## Notes

Not applicable.

## Audio & images

All assets are plain entries named by the `.fsc` fields.

## Versions & variants

- `.fms` (maps), `.fsk` (skins). The same extension is used for packages created by other-game importers (map status `>= 100` means "from a different game": online lookup is skipped).
- No known version field.

## Quirks & pitfalls

- Every `.fsc` is parsed during import; one broken difficulty fails the whole set.
- Paths with `\` from Windows-made archives are normalised on extraction; absolute/`..` entries are not specially handled in the shown code (`ExtractToFile` to the computed path). [inference: security-relevant for third-party readers]

## Example

No sample in the repo. Illustrative archive listing, hand-built from the importer logic:

```
Example - Artist [Mapper].fms (ZIP)
  4k-easy.fsc
  4k-hard.fsc
  audio.mp3
  bg.jpg
  cover.jpg
  effects.ffx
```

## ROX support

Not read by ROX (ZIP of fluXis maps; ROX has no fluXis reader).

## Parsers & tools

fluXis (C#): [`FluXisImport.cs`](https://github.com/InventiveRhythm/fluXis/blob/master/fluXis/Import/FluXisImport.cs), [`MapImporter.cs`](https://github.com/InventiveRhythm/fluXis/blob/master/fluXis/Import/MapImporter.cs) (`CreatePackage`), converters `fluXis.Import.osu`, `fluXis.Import.Quaver`, `fluXis.Import.Stepmania`.

## Getting samples

- **Committed**: none (no `.fms` is published in the fluXis repository, and a real `.fms` contains the audio and cover of the map, which cannot be redistributed; an audio-less rebuilt zip would need a real `.fsc`, which could not be obtained either, see [`fsc`](../fsc/#getting-samples)).
- **How to get a real one**: download a mapset from the fluXis map list (https://fluxis.flux.moe) or export it from the game (export name `"{Title} - {Artist} [{Mapper}].fms"` in `MapStore.cs`); the file is a ZIP (open with any unzip tool, entries listed in the Structure section above). Converters of the repo (osu!, Quaver) also create `.fms` packages from other games' maps (`MapImporter.CreatePackage`). Online availability without a login was not tested.

## Sources

- https://github.com/InventiveRhythm/fluXis (commit `4187865461e9bf7d1b8201843b0a522229f87699`): `fluXis/Import/FluXisImport.cs`, `fluXis/Import/MapImporter.cs`, `fluXis/Import/ImportManager.cs`, `fluXis/Map/MapStore.cs`, `fluXis.Desktop/FileExtensionHelper.cs`, `fluXis.Android/MainActivity.cs`
