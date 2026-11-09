# FNF legacy chart JSON (`<song>.json`, "week charts")
Kind: chart

Doc status: complete · ROX: reads/writes (experimental; this is the layout ROX targets) · Category: vsrg · Encoding: json

## Overview

The original chart layout of Friday Night Funkin' (the "week" charts of the 0.2.x builds; the sources read are tag `v0.2.7.1`) and the base of the loaders of Kade Engine and Psych Engine (both carry `Song.hx`/`Section.hx` derived from it, see their folders). One JSON file per song and difficulty. Source of truth: `Song.hx`, `Section.hx`, `PlayState.generateSong`, `Conductor.hx` of the tag `v0.2.7.1` of FunkinCrew/Funkin (also the format Moonchart calls "FNF (Legacy)").

## Container & encoding

- UTF-8 JSON, a single object `{ "song": { ... } }`. The official loader trims trailing garbage: `while (!rawJson.endsWith("}")) rawJson = rawJson.substr(0, rawJson.length - 1)` (some chart files end with stray characters), so a robust reader should tolerate trailing bytes after the last `}`.
- One file per difficulty. The vanilla loader reads `assets/data/<folder>/<jsonInput>.json` lower-cased; the difficulty is the suffix of the file name (`bopeebo.json` normal, `bopeebo-easy.json`, `bopeebo-hard.json`) [inference from `Song.loadFromJson(jsonInput, folder)` and the difficulty suffix convention in PlayState; the exact string composition was not read]. Audio is separate (`Inst.ogg`, `Voices.ogg`).
- No compression, no archive.

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

- `bpm` at the song start; `Conductor.crochet = 60000 / bpm` (ms per beat), `stepCrochet = crochet / 4`. A section is `lengthInSteps` steps = `lengthInSteps * stepCrochet` ms (16 steps = 4 beats = one 4/4 measure).
- **Note times are absolute milliseconds** (`sectionNotes[i][0]`), so notes do not depend on the section layout for placement. Section lengths are needed only to find when a BPM change takes effect: `Conductor.mapBPMChanges` walks the sections accumulating `totalSteps` and `totalPos += (60 / curBPM * 1000 / 4) * lengthInSteps`; when a section has `changeBPM && bpm != curBPM` it records `{stepTime, songTime, bpm}` at that section's start.
- During play the engine calls `Conductor.changeBPM(SONG.notes[floor(curStep / 16)].bpm)` when that section has `changeBPM`.
- Sustain pieces use the BPM in force when notes are generated: vanilla uses the song-level `stepCrochet` for all sustains (a known approximation); Psych tracks the section BPM (`daBpm`).
- No stops, no time signatures other than 4/4 (steps per section may differ; 16 is the norm), no scroll velocity changes (a single `speed`).

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

So with `mustHitSection: true`, lanes 0-3 are the player's and 4-7 the opponent's; with `mustHitSection: false` it is reversed. The `mustHitSection` flag therefore must be combined with the lane for every note.

Holds: the head note plus `floor(sustainLength / stepCrochet)` sustain pieces, one per step, spawned at `strumTime + stepCrochet * (i + 1)` (vanilla). Hold lengths are not quantised in the file.

Other note kinds do not exist in vanilla; mods use extra array slots or negative lanes (Psych <= 0.6 stored events as notes with `noteData < 0`, see Psych doc). No mines, no keysounds, no per-note volume.

Simultaneous notes (several lanes at the same time) are allowed; duplicate (time, lane) pairs ("ghost notes") exist in sloppily made charts.

## Audio & images

Not in the chart. Vanilla loads `Inst` and, if `needsVoices`, `Voices` by song name; characters, stage, icons are code/asset data. `player1`/`player2` name character definitions.

## Versions & variants

The vanilla format never carried a version field (Psych adds `format`, Kade adds `chartVersion`, V-Slice replaced it). Differences: `bpm` int vs float, extra per-engine fields (`gfVersion`/`player3`, `stage`, `events`, `sectionBeats`, `eventObjects`, `noteStyle`, `offset` ...). See [psych-json](../psych-json/README.md), [kade-json](../kade-json/README.md), [fps-plus-json](../fps-plus-json/README.md), [codename-json](../codename-json/README.md), [vslice-chart-json](../vslice-chart-json/README.md). Week 7 / 0.3 pre-release charts typed notes with an int in slot 3 (Psych's `Note.defaultNoteTypes` maps it).

## Quirks & pitfalls

- `mustHitSection` flips lane ownership; ignoring it swaps the sides.
- Section lengths other than 16 steps exist; times stay absolute.
- A BPM change in a section is applied from the section start, but the notes keep their absolute times; a converter must compute the beat position from the BPM map, not from the note index.
- `sectionNotes` can contain lanes outside 0-7 or negative lanes (events in engine charts).
- Holds with `sustainLength` shorter than one step produce no sustain piece in vanilla (floor).
- `bpm` fields are ints in vanilla; fractional BPM were rounded by that type, engines changed to float.
- Trailing garbage after the final `}` appears in real charts: the vanilla charts of tag v0.2.7.1 end with thousands of NUL bytes after the closing brace [observed in samples/funkin-v0.2.7.1_bopeebo.json]; a strict JSON parser fails on them.

## Example

Illustrative, hand-built from the rules above (not a real chart):

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

At 120 BPM one step = 125 ms. Notes: the player's left arrow at 0 ms; the opponent's down arrow (lane 5 -> `noteData % 4 = 1`, other side because `5 > 3`) at 125 ms; the player's up arrow at 500 ms held for 250 ms (2 sustain steps).

## ROX support

ROX source `src/formats/fnf` (`FnfDecoder`/`FnfEncoder`, extension `json`, so every `.json` is routed to this codec by `auto/detect.rs`: `"json" => DetectedFormat::Fnf`; `.jrox` is a different extension):
- Types: `FnfChart { song: FnfSong }`, `FnfSong { song, bpm: f32, speed (default 1.0), player1 ("bf"), player2 ("dad"), needsVoices (false), notes: [FnfSection] }`, `FnfSection { sectionNotes, lengthInSteps (16), mustHitSection (false), changeBPM (false), bpm (0.0) }`, a note is `[time_ms, lane, duration_ms]` as a `Vec<f64>`. Unknown fields (`gfVersion`, `events`, `sectionBeats`...) are ignored; note extras after index 2 are ignored.
- Decode side choice: `FnfSide::Player` (default, 4 columns: only the player's notes), `Opponent` (4 columns), `Both` (8 columns, `is_coop = true`: opponent in columns 0-3, player in 4-7). Lane resolution (`resolve_column`): `raw_lane < 4` -> player iff `mustHitSection`, else (`>= 4`) player iff `!mustHitSection`; column = `raw_lane` or `raw_lane - 4`. This is the legacy rule above. A raw lane is cast `f64 as u8` (negative values saturate to 0, so legacy "event notes" with lane -1 become column-0 notes if their section matches [inference from the code]).
- Timing: BPM point at 0 from `song.bpm`; for every section with `changeBPM && bpm > 0` and at least one note, a BPM point is placed at the time of the section's FIRST NOTE (not at the section start), if that time is > 0 [from `build_timing_points`]. No SV points, `speed` is dropped. Duration > 0 -> hold; times `ms * 1000` as `i64` (truncated).
- Metadata is synthetic: title = `song`, artist `"Unknown"`, creator = `player2`, difficulty name `"Normal"`, audio `"Inst.ogg"`, source `"Friday Night Funkin'"`, tags `["fnf"]`.
- Encode (`to_fnf`): one single section for the whole song (`lengthInSteps` 160000, `mustHitSection = !(key_count >= 8)`, `changeBPM: true`, `bpm` = first BPM), `player1: "bf"`, `player2` = creator, `speed 1.0`, notes `[time_ms, column, duration_ms]` (Burst -> hold, Mine -> tap), pretty-printed JSON. BPM changes after the first and SV points are lost. For 8K charts columns 0-3 are the opponent's and 4-7 the player's.
- Version/format detection: only the Psych `format` field: a value starting with `psych_v1` makes lanes 0-3 the player's and 4-7 the opponent's regardless of `mustHitSection` (see [psych-json](../psych-json/README.md)); any other file is read with the legacy lane rule. The 100 MiB limit applies. V-Slice charts are a different format, see [vslice-chart-json](../vslice-chart-json/README.md).

## Parsers & tools

- FNF source (Haxe): https://github.com/FunkinCrew/Funkin/tree/v0.2.7.1 (`source/Song.hx`, `Section.hx`, `PlayState.hx`, `Conductor.hx`)
- Moonchart `FNFLegacy` (Haxe): https://github.com/MaybeMaru/moonchart
- ROX `formats/fnf` (Rust): vendored.
- Browser visualiser: https://jsm925.github.io/FunkinChart [listed by search; not examined]

## Getting samples

- Committed ([samples/](samples/) and [samples/SOURCES.md](samples/SOURCES.md)): five vanilla charts of FunkinCrew/Funkin tag `v0.2.7.1` (`assets/data/<song>/<song>[-hard].json`), ROX's MIT test chart, and two synthetic charts. FNF base-game data belongs to The Funkin Crew Inc. (funkin.assets LICENSE.md: all rights reserved; Funkin `LICENSE.md`: only the source code is Apache-2.0); the owner accepted that risk, so the charts are committed as downloaded snapshots.
- Observed: four of five vanilla charts end with thousands of NUL bytes after the closing brace (e.g. 4192 in `funkin-v0.2.7.1_bopeebo.json`); bpm is an int; every note array has 3 elements.
- More: the same tag has every week song (easy/normal/hard); the Kade and Psych repositories ship base-game charts in this layout (`assets/preload/data/songs/` in Kade, `assets/base_game/shared/data/` in Psych); community mods carry `data/<song>/<song>-<diff>.json` (GameBanana submissions, e.g. https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=...). Moonchart (https://github.com/MaybeMaru/moonchart) can also write it.

## Sources

- https://raw.githubusercontent.com/FunkinCrew/Funkin/v0.2.7.1/source/{Song,Section,Conductor,PlayState}.hx
- https://github.com/MaybeMaru/moonchart
- ROX source: `src/formats/fnf/{types,parser,decoder,encoder}.rs`, `src/formats/auto/detect.rs`
