# Samples: Rhythm Master classic chart (`.imd`)

## Committed
| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rmessentials-fromimd_noteng.imd` | https://github.com/Fsu0413/RMEssentials `src/librmessentials/test/tst_rmechart/fromimd/noteng.imd` @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` | Fsu0413 | AGPL-3.0 (repo `LICENSE`) | invalid: bad note data (37 B) |
| `rmessentials-fromimd_separatorng.imd` | https://github.com/Fsu0413/RMEssentials `src/librmessentials/test/tst_rmechart/fromimd/separatorng.imd` @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` | Fsu0413 | AGPL-3.0 (repo `LICENSE`) | invalid: separator is not 0x0303 (56 B) |
| `rmessentials-fromimd_sizebpmcountng.imd` | https://github.com/Fsu0413/RMEssentials `src/librmessentials/test/tst_rmechart/fromimd/sizebpmcountng.imd` @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` | Fsu0413 | AGPL-3.0 (repo `LICENSE`) | invalid: BPM count larger than file (41 B) |
| `rmessentials-fromimd_sizeng.imd` | https://github.com/Fsu0413/RMEssentials `src/librmessentials/test/tst_rmechart/fromimd/sizeng.imd` @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` | Fsu0413 | AGPL-3.0 (repo `LICENSE`) | invalid: empty file (0 B) |
| `rmessentials-fromimd_sizenotecountng.imd` | https://github.com/Fsu0413/RMEssentials `src/librmessentials/test/tst_rmechart/fromimd/sizenotecountng.imd` @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` | Fsu0413 | AGPL-3.0 (repo `LICENSE`) | invalid: note count larger than file (49 B) |
| `synthetic_4k_hd.imd` | hand-built for this repository | vsrg-format-docs | CC0 / public domain | `synthetic`: valid 4-key file (317 B), total 8000 ms, 17 BPM entries (120 BPM, one per beat), separator `0x0303`, 9 notes: taps, flick (`0x01`, +1 lane), hold (`0x02`, 500 ms), chain `0x62` -> `0x22` -> `0xA2`, a double tap. Size = `8+12*17+6+11*9` as the fiche states; chain-end semantics not verified against the game. |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `1987wbzhyjn_4k_ez.imd`, `1987wbzhyjn_5k_hd.imd`, `1987wbzhyjn_6k_nm.imd`, `2differenttears_5k_hd.imd` | https://raw.githubusercontent.com/GirlKiller512/RhythmMasterResource/6deafea7f3d0ea90b09d1c3ef3861659536ae986/res/song/... | no licence; official classic-mode resources of the closed game | 4/5/6 keys and ez/nm/hd difficulties |
| `crunch_5k_hd.imd`, `caiyilinbeast_6k_hd.imd` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/tojson/... | repo AGPL-3.0, song charts of unclear origin | IMD inputs of the IMD->imdjson test |

The archive also holds the `.mde` placeholder `tst_rmeutils/existnotes/existnotes_Papa_Normal.mde` (0 bytes, not a sample).
