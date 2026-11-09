# RoBeats custom-server song map (Roblox Lua ModuleScript)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (Lua source code)

## Overview

In the open-source RoBeats Custom Server Template (spotco, 2020; last commit seen 2026), each song is a ModuleScript under `Workspace/SongMaps/` that builds and returns a Lua table. There is no separate file extension: the "file" is a Roblox `ModuleScript` instance (in the Rojo repository a `.lua` file). The list of playable songs is `Workspace/SongMapList.lua`, a Lua table of references to those modules. The song's audio is a Roblox asset id, not a file. Source: `Workspace/SongMaps/{MondayNightMonstersNormal,MondayNightMonstersHard,TestingMap}.lua`, `ReplicatedStorage/RobeatsGameCore/{SongDatabase,SongErrorParser,AudioManager}.lua`.

## Container & encoding

- A `.lua` text file (Rojo layout) or a ModuleScript inside a Roblox place (`.rbxl`/`.rbxlx`). It is executable code: `require(songModule)` runs it. The template loads each song via a cloned module (`require_module_clone`) and then destroys the clone. A parser outside Roblox must therefore either interpret the Lua table-constructor subset used here or run a Lua interpreter (sandboxed: the file is arbitrary code).
- One module per difficulty ("MondayNightMonstersNormal", "MondayNightMonstersHard" are two separate modules of the same audio).
- Song id = position in `SongMapList` (comments in the list: "song id: 1/2/3").

## Structure / metadata

Header fields set on the returned table `rtv` (from the three shipped songs):

| Field | Type | Meaning |
|---|---|---|
| `AudioAssetId` | string | Roblox audio asset, `"rbxassetid://<id>"` |
| `AudioFilename` | string | display name (also used in error messages) |
| `AudioDescription` | string | |
| `AudioCoverImageAssetId` | string | `rbxassetid://...` or a `rbxasset://` placeholder |
| `AudioArtist` | string | |
| `AudioDifficulty` | number | displayed difficulty rating (1 and 14 in the shipped songs) |
| `AudioTimeOffset` | number ms | added to the audio time (`-75` in all shipped songs) |
| `AudioVolume` | number 0-1 | `0.5`; optional (default 0.5 in `AudioManager`) |
| `AudioNotePrebufferTime` | number ms | how long before its hit time a note is spawned (`1500`), divided by the player's note speed |
| `AudioMod` | int | `0` normal, `1` supporter-only (`SongDatabase.SongMode`: `Normal = 0`, `SupporterOnly = 1`) |
| `AudioHitSFXGroup` | int | id of the hit sound-effect group (0..; `HitSFXGroup.lua`, e.g. 0 = tambourine, 1 = hi-hat variants, 2 = drum, 3 = clap) |
| `HitObjects` | array | notes, below |
| `TimingPoints` | array, optional | `{ Time = ms; BeatLength = ms }`; the template only uses the FIRST entry's `BeatLength` to display `BPM = floor(60000 / BeatLength + 0.5)` (`calculate_bpm`). Optional extra header fields consumed by the template: `BPM`, `HitCount`, `HitObjectsCount`, `LastNoteTime` (computed if absent) |

## Timing model

Absolute milliseconds from the start of the audio (`Time`); the engine adds `AudioTimeOffset` plus the player's/global audio offset to the audio position (`get_current_time_ms`). A pre-start countdown shifts notes by `_pre_countdown_time_ms`. No BPM-based positioning: `TimingPoints` is informational (BPM display); no scroll velocity changes, no stops.

## Notes

Every `HitObjects[i]` is a table with `Time` (ms), `Type`, `Track`, and for holds `Duration`:

| `Type` | Meaning | Fields |
|---|---|---|
| `1` | single note | `Time`, `Track` |
| `2` | held note | `Time`, `Track`, `Duration` (ms) |

- `Track` is an integer 1..4 (`GameTrack.Track1..Track4`, mapped to the 4 keys; `AssertType:is_int(track_number)`).
- Maps are written by helper calls, e.g. in the shipped files: `local function note(time,track) rtv.HitObjects[#rtv.HitObjects+1]={Time=time;Type=1;Track=track;} end` and `local function hold(time,track,duration) ... {Time=time;Type=2;Track=track;Duration=duration;} end`, then `note(420,1)`, `hold(8370,1,450)`, one per line with a trailing `--<index>` comment; or direct table inserts (`rtv.HitObjects[#rtv.HitObjects + 1] = { Time = 0; Type = 1; Track = 1; } --#0`).
- Objects must be sorted by `Time`: `update_spawn_notes` stops scanning at the first object that is not yet due.
- Scoring counts: a single note = 1 hit, a held note = 2 (`calculate_hit_count`, `_note_count`).
- Validation (`SongErrorParser:scan_audiodata_for_errors`): a repeated (track, time) pair, or a hold end that lands on an existing (track, time) pair, raises an error ("Likely duplicate time/track note"). [the key is built as `string.format("%d_%d", p_track, p_time)` but called as `(Time, Track)`, swapped; still unique per pair]. A missing `Track` gets a temporary id (assigned from a counter starting at 4).
- No mines, no keysounds per note; only the song-wide `AudioHitSFXGroup`.

## Audio & images

Roblox asset ids (`rbxassetid://...`) for the song and cover; the audio is hosted by Roblox, so the chart cannot be played without the uploaded audio (the template README/forum notes the included song needs re-uploading after Roblox's 2022 audio permission change). Hit sounds are built-in SFX groups.

## Versions & variants

No version field. The template repository changed over time (115 commits); the schema above is the one of the current files. The official RoBeats game may use a different internal format: Unknown.

## Quirks & pitfalls

- It is code: `;` or `,` separators inside table constructors are both used (`{Time=time;Type=1;Track=track;}`), comments `--`.
- Track numbers are 1-based.
- Hold `Duration` is a length, not an end time.
- Duplicate (track,time) pairs are rejected at load.
- `AudioTimeOffset` is negative in the samples (notes 75 ms earlier relative to the audio).
- The same audio can appear in several modules (one per difficulty).

## Example

Real excerpt of the template's `TestingMap.lua` (spotco/RobeatsCustomServerTemplate), shortened:

```lua
local rtv = {}
rtv.AudioAssetId = "rbxassetid://654442447"
rtv.AudioFilename = "Welcome to Monday Night (Debug)"
rtv.AudioTimeOffset = -75
rtv.AudioNotePrebufferTime = 1500
rtv.AudioHitSFXGroup = 0
rtv.HitObjects = {}
rtv.HitObjects[#rtv.HitObjects + 1] = { Time = 0; Type = 1; Track = 1; }
rtv.HitObjects[#rtv.HitObjects + 1] = { Time = 0; Type = 1; Track = 2; }
rtv.HitObjects[#rtv.HitObjects + 1] = { Time = 500; Type = 1; Track = 3; }
rtv.TimingPoints = { [1] = { Time = 0; BeatLength = 500; }; };  -- 120 BPM
return rtv
```

(the real file also defines `AudioDescription`, cover, artist, difficulty, volume, mode and ~9 objects.)

## ROX support

Not read. Mapping to ROX would be direct: `Track - 1` -> column of a 4K chart, `Type 1` -> Tap, `Type 2` -> Hold (`Duration` ms -> us), BPM from `TimingPoints[1]`, `AudioTimeOffset` -> `audio_offset_us` (ms -> us, sign to be checked). The obstacle is the container: Lua code, not data.

## Parsers & tools

- Template engine (Lua): https://github.com/spotco/RobeatsCustomServerTemplate
- The Roblox forum post describes the template: https://devforum.roblox.com/t/open-source-robeats-rhythm-game-custom-server-template/824563
- RoBeats wiki mentions community osu!-based map creation workflows for the custom server (the page `RoBeats_Custom_Server` returned HTTP 403 to the fetcher; only a search snippet was seen: "Go to the osu! Song Folder of the map, and upload t...", so the converter itself is not identified).

## Getting samples

- **Committed** ([`samples/`](samples/), see [`SOURCES.md`](samples/SOURCES.md)): the three songmaps of `spotco/RobeatsCustomServerTemplate` (commit `df8f4d3145ed474ad92b4371d030ee73d003b250`) and one converted map from Pastebin (https://pastebin.com/EkQrkfUL).
- **More**: the Robeats wiki (https://robeats.fandom.com/wiki/RoBeats_Custom_Server) explains converting a `.osu` into a songmap. The repositories `RoVSRG/robeats-cs-legacy` (`songs/`), `RoVSRG/robeats-cs-maps` and `thenerdie/robeats-community-maps` are named by search results but now require authentication (private or removed), and Wayback has no copy of the files; community Roblox places hold songmaps as ModuleScripts.

## Sources

- https://github.com/spotco/RobeatsCustomServerTemplate (cloned; files listed in Overview)
- https://devforum.roblox.com/t/open-source-robeats-rhythm-game-custom-server-template/824563
- https://robeats.fandom.com/wiki/RoBeats! (search snippet)
