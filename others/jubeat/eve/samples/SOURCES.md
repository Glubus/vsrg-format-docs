# Samples: EVE (`.eve`, jubeat chart events)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-example.eve` | hand-written for this repository from the field list of `../README.md` (jubeatools `konami/commons.py` rules re-implemented in scratch: value ranges, LONG tail must stay on the 4x4 grid, three comma-separated fields, `{time:>8},{command:<8},{value:>8}` layout) | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | ASCII `.eve` with LF endings: two `TEMPO` events (400000 = 150 BPM, then 500000 = |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)


| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `jubeatools_Life_Without_You.eve` | https://raw.githubusercontent.com/Stepland/jubeatools/1aa4d33dd08760cb1b0c2a23a7d47a07c97d97a1/jubeatools/cli/tests/data/Life%20Without%20You.eve | 2026-11-09 | 18b3e304bacf047a212fcf97af53e546029547966856bbea9cd8fa0f2fe81816 | Stepland | none stated | jubeatools CLI test fixture: 33 964 bytes, ASCII `time,command,value` lines, right-aligned fields; single `TEMPO 400000` |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `jubeatools_Life_Without_You.eve` | https://raw.githubusercontent.com/Stepland/jubeatools/1aa4d33dd08760cb1b0c2a23a7d47a07c97d97a1/jubeatools/cli/tests/data/Life%20Without%20You.eve | 2026-11-09 | `18b3e304bacf047a212fcf97af53e546029547966856bbea9cd8fa0f2fe81816` | Stepland | none stated | jubeatools CLI test fixture: 33 964 bytes, ASCII `time,command,value` lines, right-aligned fields; single `TEMPO 400000` |
| `jubeatools_351450202_ext.eve` | https://gitlab.com/Buggyroom/jubeatools/-/raw/95851e87689bd9c3e487d78d83cf4cf5f1515fed/jubeatools/formats/konami/eve/tests/data/351450202_ext.eve | 2026-11-09 | `2ffbc7f885d5584836c089e159f2807094bcbabf993e8fc97e40988afdd06fa5` | Stepland | none stated | jubeatools EVE test fixture, `ext` difficulty file named by a numeric id; likely game-derived arcade |
| `jubeatools_padded_end_ext.eve` | https://gitlab.com/Buggyroom/jubeatools/-/raw/95851e87689bd9c3e487d78d83cf4cf5f1515fed/jubeatools/formats/konami/eve/tests/data/padded_end_ext.eve | 2026-11-09 | `850958f7613ec1ae48186d1c81b3fe5bb3e2b5d8c80d293a25f30b326d8fc64e` | Stepland | none stated | EVE fixture with a padded `END` event (edge case) (33964 bytes) |
