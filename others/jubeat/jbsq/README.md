# JBSQ (`.jbsq`, jubeat binary sequence)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (little-endian, fixed 96-byte header + 8-byte events)

## Overview

Compiled binary form of the [`.eve`](../eve/README.md) event list of Konami's jubeat games: the same six commands (tap, long note, tempo, measure line, beat line, end) and 300 Hz time base, packed as 8-byte records after a header that also stores max combo, end time, the buttons lit at the start and a 60-bar density graph. The layout below is the `construct` definition from jubeatools (`konami/jbsq/construct.py`); the loader maps each event onto the same internal model as `.eve`. `jubeat plus` charts in `.jbt` archives are described in the Reflec Beat/iOS page (encrypted zip entries `seq_*`; "notes are assumed to be encoded the same way as their arcade counterparts" per SaxxonPike).

Category: others, see [../README.md](../README.md).

## Container & encoding

Little-endian binary, no compression. Magic is one of `IJBQ`, `IJSQ` or `JBSQ` (ASCII, 4 bytes). One file per difficulty; jubeatools loads `*.jbsq` from a folder and guesses the difficulty from the last three characters of the file stem (`bsc`/`adv`/`ext`, case-insensitive), default EXTREME.

## Structure / metadata

### Header (96 bytes)

| Offset | Type | Field |
|---|---|---|
| 0 | 4 bytes | magic: `IJBQ` \| `IJSQ` \| `JBSQ` |
| 4 | u32 | `num_events` |
| 8 | u32 | `combo` (max combo) |
| 12 | u32 | `end_time` (ticks) |
| 16 | 2 bytes | padding |
| 18 | u16 | `starting_buttons` (bitmask of panels lit at start) |
| 20 | u32 | `start_time` (ticks) |
| 24 | 12 bytes | padding |
| 36 | 60 × u8 | `density_graph` |
| 96 | `num_events` × 8 bytes | events |

### Event (8 bytes)

| Offset | Type | Field |
|---|---|---|
| 0 | u8 | type: `PLAY` = 1, `END` = 2, `MEASURE` = 3, `HAKU` = 4, `TEMPO` = 5, `LONG` = 6 |
| 1 | u24 LE | time in ticks (300 per second) |
| 4 | u32 LE | value (same meaning as `.eve`: panel 0–15 for PLAY, packed long-note word for LONG, `6·10⁷/BPM` for TEMPO, 0 otherwise) |

See `.eve` for the LONG packing (position 4 bits, direction 2, length 2, duration in ticks).

## Timing model

`seconds = ticks / 300`; `BPM = 6·10⁷ / value`; `MEASURE`/`HAKU` are guide lines. `start_time`/`end_time` bound the playable range.

## Notes

`PLAY` and `LONG` only, as in `.eve`.

## Audio & images

Unknown.

## Versions & variants

jubeatools accepts three magics (`IJBQ`, `IJSQ`, `JBSQ`); which game/version uses which is not stated in the sources opened. Command ids differ from the order jubeatools uses for `.eve`.

## Quirks & pitfalls

- The 24-bit time field limits the range to 16 777 215 ticks ≈ 15.5 hours.
- Header padding bytes are unknown (possibly meaningful in real files).
- Command ids differ from the `.eve` enum order.
- `density_graph` and `combo` should be recomputed when writing a chart.

## Example

No real file opened. Hand-built from the struct: an event `PLAY` at tick 150 on panel 5 is the 8 bytes `01 96 00 00 05 00 00 00`.

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

[Stepland/jubeatools](https://github.com/Stepland/jubeatools) (`construct`-based loader/dumper).

## Getting samples

Committed: none. No `.jbsq` is public (jubeatools ships only the Kaitai description `jbsq.ksy`); no synthetic binary was written because the 96-byte header has padding of unknown content. jubeatools can write `.jbsq` from other formats. Originals are arcade data; jubeat plus `.jbt` archives hold encrypted `seq_*` entries (<https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/jbt-rb-orb.md>).

## Sources

- <https://raw.githubusercontent.com/Stepland/jubeatools/master/jubeatools/formats/konami/jbsq/construct.py> and `load.py` (read)
- <https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/jbt-rb-orb.md> (iOS packages, read)
