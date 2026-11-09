# Samples: Just Dance UbiArt tape (`.dtape.ckd`, `.ktape.ckd`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic_tml_dance.dtape.ckd` | hand-written for this repository from the `Tape` / clip field list of `../README.md` (Ferris Dancing and json2tape key names); not run through any parser (the Ferris Dancing JSON reader is unfinished at the pinned commit) | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | UbiArt-style dance tape: one compact JSON line + trailing NUL byte; 4 `MotionClip` (two coaches via `CoachId`, two gold moves with `GoldMove` 1, `MotionPlatformSpecifics` X360/ORBIS), 4 `PictogramClip` (`CoachCount` 0xFFFFFFFF = all, and 1), 1 `GoldEffectClip`; ticks at 24 per beat. Real files may differ in key order/formatting [inference] (2706 bytes) |
| `synthetic_tml_karaoke.ktape.ckd` | hand-written for this repository from the `Tape` / clip field list of `../README.md` (Ferris Dancing and json2tape key names); not run through any parser (the Ferris Dancing JSON reader is unfinished at the pinned commit) | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | Karaoke tape: three `KaraokeClip` with `Pitch`, `Lyrics`, `IsEndOfLine`, tolerances; compact JSON + trailing NUL (768 bytes) |

