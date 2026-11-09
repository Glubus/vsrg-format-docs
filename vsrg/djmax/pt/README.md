# DJMAX pattern (`.pt`, "PTFF")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian), often encrypted

## Overview
`.pt` files hold the note pattern of DJMAX Online (PC, 2006) and DJMAX Technika (arcade; versions 0.6 and 1.0 found in DJMAX Technika Q too). The header magic is `PTFF`, tracks use the `EZTR` magic: this is the same chunk family as the EZ2DJ [EZFF `.ez`](../../ez2/ez/README.md) format (a shared lineage is an [inference]; the common `EZTR` track magic is the evidence). Parsers: DJMax-Editor (C#, hsreina; reused by techmania-converter), DMTQ-Tools (C#, samnyan / CHN-WolF), PTfluffy (Python, DJMax Online only). A `.pt` holds one chart; keysound names are in the file's own sound table. Metadata (title, composer, level) is not in the file for DJMAX Online (PTfluffy: stored separately in a database).

## Container & encoding
Little-endian (except the 2-byte version field). 0x18-byte header, sound table, tracks. The header is never encrypted; the rest may be (DMTQ-Tools: "If the remaining data is encrypted, decrypt it before reading the sound table and tracks"). Encryption schemes found:
- DJMAX Technika 1 (China): per the CHN-WolF crack write-up, PTFF files are encrypted with MT19937 (`init_by_array` seeded with the six header dwords) combined with a feedback derived from an XTEA variant (8-byte blocks; `plain = cipher ^ fk ^ mt_block`; `fk_0` = header 24-byte sum/CRC32; `fk_{j+1}` = XTEA-variant(fk_j, plaintext block twice)). Decrypting yields a resource bundle ("version u32 + wav entries") in that write-up: i.e. the layout below may not apply to that client [unclear]. TPK packages use AES-128 (state byte order non-standard).
- DJMAX Technika Q: DMTQ-Tools reads plaintext and encrypted input offline (the decrypt algorithm is inside the tool; not reproduced).
- DJMAX Online: `.pt` files extracted from `.pak` archives; PTfluffy parses them directly (it says nothing about encryption); MPGH forum thread says "pt files are encrypted" (unverified).

## Structure / metadata
Header (decrypted layout, DMTQ-Tools `pt-format.md`, 0x18 bytes, same in versions 0.6/1.0):

| Offset | Type | Field |
|---|---|---|
| 0x00 | char[4] | `PTFF` |
| 0x04 | 2 bytes | version: `00 06` = 0.6, `01 00` = 1.0 (not little-endian) |
| 0x06 | u16 | ticks per measure (DJMax-Editor calls it `tickPerMinute`; naming conflict between the two sources) |
| 0x08 | f32 | initial BPM |
| 0x0C | u16 | number of tracks |
| 0x0E | u32 | total ticks / end position |
| 0x12 | f32 | play time in seconds |
| 0x16 | u16 | number of sounds |

Sound table at 0x18, `count` entries: v0.6 entry 0x42 bytes `{u8 index; u8 flag; char name[64]}`; v1.0 entry 0x44 bytes `{u16 index; u8 flag; u8 reserved; char name[64]}`. Indices are ids referenced by notes (v1.0: 0..1023; DJMax-Editor aborts above 1000), not row numbers. Name = OGG file name.

Track = header + events. Header v0.6 78 bytes (0x4E), v1.0 80 bytes (0x50): `char[4] "EZTR"`, `u16 reserved`, `char name[64]`, `u32 end tick @0x46`, `u32 event bytes @0x4A`, v1.0 only `u16 reserved @0x4E`. Event count = bytes / event size.

Event: v0.6 11 bytes `{u32 tick; u8 type; 6 params}`; v1.0 16 bytes `{u32 tick; u8 type; 3 reserved; 8 params}`.

| type | params v0.6 | params v1.0 |
|---|---|---|
| 1 Note | `u8 sound; u8 vol (0-127); u8 pan (0-127); u8 attribute; u16 duration` (duration ticks, 6 for a short note) | `u16 sound; u8 vol; u8 pan; u8 attribute; u16 duration; u8 reserved` |
| 2 Volume | `u8 volume` + 5 reserved | `u8 volume` + 7 reserved |
| 3 BPM | `f32 bpm` + 2 reserved | `f32 bpm` + 4 reserved |
| 4 Beat | `u8 beat` + 5 reserved | `u8 beat` + 7 reserved (DJMax-Editor reads a u16) |
| other | unspecified, keep the buffer | same |

## Timing model
Tick-based: positions are ticks; the header gives ticks per measure, initial BPM and the BPM events (type 3); Beat events (type 4) set beats per measure [inference]. Conversion: time = integrate BPM per tick; tick -> beat = tick / (ticks_per_measure / beats_per_measure) [inference: EZFF note at 1/48 beat]. Exact rounding: Unknown.

## Notes
- Note `attribute` (Technika Q `.bytes` list, same lineage: [bytes](../../../others/djmax-technika-q/bytes/README.md)): 0 normal (drag note if length != 6), A repeat, B last repeat, C hold, 5 chain start, 6 chain end, 1 half-speed, 2 double-speed. Whether these match `.pt` of DJMAX Online: Unknown.
- Which track maps to which lane/key: Unknown from the sources read (the CHN-WolF write-up has `lanes.tsv`/`ptmap.tsv` research files; not read). In DMTQ's format the playable tracks are the first three (top/middle/bottom line). PTfluffy outputs 5-key or 7-key BMS (`-5`/`-7`, default 7).
- Long notes: `duration` > 6 ticks [inference by analogy with EZFF's length bias 6].
- Auto-play/BGM notes live in non-lane tracks [inference from EZFF].

## Audio & images
Sound table names OGG files stored in the game archive (`.pak` for DJMAX Online, `.fpk` for Technika Q); PTfluffy refers to YoMax for unpacking `.pak`.

## Versions & variants
0.6 and 1.0 as above. DJMAX Online, DJMAX Technika 1..3, Technika Tune/Q (Q additionally has `.bytes` charts). DJMAX Portable/Trilogy are explicitly not supported by PTfluffy (different formats; Unknown).

## Quirks & pitfalls
Version bytes in a different order from other fields; header unencrypted, body encrypted; sound index width differs; event size 11 vs 16; beat param width disagreement.

## Example
Not provided (no sample file available; encrypted in retail).

## ROX support
Not read by ROX.

## Parsers & tools
- DJMax-Editor (C#, Apache-2.0): https://github.com/hsreina/DJMax-Editor (`DJMaxEditor/Files/pt/PTOpenFile.cs`)
- DMTQ-Tools: https://github.com/CHN-WolF/DMTQ-Tools (pt_to_text, `pt-format.md`); upstream https://github.com/samnyan/DMTQ-Tools
- techmania-converter: https://github.com/techmania-team/techmania-converter
- PTfluffy (Python, DJMAX Online, GPLv3): https://sites.google.com/site/twisteroidambassador/ptff
- DJMAX Technika 1 CN crack notes: https://github.com/CHN-WolF/DJMax_Technika_1_CN_Ver_Crack

## Sources
- https://raw.githubusercontent.com/CHN-WolF/DMTQ-Tools/master/pt-format.md
- https://raw.githubusercontent.com/hsreina/DJMax-Editor/master/DJMaxEditor/Files/pt/PTOpenFile.cs
- https://sites.google.com/site/twisteroidambassador/ptff
- https://github.com/CHN-WolF/DJMax_Technika_1_CN_Ver_Crack (README section 6.2)
- https://github.com/kangalio/vsrg-format-docs (upstream of this repo)
