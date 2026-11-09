# SNG song package (`.sng`)
Kind: package

Doc status: complete · ROX: decode only · Category: vsrg · Encoding: binary

## Overview
`.sng` is a generic, unencrypted-but-masked binary container created by mdsitton (Clone Hero developer; MIT license) that packs a whole song folder (chart, audio, images, video) plus a metadata key/value table into a single file. It is read by Clone Hero and YARG, and tools like Chart-Packer, Nautilus, Onyx; YARG's own `.yargsong` is a related single-file package (see [yargsong](../../yarg/yargsong/README.md)). The chart inside is a `notes.chart` or `notes.mid`, see those docs.

## Contents

- A whole song folder (chart, audio, images, video) plus a metadata table, in one masked container.
- Chart formats inside: [`.chart`](../chart/README.md) or [`.mid`](../mid/README.md).

## Container & encoding
Binary, **little-endian**. No compression (offsets stay valid so audio can be streamed via memory mapping); file bytes are XOR-masked. Strings are UTF-8 without NUL. Layout: header, then three sections each prefixed with a `uint64 sectionLength` (bytes after that field): Metadata, FileIndex, FileData.

## Structure / metadata
| Block | Field | Type | Size | Meaning |
| --- | --- | --- | --- | --- |
| Header | fileIdentifier | bytes | 6 | `SNGPKG` (`53 4E 47 50 4B 47`) |
| Header | version | uint32 | 4 | format version |
| Header | xorMask | byte[] | 16 | random mask bytes |
| Metadata | metadataLen | uint64 | 8 | bytes after this field |
| Metadata | metadataCount | uint64 | 8 | number of pairs |
| MetadataPair | keyLen | int32 | 4 | |
| MetadataPair | key | utf-8 | keyLen | |
| MetadataPair | valueLen | int32 | 4 | |
| MetadataPair | value | utf-8 | valueLen | |
| FileIndex | fileMetaLen | uint64 | 8 | |
| FileIndex | fileCount | uint64 | 8 | |
| FileMeta | filenameLen | byte | 1 | |
| FileMeta | filename | utf-8 | filenameLen | relative path in the song folder, `/` separators |
| FileMeta | contentsLen | uint64 | 8 | |
| FileMeta | contentsIndex | uint64 | 8 | absolute offset in the .sng file of this file's bytes |
| FileData | fileDataLen | uint64 | 8 | total length of all file data |
| FileData | fileDataArray | bytes | fileDataLen | concatenated masked files |

Metadata values are strings carrying typed text: `True`/`False` booleans (case sensitive), integers `[+-]digits`, floats `[+-]int.frac`, else string. Keys/values must not contain `;` or newline; keys must not contain `=` (so metadata can be serialized to an INI). The metadata keys are the `song.ini` tags ([ini](../ini/README.md)); `song.ini` itself is not stored.

## Timing model
Not applicable (see the contained chart).

## Notes
Not applicable.

## Audio & images
Registered file names (lowercase): `notes.chart`, `notes.mid`, `song.ini` (reserved, not stored), `album.{png,jpg,jpeg}`, `background.*`, `highway.*`, `video.{mp4,avi,webm,vp8,ogv,mpeg}`, `guitar`, `bass`, `rhythm`, `vocals`, `vocals_1`, `vocals_2`, `drums`, `drums_1..4`, `keys`, `song`, `crowd`, `preview` with audio extensions `{mp3,ogg,opus,wav}`. File names are at most 255 bytes and exclude `<>:"/\|?*`, control characters, `..`, trailing dot/space, and Windows reserved names.

## Versions & variants
Header `version` field: 1 in every file inspected [observed: 6 `.sng` packages downloaded from Chorus Encore on 2026-11-09, not committed; they hold `notes.chart` or `notes.mid`, `album.jpg`, and `.opus` audio stems such as `song.opus`, `guitar.opus`, `drums_1.opus`; SngSerializer.cs also rejects any version other than 1]. YARG's `.yargsong` is a separate extension.

## Quirks & pitfalls
Masking: for each byte `i` of a file, `plain[i] = masked[i] XOR xorMask[i % 16] XOR (i & 0xFF)`. `contentsIndex` is relative to the start of the file, not of FileData.

## Example
Not applicable (binary); the spec gives the masking pseudo-code above.

## ROX support
Read by ROX (`SngPackage`, `rox::formats::clone_hero`; decode only): header (version 1 only), metadata pairs (the `song.ini` tags), file index and the masked file data (`SngPackage::read` unmasks an entry); lengths and offsets are checked against the bytes that remain, a file name that is absolute, holds `..`, `\`, a control character or one of `<>:"|?*` is an error. The chart is `notes.chart` (`notes.mid` is not read); the audio plan gives one event per stem entry with `file` = the `.sng` name and `index` = the entry number.

## Parsers & tools
- SngFileFormat reference tool SngCli (C#): https://github.com/mdsitton/SngFileFormat
- parse-sng (TypeScript): https://github.com/Geomitron/parse-sng
- LUA-SNG-Parser: https://github.com/GwyrddGlas/LUA-SNG-Parser
- Chart-Packer: https://github.com/jcub1011/Chart-Packer

## Getting samples
Container only: **no `.sng` file is committed** (the repository keeps chart files only). The charts that live inside `.sng` packages are committed as `notes.chart` / `notes.mid` in [chart](../chart/samples/SOURCES.md) and [mid](../mid/samples/SOURCES.md) (rows marked "extracted from ... .sng"), and the metadata pairs correspond to the [`song.ini`](../ini/README.md) tags. To get real packages: Chorus Encore serves them directly (`https://files.enchor.us/<md5>.sng`, found via `POST https://api.enchor.us/search`), or build one with `SngCli encode` (https://github.com/mdsitton/SngFileFormat); `SngCli decode` extracts them. The format is documented byte by byte in the Container & encoding / Structure sections above.

## Sources
https://github.com/mdsitton/SngFileFormat (README: specification, registry)
