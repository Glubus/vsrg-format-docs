# O2Jam note file (`.ojn`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: binary (little-endian)

## Overview
OJN is the chart file of O2Jam (O2Media). One file holds the metadata of a song, three charts (Easy "EX", Normal "NX", Hard "HX"), and the cover images. Official files are named `o2ma<songid>.ojn` (official ids start at 100; the tutorial is `Tutorial.ojn`) and are paired with an `.ojm` of the same base name that carries all samples ([ojm](../ojm/README.md)). Readers: Open2Jam, O2Mania, Raindrop, CXO2, o2tools, render-ojn, O2Lazer. The existing wiki page this README extends is kept in [docs/format-spec.html](docs/format-spec.html) (File Formats Wiki "O2Jam note files": stub; its note section is "unknown" and its header layout is partly wrong, see Quirks). This page is built from the Open2Jam `OJNParser.java`, the Open2Jam documentation posts, Raindrop `NoteLoaderOJN.cpp`, CXO2 docs, and the 10 sample files in [samples/](samples/README.md) (header fields and block walks verified against them).

## Container & encoding
- Little-endian. Strings are fixed-size, NUL-padded byte arrays; charset is the distributing client's (e-Games: ASCII, Korean mgame/NOWCOM: EUC-KR/CP949). Sample `o2ma2906.ojn` has CP949 artist/noter bytes (e.g. `b1 fa ba c1 ...`).
- File = 300-byte header, then three note sections back to back (easy, normal, hard), then the cover section (JPEG, then BMP thumbnail).
- One file = three difficulties. Section extents come from `note_offset[]`; the end of the hard section is `cover_offset`. A difficulty may be empty (offset equal to the next one, `package_count` = 0).
- Encrypted variant (late O2Jam NX and later): see Versions.

## Structure / metadata
Header, 300 bytes (struct from Open2Jam `OJNParser`; confirmed field by field on the samples):

| Offset | Size | Field | Meaning |
|---|---|---|---|
| 0 | 4 | `songid` int32 | Song id, usually equals the `o2ma<id>` in the filename |
| 4 | 4 | `signature` | `6F 4A 4E 00` = `"ojn\0"` (Open2Jam checks int `0x006E6A6F`) |
| 8 | 4 | `encode_version` float | OJN version, `2.9` (`9A 99 39 40`) in all samples |
| 12 | 4 | `genre` int32 | 0 Ballad, 1 Rock, 2 Dance, 3 Techno, 4 Hip-hop, 5 Soul/R&B, 6 Jazz, 7 Funk, 8 Classical, 9 Traditional, 10 Etc (out of range -> Etc in Open2Jam) |
| 16 | 4 | `bpm` float | Initial BPM; display value, but Raindrop uses it as the BPM at beat 0 when no BPM event sits at 0 |
| 20 | 8 | `level[4]` int16 | Level of Easy, Normal, Hard; 4th slot always 0 |
| 28 | 12 | `event_count[3]` int32 | Events per difficulty (all events: notes, BPM, measure fraction, autoplay) |
| 40 | 12 | `note_count[3]` int32 | Playable notes per difficulty (wiki calls the previous field "total with BGM" and this "playable") |
| 52 | 12 | `measure_count[3]` int32 | Measures per difficulty |
| 64 | 12 | `package_count[3]` int32 | Number of packages (blocks) per difficulty |
| 76 | 2 | `old_encode_version` int16 | Legacy; 0 or 29 (=2.9*10) in samples |
| 78 | 2 | `old_songid` int16 | Legacy; 0 or equals the song id in samples |
| 80 | 20 | `old_genre` char[20] | Legacy string genre; samples show mostly zero bytes, sometimes a trailing `01` |
| 100 | 4 | `bmp_size` int32 | Size in bytes of the BMP thumbnail after the JPEG cover (observed matches the BMP file-size field) |
| 104 | 4 | `file_version` int32 | Chart revision; 0 in all samples (Open2Jam: "old_file_version"/"Version of the chart") |
| 108 | 64 | `title` | Title |
| 172 | 32 | `artist` | Artist |
| 204 | 32 | `noter` | Note charter |
| 236 | 32 | `ojm_file` | Name of the sample OJM (Open2Jam resolves it next to the OJN) |
| 268 | 4 | `cover_size` int32 | JPEG size; 0 when no cover (e.g. `o2ma2906`) |
| 272 | 12 | `time[3]` int32 | Duration in seconds per difficulty (display metadata; render-ojn reports it can under-report the real chart length) |
| 284 | 12 | `note_offset[3]` int32 | Absolute file offsets of the Easy, Normal, Hard sections; the first is always 300 |
| 296 | 4 | `cover_offset` int32 | Offset of the cover section = end of the hard section |

Offset 300 = first note byte. The wiki table gives different offsets after byte 76 (title at 82 of 58 bytes, artist at 140 of 64, etc.): it does not match Open2Jam/Raindrop nor the samples (title read at 108 gives e.g. `[SHD]Milk Chocolate` in `o2ma2420.ojn`).

Sample check (`o2ma2420.ojn`, my script): songid 2420, genre 2, bpm 124.0, levels 9/16/33, note_count 960/1693/2191, measures 89, packages 599/726/629, note_offset 300/104164/226532, cover_offset 362256, cover_size 74352, JPEG `ffd8ffe0` at cover_offset, `BM` header right after it. Walking blocks from each `note_offset` consumed exactly up to the next offset in all 3 difficulties of the 4 files tested.

## Timing model
Beat/measure based, like BMS.
- A section is a list of **packages**. Each package is a 8-byte header followed by `events` 4-byte slots:

```
struct package_header { int32 measure; int16 channel; int16 events; }
```

- `measure` is the 0-based measure index; `events` is the subdivision of that measure for this package. Event `i` of `n` sits at fractional position `i/n` of the measure. Slots with value 0 are padding (that is why files contain many empty slots: they hold the grid). Packages for one (measure, channel) are normally unique; Raindrop notes measures may be out of order, events within one (measure, channel) are in order.
- Channels and 4-byte slot meaning:

| channel | meaning | slot |
|---|---|---|
| 0 | measure fraction | float32; the measure's length is this value x a normal 4-beat measure (0.75 = 3 beats). Rare (Open2Jam doc: "Phase 1", Easy, measure 42). Value 0 ignored. |
| 1 | BPM change | float32 new BPM at that position; value 0 ignored |
| 2..8 | note, lanes 1..7 (lane 4 = middle) | note_event, see Notes |
| 9 and above (9~22 documented; sample `o2ma2968` HX contains channel 29) | autoplay samples (BGM) | note_event; Open2Jam maps every channel >= 9 to AUTO_PLAY, Raindrop likewise |

- Converting to time: beat length of measure m = 4 x fraction(m) (default fraction 1). Position inside the measure: Open2Jam EventList uses position `i/n` of the measure; Raindrop computes `beat = beats_before(measure) + (i/n) * 4` ("fractional measures don't compress the notes inside": position is in beats of a full 4-beat measure; the following measure starts after the shortened length [inference: Raindrop applies the length only to `BeatForMeasure`]). Then integrate the BPM changes (beat 0 uses the header `bpm` if no BPM event is at 0; duplicate consecutive BPMs may be skipped). time = sum(beats * 60/bpm). Cell/measure "halving" in the official NoteTool is the measure-fraction channel (comments in the Open2Jam doc).

## Notes
note_event slot (4 bytes, channels 2..8 and autoplay >= 9):

| Byte | Field | Meaning |
|---|---|---|
| 0-1 | `value` int16 | 0 = empty slot (ignored); otherwise 1-based sample reference into the OJM |
| 2 | `volume_pan` | high nibble = volume (1..15, 0 = max/16), low nibble = pan (1..7 left->center, 0 or 8 = center, 9..15 right) |
| 3 | `note_type` | see below |

- `note_type` (Open2Jam `OJNParser`): `type % 4`: 0 = normal note, 1 = unused (NoteTool shows "#W Normal"), 2 = long note start, 3 = long note end. If `type % 8 > 3` (i.e. values 4..7 as bit 2) the sample is an OGG-section/BGM-type sample: `value` is shifted by 1000 after the 1-based fix (`ref = value - 1 (+1000)`). The Open2Jam note-section post: "4 indicates an OGG sample".
- Sample index convention: OJM wav/key samples have ids 0..999 and OGG samples 1000+ (see [ojm](../ojm/README.md)); `value - 1` (+1000 if bit 2) is that id.
- Long notes: a type-2 event in a lane starts a hold, the next type-3 event in the same lane ends it; the end event is the release (its own sample id is mostly the same as the head's; Raindrop uses the head's sound). In Open2Jam autoplay long notes are converted to normal.
- Simultaneous notes: different lanes at the same position; 7 lanes, no mines. Autoplay channels hold unplayed BGM samples; for Easy files these are used a lot (Open2Jam doc).
- Malformed holds exist in official files (tap inside a hold, start inside a hold, end without a start). Open2Jam's `fixEventList` has two policies: "O2Jam" (tap inside hold, double start -> moved to autoplay; stray end -> removed, as the original game does) and "OPEN2JAM" (look ahead/behind to repair). Raindrop `FixOJNEvents` does the same as the O2Jam policy.
- Counting: `note_count` in the header = playable notes; `event_count` also includes autoplay and non-zero events.

## Audio & images
- Audio: all sounds live in the OJM named by `ojm_file` ([ojm](../ojm/README.md)); there is no background track in the OJN. Songs are played by triggering samples.
- Cover section at `cover_offset`: JPEG of `cover_size` bytes, then a BMP thumbnail of `bmp_size` bytes (Open2Jam: "8x8 thumbnail" [sample: `BM` header with the file size = bmp_size]). Sample `o2ma2420.ojn` has 72934 bytes after the JPEG while bmp_size is 19254: extra trailing data exists (Unknown).
- No video.

## Versions & variants
- `encode_version` 2.9 in all officially distributed files seen; Open2Jam: "usually 2.9". `old_*` fields are leftovers of earlier versions.
- **Encrypted OJN** (late O2Jam NX onward, per CXO2): header `"new"` (3 bytes), then `xor_key_block_size` (byte 3), primary key (byte 4), middle key (byte 5), initial key (byte 6). Build key[block_size] filled with primary, key[0] = initial, key[block_size/2] = middle. Payload = bytes after the header, read **in reverse order from the end of the file**, XORed in chunks of block_size against the key. The CXO2 doc says a 7-byte header; its C++ (`O2JamChartLoader::Decrypt`) skips 8 bytes and reads backwards from `totalSize-1` down to index 8: use the code as reference. The result is a normal OJN.
- O2Jam China/new songs: Open2Jam notes (2011) that O2China OJM used another encryption (blowfish suspected there).
- KrazyRain (a related game) uses a different chart format, `.xnt`, see [xnt](../xnt/README.md).
- Version/language specific string encodings (ASCII vs EUC-KR) differ by distribution.

## Quirks & pitfalls
- Do not rely on `time`/`bpm` header fields for the real song (display data).
- Event slots with value 0 must be skipped but still count toward the subdivision.
- Section end: use `note_offset[]` (or consume exactly `package_count` packages). Never assume easy end = normal start (they are equal only because sections are contiguous; empty sections have equal offsets).
- A header can carry the same chart for all three difficulties: in sample `o2ma2906.ojn` levels are 159/159/159, note_count/event_count/measure/package counts are identical (1941 packages each) and the three sections have about equal size (note_offset 300 / 503904 / 1007508); no cover (`cover_size` 0, `cover_offset` = file size). A difficulty can also be empty (equal consecutive offsets).
- Channel numbers outside 0..22 occur (29 in `o2ma2968`) and are autoplay.
- Malformed long notes; BPM 0 events; measure fraction events.
- The wiki's header offsets (title at 82 etc.) are wrong for real files.
- CP949 strings; `ByteHelper.toString` in Open2Jam cuts at NUL.
- Note value shifted by 1000 when bit 2 of the type is set.

## Example
Illustrative, from the real sample `samples/o2ma2420.ojn` (Easy section start, decoded by my script): 

```
off 300: measure=0 channel=9 events=192  (autoplay, all 192 slots 0 in the first slots)
off ..:  measure=2 channel=3 events=32   (lane 2)
off ..:  measure=2 channel=8 events=32   first slot = 02 00 00 00 -> sample ref 2 (id 1), volume/pan byte 0, type 0 (normal)
```

## ROX support
Read by ROX since Prism's addition of `rox::formats::o2jam` (decode only: ROX does not write OJN). `OjnDecoder` gives a 7-column chart per playable difficulty (`variants`, `decode_variant`; an empty difficulty is not a variant), `decode_with_audio_plan` gives the sounds of every note and every autoplay event as events on the `.ojm` of the header. Not handled: the encrypted `new` OJN (an error), the cover images, the pan nibble, the fields this page marks unknown. Source: `rhythm-open-exchange/src/formats/o2jam/` (decisions in its `mod.rs`, tests in `tests.rs`, built in memory). Checked on the ten samples of this folder: the number of events on the note lanes equals the header `note_count` for the 30 charts, and an independent re-implementation of the Open2Jam/Raindrop timing model gives the same notes and sound times.

## Parsers & tools
- Open2Jam parsers (Java): https://github.com/open2jamorg/open2jam/blob/master/parsers/src/org/open2jam/parsers/OJNParser.java
- Raindrop (C++): https://github.com/zardoru/raindrop/blob/master/src/NoteLoaderOJN.cpp
- CXO2 (C++ client, incl. encrypted OJN): https://github.com/SirusDoma/CXO2
- o2tools (Python): https://github.com/SweepSweep2/o2tools ; render-ojn (Node): https://github.com/djzmo/render-ojn ; O2Lazer (osu!lazer ruleset): https://github.com/sumiyuki727/O2Lazer ; Fadreus/Open2Jam `tools/ojn_header.pl`; SirusDoma/O2MusicList; o2jam-workshop-center; OJN Database https://ojn-database.kenzync.dev/

## Sources
- https://open2jam.wordpress.com/the-ojn-documentation/
- https://open2jam.wordpress.com/2010/10/05/the-notes-section/
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/OJNParser.java , OJNChart.java, EventList.java
- https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderOJN.cpp
- https://github.com/SirusDoma/CXO2/blob/develop/docs/file-format/FileFormat.md
- https://fileformats.fandom.com/wiki/O2Jam_note_files (local: docs/format-spec.html)
- local sample files in samples/ (read only)
