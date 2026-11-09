# Psych Engine chart JSON (`<song>.json`, format `psych_v1`)
Kind: chart

Doc status: complete · ROX: no dedicated codec; the legacy codec reads both the old (pre-1.0) layout and `psych_v1` files (lane rule fixed 2026-10-28, see ROX support) · Category: vsrg · Encoding: json

## Overview

Psych Engine (ShadowMario and contributors) is a widely used FNF mod engine. Its chart file is the legacy week JSON ([../legacy-json/README.md](../legacy-json/README.md)) extended with events, a stage, a girlfriend character, per-note types, and, in the current source, a normalised lane meaning marked by a `format` field. Source: `source/backend/Song.hx`, `source/states/PlayState.hx` (main branch).

## Container & encoding

- UTF-8 JSON. `Song.parseJSON` accepts both `{ "song": { ... } }` (legacy wrapper: if the parsed object has a `song` field of object type, that sub-object is used) and the bare object.
- One file per difficulty: `data/<songFolder>/<song>[-<difficulty>].json` (loader `Paths.json('$formattedFolder/$formattedSong')`, where `formattedSong` is the song name plus the difficulty suffix chosen by the caller; names are lower-cased with spaces -> dashes by `Paths.formatToSongPath`). Optional `data/<songFolder>/events.json` holds extra events with the same `events` schema (loaded by `Song.getChart('events', songName)`).
- Audio is separate (`Inst.ogg`, `Voices.ogg`, optional `Voices-Player.ogg` / `Voices-Opponent.ogg`) [inference for the split vocal names; not read in the sources consulted].

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

As in the legacy format: absolute ms for notes and events; BPM from `bpm`, changes via `changeBPM`+`bpm` of a section (`PlayState.generateSong` keeps `daBpm`; a change applies from the section). Step length for sustains is `60 / daBpm * 1000 / 4`; the section length is `sectionBeats` beats (default 4) instead of `lengthInSteps` steps (old files converted: `sectionBeats = 4`, `lengthInSteps` removed).

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, noteType?]`:

- `noteType`: a string in Psych 1.0 (custom names allowed). Older charts used an int index into `Note.defaultNoteTypes = ['', 'Alt Animation', 'Hey!', 'Hurt Note', 'GF Sing', 'No Animation']` (mapped during `convert` and again in `generateSong`).
- **`psych_v1` lane semantics (changed from legacy)**: `noteData` 0-3 = the player's side (`mustPress`), 4-7 = the opponent's, regardless of `mustHitSection` (`PlayState`: `gottaHitNote = (songNotes[1] < totalColumns)`, `noteColumn = songNotes[1] % totalColumns`, `totalColumns = 4`). `Song.convert` rewrites old charts to this: `gottaHit = (note[1] < 4) ? section.mustHitSection : !section.mustHitSection; note[1] = (note[1] % 4) + (gottaHit ? 0 : 4)`. So `mustHitSection` in a `psych_v1` file now only tells the camera and the `gfSection`/`altAnim` logic.
- Sustain: `holdLength` ms; pieces `Math.round(holdLength / curStepCrochet)` (rounded, not floor as in vanilla).
- Ghost notes (same lane, type and time, within epsilon) are removed at load time (`ghostNotesCaught`).
- `gfNote = section.gfSection && gottaHitNote == section.mustHitSection`; `altAnim` applies to the opponent's notes of an `altAnim` section.
- Pre-1.0 Psych stored **events** in `sectionNotes` as notes with `noteData < 0` (`[time, -1, name, value1, value2]`); `convert` moves them to `events` when `events == null`.

### Events

`events: [ [time, [ [name, value1, value2], ... ]], ... ]`: each entry has a time and a list of simultaneous events (`makeEvent(event, i)`: `strumTime = event[0]`, `event = event[1][i][0]`, `value1 = event[1][i][1]`, `value2 = event[1][i][2]`). Values are strings. Event names handled in `PlayState.triggerEvent` (main branch): `Hey!`, `Set GF Speed`, `Add Camera Zoom`, `Play Animation`, `Camera Follow Pos`, `Alt Idle Animation`, `Change Character`, `Change Scroll Speed`, `Play Sound` (the list is not exhaustive; `Kill Henchmen` has an early-trigger offset of 280 ms in `eventEarlyTrigger`). The runtime adds `ClientPrefs.data.noteOffset` to each event time.

## Audio & images

Not in the chart (characters, stage, skins are referenced by name).

## Versions & variants

- Older Psych (before `format` existed): legacy layout, `player3`, no `events` array (events stored as negative-lane notes), integer note types, `lengthInSteps` sections, `mustHitSection`-relative lanes (all handled by `Song.convert`).
- Newer (`format: "psych_v1"`): `sectionBeats` instead of `lengthInSteps`, string note types, mustPress-absolute lanes, `gfVersion`. The exact Psych release numbers of these changes were not established from the sources consulted.
- `format` values seen in the loader: `psych_v1`, `psych_v1_convert` (while converting), `unknown` (no field).
- Troll Engine derives its chart JSON from the Psych one (Moonchart's `FNFTroll extends FNFPsychBasic`): see [troll-json](../troll-json/README.md).

## Quirks & pitfalls

- The lane meaning depends on `format`: a legacy-style reader must check it.
- Both `{song: {...}}` wrapped and bare files exist.
- `events` entries are lists of lists; a single time can hold several events.
- BPM is a float; `bpm`/`changeBPM` optional per section.
- A converter must remove the negative-lane pseudo-notes of old files.

## Example

Illustrative, hand-built from `Song.hx` / `PlayState` rules (not a real chart):

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

Notes: the player's left arrow at 0 ms; the opponent's left arrow at 400 ms (4 -> opponent side); the player's down arrow at 800 ms, 400 ms hold, type `Hey!`; one event.

## ROX support

Not a ROX format of its own, but `.json` is routed to the FNF (legacy) codec, [../legacy-json/README.md](../legacy-json/README.md). Consequences for a Psych file (derived from the ROX decoder and the Psych source above):
- Old Psych (< 1.0) files: the `mustHitSection`-relative lane rule matches, so notes decode correctly. Negative-lane event notes would be treated as lane 0.
- `psych_v1` files (`format` starting with `psych_v1`): lanes 0-3 are the player's side, 4-7 the opponent's, whatever `mustHitSection` says (checked against Psych's `PlayState.generateSong`, `gottaHitNote = noteData < 4`, and `Song.convert`, which only flips by `mustHitSection` for files that are not `psych_v1`). ROX used to apply the legacy `mustHitSection` flip to them and read the opponent's notes as the player's in sections with `mustHitSection: false`; since 2026-10-28 the legacy decoder reads the `format` field and does not flip.
- Still not handled: a note with a string note type (a fourth element) makes the whole file fail (`invalid type: string "Hey!", expected f64`, run on 2026-10-28), because a legacy note is a `Vec<f64>`; a bare file without the `{ "song": ... }` wrapper is not read either.
- `events`, note types, `sectionBeats`, `gfSection`, `stage`, `offset` are ignored; BPM changes are placed at the first note of the section.

## Parsers & tools

- Psych Engine source: https://github.com/ShadowMario/FNF-PsychEngine (`source/backend/Song.hx`, `states/PlayState.hx`), built-in Chart Editor
- Moonchart `FNFPsych` (Haxe): https://github.com/MaybeMaru/moonchart
- Codename Engine's `PsychParser` imports it: https://github.com/FNF-CNE-Devs/CodenameEngine

## Getting samples

- Committed ([samples/](samples/) and [samples/SOURCES.md](samples/SOURCES.md)): base-game charts of ShadowMario/FNF-PsychEngine at tags `0.6.3`, `0.7.3` and main (Apache-2.0 code; FNF base-game data belongs to The Funkin Crew Inc. (funkin.assets LICENSE.md: all rights reserved; Funkin `LICENSE.md`: only the source code is Apache-2.0); the owner accepted that risk, so the charts are committed as downloaded snapshots.), four community charts from MeguminBOT/fnf-chart-info-tool (`megumin-tool_*`: a bare psych object, a Psych-fork chart, an `everlasting` 0.6-era chart, an events file) and four synthetic files.
- Observed: the charts shipped in main carry `"format": "psych_v1_convert"` (the loader converts lanes on load), not `psych_v1`; `picospeaker.json` and `megumin-tool_wizdomiot-chart.json` are bare objects without the `song` wrapper; in 0.6.3 the events are negative-lane pseudo-notes in sectionNotes.
- More: any Psych mod keeps charts in `mods/<mod>/data/<song>/`; GameBanana has thousands of Psych mods; the repository tags list every release.

## Sources

- https://raw.githubusercontent.com/ShadowMario/FNF-PsychEngine/main/source/backend/Song.hx
- https://raw.githubusercontent.com/ShadowMario/FNF-PsychEngine/main/source/states/PlayState.hx (`generateSong`, `makeEvent`)
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (comparison of engines; community doc)
