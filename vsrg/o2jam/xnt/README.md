# KrazyRain chart (`.xnt`, signature "XNOT")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian), stored zlib-compressed inside `.snp`

## Overview
Chart file of KrazyRain, stored inside a [`.snp`](../snp/README.md) archive (see there for decompression). Each `.xnt` is accompanied by an `.xne` XML file whose `tempo` attribute is the real BPM. Only the Open2Jam `XNTParser.java` / `XNTChart.java` describe it; many bytes are "junk"/unknown to that parser.

## Packaged in

- Packaged in [`snp`](../snp/).

## Container & encoding
After inflating: header of 11 bytes: `char[4] "XNOT"` (int `0x544F4E58`), `int16 unk1`, `int32 segments`, `byte unk2`. `segments == 3` means a BPM block comes first; otherwise only the two note blocks.

## Structure / metadata
Blocks in order: [BPM block (if segments==3)], key-sound note block, BGM note block, sample table. Each block starts with 12 unknown bytes then `int32 count`.

| Block | Event layout (14 bytes) |
|---|---|
| BPM | `byte zero; int16 measure; float32 position; 3 unknown bytes; float32 bpm` |
| Notes (and BGM) | `byte zero; int16 measure; float32 position; byte channel; int16 sample_id; float32 hold` |
| Sample table | `int32 count`, then `{int16 id; int16 unk; int32 name_len; char name[name_len]}` ; names point to files inside the SNP |

## Timing model
`measure` int16 + `position` float32 (fraction of the measure, 0..1); BPM initial from the `.xne` `tempo` attribute (Open2Jam adds a BPM event at measure 0 position 0), later BPM events from the BPM block (`measure+position`). Measure length model: Unknown (Open2Jam treats measures like OJN).

## Notes
`channel` 1..7 = lanes 1..7 for the first (key) block, anything else logs unknown; second block is BGM (autoplay). `hold > 0` = hold note whose release is at `measure + position + hold` (hold expressed in measures; Open2Jam adds a release event at `(short)release` / `release - measure`); `hold == 0` = tap. `sample_id` refers to the sample table.

## Audio & images
Samples are OGG files in the SNP, named in the table.

## Versions & variants
Unknown.

## Quirks & pitfalls
Many unknown fields; metadata external to the file; BPM in the XML wrong, use `.xne`.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
Open2Jam: https://github.com/open2jamorg/open2jam/blob/master/parsers/src/org/open2jam/parsers/XNTParser.java and XNTChart.java

## Getting samples
- **Committed: none (no real file found).** `.xnt` charts live inside `.snp` archives of KrazyRain, which are not publicly distributed (see [snp](../snp/README.md#getting-samples)).
- **How to get one**: extract an `.snp` of an installed KrazyRain with Arrowgene.KrazyRain's `vdisk-extract` (https://github.com/sebastian-heinz/Arrowgene.KrazyRain, README); inside, each `.xnt` comes with an `.xne` XML holding the tempo. Open2Jam's `XNTParser.java` reads them.

## Sources
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/XNTParser.java
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/XNTChart.java
