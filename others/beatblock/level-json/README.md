# Beatblock level (`level.json` and chart JSON)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview

A Beatblock custom level is a folder (`%appdata%/Beatblock/Custom Levels`, `~/Library/Application Support/Beatblock/Custom Levels` or `~/.local/share/beatblock/Custom Levels`) of JSON files written by the in-game editor. No standalone parser or public schema exists. This page rests on the official editor guide, the early-access technical notes (property names of every event), the community guide, and real level packages (see "Unknown").

## Container & encoding
- JSON, UTF-8. From format version 15/17 on, files are saved pretty-printed ("saved jsons now have formatting applied", technical notes); earlier versions wrote a single line.
- Folder contents: level/chart JSON files, the audio (`.ogg` Vorbis preferred, `.wav` usable, MP3 no longer usable), optional decoration spritesheets (`.png` + same-name `.json` animation file), GLSL files for shaders, custom sprites/fonts, a `tags/` folder with `<tag>.json` event lists created by "Change to tag" (editor guide).
- A level can contain several charts (the guide mentions "Variant Specific" properties; the paddle event moved "to chart instead of level" in format v16, which implies a level file plus chart file(s)). [inference: exact file names unknown except `level.json`, mentioned by users]
- Distribution: `.zip` (preferred) or `.7z` of the folder; also dragging a zip onto the window or Steam Workshop.

## Structure / metadata
- Level properties (Ctrl+I): title, subtitle/description, charter, difficulty and a song-select background (must fit the eight-colour palette); a "METADATA" section and Variant Specific, BG and OTHER sections (guide). Text fields can hold rich-text triggers.
- Format versions listed in the technical notes: v15 (eight-channel effect canvas colours), v16 (paddle event stored in the chart), v17 (`effectCanvasRaw` forced on in old decorations). Backwards-compat flags: `vfx.effectCanvas.oldColors`, `forceStoreInLevel`, `newHoldDetection`.
- Events are objects with a `type` string and per-type properties. A user-quoted sample (Beatblock-Utilities README, as reported by a search result; the repository page was not retrievable by me): `{"type":"mine","time":1,"angle":90}`. Property names below are those of the editor's event panel and are probably the JSON keys [inference].

## Timing model
- `time` is a beat position ("On which beat will the item hit Cranky") and may be fractional (decimals, so triplets are typed as fractions of a beat). The editor snaps to 1/4, 1/3, 1/6, 1/12 subdivisions.
- A "Play song" event starts the audio and holds its file name, BPM and start offset; "Set BPM" changes tempo mid-song. So tempo and offset are events on the beat timeline, not header fields.
- `duration` (holds, eases) and `delay` (bounces) are in beats. Ease sequences use "distance in beats" before the hit (time -1 = 1 beat away; time 0 = hit).
- Beat to seconds requires walking the tempo events: `seconds = offset + beats * 60 / BPM` within each BPM segment. [inference from the editor description]

## Notes
Properties per note event (editor guide, "Events > Notes section"):

| Event | Properties |
|---|---|
| Block, Side, Inverse, Mine | `time`, `angle`, `order`, `endAngle`, `spinEase`, `speedMult`, `tap` (not on Mine), `color0` (fill), `color1` (outline), `easeSequence` |
| Bounce | `time`, `angle`, `order`, `bounces`, `delay`, `rotation`, `tap`, `endAngle`, `spinEase`, `speedMult`, `heightMult`, `easeSequence` |
| Hold, Mine Hold | `time`, `angle`, `angle2` (end angle), `order`, `duration`, `segments`, `holdEase`, `endAngle`, `spinEase`, `speedMult`, `startTap`, `endTap`, `easeSequence`, `taileaseSequence` (sic); Mine Hold adds `tickRate` |
| Extra Tap | `time`, `angle` (organisation only), `order`, `speedMult`, `color1`, `easeSequence` |
| Trace (dev-only) | dithered line between two points |

- `angle` is the rotation angle (degrees) the note arrives from; `order` is draw priority.
- Other events: Ease (`var`, `start`, `value`, `duration`, `ease`, `repeats`, `repeatDelay`), Ease Sequence (`name`), Decoration, Hall of Mirrors, Noise, Set Color, Edit Player, AFT, Stamp, New/Edit canvas, Deco/Shader Uniform, Text decoration, Edit Paddle, Set Bounce Height, Bookmark/Comment, Tags/Run tag, Play Song, Play Sound, Set BPM, Show Results (ends the level), Set Bool.
- Eases drive named variables (`vfx.*`, `p.*`, `bounceHeight`, ...) and booleans (`paused`, `vfx.drawCombo`, `newHoldDetection`, ...); the full lists are in the guide.
- The score: hold detection changed in early access ("holds die faster ... `newHoldDetection`").

## Audio & images

Audio file name is a property of the Play Song event (`.ogg` preferred); offset is set there or by trimming the audio. Decorations: PNG spritesheet + same-name JSON (`states`, fps). Shaders: `.glsl` files in the level folder. Play Sound plays audio from the level or the base game.

## Versions & variants

Demo (0.4.x) versus early access (format v15+). Dev-only events (Init Object, Single/Multi Pulse, Parallax BG, Play Midi, Set Background, Set Joystick Color, Trace, Video Background; deprecated: Spawn Beat, Paddle Count, Change Width) stay hidden unless the game's `DEVONLY` marker files are removed.

## Quirks & pitfalls

- Guide property names such as `taileaseSequence` contain typos; whether the JSON spells them the same is unverified.
- Format version bumps change behaviour via boolean flags; old levels must keep them.
- MP3 audio no longer loads.

## Unknown
Resolved by real packages [observed in samples/*/level.json, format versions 12 to 14]: `level.json` has top-level keys `properties` (`speed`, `offset`, `formatversion`, `loadBeat`/`startBeat`/`startingBeat`) and `events` (`play`, `setBPM`, `setColor`, `setBgColor`, `ease`, `deco`, `paddles`, `tag`, `bookmark`, `showResults`, ...), and sometimes `metadata`; the chart is a separate JSON array of note objects with `time` (beats), `angle` and `type` (`block`, `inverse`, `side`, `hold`, `mineHold`, `mine`, `extraTap`; holds add `angle2`, `duration`; also `tap`, `startTap`, `endTap`, `speedMult`, `spinEase`, `holdEase`, `segments`, `order`); `manifest.json` has `metadata`, `properties`, `variants[]` (`display`, `difficulty`, `charter`, `name`) and `defaultVariant`, and the chart file is named `chart-<variant name>.json` (or plain `chart.json`). Still Unknown: version history, the exact semantics of most event fields, any checksum.

## Example

Synthetic level: `samples/synthetic-level.json`, `samples/synthetic-chart-Synthetic.json`, `samples/synthetic-manifest.json` (see `samples/SOURCES.md`). The single-event sample under "Structure / metadata" is the only quoted fragment.

## ROX support

Not read by ROX. Mapping to columns would discard `angle` and most events.

## Parsers & tools
- In-game level editor (official).
- Beatblock-Utilities (event randomizer etc., reported): https://github.com/K4kadu/Beatblock-Utilities
- BetterBrowser (scraper for Beatblock Browser level lists): https://github.com/BeatblockTools/BetterBrowser

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (https://github.com/ItsBritex/beatblock-levels, plus synthetic files). Levels are written by the in-game editor into the custom levels folder (paths in Overview) and shared as `.zip` via the Steam Workshop, https://beatblockbrowser.me/ (TLS errors when checked) and Discord. Observed layout (formats 12-14): `level.json` (`properties`, `events`, optionally `metadata`), a chart file that is a JSON array of notes (`chart.json` or `chart-<variant>.json`), optional `manifest.json`, `backup/`, `tags/`.

## Sources
- https://docs.google.com/document/d/1myd85jpTYQCtE1Mlu6fJEm3fJEIN_-7Q1TFcB1OcrT4 (Editor Guide, exported as text)
- https://docs.google.com/document/d/1MiFn-mzv8NbKYYSU0lSAbWsx_wjX6T3rmNaB8YXMYJI (technical notes, exported as text)
- https://github.com/Modblock/bblock-guide
- https://beatblock.wiki.gg/wiki/Custom_Levels
