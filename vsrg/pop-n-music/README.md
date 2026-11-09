# pop'n music

Konami's 9-button arcade rhythm game (1998-09-28). Category: **vsrg** - notes scroll down nine fixed columns (one per colour-coded button).

| Folder | Format | Status |
| --- | --- | --- |
| [`arcade-chart/`](arcade-chart/README.md) | Arcade chart events as read by `popntowav` (8- or 12-byte events, `.2dx` keysounds) | stub/partial |
| [`../bms/pms/`](../bms/pms/README.md) | `.pms` - BMS-compatible 9-button text format made for the community simulators (feeling pomu, LR2, beatoraja) | complete |
| [`../bms/bmson/`](../bms/bmson/README.md) | bmson with `mode_hint` `popn-5k` / `popn-9k` | complete |

Hitkey BMS memo: "Keep-kun" (fixed-length hold bar, pop'n music MICKEY TUNES, 2000-04-20) is a long-note kind BMS has to emulate; the 5-button and "pomu-battle" 3-button layouts exist as PMS key maps.

Public knowledge of the arcade chart is one JavaScript reader (`popnchart.js`, event layout only); file name, difficulty/slot layout, most flags and tick rate are Unknown ([`arcade-chart/`](arcade-chart/README.md)). Keysounds are `.2dx` containers ([`../beatmania-iidx/2dx`](../beatmania-iidx/2dx/README.md)); charts and sounds sit in Konami `.ifs` archives (extract with mon/ifstools).

Links: https://popn.tools/ (song/chart database), https://github.com/Gi-z/popntowav, https://github.com/DragonMinded/bemaniutils (server emulator).
