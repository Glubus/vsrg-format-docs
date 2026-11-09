# DDR S+ song container (`.gen`)
Kind: package

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (little-endian, partly Blowfish-encrypted)

## Overview

`.gen` is the **single-file song package of Dance Dance Revolution S+ on iOS** (App Store title; Konami). One file bundles the full-song MP3, a preview MP3, the banner texture (PVR), the **step data in [SSQ format](../ssq/README.md)** and the song information. Songs were purchased in-app and downloaded as `.gen`. Almost nothing about it is documented beyond the notes of SaxxonPike's `rhythm-game-formats` repository (`ios/gen.md`), which says "Not much is known about this format internally." This page restates those notes; everything not in that source is "Unknown".

## Contents

- Full-song MP3, preview MP3, banner texture, step data and song information.
- Chart format inside: [SSQ](../ssq/README.md).

## Container & encoding

- Little-endian 32-bit integers in the header.
- **Download wrapper**: when downloaded from the store, a hashing algorithm is used (likely a checksum for verification) "and then the first 8 bytes of the file are stripped. The file is then a valid `.gen` file." So a raw download has 8 extra leading bytes before the header. (Quoted/paraphrased from `gen.md`.)
- **Encryption**: "Almost all sections are encrypted using a Blowfish implementation. They all start with the characters `b"KDEI"`." The format description given is *after* decryption; "it is likely these 4 bytes must be removed prior to beginning decryption". The key/IV/mode and the exact block layout are **not documented** in the source: Unknown.
- The game decrypts lazily: e.g. the MP3 is not decrypted until playback starts.
- The song-information section is **not encrypted**.

## Structure / metadata

### Header (0x40 bytes at offset 0)

A table of 8-byte entries `{ uint32 absolute_file_offset; uint32 size }`. The notes say the header "starts at `0x00` and ends `0x3F`, leaving room for 7 file offsets and sizes", but the offset list and the C struct both show **eight** pairs (0x00..0x3F is 64 bytes = 8 pairs). Section roles:

| Header offset | Section | Content |
|---|---|---|
| `0x00` | song | MP3 of the full song |
| `0x08` | preview | MP3 preview |
| `0x10` | banner | PVR texture, "optimised for use with the game engine", stored upside-down and mirrored horizontally: rotate 180 degrees and mirror to correct. The exact PVR pixel format is not known (QuickPVR can read it; "there are many choices"). |
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

Usually three fields of at most **70 characters**: title (at +0), alternate title (possibly romaji; +73), artist (+143). Each field starts with a **3-byte big-endian length** (e.g. `00 00 0e` = 15) followed by the UTF-8 string, zero-padded. The stored length counts characters, not bytes (the example *ＴЁЯＲＡ* has length 5 but 13 UTF-8 bytes), so the safe approach is to read until `\0` with a limit of 70 (the notes recommend this when the 3-byte length is implausible, > 70).

## Timing model

Inside the embedded SSQ (tempo chunk with ticks per second and measure-tick offsets, see [`../ssq`](../ssq/README.md)). Nothing `.gen`-specific.

## Notes

Inside the embedded SSQ: step rows with panel bitmasks, freeze arrows, shock arrows (see [`../ssq`](../ssq/README.md)). What the S+ engine does with them is not documented in the source.

## Audio & images

Full MP3 and preview MP3 (section 0x00 and 0x08, both Blowfish-encrypted), banner PVR (0x10).

## Versions & variants

Only the SaxxonPike notes exist; no revision history. Related iOS Konami formats described in the same repository (`ios/jbt-rb-orb.md`) belong to jubeat plus / REFLEC BEAT plus / ORB and are not charts of a column game.

## Quirks & pitfalls

- Leading 8-byte checksum prefix on freshly downloaded files.
- Sections start with the ASCII tag `KDEI` that is probably not part of the Blowfish ciphertext.
- The count of header pairs is stated as 7 but is 8 in the offsets/struct.
- The length field in the info strings is a character count, not a byte count.
- Banner texture is flipped.

## Example

Not available: no sample files are known to be public and the content is encrypted. The structure above is the whole public knowledge.

## ROX support

Not read by ROX. A reader would need the (unpublished here) Blowfish key to reach the SSQ, then an SSQ decoder (which ROX also lacks).

## Parsers & tools

None found. DDR-oriented SSQ tools: [`skogaby/ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (Rust, SSQ <-> SSC; does **not** read `.gen`), [`sbruder/brd`](https://github.com/sbruder/brd) (Rust, SSQ -> osu!mania).

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/gen.md
- http://www.flashflashrevolution.com/vbz/showthread.php?t=118010 (thread titled "Is anyone familiar with the .SSQ file format? (DDR iPhone)", seen only as a search-result title; not read)
