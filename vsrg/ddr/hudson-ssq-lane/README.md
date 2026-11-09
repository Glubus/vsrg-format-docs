# Hudson SSQ type 16 lane-format chunk (DDR Hottest Party 4/5, Wii)
Kind: chart

Doc status: complete (as reverse engineered) · ROX: no · Category: vsrg · Encoding: binary (little-endian chunk inside an `.ssq`)

## Overview

DDR Hottest Party 4 and 5 (Wii, Hudson Soft) store each chart in a type 16 chunk of the [`.ssq`](../ssq/README.md) container. It replaces the [type 9](../hudson-ssq/README.md) chart of Hottest Party 1 and Mario Mix (only the 12-byte header is shared). Type 3 and 9 rows are panel masks; a type 16 row names a single lane. skogaby documented it in `ddr-chart-tools/docs/hudson_lane_ssq_format.md`, verified against the HP4 and HP5 main DOLs and every chart on both discs (57 HP4 songs / 1,098 charts; 121 HP5 songs / 798 charts). The chunk also carries Wii Remote "hand" charts and controller variants; only foot charts matter for conversion.

## Container & encoding

Little-endian (the PowerPC game byte-swaps on load). The game routes chunk types 3, 9 and 16 into the same chart-slot table; HP4/HP5 use type 16 only. Chunks advance by `length` rounded up to a dword.

## Structure / metadata

### Chunk header

| Offset | Type | Field |
|---|---|---|
| +0x00 | u32 | chunk length including header, dword-aligned |
| +0x04 | u16 | `16` |
| +0x06 | u16 | `param2`: style code (low byte) and difficulty slot (high byte) |
| +0x08 | u16 | `param3`: row count `N` |
| +0x0A | u16 | 0 |

Difficulty high byte: arcade values (`0x01` Basic, `0x02` Difficult, `0x03` Expert, `0x04` Beginner; HP5 also accepts `0x06` Challenge). The low byte is split into a low nibble (lane layout) and a high nibble (controller variant):

| Low byte | Game slot | Meaning | Lanes |
|---|---|---|---|
| `0x14` | 0 | Single, foot | 0-3 |
| `0x18` | 2 | Double, foot (HP5 only) | 0-7 |
| `0x1a` | 1 | Single, foot + Wii Remote hands | 0-3 foot, 4-5 hand |
| `0x24`, `0x34` | 3, 4 | Single, Wii-controller variants (HP4 only) | 0-3 |
| `0x2a`, `0x3a` | 5, 6 | foot + hands, controller variants (HP4 only) | 0-5 |
| `0x4a` | 7 | foot + hands, controller variant (HP4 only) | 0-5 |

Which controller each of slots 3-7 maps to (Balance Board, Remote only, Remote + Nunchuk...) was not traced.

### Body

| Offset | Type | Field |
|---|---|---|
| +0x0C | N x i32 | row ticks in measure ticks (4096 per measure), ascending |
| +0x0C + 4N | N x u8 | row lane index |
| ... | 0-3 bytes | pad so the item records start on a dword |
| ... | N x 4 bytes | row item records |

Total body size is `4N + ceil4(N) + 4N`. There is **no extra block**, no `CHAR`/`FREZ` table and no offset field: the loader computes the item-record offset directly from `N`.

A row is the i-th element of each of the three arrays:
- tick: i32 measure ticks.
- lane: u8 lane index: the bit position in the type 3 mask (0 P1 Left, 1 Down, 2 Up, 3 Right, 4-7 the same for P2; 4-5 are hands in the `0x?a` styles). **`0xFF` = no note** (row skipped).
- item: `{ i16 type, u16 param }`:

| type | param | Meaning |
|---|---|---|
| 0 | 0 | plain arrow on `lane` |
| 0 | 1 | **freeze end** on `lane` |
| -1 | any | no note; the row is skipped |
| k >= 1 | any | arrow on `lane` carrying gimmick item `k` with parameter `param` |

### Row merging

The loader walks rows in order and merges every run of rows whose tick is `<=` the run's first tick into **one step record** (mask of arrow lanes) and **one hold record** (mask of freeze-end lanes), as a type 3 step byte and freeze entry would be. Rows are sorted ascending on disc, so a run is "all rows at the same tick". A tick can yield both a step and a hold record. Hard limits: 0x800 step records, 0x800 hold records, 128 distinct gimmick items per chart.

## Timing model

Measure ticks (4096 per whole note) through the file's type 1 tempo chunk (HP4/HP5: TPS = 150, type 2 events as on HP1). See [`../ssq`](../ssq/README.md).

## Notes

- Tap: item `(0, 0)` on a lane. Chord = several rows at the same tick.
- Freeze: head = ordinary arrow; end = item `(0, 1)` on the same lane. A freeze end closes the most recent earlier arrow on that lane (like a type 3 freeze entry of kind 1). In the whole corpus every freeze end has a head, no head and end share a tick, and no lane has two arrows on one tick. When a freeze end and a new arrow on the same lane share a tick, the end must resolve first (emit the end row ahead of the step row at equal ticks).
- Gimmicks: HP4/HP5 moved foot-chart gimmicks out of the SSQ into separate files (`ssq/GIMMICK/%s.bin`), so foot charts carry only type 0 items. Non-zero item types appear only in hand styles (`0x?a`): HP4 uses types 1-7 with parameters 0-8 and 100-108 for Wii Remote actions (semantics not traced).

## Audio & images

Not in the chunk.

## Versions & variants

- HP4 and HP5: type 16; HP5 adds double (`0x18`) and Challenge (`0x06`).
- Other chunks on these discs: type 1 tempo, type 2 events, type 17 section markers as on arcade; type 18 (HP5 only, 4 songs): `N x u32` ticks then `N x u32` zeros, not used by the step engine; one HP5 file has an arcade-style type 9 metadata chunk (`param2 = 0`).

## Quirks & pitfalls

- Ticks, lanes and items are three parallel arrays, not records.
- Skip rows with `lane = 0xFF` or item type `-1`.
- The style low byte sets the lane count; ignoring it mixes foot and hand charts.
- At equal ticks, resolve a freeze end before a new arrow on the same lane.

## Example

Hand-built for a single-foot chart with `N = 3` (tick 0 Left arrow, tick 1024 Right arrow, tick 2048 freeze end on Right):

```
ticks:  00000000  00040000  00080000      (i32 LE: 0, 1024, 2048)
lanes:  00 03 03  + 0 pad byte            (u8, padded to a dword)
items:  0000 0000 | 0000 0000 | 0000 0100 (i16 type, u16 param: (0,0), (0,0), (0,1))
```

## ROX support

Not read by ROX (no SSQ support).

## Parsers & tools

[`skogaby/ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (Rust): converts type 16 foot charts (`0x14` single, `0x18` double) to SSC / modern SSQ; drops hand and controller-variant charts with a warning.

## Getting samples

No sample: same situation as [`hudson-ssq`](../hudson-ssq/README.md) (no public extract; only multi-GB Wii disc images on archive.org). Dump a Hottest Party 4 or 5 (Wii) disc you own, extract the `.ssq` files with type 16 chart chunks and read them with [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools).

## Sources

- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/hudson_lane_ssq_format.md
- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/ssq_format.md
