# NanoChart (`.nanochart`, rizu compact binary note stream)
Kind: chart

Doc status: complete (the whole format is a single Lua module) · ROX: no · Category: vsrg · Encoding: binary

## Overview

NanoChart is a compact binary encoding of a column chart's note events in the rizu engine (`semyon422/rizu`, `chart/transform/NanoChart.lua`): a version byte, a 16-byte chart hash, an input count, then a flat list of `(time, press|release, input)` events with 1/1024 s resolution. Replay events and exported `.nanochart` files depend on it; the repository spec requires exact-byte fixtures for the version 1 and 2 wire formats. It has no BPM, scroll velocity or keysounds, so it is a note skeleton (preview, replay verification), not a playable chart.

## Container & encoding

Raw binary, big-endian bit fields as drawn below, no compression. Extension `.nanochart` (also embedded in replay data [inference]).

## Structure / metadata

Header (18 bytes):

| Offset | Size | Field |
|---|---|---|
| 0 | u8 | `version` (1 or 2; the encoder writes **2**) |
| 1 | 16 bytes | chart `hash` (raw bytes; the encoder asserts exactly 16 bytes) |
| 17 | u8 | `inputCount` ("need to convert to keys only") |

Then a sequence of **objects** until end of data. The first nibble of the first byte selects the object kind:

**Start object** (2 bytes; `input` nibble 1..12, or 0 for a pure time marker):

```
iiii t s nn nnnnnnnn   byte 0: iiii = input 1..12 (0 = no object, defines time only), t = 1 press / 0 release (0x08),
                                s = same-time bit = 0 (0x04), nn = high 2 bits of the time numerator
                       byte 1: low 8 bits; numerator = 10 bits, n/1024 s within the current second offset
```

**Next object, same time** (1 byte, input 1..12, same-time bit set):

```
iiii t s 00   iiii = input 1..12, t = 1 press / 0 release, s = 1 (same time as the previous object), low 2 bits unused
```

**Extended object** (2 bytes; first nibble `1111` = 15, input 13..255 in the second byte). As written by `encodeNote` (`0xf0 + (type << 3) + same_time_bit`, then the input byte):

```
1111 t s 00   byte 0: t = 1 press / 0 release (bit 0x08), s = same-time bit (0x04)
iiii iiii     byte 1: input = 13..255
```

(The in-source comment draws the object as `1111 .... .... ....` with the input in the low byte; the encoder/decoder code above is authoritative.)

For input > 12 the encoder first emits a start object with input 0 to define the time when the time differs ("use 0-input object to define time").

**Delay object** (1 byte): `1110 dddd`, `dddd` = delay in whole seconds added to the running **second offset**: unsigned 0..15 in version 1, **signed -8..7** (two's complement of the nibble) in version 2. Long gaps are emitted as repeated delay objects.

Decoding algorithm (`NanoChart:decode`): keep `offset` (integer seconds) and `noteTime` (current 10-bit fraction); for each byte, `input = byte >> 4`: if 14, add the delay; if 15, emit a note at `offset + noteTime/1024` with type bit `0x08` and the following byte as input; otherwise read `type = (byte & 8) >> 3`, `same = byte & 4`; if not `same`, `noteTime = ((byte & 3) << 8) | nextbyte`; if `input ~= 0`, emit a note `{time = offset + noteTime/1024, type, input}`.

## Timing model

Absolute time in **seconds**: integer part accumulated by delay objects (up to 15 s, or -8..+7 s in version 2), fractional part is `n/1024` (about 1 ms resolution, floored by the encoder: `floor(time * 1024)`). There is no tempo information.

## Notes

`type` 1 = press, 0 = release (a hold is a press then a release on the same input). `input` 1..255 is the column index (13..255 use extended objects). Simultaneous events share one time via the same-time bit.

## Audio & images

None.

## Versions & variants

Version 1: delays 0..15 s. Version 2 (written by the encoder): delays -8..7 s.

## Quirks & pitfalls

- A start object's time applies to the following same-time objects until the next start object.
- The encoder truncates times to 1/1024 s.
- Input 0 means time marker only.
- Version 2 delay nibble > 7 is negative (`delta - 16`); version 1 is unsigned.
- The hash is raw 16 bytes, not hex.

## Example

From the repository's own test (`NanoChart_test.lua`, exact bytes of single objects):

```
encodeNote(input 1,   release, new time, t = 0.125)  -> 10 80
encodeNote(input 12,  press,   same time)            -> cc
encodeNote(input 128, release, new time, t = 1/128)  -> 00 08 f0 80
encodeNote(input 128, release, same time)            -> f4 80
```

(Here the call argument `0` = release and `1` = press, matching `bit.lshift(note_type, 3)`.)

## ROX support

Not read by ROX, on purpose (2026-11-10): the stream has no tempo, no audio and no keysounds, and the only genuine file is the rizu test vector (every other sample is a re-encoding), so a reader would invent a tempo for notes nothing plays; the `.sph` chart it is derived from is read.

## Parsers & tools

rizu (Lua): https://github.com/semyon422/rizu (`chart/transform/NanoChart.lua`, test `NanoChart_test.lua`).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md); the real-chart files were written by a Python port of `NanoChart:encode` (decoded back and compared), not by rizu.

The real exporter (`rizu/editor/exports/NanoChartExporter.lua`, read at commit `cf4603379dcab949d3510b8c31d1d3e421df6ec0`) writes `<chart path>.nanochart` with version 2, an all-zero 16-byte hash, `inputCount` = key count and only key press events (taps and hold starts, `type = 1`), sorted by time then input. Next to it go a zlib-compressed `<path>.nanochart_compressed` and `.preview0/.preview1` (plus `_compressed`) SPH previews. A genuine export needs the rizu editor (https://github.com/semyon422/rizu): open a chart and export. No genuine export is published in any repository or CDN reached (`semyon422/soundsphere` is the same tree as rizu; `sphere`/`sphlib` repos need authentication).

## Sources

- https://github.com/semyon422/rizu (commit `37df09654581800fa30df613385080b99c795c9a`): `chart/transform/NanoChart.lua`, `chart/transform/NanoChart_test.lua`, `chart/spec.md`
