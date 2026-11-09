# DTXMania older chart format (`.gda`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text

## Overview
`.gda` is an older text chart format for GuitarFreaks/DrumMania that DTXMania can still load (original README: "`.gda`/`.g2d`: DTXMania chart (older format)"). The only authoritative description found is the DTXMania loader: `CDTX.tRead` sets `EType.GDA` for the `.gda` extension and then parses it with the normal DTX line parser, but replaces the 2-hex-digit channel with a 2-letter/2-digit channel name looked up in a table. Community note: the GDAmania blog converted its GDA charts to DTX ("Changed all format to DTX files"). Origin of the name/layout beyond that: Unknown.

## Container & encoding
Text lines `#mmmcc: objects` as in [DTX](../dtx/README.md) (3-char measure number, 2-char channel, base-36 objects) [inference: shared parser path `tInput_LineAnalysis_ChipLocation`]. Charset: Unknown (probably Shift_JIS).

## Structure / metadata
Channel string -> DTX channel (`STGDAPARAM` table in `CDTX.cs`; also `DTXCreator CDTXInputOutput`):

| GDA | DTX channel | | GDA | DTX channel |
|---|---|---|---|---|
| TC | 03 BPM | | HH | 11 hi-hat close |
| BL | 02 bar length | | SD | 12 snare |
| GS | 29 guitar flowspeed (unused) | | BD | 13 bass drum |
| DS | 30 drum flowspeed (unused) | | HT | 14 high tom |
| FI | 53 fill-in | | LT | 15 low tom |
| CY | 16 cymbal | | G0 | 20 guitar open |
| G1..G7 | 21..27 guitar chords (B, G, GB, R, RB, RG, RGB) | | B0 | A0 bass open |
| GW | 28 guitar wailing | | B1..B7 | A1..A7 bass chords |
| 01..09, 0A..0F, 10..1F, 20 | SE01..SE32 (channels 61-69, 70-79, 80-89, 90-92) | | BW | A8 bass wailing |

Header commands, resource tables (`#WAV`, ...) are assumed the same as DTX (Unknown whether GDA headers differ).

## Timing model
Same as DTX when parsed by DTXMania: 384 ticks per measure, BL = bar length, TC = tempo. See [dtx](../dtx/README.md).

## Notes
Lanes: drums HH, SD, BD, HT, LT, CY (6 drum lanes, no floor tom/ride/open HH in the table: [inference] the original arcade GF/DM 1st-3rd gen), guitar and bass 3 buttons + open + wailing.

## Audio & images
Unknown (same `#WAVzz` mechanism if parsed as DTX).

## Versions & variants
`.g2d`: see [g2d](../g2d/README.md). 

## Quirks & pitfalls
The original GDA spec is not available publicly in what I could fetch; behaviour is known only through DTXMania's code.

## Example
No real GDA sample available; a hand-written one built from the loader table is in [samples/](samples/SOURCES.md).

## ROX support
Not read by ROX.

## Parsers & tools
DTXmaniaNX CDTX.cs and DTXCreator `CDTXInputOutput.cs` (https://github.com/limyz/DTXmaniaNX).

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): one hand-written `synthetic-drums-guitar-bass.gda`, built from the loader's `STGDAPARAM` table (`CDTX.cs`); it demonstrates what DTXMania accepts, not a real GDA file.
- **No real file found**: no repository, spec or open archive with a `.gda` was reachable. The GDAmania blog converted its charts to DTX (fiche), so the originals are gone from that source.
- **How to get more**: the DrumGamer site lists "GDA Creator 2 English Version" ("Editor for GDA, DTX and BMS files", https://drumgamer.weebly.com/tools2.html) and the simulator DigiBand ("Supports GDA and DTX files", https://drumgamer.weebly.com/simulators.html): a GDA can be written with GDA Creator 2 [inference: it is an editor for the format by its description]. DTXMania itself loads `.gda` (and `.g2d`), see [dtx](../dtx/README.md).

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
- http://gdamania.blogspot.com/ (GDA to DTX conversion project)
