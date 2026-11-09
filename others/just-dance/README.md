# Just Dance (Ubisoft)

Ubisoft's motion dance series (Wii 2009 onward; UbiArt Framework engine from Just Dance 2014/2015 on; Switch, PS4/5, Xbox, Wii U, PC, mobile "Just Dance Now"). The player copies a coach's choreography; the console scores controller or camera motion against reference "moves" while pictograms scroll in a timeline, and karaoke lyrics in sing-along modes. Maps are authored as UbiArt "tapes" (timelines of clips) plus music track data and motion classifiers.

Category: **others**: a motion-scored dance game; the chart is a clip timeline of full-body moves and pictograms, not notes on lanes.

## Formats
| Folder | File | Status |
|---|---|---|
| [ubiart-tape/](ubiart-tape/README.md) | `*.dtape.ckd`, `*.ktape.ckd` (and `*.tape.ckd`) | UbiArt cooked tape: JSON `Tape` object with `Clips[]` (moves, pictograms, gold effects, karaoke lyrics) |

## Links
- Ferris Dancing (Rust UbiArt toolkit, includes the `Tape` parser): https://github.com/Kriskras99/ferris_dancing
- json2tape (Just Dance Now JSON to UbiArt tapes): https://github.com/matty0004/json2tape
- BlueStar (Python module for the Just Dance Now/BlueStar engine files): https://github.com/MZommer/BlueStar
- JustDanceModTools (KtapeTool, IpkTool): https://github.com/nkrapivin/JustDanceModTools
- JD Timeline Studio (editor for JD 2017 tapes): https://github.com/MaximJDTOOLS/Just-dance-2017-timeline-studio
