# FNF legacy chart JSON (`<song>.json`, "week charts")
Kind: chart

Doc status: complete · ROX: reads/writes (experimental; this is the layout ROX targets) · Category: vsrg · Encoding: json

## Overview

The original FNF chart layout ("week" charts of the 0.2.x builds), base of the Kade and Psych loaders. One JSON file per song and difficulty. Moonchart calls it "FNF (Legacy)". Sources: `Song.hx`, `Section.hx`, `PlayState.generateSong`, `Conductor.hx` at tag `v0.2.7.1` of FunkinCrew/Funkin.

## Container & encoding

- UTF-8 JSON `{ "song": { ... } }`. The official loader trims trailing garbage: `while (!rawJson.endsWith("}")) rawJson = rawJson.substr(0, rawJson.length - 1)`, so readers must tolerate bytes after the last `}`.
- The loader reads `assets/data/<folder>/<jsonInput>.json` lower-cased; the difficulty is the file-name suffix (`bopeebo.json` normal, `bopeebo-easy.json`, `bopeebo-hard.json`) [inference from `Song.loadFromJson(jsonInput, folder)`; the string composition was not read]. Audio is separate (`Inst.ogg`, `Voices.ogg`).

## Structure / metadata

`SwagSong` (vanilla `Song.hx`):

| Field | Type | Meaning |
|---|---|---|
| `song` | string | song name (used for asset paths) |
| `notes` | array of sections | the note data |
| `bpm` | int (vanilla; float in engines) | initial BPM |
| `needsVoices` | bool | whether a `Voices` track exists |
| `speed` | float | scroll speed multiplier |
| `player1` | string | player character (default `bf`) |
| `player2` | string | opponent character (default `dad`) |
| `validScore` | bool | set to `true` by the loader after parsing (`parseJSONshit`); some files carry it |

`SwagSection` (vanilla `Section.hx`):

| Field | Type | Meaning |
|---|---|---|
| `sectionNotes` | array of arrays | notes, see Notes |
| `lengthInSteps` | int | 16 by default (4 beats of 4 steps) |
| `typeOfSection` | int | 0 normal; `COPYCAT = 0` constant exists in the class; unused by gameplay in the files seen [inference] |
| `mustHitSection` | bool | camera focus AND which strumline `sectionNotes` lane 0-3 belongs to |
| `bpm` | int | BPM of the section, used only with `changeBPM` |
| `changeBPM` | bool | true -> this section starts at `bpm` |
| `altAnim` | bool | opponent plays the alt animation in this section |

## Timing model

- `Conductor.crochet = 60000 / bpm` (ms per beat), `stepCrochet = crochet / 4`. A section is `lengthInSteps * stepCrochet` ms (16 steps = 4 beats).
- Note times are absolute ms (`sectionNotes[i][0]`). Section lengths matter only for BPM changes: `Conductor.mapBPMChanges` accumulates `totalSteps` and `totalPos += (60 / curBPM * 1000 / 4) * lengthInSteps`; a section with `changeBPM && bpm != curBPM` records `{stepTime, songTime, bpm}` at its start. During play the engine calls `Conductor.changeBPM(SONG.notes[floor(curStep / 16)].bpm)` for such sections.
- Sustain pieces use the BPM in force at note generation: vanilla uses the song-level `stepCrochet`; Psych tracks the section BPM (`daBpm`).
- No stops, no signature other than 4/4 (steps per section may differ; 16 is the norm), no scroll velocity changes (single `speed`).

## Notes

`sectionNotes` is an array of arrays: `[strumTime, noteData, sustainLength]`, optionally followed by engine-specific extras (note type, etc.; Kade adds `isAlt` and `beat`, Psych adds a note type string).

| Index | Meaning |
|---|---|
| 0 | `strumTime`: absolute ms |
| 1 | `noteData`: 0-7. `noteData % 4` is the lane: 0 left, 1 down, 2 up, 3 right |
| 2 | `sustainLength` in ms; 0 = tap; > 0 = hold |

Strumline ownership (vanilla `PlayState.generateSong`):

```
gottaHitNote = section.mustHitSection
if (noteData > 3) gottaHitNote = !gottaHitNote
```

With `mustHitSection: true`, lanes 0-3 are the player's and 4-7 the opponent's; with `mustHitSection: false` it is reversed. Combine the flag with the lane for every note.

Holds: the head note plus `floor(sustainLength / stepCrochet)` sustain pieces, one per step, spawned at `strumTime + stepCrochet * (i + 1)` (vanilla). Hold lengths are not quantised.

Vanilla has no other note kinds, mines, keysounds or per-note volume. Mods use extra array slots or negative lanes (Psych <= 0.6 stored events as notes with `noteData < 0`, see Psych doc).

Simultaneous notes are allowed; duplicate (time, lane) pairs ("ghost notes") exist in sloppy charts.

## Audio & images

Not in the chart. Vanilla loads `Inst` and, if `needsVoices`, `Voices` by song name. `player1`/`player2` name character definitions.

## Versions & variants

No version field in vanilla (Psych adds `format`, Kade `chartVersion`, V-Slice replaced it). Engines differ in `bpm` int vs float and add `gfVersion`/`player3`, `stage`, `events`, `sectionBeats`, `eventObjects`, `noteStyle`, `offset`: see [psych-json](../psych-json/README.md), [kade-json](../kade-json/README.md), [fps-plus-json](../fps-plus-json/README.md), [codename-json](../codename-json/README.md), [vslice-chart-json](../vslice-chart-json/README.md). Week 7 / 0.3 pre-release charts typed notes with an int in slot 3 (Psych's `Note.defaultNoteTypes` maps it).

## Quirks & pitfalls

- `mustHitSection` flips lane ownership; ignoring it swaps the sides.
- Sections other than 16 steps exist; times stay absolute. Compute beat positions from the BPM map, not the note index.
- `sectionNotes` can hold lanes outside 0-7 or negative (events in engine charts).
- A hold shorter than one step makes no sustain piece in vanilla (floor).
- `bpm` is an int in vanilla (fractional BPM rounded); engines use float.
- Vanilla charts of tag v0.2.7.1 end with thousands of NUL bytes after the closing brace [observed: funkin-v0.2.7.1_bopeebo.json]; strict JSON parsers fail.

## Example

Hand-built from the rules above (not a real chart):

```json
{
  "song": {
    "song": "Test",
    "bpm": 120,
    "speed": 2.0,
    "needsVoices": true,
    "player1": "bf",
    "player2": "dad",
    "notes": [
      {
        "lengthInSteps": 16,
        "mustHitSection": true,
        "changeBPM": false,
        "bpm": 120,
        "altAnim": false,
        "typeOfSection": 0,
        "sectionNotes": [
          [0, 0, 0],
          [125, 5, 0],
          [500, 2, 250]
        ]
      }
    ]
  }
}
```

At 120 BPM one step = 125 ms. The player's left arrow at 0 ms; the opponent's down arrow (lane 5 -> `noteData % 4 = 1`, other side because `5 > 3`) at 125 ms; the player's up arrow at 500 ms held for 250 ms (2 sustain steps).

## ROX support

`src/formats/fnf` (`FnfDecoder`/`FnfEncoder`); `auto/detect.rs` routes every `.json` here (`"json" => DetectedFormat::Fnf`; `.jrox` is a different extension).
- Types: `FnfChart { song: FnfSong }`, `FnfSong { song, bpm: f32, speed (1.0), player1 ("bf"), player2 ("dad"), needsVoices (false), notes: [FnfSection] }`, `FnfSection { sectionNotes, lengthInSteps (16), mustHitSection (false), changeBPM (false), bpm (0.0) }`, note `[time_ms, lane, duration_ms]` as `Vec<f64>`. Unknown fields (`gfVersion`, `events`, `sectionBeats`...) and note extras after index 2 are ignored.
- Decode sides: `FnfSide::Player` (default, 4 columns), `Opponent` (4 columns), `Both` (8 columns, `is_coop = true`: opponent 0-3, player 4-7). `resolve_column`: `raw_lane < 4` is the player's iff `mustHitSection`, else (`>= 4`) iff `!mustHitSection`; column = `raw_lane` or `raw_lane - 4` (the legacy rule). Raw lane is cast `f64 as u8`: negative lanes saturate to 0, so event notes with lane -1 become column-0 notes if their section matches [inference].
- Timing: BPM point at 0 from `song.bpm`; for each section with `changeBPM && bpm > 0` and at least one note, a BPM point at the time of the section's first note (not its start), if > 0 [`build_timing_points`]. No SV points, `speed` dropped. Duration > 0 is a hold; times `ms * 1000` as `i64` (truncated).
- Metadata is synthetic: title = `song`, artist `"Unknown"`, creator = `player2`, difficulty `"Normal"`, audio `"Inst.ogg"`, source `"Friday Night Funkin'"`, tags `["fnf"]`.
- Encode (`to_fnf`): one section for the whole song (`lengthInSteps` 160000, `mustHitSection = !(key_count >= 8)`, `changeBPM: true`, `bpm` = first BPM), `player1: "bf"`, `player2` = creator, `speed 1.0`, notes `[time_ms, column, duration_ms]` (Burst -> hold, Mine -> tap), pretty-printed. Later BPM changes and SV points are lost. For 8K charts columns 0-3 are the opponent's, 4-7 the player's.
- Detection: only the Psych `format` field; a value starting with `psych_v1` makes lanes 0-3 the player's regardless of `mustHitSection` (see [psych-json](../psych-json/README.md)); everything else uses the legacy rule. The 100 MiB limit applies. V-Slice charts: [vslice-chart-json](../vslice-chart-json/README.md).

## Parsers & tools

- FNF source (Haxe): https://github.com/FunkinCrew/Funkin/tree/v0.2.7.1 (`source/Song.hx`, `Section.hx`, `PlayState.hx`, `Conductor.hx`)
- Moonchart `FNFLegacy` (Haxe): https://github.com/MaybeMaru/moonchart
- ROX `formats/fnf` (Rust): vendored.
- Browser visualiser: https://jsm925.github.io/FunkinChart [listed by search; not examined]

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: tag `v0.2.7.1` has every week song (easy/normal/hard); Kade (`assets/preload/data/songs/`) and Psych (`assets/base_game/shared/data/`) repositories ship base-game charts in this layout; mods carry `data/<song>/<song>-<diff>.json` (GameBanana, e.g. https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=...); Moonchart (https://github.com/MaybeMaru/moonchart) can write it. Observed: four of five vanilla charts end with NUL bytes (4192 in `funkin-v0.2.7.1_bopeebo.json`); bpm is an int; every note array has 3 elements.

## Sources

- https://raw.githubusercontent.com/FunkinCrew/Funkin/v0.2.7.1/source/{Song,Section,Conductor,PlayState}.hx
- https://github.com/MaybeMaru/moonchart
- ROX source: `src/formats/fnf/{types,parser,decoder,encoder}.rs`, `src/formats/auto/detect.rs`
