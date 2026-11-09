# Samples: VOEZ chart JSON
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-info_song.json | hand-written following VoezEditor ProjectData.cs writer (https://github.com/AndrewFM/VoezEditor) | vsrg-format-docs | CC0 / public domain | synthetic info_song.json (tabs, CRLF), levels 1/3/5 |
| synthetic-songconfig.txt | same (writer produces `songconfig.txt`) | vsrg-format-docs | CC0 | config text file id/name/bpm/author/diff/version |
| synthetic-note_hard.json | same | vsrg-format-docs | CC0 | click, hold (Hold 1.0), swipe, slide; 2 tracks |
| synthetic-track_hard.json | same | vsrg-format-docs | CC0 | 2 tracks without transformations |
| synthetic-note_extra.json | same | vsrg-format-docs | CC0 | Dir 1 swipe, hold 1.5, slides on a second track |
| synthetic-track_extra.json | same | vsrg-format-docs | CC0 | Move/Scale/ColorChange keyframes with easelinear, easeinoutquad, easeoutexpo |

Files are valid JSON written in the writer style (single-line arrays, no spaces). The `version`/`song_version` strings are arbitrary (the editor VERSION constant was not read).
