# DJMAX Technika Q song (`.bytes`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (little-endian)

## Overview

Chart format of DJMAX Technika Q (mobile), one file per pattern. Documented from `bytes-format.md` of DMTQ-Tools, derived from https://github.com/oliverchang/technika_q/blob/master/format.md ("the track format has changed from that, this is the latest format"). DMTQ-Tools `bytes_to_text` and `pt_to_text` convert between `.bytes`, text and `.pt`.

## Container & encoding
Binary. Layout is "header, sounds, tracks, song info at the end".

## Structure / metadata
- Header: 4 bytes unknown (zeros), 4 bytes offset to song information.
- Song info (usually at file end): u16 number of sounds, u16 tracks(?), u16 positions per measure(?), f32 initial BPM (can be 0 if a BPM command exists), u32 end position, u32 unknown (maybe float, "Tag B"), u32 end position, u32 total command count(?) (may be 0; excludes track starts, includes BPM changes).
- Sound table at offset 8: entries of 0x43 bytes: `u16 index; u8 unknown; char name[0x40]`.
- Tracks (usually 64): track header = 2 zero bytes + 0x3B bytes name (names are not meaningful, empty in later patterns), followed by commands of 0xD bytes: `u32 position; u8 type; 8 bytes params`.

## Timing model

Positions count in units of positions per measure; 4/4 assumed.

## Notes

Playable tracks for the 3 lines are the first three tracks (0 top, 1 middle, 2 bottom). Command types: 0 start of track (params: note count shifted, note count); 1 note (u16 sound index, u8 volume, u8 pan, u8 attribute, u8 length (long note, unit = one position; 6 = short), 2 unknown bytes); 2 volume (1 byte); 3 BPM change (f32 + 4 unknown); 4 unknown. Note attributes: 0 normal (drag note if length != 6), A repeat, B last repeat, C hold, 5 chain start (notes in between have type 0), 6 chain end, 1 half-speed, 2 double-speed, 100 video start, 150 keysound on/off (the game then plays `xxxx.a.ogg` from `song.fpk`).

## Audio & images

Audio in `song.fpk` (DMTQ-Tools `fpk_tool` packs/unpacks); videos `.webm`.

## Versions & variants

PT 1.0 / 0.6 in the same toolset (see [pt](../../../vsrg/djmax/pt/README.md)).

## Quirks & pitfalls

Many fields are unknown; song info sits at the file end.

## Example

Unknown.

## ROX support
Not read by ROX.

## Parsers & tools
DMTQ-Tools https://github.com/CHN-WolF/DMTQ-Tools ; upstream https://github.com/samnyan/DMTQ-Tools ; technika_q https://github.com/oliverchang/technika_q

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (pattern files from the private-server archive https://github.com/UrsulaProject/DMTQResearch, `DMTQ-server/dmtq/dmqglb.mb.pmang.com/DMQ/Patterns/<patternId>`, 2,634 files in the repo; headers match this page: zero word, offset to song info, 64 tracks, 192 positions per measure).

More: take files from the same `Patterns/` folder. `SongList.json` in that repo maps song and pattern ids; `_EARPHONE` suffix = earphone-mode pattern. samnyan/DMTQ-Localserver reads `Patterns.zip` with the same naming (pattern id); DMTQ-Tools (`bytes_to_text`) converts files to text.

## Sources
- https://raw.githubusercontent.com/CHN-WolF/DMTQ-Tools/master/bytes-format.md
