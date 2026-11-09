# Rizline

Mobile rhythm game (iOS, Android, released 9 April 2023; a Steam PC version supports Workshop custom charts). Notes (Tap, Catch, Hold) fall toward a judgement line while "lines" (polylines drawn over moving canvases, colored by gradients) carry them; the camera and canvases move, scale and change speed during the song, and "Riztime" sections change the color theme. The community documentation lives on the Rhythm Game Wiki (rgwiki.stary.pc.pl) and in the Rust library `rizlib`.

Category: **others**: notes ride on freely shaped, moving lines (canvas positions, speeds and camera moves change over time), so a note's screen position is not a fixed lane.

## Formats
| Folder | File | Status |
|---|---|---|
| [chart-json/](chart-json/README.md) | `chart.json` (+ `metadata.json` for Workshop custom charts) | JSON chart, times in beats, fully field-documented by the wiki and rizlib |

## Links
- Rhythm Game Wiki, Rizline: https://rgwiki.stary.pc.pl/wiki/Rizline:Chart
- rizlib (Rust library for Rizline files): https://gitlab.com/TadeLn/rizlib
