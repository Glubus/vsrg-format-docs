# Kade Engine chart JSON (`<song><-difficulty>.json`, chart version `KE1`)
Kind: chart

Doc status: partial · ROX: no dedicated codec (the legacy codec reads the subset it knows; `eventObjects`-based BPM changes are not understood) · Category: vsrg · Encoding: json

## Overview

Kade Engine (Kade-github) is an FNF mod engine with its own chart editor. Its chart is the legacy layout ([../legacy-json/README.md](../legacy-json/README.md)) plus `eventObjects` (BPM and scroll-speed changes, positioned in beats), `songId`, `chartVersion`, `noteStyle`, `offset`. Sources: `source/Song.hx`, `Section.hx`, `PlayState.hx` on `master` (`Song.latestChart = "KE1"`).

## Container & encoding

- UTF-8 JSON `{ "song": { ... } }` (`parseJSONshit` reads `jsonData.song`); `loadFromJsonRAW` trims trailing characters until the text ends with `}`.
- Files: `songs/<songId>/<songId><difficulty>.json` (difficulty appended directly, e.g. `-hard`) plus `songs/<songId>/_meta.json` (`Paths.loadJSON('songs/$songId/$songId$difficulty')` and `.../_meta`).
- `_meta.json` (`SongMeta`): `{ "name": <display name>, "offset": <int ms> }`; `songName` defaults to the song id with dashes replaced by spaces, `offset` to 0.

## Structure / metadata

`SongData` (`Song.hx`):

| Field | Type | Meaning |
|---|---|---|
| `song` | string (deprecated) | old song name |
| `songName`, `songId` | string | set from `_meta.json` and the file location |
| `chartVersion` | string | `"KE1"` after load; absent in vanilla-derived charts (treated as unconverted) |
| `notes` | array of `SwagSection` | |
| `eventObjects` | array of `Event` | BPM changes, scroll changes (below) |
| `bpm`, `speed` | float | |
| `needsVoices` | bool | |
| `player1`, `player2`, `gfVersion` | string | characters (default `gfVersion` `gf`) |
| `noteStyle` | string | default `normal` |
| `stage` | string | |
| `validScore`, `offset` | optional | |

`SwagSection` adds to the legacy one: `startTime`, `endTime` (floats), `CPUAltAnim`, `playerAltAnim` (bools) next to `sectionNotes`, `lengthInSteps`, `typeOfSection`, `mustHitSection`, `bpm`, `changeBPM`, `altAnim`.

`Event`: `{ name: string, position: float (in BEATS), value: float, type: string }`. Types seen in the source: `"BPM Change"` (value = new BPM) and `"Scroll Speed Change"` (value = scroll multiplier; handled in `PlayState`). The first event is created as `Event("Init BPM", 0, song.bpm, "BPM Change")` when `eventObjects` is missing.

## Timing model

- `eventObjects` of type `"BPM Change"` define `TimingStruct`s in beats: `addTiming(beat, bpm, endBeat, startTime)`; each segment has `startBeat`, `bpm`, `startStep`, `startTime` (SECONDS), `length` (beats). `getBeatFromTime(ms)` = `seg.startBeat + (ms/1000 - seg.startTime) * (seg.bpm / 60)`; `getTimeFromBeat` is the inverse. Kade's real tempo map is this event list, not the per-section `changeBPM`.
- Charts without `chartVersion` are converted at load (`conversionChecks`): section `changeBPM` becomes `"FNF BPM Change <index>"` events at beat `4 * index` (4 beats per section) and every note gets `[3] = false`, `[4] = beat`.
- Sustain length: `TimingStruct.getTimeFromBeat(getBeatFromTime(songNotes[2]))`.
- Sections are 16 steps (`lengthInSteps`); times are absolute ms as in vanilla.

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, isAlt, beat]`:

| Index | Meaning |
|---|---|
| 0 | `strumTime` ms (divided by the song rate multiplier at load) |
| 1 | `noteData`: `% 4` is the lane |
| 2 | sustain length ms |
| 3 | `isAlt` (bool): alternate animation (old charts: `false`) |
| 4 | `beat` the note sits on (float) |

Strumline ownership is the legacy rule: lane > 3 with `mustHitSection`, or lane < 4 without it, is the opponent's (`gottaHitNote = false`). Alt animation also applies when `section.altAnim || CPUAltAnim` (opponent notes) or `playerAltAnim` (player notes). Negative times clamp to 0 at load.

## Audio & images

External (`Inst.ogg`, `Voices.ogg`).

## Versions & variants

`chartVersion`: absent (vanilla-compatible, converted at load) or `"KE1"` (`Song.latestChart`). Other releases and branches were not inspected. Moonchart implements the format as `FNFKade`.

## Quirks & pitfalls

- Beat numbers (`[4]`) and `eventObjects` positions are in beats; everything else is ms.
- `[3]` is a bool here, an int/type in Psych.
- `eventObjects` wins over section `changeBPM` in KE1 charts; scroll speed changes are events.

## Example

Hand-built from `Song.hx` (not a real file):

```json
{ "song": { "songName": "Test", "songId": "test", "chartVersion": "KE1",
  "bpm": 120, "speed": 2.0, "needsVoices": true,
  "player1": "bf", "player2": "dad", "gfVersion": "gf", "noteStyle": "normal", "stage": "stage",
  "eventObjects": [ { "name": "Init BPM", "position": 0, "value": 120, "type": "BPM Change" } ],
  "notes": [ { "startTime": 0, "endTime": 2000, "lengthInSteps": 16, "mustHitSection": true,
               "changeBPM": false, "bpm": 120, "altAnim": false, "typeOfSection": 0,
               "sectionNotes": [ [0, 0, 0, false, 0], [500, 2, 250, false, 1] ] } ] } }
```

## ROX support

`.json` goes to the legacy FNF codec ([../legacy-json/README.md](../legacy-json/README.md)): notes decode (same lane rule), `bpm` is the initial BPM, section `changeBPM` points land at the section's first note. `eventObjects`, `chartVersion`, `_meta.json` and the `[3]`/`[4]` slots are ignored, so charts with several tempo events get wrong BPM points [inference].

## Parsers & tools

- Kade Engine (Haxe): https://github.com/Kade-github/Kade-Engine
- Moonchart `FNFKade` (Haxe): https://github.com/MaybeMaru/moonchart

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: https://github.com/Perkedel/Kaded-fnf-mods (`assets/preload/data/songs/`, about 200 JSON files, many with `chartVersion`); run Kade Engine and save from its chart editor. Perkedel files: note arrays of 3, 5 or 6 elements (`[time, lane, sustain, isAlt, beat, 0]`), event objects with `value2`/`value3`, mod fields (`videoPath`, `hasVideo`, `isCreditRoll`, `sectionLengths`...), 34 BPM-change events in `perkedel_heartbreaking.json`.

## Sources

- https://raw.githubusercontent.com/Kade-github/Kade-Engine/master/source/{Song,Section,TimingStruct,PlayState}.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/FNFKade.hx (listed, not read in detail)
