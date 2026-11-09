# VOEZ chart set (info / note / track JSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

VOEZ charts are a set of JSON files per song, produced and consumed by AndrewFM's **VoezEditor** (Unity). The format mirrors what the game stores in its asset bundles (the Switch version loads them from AssetBundles; the editor exports exactly the files below). Source: VoezEditor's `ProjectData.cs` (reader/writer) and its export manual; no official spec.

## Container & encoding

Per song folder: `info_song.json`, `note_easy.json`, `note_hard.json`, `note_extra.json` (Special), `track_easy.json`, `track_hard.json`, `track_extra.json`, a `config`-style text file (`id=...`, `name=...`, `bpm=...`, `author=...`, `diff=easy-hard-extra`, `version=...`), `song_full.mp3`, `song_pv.mp3` (20 s preview), `image_regular.png` (1024x1024), `image_blur.png` (256x256), `image_thumbnail.png` (256x256). For the Switch these are packed into a Unity AssetBundle `songs/<name>`. UTF-8 JSON.

## Structure / metadata

`info_song.json`: `{ "info": { "version", "song_version", "id" (24-digit string), "author", "bpm" (number), "name" }, "level": { "easy", "hard", "extra" } }`.

`note_<diff>.json` - array of notes sorted by time: `{ "Id": int, "Type": "click"|"hold"|"swipe"|"slide", "Track": int, "Time": float, "Hold": float (0.0 unless hold), "Dir": int }` (`Dir` meaning not documented; swipe direction presumably).

`track_<diff>.json` - array of tracks sorted by `Start`: `{ "Id", "EntranceOn": bool, "PositionLock": bool, "X": float, "Size": float, "Start": float, "End": float, "Color": int, "Move": [...], "Scale": [...], "ColorChange": [...] }`; the three lists contain transformations `{ "To": float, "Ease": string, "Start": float, "End": float }` (for `ColorChange` `To` is an int colour id). Editor colour names in order: Red, Yellow, Gray, Light Blue, Green, Orange, Violet, Blue, Cyan, Purple [inference: id order].

Ease strings: `easelinear`, `easeinexpo`, `easeoutexpo`, `easeinoutexpo`, `easeoutinexpo`, `easeinquad`, `easeoutquad`, `easeinoutquad`, `easeoutinquad`, `easeincirc`, `easeoutcirc`, `easeinoutcirc`, `easeoutincirc`, `easeoutback`, `easeinback`, `easeinoutback`, `easeoutinback`, `easeintelastic` (sic), `easeoutelastic`, `easeinoutelastic`, `easeoutinelastic`. The editor re-saves `easeinoutback` for float transformations as an `easeinback` + `easeoutback` pair because the original is "glitched" in the game.

## Timing model

`Time`, `Hold`, `Start`, `End` are floats in **seconds** from the start of the song (the editor compares them with `songTime` in seconds); the BPM in `info_song.json` is only used for the editor's grid/metronome [inference from editor code]. Notes spawn `NOTE_DURATION` seconds before their time and travel along their track.

## Notes

Click (tap), Hold (`Hold` seconds; hold ticks every fixed interval in the editor), Swipe, Slide. A note references a track by id (`Track`); the track defines the note's horizontal position over time (`X` plus `Move` keyframes, `Size` plus `Scale` keyframes). Track ids are re-numbered by `Start` order on save and note `Track` values are re-linked accordingly.

## Audio & images

File names fixed as listed above; `song_pv` must be exactly 20 s per the manual.

## Versions & variants

Editor supports a `ProjectMigrator`; Switch and mobile builds use the same JSON layout (not verified for mobile).

## Quirks & pitfalls

- Track must be exported before notes (ids change).
- Writers use string concatenation, so the JSON is irregular (no whitespace guarantees); the editor parses by splitting on `]},`.
- `easeinoutback` bug workaround (see above).

## Example

Illustrative, hand-built from the field list above (not a real chart):

```json
// note_hard.json
[{"Id":0,"Type":"click","Track":0,"Time":1.5,"Hold":0.0,"Dir":0}]
// track_hard.json
[{"Id":0,"EntranceOn":true,"PositionLock":false,"X":0.5,"Size":0.2,"Start":0.0,"End":10.0,"Color":0,"Move":[],"Scale":[],"ColorChange":[]}]
```

## ROX support

Not read by ROX.

## Parsers & tools

VoezEditor (C#, Unity): <https://github.com/AndrewFM/VoezEditor>; VOEZ JSON parser by the same author discussed on GBAtemp.

## Getting samples

Committed: a synthetic mini song (info, config, hard + extra notes/tracks) built from the VoezEditor writer code ([`samples/`](samples/)). Real data: VoezEditor has no LICENSE file and no sample project; official charts are copyrighted (Rayark). To get real files: use VoezEditor's export (`README/export.html`, `usage.html` in its repository) on the Switch assets, or dump the game's AssetBundle `songs/<name>` as described in the fiche; see also the GBAtemp thread cited in Sources.

## Sources

- <https://cdn.jsdelivr.net/gh/AndrewFM/VoezEditor@master/Assets/Scripts/ProjectData.cs>
- <https://cdn.jsdelivr.net/gh/AndrewFM/VoezEditor@master/README/export.html> and `usage.html`
- <https://gbatemp.net/threads/voez-custom-songs.509678/> (listed, not read)
