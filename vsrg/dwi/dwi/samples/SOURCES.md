# Samples: Dance With Intensity `.dwi`

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-demo.dwi | Public domain (CC0); hand-written for this corpus | StepmaniaFamily corpus (generated) | CC0 / public domain | synthetic, built from this folder's README: #GAP, #BPM, #DISPLAYBPM `a..b`, #FREEZE (DWI counter 96 = SM beat 24, 500 ms), #CHANGEBPM (counter 64 = SM beat 16), #SAMPLESTART/#SAMPLELENGTH; charts #SINGLE BASIC/MANIAC, #DOUBLE ANOTHER (two pad strings), #SOLO (C..M six-panel codes), #COUPLE; `( )` 1/16, `[ ]` 1/24 groups, `<..>` jumps/hands, `!` holds (`8!8` ... `8`). Validated with an ad-hoc parser: every chart string fills a whole number of measures and every hold is closed |

Real DWI files exist only as non-redistributable game charts (see manifest) or in the official sample song zip `NotMyBattle.zip` on dwi.ddruk.com (live URL; the only Wayback copy, 20221202004533, is truncated to 1 MiB, so it cannot be hashed: not in the manifest). The latter holds `notmybattle.dwi` (2094 bytes in the 2.1 MB zip; #BPM:155.88, #GAP:130, #CHANGEBPM:672=77.94,800=155.88, #SINGLE BASIC/ANOTHER/MANIAC with `!` holds, `( )` groups and spaces inside the step strings), observed 2026-11-09.

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| ddr-3rdmix_GET-UP-AND-DANCE.dwi | https://raw.githubusercontent.com/noahm/simfile-parser/f7ff6e3c754a9a04aa705b8129dc89523fd4b02f/packs/3rdMix/GET%20UP%20AND%20DANCE/GET%20UP%20AND%20DANCE.dwi | Unknown (no licence in noahm/simfile-parser; charts of a Konami game) | DDR 3rdMix chart as .dwi (4-panel + holds); not committed |
| ddr-5thmix_17SAI.dwi | https://raw.githubusercontent.com/noahm/simfile-parser/f7ff6e3c754a9a04aa705b8129dc89523fd4b02f/packs/5thMix/17SAI/17SAI.dwi | Unknown (no licence in noahm/simfile-parser; charts of a Konami game) | DDR 5thMix chart as .dwi; not committed |
| bhop-ball_02-Ants.dwi | https://raw.githubusercontent.com/noahm/simfile-parser/f7ff6e3c754a9a04aa705b8129dc89523fd4b02f/packs/Bhop%20Ball/%5BT07%5D%20Ants%20%28No%20CMOD%29/02%20Ants.dwi | Unknown (no licence in noahm/simfile-parser) | Community-pack .dwi (non-DDR song) used as parser fixture; not committed |
