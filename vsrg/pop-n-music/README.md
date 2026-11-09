# pop'n music

Konami's 9-button arcade rhythm game (1998-09-28). Category: **vsrg** - notes scroll down nine fixed columns (one per colour-coded button) toward a judgement line.

| Folder | Format | Status |
| --- | --- | --- |
| [`arcade-chart/`](arcade-chart/README.md) | Arcade chart events as read by `popntowav` (8- or 12-byte events, `.2dx` keysounds) | stub/partial |
| [`../bms/pms/`](../bms/pms/README.md) | `.pms` - BMS-compatible 9-button text format made for the community simulators (feeling pomu, LR2, beatoraja) | complete |
| [`../bms/bmson/`](../bms/bmson/README.md) | bmson with `mode_hint` `popn-5k` / `popn-9k` | complete |

Notes from the hitkey BMS memo: pop'n music's "Keep-kun" (fixed-length hold bar, pop'n music MICKEY TUNES, 2000-04-20) is one of the long-note kinds the BMS world has to emulate; the 5-button and "pomu-battle" 3-button layouts exist as PMS key maps.

Public knowledge of the arcade chart is limited to one JavaScript reader (`popnchart.js`, event layout only). The chart file name, difficulty/slot layout, the meaning of most flags and the tick rate are Unknown; see [`arcade-chart/`](arcade-chart/README.md).

Keysounds of the arcade game are `.2dx` containers ([`../beatmania-iidx/2dx`](../beatmania-iidx/2dx/README.md)); charts and sounds are packed in Konami `.ifs` archives (extractable with mon/ifstools).

Links: https://popn.tools/ (song/chart database), https://github.com/Gi-z/popntowav, https://github.com/DragonMinded/bemaniutils (server emulator).
