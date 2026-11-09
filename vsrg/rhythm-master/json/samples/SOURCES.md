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

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `crunch_5k_hd.imd.json` | https://raw.githubusercontent.com/Fsu0413/RMEssentials/8945cab60ec58aec2f3bf08966e7c75f2f0d1bca/src/librmessentials/test/tst_rmechart/tojson/crunch_5k_hd.imd.json | AGPL repo, chart of unclear origin | imdjson 1.2.2, tempo 135, volume 127/pan 64, 60 KB, converted from `crunch_5k_hd.imd` |
| `reai105dudeni_5k_hd.imd.json` | same repo, `.../toimd/reai105dudeni_5k_hd.imd.json` | same | imdjson fixture for the JSON->IMD test |
