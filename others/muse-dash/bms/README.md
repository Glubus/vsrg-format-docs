# Muse Dash BMS dialect (`.bms`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview
Muse Dash custom album charts (`map1.bms`..`map5.bms`) use BMS syntax (`#KEY value` headers, `#MMMCC:data` lines) with game-specific meaning: 2-character data values are Muse Dash object ids and channels select the lane (air/ground) or special tracks. Official charts are Unity assets; CustomAlbums converts BMS to in-memory note data (`Data/Bms.cs`, `BmsLoader.cs`, the source of this page).

## Packaged in

- `.mdm` (zip of a custom album: `info.json`, `map1.bms`..`map5.bms`, cover, demo, music; a `.mdp` pack is a zip of `.mdm`).

## Container & encoding

Plain text (BMS); lines starting with `#` count, others are ignored. The loader skips `#WAVxx` definitions. `#BPM` is required (> 0); `#GENRE` is expected (a warning is logged if missing).

## Structure / metadata

Headers: `#BPM <float>` / `#BPMxx <float>` (BPM table for channel 08), `#GENRE`; others are stored but unused. Object lines: `#MMMCC:dddd...` where `MMM` = 3-digit measure, `CC` = channel (2 chars), data = pairs of characters.

Channels (from `Bms.Channels`):

| Channel | Role |
|---|---|
| `01` | scene events |
| `02` | time signature |
| `03` | BPM change, hex value directly in data |
| `08` | BPM change via `#BPMxx` table |
| `15`, `16`, `18` | events (boss/effects) |
| `11`, `13`, `31`, `33`, `51`, `53`, `D1`, `D3` | air lane objects (`31`/`33` can become Heart enemies; `D1`/`D3` tap holds) |
| `12`, `14`, `32`, `34`, `52`, `54`, `D2`, `D4` | ground lane objects (same specials: `32`/`34` hearts, `D2`/`D4` tap holds) |
| `SC` | scroll speed change |

Object ids (2-character codes, base-36 digits; selection from `Bms.BmsIds`): `00` none, `01` small, `02` small up, `03` small down, `04`..`06` medium1 (+up/down), `07`..`09` medium2, `0A` large1, `0B` large2, `0C` raider, `0D` hammer, `0E` gemini, `0F` hold, `0G` masher, `0H` gear, `0I` upside-down raider, `0J` upside-down hammer, `0O`..`0W` speed changes (speed 1-3 for both/low/high), `10` music marker, `11`..`18` boss melee/projectile/masher/gear, `1A`/`1B` boss entrance/exit, `1C`..`1H` boss phase control, `1J`..`1M` hide/unhide notes or boss, `1O`..`1X` scene switches (space station, retro city, castle, rainy night, oriental, groove coaster, touhou, djmax, miku), `20` P item, `21` ghost, `22` heart, `23` note, `25`..`2S` visual effects (hide background, screen scroll, scanline ripples, chromatic aberration, vignette, TV static, flashbang, bg stop, mosaic, sepia), `30`..`3F` bullets (medium/small/large + up/down/lane shift) and boss bullets. Full list in `Data/Bms.cs`.

## Timing model
Standard BMS grid: measure `m`, position `i/N` in the measure (`N` = pairs in the data); beat = `measure_start_beats + i/N`. The loader converts to seconds through BPM and time-signature entries (`CalculateNoteTime`). The base BPM entry is stored as `freq = 60 / bpm * 4` (seconds per 4/4 measure). A community editor uses `time = tick * 240 / bpm` [from a search summary of its README, not read in full].

## Notes
The object id sets the note kind; the channel sets the lane. Holds are id `0F` objects whose length comes from the loader's hold-end handling (not read). `0G` masher, `0H` gear etc. are special enemies. Channel sets `3x`, `5x`, `Dx` are alternative layers merged by the loader.

## Audio & images
Music/demo/cover are separate files in the `.mdm` (see `../mdm/`); the `#WAV` table is ignored.

## Versions & variants
Official data differs per game version (scene count grows; "the new scene 12 does not appear in the scene list", CustomAlbums code comment).

## Quirks & pitfalls
- Odd data length rejects the line (warning); the measure number must parse; a key shorter than 5 chars is malformed.
- BPM changes use `03` (direct hex) and `08` (lookup table).
- Object ids are base-36, case-sensitive in the dictionaries (`0A`, `0G`...).

## Example

Real excerpt from a hand-made test chart (CloneDash `TestCharts/test1-alltypes-labeled/map2.bms`, MIT; first measures of the main data, header trimmed) [observed in samples/clonedash-alltypes-labeled_map2.bms]:

```
*---------------------- HEADER FIELD
#PLAYER 3
#GENRE scene_01
#BPM 120
#LNTYPE 1
#WAV01 Small
#WAV0F Hold
*---------------------- MAIN DATA FIELD
#00015:00002I2J
#00053:0000000F
#00114:01020304
#00115:2K002J2K
```

The file starts with a UTF-8 BOM and defines about 116 `#WAVxx` ids; the names are labels, the id in the data matters. Channels `53`/`54` are alternate layers; channel `55` also occurs but is not in the table; channel `15` carries boss/event ids such as `1A`..`1H`.

## ROX support
Not read.

## Parsers & tools

CustomAlbums (C#, `BmsLoader.cs`): <https://github.com/MDMods/CustomAlbums>; MDBMSC editor; iBMSC (generic BMS editor); chart_manager: <https://github.com/taypexx/chart_manager>.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: <https://mdmc.moe/charts>; the site API lists charts at `https://api.mdmc.moe/v3/charts?page=N` and serves `.mdm` zips at `/v3/charts/<id>/download` (as used by themadadder/MDMC-Bulk-Downloader). Extract `mapN.bms` and `info.json` from the zip.

## Sources

- <https://cdn.jsdelivr.net/gh/MDMods/CustomAlbums@master/Data/Bms.cs>
- <https://cdn.jsdelivr.net/gh/MDMods/CustomAlbums@master/BmsLoader.cs>
- <https://github.com/magjangin/muse-dash-bms-editer-test> (appeared in search; used only for the tick formula via the search summary)
