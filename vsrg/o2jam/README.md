# O2Jam

O2Jam is a Korean 7-key vertical-scroll online rhythm game (O2Media, 2003; many regional releases: Korea mgame/NOWCOM, e-Games, GAMANIA, 9you, O2Jam Thai, O2Jam China; later O2Jam X2, O2Jam O2, Classic). Seven lanes fall towards a judgement line, with long notes and keysounded charts: so it belongs to the **vsrg** category (fixed columns, vertical scroll).

| Folder | File(s) | Role |
|---|---|---|
| [ojn/](ojn/README.md) | `.ojn` (`o2maNNN.ojn`) | Note chart + metadata + cover image, 3 difficulties (EX/NX/HX) per file |
| [ojm/](ojm/README.md) | `.ojm` (M30 / OMC / OJM containers) | Sample bank (keysounds + BGM) paired with an OJN of the same base name |
| [ojnlist-dat/](ojnlist-dat/README.md) | `OJNList.dat`, `X2OJNList.dat` | Client song index: array of 300-byte OJN headers + extra sections |
| [snp/](snp/README.md) | `.snp` | KrazyRain: VDISK1.0 archive of zlib-compressed `.xnt`/`.xne` charts + OGG samples |
| [xnt/](xnt/README.md) | `.xnt` (+ `.xne`) | KrazyRain chart binary stored inside a `.snp` |
| [txt/](txt/README.md) | `.txt` | O2Jam - Music & Game (mobile) chart, stub |

Other O2Jam client files (not charts, only identified in [CXO2 docs](https://github.com/SirusDoma/CXO2/blob/develop/docs/file-format/FileFormat.md)): `.opi`/`.opa` package archives, `.ojs/.oji/.ojt/.oja` sprites (RGB555 frames), `.bnd` hit-test bounds, `ControlList_*.txt` UI layout, `ItemData*.dat`, `SetInfoData.ojs`. Not documented further here.

Related: Open2Jam (Java emulator, read-only parsers for all of the above), O2Mania (older emulator), CXO2 (C++ client reimplementation), Raindrop (VSRG that loads OJN).

Real sample files: [ojn/samples](ojn/samples/README.md).
