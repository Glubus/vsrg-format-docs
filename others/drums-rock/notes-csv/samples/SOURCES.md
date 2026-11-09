# Samples: Drums Rock custom song (`notes.csv`, `info.csv`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-notes.csv` | hand-written from the fiche column rules (official instruction page + Editor on Fire dr.c) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Header `Time [s],Enemy Type,Aux Color 1,Aux Color 2,No Enemies,interval,Aux`; single notes (type 1), doubles (type 2, colors 2+3 and 1+6), one 5-hit drum roll (type 3 with `interval` 5); `Aux` follows the Aux Color 1 mapping (1->6, 2->7, 3->5, 4->8, 5->5) |
| `synthetic-info.csv` | hand-written from the fiche (EoF export header) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. `info.csv` header exactly `Song Name,Author Name,Difficulty,Song Duration in seconds,Song Map` and a data row (difficulty 2 = Hard) |
