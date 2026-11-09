# Samples: Bemuse sound pack (.bemuse + metadata.json)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `bemuse-test-a-metadata.json` | https://github.com/bemusic/bemuse at `4bf3e7d98a44841b323741cc403ecb7b41618ade`, `bemuse/src/resources/test-fixtures/a/metadata.json` (fixture `b` has a byte-identical metadata.json) | Bemuse contributors | AGPL-3.0 | `metadata.json` index: 3 files mapped to one chunk (`ref` = `[chunk index, start, end]`), `refs` with payload hash. |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)
Only the `metadata.json` index files are committed; the `.bemuse` chunks are audio containers and are not stored.

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `bemuse-ninja_5argon_maidbattle_metadata.json` | https://bemuse.ninja/music/%5B5argon%5Dmaidbattle/assets/metadata.json | 2026-11-09 | `fb95304e97b9a1933f0f31b32323ada814a1373740de790dee66a28a93916bfc` | 5argon | Served by the official Bemuse music server | pack index of 140 KB (many keysounds) |
| `bemuse-ninja_aoi_olivia_metadata.json` | https://bemuse.ninja/music/%5Baoi%5Dolivia/assets/metadata.json | 2026-11-09 | `0272084a410bf9dc773b38ff452a9bf553eb9cc4f41ab7465b2b292fc56ce921` | aoi | Served by the official Bemuse music server | pack index, 111 KB |
| `bemuse-ninja_drreb_fakepuppet_metadata.json` | https://bemuse.ninja/music/%5Bdrreb%5Dfakepuppet/assets/metadata.json | 2026-11-09 | `68f2b0e6f92b87a09a1ba3f3e4b30e6797c93701ec2785b0b44289f7174b065d` | drreb | Served by the official Bemuse music server | pack index, 180 KB |
| `bemuse-ninja_flicknote_onlylove_remix_metadata.json` | https://bemuse.ninja/music/%5Bflicknote%5Donlylove_remix/assets/metadata.json | 2026-11-09 | `7012d7b724893d28dd1fe8d5f2c5c10c41832e80373d590b967fd1452794de29` | flicknote | Served by the official Bemuse music server | 20 files mapped onto ogg.N and m4a.N chunks |
| `bemuse-ninja_ice_l_metadata.json` | https://bemuse.ninja/music/%5Bice%5Dl/assets/metadata.json | 2026-11-09 | `a439c7d0950ee980f46a7c47f0fb229c32f6591031dca7b905443907a02073b6` | ice | Served by the official Bemuse music server | pack index, 54 KB |
| `bemuse-ninja_litmus_latch_metadata.json` | https://bemuse.ninja/music/%5Blitmus%5Dlatch/assets/metadata.json | 2026-11-09 | `ca77f7f79bac3e56b90c0d4b1d16b09df08992aea8ecbc1c416517446eb92a3b` | litmus | Served by the official Bemuse music server | pack index, 63 KB |
| `bemuse-ninja_snack_dddd_metadata.json` | https://bemuse.ninja/music/%5Bsnack%5Ddddd/assets/metadata.json | 2026-11-09 | `4baf8b4c4e8db994a0eb672175b6be5d3f5fc561540d2a301953ede792086abd` | snack | Served by the official Bemuse music server | pack index, 55 KB |
| `bemuse-ninja_w_tre_chicken_metadata.json` | https://bemuse.ninja/music/%5Bw_tre%5Dchicken/assets/metadata.json | 2026-11-09 | `485c3d6d60d1d2161ef21301a4b3341a53938e95c9b3564cd2b8a5eff68f012a` | w_tre | Served by the official Bemuse music server | pack index, 78 KB |
