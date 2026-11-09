# GuitarFreaks/DrumMania sequence (`.sq2`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview
Sequence format of the GuitarFreaks & DrumMania generation before GITADORA (`d<id>.sq2` drums, `g<id>.sq2` guitar/bass in the gitadora-customs writer). Source: `fisyher/gitadora-customs` `plugins/sq2.py` only.

## Container & encoding
Same two-level container as [sq3](../sq3/README.md): `SEQP` archive header (archive size @0x0C, header size @0x0C of the chunk header, music id @0x14, chart count @0x18, charts from 0x20) with `SEQT` chunk headers (0x20 bytes: header size @0x0C, entry count @0x10), but entries are 0x10 bytes and time division is fixed at 300.

## Structure / metadata
Entry (16 bytes), as read by the tool: `u32 timestamp @0; u8 note flags @4; u8 event id @5; u32 @8; u8 @0x0C; u8 @0x0D`. Event ids: 0x00 note, 0x01 auto note, 0x10 bpm (u32 @8 = microseconds per beat; BPM = 60000000/value), 0x20 barinfo (numerator @0x0C, log2 denominator @0x0D). Note entries: sound id u16 @8, u16 unknown @0x0A, volume @0x0C; `flags@4 & 0x0F` = lane (tables as in the DTX-oriented plugin: drums as sq3, guitar/bass 3-button codes), `& 0x10` = open note, `& 0x20` = wail.

## Timing model
Timestamp in 1/300 units; BPM events in microseconds per beat; no beat field (unlike sq3).

## Notes
Lanes per note flags. No hold durations in the entry layout the tool reads [inference].

## Audio & images
Sound ids (u16).

## Versions & variants
sq3 has 64-byte entries with an explicit beat field. Earlier: `.dsq`/`.gsq` ([dsq](../dsq/README.md)).

## Quirks & pitfalls
Open note = bit 0x10 of the flag byte; the tool preserves the unknown u16 at 0x0A.

## Example
Unknown.

## ROX support
Not read by ROX.

## Parsers & tools
gitadora-customs `plugins/sq2.py`: https://github.com/fisyher/gitadora-customs

## Getting samples
None committed: no public `.sq2` or test data found (gitadora-customs holds only `plugins/sq2.py`).

To get one: extract GuitarFreaks & DrumMania V-series/XG data you own; `fisyher/gitadora-customs` reads `.sq2` (front end `seqtool.py`, see [sq3](../sq3/README.md#getting-samples)). Whether DTX can be written to `.sq2` is unchecked (the README lists "DTX (input, output)" generally).

## Sources
- https://raw.githubusercontent.com/fisyher/gitadora-customs/master/plugins/sq2.py
