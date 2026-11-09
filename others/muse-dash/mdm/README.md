# Muse Dash custom album (MDM) (`.mdm`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive

## Overview

`.mdm` is the package format of the Muse Dash Modding Community (MDMC) for custom charts loaded by the **CustomAlbums** MelonLoader mod (source: MDMods/CustomAlbums). A chart folder can also be loaded unpacked (`info.json` next to the other files). Nested zips are used for packs (a `.mdp` containing `.mdm` files).

## Contents

- A chart folder in a ZIP: `info.json`, cover, audio and one BMS file per difficulty (`map1.bms`..`map5.bms`).
- Chart format inside: [BMS](../bms/README.md).

## Container & encoding

Zip archive (extension `.mdm`; packs `.mdp` are zips of `.mdm`). Entries searched by CustomAlbums: `info.json`, `cover.png` (also `.gif` animated cover supported per the chart manager docs), `demo` audio, `music` audio (`.mp3`/`.ogg`), `map1.bms` .. `map5.bms` (one per difficulty id), optional `.mp4` cinema video.

## Structure / metadata

`info.json` (class `AlbumInfo`):

| Field | Meaning |
|---|---|
| `name`, `name_romanized`, `author` | titles/artist |
| `levelDesigner`, `levelDesigner1..5` | charters (overall and per difficulty) |
| `bpm` | string |
| `scene` | default `scene_01` |
| `sceneEgg` | scene easter-egg enum |
| `difficulty1..difficulty5` | difficulty labels; `"0"` means the difficulty does not exist |
| `hideBmsMode` (`CLICK`/`PRESS`/`TOGGLE`), `hideBmsDifficulty`, `hideBmsMessage` | hidden-chart unlock |
| `searchTags` | string array |

Difficulty id 1..5 maps to files `map1.bms`..`map5.bms`.

## Timing model

See `../bms/` (BMS measure/tick timing; notes carry absolute seconds after conversion).

## Notes

See `../bms/`.

## Audio & images

`cover.png`/`cover.gif`, `demo` (preview), `music` (full track), optional `.mp4` (needs the Cinema mod).

## Versions & variants

Mod versions track game versions (ver180 for the Long Live Happy Otaku update, ver170 for the old game, per the maintained forks). The chart manager (Lua) can generate and pack MDM files.

## Quirks & pitfalls

The BMS is read with game-specific rules, not like normal BMS (see `../bms/`). Difficulty `"0"` entries are skipped.

## Example

`info.json` of the CloneDash test album [observed in samples/clonedash-all-effects_info.json]:

```json
{
	"name": "All Effects",
	"author": "March",
	"bpm": "120",
	"scene": "scene_01",
	"levelDesigner": "March",
	"difficulty2": "500",
	"searchTags": ["test"]
}
```

Only difficulty 2 exists (`map2.bms`); a minimal package is `info.json` + `map2.bms` (+ audio and cover for actual play) [observed in samples/clonedash-all-effects-noaudio.mdm].

## ROX support

Not read by ROX.

## Parsers & tools

CustomAlbums (C#): <https://github.com/MDMods/CustomAlbums>; chart_manager (Lua): <https://github.com/taypexx/chart_manager>; MDBMSC / iBMSC editors; mdmc-client: <https://github.com/amydevs/mdmc-client>.

## Getting samples

Container only: an `.mdm` is a zip (`info.json`, `mapN.bms`, cover, audio, optional video); this folder holds no archive. Extracted charts and `info.json` files are in [`../bms/samples/`](../bms/samples/SOURCES.md), one subfolder per album. More: <https://mdmc.moe/charts> (API in the BMS fiche), chart_manager (<https://github.com/taypexx/chart_manager>) to pack your own.

## Sources

- <https://cdn.jsdelivr.net/gh/MDMods/CustomAlbums@master/Data/AlbumInfo.cs>
- <https://cdn.jsdelivr.net/gh/MDMods/CustomAlbums@master/Data/Album.cs>
- <https://mdmods.github.io/CustomAlbums/>
- <https://github.com/taypexx/chart_manager> (README)
