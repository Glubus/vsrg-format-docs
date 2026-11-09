# FNF V-Slice chart data (`<songid>-chart.json`, `<songid>-chart-<variation>.json`)
Kind: chart

Doc status: complete · ROX: decode only (with the metadata file) · Category: vsrg · Encoding: json

## Overview

Note/event file of Friday Night Funkin' 0.3+ ("V-Slice"). It replaces the legacy `{song: {...}}` file ([../legacy-json/README.md](../legacy-json/README.md)) and holds the notes of every difficulty of one variation plus the song events. Song-level data is in [`-metadata.json`](../vslice-metadata-json/README.md). The shipped game stores both loose (`data/songs/<songid>/<songid>-chart.json`); the chart editor packs them into an `.fnfc` ZIP (../fnfc/README.md). Source: `source/funkin/data/song/SongData.hx` (`SongChartData`), `SongRegistry.hx`, `docs/FNFC-SPEC.md`.

## Packaged in

`.fnfc` (zip saved by the Chart Editor: `-metadata.json`, `-chart.json`, audio) and `.fnfmod` (zip of a whole mod from the official Mod Menu: V-Slice chart/metadata files, characters, stages).

## Container & encoding

- UTF-8 JSON object. `<songid>-chart.json` for the `default` variation, `<songid>-chart-<variation>.json` otherwise (`SongRegistry`: `$id-chart${variation == 'default' ? '' : '-$variation'}`). Variations come from the default metadata (`playData.songVariations`, e.g. `erect`, `pico`, `bf`).
- Semver `version`; the registry accepts `2.0.x` (`SONG_CHART_DATA_VERSION = 2.0.0`, `SONG_CHART_DATA_VERSION_RULE = 2.0.x`).
- Read by `json2object` with field aliases (`t`, `d`, `l`, `k`, `p`, `e`, `v`).

## Structure / metadata

| Key | Type | Meaning |
|---|---|---|
| `version` | semver string | `2.0.0` |
| `scrollSpeed` | object: difficulty id -> float | scroll speed per difficulty; key `default` is the fallback (`getScrollSpeed(diff = 'default')`) |
| `events` | array of event | song events |
| `notes` | object: difficulty id -> array of note | one note list per difficulty of THIS variation |
| `generatedBy` | string | debug string; not read by the game |

Difficulty ids: the base game uses `easy`, `normal`, `hard`, `erect`, `nightmare` (`Constants.DEFAULT_DIFFICULTY_LIST_FULL`; the writers order keys by this list). Custom ids are allowed.

### Note object

| Key | Type | Meaning |
|---|---|---|
| `t` | float | time, in the metadata `timeFormat` (ms in practice) |
| `d` | int | data: `d % 4` = direction (0 left, 1 down, 2 up, 3 right); `floor(d / 4)` = strumline index (0 = player, 1 = opponent, more allowed by `strumlineSize`) |
| `l` | float | sustain length, same unit as `t`; default 0; `l > 0` = hold note (`isHoldNote`) |
| `k` | string | note kind (custom behaviour); `""`/absent = none (the getter normalises `''` to null) |
| `p` | array | `NoteParamData` list `{ "n": name, "v": value }` for custom kinds; default `[]` |

### Event object

| Key | Type | Meaning |
|---|---|---|
| `t` | float | time |
| `e` | string | event kind, e.g. `FocusCamera`, `PlayAnimation` (named in the `SongEventDataRaw` doc comment; scripts can add custom kinds with `ScriptedSongEvent`) |
| `v` | any JSON | event data, schema depends on the kind (e.g. `{"char": 1}` for `FocusCamera` in the community docs); optional |

## Timing model

- Times use the metadata `timeFormat`: `"ms"` is the only one the FNFC spec supports; `SongTimeFormat` lists `ticks`, `float`, `ms` (default). Notes carry no beat or step; the game derives steps from the time and the metadata `timeChanges` (cached `_stepTime`).
- BPM, signature and beat tuplets live only in the metadata `timeChanges` ([../vslice-metadata-json/README.md](../vslice-metadata-json/README.md)); a chart cannot be placed on a beat grid without it.
- Scroll speed is per difficulty (`scrollSpeed`). A draft RFC (`rfc/chart-format/chartformat-7.jsonc` in the Funkin repository) mentions a `SetScrollSpeed` event [seen only in a search-result snippet; not read]. Shipped charts use `ScrollSpeed` with `v` = `{ absolute, duration, ease, scroll, strumline }` [observed: tutorial-chart.json]; `FocusCamera` has a bare integer `v` (strumline index) in `bopeebo-chart.json`.

## Notes

- No sections, no `mustHitSection`: the strumline is in `d` (0-3 player, 4-7 opponent).
- The game builds the hold body from `l`; a hold shorter than a step is possible.
- Kinds (`k`) are scripted note types (`NoteKindManager`); `p` carries their typed parameters.
- No mines in the schema (kinds can implement them).

## Audio & images

None here; `Inst*.ogg` / `Voices-*.ogg` are named by the metadata (`playData.characters`).

## Versions & variants

Chart data `2.0.0` (FNFC-SPEC of 2024-04-29 also says `2.0.0`). One chart and one metadata file per variation. RFC drafts (`rfc/chart-format/*`) were not read.

## Quirks & pitfalls

- `notes` and `scrollSpeed` are maps keyed by difficulty.
- A different `strumlineSize` changes the strumline split in `d`.
- Read `timeFormat` from the metadata; `k` may be `""`.
- Load chart and metadata together to compute beats.

## Example

Hand-built from the field list above (not a real chart); a comparable snippet is on the community page MeguminBOT/FNF-Modding-Engine-Differences:

```json
{
  "version": "2.0.0",
  "scrollSpeed": { "default": 1.0, "hard": 1.8 },
  "notes": {
    "hard": [
      { "t": 1000, "d": 0, "l": 0 },
      { "t": 1500, "d": 5, "l": 400, "k": "", "p": [] }
    ]
  },
  "events": [ { "t": 0, "e": "FocusCamera", "v": { "char": 1 } } ],
  "generatedBy": "hand-built"
}
```

At 1000 ms the player's left arrow; at 1500 ms the opponent's down arrow (`d = 5` -> strumline 1, direction 1) held 400 ms.

## ROX support

Decode only: `VSliceDecoder` (`variants`, `decode_variant`, `decode_with_report`, `decode_with_audio_plan`) with the companion `-metadata.json`. `auto_decode*` routes `<song>-chart[-<variation>].json` (by name, `is_vslice_chart_name`, and content: a top-level `song` means legacy) and reads the metadata next to it.
- One variant per difficulty of `notes`, ordered `easy`, `normal`, `hard`, `erect`, `nightmare`, then other ids by name; a difficulty with no player note is skipped.
- Player strumline only: `d` 0-3 = columns 0-3; `d` >= 4 dropped and counted. `l` > 0 is a hold (ms -> µs). `k` ignored and counted by name; `events` ignored and counted; `p` ignored. Only `timeFormat` `ms`, chart `2.0.x`.
- `scrollSpeed` is reported (`VSliceReport::scroll_speed`), not turned into an SV point. Details: `src/formats/fnf_vslice/mod.rs` in ROX.

## Parsers & tools

- FNF source (Haxe, json2object): https://github.com/FunkinCrew/Funkin/blob/main/source/funkin/data/song/SongData.hx
- Moonchart `FNFVSlice` (Haxe): https://github.com/MaybeMaru/moonchart
- In-game Chart Editor (saves `.fnfc`).
- Codename Engine refuses V-Slice at runtime but imports it in its editor.

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: `.fnfc` exports on GameBanana (search `fnfc`, https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=fnfc&_idGameRow=8694); the game's `preload/data/songs/` tree; the in-game Chart Editor. Observed: shipped events use `ScrollSpeed`, not `SetScrollSpeed`; a difficulty may be an empty list (`ugh-chart-erect.json`, `nonsense-theme-chart.json`: `normal` has 0 notes); `stress-chart.json` has an extra `picospeaker` difficulty; community exports often hold several empty difficulties. Base-game data belongs to The Funkin' Crew Inc.: funkin.assets LICENSE.md is all rights reserved, Funkin `LICENSE.md` makes only the source Apache-2.0.

## Sources

- https://github.com/FunkinCrew/Funkin/blob/main/docs/FNFC-SPEC.md
- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/source/funkin/data/song/SongData.hx, `SongRegistry.hx`, `source/funkin/util/Constants.hx`
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (community example)
