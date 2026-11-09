# Sound Space Plus map (`.sspm`)
Kind: package

Doc status: complete · ROX: no · Category: others · Encoding: binary

## Overview
`.sspm` is the map package of Sound Space Plus and its successor Rhythia. One file holds metadata, the audio (mp3/ogg), an optional PNG cover and the notes of ONE difficulty. Two versions: v1 (SS+ early, newline-terminated strings, notes only) and v2 (pointer table, typed custom data, extensible "marker" system). Specs by the SS+ community (basils-garden/types); readers in SS+ source (`Song.gd`), `pysspm-rhythia`, `sspm-player`. Maps are shared on community sites (e.g. https://sspm.paada.fr) and the Rhythia site.

## Container & encoding
- Binary, **little endian**, integers unsigned unless stated ("all numbers listed are little endian and all integers are unsigned", types index).
- Signature `53 53 2B 6D` ("SS+m"). Version field decides layout.
- Strings: UTF-8; "uint16 length" strings = 2-byte byte-length prefix + bytes (v2); v1 strings are newline-terminated.
- No compression; audio and cover are embedded raw (MP3/OGG; PNG, APNG unsupported).
- One file = one difficulty.

## Structure / metadata
### v1
| Part | Layout |
|---|---|
| Header | 4 B signature, u16 version = 1, 2 B reserved `00 00` |
| Metadata | `map id\n`, `map name\n`, `creator\n` (multiple mappers separated by " & " or ", "), u32 last note ms, u32 note count, u8 difficulty |
| Difficulty | 0 N/A, 1 Easy, 2 Medium, 3 Hard, 4 Logic, 5 Tasukete |
| Cover | u8 type (0 none, 1 no longer used, 2 PNG); if 2: u64 length + PNG bytes |
| Audio | u8 type (0 none, 1 stored); if 1: u64 length + audio bytes |
| Notes | per note: u32 ms; u8 storage (0 integer, 1 quantum); integer: u8 x, u8 y; quantum: f32 x, f32 y |
Positions: x 0 = left column, 1 = center, 2 = right; y 0 = top row, 1 = center, 2 = bottom row.

### v2
Header: 4 B signature, u16 version = 2, 4 B reserved zeros (10 bytes).
Static metadata (start 0x0A):
| Field | Size |
|---|---|
| SHA1 of marker and marker-definition blocks | 20 B |
| ms position of last marker | u32 |
| number of notes | u32 |
| number of markers (incl. notes) | u32 |
| difficulty group | u8 (0 N/A, 1 Easy, 2 Medium, 3 Hard, 4 Logic, 5 Tasukete) |
| map rating | u16 |
| has audio / has cover / requires mod | u8 x 3 (0 or 1) |
Pointers (5 offset/length pairs, each u64 + u64; offset 0 = absent): custom data, audio, cover, marker definitions, markers. SS+ reads the marker block offset at file position 0x70 (the 5th pair's offset), consistent with the pairs starting at 0x30.
Strings: u16-prefixed map ID, map name, song name; u16 mapper count + u16-prefixed mapper names.
Custom data (at its pointer): u16 field count; each: u16-prefixed field id (unique), u8 data type, (if type 0x0C) u8 array element type, value.
Audio block: whole MP3/OGG file. Cover block: whole PNG.
Marker definitions: u8 count; each: u16-prefixed id (notes are `ssp_note`, must be first), u8 value count (incl. arrays), then one type byte per value, then `00` terminator.
Markers: repeated `u32 ms; u8 marker type (index into definitions); data per definition`.
Doc inconsistency: the spec says "audio present flag at byte 0x2E, cover at 0x2F"; counting the fields in order gives audio at 0x2D, cover at 0x2E, requires-mod at 0x2F. Readers (pysspm) use the sequential order [inference]; do not trust the hard-coded offsets.

### Data type ids (custom data + markers)
| Id | Size | Meaning |
|---|---|---|
| 0x00 | n/a | end of definition |
| 0x01 | 1 | signed 8-bit int (pysspm reads signed; spec says "8 bit integer") |
| 0x02 | 2 | u16 |
| 0x03 | 4 | u32 |
| 0x04 | 8 | u64 |
| 0x05 | 4 | f32 |
| 0x06 | 8 | f64 |
| 0x07 | var | position: u8 flag 0 = ints (u8 x, u8 y), 1 = quantum (f32 x, f32 y); stored as two values `[x, y]` |
| 0x08 | var | buffer: u16 length + bytes |
| 0x09 | var | string: u16 length + UTF-8 |
| 0x0A | var | long buffer: u32 length + bytes |
| 0x0B | var | long string: u32 length + UTF-8 |
| 0x0C | var | array: u32 total byte length (excluding itself), u16 count, n values of the element type. Not allowed in markers |

Common custom fields: `difficulty_name` (string; SS+ stores it for non built-in difficulty names). Others Unknown; pysspm uses `ai_generated`, `ai_generator`, `ai_fingerprint` (its own convention). Readers must skip unknown fields.

## Timing model
Absolute milliseconds (u32) from the start of the audio. No BPM, beats, stops or SV. Notes are sorted by time (SS+ sorts after read).

## Notes
Only taps ("hit by hovering"). Position: 3 x 3 grid, integer cells or "quantum" (float, possibly outside 0..2 or negative) notes. Simultaneous notes: same ms, different positions. v2 markers allow other object kinds besides `ssp_note`, whose format is defined by the definition table; only `ssp_note` (one position value) is standard. No holds, mines or keysounds.

## Audio & images
Embedded audio (MP3 or OGG) and PNG cover; flags and pointers say whether present. No preview, background, video fields (video support is an unreleased/unknown extension). Map ID, name, song name are strings; map ID is sanitized by readers (pysspm replaces `,` and invalid characters; SS+ requires lowercase `[0-9a-z_-]`, no leading `_`).

## Versions & variants
- v1 (original SS+). SS+ can convert maps to v1 (`convert_to_sspm_v1`). Rhythia writes v2.
- v2 (current). pysspm reads both and writes v2.
- Newer Rhythia/Phoenyx/Nova formats exist ("Support for Pheonix/Nova Filetype (when I get my hands on the data structure)" in the pysspm roadmap): Unknown.
- SS+ also imports Sound Space `.txt` maps and Vulnus JSON, see [txt](../txt/README.md), [vulnus](../../vulnus/json/README.md).

## Quirks & pitfalls
- Use pointers to seek (audio/cover blocks may be absent); do not read sequentially after metadata.
- Strings in old SS+ files may not be valid UTF-8; pysspm falls back to latin-1.
- `ms` is u32; the "last marker ms" field is not trusted by all readers.
- Notes may not be sorted; mirrored axes: SS+ internally mirrors x/y for some imports (see txt).
- Markers: unknown marker type must still be skipped using the definition table.
- Hash field covers only markers + definitions.

## Example
Illustrative, hand-built from the v1 rules above (bytes in hex, not a real file):
```
53 53 2B 6D | 01 00 | 00 00                        header
"id\n" "name\n" "creator\n"
78 56 34 12 -> last ms | 01 00 00 00 -> 1 note | 03 -> Hard
00 -> no cover | 00 -> no audio
E8 03 00 00 | 00 | 01 | 01   note at 1000 ms, integer, x=1, y=1 (center)
```

## ROX support
Not read by ROX.

## Parsers & tools
- pysspm-rhythia (Python): https://github.com/David-Jed/pysspm-rhythia (v1/v2 read, v2 write)
- sspm-player (C99 + raylib): https://github.com/lolopada/sspm-player
- Sound Space Plus (GDScript): https://github.com/Rhythia/sound-space-plus (`scripts/content/game/Song.gd`)
- Spec: https://github.com/basils-garden/types

## Getting samples

Committed: two hand-built, audio-less synthetic files (v1 and v2) in [`samples/`](samples/). Real maps embed audio (and cover) of third-party songs and carry no licence, so none is committed or listed: the community site named by sspm-player's README, `https://sspm.paada.fr`, did not answer from here, and live map sites are not hashable. How to get more: download `.sspm` from the Rhythia / Sound Space Plus map sites ("Download maps" section of <https://github.com/lolopada/sspm-player>), install Sound Space Plus (itch.io, chedski) and look in its maps folder, or export from the editor SSQE. Old `.txt` maps are documented in [`../txt/`](../txt/README.md).

## Sources
- https://raw.githubusercontent.com/basils-garden/types/main/sspm/v1.md
- https://raw.githubusercontent.com/basils-garden/types/main/sspm/v2.md
- https://basils-garden.github.io/types
- https://raw.githubusercontent.com/David-Jed/pysspm-rhythia/main/pysspm_rhythia/parser.py
- https://raw.githubusercontent.com/David-Jed/pysspm-rhythia/main/README.md
- https://raw.githubusercontent.com/Rhythia/sound-space-plus/HEAD/scripts/content/game/Song.gd
- https://raw.githubusercontent.com/lolopada/sspm-player/main/README.md
