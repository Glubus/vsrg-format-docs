# Samples: DanceRail chart (`.drb`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-demo.drb` | hand-written from the DR3Editor grammar (src/utils/levelFormat.ts validateLevelText; every line checked against its regexes) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Header with 2 BPM entries (120, then 180 at measure 2), one speed change (#SC/#SCI), 7 notes of types 1, 2, 3 (hold start), 4 (hold end with parentId 2), 9 (circle flick), 13 (flick left with appearMode L), 10 (damage). Whether real `.drb` files match this `.txt` grammar is unverified (see fiche) |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `dr3viewer_bluemelody.1.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.1.txt | 2026-11-09 | d0adc4241f32dfadd34f693e1dc54625fb63acd53b3faf9012c403c9b142a84e | see remarks | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.1.txt: #OFFSET=-2.39, two BPMs (100 then 208 at position 11), 18 KB. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) |
| `dr3viewer_bluemelody.6.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.6.txt | 2026-11-09 | d7ac38a768915194699cdd1a4f603b01e83625c35ee021bbbb36f062cb93e9c5 | see remarks | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.6.txt: 44 KB chart. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) |
| `dr3viewer_bluemelody.8.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.8.txt | 2026-11-09 | aeca5e1f3c9e42c3b301e5b042283b161769f3b077a51dfe58e515ce93c5448b | see remarks | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.8.txt: 52 KB chart. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) |
