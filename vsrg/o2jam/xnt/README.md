# KrazyRain chart (`.xnt`, signature "XNOT")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian), stored zlib-compressed inside `.snp`

## Overview

KrazyRain chart stored in a `.snp` archive (see the Packages section of the root README). Each `.xnt` comes with an `.xne` XML whose `tempo` attribute is the real BPM. Only Open2Jam `XNTParser.java` / `XNTChart.java` describe it; many bytes are unknown.

## Packaged in

- `.snp` (KrazyRain `VDISK1.0` archive: zlib-compressed `.xnt` charts, `.xne` XML files and OGG samples).

## Container & encoding
After inflating: 11-byte header `char[4] "XNOT"` (int `0x544F4E58`), `int16 unk1`, `int32 segments`, `byte unk2`. `segments == 3`: a BPM block comes first; otherwise only the two note blocks.

## Structure / metadata
Blocks in order: [BPM block (if segments==3)], key-sound note block, BGM note block, sample table. Each block starts with 12 unknown bytes then `int32 count`.

| Block | Event layout (14 bytes) |
|---|---|
| BPM | `byte zero; int16 measure; float32 position; 3 unknown bytes; float32 bpm` |
| Notes (and BGM) | `byte zero; int16 measure; float32 position; byte channel; int16 sample_id; float32 hold` |
| Sample table | `int32 count`, then `{int16 id; int16 unk; int32 name_len; char name[name_len]}` ; names point to files inside the SNP |

## Timing model
`measure` int16 + `position` float32 (fraction of the measure, 0..1). Initial BPM comes from the `.xne` `tempo` attribute (Open2Jam adds a BPM event at measure 0 position 0); later ones from the BPM block (`measure+position`). Measure length model: Unknown (Open2Jam treats measures like OJN).

## Notes
`channel` 1..7 = lanes 1..7 in the first (key) block; anything else logs unknown. The second block is BGM (autoplay). `hold > 0` is a hold note released at `measure + position + hold` (hold in measures; Open2Jam adds a release event at `(short)release` / `release - measure`); `hold == 0` is a tap. `sample_id` indexes the sample table.

## Audio & images
OGG files in the SNP, named in the sample table.

## Versions & variants
Unknown.

## Quirks & pitfalls

Many unknown fields. Metadata is external. The BPM in the XML is wrong; use `.xne`.

## Example
Unknown.

## ROX support
Not read by ROX.

## Parsers & tools
Open2Jam: https://github.com/open2jamorg/open2jam/blob/master/parsers/src/org/open2jam/parsers/XNTParser.java and XNTChart.java

## Getting samples

Committed: none. `.xnt` files live in KrazyRain `.snp` archives, which are not publicly distributed. Extract one from an installed game with Arrowgene.KrazyRain's `vdisk-extract` (https://github.com/sebastian-heinz/Arrowgene.KrazyRain, README); each `.xnt` comes with an `.xne` holding the tempo.

## Sources
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/XNTParser.java
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/XNTChart.java
