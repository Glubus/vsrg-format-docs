# Virtual Orchestra Studio song (`.vos`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary

Binary song file of HanseulSoft's Virtual Orchestra Studio. The only open parser found is `VosParser.java` of ReVanTis/VosDroid (Android re-implementation, 2014); this page derives from it. No official specification exists.

## Overview

- VOS (1999, HanseulSoft, Korea; freeware) is a 7-key "piano" game: a song is a MIDI arrangement in which some notes are marked as the ones the player performs. Files are tiny (rarely above 100 KB, per the gpbeta introduction). "Mania" (1.4.2+) and VosDroid play the format; a "VOS Creator" tool converts a MIDI to `.vos`.
- The original README lists "`.vos`: Virtual Orchestra Studio and CanMusic chart, including 000, 001, 006, 022 versions". The parser only checks a header value of 3; what "000/001/006/022" refer to is Unknown.

## Container & encoding

- Little-endian 32-bit integers (the VosDroid comments say "Big Endian" but `VosByte.byte2int` uses `ByteOrder.LITTLE_ENDIAN`; the code is what works).
- Text fields are length-prefixed byte strings, code page unspecified (the parser notes a possible GB2312 issue; Korean originals are probably another code page [inference]). Segment names are 16-byte fields.
- One song per file; the file embeds a complete Standard MIDI File as its last segment.

## Structure / metadata

Parsing flow (comments + code of `VosParser.Parse`):

1. `int32` header = `3` (else "not vos file").
2. Segment table: repeated entries of `int32 address` + `16-byte name`, until a name starting with `EOF` or the bytes `B1 E0 D0 B4` (GBK for "编写"). The first segment is the info block (`INF`), the second begins the MIDI data (`Segments[1].addr` is where channel data stops).
3. Info segment (starts right after the table):

| Field | Size | Notes |
| --- | --- | --- |
| title length, title | 1 + n | |
| artist length, artist | 1 + n | |
| comment length, comment | 1 + n | usually 0 |
| author length, author | 1 + n | |
| music type | 1 | 01 Pop, 02 New Age, 03 Techno, 04 Rock, 05 SoundTrack, 06 Game&Anime, 07 Jazz, 08 CenturyEnd, 09 Classical, 0A Other |
| extended music type | 1 | |
| total length | int32 | milliseconds |
| level | 1 | read as `Level` right after the length |
| padding | 1023 | all zero (the parser throws if not) |

4. Channel blocks (until the position reaches `Segments[1].addr`), each:

| Field | Size | Notes |
| --- | --- | --- |
| instrument | int32 | MIDI program number |
| note count | int32 | |
| padding | 14 | zeros ("some versions 12 bytes" says the comment) |
| notes | 13 x count | see below |

The parser then treats channels 0-15 as the 16 MIDI channels and the 17th block (index 16) as the **playable notes** (`Channels.get(16)` becomes `playNote`).
5. MIDI segment: the rest of the file is a Standard MIDI File (parsed with a MIDI library; tempo events are used to convert ticks to milliseconds).

Note record (13 bytes, `VosNote.Parse`):

| Offset | Size | Field |
| --- | --- | --- |
| 0 | int32 | `sequencer` (start position) |
| 4 | int32 | `duration` |
| 8 | 1 | MIDI channel |
| 9 | 1 | pitch |
| 10 | 1 | volume (velocity) |
| 11 | 1 | keyboard key position |
| 12 | 1 | flags |

Flags (comment in the source, not verified): bits 0-3 colour (RGB?), bits 4-6 corresponding key (do, re, mi, fa, so, la, ti), bit 7 set for notes played by the user, "bit 8" set for long notes.

## Timing model

- `sequencer` and `duration` are in an internal unit converted to MIDI ticks by the parser: `tick = ceil(sequencer * resolution / 0x300)` and `durationTicks = ceil(duration * resolution / 0x2E4)` where `resolution` is the MIDI file's ticks-per-quarter (note the two different divisors, 0x300 = 768 and 0x2E4 = 740, exactly as in the code; whether the second is intentional is unknown).
- Tempo comes from the embedded MIDI tempo events (`mpqn`, default 500000 = 120 BPM if none); milliseconds per tick = `mpqn / resolution / 1000`. Note times are looked up in a cumulative tick->ms table.
- No separate BPM/stop fields in the info segment except the total length.

## Notes

- Playable notes = the 17th channel block; `keyboard` selects one of the seven keys; flag bit 8 marks long notes (VosDroid 0.5.1 added long-note support). Everything else is MIDI backing music played automatically.
- Each note is a MIDI note: the original game sends `pitch`/`volume` on `channel` when the key is pressed.

## Audio & images

No external audio: all sound is MIDI (instrument = GM program). No images.

## Versions & variants

Unknown beyond header value 3. [observed: samples/1.vos, 103.vos] The first int32 may be 2: the file then continues with a length-prefixed file name (`Vosctemp.trk`), a size and a tag `VOS022` / `VOS008`, then 16-bit-length-prefixed text fields. [observed: samples/23.vos, 24.vos, 109.vos] With int32 3 the segment table is `inf`/`mid`/`EOF`, followed by a `VOS1` tag in 23/24 and not in 109. Both layouts are read by the MIT parser `src/ChartLoaderVOS.cpp` of https://github.com/rhythmus-emulator/rparser (`ParseMetaDataV2`/`V3`); they probably are the "000/001/006/022 versions" of the original README [inference]. The game's `Album/` folder holds the songs; VOS Creator makes `.vos` from MIDI.

## Quirks & pitfalls

- The reference parser's comments are wrong about endianness.
- The 1023-byte zero padding and 14-byte channel padding are hard checks in that parser and may fail on other versions ("some versions 12 bytes").
- Text encoding is unspecified.
- Total length can be wrong; the MIDI segment is authoritative.

## Example

Header bytes of `samples/1.vos`: `02 00 00 00 0C 00 00 00 "Vosctemp.trk" ... "VOS022"`; of `samples/23.vos`: `03 00 00 00 40 00 00 00 "inf" ... "mid" ... "EOF"`. See [samples/](samples/SOURCES.md); `Canon in D.vos` of VosDroid is a manifest entry.

## ROX support

Not read by ROX, on purpose (2026-11-10): two file layouts (header 2 and 3) and the only two readers disagree on the length of a note (`VosDroid` divides it by 0x2E4, `rparser` scales it with the same 0.156 as the start; the second one flags it as "not correct"); the start unit is 1/768 of a quarter note in both. A reader would have to choose between them with no file the game plays to check against.

## Parsers & tools

- https://github.com/ReVanTis/VosDroid (Java; `VosParser`, `VosNote`, `VosSegment`, `VosByte`)
- VOS Creator (MIDI to VOS converter) and Mania, linked from the gpbeta page.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (version-2 and version-3 files from the MIT-licensed test folder of https://github.com/rhythmus-emulator/rparser, plus `vosdroid_Canon_in_D.vos`, shipped with VosDroid, which has no licence file). Song authorship is unknown.

More: the game is freeware and the song library community made (http://www.gpbeta.com/en/post/intro/vos-intro, "VOS Creator" MIDI-to-VOS tool). Songs sit in the game's `Album/` folder. VosDroid's roadmap lists a vos-to-mid conversion (https://github.com/ReVanTis/VosDroid, README: "D0.3 ... conversion from vos to mid"; SPECIALTHANKS credits vos2midi). `VOS022`/`VOS008` are tags of the v2 container.

## Sources

- https://raw.githubusercontent.com/ReVanTis/VosDroid/master/VosDroidLibrary/src/main/java/com/revantis/vosdroid/lib/VosParser.java (and `VosNote.java`, `VosSegment.java`, `VosByte.java`)
- https://github.com/ReVanTis/VosDroid
- http://www.gpbeta.com/en/post/intro/vos-intro/
- https://github.com/kangalio/vsrg-format-docs (original README)
