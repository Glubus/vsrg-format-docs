# Samples: Just Dance UbiArt tape (`.dtape.ckd`, `.ktape.ckd`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic_tml_dance.dtape.ckd` | hand-written for this repository from the `Tape` / clip field list of `../README.md` (Ferris Dancing and json2tape key names); not run through any parser (the Ferris Dancing JSON reader is unfinished at the pinned commit) | vsrg-format-docs contributors | CC0-1.0 | UbiArt-style dance tape: one compact JSON line + trailing NUL byte; real files may differ [inference] |
| `synthetic_tml_karaoke.ktape.ckd` | hand-written for this repository from the `Tape` / clip field list of `../README.md` (Ferris Dancing and json2tape key names); not run through any parser (the Ferris Dancing JSON reader is unfinished at the pinned commit) | vsrg-format-docs contributors | CC0-1.0 | Karaoke tape: three `KaraokeClip` with `Pitch`, `Lyrics`, `IsEndOfLine`, tolerances |

