# Rhythm Master classic chart (`.imd`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: binary (little-endian)

## Overview
IMD is the chart format of Rhythm Master's classic mode (4, 5 or 6 lanes). Files are named `<song>_<4|5|6>k_<ez|nm|hd>.imd` (key count; easy/normal/hard) and sit next to `<song>.mp3` and cover images (self-made chart import rules: song `xxx.mp3`, large image `xxx.png`, small `xxx__hd(ipad).png`, chart `xxx_4(5,6)k_ez(nm,hd).imd` per community guides). Fan charts exist in large numbers (dreamimd.com). One file = one difficulty. The layout below is read from RMEssentials `rmechart.cpp` (`RmeChart::fromImd/toImd`) and RM2Malody `imd_helper.py`, and verified by parsing the real file `keluodiya_4k_hd.imd` (RM2Malody repo) with a short script: header 130273 ms, 417 BPM entries, separator 0x0303, 822 notes, file length = 8 + 12*417 + 6 + 11*822.

## Container & encoding
Little-endian, no compression, no encryption in the classic files (the newer client downloads encrypted charts; not covered).

## Structure / metadata
| Offset | Type | Field |
|---|---|---|
| 0 | u32 | total time in ms |
| 4 | u32 | BPM entry count `n` |
| 8 | n x 12 bytes | `{u32 time_ms; f64 bpm}` |
| 8+12n | u16 | separator `0x0303` (RM2Malody reads it as a "flag"; RMEssentials requires 0x0303) |
| 10+12n | u32 | note count `m` |
| 14+12n | m x 11 bytes | notes |

Total file size is exactly `8 + 12n + 6 + 11m`. No title/artist in the file (they come from the song list XML).

Note record, 11 bytes: `u16 type; u32 time_ms; u8 track; i32 action`.

## Timing model
Milliseconds. BPM entries: official files contain one entry per beat (e.g. 0, 312, 625 ms ... all at 192 BPM in the sample: RMEssentials' writer also generates `floor(totalTime*bpm/60000)+1` entries one beat apart); RMEssentials and RM2Malody only use the first BPM (dynamic BPM is not supported by their converters), so a variable-BPM IMD is treated as constant [inference: not verified whether the game changes tempo]. Note times are absolute ms; the beat grid is only needed for conversion: `tick = round(time_ms * bpm / 1250)` gives 48 ticks per beat (RMEssentials `timestampToTick`).

## Notes
- `track`: 0-based lane index (0..3 for 4k, 0..4, 0..5); RMEssentials maps it to imdjson track `track+3`.
- `type` (RMEssentials' mapping to `{attr, isEnd, timeDur/toTrack}`):

| type | meaning (as in RMEssentials / RM2Malody) | `action` |
|---|---|---|
| 0x00 | tap | 0 |
| 0x01 | single slide (flick) in one note; moves to lane `track + action` | signed lane delta |
| 0x02 | hold (long press), standalone | duration ms |
| 0x21 / 0x22 | slide / hold, "attr 4, not end" (a part of a chain that continues) | delta / duration ms |
| 0x61 / 0x62 | slide / hold, "attr 3, not end" (start of a chain) | delta / duration ms |
| 0xA1 / 0xA2 | slide / hold, "attr 4, end" (end of a chain) | delta / duration ms |

  (bit meanings: 0x20, 0x40 and 0x80 combine start/continuation/end of a hold-and-slide chain; RMEssentials `fromImdNote` only accepts these 9 values and treats others as invalid.) In the real sample, counts were: 0x00 x582, 0x02 x75, 0x21 x59, 0x62 x32, 0xA2 x31, 0x22 x28, 0x01 x14, 0xA1 x1.
- A chain ("worm"/"noodle" in the community) is: start note (0x61/0x62/0x21) -> following notes joined when the next note is at `time + duration` on the (moved) lane (RMEssentials `sortNotes` splices by `toTrack` and `timestamp + timeDur`), ending with `isEnd`.
- Note counting (RMEssentials): a note with duration 0 counts as 1 unless it is a chain start; a note with a duration counts `1 + ticks/12` (combo from hold body).
- Notes within one lane at equal timestamps sorted slide-before-hold ("0x21/0x61 before corresponding 0x22/0xA2").

## Audio & images
`<song>.mp3` (single backing track, no keysounds), cover jpg/png.

## Versions & variants
Classic IMD only; star-motion charts use [mde](../mde/README.md); the JSON dialect is [json](../json/README.md) (imdjson 1.2.1/1.2.2/1.2.3/1.3.0).

## Quirks & pitfalls
Wrong track ids exist (RMEssentials ignores notes outside 3..8 when loading); BPM list can have thousands of entries; chain notes must be kept in order.

## Example
Header of the real `keluodiya_4k_hd.imd` decoded by my script (origin: https://github.com/nladuo/RM2Malody, file read once, not copied):
```
total_ms=130273, bpm_count=417, bpm[0]=(0 ms, 192.0), bpm[1]=(312 ms, 192.0)
separator=0x0303, notes=822
note0: type=0x00 time=3750 track=2 action=0
note2: type=0x02 time=4062 track=1 action=625   (hold 625 ms)
```

## ROX support
Read by ROX since Prism's addition of `rox::formats::imd` (decode only): `ImdDecoder` (`decode`, `decode_with_title`, `decode_with_name`, `decode_with_report` giving an `ImdReport`, `decode_file`; `DetectedFormat::Imd`). ONE chart per file, **4, 5 or 6 columns**: the file does not store the count, the NAME does (`<song>_<4|5|6>k_<ez|nm|hd>.imd`, which also gives the difficulty `Easy`/`Normal`/`Hard` and the title: the part before the suffix), else the highest `track` used plus one (at least 4, at most 6, as RMEssentials' chart viewer does); a note on a track the chart has not is dropped and counted. The file must be exactly `8 + 12n + 6 + 11m` bytes with the separator `0x0303`. Times are the notes' ms (x 1000 µs), the BPM table is read as one timing point per change of BPM (a table of one entry per beat at one tempo is ONE point), the first moved to the first note when it came later. Note types: `0x00` tap; `0x01` single slide = a tap on its lane (target lane lost); `0x02` hold; `0x22`/`0x62`/`0xA2` hold segments of a chain = one hold each on their own lane; `0x21`/`0x61`/`0xA1` slides of a chain = dropped when a segment ends or starts beside them (within 2 ms, a tolerance of the reader: real files round a segment's length by one ms or two), else kept as a tap; any other type is dropped and counted. A hold of length 0 is a tap. The title comes from the file name, `audio_file` is empty (the caller looks for `<song>.mp3`). `looks_like_imd` / `is_imd_chart_file` tell an `.imd` from another program's file (the extension is shared and the format has no signature). Verified locally on the 31 official 4K charts of the RM2Malody repository and the 4K, 5K and 6K fixtures of RMEssentials (no note dropped, no isolated slide, no overlap; the fixtures RMEssentials refuses are refused too), none kept in the repository. Not handled: `.mde`, the `imdjson` dialect, encrypted charts.

## Parsers & tools
- RMEssentials (C++/Qt, AGPL-3.0): https://github.com/Fsu0413/RMEssentials
- RM2Malody (Python): https://github.com/nladuo/RM2Malody ; Malody `imd_2_mc` plugin; imd2mc web tool https://imd2mc.single.eu.org/default/
- rmstZ: https://lrfasd.github.io/rmstZ/ (closed source converter; lists imd read+write)
- RhythmMasterResource (classic-mode chart dump): https://github.com/GirlKiller512/RhythmMasterResource

## Getting samples

- Committed in [`samples/`](samples/): 9 real charts (7 official classic-mode files from GirlKiller512/RhythmMasterResource covering 4k/5k/6k and ez/nm/hd, 2 RMEssentials song fixtures), 5 deliberately invalid RMEssentials files and `synthetic_4k_hd.imd`. Everything is listed with origin, date and sha256 in [`samples/SOURCES.md`](samples/SOURCES.md).
- More: https://github.com/GirlKiller512/RhythmMasterResource holds 4134 `.imd` files (all songs of the classic mode, 3 key counts x 3 difficulties) with `mrock_song_client_android.xml` as song list; https://github.com/nladuo/RM2Malody has more (e.g. `keluodiya_4k_hd.imd`); fan charts at https://www.dreamimd.com; the Malody RM guide https://m.mugzone.net/wiki/2368.

## Sources
- https://raw.githubusercontent.com/Fsu0413/RMEssentials/master/src/librmessentials/src/rmechart.cpp , rmechart.h
- https://raw.githubusercontent.com/nladuo/RM2Malody/master/imd_helper.py
- https://m.mugzone.net/wiki/2368 (Malody RM guide)
- https://lrfasd.github.io/rmstZ/
- https://github.com/GirlKiller512/RhythmMasterResource
