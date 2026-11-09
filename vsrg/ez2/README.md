# EZ2DJ / EZ2AC / EZ2ON

EZ2DJ (Amuse World, Korea, 1999; The 1st Tracks ... 7th Trax ... Azure Expression; brand renamed EZ2AC in 2013 by SQUARE PIXELS, last arcade version "EZ2AC: Evolve", 2014; later mobile/PC EZ2ON) is a beatmania-like arcade DJ game: 5 keys + turntable + foot pedal (Ruby/5K/7K/10K Club/14K Space modes) with vertical-falling notes: **vsrg**. Charts are `.ez` (binary "EZFF", usually encrypted in the retail game), accompanied by a keysound index `.ezi` (text) and a settings `.ini`. The reverse-engineering sources used here are EZ2BMS (TypeScript, clean-room chart suite) and the EZ2PORT engine it mirrors; the more complete notes that the web search pointed to (`libhwang50/ez2ac-re`, `ez2onrr-re`, `3s-re`) return HTTP 404 from GitHub (private/removed), and `ez2stuff` (`ezdec_715.c`/`ezdec_720.c` for 7th Trax) could not be located.

| Folder | File | Role |
|---|---|---|
| [ez/](ez/README.md) | `.ez` | EZFF binary chart (v4..v8), per-mode and per-key-count, one file per difficulty |
| [ezi/](ezi/README.md) | `.ezi` | text keysound index of a chart |

Other game files (not charts; names only): `.ini` (judgement/gauge per chart), `.ssf` (keysound audio), `.gds` (lane descriptors), `.pvi` (skins), `.abm` (art), `song.bin` (song tables, starts with `EZSL`, encrypted), `song.ini` (EZ2PORT package). Related: the DJMAX [pt](../djmax/pt/README.md) format reuses the same `EZTR` track container (the PTFF family), which is likely a common code base [inference].

EZ2ON (Reboot: R) and Sabin Sound Star (3S, `.sss` = `.ezi` text half + EZFF v6 payload, per search snippets of ez2ac-re, unverified here) have no accessible public specification: Unknown.
