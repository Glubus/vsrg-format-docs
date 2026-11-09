# fluXis map (`.fsc`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview

`.fsc` is the **per-difficulty map file of fluXis**, a community-driven open-source vertical-scrolling rhythm game built on osu!framework (C#). One `.fsc` holds one difficulty: metadata, timing points, scroll velocities, hit objects (lane based, 1..N keys), plus references to an audio/background/cover/video file and to the companion effects file ([`.ffx`](../ffx/README.md)) and storyboard (`.fsb`). A mapset is a ZIP of several `.fsc` files and their assets, distributed as [`.fms`](../fms/README.md). fluXis has built-in importers that convert osu!, Quaver and StepMania maps into `.fsc` (`fluXis.Import.osu`, `fluXis.Import.Quaver`, `fluXis.Import.Stepmania`). The format is defined by the C# classes (`MapInfo`, `HitObject`, `TimingPoint`, `ScrollVelocity`, `HitSoundFade`), serialised with Newtonsoft.Json; there is no separate spec document, so this page is derived from the source. Property names that carry no explicit `[JsonProperty]` attribute are listed with their C# names (see Quirks).

## Packaged in

- Packaged in [`fms`](../fms/).

## Container & encoding

- One JSON object per file, UTF-8 (Newtonsoft.Json). File name: any `*.fsc`; the game generates `<unix timestamp>.fsc` for new maps and `<difficulty>.fsc`/`<source name>.fsc` for converted maps.
- `MapInfo.Sort()` orders `HitObjects` by `time` then `lane`, and `TimingPoints`, `ScrollVelocities`, `HitSoundFades` by `time`.
- Hash: the game identifies a difficulty by a hash of the file content (`MapUtils.GetHash`) and the audio by an xxHash of the audio file; they are used for online lookup (not stored in the file).

## Structure / metadata

### Top level (`MapInfo`)

| Field | Type | Meaning |
|---|---|---|
| `AudioFile`, `BackgroundFile`, `CoverFile`, `VideoFile`, `EffectFile`, `StoryboardFile` | string | File names inside the mapset (no explicit JSON name in source). `EffectFile` is the [`.ffx`](../ffx/README.md) events file, `StoryboardFile` the `.fsb` storyboard. |
| `metadata` | object | See below. |
| `colors` | object | `accent`, `primary`, `secondary`, `middle`: hex colour strings (empty = default). |
| `HitObjects` | array | Notes. |
| `TimingPoints` | array | BPM / time signature. |
| `ScrollVelocities` | array | SV multipliers. |
| `HitSoundFades` | array | Volume fades of hitsounds. |
| `AccuracyDifficulty`, `HealthDifficulty` | float | Default 8 each. |
| `dual` | enum | `DualMode`: `0` Disabled, `1` Mirrored, `2` Separate (second playfield; the importer computes the key count as `ceil(maxLane / 2)` when `Separate`, so lanes above half belong to the second field [inference]). |
| `ls-v2` | bool | New lane-switch layout flag. |
| `force-169` | bool | Force 16:9 playfield. |
| `editor-time` | long | Editor time counter. |
| `extra-playfields` | int | 0..9 extra playfields (clamped on set). |
| `visualization-enabled` | bool | Audio visualisation. |

Key count = highest `lane` over all hit objects (`KeyCount => HitObjects.Max(x => x.Lane)`); lane numbers are **1-based** (validation: "A hit object in this map is in a lane below 1"); `MinKeymode` default 1, no upper bound (`MaxKeymode = -1`).

### `metadata`

`title`, `title-rm` (romanised), `artist`, `artist-rm`, `mapper`, `difficulty` (name), `source` (audio source), `bg-source`, `cover-source`, `tags` (space-separated string), `previewtime` (int ms).

### `HitObject`

| Field | Type | Meaning |
|---|---|---|
| `time` | double | Start time in **milliseconds**. |
| `lane` | int | 1-based lane. |
| `visual-lane` | float | Visual lane (only for `Tick` notes). Omitted when 0. |
| `holdtime` | double | Hold duration in ms; `> 0` with `type = 0` makes a long note; end time = `time + holdtime`. Omitted when 0. |
| `hitsound` | string | Hitsound name/path (default sound when empty). |
| `group` | string | Scroll group id the note belongs to (omitted when null). |
| `hidden` | bool | Hidden note. |
| `type` | enum | `0` Normal, `1` Tick, `2` Landmine. |

`LongNote = HoldTime > 0 && Type == Normal`; `Landmine = Type == Landmine`. Tick notes are decorative/optional hit objects (no judgement beyond ticks) [inference: from the name `Tick` and the `visual-lane` doc comment; the scoring role was not read].

### `TimingPoint`

`time` (ms), `lane` (editor lane, unused in play), `bpm` (float, default 120, must be > 0), `signature` (int beats per measure, default 4, must be > 0), `hide-lines` (hide beat lines). `MsPerBeat = 60000 / bpm`. A map needs at least one timing point (default `{time 0, bpm 120, signature 4}`).

### `ScrollVelocity`

`time` (ms), `multiplier` (double, default 1), `group` (string, omitted when null), `groups` (list of group ids the SV applies to), and the obsolete `mask` (bool per lane, converted to groups `$1..$n`). Scroll groups are fluXis's way to give different lanes/notes independent SV: `$<n>` is the implicit group of lane n [inference from the `mask` conversion `Groups.Add($"${i + 1}")`].

### `HitSoundFade`

`time` (ms), `sound` (hitsound name), `volume` (double, 0..1 [inference]), `duration` (float ms), `ease` (easing enum from osu-framework).

## Timing model

Pure **millisecond** times; there are no measures/beats in the file: `TimingPoint`s provide BPM and signature for beat lines and the editor snap grid, `ScrollVelocity` provides speed changes (position = integral of multiplier over time; velocity groups allow different SV per lane). Offsets: the Quaver/osu importers bake offsets into times; an in-game `TimeOffsetEvent` ([`.ffx`](../ffx/README.md)) can shift hit windows during the map. Converting `time` to seconds = `time / 1000`.

## Notes

- Normal tap: `type 0`, no `holdtime`.
- Hold (long note): `type 0`, `holdtime > 0`.
- Tick note: `type 1` (with optional `visual-lane`).
- Landmine: `type 2` (`Landmine => Type == Landmine`).
- Hidden: `hidden: true`.
- Chords: several objects with the same `time` and different `lane`.
- Per-note keysound: `hitsound` string (plus fades via `HitSoundFades`).
- Lane switching (changing the visible key count mid-map) is done by `laneswitch` events in the [`.ffx`](../ffx/README.md) file; `FluXisImport` raises the key count to the maximum `Count` seen in lane-switch events.

## Audio & images

`AudioFile` (the song), `BackgroundFile`, `CoverFile`, `VideoFile` are file names resolved inside the mapset folder. A `previewtime` in `metadata` (ms). Hitsounds are referenced by name (custom samples are ordinary files in the set).

## Versions & variants

- The legacy layout kept effects in a custom text file (`LaneSwitch(...)`, `Flash(...)`, `Pulse(...)` lines, see [`.ffx`](../ffx/README.md)); new maps use JSON.
- `ScrollVelocity.mask` (bool list) was replaced by `groups`.
- `PlayfieldFade`/`HitFade` events were replaced by `layerfade`.

## Quirks & pitfalls

- Properties without `[JsonProperty]` (e.g. `AudioFile`, `HitObjects`, `TimingPoints`, `AccuracyDifficulty`) have no explicit name in the source; the serialiser helpers (`Serialize()`/`Deserialize<T>()`) come from the external `flustix.Midori` NuGet package, whose naming policy was **not verified** here. A reader should accept case-insensitive keys. [inference]
- `lane` is 1-based and, in `Separate` dual mode, spans both fields.
- `holdtime` and `visual-lane` are omitted when zero (`DefaultValueHandling.Ignore`).
- Times are doubles (ms); do not assume integers.
- `KeyCount` in the importer is `ceil(maxLane / (isSplit ? 2 : 1))` and then maximised with lane-switch counts.

## Example

No sample in the repo; hand-built from the documented fields (illustrative; key names with explicit attributes are exact, the PascalCase names are unverified):

```json
{
  "AudioFile": "audio.mp3",
  "metadata": { "title": "Example", "artist": "Artist", "mapper": "Me", "difficulty": "4K Easy", "previewtime": 30000 },
  "TimingPoints": [ { "time": 0, "lane": 0, "bpm": 120, "signature": 4, "hide-lines": false } ],
  "ScrollVelocities": [],
  "HitObjects": [
    { "time": 1000, "lane": 1, "hitsound": "", "hidden": false, "type": 0 },
    { "time": 1500, "lane": 3, "holdtime": 500, "hitsound": "", "hidden": false, "type": 0 }
  ]
}
```

## ROX support

Not read by ROX. The model is a close fit to ROX (key columns, tap/hold/mine = Landmine, BPM + SV in ms); lossy parts: Tick notes, scroll groups, dual playfields, effects/camera/playfield events and lane switching.

## Parsers & tools

- fluXis (C#): https://github.com/InventiveRhythm/fluXis (`fluXis/Map/MapInfo.cs`, `Map/Structures/*.cs`, `Import/FluXisImport.cs`, `fluXis.Import.osu|Quaver|Stepmania`).
- Built-in editor.
- Midori (serialisation helpers): NuGet `flustix.Midori` (source not fetched).

## Getting samples

- **Committed**: none. The `InventiveRhythm/fluXis` repository (MIT, commit `4187865461e9bf7d1b8201843b0a522229f87699`, `LICENSE` read) contains no `.fsc`, `.fms` or `.ffx` file (checked on the full file tree), and no hand-written file was added because the JSON key names of properties without `[JsonProperty]` (`AudioFile`, `HitObjects`, `TimingPoints`, ...) depend on the external Midori serialiser and could not be verified. The old pre-2025 Haxe client in `InventiveRhythm/fluXis-archive` uses a different format (`.fluxsc`/`.fluxsm`), not `.fsc`.
- **How to get a real one**: (1) install fluXis (https://github.com/InventiveRhythm/fluXis), get any mapset as `.fms` (maps from the game's online map list, https://fluxis.flux.moe, or exported from the editor; the file name on export is `"{Title} - {Artist} [{Mapper}].fms"` per `MapStore.cs`), rename to `.zip` (it is a ZIP archive) and read the `*.fsc` entries; (2) import an osu!mania or Quaver map with the importers shipped in the repo (`fluXis.Import.osu`, `fluXis.Import.Quaver`) and let the game save it as fluXis maps; (3) the game's data folder is opened from Settings -> General -> Folders -> Open fluXis folder (Windows: `C:\Users\{username}\AppData\Roaming\fluXis\`, per https://fluxis.flux.moe/wiki/skinning); the map files live under it [inference: sub-folder names not read]. Whether the online map download needs a login was not tested.

## Sources

- https://github.com/InventiveRhythm/fluXis (commit `4187865461e9bf7d1b8201843b0a522229f87699`): `fluXis/Map/MapInfo.cs`, `MapMetadata.cs`, `MapColors.cs`, `MapEvents.cs`, `Map/Structures/HitObject.cs`, `TimingPoint.cs`, `ScrollVelocity.cs`, `HitSoundFade.cs`, `fluXis/Import/FluXisImport.cs`, `MapImporter.cs`, `fluXis/Map/MapStore.cs`, `fluXis/Online/API/Models/Maps/DualMode.cs`
