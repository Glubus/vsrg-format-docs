# Samples: DanceRail chart (`.drb`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-demo.drb` | hand-written from the DR3Editor grammar (src/utils/levelFormat.ts validateLevelText; every line checked against its regexes) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Header with 2 BPM entries (120, then 180 at measure 2), one speed change (#SC/#SCI), 7 notes of types 1, 2, 3 (hold start), 4 (hold end with parentId 2), 9 (circle flick), 13 (flick left with appearMode L), 10 (damage). Whether real `.drb` files match this `.txt` grammar is unverified (see fiche) |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `dr3viewer_bluemelody.1.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.1.txt | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.1.txt: #OFFSET=-2.39, two BPMs (100 then 208 at position 11), 18 KB. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) (18275 bytes) |
| `dr3viewer_bluemelody.6.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.6.txt | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.6.txt: 44 KB chart. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) (44411 bytes) |
| `dr3viewer_bluemelody.8.txt` | https://raw.githubusercontent.com/lucarioex/DanceRail3Viewer/7b60f2b428f9b4934c3bbba969fa352bd96af435/Assets/Resources/SONGS/bluemelody.8.txt | No licence in repo (lucarioex/DanceRail3Viewer); chart of the bundled song 'bluemelody'; not committed | bluemelody.8.txt: 52 KB chart. Real DanceRail text chart (.txt, the repo stores them under Resources/SONGS) (51762 bytes) |

The real charts listed above are `.txt` files (DanceRail3Viewer resources); the fiche's question whether `.drb` equals this `.txt` grammar is not settled by them.
