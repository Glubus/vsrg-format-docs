# VOEZ chart set (info / note / track JSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

JSON files per song, produced and consumed by AndrewFM's VoezEditor (Unity). The format mirrors the game's asset bundles (the Switch version loads AssetBundles). Source: VoezEditor's `ProjectData.cs` and its export manual; no official spec.

## Container & encoding

Per song folder: `info_song.json`, `note_easy.json`, `note_hard.json`, `note_extra.json` (Special), `track_easy.json`, `track_hard.json`, `track_extra.json`, a `config`-style text file (`id=...`, `name=...`, `bpm=...`, `author=...`, `diff=easy-hard-extra`, `version=...`), `song_full.mp3`, `song_pv.mp3` (20 s preview), `image_regular.png` (1024x1024), `image_blur.png` (256x256), `image_thumbnail.png` (256x256). For the Switch these are packed into a Unity AssetBundle `songs/<name>`. UTF-8 JSON.

## Structure / metadata

`info_song.json`: `{ "info": { "version", "song_version", "id" (24-digit string), "author", "bpm" (number), "name" }, "level": { "easy", "hard", "extra" } }`.

`note_<diff>.json`: array of notes sorted by time: `{ "Id": int, "Type": "click"|"hold"|"swipe"|"slide", "Track": int, "Time": float, "Hold": float (0.0 unless hold), "Dir": int }` (`Dir` meaning undocumented; swipe direction presumably).

`track_<diff>.json`: array of tracks sorted by `Start`: `{ "Id", "EntranceOn": bool, "PositionLock": bool, "X": float, "Size": float, "Start": float, "End": float, "Color": int, "Move": [...], "Scale": [...], "ColorChange": [...] }`. The three lists hold transformations `{ "To": float, "Ease": string, "Start": float, "End": float }` (for `ColorChange`, `To` is an int colour id). Editor colour names in order: Red, Yellow, Gray, Light Blue, Green, Orange, Violet, Blue, Cyan, Purple [inference: id order].

Ease strings: `easelinear`, `easeinexpo`, `easeoutexpo`, `easeinoutexpo`, `easeoutinexpo`, `easeinquad`, `easeoutquad`, `easeinoutquad`, `easeoutinquad`, `easeincirc`, `easeoutcirc`, `easeinoutcirc`, `easeoutincirc`, `easeoutback`, `easeinback`, `easeinoutback`, `easeoutinback`, `easeintelastic` (sic), `easeoutelastic`, `easeinoutelastic`, `easeoutinelastic`. For float transformations the editor re-saves `easeinoutback` as an `easeinback` + `easeoutback` pair because the original is "glitched" in the game.

## Timing model

`Time`, `Hold`, `Start`, `End` are floats in seconds from the start of the song (the editor compares them with `songTime` in seconds). The BPM in `info_song.json` only drives the editor's grid/metronome [inference from editor code]. Notes spawn `NOTE_DURATION` seconds before their time and travel along their track.

## Notes

Click (tap), Hold (`Hold` seconds; hold ticks every fixed interval in the editor), Swipe, Slide. A note references a track by id (`Track`); the track defines its horizontal position over time (`X` plus `Move` keyframes, `Size` plus `Scale` keyframes). Track ids are re-numbered by `Start` order on save and note `Track` values are re-linked.

## Audio & images

File names are fixed as above; `song_pv` must be exactly 20 s per the manual.

## Versions & variants

The editor has a `ProjectMigrator`. Switch and mobile builds use the same layout (mobile not verified).

## Quirks & pitfalls

- Export tracks before notes (ids change).
- Writers use string concatenation, so whitespace is irregular; the editor parses by splitting on `]},`.
- `easeinoutback` workaround (see above).

## Example

Hand-built from the field list (not a real chart):

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

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (synthetic only). No real VOEZ chart was obtained: official charts live in AssetBundles (not publicly downloadable), VoezEditor has no sample project or licence, and the voez.fandom.com blog and GBAtemp thread links are dead or audio only. Export from VoezEditor as its manual describes, or extract the Switch/mobile AssetBundles.

## Sources

- <https://cdn.jsdelivr.net/gh/AndrewFM/VoezEditor@master/Assets/Scripts/ProjectData.cs>
- <https://cdn.jsdelivr.net/gh/AndrewFM/VoezEditor@master/README/export.html> and `usage.html`
- <https://gbatemp.net/threads/voez-custom-songs.509678/> (listed, not read)
