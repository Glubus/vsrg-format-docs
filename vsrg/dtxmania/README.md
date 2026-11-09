# DTXMania

DTXMania (by Mr. "yyagi" and community; fork lineage DTXManiaXG verK, DTXManiaNX by limyz, DTXManiaAL, BocuD fork, official 4.x at https://dtxmania.net/) is a free Windows simulator of Konami's arcade GuitarFreaks / DrumMania (later GITADORA). Drum charts use 9-11 vertical lanes (hi-hat, snare, bass, toms, cymbals, ride, left cymbal, left pedal). Guitar/bass use 3 (RGB) then 5 (RGBYP) fret lanes plus open and wailing. Notes fall on fixed vertical lanes, so it is **vsrg** (see also the [GITADORA README](../gitadora/README.md)).

| Folder | File | Role |
|---|---|---|
| [dtx/](dtx/README.md) | `.dtx` | BMS-derived text chart: DTXMania native format (also read: `.bms`, `.bme`, `.mid` per `CDTX.tRead`) |
| [gda/](gda/README.md) | `.gda` | older GuitarFreaks/DrumMania text variant: DTXMania loads it with the DTX parser and a 2-letter channel table |
| [g2d/](g2d/README.md) | `.g2d` | sibling of `.gda` (same table); Unknown origin |
| [set-def/](set-def/README.md) | `set.def` | song set descriptor grouping difficulties |

Real DTX samples: [dtx/samples](dtx/samples/README.md).
