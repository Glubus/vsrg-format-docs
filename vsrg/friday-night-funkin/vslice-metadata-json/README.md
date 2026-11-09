# FNF V-Slice song metadata (`<songid>-metadata.json`, `<songid>-metadata-<variation>.json`)
Kind: metadata

Doc status: complete · ROX: decode only (with the chart file) · Category: vsrg · Encoding: json

## Overview

Song-level file of Friday Night Funkin' 0.3+ ("V-Slice"): name, artist, tempo map, play data (difficulties, characters, stage...), audio offsets. The game caches it for menus (Freeplay); the notes ([`-chart.json`](../vslice-chart-json/README.md)) load only when a song plays. Loose at `data/songs/<songid>/<songid>-metadata.json` (the registry scans `songs/` for `-metadata.json`) or inside an `.fnfc` ZIP (../fnfc/README.md). Source: `docs/FNFC-SPEC.md` (metadata 2.2.2, 2024-04-29), `SongData.hx` (`SongMetadata`, `SongTimeChange`, `SongOffsets`, `SongPlayData`, `SongCharacterData`); `SongRegistry.SONG_METADATA_VERSION = '2.2.4'` (rule `2.2.x`) on main.

## Packaged in

`.fnfc` (zip saved by the Chart Editor: `-metadata.json`, `-chart.json`, audio) and `.fnfmod` (zip of a whole mod from the official Mod Menu: V-Slice chart/metadata files, characters, stages).

## Container & encoding

UTF-8 JSON object. `<songid>-metadata.json` (default variation) or `<songid>-metadata-<variation>.json` (variations listed in the default file's `playData.songVariations`). A `SongMusicData` variant (`music/<id>/<id>-metadata.json`, version `2.0.0`) exists for menu music with the same time fields.

## Structure / metadata

| Key | Type | Meaning |
|---|---|---|
| `version` | semver string | `2.2.x` accepted |
| `songName` | string | human readable name (default `Unknown`) |
| `artist` | string | artist(s) (default `Unknown`) |
| `charter` | string, optional | chart author |
| `divisions` | int, optional | default 96 (ticks per beat for the `ticks` time format [inference]) |
| `looped` | bool, optional | default false |
| `offsets` | object, optional | audio offsets in ms: `instrumental` (float), `altInstrumentals` (id -> float), `vocals` (character id -> float), `altVocals` (id -> id -> float) |
| `playData` | object | see below |
| `generatedBy` | string | free debug string |
| `timeFormat` | `"ms"` / `"ticks"` / `"float"` | default `ms`; the FNFC spec says only `ms` is supported |
| `timeChanges` | array | tempo map; at least one entry with `t = 0` |

`playData`:

| Key | Type | Meaning |
|---|---|---|
| `songVariations` | array of string | variation ids whose `-metadata-<id>.json` / `-chart-<id>.json` exist |
| `difficulties` | array of string | playable difficulty ids |
| `characters` | object | `player`, `girlfriend`, `opponent` (character ids), `instrumental` (id; `''` = `Inst.ogg`), `altInstrumentals` (array), `opponentVocals`, `playerVocals` (arrays of character ids, nullable) |
| `stage` | string | stage id (default constant `mainStage`) |
| `noteStyle` | string | note skin id (default `funkin`) |
| `ratings` | object: difficulty -> int | Freeplay rating |
| `album` | string, nullable | Freeplay album id |
| `stickerPack` | string, nullable | |
| `previewStart`, `previewEnd` | float | Freeplay preview, same unit as time |
| `discordRPCImage` | string | |

`timeChanges[]` (`SongTimeChange`, aliases in brackets):

| Key | Type | Meaning |
|---|---|---|
| `t` | float | timestamp of the change (ms) |
| `b` | float, optional | time in beats; recalculated when absent |
| `bpm` | float | quarter notes per minute; required in the first entry, otherwise defaults to the previous one |
| `n` | int, optional | time signature numerator, default 4 |
| `d` | int, optional | denominator, default 4, power of two |
| `bt` | array of int (or int), optional | beat tuplets: steps per beat, default `[4, 4, 4, 4]` (the source comment says default `[4]` for the int form) |

## Timing model

Piecewise-constant BPM from `timeChanges`, absolute `t` in ms (`timeFormat: "ms"`). A beat is `60000 / bpm` ms; steps per beat come from `bt` (default 4); a measure has `n` beats. Beat position of time `T`: sum of `(t_{i+1} - t_i) * bpm_i / 60000` over preceding segments + `(T - t_last) * bpm_last / 60000`. `offsets.*` shift instrumental/vocals relative to the chart.

## Notes

See the chart file.

## Audio & images

- Files in the same folder/zip, all OGG Vorbis (FNFC-SPEC): `Inst.ogg`, `Inst-<instid>.ogg` (alt instrumental, chosen by `playData.characters.instrumental`), `Voices-<charid>.ogg`, `Voices-<charid>-<variation>.ogg`. Vocals are looked up for the player and opponent ids (`playData.characters.player/opponent`, or `playerVocals`/`opponentVocals`); missing vocals are ignored; `Inst.ogg` is mandatory.
- Freeplay preview via `previewStart`/`previewEnd`; album and sticker pack by id.

## Versions & variants

- `version`: 2.2.2 in FNFC-SPEC (2024-04-29), 2.2.4 in main's constants; loader rule `2.2.x`. `generatedBy` carries the writer's version (community docs: `FNF SongData v2.2.4`).
- Variations (`erect`, `pico`, `bf` in `DEFAULT_VARIATION_LIST` plus custom): one metadata file each.
- `characters.altInstrumentals` and the "Song Offset Data" keys are empty in `FNFC-SPEC.md`; the source (`SongOffsets`) gives the keys above.

## Quirks & pitfalls

- At least one `timeChanges` entry with `t: 0` is mandatory; later entries inherit `bpm`.
- Nullable: `album`, `stickerPack`, `opponentVocals`.
- Do not rely on `timeFormat != "ms"`.
- `ratings` keys follow the difficulty ids.

## Example

Example from the official spec (`docs/FNFC-SPEC.md`, DadBattle, comments removed):

```json
{
  "version": "2.2.2",
  "songName": "DadBattle",
  "artist": "Kawai Sprite",
  "timeFormat": "ms",
  "timeChanges": [ { "t": 0, "bpm": 180 } ],
  "playData": {
    "album": "volume1", "previewStart": 0, "previewEnd": 15000,
    "ratings": { "easy": 1, "normal": 3, "hard": 5 },
    "songVariations": [ "erect" ],
    "difficulties": [ "easy", "normal", "hard" ],
    "characters": { "player": "bf", "girlfriend": "gf", "opponent": "dad" },
    "stage": "mainStage", "noteStyle": "funkin"
  },
  "generatedBy": "EliteMasterEric (by hand)"
}
```

## ROX support

Decode only, with the chart file (`VSliceDecoder`). `timeChanges` become BPM points (`t` ms -> µs, `bpm`, `n` -> signature; sorted, negative time moved to 0, first entry must be at 0 with a `bpm`, absent `bpm` inherits, absent `n` is 4; `d` and `bt` have no ROX equivalent). `songName` is the title, `artist`/`charter` the creator, `playData.ratings` the difficulty value, `previewStart`/`previewEnd` the preview; `audio_file` is empty. Version `2.2.x` only; `timeFormat` other than `ms` is an error.
- `offsets` (ms) shift each stem in the audio plan; positive delays the stem (`Conductor.hx`, `PlayState.hx` 1090, `VoicesGroup.hx` 74-78). Instrumental at `offsets.instrumental` (or `altInstrumentals[id]`); a vocal at that plus `vocals[character]` (or `altVocals[id][character]`).
- The plan names `Inst.ogg` / `Inst-<id>.ogg` (required) and `Voices-<character>[-<variation>].ogg` (optional), as `Song.hx` builds them.

## Parsers & tools

- FNF source (Haxe): https://github.com/FunkinCrew/Funkin/blob/main/source/funkin/data/song/SongData.hx
- Moonchart `FNFVSlice` (needs this metadata file): https://github.com/MaybeMaru/moonchart
- Chart Editor in the game.

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: GameBanana `.fnfc` mods; funkin.assets also holds `-metadata-erect.json` / `-metadata-pico.json`. Observed: version `2.2.4`, `generatedBy` "Friday Night Funkin' - v0.8.1", `bt` [4, 4, 4, 4], `b` in beats; community exports also carry `2.2.3`; one base-game file has 14 `timeChanges`, one has fractional BPM 111.5. Base-game data belongs to The Funkin' Crew Inc.: funkin.assets LICENSE.md is all rights reserved, Funkin `LICENSE.md` makes only the source Apache-2.0.

## Sources

- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/docs/FNFC-SPEC.md
- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/source/funkin/data/song/SongData.hx, `SongRegistry.hx`, `source/funkin/util/Constants.hx`
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (shows a 2.2.4 example)
