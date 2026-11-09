# Vulnus map (`meta.json` + difficulty `.json`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
Vulnus maps are folders: `meta.json` (song metadata, list of difficulty files), one JSON per difficulty with `_notes`, an audio file and `cover.png`. Known only from the importer in Sound Space Plus (`Song.gd`: `load_from_vulnus_map`, `setup_from_vulnus_json`, `loadVulnusNoteArray`); the file `official.json` is the name of the official-map difficulty file there.

## Container & encoding
Folder of JSON files (text), audio next to them. One `meta.json` per map set; one difficulty JSON per difficulty.

## Structure / metadata
`meta.json` keys read by SS+: `_artist`, `_title`, `_mappers[]`, `_music` (audio filename, must be a valid filename in the folder), `_difficulties[]` (difficulty JSON filenames). Difficulty JSON keys read by SS+: `_name` (difficulty name), `_notes[]`, with `_time`, `_x`, `_y` per note. Other keys: Unknown.

## Timing model
`_time` is in **seconds** (SS+ multiplies by 1000 to get ms). No BPM data used.

## Notes
Tap-only grid notes. SS+ maps `x_internal = 2 - (_x + 1)`, `y_internal = 2 - (_y + 1)` (so `_x`, `_y` are centered around 0: -1, 0, 1 for the 3 x 3 grid, floats allowed). Missing `_time`/`_x`/`_y` count as invalid notes.

## Audio & images
`_music` file; `cover.png`.

## Versions & variants / Quirks & pitfalls
Unknown. SS+ finds the last note by text search of `"_time"` in the file (importer implementation detail, not a format rule).

## Example
Illustrative, hand-built from the rules above: `{ "_name": "Easy", "_notes": [ { "_time": 1.5, "_x": 0, "_y": 0 } ] }`

## ROX support
Not read by ROX.

## Parsers & tools
- Sound Space Plus importer: https://github.com/Rhythia/sound-space-plus

## Getting samples

Committed: a synthetic map (meta + two difficulties) following the keys read by the Sound Space Plus importer ([`samples/`](samples/)). Real Vulnus maps are folders with audio and `cover.png` shared by the community (no stated licence); no stable public archive was identified, so none is listed. Vulnus itself is on itch.io (ducc); Rhythia/SS+ can import Vulnus folders (`load_from_vulnus_map` in `Song.gd`).

## Sources
- https://raw.githubusercontent.com/Rhythia/sound-space-plus/HEAD/scripts/content/game/Song.gd
