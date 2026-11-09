# Samples: iBMSC project (.ibmsc)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-minimal.ibmsc` | Hand-built by BmsAux with a Python writer that follows `OpeniBMSC` / `SaveiBMSC` in `iBMSC/ChartIO.vb` and `Note.WriteBinWriter` (`iBMSC/Option Windows/Note.vb`) of https://github.com/Shimi9999/pBMSC at `06aaf7438dbca3c8a0611bd13d134f6d1ce04a28`; checked with a Python reader that mirrors `OpeniBMSC` (all blocks parsed, file consumed exactly). Never opened in iBMSC itself. | BmsAux (synthetic) | CC0 / public domain | Smallest valid project: `iBMSC` signature, version bytes 3.5.5, Pref/Head/WAV/BMP/Beat/Expn/Note/Undo blocks, 1 WAV, 4 taps on A1..A4. |
| `synthetic-features.ibmsc` | Same method | BmsAux (synthetic) | CC0 / public domain | Full header fields, 4 WAV + 2 BMP entries (including index 1295 = `ZZ`), custom measure lengths (measure 1 = 144 ticks, measure 3 = 240), 8 A-column notes (scratch + 7 keys), BGM column, BMSE long-note pair, NT long note (`Length` 96), hidden, landmine, ghost and comment flags, BPM / STOP / SCROLL column notes, player-2 note, BGA/LAYER/POOR notes, expansion code, empty undo/redo slots (201). |

No real `.ibmsc` was found: the iBMSC (aqtq314) and pBMSC (Shimi9999) repositories ship neither a sample project nor a LICENSE file.
