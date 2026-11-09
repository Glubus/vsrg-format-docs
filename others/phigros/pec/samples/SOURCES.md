# Samples: PhiEdit Chart (`.pec`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-all-records.pec` | hand-written for this repository, built from the fiche tables (see Notes below) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic`: offset line 175 (real offset 0 per the fiche), 2 `bp` lines, `n1`/`n2`/`n3`/`n4` notes with `#` and `&` modifiers, one fake note, `cv`/`cp`/`cd`/`ca`/`cm`/`cr`/`cf` events on 2 lines, `ca` -1 |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `TSLove_chart.pec` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/TSLove/chart.pec | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); fan chart by Eroslon_Dusk per the repo's meta.json | real fan PEC chart: first line 150 (offset), one bp line (185 BPM), n1 notes with # and & modifier lines; not committed: unclear licence |
| `All_the_time.pec` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/allTheTime/All_the_time.pec | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); fan chart | real fan PEC chart, negative offset line (-50), BPM change (72.5 then 65 at beat 234.25); not committed: unclear licence |
| `Tempestissimo.pec` | https://raw.githubusercontent.com/yuameshi/phigros-charts-repo/42e92ee9620c561ab12e700d65f7bdaa553585be/samplePec/Tempestissimo.pec | No licence file in the source repo (yuameshi/phigros-charts-repo, archived); fan chart | real fan PEC chart, negative offset line (-80), single bp line (231 BPM); folder samplePec of the source repo; not committed: unclear licence |

Notes: the synthetic file follows the record table of the fiche (Phira docs); it was not loaded in Phira or PhiEdit. The real files in the manifest were observed to start with an offset line (150, -50, -80) followed by `bp` lines and `n1` records with `#`/`&` modifier lines, as the fiche says.
