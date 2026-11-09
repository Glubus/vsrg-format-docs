# DDR S+ song container (`.gen`)
Kind: package

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (little-endian, partly Blowfish-encrypted)

## Overview

`.gen` is the single-file song package of Dance Dance Revolution S+ on iOS (Konami), bought in-app. It bundles the full-song MP3, a preview MP3, the banner texture (PVR), the step data in [SSQ format](../ssq/README.md) and the song information. The only documentation is SaxxonPike's `rhythm-game-formats` (`ios/gen.md`: "Not much is known about this format internally."); this page restates it.

## Contents

Full-song MP3, preview MP3, banner texture, [SSQ](../ssq/README.md) step data, song information.

## Container & encoding

- Little-endian 32-bit integers in the header.
- Download wrapper: a store download is hashed (likely a checksum) "and then the first 8 bytes of the file are stripped. The file is then a valid `.gen` file." (`gen.md`) A raw download has 8 extra leading bytes before the header.
- Encryption: "Almost all sections are encrypted using a Blowfish implementation. They all start with the characters `b"KDEI"`." The format description is for the decrypted data; "it is likely these 4 bytes must be removed prior to beginning decryption". Key, IV, mode and block layout: Unknown.
- The game decrypts lazily (the MP3 is not decrypted until playback starts).
- The song-information section is not encrypted.

## Structure / metadata

### Header (0x40 bytes at offset 0)

A table of 8-byte entries `{ uint32 absolute_file_offset; uint32 size }`. The notes say the header "starts at `0x00` and ends `0x3F`, leaving room for 7 file offsets and sizes", but the offset list and the C struct show eight pairs (0x00..0x3F is 64 bytes = 8 pairs). Section roles:

| Header offset | Section | Content |
|---|---|---|
| `0x00` | song | MP3 of the full song |
| `0x08` | preview | MP3 preview |
| `0x10` | banner | PVR texture, "optimised for use with the game engine", stored upside-down and mirrored horizontally: rotate 180 degrees and mirror to correct. The exact PVR pixel format is unknown (QuickPVR can read it; "there are many choices"). |
| `0x18` | steps | **SSQ** chart data, "with a chunk type 0x09 at the end storing metadata" |
| `0x20` | unknown | |
| `0x28` | song info | title/artist strings (below), not encrypted |
| `0x30` | unknown | small (e.g. 0x24 = 36 bytes) |
| `0x38` | unknown | same idea as `0x30` |

```c
struct gen_hdr {
    uint32_t song_offset;          uint32_t song_size;
    uint32_t song_preview_offset;  uint32_t song_preview_size;
    uint32_t unk_texture1_offset;  uint32_t unk_texture1_size;   // banner
    uint32_t ssq_offset;           uint32_t ssq_size;
    uint32_t unk1_offset;          uint32_t unk1_size;
    uint32_t song_info_offset;     uint32_t song_info_size;
    uint32_t unk2_offset;          uint32_t unk2_size;
    uint32_t unk3_offset;          uint32_t unk3_size;
};
```

### Song information section

Usually three fields of at most 70 characters: title (at +0), alternate title (possibly romaji; +73), artist (+143). Each field starts with a 3-byte big-endian length (e.g. `00 00 0e` = 15) followed by the UTF-8 string, zero-padded. The length counts characters, not bytes (the example *ＴЁЯＲＡ* has length 5 but 13 UTF-8 bytes). The notes recommend reading until `\0` with a limit of 70 when the 3-byte length is implausible (> 70).

## Timing model

In the embedded SSQ ([`../ssq`](../ssq/README.md)). Nothing `.gen`-specific.

## Notes

In the embedded SSQ: panel-bitmask rows, freeze and shock arrows ([`../ssq`](../ssq/README.md)).

## Audio & images

Full MP3 and preview MP3 (sections 0x00 and 0x08, both Blowfish-encrypted), banner PVR (0x10).

## Versions & variants

Only the SaxxonPike notes exist. `ios/jbt-rb-orb.md` in the same repository covers jubeat plus / REFLEC BEAT plus / ORB, not column-game charts.

## Quirks & pitfalls

- Leading 8-byte checksum prefix on freshly downloaded files.
- Sections start with the ASCII tag `KDEI`, probably not part of the Blowfish ciphertext.
- The header pair count is stated as 7 but is 8 in the offsets/struct.
- The info-string length field is a character count, not a byte count.
- The banner texture is flipped.

## Example

None: no public samples and the content is encrypted.

## ROX support

Not read by ROX. It would need the (unpublished) Blowfish key, then an SSQ decoder, which ROX also lacks.

## Parsers & tools

None found. DDR-oriented SSQ tools: [`skogaby/ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (Rust, SSQ <-> SSC; does not read `.gen`), [`sbruder/brd`](https://github.com/sbruder/brd) (Rust, SSQ -> osu!mania).

## Getting samples

No `.gen` committed: each file embeds the full-song and preview MP3 (encrypted audio) and the chart cannot be separated without the undocumented key. Public copies: the iOS app `DanceDanceRevolution S Lite (US) (v2.1.2) [Decrypted].ipa` (archive.org item `ios-ipa-com.konami.ddrslite`) bundles `A_Brighter_Day.gen` 2,116,742 bytes, `DYNAMITE_RAVE.gen` 1,844,158, `TRUE_LOVE_Club_Mix.gen` 1,931,926 in `Payload/DDRSPlusUS.app/` (read 2026-11-09; `DYNAMITE_RAVE.gen` header observed: first word `0x40`, offsets table, then `KDEI` Blowfish blocks). Unzip `Payload/DDRSPlusUS.app/*.gen` (or buy songs in-app) and unpack with [`brd`](https://github.com/sbruder/brd) or [`ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (neither ships fixtures); compare the embedded SSQ with [`../ssq`](../ssq/samples/SOURCES.md).

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/gen.md
- http://www.flashflashrevolution.com/vbz/showthread.php?t=118010 (thread titled "Is anyone familiar with the .SSQ file format? (DDR iPhone)", seen only as a search-result title; not read)
