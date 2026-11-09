# Samples: Robeats Lua songmap
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `MondayNightMonstersNormal.lua` | https://github.com/spotco/RobeatsCustomServerTemplate at `df8f4d3145ed474ad92b4371d030ee73d003b250`, `Workspace/SongMaps/MondayNightMonstersNormal.lua` | spotco | No LICENSE file in the repo; the author's announcement says the template is "100% Free and open source to do anything you want with" (https://devforum.roblox.com/t/open-source-robeats-rhythm-game-custom-server-template/824563) | `AudioDifficulty = 1`, 124 `note(...)` and 38 `hold(...)` calls (helper functions `note`/`hold` writing `Type=1` / `Type=2` + `Duration`), one `TimingPoints` entry (`BeatLength = 600`). |
| `MondayNightMonstersHard.lua` | same repo/commit, `Workspace/SongMaps/MondayNightMonstersHard.lua` | spotco | same | `AudioDifficulty = 14`, 360 `note(...)` and 88 `hold(...)` calls, `AudioMod = 1`. |
| `TestingMap.lua` | same repo/commit, `Workspace/SongMaps/TestingMap.lua` | spotco | same | Short debug map (9 taps written as explicit `rtv.HitObjects[#rtv.HitObjects + 1] = { Time=...; Type=1; Track=...; }` table literals instead of helper calls, tracks 1..4, `BeatLength = 500`). |

The song ("Monday Night Monsters", FinnMK) is the template's own sample; the author says the mp3 may be used for anything. Only the Lua maps are committed (no audio). Licence caveat noted in the doubts file.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)
| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `pastebin-EkQrkfUL_robeats_script.lua` | https://pastebin.com/raw/EkQrkfUL | 2026-11-09 | `6abbdf5a211a743fa6983789767aca193c1334c71ac7c4c266ed011a55347d84` | anonymous Pastebin user (map "Kuusou Mesorogiwi", converted) | Pastebin paste, no licence stated | Robeats songmap converted from osu: placeholder AudioAssetId, `note`/`hold` helpers, long TimingPoints list |
