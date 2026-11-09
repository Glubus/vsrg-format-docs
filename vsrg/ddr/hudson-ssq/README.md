# Hudson SSQ type 9 step chunk (DDR Mario Mix / Hottest Party 1, Wii/GameCube)
Kind: chart

Doc status: complete (as reverse engineered) · ROX: no · Category: vsrg · Encoding: binary (little-endian chunk inside an `.ssq`)

## Overview

Hudson Soft's Nintendo ports of DDR (Mario Mix, GameCube; Hottest Party 1, Wii) keep charts in a type 9 chunk of the [`.ssq`](../ssq/README.md) container instead of type 3. Type 9 is type 3 plus per-arrow "chara note" (gimmick item) references and a trailing extra-data block ("Koopa" double arrows, "Spiny" hazards, Wii Remote "hand" markers). The layout comes from skogaby's reverse engineering of the Hottest Party 1 main DOL (`ddr-chart-tools/docs/hudson_ssq_format.md`), verified against 52 songs / 211 charts. HP4/HP5 use the [type 16 lane format](../hudson-ssq-lane/README.md).

The arcade type 9 song metadata chunk (see [`../ssq`](../ssq/README.md), section 8 of the upstream spec) is a different chunk: a Hudson step chunk has a valid step difficulty code in `param2`, the metadata chunk does not.

## Container & encoding

Little-endian (the PowerPC game byte-swaps on load). Dword-aligned chunk in an SSQ file (12-byte header, chunks walked by `length`, `00 00 00 00` terminator), see [`../ssq`](../ssq/README.md). The source does not say how SSQ files are stored on the disc (the type 16 doc mentions `ssq/GIMMICK/%s.bin` for HP4/HP5).

## Structure / metadata

### Chunk header (12 bytes, as every SSQ chunk)

| Offset | Type | Field |
|---|---|---|
| +0x00 | u32 | chunk length (dword-aligned) |
| +0x04 | u16 | type = `9` |
| +0x06 | u16 | `param2` = difficulty code, same encoding as type 3 (high byte slot: `01` Basic, `02` Difficult, `03` Expert, `04` Beginner, ...; low byte style, e.g. `0x14` single) |
| +0x08 | u16 | `param3` = row count `N` |
| +0x0A | u16 | `param4` = unused (0) |

### Body

| Offset | Type | Field |
|---|---|---|
| +0x0C | u32 | `extra_offset`: offset of the extra block, relative to chunk start + 0x10; 0 = no extra block |
| +0x10 | N x i32 | row time offsets in measure ticks (4096 per measure), as type 3 |
| ... | variable | N row records, packed with no padding between them |
| ... | 0-3 bytes | pad to the next dword |

### Row record

One mask byte followed by zero or more item bytes:

- mask != 0: a step row. One item byte follows per set bit of the mask, lowest bit first. Item byte `0` = plain arrow; `k >= 1` = entry `k` (1-based) of the `CHAR` table.
- mask == 0: a freeze-end row. No item bytes follow; its data is the next entry of the `FREZ` table.

Mask bit layout = type 3 panel layout (bit 0 P1 Left, 1 Down, 2 Up, 3 Right, 4-7 the same for P2). The Hottest Party engine builds notes only from the low nibble.

### Extra block (`EXDT`)

At `chunk start + 0x10 + extra_offset`:

| Offset | Type | Field |
|---|---|---|
| +0x00 | 4 bytes | magic `EXDT` (not validated by the game) |
| +0x04 | u32 | block length including this 8-byte header |
| +0x08 | ... | sub-blocks |

Each sub-block is `{ 4-byte ASCII magic, u32 length including its 8-byte header, payload }`. The game walks them by length and looks them up by magic. Defined: `CHAR` and `FREZ`; either can be absent.

`CHAR` (chara note table): `(length - 8) / 12` entries of 12 bytes:

| Offset | Type | Field |
|---|---|---|
| +0 | u16 | item type (table below) |
| +2 | u16 | unused |
| +4 | i32 | parameter 1 (always 0 on HP1) |
| +8 | i32 | parameter 2 (always 0 on HP1) |

`FREZ` (freeze-end table): one fixed 3-byte entry per freeze-end row, in row order: `u8 panel mask` of the freezes that end here, `u8 kind` (always 1, ignored by the game), `u8 item byte` (ignored). A freeze end closes, for each bit of its mask, the most recent earlier note on that panel in the game's note list. That list is in row order, with item-2 echo notes appended right after the row that created them.

## Timing model

As standard SSQ: measure ticks (4096 per whole note) converted through the type 1 tempo chunk (`time_offset[]` / `tempo_data[]`, per-file ticks-per-second). See [`../ssq`](../ssq/README.md).

## Notes

Rows hold freeze heads (arrow rows), freeze ends (mask 0 rows resolved through `FREZ`) and gimmick items:

| Item type | Hottest Party meaning | With gimmicks off |
|---|---|---|
| 0 (none), 3, 4, 7, 9, 10, 11, others | assorted gimmick arrows | normal arrow |
| 1 | Wii Remote "hand" marker (Left/Right panels only) | normal arrow |
| 2 | "Koopa" double arrow | normal arrow plus an echo arrow on the same panel 1024 ticks (one beat) later, at most 2 echoes per row |
| 5, 14 | hazard ("Spiny"), mine-like | removed |

With Groove Gimmick off and hand markers off, every arrow becomes a normal step except the removals above. Freezes are kept whatever item their head carries; a freeze whose end resolves to a removed hazard note disappears with it. With hand markers on, an item-1 arrow on panel 0 or 3 becomes a hand-only note (no foot arrow). The option gates are per-player option word bit 29 (hand markers) and the per-player Groove Gimmick flag. With gimmicks on, item types `{2, 3, 4, 5, 7, 9, 14}` keep their behaviour.

## Audio & images

Separate game assets.

## Versions & variants

Mario Mix (GameCube) and Hottest Party 1 (Wii): type 9. Hottest Party 4/5: type 16 ([`../hudson-ssq-lane`](../hudson-ssq-lane/README.md)).

## Quirks & pitfalls

- Rows are variable-length: read the mask first. Mask 0 consumes no item bytes.
- `extra_offset` is relative to chunk start + 0x10, not +0x0C where the field lives.
- Item-2 echo notes sit in the note list right after their row, which matters when resolving `FREZ` ends.
- Verified only on Hottest Party 1; the source lists no Mario Mix usage beyond its introduction.

## Example

Hand-built from the row rules for `N = 2` (plain Left arrow, then a freeze end):

```
mask 0x01, item 0x00      -> P1 Left plain arrow          (2 bytes)
mask 0x00                 -> freeze end (1st FREZ entry)  (1 byte)
```

## ROX support

Not read by ROX (no SSQ support). Conversion would drop gimmick items or map them to taps/mines.

## Parsers & tools

[`skogaby/ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (Rust): converts Hudson/legacy SSQs into SSC or modern SSQ (gimmicks off).

## Getting samples

No sample committed: no chart extract is public and archive.org (searched 2026-11-09) has only multi-GB Wii/GameCube disc images (e.g. `ddr-ffp-wii` 1.8 GB, `dance-dance-revolution-disney-grooves-wii` 862 MB). The tests of [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (`tests/hudson_legacy_to_ddr.rs` ...) build their data in code. To get charts: dump a Hottest Party 1 (Wii) or Mario Mix (GameCube) disc you own, locate the song `.ssq` files (type 9 step chunks) and parse them with `ddr-chart-tools`. Container: standard SSQ ([`../ssq`](../ssq/samples/SOURCES.md)).

## Sources

- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/hudson_ssq_format.md (commit `a733404f43427bfc7b9dea3cae67710149767993` of the cloned repo)
- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/ssq_format.md
