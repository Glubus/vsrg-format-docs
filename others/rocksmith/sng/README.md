# Rocksmith 2014 SNG (`.sng`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (encrypted + zlib)

## Overview
The compiled arrangement used by the game, stored under `songs/bin/generic/*.sng` inside the `.psarc` of a Rocksmith 2014 package (not related to Clone Hero's [`.sng`](../../../vsrg/clone-hero/sng/README.md) container, despite the identical extension). The Rocksmith Custom Song Toolkit converts XML to SNG (`sng2014`).

## Packaged in

- Packaged in [`psarc`](../psarc/).

## Container & encoding
Little-endian binary; encrypted with AES-256 in a custom counter mode (each 16-byte block XORed with `AES_ECB(key, IV + i)`, IV embedded at the start of the file) and, after decryption, a 4-byte uncompressed length followed by zlib-compressed data (per the rs2ir-converter README). Keys are platform-specific and not documented here.

## Structure / metadata
The decompressed data is read sequentially through 14 typed sections, including BPM, chords, vocals, sections, arrangements (levels) and metadata (rs2ir-converter). Field layouts: see the CST source `sng2014` in the toolkit; Unknown here.

## Timing model
Unknown.

## Notes
Unknown beyond the above; vocal entries are 60-byte records with timestamps, duration and a null-terminated UTF-8 string (slopsmith excerpt).

## Audio & images
Audio is separate (`.wem` in the package) [inference]; Unknown.

## Versions & variants
Unknown.

## Quirks & pitfalls
Keys and layouts differ per platform (PC/Mac/console) [inference]; Unknown.

## Example
[observed in samples/rocksmith2014net_packed_pc.sng and the other packed files] Packed files start with the bytes `4A 00 00 00 03 00 00 00`; the unpacked data file `samples/rocksmith2014net_unpacked.sng` starts `26 01 00 00 ...` (no such header). See [samples/](samples/).

## ROX support
Not read by ROX.

## Parsers & tools
Rocksmith Custom Song Toolkit (C#): https://github.com/rscustom/rocksmith-custom-song-toolkit · rs2ir-converter (Python): https://github.com/jermn007/rs2ir-converter · slopsmith: https://github.com/byrongamatos/slopsmith

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): six `.sng` test files from Rocksmith2014.NET (MIT): one unpacked, PC and macOS packed variants, packed instrumental / vocals / technique-test arrangements. No decoder was run on them here.
- More: every Rocksmith 2014 `.psarc` holds `songs/bin/generic/*.sng`; unpack it with the Rocksmith Custom Song Toolkit or Rocksmith2014.NET; build `.sng` from `.xml` with the toolkit's `sng2014` CLI (`RocksmithToolkitCLI/sng2014/Program.cs`).

## Sources
https://github.com/jermn007/rs2ir-converter · https://github.com/rscustom/rocksmith-custom-song-toolkit/blob/master/RocksmithToolkitCLI/sng2014/Program.cs · https://deepwiki.com/byrongamatos/slopsmith/2.4-psarc-and-file-format-support
