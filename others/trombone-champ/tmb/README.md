# Trombone Champ custom track (`song.tmb`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json

## Overview
`song.tmb` is the chart file of a Trombone Champ custom track. It is a single JSON object (the game's own binary `SavedLevel` form can also be exported, but JSON is the format used by the community: modding guides recommend JSON because binary tracks cannot be uploaded or have difficulty computed, per a Steam editor thread). The loader TrombLoader scans `BepInEx/CustomSongs/**/song.tmb` (and plugin folders), deserialises it with Newtonsoft.Json into `CustomTrackData`, de-duplicates by `trackRef`, and converts it to the game's `SavedLevel`. Editors: TromboneCharter (Godot), TootMaker (Unity editor), Trombone-Champ-Charter (Unity); converters: Midi2TromboneChamp (MIDI to TMB), TmbToMidi (TMB to MIDI), TCCC web converter. Trombone Champ has no timing points: one tempo for the whole song.

## Container & encoding
- Plain JSON, UTF-8. One file = one chart (one difficulty); there is no difficulty set. The folder holds `song.tmb`, `song.ogg` (fixed name, `Globals.defaultAudioName`), and optionally `bg.png`, `bg.mp4` or `bg.trombackground` (Unity AssetBundle) (TrombLoader `CustomTrack.cs`).
- Fixed file names: chart `song.tmb`, audio `song.ogg`. The folder name is free; identity is `trackRef`.

## Structure / metadata
Fields read by TrombLoader `CustomTrackData` and written by Midi2TromboneChamp / TromboneCharter:

| Field | Type | Meaning |
|---|---|---|
| `name` | string | title (TromboneCharter reads `data.name`; Midi2TromboneChamp writes `name`). Web search summaries show `title`; the code sources use `name` |
| `shortName` | string | short title |
| `trackRef` | string | unique track identifier ("Track Tag", folder name in Midi2TromboneChamp); duplicates are skipped by TrombLoader |
| `author` | string | author/artist string (Midi2TromboneChamp fills it from its "Author" box, variable `artist`) |
| `genre`, `description` | string | free text |
| `year` | int | release year |
| `difficulty` | int | rating, 0-10 scale in practice (editor default 5) |
| `tempo` | float | BPM, constant (editor default 120) |
| `timesig` | int | beats per bar (editor default 2; Midi2TromboneChamp field "Beats Per Bar") |
| `endpoint` | float | song end in beats (editors default 4; Midi2TromboneChamp uses last bar + 4) |
| `savednotespacing` | int | editor note spacing (default 120 in both editors) [role: editor display, inference] |
| `notes` | array of float[5] | see below |
| `lyrics` | array of `{bar, text}` | lyric events; `bar` float beat position, `text` string. TromboneCharter's comment names the field `lyric`, TrombLoader and TmbToMidi read `text` |
| `improv_zones` | array of float[2] | `[startBeat, endBeat]` of improv (free-play) sections (TmbToMidi) |
| `bgdata` | array of float[2] | background events: `[time, eventId]`; TmbToMidi emits text event `bg_<id>` and rescales time by `tempo/60`, so the first value is in seconds [inference] |
| `note_color_start`, `note_color_end` | float[3] | RGB 0..1 of the note ribbon gradient; defaults `[1.0, 0.21, 0.0]` and `[1.0, 0.8, 0.3]` (TrombLoader) |
| `backgroundMovement` | string | default `"none"` (TrombLoader) |
| `UNK1` | int | written as 0 by Midi2TromboneChamp and TromboneCharter, role unknown |

## Timing model
- All positions in `notes`, `lyrics`, `improv_zones`, `endpoint` are in **beats** (the field is called `bar` in code but is a beat count; one `timesig` unit is one beat). Midi2TromboneChamp stores `ticks/ticks_per_beat`; TmbToMidi converts with `beats * 960` ticks.
- Seconds from beats: `t = bar * 60 / tempo`. There is only one tempo; tempo changes in a MIDI source are baked into beat positions (TmbToMidi README: "notes are in the post-tempo shifted positions"). The game has no timing points (Thunderstore note on TromboneChampTimingColors).
- Audio alignment: the first beat of the chart is time 0 of `song.ogg`; there is no offset field, so audio must be trimmed/padded.

## Notes
Each note is a 5-element float array (TromboneCharter `TMBInfo`: `NOTE_BAR, NOTE_LENGTH, NOTE_PITCH_START, NOTE_PITCH_DELTA, NOTE_PITCH_END`):

| Index | Name | Meaning |
|---|---|---|
| 0 | bar | start in beats |
| 1 | length | duration in beats |
| 2 | start_pitch | pitch at start, in game units |
| 3 | delta_pitch | `end_pitch - start_pitch` (a slide within one note) |
| 4 | end_pitch | pitch at end |

- Pitch units: 13.75 units per semitone, 0 = MIDI note 60 (middle C). The playable range is B2 (MIDI 47, -178.75) to C#5 (MIDI 73, +178.75) (TmbToMidi comments, Midi2TromboneChamp `SetupNote: (note-60)*13.75`). Fractional values are microtones (TmbToMidi turns them into MIDI pitch bends).
- A slide is either one note with `delta_pitch != 0`, or two notes where the second starts exactly where the first ends (TromboneCharter: such a pair forms a slide when pitches match). TmbToMidi converts a slide into two overlapping MIDI notes (TCCC convention).
- Notes must be sorted by start; overlapping notes are allowed but TmbToMidi has to split them into separate tracks. Notes ending after `endpoint` are dropped by TromboneCharter on save.
- No simultaneous different-pitch notes in normal play (one trombone).

## Audio & images
`song.ogg` (Ogg Vorbis) plus optional `bg.png`, `bg.mp4`, `bg.trombackground`. No preview or offset fields. Lyrics are shown as karaoke text.

## Versions & variants
- The game's native binary format (`SavedLevel` with `savedleveldata`, `bgdata`, `lyricspos`, `lyricstxt`, `endpoint`, `tempo`, `timesig`, `savednotespacing`, `note_color_*`); TrombLoader maps JSON to it in `CustomTrackData.ToSavedLevel` (notes -> `savedleveldata`, lyrics -> `lyricspos` `[bar, 0]` + `lyricstxt`).
- Older Midi2TromboneChamp output has no `improv_zones`/`bgdata`; those are optional.

## Quirks & pitfalls
- `name`/`title` and lyric `text`/`lyric` naming differs between secondary sources; use the code of TrombLoader as reference.
- Floating point jitter: TmbToMidi notes that adjacent notes can differ by 1 MIDI tick because of float precision in the TMB.
- Tempo is read as float but Midi2TromboneChamp writes `int(bpm)`.
- `year`, `difficulty`, `savednotespacing`, `timesig` are ints (parsers using strict types fail on floats).

## Example
Illustrative, hand-built from the rules above (not a real chart): a 120 BPM track with a one-beat note on middle C followed by a one-beat slide up 2 semitones.

```json
{
  "name": "Example", "shortName": "Example", "trackRef": "example", "author": "Nobody",
  "genre": "Test", "description": "", "year": 2024, "difficulty": 5,
  "tempo": 120, "timesig": 2, "endpoint": 8, "savednotespacing": 120,
  "notes": [[0, 1, 0, 0, 0], [2, 1, 0, 27.5, 27.5]],
  "lyrics": [{"bar": 0, "text": "la"}], "improv_zones": [], "bgdata": [], "UNK1": 0
}
```

## ROX support
Not read by ROX. Pitch-based, no lanes; at best a lossy projection onto columns by pitch band.

## Parsers & tools
- TrombLoader `CustomTrackData` (C#): https://github.com/NyxTheShield/TrombLoader
- TromboneCharter `tmb_info.gd` (GDScript, read/write): https://github.com/towai/TromboneCharter
- Midi2TromboneChamp (Python, MIDI to TMB): https://github.com/NyxTheShield/Midi2TromboneChamp
- TmbToMidi (C#, TMB to MIDI): https://github.com/Gloomhonk/TmbToMidi
- Trombone-Champ-Charter (Unity): https://github.com/bakerj76/Trombone-Champ-Charter
- boner-viewer (web previewer): https://github.com/Paturages/boner-viewer
- TCCC chart converter: https://tc-chart-converter.github.io/

## Sources
- https://raw.githubusercontent.com/NyxTheShield/TrombLoader/master/CustomTracks/CustomTrackData.cs
- https://raw.githubusercontent.com/NyxTheShield/TrombLoader/master/CustomTracks/TrackLoader.cs
- https://raw.githubusercontent.com/NyxTheShield/TrombLoader/master/Helpers/Globals.cs
- https://raw.githubusercontent.com/towai/TromboneCharter/master/tmb_info.gd
- https://github.com/towai/TromboneCharter
- https://raw.githubusercontent.com/NyxTheShield/Midi2TromboneChamp/main/Midi2TromboneChamp.py
- https://raw.githubusercontent.com/Gloomhonk/TmbToMidi/master/TmbToMidi/TmbConverter.cs
- https://raw.githubusercontent.com/Gloomhonk/TmbToMidi/master/TmbToMidi/TmbData.cs
- https://github.com/Gloomhonk/TmbToMidi
- https://thunderstore.io/c/trombone-champ/p/CraftedCart/TromboneChampTimingColors/
- https://steamcommunity.com/app/1059990/discussions/0/4753074677209818267/?l=english&ctp=2
