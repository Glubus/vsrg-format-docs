# Rocksmith 2014 package (`.psarc`)
Kind: package

Doc status: complete · ROX: no · Category: others · Encoding: archive (binary, zlib blocks, AES-CFB encrypted table of contents)

## Overview
Every Rocksmith 2014 song (official DLC and custom DLC "CDLC") is delivered as a `.psarc`, the archive format of the PlayStation 3 SDK ("PlayStation ARChive"). The package holds the compiled arrangements ([`sng`](../sng/README.md)), per-arrangement JSON manifests, Wwise audio banks and streams (`.bnk`, `.wem`), album art, show lights and engine metadata. Arrangement XML ([`xml`](../xml/README.md)) is not inside the package: authoring tools convert it to `.sng` when building. Package file names end in `_p` (PC) or `_m` (Mac) per the library's platform detection. This page is the container; the layout comes from the open-source Rocksmith2014.NET library (iminashi), which reads and writes PSARCs with an encrypted TOC like the official files.

## Contents

- Compiled arrangements, JSON manifests, Wwise audio, album art and show lights for each song.
- Chart format inside: [`.sng`](../sng/README.md). The XML arrangement is not inside (see [`xml`](../xml/README.md)).

## Container & encoding
- **Big-endian** numbers throughout. Layout: header (32 bytes), table of contents (ToC: entries + block size table), then the data blocks.
- The ToC of Rocksmith packages is **encrypted** (header flag `ArchiveFlags = 4`): AES-256 in CFB mode, block size/feedback 128 bits, IV all zero, zero padding, with the well-known fixed key `C5 3D B2 38 70 A1 A2 F7 1C AE 64 06 1F DD 0E 11 57 30 9D C8 52 04 D4 C5 BF DF 25 09 0D F2 57 2C` (from `Cryptography.fs`). Only the ToC (bytes from offset 32 to `ToCLength`) is encrypted; entry data is not.
- Compression: zlib, in blocks of at most `BlockSizeAlloc` (default 64 KiB). Not every file is compressed: `.wem`, `.sng`, `appid` and `7z` entries are written uncompressed by the library, and readers must test each block (a block starting with a zlib header may still be raw data; the library falls back to raw if inflating fails).

## Structure / metadata
Header:

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | magic `PSAR` |
| 4 | u16 | version major (1) |
| 6 | u16 | version minor (4) |
| 8 | 4 | compression method `zlib` |
| 12 | u32 | `ToCLength`: total length of the ToC including the 32-byte header and the block size table |
| 16 | u32 | ToC entry size (30) |
| 20 | u32 | entry count (includes the manifest entry) |
| 24 | u32 | block size (65536) |
| 28 | u32 | archive flags: 0 plain ToC; 4 encrypted ToC (in this library `IsEncrypted = flags == 4`) |

ToC entry (30 bytes): `NameDigest` 16 bytes (MD5 of the ASCII entry name; 16 zero bytes for the empty name), `ZIndexBegin` u32 (index of the first block in the block size table), `Length` u40 (uncompressed size), `Offset` u40 (byte offset in the file of the first block).

Block size table follows the entries: one value per block, width `zType = log256(blockSize)` (2 bytes for 64 KiB, 3 for up to 16 MiB, 4 for up to 4 GiB). A value `0` means a full raw block of `BlockSizeAlloc` bytes; otherwise it is the stored size of the block (compressed or raw).

The **first entry (index 0) is the manifest**: a text list of entry names, one per line (`\n`), in ToC order; names are matched to the remaining entries by position (`ID - 1`). Names use `/` separators.

Reading algorithm: read the 32-byte header; if flags = 4, decrypt `ToCLength - 32` bytes; read `entryCount` entries; read `(ToCLength - 32 - entryCount*30) / zType` block sizes; inflate entry 0 to get names; for each entry seek to `Offset`, then read blocks `ZIndexBegin`, `ZIndexBegin+1`, ... until `Length` bytes are produced.

## Timing model
Not applicable to the container. Timing lives in the arrangements (`sng` / `xml`): seconds-based note times and beat/phrase tables.

## Notes
Not applicable. The relevant files for charting inside a CDLC package (names from the DLC builder and the CDLC Project code):
- `songs/bin/generic/<key>_<arrangement>.sng` (PC; `songs/bin/macos/...` on Mac): compiled arrangement; `<key>` is the lowercase DLC key.
- `manifests/songs_dlc_<key>/<key>_<arrangement>.json` and `manifests/songs_dlc_<key>/songs_dlc_<key>.hsan`: per-arrangement attribute manifests (song bank name, tuning, difficulty, techniques) and the HSAN index.
- `audio/windows/song_<key>.bnk`, `song_<key>_preview.bnk`, `<id>.wem` (`audio/mac` on Mac): Wwise audio bank and stream.
- `gfxassets/album_art/album_<key>_<size>.dds` (typically sizes 64, 128, 256), `assets/ui/lyrics/<key>/*.dds` (lyrics font for vocals arrangements).
- `appid.appid`, `*.xblock`, `*.aggregategraph.nt`, `flatmodels/...` (engine entries).

## Audio & images
Audio is Audiokinetic Wwise (`.bnk` sound banks + `.wem` Ogg-Vorbis-derived streams); album art is DDS. The two audio banks (song and preview) are referenced by name from the arrangement manifests.

## Versions & variants
- PSARC version 1.4 with zlib is the only variant handled; any other compression method string raises `NotSupportedException`.
- Platform variants handled by the library: PC (`_p`, `windows`, `generic`) and Mac (`_m`, `mac`, `macos`); it converts between them by renaming entries and adjusting the aggregate graph. Console packages are not covered by the sources opened.
- `cache.psarc` and `audio.psarc` of the game are the same container (the latter has `.wem` blocks that look like zlib streams but are raw).

## Quirks & pitfalls
- The compressed/raw status of a block cannot be derived from its first bytes; try inflate and fall back to raw.
- Archives built by the Custom Song Toolkit can contain partially compressed `.sng` files.
- Padding: AES zero padding after the encrypted ToC must be ignored (only `ToCLength - 32` bytes are meaningful).
- Entry names are looked up by MD5 digest in the ToC but listed by the manifest: the manifest must stay in the same order as the ToC.
- The PSARC key is public; encrypted CFB must use the block size 128 for both block and feedback.

## Example
Not a hex dump (no sample was copied). A hand-built description of the first 32 bytes of a Rocksmith 2014 PC package, derived from the header table (illustrative): `50 53 41 52` `00 01` `00 04` `7A 6C 69 62` `<u32 ToCLength>` `00 00 00 1E` `<u32 count>` `00 01 00 00` `00 00 00 04`.

## ROX support
Not read by ROX. Only a container: decoding charts requires extracting the `.sng` and decoding it (string/fret model, not columns).

## Parsers & tools
- Rocksmith2014.NET `Rocksmith2014.PSARC` (F#; read, edit, create, pack directory): https://github.com/iminashi/Rocksmith2014.NET
- Rocksmith Custom Song Toolkit (C#): https://github.com/rscustom/rocksmith-custom-song-toolkit
- slopsmith documentation of PSARC support: https://deepwiki.com/byrongamatos/slopsmith/2.4-psarc-and-file-format-support (referenced by the SNG page)

## Sources
- https://github.com/iminashi/Rocksmith2014.NET (`src/Rocksmith2014.PSARC/{Header,Entry,Cryptography,PSARC,Utils}.fs`, `src/Rocksmith2014.Common/{Platform,Compression}.fs`, `src/Rocksmith2014.DLCProject/*`)
- ../sng/README.md and ../xml/README.md in this repository
