# Samples: SRT / SZT / SCT / SDT (maimai classic)

Synthetic files are hand-written from the column layout in `../README.md`; each parses without error with MaiConverter's SXT reader (`MaiSxt.open`, MIT) run in scratch.

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-srt.srt` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | SRT (7 columns, 6-decimal fractions): taps, hold, break tap (type 4), slides as tap-with-slide-id + |
| `synthetic-szt.szt` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | SZT (7 columns): tap 1, hold 2, break tap 3, star 4, break star 5 |
| `synthetic-sct.sct` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | SCT (8 columns): as SZT plus the slide-amount column; a break star launching two slides |
| `synthetic-sdt.sdt` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | SDT (9 columns, 4-decimal fractions, slide delay in the last column): as SCT, delays 0.25 |

