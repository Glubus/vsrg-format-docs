# DDR SSQ step data (`.ssq`)
Kind: chart

Doc status: complete (arcade core); Hudson/Wii and mine-chunk variants summarized (partial) · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: binary (little-endian chunks)

## Overview

`.ssq` is the step-data file of Konami's Dance Dance Revolution arcade/console games: one `.ssq` (usually named `<song code>_all.ssq`) holds the tempo table, an event list and **every chart of the song** (Single/Double x Beginner/Basic/Difficult/Expert/Challenge). It is a sequence of "chunks" much like a WAV/RIFF file. The format has no public specification from Konami; it is documented by reverse engineering: SaxxonPike's `ssq.md` ("To date, SSQ is the most recent format used by Konami's DDR series. Its earliest occurrence is in unreferenced files in DDR 3rd Mix Plus. They are first officially used in DDR 4th Mix"; "originally developed without freeze notes in mind"), the DDR Research Master Thread (ZIv, travelsonic; edit-mode/stepdata notes), and skogaby's `ssq_format.md` (the most complete, verified against DDR World binaries and ~1,500 chunks). Files are found next to the audio bank (`.xwb`) in the game data; Ultramix (Xbox) packs them in `x_data_*.bin` archives. Tools convert SSQ <-> StepMania (`.ssc`).

## Packaged in

- Packaged in [`gen`](../gen/).

## Container & encoding

- **Endianness**: little-endian. **No magic**: identified by extension. **Alignment**: every chunk is dword-aligned (length multiple of 4). **Terminator**: a final `00 00 00 00` (chunk length 0); trailing zero padding is ignored; "there is no indication how long an SSQ file actually is", readers loop until length 0.
- Chunk header (12 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| +0x00 | u32 | length | chunk size **including** this header (multiple of 4) |
| +0x04 | u16 | type | chunk type: 1 tempo, 2 events, 3 steps, 4/5 effect data (legacy), 9 metadata (rare), 17 sections (rare), 20 mines (mod) |
| +0x06 | u16 | param2 | type-dependent (TPS for tempo; difficulty code for steps) |
| +0x08 | u16 | param3 | type-dependent (entry count) |
| +0x0A | u16 | param4 | always 0 in observed files |

- Order: tempo (1) first, events (2) second, step chunks (3), then auxiliary chunks. Required: 1, 2 and at least one 3. The game finds tempo/events by linear walk and steps by `(type, param2)`; any chunk with `param2 == 0xFFFF` aborts the search (a forward-compat sentinel never used).
- Ticks: a **measure (whole note) is 4096 ticks** in every tick-valued field (a beat = 1024 ticks). Time uses **TPS** (ticks per second) stored in the tempo chunk's `param2`: observed values `1000` (modern, dominant), `150` and `75` (older "legacy" charts).

## Structure / metadata

All time-based chunks store **all timestamps first, then all payload values** (struct-of-arrays).

### Type 1: tempo (`param2` = TPS, `param3` = N)

Body: `i32 time_offset[N]` (measure ticks, 4096 = one whole note) then `i32 tempo_data[N]` (cumulative time in *seconds-ticks* = seconds x TPS). Size `12 + 8N`.

- BPM between entries `i-1`, `i`: `BPM = 240 * TPS * dMeasureTicks / (4096 * dSecondsTicks)`.
- **Stop**: two consecutive entries with the **same** `time_offset` and different `tempo_data`; `stop_seconds = d(tempo_data)/TPS` (BPM formula divides by zero: special-case it).
- `time_offset[0]`: origin shift between the chart timeline and the audio-sync timeline (always 0 at TPS=1000; legacy files can be any i32, e.g. -4096, -8192, -12288 = the audio plays several beats before chart tick 0). Chart rows are always >= 0.
- `tempo_data[0]` = audio time of measure tick 0, in seconds x TPS (bounded to +-22 ms in TPS=1000 files; several seconds in legacy files). Relationship to StepMania: `tempo_data[0] = -#OFFSET x TPS` (a simfile `#OFFSET:-0.250` becomes `tempo_data[0] = 250` at TPS 1000; copying the offset without negating desyncs by `2*|offset|`).
- Runtime normalization (game): `normalized[i] = round(tempo_data[i]*1000/TPS + 0.5)`.

### Type 2: events (`param2` = 1, `param3` = N)

Body: `i32 time_offset[N]`, then `N x {u8 code, u8 arg}`. Dispatch: code 1 = no effect (reserved); code 2 = flow-control marker (arg 1 = song start, 2 = chart start/"ready go" off, 3 = pre-end cue, 4 = song end/results trigger, 5 = alternate start cue); code 4 and 5 emit events into a separate list (`{time,4,arg}`, `{time,(arg&0x3F)+1,random()}`); others consumed silently. Canonical 6-entry pattern: `(1,4)@0, (2,1)@0, (2,2)@4096, (2,5)@4096, (2,3)@END-4096, (2,4)@END`.

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

Body: `i32 time_offset[N]` (measure ticks, ascending, >= 0), `u8 step[N]`, then (if the 1-byte array has odd length) 1 pad byte, then the **freeze block** `F x {u8 panels, u8 kind}` where `F` = number of `0x00` step bytes, then 0 or 2 bytes of pad to a dword. `chunk_length = 12 + 4N + round_up_to_even(N) + 2F + trailing_pad`.

Step byte (bit `0` = P1 Left, `1` = P1 Down, `2` = P1 Up, `3` = P1 Right, `4..7` = the same four for P2; singles use only the low nibble):

| Value | Meaning |
|---|---|
| `0x00` | **freeze-end marker**: consumes the next freeze-block entry |
| `0xFF` | shock arrow, both sides (all 8 panels) |
| `0x0F` | shock arrow P1 side (single: shock; double: P1 only) |
| `0xF0` | shock arrow P2 side (double only) |
| other | normal step: bitmask of panels hit simultaneously |

Shock arrows are DDR X+ ("As of DDR X, shock arrows are part of the format ... all bits set"); older games have none.

**Freeze (hold) arrows** are encoded in two places: (1) a normal step byte at the head time whose bits include the freeze panels; (2) a later `0x00` step at the tail time plus one freeze-block entry `(panels, kind)` with `kind = 0x01` (normal freeze; other kinds are silently ignored) and `panels` = the panels whose freeze ends. Resolution (game): for each bit of `panels`, walk **backwards** through already-built notes to the most recent earlier note hit on that panel and set its duration = `tail_time - head_time`. Several heads can share one tail by setting several bits. The trailing pad `00 00` is read as a kind 0 entry and ignored.

### Auxiliary chunks (legacy / rare; ignored by the step engine)

- **Type 4** (effect data A, `param2` = 1, legacy TPS=150 files only, always paired with type 5): `i32 time_offset[N]` (first = sentinel `-99999` = bytes `61 79 FE FF`), `u8 data[N]` in `{0x80, 0xFF}` (binary toggle, believed to be a stage-lamp script), pad to dword.
- **Type 5** (effect data B, `param2` = 0): `i32 time_offset[N]`, `(N-1)` 4-byte records `{u8 tag, u8 arg, u16 param}`, separator `95 14 00 00`, `i32 M`, `M` records. Semantics unknown (round-trips byte for byte).
- **Type 9** (metadata, one known file `thr8.ssq`): embedded artist string + unstructured data; SaxxonPike: "contains at least the title and artist of a song... discovered by looking at DDR S+". Format unknown.
- **Type 17** (sections, rare): `N x {i32 start, i32 end}`; semantics unknown.

## Timing model

Position -> time uses the tempo chunk exclusively: a note at `tick` lies in the tempo segment `[time_offset[i-1], time_offset[i]]`; its audio time in seconds-ticks is the linear interpolation `tempo_data[i-1] + (tick - time_offset[i-1]) * (tempo_data[i] - tempo_data[i-1]) / (time_offset[i] - time_offset[i-1])` (this is what the game does at runtime), divided by TPS for seconds; `tempo_data[0]/TPS` is already the audio time of tick 0, so no separate offset is added. Stops are zero-length segments (equal `time_offset`). There are **no** stored BPM numbers: BPM is derived from the two arrays. Charts of one song share the single tempo chunk (no per-chart timing). The time signature is always 4/4 (4096 ticks per measure).

## Notes

- Notes are **rows**: `(tick, panel bitmask)`; jumps = several bits; no per-note type except freeze (via `0x00`/freeze block) and shock (`0xFF/0x0F/0xF0`). No mines in vanilla files (the DDR World mod adds a mine chunk, below), no rolls, no lifts, no keysounds.
- ZIv's research thread also describes the pre-MAX (1st-5th Mix) **edit mode** in-memory layout: one byte per beat, high nibble = P2 and low nibble = P1 (4-panel nibble values `1` Left, `2` Right, `4` Up, `8` Down, `0xF` = quantization marker; solo charts use the P2 nibble for UL/UR). That is RAM layout of the editor, not the on-disc SSQ encoding.
- The SSQ step values quoted in the same thread ("Single arrow values: 1 = Left, 2 = Down, 4 = Up, 8 = Right; add values for jumps; 0x0F as 'quad step' in edit mode") agree with the bit table above and with SaxxonPike's `ssq.md` (bits 0-3 = P1 Left/Down/Up/Right, 4-7 = P2).

## Audio & images

None in the file. Audio is a separate bank (`.xwb` XACT wave bank in newer games, sometimes with `.xsb`; `WAVM` in Ultramix) named by the same song code; jackets/banners are separate assets. File naming for conversion: `<songcode>_all.ssq` + `<songcode>.xwb`.

## Versions & variants

- **Arcade/modern** (TPS=1000, chunks 1/2/3 only): DDR A, A20, A3, World etc. (skogaby verified against DDR World).
- **Legacy** (TPS 150 or 75; chunks 1/2/3 plus 4/5/9/17; non-zero `time_offset[0]`): older mixes and Ultramix-era Xbox titles ("DDR_LEGACY" in ddr-chart-tools).
- **Hudson Soft Wii ports** (DDR Mario Mix, Hottest Party 1): chart in a **type 9** chunk (header like type 3, `param2` = difficulty code) with body `u32 extra_offset`, `N x i32` ticks, then variable rows (`mask byte` + one item byte per set bit; `mask 0` = freeze end whose data is in the extra block's `FREZ` table) and an `EXDT` extra block with `CHAR` (12-byte gimmick-item entries) and `FREZ` (3-byte entries) sub-blocks. Items: 2 = "Koopa" double arrow (echo arrow one beat later), 5/14 = hazards. Distinguished from the arcade type 9 metadata chunk by `param2`.
- **Hudson Hottest Party 4/5**: **type 16** "lane format": body `N x i32` ticks, `N x u8` lane (0xFF = no note), pad, `N x {i16 type, u16 param}` items (`type 0 param 1` = freeze end); style codes `0x14` single foot, `0x18` double foot (HP5), `0x1a` foot + Wii Remote hands, plus controller variants `0x24/0x34/0x2a/0x3a/0x4a` (HP4).
- **Mine chunk (DDR World mod, kind 20)**: `12 + 8N` bytes; per-difficulty (`param2` = same difficulty code); entries `{i32 tick, u8 panels, u8 flags(=0), u16 reserved(=0)}`; panel bitmask as type 3; `0x00`/`0xFF`/`0x0F`/`0xF0` masks illegal. Vanilla DDR ignores it. Specified in skogaby's `ssq_mine_chunk_format.md`.
- Games before 4th Mix used the **`STEP`/`STEP2`** formats ([step](../step/README.md), [step2](../step2/README.md)).

## Quirks & pitfalls

- Everything is struct-of-arrays: read all `N` timestamps before `N` payload items.
- **Odd N** needs a pad byte before the freeze block; the chunk then needs dword padding after it.
- A freeze tail is a `0x00` step byte, not a "tail note": its panel mask lives in a separate table in file order.
- A step byte of `0x0F`/`0xF0`/`0xFF` is a shock arrow, not a four-panel jump.
- Stops are encoded by *equal offsets*; BPM by deltas; TPS differs per file.
- `time_offset[0]` can be negative; `tempo_data[0]` is the audio-sync base: sign convention is **opposite** to StepMania `#OFFSET`.
- `param2 == 0xFFFF` aborts lookup; tools must not emit it.
- Duplicate `(type, param2)` chunks: only the first is found.

## Example

No `.ssq` binary is vendored (files are game data). Annotated example of a tempo chunk with stops at TPS=150, quoted from skogaby's `ssq_format.md` §3.5:

```
0x0000  54 00 00 00      chunk length = 84
0x0004  01 00            type = 1 (tempo)
0x0006  96 00            param2 = 150 (TPS)
0x0008  09 00            param3 = 9 entries
0x000A  00 00            param4 = 0
0x000C  time_offset[0..8] = 0, 4096, 73728, 73728, 272384, 370688, 370688, 372736, 684032
0x0030  tempo_data[0..8]  = 1, 94, 1689, 1829, 6376, 10876, 10970, 11064, 18189
```

Entries 2 and 3 share `time_offset` 73728: a stop of (1829-1689)/150 = 0.933 s; BPM between entries 1 and 2 = 240*150*(73728-4096)/(4096*(1689-94)) ~ 383.7.

## ROX support

Read by ROX since Prism's addition of `rox::formats::ssq` (decode only: ROX does not write SSQ). `SsqDecoder::variants` lists the playable charts (step chunks with one of the ten difficulty codes above, the first chunk of each code, with at least one playable note), `decode_variant` / `decode_with_report` / `decode_with_title` / `decode_file` give a 4-column (Single) or 8-column (Double) chart per variant. Chunk walk as above (zero length ends it; a bad length keeps the chunks before it; `param2 == 0xFFFF` ends it as in the game). Ticks to time by the interpolation of the tempo chunk (`tempo_data[0]` is the audio time of entry 0, nothing is added); BPM points are derived per segment, stops are zero-length segments, a note on a stop's tick is hit when the stop begins. Freezes become holds (head = the most recent earlier note on each panel of the freeze entry), shock arrows (`0x0F`, `0xF0`, `0xFF`) become one mine per panel of the side, the DDR World mine chunk (type 20) adds mines; difficulty names are the slot names (`Beginner`, `Basic`, `Difficult`, `Expert`, `Challenge`). The file has no title or audio: `audio_file` is empty and the title is the file stem when decoded from a path (`auto_decode*`, `decode_file`). Not read: Hudson charts (types 9 and 16, named in the report), the effect, event and section chunks. No real `.ssq` is in the repository (Konami's data has no licence); the tests use files built in memory and the tempo chunk of the example above as a byte-for-byte vector. Source: `rhythm-open-exchange/src/formats/ssq/` (decisions in its `mod.rs`, tests in `tests.rs`).

Read by Prism (`docs/game.md` "Formats de danse"): one entry per Single/Double chart, titled by the file stem; the sound is the audio file of the folder with the `.ssq`'s own name (`a01_all.ssq` plays `a01_all.ogg`), else the folder's first audio file, else the charts are listed without sound, marked as missing their audio, and played silent. The `.xwb` bank of the arcade is not read. Any other StepMania-family file of the folder shadows the `.ssq` (it comes last in the loader order); the MP3 is timed gapless.

## Parsers & tools

- [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (Rust; SSQ <-> SSC, legacy/Ultramix/Hudson variants, `docs/ssq_format.md`).
- [SaxxonPike/RhythmCodex](https://github.com/SaxxonPike/RhythmCodex) (C#, SSQ/XWB decoding); [SaxxonPike/rhythm-game-formats](https://github.com/SaxxonPike/rhythm-game-formats) (docs); Scharfrichter (named by `ddr-render.py` as its default converter backend); `ddrcharttool.py` (SM -> SSQ, mentioned in community guides); [drmext/ddr-datatools](https://github.com/drmext/ddr-datatools) (`ddr-render.py` mass converts xwb+ssq to ogg/.sm); [sbruder/brd](https://github.com/sbruder/brd) (`ddr2osu`: SSQ+XWB -> osu!).

## Getting samples

Manifest (fetched to `samples-local/vsrg/ddr/ssq/`, [`SOURCES.md`](samples/SOURCES.md)): the four real `.ssq` fixtures of the RhythmCodex test suite ([SaxxonPike/RhythmCodex](https://github.com/SaxxonPike/RhythmCodex), commit `6c60e9b710150c6ca4adf9b7d93e51c2ad39b2ee`, `Source/RhythmCodex.Lib.Test.Data/Ssq/`: `freeze.ssq` 12,560 bytes, `shock.ssq` 12,572, `59rm_all.ssq` 7,932 (offset/tempo test), `solo.ssq` 8,980 (6-panel)), each inside a small ZIP. The repository licence (MIT, file `LICENSE.md`) lists that path, but the data are charts of commercial DDR releases, so nothing is committed.

More: the SSQ of any DDR arcade/console release you own (`<song id>_all.ssq`, e.g. in the arcade game's data or the `.gen` of DDR S+); the Ultramix charts via the extractor of `ddr-chart-tools` ([`../ultramix-archive`](../ultramix-archive/README.md)); Hudson variants in [`../hudson-ssq`](../hudson-ssq/README.md). Tools that read SSQ: RhythmCodex, [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools), [sbruder/brd](https://github.com/sbruder/brd), drmext/ddr-datatools; none ships fixtures other than RhythmCodex's.

## Sources

- https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ddr/ssq.md
- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/ssq_format.md (+ ssq_mine_chunk_format.md, hudson_ssq_format.md, hudson_lane_ssq_format.md, ultramix_archive_formats.md)
- https://zenius-i-vanisher.com/v5.2/thread?threadid=7564 (DDR Research Master Thread)
- https://github.com/skogaby/ddr-chart-tools, https://github.com/sbruder/brd, https://github.com/drmext/ddr-datatools
