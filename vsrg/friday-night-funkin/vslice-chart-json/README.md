# FNF V-Slice chart data (`<songid>-chart.json`, `<songid>-chart-<variation>.json`)
Kind: chart

Doc status: complete · ROX: decode only (with the metadata file) · Category: vsrg · Encoding: json

## Overview

The note/event data file of Friday Night Funkin' 0.3+ ("V-Slice", official game by The Funkin' Crew Inc.). It replaces the legacy `{song: {...}}` file ([../legacy-json/README.md](../legacy-json/README.md)). It contains ONLY the notes of every difficulty of one "variation" and the song events; the song-level data (title, BPM, characters, stage...) is in the companion [`-metadata.json`](../vslice-metadata-json/README.md). Both files are packed by the chart editor into an `.fnfc` ZIP (../fnfc/README.md); the shipped game stores them loose (`data/songs/<songid>/<songid>-chart.json`). Source: `source/funkin/data/song/SongData.hx` (class `SongChartData`), `SongRegistry.hx`, `docs/FNFC-SPEC.md`.

## Packaged in

- Shipped in: `.fnfc` (zip saved by the V-Slice Chart Editor: `-metadata.json`, `-chart.json` and the audio).
- Shipped in: `.fnfmod` (zip of a whole FNF mod from the official Mod Menu: songs as V-Slice chart/metadata files, characters, stages).

## Container & encoding

- UTF-8 JSON, a single object. File name: `<songid>-chart.json` for the `default` variation; `<songid>-chart-<variation>.json` for others (`SongRegistry`: `$id-chart${variation == 'default' ? '' : '-$variation'}`). Variations declared in the default metadata (`playData.songVariations`, e.g. `erect`, `pico`, `bf`).
- Versioned with a semver string; the registry accepts `2.0.x` (`SONG_CHART_DATA_VERSION = 2.0.0`, `SONG_CHART_DATA_VERSION_RULE = 2.0.x`).
- JSON is read by `json2object` with field aliases (`t`, `d`, `l`, `k`, `p`, `e`, `v`).

## Structure / metadata

| Key | Type | Meaning |
|---|---|---|
| `version` | semver string | `2.0.0` |
| `scrollSpeed` | object: difficulty id -> float | scroll speed per difficulty; key `default` is the fallback (`getScrollSpeed(diff = 'default')`) |
| `events` | array of event | song events |
| `notes` | object: difficulty id -> array of note | one note list per difficulty of THIS variation |
| `generatedBy` | string | debug string; not read by the game |

Difficulty ids: the base game uses `easy`, `normal`, `hard`, `erect`, `nightmare` (`Constants.DEFAULT_DIFFICULTY_LIST_FULL`; the writers order keys by this list); custom ids are allowed.

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
| `e` | string | event kind, e.g. `FocusCamera`, `PlayAnimation` (named in the `SongEventDataRaw` doc comment; custom kinds can be added by scripts with `ScriptedSongEvent`) |
| `v` | any JSON | event data, schema depends on the kind (e.g. `{"char": 1}` for `FocusCamera` in the community docs); optional |

## Timing model

- Times are in `timeFormat` of the metadata: `"ms"` is the only format the FNFC spec says is supported; the source enum `SongTimeFormat` lists `ticks`, `float` and `ms` (`ms` = `'ms'` is the default). Notes carry no beat/step: step positions are computed by the game from the time and the metadata `timeChanges` (cached `_stepTime`).
- BPM, time signature and beat tuplets: only in the metadata `timeChanges` ([../vslice-metadata-json/README.md](../vslice-metadata-json/README.md)), so a chart cannot be placed on a beat grid without its metadata.
- Scroll speed is per difficulty (`scrollSpeed`), not per section. A draft RFC of the chart format (`rfc/chart-format/chartformat-7.jsonc` in the Funkin repository) mentions a `SetScrollSpeed` event [seen only in a search-result snippet; the RFC itself was not read]. The shipped charts use an event named `ScrollSpeed` with `v` = `{ absolute, duration, ease, scroll, strumline }` [observed in samples/tutorial-chart.json]; `FocusCamera` has a bare integer `v` (strumline index) in `bopeebo-chart.json`.

## Notes

- No sections, no `mustHitSection`: the strumline is in `d` (0-3 player, 4-7 opponent).
- Holds: `l` ms. The game builds the hold body from `l`; a hold shorter than a step is possible.
- Kinds (`k`) are scripted note types (`NoteKindManager`); `p` carries typed parameters for them.
- No mines in the schema read (note kinds can implement them).

## Audio & images

None here; audio is in `Inst*.ogg` / `Voices-*.ogg` named by the metadata (`playData.characters`).

## Versions & variants

- Variations: separate chart (and metadata) files per variation.
- Version strings: chart data `2.0.0` (current), FNFC-SPEC dated 2024-04-29 also states chart `2.0.0`.
- RFC drafts of the chart format (`rfc/chart-format/*`) exist in the repository but were not read.

## Quirks & pitfalls

- `notes` is a MAP keyed by difficulty, not a list; `scrollSpeed` likewise.
- The strumline index is encoded in `d`; with a different `strumlineSize` the split changes.
- Time unit depends on `timeFormat`; read it from the metadata.
- `k` may be `""`.
- Chart and metadata must be loaded together to compute beats.

## Example

Illustrative, hand-built from the field list above (not a real chart); a comparable snippet appears in the community comparison page MeguminBOT/FNF-Modding-Engine-Differences:

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

Read, decode only: `rox::formats::fnf_vslice::VSliceDecoder` (`variants`, `decode_variant`, `decode_with_report`, `decode_with_audio_plan`) with the companion `-metadata.json` as a second input; `auto_decode*` route a `<song>-chart[-<variation>].json` file (checked by name, `is_vslice_chart_name`, and by content: a top-level `song` means legacy) and read the metadata file next to it.
- One variant per difficulty of the file's `notes` map, ordered `easy`, `normal`, `hard`, `erect`, `nightmare`, then the other ids by name; a difficulty with no player note is not a variant.
- Player strumline only: `d` 0-3 = columns 0-3 of a 4-key chart; `d` 4 and above (opponent, further strumlines) are dropped and counted. `l` > 0 is a hold (ms -> µs); `k` is ignored and counted by name; `events` are ignored and counted; `p` is ignored. Only `timeFormat` `ms`.
- `scrollSpeed` is a constant display speed per difficulty, not a timing change: it is NOT turned into an SV point, it is reported (`VSliceReport::scroll_speed`).
- Version check: chart `2.0.x` only (as `SongRegistry`). Details and every decision: `src/formats/fnf_vslice/mod.rs` in ROX.

## Parsers & tools

- FNF source (Haxe, json2object): https://github.com/FunkinCrew/Funkin/blob/main/source/funkin/data/song/SongData.hx
- Moonchart `FNFVSlice` (Haxe): https://github.com/MaybeMaru/moonchart
- In-game Chart Editor (saves `.fnfc`).
- Codename Engine refuses V-Slice at runtime but imports it in its editor.

## Getting samples

- Committed ([samples/](samples/) and [samples/SOURCES.md](samples/SOURCES.md)): eight charts from FunkinCrew/funkin.assets (`preload/data/songs/...`; FNF base-game data belongs to The Funkin Crew Inc. (funkin.assets LICENSE.md: all rights reserved; Funkin `LICENSE.md`: only the source code is Apache-2.0); the owner accepted that risk, so the charts are committed as downloaded snapshots.), real community charts extracted from `.fnfc` exports and mod packages downloaded from GameBanana (one subfolder per set: `17bucksfull/`, `nonsense-theme/`, `cant-hold-us/`, `lit-up/` (with the erect variation), `love-me/`, `mesmerizer/`, `phony/`, `tengoku-he-ikou/`, `guns-pico-remix/`, `2hot-bf-mix/`, `thorns-erect-fnfc/`), the MeguminBOT/fnf-chart-info-tool thorns-erect test charts and two synthetic charts. The archives themselves are not committed.
- Observed: the shipped events use `ScrollSpeed` (`{absolute, duration, ease, scroll, strumline}`, the fiche had guessed `SetScrollSpeed`); `FocusCamera` carries a bare int `v` in `bopeebo-chart.json`; a difficulty may be an empty list (`ugh-chart-erect.json`, community `nonsense-theme-chart.json`: `normal` has 0 notes); `stress-chart.json` has an extra `picospeaker` difficulty; community exports often contain several empty difficulties.
- More: `.fnfc` exports on GameBanana (search `fnfc`, https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=fnfc&_idGameRow=8694); the game's `preload/data/songs/` tree; the in-game Chart Editor.

## Sources

- https://github.com/FunkinCrew/Funkin/blob/main/docs/FNFC-SPEC.md
- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/source/funkin/data/song/SongData.hx, `SongRegistry.hx`, `source/funkin/util/Constants.hx`
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (community example)
