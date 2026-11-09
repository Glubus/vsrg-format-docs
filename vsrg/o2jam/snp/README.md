# KrazyRain package (`.snp`, "VDISK1.0")
Kind: package

Doc status: partial · ROX: no · Category: vsrg · Encoding: archive (binary, zlib-compressed members)

## Overview
KrazyRain (a Korean game from the same family of 7-key games as O2Jam) ships songs in `.snp` archives. Each archive holds `.xnt` charts, `.xne` XML files and OGG samples. Open2Jam can read them (`SNPParser.java`), with the chart metadata (title, artist, level) coming from an external XML database `KrazyRainDB` that Open2Jam bundles (not in the archive). Details come only from Open2Jam's parser.

## Contents

- KrazyRain archive with `.xnt` charts, `.xne` XML files and OGG samples.
- Chart format inside: [`.xnt`](../xnt/README.md).

## Container & encoding
Little-endian. Signature: the first 8 bytes read as long `0x302E314B53494456` = ASCII `"VDISK1.0"`. 24-byte file header (the 16 bytes after the signature: Unknown), followed by consecutive entries until end of file.

Entry = 145-byte header + `size_packed` bytes:

| Offset | Size | Field |
|---|---|---|
| 0 | 1 | `isDir` (entries with isDir >= 1 are directories and skipped) |
| 1 | 128 | file name (NUL-terminated, trimmed) |
| 129 | 4 | `size_original` int32 |
| 133 | 4 | `size_packed` int32 |
| 137 | 8 | not read by Open2Jam (Unknown) |

Payload (`size_packed` bytes) is a zlib stream (java `Inflater`); extraction = inflate. Next entry at `pointer + 145 + size_packed`.

## Structure / metadata
Names are paths inside the archive, extension-indexed: `.xnt` (chart, see [xnt](../xnt/README.md)), `.xne` (XML with a `tempo="..."` attribute: Open2Jam takes the real BPM from the first `tempo="` value, "the xml bpm isn't it"), `.ogg` samples referenced by the XNT sample table. Open2Jam creates one chart per `.xnt`; if the XML DB has no entry it falls back to title = archive name, artist "KrazyRain", genre Unknown, level 1, XNE name = XNT name with `.xne`.

## Timing model / Notes / Audio & images
See [xnt](../xnt/README.md). Samples are OGG files in the archive (decompressed with the same zlib step).

## Versions & variants
Unknown beyond the "1.0" signature.

## Quirks & pitfalls
Unused 8 bytes of the entry header; the metadata is outside the archive; files with `size_packed` 0 are skipped.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
Open2Jam SNPParser (Java): https://github.com/open2jamorg/open2jam/blob/master/parsers/src/org/open2jam/parsers/SNPParser.java ; Raindrop's NoteLoaderOJN.cpp is the other link in the original README (it only loads OJN, not SNP: verified by reading it).

## Sources
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/SNPParser.java , utils/Compressor.java
- https://github.com/SirusDoma/open2jam-modern (confirms SNPParser = "KrazyRain archive format (VDISK)")
