# DTXMania older chart format (`.gda`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text

## Overview
`.gda` is an older text chart format for GuitarFreaks/DrumMania that DTXMania can still load (original README: "`.gda`/`.g2d`: DTXMania chart (older format)"). The only authoritative description found is the DTXMania loader: `CDTX.tRead` sets `EType.GDA` for the `.gda` extension and then parses it with the normal DTX line parser, but replaces the 2-hex-digit channel with a 2-letter/2-digit channel name looked up in a table. Community note: the GDAmania blog converted its GDA charts to DTX ("Changed all format to DTX files"). Origin of the name/layout beyond that: Unknown.

## Container & encoding
Text lines `#mmmcc: objects` as in [DTX](../dtx/README.md) (3-char measure number, 2-char channel, base-36 objects) [inference: shared parser path `tInput_LineAnalysis_ChipLocation`; confirmed by real files, e.g. `#002G2:0001` in samples/mitchi_Happy_man_BSC.gda]. Charset [observed in samples/*.gda]: Shift_JIS (CP932) with CRLF in most real files (Japanese `#TITLE`/`#ARTIST`, e.g. samples/nari_konan.gda), some pure ASCII (samples/BLAST_model_dd5_hell.gda); no BOM. Header lines are `#KEY value` with a **space** instead of a colon (`#TITLE HAPPY MAN BASIC`, `#BPM 180`, `#BASEBPM 0`, `#DLEVEL 0`, `#GLEVEL 18`, `#BLEVEL 0`, `#PREVIEW Happy manpre.wav`, `#WAV02 Happy man.wav`) while data lines use a colon; the first line is usually a comment written by the editor (`;Created by GDA Creator Professional Ver.0.14`, `...Ver.0.16`, `...Ver.0.22`, `;Created by GDA Creator Ver.1.25 Rev.Final`).

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

Header commands and resource tables (`#WAV`, `#BPM`, `#DLEVEL` ...) are the same as DTX [observed in samples/*.gda]. Tempo: `#BPM` with an initial value (180, 124, 300, 161.00) or `#BPM 0` plus a `TC` data line (samples/KOUICHI_hurukawa.gda, samples/nari_konan.gda). Drum files use the channels `BD CY HH HT LT SD` only; guitar/bass files use `G0`(open, samples/mitchi_YOU_CAN'T_EXT(OPEN).gda), `G1`..`G7`, `GW`; a difficulty = one file (`... BSC/ADV/EXT.gda`) grouped by [set.def](../set-def/README.md) (`#L1FILE: bas.gda`).

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
Real excerpt, samples/mitchi_Happy_man_BSC.gda (CP932, CRLF): `;Created by GDA Creator Professional Ver.0.14` / `#TITLE HAPPY MAN BASIC` / `#ARTIST ...` / `#BPM 180` / `#GLEVEL 18` / `#WAV02 Happy man.wav` / `#002G2:0001` / `#002G4:0100` / `#003G1:0100000000000000`. A hand-written file built from the loader table is also in [samples/](samples/SOURCES.md).

## ROX support
Not read by ROX.

## Parsers & tools
DTXmaniaNX CDTX.cs and DTXCreator `CDTXInputOutput.cs` (https://github.com/limyz/DTXmaniaNX).

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): 18 real `.gda` charts of community packs from the archive.org item "Rare DTX&GDA Simfile Collection" (`raredtxgda`): guitar/bass charts (mitchi `HAPPY MAN` BSC/ADV/EXT, `YOU CAN'T DO IT` BSC/ADV/EXT plus the BASS and OPEN variants), drum charts (BLAST `konoko`, `MODEL DD5`, KOUICHI, nari) and two GUNDAM charts, written by GDA Creator Professional 0.10-0.22 and GDA Creator 1.25; plus one hand-written `synthetic-` file.
- **More**: the item has ~358 `.gda` files in the ~95 smaller packs alone (`old era/Ready-to-Play/dmGF ONLY/`, `from GDAMANIA/`, `No BGM/` folders); each pack is a RAR: download it (`https://archive.org/download/raredtxgda/<path>`) and extract with `bsdtar`/`7z`. The GDAmania site (gdamania.net) is gone; DrumGamer lists "GDA Creator 2" and DigiBand as GDA tools (https://drumgamer.weebly.com/tools2.html).

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
- http://gdamania.blogspot.com/ (GDA to DTX conversion project)
