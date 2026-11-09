# Samples: Deemo chart (JSON) (`.json`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-deemo.json` | hand-written from the fiche field list; extra root `speed` and `time`-less notes follow the real files observed in the manifest samples (Deenote test charts) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Compact one-line JSON: `speed`, 5 notes with `$id`, `pos`, `size`, `_time`, `sounds[{d,p,v}]` (one note with two sounds incl. relative delay `w`), one silent note without `sounds`, and one `links` entry chaining notes 2-3-4 through `{"$ref": ...}` |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `Deemo-I-Charts_AI01creamstew.easy.json` | https://raw.githubusercontent.com/LibrarristShalinward/Deemo-I-Charts/313578104c64a07860b4ff5875201cede6a89a2b/%E5%8E%9F%E7%89%88%E8%B0%B1%E9%9D%A2/AI01creamstew.easy.json | 2026-11-09 | 990f8ca34a3ffb1794b60f462d708fb256cfd28d8f2e3d501455cf9ac84c14a8 | see remarks | No licence in repo; extracted official Deemo (Rayark) chart data, not committed | Official Deemo I chart extracted from the game (Easy), JSON with notes and links |
| `Deemo-I-Charts_AI01creamstew.hard.json` | https://raw.githubusercontent.com/LibrarristShalinward/Deemo-I-Charts/313578104c64a07860b4ff5875201cede6a89a2b/%E5%8E%9F%E7%89%88%E8%B0%B1%E9%9D%A2/AI01creamstew.hard.json | 2026-11-09 | c638cccb9e6ae294c9a1ecc6a17ab622fe1642f0c7a36331e487571893036167 | see remarks | No licence in repo; extracted official Deemo (Rayark) chart data, not committed | Official Deemo I chart (Hard) |
| `deenote_12.Magnolia.hard.txt` | https://raw.githubusercontent.com/Chlorie/Deenote/f1d7786b55f81bd6bebf77ae6f6eac1b1cffcf8a/Assets/Dev/TestCharts/12.Magnolia.hard.txt | 2026-11-09 | aefeb7a4ae21f412cfd330ebf584ade0f2030fcc0c0f0b62f1232387c82a1ed6 | see remarks | No licence file in repo (Chlorie/Deenote); game chart used as editor test data, not committed | Deemo chart JSON saved with a .txt extension (root speed + notes), 151 KB |
| `deenote_finale.hard.json` | https://raw.githubusercontent.com/Chlorie/Deenote/f1d7786b55f81bd6bebf77ae6f6eac1b1cffcf8a/Assets/Dev/TestCharts/finale.hard.json | 2026-11-09 | f25b1bfb0dde1da9e20313e242a81c817db9cf8efa0993e91fb47188aca56e86 | see remarks | No licence file in repo (Chlorie/Deenote); game chart used as editor test data, not committed | Deemo chart JSON with root fields speed, oriVMin, oriVMax, remapVMin, remapVMax, notes[] ($id, sounds[{d,p,v}], pos, size, _time, speed, eventID, time); 307 KB |
