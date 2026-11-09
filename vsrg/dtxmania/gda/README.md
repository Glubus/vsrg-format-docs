# DTXMania older chart format (`.gda`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: text

## Overview
`.gda` is an older text chart format for GuitarFreaks/DrumMania that DTXMania still loads. `CDTX.tRead` sets `EType.GDA` for the extension and parses it with the DTX line parser, looking the 2-letter/2-digit channel name up in a table instead of reading 2 hex digits. The GDAmania blog converted its GDA charts to DTX ("Changed all format to DTX files"). No public spec; origin of the layout: Unknown.

## Container & encoding
Text lines `#mmmcc: objects` as in [DTX](../dtx/README.md) (3-char measure number, 2-char channel, base-36 objects) [inference: shared parser path `tInput_LineAnalysis_ChipLocation`; confirmed by real files, e.g. `#002G2:0001` in samples/mitchi_Happy_man_BSC.gda]. [observed: *.gda] Shift_JIS (CP932) with CRLF in most files (Japanese `#TITLE`/`#ARTIST`, e.g. samples/nari_konan.gda), some pure ASCII (samples/BLAST_model_dd5_hell.gda); no BOM. Header lines are `#KEY value` with a space instead of a colon (`#TITLE HAPPY MAN BASIC`, `#BPM 180`, `#BASEBPM 0`, `#DLEVEL 0`, `#GLEVEL 18`, `#BLEVEL 0`, `#PREVIEW Happy manpre.wav`, `#WAV02 Happy man.wav`); data lines use a colon. The first line is usually an editor comment (`;Created by GDA Creator Professional Ver.0.14`, `...Ver.0.16`, `...Ver.0.22`, `;Created by GDA Creator Ver.1.25 Rev.Final`).

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

Header commands and resource tables (`#WAV`, `#BPM`, `#DLEVEL` ...) match DTX [observed: *.gda]. Tempo: `#BPM` with an initial value (180, 124, 300, 161.00) or `#BPM 0` plus a `TC` data line (samples/KOUICHI_hurukawa.gda, samples/nari_konan.gda). Drum files use only `BD CY HH HT LT SD`; guitar/bass files use `G0` (open, samples/mitchi_YOU_CAN'T_EXT(OPEN).gda), `G1`..`G7`, `GW`. One file is one difficulty (`... BSC/ADV/EXT.gda`), grouped by [set.def](../set-def/README.md) (`#L1FILE: bas.gda`).

## Timing model
As [DTX](../dtx/README.md): 384 ticks per measure, BL = bar length, TC = tempo.

## Notes
Lanes: drums HH, SD, BD, HT, LT, CY (6 lanes, no floor tom/ride/open HH in the table: [inference] the original arcade GF/DM 1st-3rd gen), guitar and bass 3 buttons + open + wailing.

## Audio & images
Unknown (same `#WAVzz` mechanism if parsed as DTX).

## Versions & variants
`.g2d`: see [g2d](../g2d/README.md).

## Quirks & pitfalls
Behaviour is known only through DTXMania's code.

## Example
Excerpt, samples/mitchi_Happy_man_BSC.gda (CP932, CRLF): `;Created by GDA Creator Professional Ver.0.14` / `#TITLE HAPPY MAN BASIC` / `#ARTIST ...` / `#BPM 180` / `#GLEVEL 18` / `#WAV02 Happy man.wav` / `#002G2:0001` / `#002G4:0100` / `#003G1:0100000000000000`. A hand-written file built from the loader table is also in [samples/](samples/SOURCES.md).

## ROX support
Decode only, `rox::formats::dtx` (`GdaDecoder`, `DetectedFormat::Gda`, `.gda` and `.g2d`): the `.dtx` reader with the GDA channel names translated by `DTXMania`'s `STGDAPARAM` table (`TC` BPM, `BL` bar length, `HH SD BD HT LT CY` drums, `G0`..`G7`/`GW` guitar, `B0`..`B7`/`BW` bass, `01`..`20` sound effects SE01..SE32); every rule of the `.dtx` reader follows (instruments as variants, holds, audio plan). All 19 committed `.gda` decode: drum charts on 4 or 6 columns, guitar charts on 4.

## Parsers & tools
DTXmaniaNX CDTX.cs and DTXCreator `CDTXInputOutput.cs` (https://github.com/limyz/DTXmaniaNX).

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: the archive.org item "Rare DTX&GDA Simfile Collection" (`raredtxgda`) has ~358 `.gda` files in its ~95 smaller packs (`old era/Ready-to-Play/dmGF ONLY/`, `from GDAMANIA/`, `No BGM/`). Each pack is a RAR: download `https://archive.org/download/raredtxgda/<path>` and extract with `bsdtar`/`7z`. gdamania.net is gone; DrumGamer lists "GDA Creator 2" and DigiBand as GDA tools (https://drumgamer.weebly.com/tools2.html).

## Sources
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXMania/Code/Score,Song/CDTX.cs
- https://raw.githubusercontent.com/limyz/DTXmaniaNX/master/DTXCreator/Code/00.App/CDTXInputOutput.cs
- http://gdamania.blogspot.com/ (GDA to DTX conversion project)
