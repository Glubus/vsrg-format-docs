# EZ2DJ / EZ2AC chart (`.ez`, "EZFF")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian); retail files encrypted with a per-file-type 512-byte table

## Overview
EZFF is the chart container of the EZ2DJ/EZ2AC arcade games (Amuse World / Square Pixels). One file per mode, key count and difficulty tier (EZ2BMS names them `<mode>1p-<key>[-tier].ez`; tiers `hd`, `shd`, `ex`; modes 5K ONLY, SCRATCH, RUBY, 5K STANDARD, 7K, 10K Club, 14K Space, Andromeda, Catch). It holds every lane's notes and the background (autoplay) tracks; keysound names live in the sibling [`.ezi`](../ezi/README.md). Sources: EZ2BMS `packages/chart-core/src/io/ez/ezff.ts` and `ez2data/crypt.ts` (citing EZ2PORT `ez2/chart.c` and "the EZ2AC Bible's ez-chart.md / cipher.md"), `docs/importing.md`, `docs/ez2port-compat.md`. The cipher key tables are unpublished: they are read from the user's game executable.

## Container & encoding
- [observed: ez2dj1st_AcidJazz_*.ez, ezdance1_3week_*.ez] The PC editions of old EZ2DJ games (1st Tracks 1999, Dance Edition Vol.1 2000) ship plaintext EZFF files (they start `45 5A 46 46 00 04` = version 4, or `... 00 05` = version 5; header at the offsets below: 192 ticks per measure, BPM 97.5 / 117.2-117.5, 20-28 tracks) with plaintext `.ezi` next to them, file names `1P-<SONG>.ez`, `2P-`, `BT-`, `CLUB-` (4 charts per song: 1P, 2P, BT, CLUB). Version 4 and 5 headers match the table below.
- Little-endian. EZ2PORT treats an `.ez` as plaintext if it starts with `EZFF`.
- Cipher (`ez2data/crypt.ts`), not XOR: the file is processed in alternating 8- and 16-byte blocks (the block length flag toggles each block; a block shorter than 8 at the end takes the rest), blocks are reversed (destination `n - pos - len`) and each byte is shifted by a table byte: decrypt `out[pos+u] = (in[src+u] - table[(roll + len - 1 - u) & 0x1ff]) & 0xff` with `src = n - pos - len`, `roll = (roll + len) & 0x1ff` per block. Encrypt is the inverse with `+`. Each file type (`.ez`, `.ezi`, `.ini`, and per game version) has its own 512-byte table in the game executable.

## Structure / metadata
Header, 0x96 bytes:

| Offset | Type | Field |
|---|---|---|
| 0x00 | char[4] | `"EZFF"` |
| 0x04 | u8 | NUL |
| 0x05 | u8 | version (4, 5, 6, 7 or 8) |
| 0x06 | char[64] | name |
| 0x46 | char[64] | name2 |
| 0x86 | u16 | ticks per measure |
| 0x88 | f32 | BPM |
| 0x8C | u16 | track count (<= 96 accepted by EZ2BMS) |
| 0x8E | u32 | total ticks |
| 0x92 | f32 | BPM2 |

Then, per track: a 0x4E-byte header followed by records:

| Offset | Type | Field |
|---|---|---|
| 0x00 | char[4] | `"EZTR"` |
| 0x04 | u16 | 0 |
| 0x06 | char[64] | track name |
| 0x46 | u32 | track end tick (the port writes its last record's tick) |
| 0x4A | u32 | data size in bytes; record count = size / record size |

Record: `u32 tick; u8 type; payload`. Record size: 10 bytes in v4, 11 in v5/v6, 13 in v7/v8.

| type | meaning | payload |
|---|---|---|
| 1 | note | v7/v8: `u16 key @5, u8 vel @7, u8 pan @8, u8 kind @9, u16 length @10`; v5/v6: `u8 key @5, vel @6, pan @7, kind @8, u16 length @9` (v4: only the low length byte) |
| 2 | volume | `u8 value @5` |
| 3 | BPM | `f32 @5` |
| 4 | beats per measure | `u8 @5` |
| 5 | mark | no payload |
| 6.. | other; type 6 = scroll-speed multiplier (f32 @5) | raw u32 words @5 (and @9 in v7+) |

`key` = index of the keysound in the `.ezi`. `vel`/`pan` are per-note velocity and pan (0..127, centre pan 64) mixed as dB, not linearly. `kind` = "hold kind byte" (the Bible's `note_type`; semantics beyond holds: Unknown).

## Timing model
- Position = tick. EZ2BMS maps ticks to 1/48 beat ("ticks (1/48 beat)": 5 pulses per tick at its resolution of 240 per beat), so `ticks_per_measure` is 192 for 4/4 [inference from 48 ticks/beat x 4].
- Tempo: header `bpm` initial value, then type-3 records (f32). A note's time integrates f32 tempos tick by tick in milliseconds: EZ2BMS `timing/engine-tempo.ts` reproduces EZ2PORT's results bit for bit (millisecond granularity).
- Type-4 records (beats per measure) and marks do not affect playback timing per EZ2BMS ("beats-per-measure, marks and the stops the engine ignores", kept read-only).
- Scroll speed: type-6 records on track 0, rate as f32.

## Notes
- Notes are tracks: a lane is a track index that depends on the mode (EZ2BMS `modes/registry.ts` table, from EZ2PORT `docs/gds-slots.md` and `ez2/mode.c`). Other tracks are background (autoplay) sounds, played as taps.
- Lane (EZ2BMS bmson `x`) -> chart track: 5K ONLY / SCRATCH: keys x11..x15 -> tracks 3..7. RUBY and 5K STANDARD: scratch x1 -> 10, keys x11..15 -> 3..7, pedal x10 -> 11. 7K adds effectors x31 -> 8, x32 -> 9. 10K Club: adds 2P keys x21..25 -> 12..16 and 2P scratch x2 -> 19 (pedal at 11). 14K Space: 2P keys x21..25 -> 14..18, effectors x31,x32 -> 8,9, x33,x34 -> 12,13, scratch 2P x2 -> 19 (the "Club gotcha": the track for 2P keys differs between 10K and 14K). Andromeda adds a 2P pedal x20 -> 20. Catch: like 10K without 2P scratch.
- Hold notes: note `length` has a bias of 6: 0 or 6 = tap (short note), `6 + n` = hold of n ticks; the `kind` byte tells the hold kind. Scratch up/down on the same lane.
- Notes carry a velocity and pan and a keysound index; in-game lane control ids (.gds): keys 10-14, turntable 15/16, pedal 17, effectors 6-9, 2P 18-22, 23/24, 25.

## Audio & images
`.ssf` keysounds (16-bit 44.1 kHz stereo for new packages) referenced by the `.ezi`. A song package contains `song.ini`, the `.ez`/`.ezi`/`.ini` set, keysounds, title plate/disc/eyecatch `.abm` images, a BGA movie (EZ2BMS lists decodable ones: AVI, MPEG ... not all). The `.ez` stores none of it.

## Versions & variants
EZFF v4 (read-only in EZ2BMS), v5/v6 (older games: EC = v6 per the search snippets), v7/v8 (FINAL EX: 13-byte records, u16 keysound indices; "four record magics" per a snippet of ez2ac-re, unverified). EZ2DJ 7th Trax uses a different cipher table (snippet: `ez2stuff` `ezdec_715.c`/`ezdec_720.c`). Version 0.6/0.7/0.8 naming of old charts appears in EZ2Tools ("convert the old V0.6 chart format to the newer V0.7 or V0.8 format that can be used in FNEX"): [inference] 0.6..0.8 correspond to the EZFF version byte.

## Quirks & pitfalls
- The `EZFF` magic is visible only after decryption.
- Per-version key tables are inside the executable.
- 2P key track ids differ between modes.
- Long note length is biased by 6.
- v4's 10-byte record is too short for a u16 length (EZ2PORT reads into the next record; EZ2BMS reads one byte).
- Records are sorted per track by the writer, two BPM records at one tick are ambiguous in EZ2PORT's `qsort`.
- Max 96 tracks (EZ2BMS check).

## Example
Unknown (retail charts are encrypted).

## ROX support
Not read by ROX.

## Parsers & tools
- EZ2BMS (TypeScript/Rust, GPL-3.0): https://github.com/Roganis/EZ2BMS (`io/ez/ezff.ts`, `ez2data/crypt.ts`)
- EZ2Tools (C++): https://github.com/ben-rnd/EZ2Tools (chart converter V0.6 -> V0.7/0.8)
- EZ2PORT (the engine EZ2BMS follows; not found publicly)

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: the PC-edition RARs hold more songs: `https://archive.org/download/19990420_/19990420/The%201st%20Tracks%20Original%20(NoExe).rar`, `.../20000807_/20000101/Dance%20Edition%20Volume%20One%20(NoExe).rar`, also `20020728_` 4th Trax Over Mind and the 6th/7th TraX HDD images `6th-new.img`, `7th-20.img` (7-13 GB gz, not downloaded). The `Songs/<song>/ez/` folders come first in the RARs.

Arcade files (EZ2AC and later) are encrypted per file type with a table read out of the user's own game (EZ2BMS `ez2data/crypt.ts`). The archive.org item `ez2ac-update-package-collection` holds only encrypted update packages (`EZUpdate/package0` + `u_key`), not charts. EZ2BMS (https://github.com/Roganis/EZ2BMS, GPL-3.0) imports and publishes `.ez` files.

## Sources
- https://raw.githubusercontent.com/Roganis/EZ2BMS/main/packages/chart-core/src/io/ez/ezff.ts
- https://raw.githubusercontent.com/Roganis/EZ2BMS/main/packages/chart-core/src/ez2data/crypt.ts
- https://raw.githubusercontent.com/Roganis/EZ2BMS/main/packages/chart-core/src/modes/registry.ts , lanes.ts
- https://raw.githubusercontent.com/Roganis/EZ2BMS/main/docs/importing.md , ez2port-compat.md
- https://github.com/ben-rnd/EZ2Tools
- https://en.wikipedia.org/wiki/EZ2DJ
- https://github.com/forkwikiman/enha/blob/master/mirror/EZ2AC.md (series history)
