# Samples: ADOFAI level (`.adofai`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `adofai-cli_demo.adofai` | https://github.com/3289david/adofai-cli/blob/878bc764cc07e445ebd093322ad120f149ab6dad/examples/demo.adofai | danwoo (adofai-cli) | MIT (repo LICENSE, "Copyright (c) 2026 danwoo") | Tiny demo level shipped with a terminal ADOFAI engine: `angleData` (32 tiles, 0/45/90/180/270/315), `settings` version 13, events Twirl, SetSpeed (absolute BPM), Flash, ShakeScreen; LF line endings, array values on one line |
| `synthetic-angledata.adofai` | hand-written from the fiche (angleData, 999 midspin, Twirl, SetSpeed Multiplier/Bpm, Checkpoint, trailing commas) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. `angleData` with a 999 midspin tile, Twirl, SetSpeed in both Multiplier and Bpm forms, Checkpoint, trailing commas before `]`/`}`, tab indentation; no audio referenced |
| `synthetic-pathdata.adofai` | hand-written from the fiche (legacy `pathData`, absolute letters and `!` midspin, ADOFAI Expansion table) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Legacy `pathData` string "RRUULLDDRR!ETo" (R=0, U=90, L=180, D=270, `!`=999 midspin, E=45, T=60, o=75); `settings.version` value is a placeholder (version history Unknown); trailing commas |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `anglepath_backup_level.adofai` | https://raw.githubusercontent.com/xiaohuihui1022/AngleData-PathData/fe964a2763c63c13e55f55f022f2a93f81380ab1/ATPCliMode/bin/Debug/backup_level.adofai | File sits in a GPL-3.0 repo (build output folder), but is a third-party community level: authorship/licence unclear, not committed | Real level: UTF-8 BOM + CRLF, tab indentation, angleData with many 999 midspin tiles (0,150,999 triplets) (2148 bytes) |
| `anglepath_before.adofai` | https://raw.githubusercontent.com/xiaohuihui1022/AngleData-PathData/fe964a2763c63c13e55f55f022f2a93f81380ab1/AngleDataToPathData/bin/Debug/before.adofai | File sits in a GPL-3.0 repo (build output folder), but is a third-party community level (artist field kry.exe): authorship/licence unclear, not committed | Real 211 KB level, settings.version 11, CRLF, rich settings/actions/decorations (large event set) (211689 bytes) |
