# Samples: Deemo chart (JSON) (`.json`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-deemo.json` | hand-written from the fiche field list; extra root `speed` and `time`-less notes follow the real files observed in the manifest samples (Deenote test charts) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Compact one-line JSON: `speed`, 5 notes with `$id`, `pos`, `size`, `_time`, `sounds[{d,p,v}]` (one note with two sounds incl. relative delay `w`), one silent note without `sounds`, and one `links` entry chaining notes 2-3-4 through `{"$ref": ...}` |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `Deemo-I-Charts_AI01creamstew.easy.json` | https://raw.githubusercontent.com/LibrarristShalinward/Deemo-I-Charts/313578104c64a07860b4ff5875201cede6a89a2b/%E5%8E%9F%E7%89%88%E8%B0%B1%E9%9D%A2/AI01creamstew.easy.json | No licence in repo; extracted official Deemo (Rayark) chart data, not committed | Official Deemo I chart extracted from the game (Easy), JSON with notes and links (141818 bytes) |
| `Deemo-I-Charts_AI01creamstew.hard.json` | https://raw.githubusercontent.com/LibrarristShalinward/Deemo-I-Charts/313578104c64a07860b4ff5875201cede6a89a2b/%E5%8E%9F%E7%89%88%E8%B0%B1%E9%9D%A2/AI01creamstew.hard.json | No licence in repo; extracted official Deemo (Rayark) chart data, not committed | Official Deemo I chart (Hard) (141393 bytes) |
| `deenote_finale.hard.json` | https://raw.githubusercontent.com/Chlorie/Deenote/f1d7786b55f81bd6bebf77ae6f6eac1b1cffcf8a/Assets/Dev/TestCharts/finale.hard.json | No licence file in repo (Chlorie/Deenote); game chart used as editor test data, not committed | Deemo chart JSON with root fields speed, oriVMin, oriVMax, remapVMin, remapVMax, notes[] ($id, sounds[{d,p,v}], pos, size, _time, speed, eventID, time); 307 KB (306917 bytes) |
| `deenote_12.Magnolia.hard.txt` | https://raw.githubusercontent.com/Chlorie/Deenote/f1d7786b55f81bd6bebf77ae6f6eac1b1cffcf8a/Assets/Dev/TestCharts/12.Magnolia.hard.txt | No licence file in repo (Chlorie/Deenote); game chart used as editor test data, not committed | Deemo chart JSON saved with a .txt extension (root speed + notes), 151 KB (151496 bytes) |
