# Kade Engine chart JSON (`<song><-difficulty>.json`, chart version `KE1`)
Kind: chart

Doc status: partial · ROX: no dedicated codec (the legacy codec reads the subset it knows; `eventObjects`-based BPM changes are not understood) · Category: vsrg · Encoding: json

## Overview

Kade Engine (Kade-github) is a FNF mod engine with its own charting editor, replays and accuracy ratings. Its chart file is the legacy layout ([../legacy-json/README.md](../legacy-json/README.md)) with extra fields: BPM changes and scroll-speed changes as `eventObjects` positioned in beats, `songId`, `chartVersion`, `noteStyle`, `offset`. Sources: `source/Song.hx`, `source/Section.hx`, `source/PlayState.hx` of the `master` branch of Kade-github/Kade-Engine (`Song.latestChart = "KE1"`).

## Container & encoding

- UTF-8 JSON `{ "song": { ... } }` (`parseJSONshit` reads `jsonData.song`); like vanilla, `loadFromJsonRAW` trims trailing characters until the text ends with `}`.
- Files: `songs/<songId>/<songId><difficulty>.json` (the difficulty string is appended directly, e.g. `-hard`) plus `songs/<songId>/_meta.json` (`loadFromJson`: `Paths.loadJSON('songs/$songId/$songId$difficulty')` and `.../_meta`).
- `_meta.json`: `{ "name": <display name>, "offset": <int ms> }` (`SongMeta`); `songName` defaults to the song id with dashes replaced by spaces, `offset` to 0.
- Audio separate.

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

- `eventObjects` of type `"BPM Change"` define `TimingStruct`s in beats: `addTiming(beat, bpm, endBeat, startTime)`; each segment has `startBeat`, `bpm`, `startStep`, `startTime` (SECONDS), `length` (beats). `TimingStruct.getBeatFromTime(ms)` = `seg.startBeat + (ms/1000 - seg.startTime) * (seg.bpm / 60)`; `getTimeFromBeat` is the inverse. So Kade's real tempo map is the beat-based event list, not the per-section `changeBPM`.
- Charts without `chartVersion` are converted at load (`conversionChecks`): section `changeBPM` become `"FNF BPM Change <index>"` events at beat `4 * index` (each section is assumed 4 beats), and every note gets `[3] = false`, `[4] = beat` computed from its ms time.
- Sustain length: `TimingStruct.getTimeFromBeat(getBeatFromTime(songNotes[2]))` (converted through the BPM map).
- Section lengths are 16 steps (`lengthInSteps`), times absolute ms as in vanilla.

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, isAlt, beat]`:

| Index | Meaning |
|---|---|
| 0 | `strumTime` ms (divided by the song rate multiplier at load) |
| 1 | `noteData`: `% 4` is the lane |
| 2 | sustain length ms |
| 3 | `isAlt` (bool): alternate animation (old charts: `false`) |
| 4 | `beat` the note sits on (float) |

Strumline ownership uses the legacy rule: lane > 3 with `mustHitSection`, or lane < 4 without it, is the opponent's (`gottaHitNote = false`); the opposite is the player's. An alt animation is also applied when `section.altAnim || CPUAltAnim` for opponent notes or `playerAltAnim` for player notes. Negative times are clamped to 0 at load.

## Audio & images

External (`Inst.ogg`, `Voices.ogg`); no references inside the chart.

## Versions & variants

`chartVersion`: absent (vanilla-compatible, converted at load) and `"KE1"` (`Song.latestChart`). Other Kade releases / branches were not inspected and may differ. Moonchart implements this format as `FNFKade`.

## Quirks & pitfalls

- Beat numbers (`[4]`) and `eventObjects` positions are in beats; everything else is in ms.
- `[3]` is a bool here, an int/type in Psych.
- Two competing BPM mechanisms (`changeBPM` sections vs `eventObjects`); the latter wins in KE1 charts.
- Scroll speed changes are events.

## Example

Illustrative, hand-built from `Song.hx` (not a real file):

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

`.json` goes to the legacy FNF codec ([../legacy-json/README.md](../legacy-json/README.md)): `song.notes[].sectionNotes` and `mustHitSection` are read (the lane rule is identical, so notes decode), `bpm` becomes the initial BPM and section `changeBPM` points are placed at the first note of the section; `eventObjects` (the real tempo map), `chartVersion`, `_meta.json`, `[3]`/`[4]` note slots are ignored. Charts with several tempo events decode with wrong BPM points [inference from the two sources].

## Parsers & tools

- Kade Engine (Haxe): https://github.com/Kade-github/Kade-Engine
- Moonchart `FNFKade` (Haxe): https://github.com/MaybeMaru/moonchart

## Getting samples

- Committed: [samples/](samples/): a synthetic KE1 chart with `eventObjects` and its `_meta.json`-style companion.
- Manifest: four charts of the Kade-github/Kade-Engine repository (commit `b1fe905d9cfdcd10705f48ff47d62d1165d6c63a`, Apache-2.0 code; base-game charts not redistributed). They carry NO `chartVersion` and no `eventObjects` [observed], i.e. they are the unconverted layout the engine converts at load; a real KE1 file (with `eventObjects`) was NOT found in any public repository.
- How to get a real KE1 file: run Kade Engine (build from the repository), open its chart editor and save a song; the engine writes `songs/<songId>/<songId><difficulty>.json` [inference from `Song.hx` as described above]. Kade releases are listed on https://github.com/Kade-github/Kade-Engine (not opened).

## Sources

- https://raw.githubusercontent.com/Kade-github/Kade-Engine/master/source/{Song,Section,TimingStruct,PlayState}.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/main/src/moonchart/formats/fnf/FNFKade.hx (listed, not read in detail)
