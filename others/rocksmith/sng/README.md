# Rocksmith 2014 SNG (`.sng`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (encrypted + zlib)

## Overview

The compiled arrangement the game reads from `songs/bin/generic/*.sng` inside the `.psarc` of a Rocksmith 2014 package (unrelated to Clone Hero's `.sng` container). The Rocksmith Custom Song Toolkit converts XML to SNG (`sng2014`).

## Packaged in

`.psarc` (PlayStation archive, encrypted table of contents: `.sng` arrangements, JSON manifests, Wwise audio, art).

## Container & encoding

Little-endian binary, encrypted with AES-256 in a custom counter mode (each 16-byte block XORed with `AES_ECB(key, IV + i)`, IV at the start of the file); after decryption a 4-byte uncompressed length and zlib data (rs2ir-converter README). Keys are platform-specific.

## Structure / metadata

The decompressed data is read sequentially through 14 typed sections (BPM, chords, vocals, sections, arrangement levels, metadata; rs2ir-converter). Field layouts: see CST `sng2014`. Vocal entries are 60-byte records with timestamps, duration and a null-terminated UTF-8 string (slopsmith excerpt).

## Timing model

Unknown.

## Notes

Unknown.

## Audio & images

Separate `.wem` in the package [inference].

## Versions & variants

Unknown.

## Quirks & pitfalls

Keys and layouts differ per platform (PC/Mac/console) [inference].

## Example

[observed: rocksmith2014net_packed_pc.sng and the other packed files] Packed files start with `4A 00 00 00 03 00 00 00`; the unpacked `rocksmith2014net_unpacked.sng` starts `26 01 00 00 ...`.

## ROX support
Not read by ROX.

## Parsers & tools
Rocksmith Custom Song Toolkit (C#): https://github.com/rscustom/rocksmith-custom-song-toolkit · rs2ir-converter (Python): https://github.com/jermn007/rs2ir-converter · slopsmith: https://github.com/byrongamatos/slopsmith

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md); no decoder was run on them. More: every Rocksmith 2014 `.psarc` holds `songs/bin/generic/*.sng`; unpack with the Rocksmith Custom Song Toolkit or Rocksmith2014.NET; build `.sng` from `.xml` with the toolkit's `sng2014` CLI (`RocksmithToolkitCLI/sng2014/Program.cs`).

## Sources
https://github.com/jermn007/rs2ir-converter · https://github.com/rscustom/rocksmith-custom-song-toolkit/blob/master/RocksmithToolkitCLI/sng2014/Program.cs · https://deepwiki.com/byrongamatos/slopsmith/2.4-psarc-and-file-format-support
