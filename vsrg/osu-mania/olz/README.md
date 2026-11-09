# osu!lazer beatmap archive (`.olz`)
Kind: package

Doc status: partial · ROX: no · Category: vsrg (osu!mania mapsets; like `.osz` it carries difficulties of all four modes) · Encoding: archive (ZIP)

## Overview

`.olz` is the archive that **osu!lazer itself exports** for a beatmap set, as opposed to [`.osz`](../osz/README.md), the stable-compatible package. The lazer source says it directly: `BeatmapExporter` is the "Exporter for beatmap archives. This is not for legacy purposes and works for lazer only", with `FileExtension => ".olz"` and `UseFixedEncoding => false`; the sibling `LegacyBeatmapExporter` ("Exporter for osu!stable legacy beatmap archives. Converts all beatmaps in the set to legacy format and exports it as a legacy package") writes `.osz`. The importer accepts both: `BeatmapImporter.HandledExtensions = { ".osz", ".olz" }` (ppy/osu @ bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2: `osu.Game/Database/BeatmapExporter.cs`, `LegacyBeatmapExporter.cs`, `osu.Game/Beatmaps/BeatmapImporter.cs`).

lazer's `client.realm` database is **not** a chart format: it is a Realm metadata database (`OsuGameBase.CLIENT_DATABASE_FILENAME = "client.realm"`); the files themselves are stored as content-addressed blobs under `files/` (`RealmFileStore`). An `.olz`/`.osz` export re-packs those blobs with their original names.

## Contents

- Same payload as an `.osz`: one or more `.osu` difficulties plus the audio, images, video, storyboard and sample files of the set, all unmodified as lazer stored them (the legacy exporter's `GetFileContents` override re-encodes the `.osu`; the plain exporter does not) [inference from the two classes].
- Chart format inside: [`.osu`](../osu/README.md) (osu!mania Mode 3 among others); storyboards in [`.osb`](../osb/README.md).

## Container & encoding

- A standard ZIP written with SharpCompress `ZipWriter`, deflate (`LegacyArchiveExporter.ExportToStream`). Entries are written with the file names stored in the database, directly at the archive root, one entry per file; duplicate names raise an error.
- **Entry names are UTF-8** (`ArchiveEncoding { Default = Encoding.UTF8 }` when `UseFixedEncoding` is false), whereas `.osz` exports force Shift-JIS (CP932) like osu!stable (`ZipArchiveReader.DEFAULT_ENCODING`).
- [observed in samples/legacy-export-stability-test.olz and decimal-timing-beatmap.olz] the three lazer test archives are ordinary ZIPs with deflated `.osu` entries only; one (`fractional-coordinates.olz`) also carries a macOS `__MACOSX/._*.osu` resource-fork entry, so it was probably repacked on macOS and is not a pure lazer export [inference].

## Structure / metadata

No manifest. Each `.osu` is self-describing. File names inside are free (`Artist - Title (Creator) [Version].osu` by convention).

## Timing model

Not applicable (container); see [`.osu`](../osu/README.md).

## Notes

Not applicable.

## Audio & images

Referenced by name from the `.osu` files, as in `.osz`.

## Versions & variants

- The `.osu` files inside keep lazer's own format version: all three samples start with `osu file format v128` [observed in samples/decimal-timing-beatmap.olz], where stable writes `v14`. The `.osu` doc describes v128 as lazer's version.
- lazer-only data allowed in those files include non-integer times and coordinates [observed in samples/decimal-timing-beatmap.olz: object time `28520.019209251084`; samples/fractional-coordinates.olz: `3.0517578E-05,1.5258789E-05,3120`], which stable cannot parse as integers.

## Quirks & pitfalls

- Not importable by osu!stable [inference from "not for legacy purposes and works for lazer only"]; use `.osz` for interchange.
- A tool that only looks for `.osz` misses these archives; the content is a normal ZIP, so renaming works for unpacking.
- `.osk` is a skin archive, not a chart package, and is out of scope.

## Example

Listing of `legacy-export-stability-test.olz` (946 bytes): one entry, `legacy export - stability test (spaceman_atlas) [].osu` (1080 bytes uncompressed), starting with `osu file format v128`.

## ROX support

Not read by ROX; unzip the archive and read the `.osu` files ([`.osu`](../osu/README.md)).

## Parsers & tools

- osu!lazer (C#): `BeatmapExporter.cs`, `LegacyArchiveExporter.cs`, `BeatmapImporter.cs` (links below).
- Any ZIP library.

## Getting samples

- **Committed** in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): the three `.olz` archives of the ppy/osu test suite (`decimal-timing-beatmap.olz`, `fractional-coordinates.olz`, `legacy-export-stability-test.olz`; MIT; 20 KB total, `.osu` only, no audio).
- **Manifest**: none.
- **How to get more**: install osu!lazer, select a beatmap set and use its export action (the exporter writes `.olz`; the option that exports for stable writes `.osz`) [inference on the UI label; the file extensions are from the source]. The exported file goes to lazer's `exports` folder [inference]. Any mapset you own can be exported this way; audio and images inside must not be redistributed.

## Sources

- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/Database/BeatmapExporter.cs
- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/Database/LegacyBeatmapExporter.cs
- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/Database/LegacyArchiveExporter.cs
- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/Beatmaps/BeatmapImporter.cs
- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/OsuGameBase.cs (`CLIENT_DATABASE_FILENAME`)
- https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game/Database/RealmFileStore.cs
- Repo samples: vsrg/osu-mania/olz/samples/
