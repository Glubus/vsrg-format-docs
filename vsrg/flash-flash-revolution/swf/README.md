# FFR legacy level SWF (`level_<id>.swf`, "beatBox")
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (Flash SWF with AS1/2 bytecode)

## Overview

FFR's legacy engines store each song/chart as a Flash movie `level_<level_id>.swf` (`ChartFFRLegacy.songUrl`) with the audio and a chart array. R^3 extracts the chart without running Flash: `Beatbox.parseBeatbox` walks the SWF tags, interprets `DoAction` bytecode (constant pool, push, init-array, set-variable/member, registers) and returns `_root.beatBox`.

## Container & encoding

SWF (header + tags). The chart sits in a `DoAction` tag as ActionScript 1/2 bytecode assigning `_root["beatBox"]` an array of arrays.

## Structure / metadata

Each beat entry: `[frame, direction, color, ms?]`. `direction` in `'L','D','U','R'`; `color` string (default `"blue"`; colours encode quantization: red 4th, blue 8th, purple 12th, yellow 16th, pink 24th, orange 32nd, light blue 48th, green 64th, white 192nd, per FFR forum); optional 4th element = time in ms. Playlists are XML (`songname, songdifficulty, songlength, level, arrows, playhash, swfhash, ...`).

## Timing model

`frame` at 30 fps (`framerate=30` for legacy): `time = (frame + sync)/30` s where `sync` is a per-engine/level `arc_sync` offset; if a 4th element exists it overrides: `time = ms/1000`.

## Notes

Taps only, 4 directions, no holds; colour is cosmetic quantization.

## Audio & images

Embedded MP3 in the SWF ("SWF MP3 + Beatbox extraction" mode).

## Versions & variants

Legacy SWF versus the R^3 formats (SM/SSC/osu/Quaver parsers).

## Quirks & pitfalls

30 fps frame quantization; per-engine sync offsets; AS bytecode subset.

## Example

Illustrative: `_root.beatBox = [[30,"L","red"],[45,"R","blue"]]` (frames 30, 45 at 30 fps = 1.0 s and 1.5 s).

## ROX support

Not read by ROX.

## Parsers & tools

rCubed (ActionScript).

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md) (rewritten without audio, images and fonts: only the DoAction/SetBackgroundColor/FileAttributes/ShowFrame/End tags kept; plus one synthetic SWF). Source: `https://www.flashflashrevolution.com/game/r3/r3-songLoad.php?id=<playhash>`; `playhash` values come from the public playlist https://www.flashflashrevolution.com/game/r3/r3-playlist.php (JSON array of about 3600 songs with `level`, `playhash`, `arrows`, `author`, `stepauthor`). Any `playhash` works with the same URL (free songs). Legacy engines load `level_<level_id>.swf` from the engine's `songURL` (rCubed `ChartFFRLegacy.songUrl`).

Observed: downloads are zlib-compressed SWFs (`CWS`, version 6) or plain `FWS`; a level has several DoAction tags (one holds `_root.beatBox`); `beatBox` entries are `[frame, direction, colour]` or `[frame, direction, colour, ms]`; the beat count equals `arrows` of the playlist entry [observed].

## Sources

- https://github.com/flashflashrevolution/rCubed (src/classes/chart/parse/ChartFFRLegacy.as, src/com/flashfla/media/Beatbox.as, classes/chart/Note.as)
- https://www.flashflashrevolution.com/simfiles/ffr-simfile-database-update/
- https://www.flashflashrevolution.com/vbz/showthread.php?t=107328
