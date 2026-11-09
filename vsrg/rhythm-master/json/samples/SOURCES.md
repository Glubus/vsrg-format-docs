# Samples: Rhythm Master imdjson (`.json`, `BNDQ`)

## Committed
All byte-exact from https://github.com/Fsu0413/RMEssentials @ `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca` (author Fsu0413, AGPL-3.0 per repo `LICENSE`), test files written for the RMEssentials unit tests (`src/librmessentials/test/`). Some invalid files hold joke strings as wrong-typed values.

| File | Origin (upstream path) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rmessentials-existnotes_5k_ez.imd.json` | `tst_rmeutils/existnotes/existnotes_5k_ez.imd.json` | Fsu0413 | AGPL-3.0 | valid imdjson 1.2.3, one note (tick 240, time 3000) |
| `rmessentials-existnotes_5k_hd.imd.json` | `tst_rmeutils/existnotes/existnotes_5k_hd.imd.json` | Fsu0413 | AGPL-3.0 | valid imdjson 1.2.3, one note, tempo 100 |
| `rmessentials-existnotes_5k_nm.imd.json` | `tst_rmeutils/existnotes/existnotes_5k_nm.imd.json` | Fsu0413 | AGPL-3.0 | valid imdjson 1.2.3, one note |
| `rmessentials-existnotes_6k_ez.imd.json` | `tst_rmeutils/existnotes/existnotes_6k_ez.imd.json` | Fsu0413 | AGPL-3.0 | valid imdjson 1.3.0 (adds duration, durationtime, samples), one note |
| `rmessentials-fromjson_130durationtimeng.json` | `tst_rmechart/fromjson/130durationtimeng.json` | Fsu0413 | AGPL-3.0 | invalid: 1.3.0 durationtime has wrong type |
| `rmessentials-fromjson_130noduration.json` | `tst_rmechart/fromjson/130noduration.json` | Fsu0413 | AGPL-3.0 | invalid: 1.3.0 without duration |
| `rmessentials-fromjson_130nodurationtime.json` | `tst_rmechart/fromjson/130nodurationtime.json` | Fsu0413 | AGPL-3.0 | invalid: 1.3.0 without durationtime |
| `rmessentials-fromjson_130notracks.json` | `tst_rmechart/fromjson/130notracks.json` | Fsu0413 | AGPL-3.0 | invalid: 1.3.0 without tracks |
| `rmessentials-fromjson_nosig.json` | `tst_rmechart/fromjson/nosig.json` | Fsu0413 | AGPL-3.0 | invalid: no signature (3 B) |
| `rmessentials-fromjson_notempo.json` | `tst_rmechart/fromjson/notempo.json` | Fsu0413 | AGPL-3.0 | invalid: no tempo |
| `rmessentials-fromjson_notracks.json` | `tst_rmechart/fromjson/notracks.json` | Fsu0413 | AGPL-3.0 | invalid: no tracks |
| `rmessentials-fromjson_noversion.json` | `tst_rmechart/fromjson/noversion.json` | Fsu0413 | AGPL-3.0 | invalid: no version |
| `rmessentials-fromjson_signg.json` | `tst_rmechart/fromjson/signg.json` | Fsu0413 | AGPL-3.0 | invalid: bad signature |
| `rmessentials-fromjson_tempong.json` | `tst_rmechart/fromjson/tempong.json` | Fsu0413 | AGPL-3.0 | invalid: bad tempo |
| `rmessentials-fromjson_trackng.json` | `tst_rmechart/fromjson/trackng.json` | Fsu0413 | AGPL-3.0 | invalid: tracks entry has wrong type |
| `rmessentials-fromjson_tracknonote.json` | `tst_rmechart/fromjson/tracknonote.json` | Fsu0413 | AGPL-3.0 | invalid: track without note array |
| `rmessentials-fromjson_tracknoteng.json` | `tst_rmechart/fromjson/tracknoteng.json` | Fsu0413 | AGPL-3.0 | invalid: bad note entry |
| `rmessentials-fromjson_tracknotesng.json` | `tst_rmechart/fromjson/tracknotesng.json` | Fsu0413 | AGPL-3.0 | invalid: bad note list |
| `rmessentials-fromjson_tracknotetojsonng.json` | `tst_rmechart/fromjson/tracknotetojsonng.json` | Fsu0413 | AGPL-3.0 | invalid: note not convertible to JSON note |
| `rmessentials-fromjson_tracknotrack.json` | `tst_rmechart/fromjson/tracknotrack.json` | Fsu0413 | AGPL-3.0 | invalid: track object without track number |
| `rmessentials-fromjson_tracksng.json` | `tst_rmechart/fromjson/tracksng.json` | Fsu0413 | AGPL-3.0 | invalid: tracks array holds a string instead of an object |
| `rmessentials-fromjson_tracktrackng.json` | `tst_rmechart/fromjson/tracktrackng.json` | Fsu0413 | AGPL-3.0 | invalid: track number has wrong type |
| `rmessentials-fromjson_versionng.json` | `tst_rmechart/fromjson/versionng.json` | Fsu0413 | AGPL-3.0 | invalid: bad version |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)


| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `crunch_5k_hd.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/tojson/crunch_5k_hd.imd.json | 2026-11-09 | 08c5ec9a64c9866206b220fff6ce0c69f38ca0d401f4ab559f5ac02c48655670 | Fsu0413/RMEssentials (repository; chart author see file) | Repo AGPL-3.0; chart of unclear origin (not committed) | imdjson 1.2.2 (tempo 135, volume 127, pan 64) converted from crunch_5k_hd.imd |
| `reai105dudeni_5k_hd.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/toimd/reai105dudeni_5k_hd.imd.json | 2026-11-09 | 6bf1c104102d0a729719b8c973b81ada5616310a43484d01b8b4ec4935bc2412 | Fsu0413/RMEssentials (repository; chart author see file) | Repo AGPL-3.0; chart of unclear origin (not committed) | imdjson fixture for the JSON->IMD direction |
| `friend01_4k_nm.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/tojson/friend01_4k_nm.imd.json | 2026-11-09 | ffcf3326ff74a19347b7b624e48d7e0ca134c7d8be63883e6a8d4e9e25bb01ed | Fsu0413 (RMEssentials output of a song chart) | Repo AGPL-3.0; chart of unclear origin | imdjson from an IMD: friend01 is version 1.3.0 tempo 290 (the fiche example); 80-180 KB |
| `legend_5k_hd.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/toimd/legend_5k_hd.imd.json | 2026-11-09 | 9005dd39423d30459472c802678bd02297bb9e0c90585200f0268f76ceeba217 | Fsu0413 (RMEssentials output of a song chart) | Repo AGPL-3.0; chart of unclear origin | imdjson from an IMD: friend01 is version 1.3.0 tempo 290 (the fiche example); 80-180 KB |
| `caiyilinbeast_6k_hd.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/tojson/caiyilinbeast_6k_hd.imd.json | 2026-11-09 | fd41d6dd4e21c90e212cbf23fed6aa38afc1ee46b8d1d9b527ce04f96d1554c2 | Fsu0413 (RMEssentials output of a song chart) | Repo AGPL-3.0; chart of unclear origin | imdjson from an IMD: friend01 is version 1.3.0 tempo 290 (the fiche example); 80-180 KB |
