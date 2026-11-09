# Neversoft Guitar Hero chart data (`songs/<name>.mid.qb`, GH3 / World Tour)
Kind: chart

Doc status: partial (logical layout from a community writer; byte-level details and platform endianness not fully verified) · ROX: no · Category: vsrg (5-lane note highway) · Encoding: binary (Neversoft "QB" node container, usually inside a PAK archive)

## Overview

From Guitar Hero III on, Neversoft's games read a QB file (`songs/<name>.mid.qb`; "QB" is the engine's generic script/data container, also used for song lists and scripts) inside the song's PAK archive (`.pak.xen` / `.pak.ps2` ...) instead of a Standard MIDI chart. It holds named sections: integer arrays for notes per instrument and difficulty, star power / face-off / battle phrases, time signatures, fret bars, markers, plus animation, camera and light-show arrays. Customs are made by compiling a Rock Band/GH2-style `.mid` with Addy's Guitar Hero Toolkit (`midqb_gen`, succeeded by Honeycomb). No public specification exists; this page reconstructs the chart arrays and container from the toolkit's writer code (`midqb_gen/midqb_functions.py`, `midqb_classes.py`, `pak_extract/Text2QB.py`), i.e. what the toolkit generates and the games accept.

## Container & encoding

- QB item stream. File name convention `songs/<name>.mid.qb`; the file-name string's CRC is stored in each item.
- Writer `create_qb(..., endian="big", console="PC", game="GH3")` (Text2QB.py): `endian` is a parameter, default "big". The code consulted does not say which platform uses which byte order (the item type constants differ per platform, see below): Unknown.
- File header (GH3/GHWT): `u32 0`, `u32 total_size` (= `28 + size of item bytes`), then a fixed 20-byte block `1C 08 02 04 10 04 08 0C 0C 08 02 04 14 02 04 0C 10 10 0C 00` (28 bytes total); items follow. For other games the header is `1C 00 00 00 00 00 00 00 <u32 item bytes length> 00*8`.
- Item (section): `u32 node type` (platform specific constant, e.g. SectionArray = `0x00200C00` on Wii/PC/Xbox and `0x000C0400` on Xbox XBX/PS2/PC WPC; SectionStruct `0x00200A00`/`0x000A0400`), `u32 CRC of the item id` (the name hashed as a QB key; a name starting with `0x` is taken as a literal hash), `u32 CRC of the file name`, then either the value inline (simple types) or `u32 pointer` to the data (absolute file offset) + `u32 next` (always 0).
- Array data: `u32 array node type` (e.g. ArrayInteger `0x00010100`, ArrayArray `0x00010C00`, ArrayStruct `0x00010A00`; Xbox XBX/PS2/PC WPC use `0x00010100`, `0x000C0100`, `0x000A0100`), `u32 item count`, `u32 pointer to list start` (omitted when count is 1), the items. Arrays of arrays/structs store a pointer table followed by the sub-arrays/structs. Struct data starts with a StructHeader node type and a first-item pointer; each struct item has a type, an id CRC, a value or pointer, and a next pointer.
- CRC hashing function: see `CRC.py` (`QBKey`) in the toolkit.

## Structure / metadata

Section names for song `<S>` (from `create_gh3_sections`), where `<I>` is the instrument key (`""` for lead guitar, else `rhythm`, `guitarcoop`, `rhythmcoop`) and `<D>` is `easy`, `medium`, `hard` or `expert`:

| Section name | Type | Content |
|---|---|---|
| `<S>_song_<D>` (guitar) / `<S>_song_<I>_<D>` | ArrayInteger | Playable notes, three integers per note: time, length, gem bitmask |
| `<S>_<D>_Star` / `<S>_<I>_<D>_Star` | ArrayArray | Star power phrases `[time, length, note count]` |
| `<S>_<D>_StarBattleMode` / ... | ArrayArray | Battle-mode star phrases (same shape) |
| `<S>_FaceOffP1`, `<S>_FaceOffP2` | ArrayArray | Face-off sections `[time, length]` |
| `<S>_BossBattleP1`, `<S>_BossBattleP2` | Array | Boss battle sections (written empty) |
| `<S>_timesig` | ArrayArray | `[time, numerator, denominator]` |
| `<S>_fretbars` | ArrayInteger | Times of beat lines |
| `<S>_markers` | ArrayStruct | Structs `{ time, marker = w"<text>" }` (section names) |
| animation/camera/light/crowd/drums/performance arrays | various | `*_anim`, `*_triggers`, `*_cameras`, `*_lightshow`, `*_crowd`, `*_drums`, `*_performance`, `*_scripts` and their `_notes` variants ([time, note, length]) |

World Tour style adds drums/vocals/keys sections such as `<S>_song_drums_expertplus`, `song_vocals`, `vocals_phrases`, `lyrics`.

### Note record (GH3)

`[time, length, mask]` with time and length in milliseconds (integers; the toolkit converts MIDI ticks through the tempo map to seconds then x1000). `mask` is a bit set (toolkit class `Note`): green `1`, red `2`, yellow `4`, blue `8`, orange `16`, force `32`, tap `64` (`colours` dict / `binForm`). A chord = several bits in one note. Lengths below a threshold (240 MIDI ticks in `Note.setLength`) are normalised to 1 ms ("default length of 1 ms to make note appear, but no sustain yet"). The World Tour path uses a different one-note-per-colour encoding (`note_bit_vals` 0..6 including open "purple" and a "2x" flag), not covered here.

## Timing model

Absolute times in milliseconds (not ticks), so the game needs no tempo map for note timing. `fretbars` gives the beat grid and `timesig` the signatures (times presumably also in ms [inference]). The toolkit's MIDI input uses 480 ticks/quarter and computes seconds via the MIDI tempo map. The compiler resolves HOPOs: it marks a note HOPO/strum with the `force` bit, based on a ticks threshold (default 170, same as Harmonix), the previous note and the force-on/off markers. The game's own HOPO check is `1/(4*x)` in beats with `x` a per-song setting (the toolkit docs: default 2.95; 2.8235 equals HMX's 170 ticks).

## Notes

Taps/chords, sustains (length > 1 ms), forced HOPOs (bit 32), tap notes (bit 64); star power/face-off/battle phrases are separate arrays. No open notes in GH3 (World Tour has them).

## Audio & images

Not in the chart QB (audio and venue assets are other PAK files).

## Versions & variants

GH3 (also GH: Aerosmith / Legends of Rock style, per the toolkit's `gha_*` camera tables), World Tour / Warriors of Rock (different note encoding, extra arrays, GH5-style performance arrays). Platforms: PC, Xbox 360, PS2, PS3, Wii (separate node type constants in `qbNodeHeaders`). The same container holds songlists and scripts.

## Quirks & pitfalls

- Absolute file offsets: any edit shifts them; writers must recompute.
- Platform-dependent constants and endianness: the same chart compiles to different bytes.
- Section names are hashed: a reader sees CRCs and needs a name dictionary.
- MIDI -> QB is lossy (animation, HOPO resolution, 1 ms lengths).

## Example

Illustrative, hand-built from the note-record rules above: two notes in `<S>_song_expert` (a Green+Yellow chord at 5000 ms lasting 480 ms, then a Red strum at 5500 ms):

```
5000, 480, 5      # 1 (green) + 4 (yellow)
5500, 1,   2      # 2 (red); length 1 = no sustain
```

## ROX support

Not read by ROX (no Neversoft reader; Clone Hero is planned).

## Parsers & tools

- Addy's Guitar Hero Toolkit (Python, archived; continued in C# as Honeycomb / GH-Toolkit-NET): https://github.com/AddyMills/Addys-Guitar-Hero-Toolkit (`midqb_gen/`, `pak_extract/Text2QB.py` and QB2Text), https://github.com/AddyMills/Honeycomb-GUI, https://github.com/AddyMills/Honeycomb-CLI, https://github.com/AddyMills/GH-Toolkit-NET
- Authoring guides: https://www.addymills.com/authoring-world-tour-style-songs/, https://www.addymills.com/compiling-guitar-hero-world-tour-style-songs/

## Getting samples

Committed: none. No real `.mid.qb` could be obtained: QB charts live inside the PAK archives of GH3 / World Tour (commercial). Checked 2026-11-09: AddyMills/Addys-Guitar-Hero-Toolkit, ZedekThePlagueDoctor/Guitar-Hero-III-Tools, donnaken15/FastGH3, nsneverhax/guitar-hero-3-deluxe, leanolin2023/GH3-Custom-Songs (no `.qb`/`.mid`/`.chart` fixtures); web searches (no direct download); Internet Archive GH3 customs (PS2 `.ISO`, e.g. `guitar-hero-3-sum-41/GH3C.ISO` with data inside `DATAP.WAD`/`DATAP.HED`, no loose `.qb`; or PC `qb.pab.xen`/`qb.pak.xen` containers, `qb.pab` item).

How to get one: compile a Rock Band/GH2-style `.mid` with Addy's Guitar Hero Toolkit (`midqb_gen/`, https://github.com/AddyMills/Addys-Guitar-Hero-Toolkit) or Honeycomb / GH-Toolkit-NET, following https://www.addymills.com/authoring-world-tour-style-songs/ and https://www.addymills.com/compiling-guitar-hero-world-tour-style-songs/. The Rock-Bots GH3 bot page says its `UnPak.exe` "Extracts Mid.Qb and Qb files from the pak.xen file in the DATA\SONGS directory" (requires `DATA\PAK\dbg.pak.xen`): real files come from the PAK of a game you own. GH3 custom songs ship as `.pak.xen` (a container).

## Sources

- https://github.com/AddyMills/Addys-Guitar-Hero-Toolkit (commit `4ec8f7139720c2b59c21b70925fd90cdb1508b1b`): `midqb_gen/midqb_definitions.py` (`qbNodeHeaders`, `difficulties`, ...), `midqb_gen/midqb_classes.py` (`Note`, `QBItem`), `midqb_gen/midqb_functions.py` (`create_gh3_sections`, `parse_gh3_qb`), `pak_extract/Text2QB.py` (`create_qb`, `bin_array_data`, `bin_struct_data`), `README.md`
- Search result page for the toolkit (RhythmVerse credits, project description)
