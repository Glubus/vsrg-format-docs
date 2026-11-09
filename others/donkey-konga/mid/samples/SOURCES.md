# Samples: Donkey Konga score MIDI (`.mid`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-konga.mid` | hand-built Standard MIDI File from the fiche/guide facts (notes on channel 10: D#4 = 63 left bongo, E4 = 64 right bongo, D#2 = 39 clap; first beat after the 2-second lead-in) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic, NOT validated in the game. SMF format 0, 480 ticks/quarter, 120 BPM, 4/4; 8 note-on/off pairs on channel 10 (MIDI channel index 9) starting at 2.0 s (tick 1920) using only the three documented note numbers; documented-but-unknown note numbers (both bongos, rolls) deliberately not used |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `gamebanana-turbo-killer_12.txt` | https://gamebanana.com/dl/1562176 | 2026-11-09 | 2b200f88fc032bcbd49ae2f5340fd88ff838fd1f7a976aefba00104d1d767649 | same mod | same | SongInfo-style text entry shipped with the mod (extracted from the zip) |
| `gamebanana-turbo-killer_12TurboKiller_1h.mid` | https://gamebanana.com/mods/633998 (download https://gamebanana.com/dl/1562176) | 2026-11-09 | 2b200f88fc032bcbd49ae2f5340fd88ff838fd1f7a976aefba00104d1d767649 | see GameBanana mod "Turbo Killer" for Donkey Konga 2 | GameBanana mod, no licence stated; accepted risk | real custom Donkey Konga 2 score MIDI (3499 bytes), extracted from turbo_killer.zip (12.dsp audio stream not included); sha256 is of the zip |
| `gamebanana-turbo-killer_12TurboKiller_1x.mid` | https://gamebanana.com/mods/633998 (download https://gamebanana.com/dl/1562176) | 2026-11-09 | 2b200f88fc032bcbd49ae2f5340fd88ff838fd1f7a976aefba00104d1d767649 | see GameBanana mod "Turbo Killer" for Donkey Konga 2 | GameBanana mod, no licence stated; accepted risk | real custom Donkey Konga 2 score MIDI (5954 bytes), extracted from turbo_killer.zip (12.dsp audio stream not included); sha256 is of the zip |
| `gamebanana-turbo-killer_12TurboKiller_2h.mid` | https://gamebanana.com/mods/633998 (download https://gamebanana.com/dl/1562176) | 2026-11-09 | 2b200f88fc032bcbd49ae2f5340fd88ff838fd1f7a976aefba00104d1d767649 | see GameBanana mod "Turbo Killer" for Donkey Konga 2 | GameBanana mod, no licence stated; accepted risk | real custom Donkey Konga 2 score MIDI (2717 bytes), extracted from turbo_killer.zip (12.dsp audio stream not included); sha256 is of the zip |
