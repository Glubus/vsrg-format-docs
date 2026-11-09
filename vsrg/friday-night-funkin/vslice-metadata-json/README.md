# FNF V-Slice song metadata (`<songid>-metadata.json`, `<songid>-metadata-<variation>.json`)
Kind: metadata

Doc status: complete · ROX: decode only (with the chart file) · Category: vsrg · Encoding: json

## Overview

The song-level data file of Friday Night Funkin' 0.3+ ("V-Slice"): name, artist, tempo map, play data (difficulties, characters, stage...), audio offsets. It is what the game caches for menus (Freeplay) while the heavy note data ([`-chart.json`](../vslice-chart-json/README.md)) stays unloaded until a song is played. Packed in an `.fnfc` ZIP ([../fnfc/README.md](../fnfc/README.md)) or stored loose at `data/songs/<songid>/<songid>-metadata.json` (the registry scans `songs/` for files ending in `-metadata.json`). Source: `docs/FNFC-SPEC.md` (metadata 2.2.2 at the time of writing 2024-04-29), `SongData.hx` classes `SongMetadata`, `SongTimeChange`, `SongOffsets`, `SongPlayData`, `SongCharacterData`; `SongRegistry.SONG_METADATA_VERSION = '2.2.4'` (rule `2.2.x`) on the main branch.

## Packaged in

- Packaged in [`fnfc`](../fnfc/).
- Packaged in [`fnfmod`](../fnfmod/).

## Container & encoding

UTF-8 JSON, one object. Default variation: `<songid>-metadata.json`; others `<songid>-metadata-<variation>.json` (variations listed in the default file's `playData.songVariations`). Also a `SongMusicData` variant (`music/<id>/<id>-metadata.json`, version `2.0.0`) exists for menu music with the same time fields.

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

Piecewise-constant BPM from `timeChanges`, absolute `t` in ms (with `timeFormat: "ms"`). A beat is `60000 / bpm` ms; steps per beat come from `bt` (default 4); a measure has `n` beats. Position of a time `T` in beats: sum over the preceding segments (`(t_{i+1} - t_i) * bpm_i / 60000`) + `(T - t_last) * bpm_last / 60000`. The chart data (`-chart.json`) refers to times only; the beat grid is derived with these changes. Audio offsets (`offsets.*`) shift instrumental/vocals relative to the chart.

## Notes

Not applicable (see the chart file).

## Audio & images

- Files named by convention in the same folder/zip: `Inst.ogg`, `Inst-<instid>.ogg` (alt instrumental, selected by `playData.characters.instrumental`), `Voices-<charid>.ogg`, `Voices-<charid>-<variation>.ogg`, all OGG Vorbis (FNFC-SPEC). Vocals are looked up for the player and opponent character ids (`playData.characters.player/opponent`, or the `playerVocals`/`opponentVocals` lists); missing vocals are ignored; `Inst.ogg` is mandatory.
- Freeplay preview via `previewStart`/`previewEnd`; album and sticker pack by id.

## Versions & variants

- `version`: 2.2.2 in the FNFC-SPEC (2024-04-29), 2.2.4 on the main branch constants; semver rule `2.2.x` for the loader. `generatedBy` carries the writer's version (community docs show `FNF SongData v2.2.4`).
- Variations (`erect`, `pico`, `bf` in `DEFAULT_VARIATION_LIST` plus custom ones): separate metadata per variation.
- Spec details marked incomplete in the spec itself: `characters.altInstrumentals` and the "Song Offset Data" keys are listed but empty in `FNFC-SPEC.md`; the source (`SongOffsets`) gives the keys above.

## Quirks & pitfalls

- At least one `timeChanges` entry with `t: 0` is mandatory.
- `bpm` may be omitted after the first entry (inherits).
- Several fields are nullable (`album`, `stickerPack`, `opponentVocals`).
- Do not rely on `timeFormat != "ms"`.
- `ratings` keys follow the difficulty ids.

## Example

Real example from the official spec (`docs/FNFC-SPEC.md`, DadBattle, comments removed):

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

Read, decode only, together with the chart file (`VSliceDecoder`): `timeChanges` become BPM points (`t` ms -> µs, `bpm`, `n` -> signature; sorted by time, a negative time moved to 0, the first entry must be at 0 with a `bpm`, an absent `bpm` inherits, an absent `n` is 4; `d` and `bt` have no ROX equivalent). `songName` is the title, `artist`, `charter` the creator, `playData.ratings` the difficulty value, `previewStart`/`previewEnd` the preview. `audio_file` is empty. Version `2.2.x` only; `timeFormat` other than `ms` is an error.
- `offsets` (ms) shift each stem in the audio plan only; a positive value delays the stem (`Conductor.hx`, `PlayState.hx` 1090, `VoicesGroup.hx` 74-78). The instrumental event is at `offsets.instrumental` (or `altInstrumentals[id]`), a vocal event at that plus `vocals[character]` (or `altVocals[id][character]`).
- The plan names `Inst.ogg` / `Inst-<id>.ogg` (not optional) and `Voices-<character>[-<variation>].ogg` (optional), as `Song.hx` builds them.

## Parsers & tools

- FNF source (Haxe): https://github.com/FunkinCrew/Funkin/blob/main/source/funkin/data/song/SongData.hx
- Moonchart `FNFVSlice` (needs this metadata file): https://github.com/MaybeMaru/moonchart
- Chart Editor in the game.

## Sources

- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/docs/FNFC-SPEC.md
- https://raw.githubusercontent.com/FunkinCrew/Funkin/main/source/funkin/data/song/SongData.hx, `SongRegistry.hx`, `source/funkin/util/Constants.hx`
- https://github.com/MeguminBOT/FNF-Modding-Engine-Differences/blob/master/docs/chart-format.md (shows a 2.2.4 example)
