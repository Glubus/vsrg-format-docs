# DDR SSQ step data (`.ssq`)
Kind: chart

Doc status: complete (arcade core); Hudson/Wii and mine-chunk variants summarized (partial) · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: binary (little-endian chunks)

## Overview

`.ssq` is the step-data file of Konami's DDR arcade/console games. One file (usually `<song code>_all.ssq`) holds the tempo table, an event list and every chart of the song (Single/Double x Beginner/Basic/Difficult/Expert/Challenge), as RIFF-like chunks. It is documented by reverse engineering: SaxxonPike's `ssq.md` ("Its earliest occurrence is in unreferenced files in DDR 3rd Mix Plus. They are first officially used in DDR 4th Mix"; "originally developed without freeze notes in mind"), the DDR Research Master Thread (ZIv, travelsonic) and skogaby's `ssq_format.md` (most complete, verified against DDR World binaries and ~1,500 chunks). Files sit next to the `.xwb` audio bank; Ultramix (Xbox) packs them in `x_data_*.bin`.

## Packaged in

- [`gen`](../gen/).

## Container & encoding

- Little-endian. No magic: identified by extension. Every chunk is dword-aligned (length multiple of 4). A final `00 00 00 00` (chunk length 0) terminates; trailing zero padding is ignored. "There is no indication how long an SSQ file actually is", so readers loop until length 0.
- Chunk header (12 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| +0x00 | u32 | length | chunk size including this header (multiple of 4) |
| +0x04 | u16 | type | chunk type: 1 tempo, 2 events, 3 steps, 4/5 effect data (legacy), 9 metadata (rare), 17 sections (rare), 20 mines (mod) |
| +0x06 | u16 | param2 | type-dependent (TPS for tempo; difficulty code for steps) |
| +0x08 | u16 | param3 | type-dependent (entry count) |
| +0x0A | u16 | param4 | always 0 in observed files |

- Order: tempo (1), events (2), step chunks (3), then auxiliary chunks. Required: 1, 2 and at least one 3. The game finds tempo/events by linear walk and steps by `(type, param2)`. A chunk with `param2 == 0xFFFF` aborts the search (a forward-compat sentinel never used).
- A measure (whole note) is 4096 ticks in every tick-valued field (a beat = 1024 ticks). Time uses TPS (ticks per second), stored in the tempo chunk's `param2`: observed `1000` (modern, dominant), `150` and `75` (older "legacy" charts).

## Structure / metadata

Time-based chunks store all timestamps first, then all payload values (struct-of-arrays).

### Type 1: tempo (`param2` = TPS, `param3` = N)

Body: `i32 time_offset[N]` (measure ticks) then `i32 tempo_data[N]` (cumulative time in seconds-ticks = seconds x TPS). Size `12 + 8N`.

- BPM between entries `i-1`, `i`: `BPM = 240 * TPS * dMeasureTicks / (4096 * dSecondsTicks)`.
- Stop: two consecutive entries with the same `time_offset` and different `tempo_data`; `stop_seconds = d(tempo_data)/TPS` (the BPM formula divides by zero: special-case it).
- `time_offset[0]`: origin shift between the chart timeline and the audio-sync timeline (always 0 at TPS=1000; legacy files can be any i32, e.g. -4096, -8192, -12288 = the audio plays several beats before chart tick 0). Chart rows are always >= 0.
- `tempo_data[0]` = audio time of measure tick 0, in seconds x TPS (bounded to +-22 ms in TPS=1000 files; several seconds in legacy files). Relation to StepMania: `tempo_data[0] = -#OFFSET x TPS` (`#OFFSET:-0.250` becomes `tempo_data[0] = 250` at TPS 1000; copying the offset without negating desyncs by `2*|offset|`).
- Runtime normalization (game): `normalized[i] = round(tempo_data[i]*1000/TPS + 0.5)`.

### Type 2: events (`param2` = 1, `param3` = N)

Body: `i32 time_offset[N]`, then `N x {u8 code, u8 arg}`. Dispatch: code 1 = no effect (reserved); code 2 = flow-control marker (arg 1 = song start, 2 = chart start/"ready go" off, 3 = pre-end cue, 4 = song end/results trigger, 5 = alternate start cue); code 4 and 5 emit events into a separate list (`{time,4,arg}`, `{time,(arg&0x3F)+1,random()}`); others are consumed silently. Canonical 6-entry pattern: `(1,4)@0, (2,1)@0, (2,2)@4096, (2,5)@4096, (2,3)@END-4096, (2,4)@END`.

### Type 3: step chart (`param2` = difficulty code, `param3` = N)

`param2` = `(slot << 8) | style`:

| Style (low byte) | Meaning | Active panels |
|---|---|---|
| `0x14` | Single | 4 (bits 0-3) |
| `0x18` | Double | 8 (bits 0-7) |

| Slot (high byte) | Name | Alt names |
|---|---|---|
| `0x01` | Basic | Light |
| `0x02` | Difficult | Standard, Another, Trick |
| `0x03` | Expert | Heavy, Maniac, SSR |
| `0x04` | Beginner | |
| `0x06` | Challenge | Oni, CHAOS |

Valid codes: `0114 0214 0314 0414 0614` (Single Basic/Difficult/Expert/Beginner/Challenge) and `0118 0218 0318 0418 0618` (Double). Slot `0x05` is not accepted. (SaxxonPike's table labels them Single Basic/Standard/Heavy/Beginner/Challenge with the same hex values.)

Body: `i32 time_offset[N]` (measure ticks, ascending, >= 0), `u8 step[N]`, then (if the 1-byte array has odd length) 1 pad byte, then the freeze block `F x {u8 panels, u8 kind}` where `F` = number of `0x00` step bytes, then 0 or 2 bytes of pad to a dword. `chunk_length = 12 + 4N + round_up_to_even(N) + 2F + trailing_pad`.

Step byte (bit `0` = P1 Left, `1` = P1 Down, `2` = P1 Up, `3` = P1 Right, `4..7` = the same four for P2; singles use only the low nibble):

| Value | Meaning |
|---|---|
| `0x00` | freeze-end marker: consumes the next freeze-block entry |
| `0xFF` | shock arrow, both sides (all 8 panels) |
| `0x0F` | shock arrow P1 side (single: shock; double: P1 only) |
| `0xF0` | shock arrow P2 side (double only) |
| other | normal step: bitmask of panels hit simultaneously |

Shock arrows are DDR X+ ("As of DDR X, shock arrows are part of the format ... all bits set"); older games have none.

Freeze (hold) arrows are encoded in two places: (1) a normal step byte at the head time whose bits include the freeze panels; (2) a later `0x00` step at the tail time plus one freeze-block entry `(panels, kind)` with `kind = 0x01` (normal freeze; other kinds are silently ignored) and `panels` = the panels whose freeze ends. The game resolves each bit of `panels` by walking backwards through already-built notes to the most recent earlier note hit on that panel and setting its duration = `tail_time - head_time`. Several heads can share one tail by setting several bits. The trailing pad `00 00` reads as a kind 0 entry and is ignored.

### Auxiliary chunks (legacy / rare; ignored by the step engine)

- Type 4 (effect data A, `param2` = 1, legacy TPS=150 files only, always paired with type 5): `i32 time_offset[N]` (first = sentinel `-99999` = bytes `61 79 FE FF`), `u8 data[N]` in `{0x80, 0xFF}` (binary toggle, believed to be a stage-lamp script), pad to dword.
- Type 5 (effect data B, `param2` = 0): `i32 time_offset[N]`, `(N-1)` 4-byte records `{u8 tag, u8 arg, u16 param}`, separator `95 14 00 00`, `i32 M`, `M` records. Semantics unknown (round-trips byte for byte).
- Type 9 (metadata, one known file `thr8.ssq`): embedded artist string + unstructured data; SaxxonPike: "contains at least the title and artist of a song... discovered by looking at DDR S+". Format unknown.
- Type 17 (sections, rare): `N x {i32 start, i32 end}`; semantics unknown.

## Timing model

Only the tempo chunk is used. A note at `tick` lies in the tempo segment `[time_offset[i-1], time_offset[i]]`. Its audio time in seconds-ticks is the linear interpolation `tempo_data[i-1] + (tick - time_offset[i-1]) * (tempo_data[i] - tempo_data[i-1]) / (time_offset[i] - time_offset[i-1])` (what the game does at runtime), divided by TPS for seconds. `tempo_data[0]/TPS` is already the audio time of tick 0, so no separate offset is added. Stops are zero-length segments (equal `time_offset`). No BPM numbers are stored; BPM derives from the two arrays. Charts of one song share the single tempo chunk. The time signature is always 4/4 (4096 ticks per measure).

## Notes

- Notes are rows `(tick, panel bitmask)`; jumps = several bits. Per-note types: freeze (via `0x00`/freeze block) and shock (`0xFF/0x0F/0xF0`). Vanilla files have no mines (the DDR World mod adds a mine chunk), rolls, lifts or keysounds.
- ZIv's thread describes the pre-MAX (1st-5th Mix) edit-mode RAM layout: one byte per beat, high nibble = P2, low nibble = P1 (4-panel values `1` Left, `2` Right, `4` Up, `8` Down, `0xF` = quantization marker; solo charts use the P2 nibble for UL/UR). It is not the on-disc encoding.
- The step values quoted there ("Single arrow values: 1 = Left, 2 = Down, 4 = Up, 8 = Right; add values for jumps; 0x0F as 'quad step' in edit mode") match the bit table above and `ssq.md` (bits 0-3 = P1 Left/Down/Up/Right, 4-7 = P2).

## Audio & images

None in the file. Audio is a separate bank (`.xwb` in newer games, sometimes with `.xsb`; `WAVM` in Ultramix) named by the same song code (`<songcode>_all.ssq` + `<songcode>.xwb`).

## Versions & variants

- Arcade/modern (TPS=1000, chunks 1/2/3 only): DDR A, A20, A3, World etc. (skogaby verified against DDR World).
- Legacy (TPS 150 or 75; chunks 1/2/3 plus 4/5/9/17; non-zero `time_offset[0]`): older mixes and Ultramix-era Xbox titles ("DDR_LEGACY" in ddr-chart-tools).
- Hudson Soft Wii ports (DDR Mario Mix, Hottest Party 1): chart in a type 9 chunk (header like type 3, `param2` = difficulty code) with body `u32 extra_offset`, `N x i32` ticks, then variable rows (`mask byte` + one item byte per set bit; `mask 0` = freeze end whose data is in the extra block's `FREZ` table) and an `EXDT` extra block with `CHAR` (12-byte gimmick-item entries) and `FREZ` (3-byte entries) sub-blocks. Items: 2 = "Koopa" double arrow (echo arrow one beat later), 5/14 = hazards. Told apart from the arcade type 9 metadata chunk by `param2`.
- Hudson Hottest Party 4/5: type 16 "lane format": body `N x i32` ticks, `N x u8` lane (0xFF = no note), pad, `N x {i16 type, u16 param}` items (`type 0 param 1` = freeze end); style codes `0x14` single foot, `0x18` double foot (HP5), `0x1a` foot + Wii Remote hands, plus controller variants `0x24/0x34/0x2a/0x3a/0x4a` (HP4).
- Mine chunk (DDR World mod, kind 20): `12 + 8N` bytes; per-difficulty (`param2` = same difficulty code); entries `{i32 tick, u8 panels, u8 flags(=0), u16 reserved(=0)}`; panel bitmask as type 3; `0x00`/`0xFF`/`0x0F`/`0xF0` masks illegal. Vanilla DDR ignores it. Specified in skogaby's `ssq_mine_chunk_format.md`.
- Games before 4th Mix used the `STEP`/`STEP2` formats ([step](../step/README.md), [step2](../step2/README.md)).

## Quirks & pitfalls

- Struct-of-arrays: all `N` timestamps precede the `N` payload items.
- Odd N needs a pad byte before the freeze block, then dword padding after it.
- A freeze tail is a `0x00` step byte; its panel mask is in a separate table in file order.
- `0x0F`/`0xF0`/`0xFF` are shock arrows, not four-panel jumps.
- Stops are equal offsets, BPM is deltas, TPS differs per file.
- `time_offset[0]` can be negative; `tempo_data[0]` has the opposite sign of StepMania `#OFFSET`.
- `param2 == 0xFFFF` aborts lookup; tools must not emit it. Of duplicate `(type, param2)` chunks only the first is found.

## Example

No `.ssq` binary is vendored (game data). Annotated tempo chunk with stops at TPS=150, from skogaby's `ssq_format.md` §3.5:

```
0x0000  54 00 00 00      chunk length = 84
0x0004  01 00            type = 1 (tempo)
0x0006  96 00            param2 = 150 (TPS)
0x0008  09 00            param3 = 9 entries
0x000A  00 00            param4 = 0
0x000C  time_offset[0..8] = 0, 4096, 73728, 73728, 272384, 370688, 370688, 372736, 684032
0x0030  tempo_data[0..8]  = 1, 94, 1689, 1829, 6376, 10876, 10970, 11064, 18189
```

Entries 2 and 3 share `time_offset` 73728: a stop of (1829-1689)/150 = 0.933 s. BPM between entries 1 and 2 = 240*150*(73728-4096)/(4096*(1689-94)) ~ 383.7.

## ROX support

Decode only (ROX never writes SSQ), since Prism added `rox::formats::ssq`. `SsqDecoder::variants` lists the first chunk of each of the ten difficulty codes that has a playable note; `decode_variant` / `decode_with_report` / `decode_with_title` / `decode_file` return a 4-column (Single) or 8-column (Double) chart. A zero length ends the chunk walk, a bad length keeps earlier chunks, `param2 == 0xFFFF` ends it as in the game. Stops are zero-length segments; a note on a stop's tick is hit when the stop begins. Freezes become holds, shock arrows (`0x0F`, `0xF0`, `0xFF`) become one mine per panel of the side, the DDR World mine chunk (type 20) adds mines. Difficulty names are the slot names (`Beginner`, `Basic`, `Difficult`, `Expert`, `Challenge`). `audio_file` is empty and the title is the file stem when decoded from a path (`auto_decode*`, `decode_file`). Not read: Hudson charts (types 9 and 16, named in the report), effect, event and section chunks. No real `.ssq` is in the repository (no licence); tests build files in memory and use the example tempo chunk above as a byte-for-byte vector. Source: `rhythm-open-exchange/src/formats/ssq/` (`mod.rs`, `tests.rs`).

Prism (`docs/game.md` "Formats de danse") lists one entry per Single/Double chart, titled by the file stem. The sound is the audio file of the folder with the `.ssq`'s name (`a01_all.ssq` plays `a01_all.ogg`), else the folder's first audio file, else the charts are marked as missing audio and played silent. The `.xwb` bank is not read. Another StepMania-family file in the folder shadows the `.ssq` (it loads last); the MP3 is timed gapless.

## Parsers & tools

- [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (Rust; SSQ <-> SSC, legacy/Ultramix/Hudson variants, `docs/ssq_format.md`).
- [SaxxonPike/RhythmCodex](https://github.com/SaxxonPike/RhythmCodex) (C#, SSQ/XWB decoding); [SaxxonPike/rhythm-game-formats](https://github.com/SaxxonPike/rhythm-game-formats) (docs); Scharfrichter (named by `ddr-render.py` as its default converter backend); `ddrcharttool.py` (SM -> SSQ, mentioned in community guides); [drmext/ddr-datatools](https://github.com/drmext/ddr-datatools) (`ddr-render.py` mass converts xwb+ssq to ogg/.sm); [sbruder/brd](https://github.com/sbruder/brd) (`ddr2osu`: SSQ+XWB -> osu!).

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md) (DDR S iOS app `Payload/DDRSUS.app/<code>.ssq` from archive.org item `DDR_S_1.0.3_ios_2.0`, plus RhythmCodex fixtures). More: the SSQ of any DDR release you own (`<song id>_all.ssq`); the DDR S+ app `DanceDanceRevolution S Lite (US) (v2.1.2) [Decrypted].ipa` (archive.org `ios-ipa-com.konami.ddrslite`) bundles three `.gen` packages ([`../gen`](../gen/README.md)); Ultramix charts via [`../ultramix-archive`](../ultramix-archive/README.md); Hudson variants in [`../hudson-ssq`](../hudson-ssq/README.md). Readers: RhythmCodex, [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools), [sbruder/brd](https://github.com/sbruder/brd), drmext/ddr-datatools.

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/ssq.md
- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/ssq_format.md (+ ssq_mine_chunk_format.md, hudson_ssq_format.md, hudson_lane_ssq_format.md, ultramix_archive_formats.md)
- https://zenius-i-vanisher.com/v5.2/thread?threadid=7564 (DDR Research Master Thread)
- https://github.com/skogaby/ddr-chart-tools, https://github.com/sbruder/brd, https://github.com/drmext/ddr-datatools
