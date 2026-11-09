# Psych Engine chart JSON (`<song>.json`, format `psych_v1`)
Kind: chart

Doc status: complete · ROX: no dedicated codec; the legacy codec reads both the old (pre-1.0) layout and `psych_v1` files (lane rule fixed 2026-10-28, see ROX support) · Category: vsrg · Encoding: json

## Overview

Psych Engine (ShadowMario and contributors) is a widely used FNF mod engine. Its chart is the legacy week JSON ([../legacy-json/README.md](../legacy-json/README.md)) plus events, `stage`, `gfVersion`, per-note types and, in current source, a `format` field marking normalised lanes. Source: `source/backend/Song.hx`, `source/states/PlayState.hx` (main).

## Container & encoding

- UTF-8 JSON. `Song.parseJSON` accepts `{ "song": { ... } }` (a `song` field of object type is unwrapped) and the bare object.
- Files: `data/<songFolder>/<song>[-<difficulty>].json` (`Paths.json('$formattedFolder/$formattedSong')`; names lower-cased, spaces to dashes by `Paths.formatToSongPath`). Optional `data/<songFolder>/events.json` holds extra events in the same `events` schema (`Song.getChart('events', songName)`).
- Audio is separate (`Inst.ogg`, `Voices.ogg`, optional `Voices-Player.ogg` / `Voices-Opponent.ogg`) [inference for the split vocal names].

## Structure / metadata

`SwagSong` (`Song.hx`):

| Field | Type | Meaning |
|---|---|---|
| `song` | string | song name |
| `notes` | array of `SwagSection` | notes |
| `events` | array | event list, see below |
| `bpm` | float | initial BPM |
| `needsVoices` | bool | |
| `speed` | float | scroll speed |
| `offset` | float | chart offset |
| `player1`, `player2`, `gfVersion` | string | characters (old files: `player3`, renamed on load) |
| `stage` | string | |
| `format` | string | `psych_v1` for current charts; absent/other = older layout, converted on load (`psych_v1_convert` is set while converting) |
| `gameOverChar`, `gameOverSound`, `gameOverLoop`, `gameOverEnd` | string, optional | |
| `disableNoteRGB` | bool, optional | |
| `arrowSkin`, `splashSkin` | string, optional | |

`SwagSection`: `sectionNotes` (array), `sectionBeats` (float, default 4; replaces `lengthInSteps`), `mustHitSection` (bool), optional `altAnim`, `gfSection` (notes of this section are sung by girlfriend), `bpm`, `changeBPM`.

## Timing model

As legacy: absolute ms; BPM from `bpm`, changes via section `changeBPM`+`bpm` (`PlayState.generateSong` keeps `daBpm`). Sustain step length is `60 / daBpm * 1000 / 4`. Sections are `sectionBeats` beats (default 4) instead of `lengthInSteps` (old files converted: `sectionBeats = 4`, `lengthInSteps` removed).

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, noteType?]`:

- `noteType`: a string in Psych 1.0 (custom names allowed). Older charts used an int index into `Note.defaultNoteTypes = ['', 'Alt Animation', 'Hey!', 'Hurt Note', 'GF Sing', 'No Animation']` (mapped during `convert` and again in `generateSong`).
- `psych_v1` lane semantics (changed from legacy): `noteData` 0-3 = the player's side (`mustPress`), 4-7 = the opponent's, regardless of `mustHitSection` (`PlayState`: `gottaHitNote = (songNotes[1] < totalColumns)`, `noteColumn = songNotes[1] % totalColumns`, `totalColumns = 4`). `Song.convert` rewrites old charts to this: `gottaHit = (note[1] < 4) ? section.mustHitSection : !section.mustHitSection; note[1] = (note[1] % 4) + (gottaHit ? 0 : 4)`. In a `psych_v1` file `mustHitSection` only drives the camera and the `gfSection`/`altAnim` logic.
- Sustain: `holdLength` ms; pieces `Math.round(holdLength / curStepCrochet)` (rounded, not floor as in vanilla).
- Ghost notes (same lane, type and time, within epsilon) are removed at load time (`ghostNotesCaught`).
- `gfNote = section.gfSection && gottaHitNote == section.mustHitSection`; `altAnim` applies to the opponent's notes of an `altAnim` section.
- Pre-1.0 Psych stored events in `sectionNotes` as notes with `noteData < 0` (`[time, -1, name, value1, value2]`); `convert` moves them to `events` when `events == null`.

### Events

`events: [ [time, [ [name, value1, value2], ... ]], ... ]`: each entry has a time and a list of simultaneous events (`makeEvent(event, i)`: `strumTime = event[0]`, `event = event[1][i][0]`, `value1 = event[1][i][1]`, `value2 = event[1][i][2]`). Values are strings. Names handled in `PlayState.triggerEvent` (main branch): `Hey!`, `Set GF Speed`, `Add Camera Zoom`, `Play Animation`, `Camera Follow Pos`, `Alt Idle Animation`, `Change Character`, `Change Scroll Speed`, `Play Sound` (not exhaustive; `Kill Henchmen` has an early-trigger offset of 280 ms in `eventEarlyTrigger`). The runtime adds `ClientPrefs.data.noteOffset` to each event time.

## Audio & images

Not in the chart.

## Versions & variants

- Old Psych (no `format`): legacy layout, `player3`, events as negative-lane notes, int note types, `lengthInSteps`, `mustHitSection`-relative lanes; all handled by `Song.convert`.
- `psych_v1`: `sectionBeats`, string note types, mustPress-absolute lanes, `gfVersion`. Release numbers of these changes were not established.
- `format` values in the loader: `psych_v1`, `psych_v1_convert` (while converting), `unknown` (no field).
- Troll Engine derives from this format (`FNFTroll extends FNFPsychBasic`): [troll-json](../troll-json/README.md).

## Quirks & pitfalls

- Lane meaning depends on `format`; legacy-style readers must check it.
- Wrapped and bare files both exist.
- `events` entries are lists of lists; one time can hold several events.
- Remove the negative-lane pseudo-notes of old files.

## Example

Hand-built from `Song.hx` / `PlayState` rules (not a real chart):

```json
{
  "song": {
    "song": "Test", "bpm": 150, "speed": 2.2, "needsVoices": true,
    "player1": "bf", "player2": "dad", "gfVersion": "gf", "stage": "stage",
    "format": "psych_v1",
    "notes": [
      { "sectionBeats": 4, "mustHitSection": true, "gfSection": false,
        "sectionNotes": [ [0, 0, 0], [400, 4, 0], [800, 1, 400, "Hey!"] ] }
    ],
    "events": [ [2000, [ ["Hey!", "BF", "0.6"] ]] ]
  }
}
```

The player's left arrow at 0 ms; the opponent's left arrow at 400 ms (4 -> opponent side); the player's down arrow at 800 ms, 400 ms hold, type `Hey!`; one event.

## ROX support

`.json` goes to the FNF (legacy) codec, [../legacy-json/README.md](../legacy-json/README.md).
- Old Psych (< 1.0): the `mustHitSection`-relative rule matches, notes decode correctly; negative-lane event notes become lane 0.
- `psych_v1` (`format` starting with `psych_v1`): lanes 0-3 are the player's, 4-7 the opponent's, whatever `mustHitSection` says (checked against `PlayState.generateSong`, `gottaHitNote = noteData < 4`, and `Song.convert`). ROX used to apply the legacy flip and read the opponent's notes as the player's in `mustHitSection: false` sections; since 2026-10-28 the decoder reads `format` and does not flip.
- Not handled: a string note type (4th element) fails the whole file (`invalid type: string "Hey!", expected f64`, run on 2026-10-28) because a legacy note is a `Vec<f64>`; bare files without the `{ "song": ... }` wrapper are not read.
- `events`, note types, `sectionBeats`, `gfSection`, `stage`, `offset` are ignored; BPM changes land at the section's first note.

## Parsers & tools

- Psych Engine source: https://github.com/ShadowMario/FNF-PsychEngine (`source/backend/Song.hx`, `states/PlayState.hx`), built-in Chart Editor
- Moonchart `FNFPsych` (Haxe): https://github.com/MaybeMaru/moonchart
- Codename Engine's `PsychParser` imports it: https://github.com/FNF-CNE-Devs/CodenameEngine

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: Psych mods keep charts in `mods/<mod>/data/<song>/`; GameBanana has thousands of Psych mods; the repository tags list every release. Observed: main's charts carry `"format": "psych_v1_convert"` (lanes converted on load), not `psych_v1`; `picospeaker.json` and `megumin-tool_wizdomiot-chart.json` are bare objects; in 0.6.3 events are negative-lane pseudo-notes.

## Sources

- https://raw.githubusercontent.com/ShadowMario/FNF-PsychEngine/main/source/backend/Song.hx
- https://raw.githubusercontent.com/ShadowMario/FNF-PsychEngine/main/source/states/PlayState.hx (`generateSong`, `makeEvent`)
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (comparison of engines; community doc)
