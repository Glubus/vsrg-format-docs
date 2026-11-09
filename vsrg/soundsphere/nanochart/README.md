# NanoChart (`.nanochart`, rizu compact binary note stream)
Kind: chart

Doc status: complete (the whole format is a single Lua module) · ROX: no · Category: vsrg · Encoding: binary

## Overview

NanoChart is a **very compact binary encoding of a column chart's note events** used by the rizu / soundsphere engine (GitHub `semyon422/rizu`, `chart/transform/NanoChart.lua`): a chart is reduced to a flat list of `(time, press|release, input)` events with 1/1024 s time resolution, preceded by a version byte, a 16-byte chart hash and an input count. The repository spec says replay events and exported `.nanochart` files depend on it and that "NanoChart uses the current `byte` buffer API while preserving the existing version 1 and version 2 wire format", so changes must be covered by exact-byte fixtures. It carries **no BPM, no scroll velocity and no keysounds**: it is a note-skeleton (for example to preview or to verify a chart against a replay), not a playable chart.

## Container & encoding

Raw binary, byte-oriented, big-endian bit fields as drawn below. No compression. Extension `.nanochart` for exported files (also embedded in replay data [inference]).

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

Each event: `type` 1 = press, 0 = release (holds are a press followed by a release on the same input), `input` 1..255 (column index in the chart's input mode; inputs 13..255 use extended objects). Simultaneous events share one time via the same-time bit.

## Audio & images

None.

## Versions & variants

Version 1: delays 0..15 s only. Version 2: delays -8..7 s (allows slightly unordered times), the version the encoder writes.

## Quirks & pitfalls

- The time of a start object applies to **following same-time objects** until the next start object.
- The encoder truncates times to 1/1024 s.
- Input 0 means "time marker only".
- In version 2 a delay nibble > 7 is negative (`delta - 16`), in version 1 it is unsigned.
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

Not read by ROX. It lacks BPM/SV/keysounds that ROX stores; at best it could be turned into a hold/tap skeleton with a constant-tempo assumption.

## Parsers & tools

rizu (Lua): https://github.com/semyon422/rizu (`chart/transform/NanoChart.lua`, test `NanoChart_test.lua`).

## Sources

- https://github.com/semyon422/rizu (commit `37df09654581800fa30df613385080b99c795c9a`): `chart/transform/NanoChart.lua`, `chart/transform/NanoChart_test.lua`, `chart/spec.md`
