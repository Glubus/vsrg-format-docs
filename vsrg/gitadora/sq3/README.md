# GITADORA sequence (`.sq3`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview
Chart archive of the GITADORA arcade games (names like `d<musicid>.sq3`/`g<musicid>.sq3`, one file per music id, containing the difficulty charts of one instrument family). Read and written by `fisyher/gitadora-customs` (`plugins/sq3.py`), whose code is the only source used: field semantics marked "unk" are unknown to it. A game never ships charts as plain files: they are extracted from the game's IFS archive.

## Container & encoding
Little-endian binary, two-level container: `SEQP` archive header (0x20 bytes) followed by N chart chunks. Detection (`is_format`): bytes 0..3 = `SEQP`, byte 0x36 = 3, bytes 0x30..0x33 = `SQ3T`.

SEQP header:

| Offset | Size | Field |
|---|---|---|
| 0x00 | 4 | `"SEQP"` |
| 0x04 | 1 | 1 (writer) |
| 0x06 | 1 | 1 (writer) |
| 0x0A | 1 | 3 (version?) |
| 0x0C | 4 | archive size = 0x20 + 0x30*N + sum(entry data) |
| 0x10 | 4 | data offset (0x20 = header size) |
| 0x14 | 4 | music id |
| 0x18 | 4 | number of charts N |
| 0x1C | 4 | 0x12345678 (writer constant) |

Then per chart: 16-byte chunk header `{u32 size (= entry data length + 0x30); byte@4 = 0x10; rest zero}` followed by the SQ3T header (0x20) and the entries; next chunk at `offset + size`.

## Structure / metadata
SQ3T header (0x20 bytes):

| Offset | Size | Field |
|---|---|---|
| 0x00 | 4 | `"SQ3T"` |
| 0x06 | 1 | 3 |
| 0x0A | 1 | 3 |
| 0x0C | 4 | header size (0x20) |
| 0x10 | 4 | entry count |
| 0x14 | 1 | `unk_sys` (unknown) |
| 0x15 | 1 | `is_metadata` (0 = note chart, 1 = metadata chart: bpm/measure/bar events; 2 exists, unknown, skipped by the tool) |
| 0x16 | 1 | difficulty (meaning not decoded in the tool; per chart order) |
| 0x17 | 1 | game type: 0 drum, 1 guitar, 2 bass |
| 0x18 | 2 | time_division (300) |
| 0x1A | 2 | beat_division (480) |
| 0x1C | 4 | entry size (0x40) |

Entry (0x40 bytes):

| Offset | Size | Field |
|---|---|---|
| 0x00 | 4 | timestamp (units of 1/`time_division`, i.e. 1/300 per time unit; the tool labels `timestamp/300` "timestamp_ms" [unit: Unknown, probably seconds*300]) |
| 0x04 | 1 | event id |
| 0x08 | 4 | note: hold duration (0 = tap) |
| 0x10 | 4 | beat position (in `beat_division` units, 480 per quarter note [inference]) |
| 0x14 | 4 | unknown (0x16C default) |
| 0x20 | 4 | note: sound id |
| 0x24 | 4 | note: note length (guitar/bass; default 0x40) |
| 0x2D | 1 | note: volume |
| 0x2E | 1 | note: auto volume |
| 0x30 | 1 | note: lane/note id (tables below) |
| 0x31 | 1 | note: wail direction (0/1 up, 2 down; alternates 0/1 in repeated wails) |
| 0x32 | 1 | note: guitar special bitmask (1 wail, 2 hold) |
| 0x34 | 1 | note: auto-note flag (1 = auto-play sound, note id forced to "auto"); bpm event: u32 = microseconds per beat (BPM = 60000000 / value); barinfo: u8 numerator @0x34, u8 log2(denominator) @0x35 |

Event ids: 0x01 bpm, 0x02 barinfo (time signature), 0x03 bar line on, 0x04 bar line off, 0x05 measure, 0x06 beat, 0x07 chip start, 0x08 chip end, 0x0C unknown (metadata chart), 0x0E start position, 0x0F end position, 0x10 note.

Note id (0x30): drums 0 hihat, 1 snare, 2 bass, 3 high tom, 4 low tom, 5 right cymbal, 6 left cymbal, 7 floor tom, 8 left pedal, 0xFF auto. Guitar/bass (5-button): 0 open, then a 5-bit mask over R,G,B,Y,P combinations: 1 R, 2 G, 3 RG, 4 B, 5 RB, 6 GB, 7 RGB, 8 Y, ..., 0x0F RGBY (0x08..0x0F add Y, 0x10..0x17 add P without Y, 0x18..0x1F with Y and P; the table is `g_`/`b_` + `rgbyp` pattern in the source), 0xFF auto.

## Timing model
Time = timestamp (fixed time base) and beat position both stored per event: the chart carries both absolute time and a musical position; BPM events give microseconds per beat; time signature events set bar length; measures are marked by measure events (0x05). A converter to DTX takes the beat/ measure to place chips (gitadora-customs "SQ3 -> JSON -> DTX"). Exact quantization: Unknown.

## Notes
Drums: single hits. Guitar/bass: fret chords, open, wail (bit 1 of 0x32), hold (bit 2), hold duration at 0x08 (ticks of the time base). Auto-play notes carry the backing sounds. Bonus notes (kicks of bonus effect) are marked via a separate `.evt`/event file in other tools (`bonus_note` flag in the JSON; the .evt format is outside this page). Simultaneous notes share a timestamp.

## Audio & images
Sound ids refer to keysounds in the song's audio archive (sound id per note; format not covered here).

## Versions & variants
SEQP archive version 3 (SQ3T flags 3). Older games: [sq2](../sq2/README.md), [dsq](../dsq/README.md).

## Quirks & pitfalls
Time unit ambiguity; metadata charts are separate chart chunks; unknown 0x14/0x0C fields should be preserved when rewriting.

## Example
Not provided (no sample available; extracted game data cannot be redistributed).

## ROX support
Not read by ROX.

## Parsers & tools
- gitadora-customs (Python, `seqtool.py`): https://github.com/fisyher/gitadora-customs
- gitadora-tools: https://github.com/RAintN22/gitadora-tools

## Sources
- https://raw.githubusercontent.com/fisyher/gitadora-customs/master/plugins/sq3.py
- https://github.com/fisyher/gitadora-customs (README)
