# Older DrumMania/GuitarFreaks sequences (`.dsq`, `.gsq`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview
`.dsq` (drums) and `.gsq` (guitar/bass) are the sequence files of the earliest Konami DrumMania/GuitarFreaks games; gitadora-customs has plugins for several generations (`dsq`, `dsq0`, `dsq05`, `dsq1`, `dsq15`, `dsq2`; `gsq`, `gsq1`, `gsq15`, `gsq2`, `gsq3`). Only the `dsq2` and `gsq` plugins were read; the generation split (which games) is Unknown.

## Container & encoding
dsq: optional 0x10 header with magic `DSQ1` (if present the tool skips 0x10 bytes), then 8-byte entries `<I B B H>`: `u32 timestamp; u8 command; u8 param1; u16 param2`. Time division 300, beat division 480 (hard-coded in the tool). The tool has no writer for dsq2.

## Structure / metadata
Command ids (drums, `plugins/dsq.py`): 0x00 hihat, 0x01 snare, 0x02 bass, 0x03 high tom, 0x04 low tom, 0x05 right cymbal, 0x06 auto-play; 0x07 measure, 0x08 beat, 0x09/0x0A/0x0C end position, 0x0B end of notes, 0x18..0x25 unknown. For a note: `param1` = volume, `param2` = sound id. gsq (guitar/bass) uses command ids 0x00/0x20/0x40/0x60 (note), 0x10 measure, 0xA0 end position and a note byte: 0x01..0x07 R,G,B combos (RGB-pattern as in DTX), 0x08 auto, 0x10 open.

## Timing model
Timestamp in 1/300 units; beat/measure events; BPM representation Unknown (not in the entries read).

## Notes
Drum lanes as listed; guitar lanes 3 buttons + open.

## Audio & images
Sound ids.

## Versions & variants
Many (dsq0, dsq05, dsq1, dsq15, dsq2, gsq1, gsq15, gsq2, gsq3), not documented here.

## Quirks & pitfalls
Unknown commands must be preserved.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
gitadora-customs plugins: https://github.com/fisyher/gitadora-customs/tree/master/plugins

## Getting samples
- **Committed / manifest: none.** No public `.dsq`/`.gsq` file found; gitadora-customs ships plugins (`dsq`, `dsq0`, `dsq05`, `dsq1`, `dsq15`, `dsq2`, `gsq`, `gsq1`, `gsq15`, `gsq2`, `gsq3`) but no test data.
- **How to get one**: extract from the data of the matching older GuitarFreaks/DrumMania game you own; the plugin names suggest one reader per game generation (which game maps to which is Unknown in the fiche). Convert with https://github.com/fisyher/gitadora-customs (`seqtool.py`). RAintN22/gitadora-tools (named in the game README) is another tool; only its releases were seen.

## Sources
- https://raw.githubusercontent.com/fisyher/gitadora-customs/master/plugins/dsq.py , dsq2.py , gsq.py
