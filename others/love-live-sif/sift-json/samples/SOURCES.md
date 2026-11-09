# Samples: SIFTrain beatmap (Love Live! SIF live JSON)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-siftrain.json` | hand-written for this repository from the field and effect-mask description of `../README.md` (SIFTrain wiki "Beatmap Format") | vsrg-format-docs contributors | CC0-1.0 | SIFTrain beatmap JSON, 2-space indent, LF: `lead_in` 1.0, obsolete `rank_info` (5 entries) and `notes_speed` |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `npps4_Live_0001.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_0001.json | 2026-11-09 | `a78769c43178178273d510836192ad40b936039c19935bb072beb3b2b282b838` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | SIF game raw beatmap (array of notes with `notes_attribute` 1 = smile, `effect` 1/2/3 normal/star?/hold |
| `npps4_Live_0004.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_0004.json | 2026-11-09 | `e2f52cd3dd9d889534d550b3f44335c9a11483f91ca4e0cd344fdad2d544b069` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | raw SIF beatmap, `notes_attribute` 2 (pure), 91 notes |
| `npps4_Live_0007.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_0007.json | 2026-11-09 | `9e6f5bad0a8faad0f4c6bc90985cbc817e27f503551789cb94df8d140894b215` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | raw SIF beatmap, `notes_attribute` 3 (cool), 81 notes |
| `npps4_Live_0003.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_0003.json | 2026-11-09 | `a77d816137b33a03338f06c370e24c3968a2109ff57dd3a050a5dfdd65e8f5b5` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | raw SIF beatmap, 181 notes incl. 35 `effect` 4 notes |
| `npps4_Live_s0719.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_s0719.json | 2026-11-09 | `ceb7826f0ee27c44e9c2bd44de38991b008dbb3f1816bce240555c6bc8534a71` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | raw SIF beatmap of an `s` (special/swing-era) id: 634 notes with 98 `effect` 11 (swing start?) notes |
| `npps4_Live_s0725.json` | https://raw.githubusercontent.com/DarkEnergyProcessor/NPPS4/81cbb3553831a59f67ba2839af288abd7ff83488/beatmaps/Live_s0725.json | 2026-11-09 | `2904d54edabb05cb371af2817ee73757ef095247a600de912bfb00b4630f190c` | KLab (game data); collected by DarkEnergyProcessor NPPS4 | NPPS4 repo licence (LICENSE.md) | raw SIF beatmap (80 KB) containing `effect` 13 notes |
| `depls_dwr.json` | https://raw.githubusercontent.com/RayFirefist/DEPLS/00b9a0ae3ac52721d79e61672f727edb59ba06ed/test/dwr.json | 2026-11-09 | `edb8de4424fbfacbd43e0e52c10698a00e57a7cea83720b38d0a9b2f380934eb` | RayFirefist/DEPLS test data | DEPLS repo LICENSE.md (not reviewed) | livesim2/DEPLS test beatmap, multi-line JSON with 4-decimal timings, `notes_attribute` 3 |
| `depls_1154_mod.json` | https://raw.githubusercontent.com/RayFirefist/DEPLS/00b9a0ae3ac52721d79e61672f727edb59ba06ed/test/1154_mod.json | 2026-11-09 | `916d2685dca61f1b5e2f5b5ace8449bf1b35c74d97ecc04ebfb90f38894208db` | RayFirefist/DEPLS test data | DEPLS repo LICENSE.md (not reviewed) | DEPLS test beatmap (modified), compact one-line JSON, `notes_attribute` 10 |
