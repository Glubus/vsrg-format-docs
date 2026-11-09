# Beat Saber beatmap files (`<Difficulty>.dat` v2 / v3 / v4, `Lightshow.dat`, `BPMInfo.dat`)
Kind: chart

Doc status: complete (interactable objects, BPM/audio data) / partial (lighting event boxes: field names only) · ROX: no · Category: others · Encoding: json

## Overview

One JSON file per beatmap (characteristic x difficulty), named in `Info.dat` (`_beatmapFilename` v2, `beatmapDataFilename` v4). Typical names: `ExpertPlus.dat`, `Standard.dat`, `ExpertPlusStandard.dat`, `NormalStandard.dat`. It holds cut notes, bombs, walls, arcs, chains, lane-rotation events, waypoints and lighting events. Three schemas: v2 (since 1.0.0, `_`-prefixed long names), v3 (1.20.0, abbreviated names), v4 (1.34.5, objects + metadata arrays, lighting in a separate Lightshow file). "v1" files (`_version` `1.5.0`, a `.json` with `_events`/`_notes`/`_obstacles`, plus `_beatsPerMinute`, `_beatsPerBar`, `_noteJumpSpeed`, `_shuffle`, `_shufflePeriod`) are in the [info doc](../info-dat/README.md) conversion gist.

## Packaged in

BeatSaver `.zip` (`Info.dat`, one difficulty `.dat` each, audio, cover).

## Container & encoding

UTF-8 JSON, possibly gzip-deflated (the game accepts it; the OST uses it from 1.34.5). Fields at default may be omitted (the game fills defaults since 1.31.0; the Official Editor always writes them; ChroMapper has a toggle). v4: `{ "version": "4.0.0" }` is valid, but NPS/note counts on the selection screen need `colorNotes`, `bombNotes`, `obstacles` all present. `customData` / `_customData` blocks hold mod data (Chroma, Noodle, ...).

## Structure / metadata
Version key: `_version` (v2) / `version` (v3, v4). Time `Beat` is a float in beats.

### Grid conventions (all versions)
- `Line Index` (v2 `_lineIndex`, v3/v4 `x`): horizontal column, 0 = leftmost; the standard grid is 4 wide (0-3). Waypoint wiki text: indices 0..3 and layers 0..2 on the grid. Values outside are possible (mapping extensions, walls up to width columns).
- `Line Layer` (`_lineLayer`, `y`): vertical row, 0 = bottom, 0..2 on the standard grid.
- Color: 0 = left saber (red), 1 = right saber (blue).
- Cut direction: 0 Up, 1 Down, 2 Left, 3 Right, 4 Up-Left, 5 Up-Right, 6 Down-Left, 7 Down-Right, 8 Any (dot). Angle offset (v3+): degrees counter-clockwise applied to the direction.
- `Rotation Lane` (v4 `r`): degrees of the lane rotation the object spawns from (360/90 degree characteristics).

### v2 (`_version` 2.0.0 .. 2.6.0)
Top level: `_notes`, `_obstacles`, `_events`; 2.2.0 adds `_waypoints`; 2.4.0 adds `_specialEventsKeywordFilters`; 2.5.0 adds `_floatValue` on events. Arcs `_sliders` are "supported unofficially" (BeatSaber-Deno table; BSMG shows the `_sliders` fields below).

| Collection | Field | Meaning |
|---|---|---|
| `_notes[]` | `_time` | beat |
| | `_lineIndex`, `_lineLayer` | grid position |
| | `_type` | 0 left saber, 1 right saber, 3 bomb (BSMG sample uses `_type: 3` for the bomb) |
| | `_cutDirection` | 0-8 as above |
| `_obstacles[]` | `_type` | 0 full-height wall, 1 crouch wall, 2 free wall (v3-like, then `_lineLayer` and `_height` required) |
| | `_time`, `_duration` | beat, length in beats |
| | `_lineIndex`, `_width` | start column, columns covered |
| | `_lineLayer`, `_height` (type 2 / 2.x later) | row start, rows (1..5) |
| `_events[]` | `_time`, `_type`, `_value` (+ `_floatValue` from 2.5.0) | basic event, see tables |
| `_waypoints[]` (2.2.0) | `_time`, `_lineIndex`, `_lineLayer`, `_offsetDirection` | 0 Up 1 Down 2 Left 3 Right 4 UL 5 UR 6 DL 7 DR |
| `_specialEventsKeywordFilters._keywords[]` (2.4.0) | `_keyword`, `_specialEvents[]` | which special lanes (types 40-43) a keyword enables |
| `_sliders[]` (arc) | `_colorType`, `_headTime`, `_headLineIndex`, `_headLineLayer`, `_headCutDirection`, `_headControlPointLengthMultiplier`, `_tailTime`, `_tailLineIndex`, `_tailLineLayer`, `_tailCutDirection`, `_tailControlPointLengthMultiplier`, `_sliderMidAnchorMode` | arc between head and tail |

Legacy wall conversion to v3 (BSMG): full-height -> layer 0, height 5; crouch -> layer 2, height 3.

### v3 (`version` 3.0.0 .. 3.3.0)
Top-level keys (BSMG samples, 3.3.0): `bpmEvents`, `rotationEvents`, `colorNotes`, `bombNotes`, `obstacles`, `sliders`, `burstSliders`, `basicBeatmapEvents`, `colorBoostBeatmapEvents`, `waypoints`, `basicEventTypesWithKeywords`, `lightColorEventBoxGroups`, `lightRotationEventBoxGroups`, `lightTranslationEventBoxGroups`, `vfxEventBoxGroups` (3.3.0), `useNormalEventsAsCompatibleEvents`. The 3.0.0/3.1.0 samples have color/rotation groups; 3.2.0 adds translation groups; the wiki sample for 3.0.0 lacks `i` in the box group objects that 3.1/3.2 have.

| Collection | Fields |
|---|---|
| `bpmEvents[]` | `b` beat, `m` BPM |
| `rotationEvents[]` | `b`, `e` execution time (0 early, 1 late), `r` degrees (+ clockwise, - counter-clockwise) |
| `colorNotes[]` | `b`, `x`, `y`, `c` color, `d` cut direction, `a` angle offset |
| `bombNotes[]` | `b`, `x`, `y` |
| `obstacles[]` | `b`, `d` duration (beats), `x`, `y`, `w` width, `h` height (vanilla up to 2y per BeatSaber-Deno) |
| `sliders[]` (arcs) | `c` color, `b`, `x`, `y`, `d` head dir, `mu` head control-point length multiplier, `tb`, `tx`, `ty`, `tc` tail dir, `tmu`, `m` mid-anchor mode (0 straight, 1 clockwise, 2 counter-clockwise) |
| `burstSliders[]` (chains) | `c`, `b`, `x`, `y`, `d` head dir, `tb`, `tx`, `ty` tail position, `sc` slice count (head counts), `s` squish factor (portion of head->tail path used) |
| `basicBeatmapEvents[]` | `b`, `et` type, `i` int value, `f` float value |
| `colorBoostBeatmapEvents[]` | `b`, `o` boost on/off |
| `waypoints[]` | `b`, `x`, `y`, `d` offset direction |
| `basicEventTypesWithKeywords.d[]` | `k` keyword, `e[]` event types |
| `lightColorEventBoxGroups[]` etc. | `b` beat, `g` group id, `e[]` event boxes: `f` index filter {`c`,`f`,`p`,`t`,`r`,`n`,`s`,`l`,`d`}, `w`,`d`,`r`/`s`/`t`,`b`..., inner events `e[]` (color) / `l[]` (rotation) etc. Field meanings are on the BSMG lightshow page. |

If an arc head or tail matches a note's time and position, the arc connects with the note and changes scoring. A chain head with cut direction 8 behaves as Down (BSMG note on chains).

### v4 (`version` 4.0.0 / 4.1.0)
Objects reference shared metadata by index: `objects[]` hold time and `i`, `objectsData[]` hold the properties.

| Objects | Fields | Metadata array | Fields |
|---|---|---|---|
| `colorNotes[]` | `b`, `r` rotation lane, `i` | `colorNotesData[]` | `x`, `y`, `c`, `d`, `a` |
| `bombNotes[]` | `b`, `r`, `i` | `bombNotesData[]` | `x`, `y` |
| `obstacles[]` | `b`, `r`, `i` | `obstaclesData[]` | `d`, `x`, `y`, `w`, `h` |
| `arcs[]` | `hb`, `tb` head/tail beat, `hr`, `tr` rotation lanes, `hi`, `ti` head/tail note index into `colorNotesData`, `ai` arc metadata index | `arcsData[]` | `m` head multiplier, `tm` tail multiplier, `a` mid-anchor mode |
| `chains[]` | `hb`, `tb`, `hr`, `tr`, `i` head note index, `ci` chain metadata index | `chainsData[]` | `tx`, `ty` tail position, `c` slice count, `s` squish |
| `spawnRotations[]` | `b`, `i` | `spawnRotationsData[]` | `t` execution time, `r` degrees (assumed deprecated for object `r`) |
| `njsEvents[]` (4.1.0) | `b`, `i` | `njsEventsData[]` [inference from the BSMG annotation "NJS Event Metadata Index"] | `d` relative NJS difference, `e` easing (-1 none, 0 linear, ..., 100-102 Beat Saber specials) per the BSMG table |

Head/tail notes of arcs/chains come from `colorNotes` + `colorNotesData`. Bomb notes have no direction field.

### v4 Lightshow file (`Lightshow.dat`)
Same `version` + objects/data pattern: `basicEvents[{b,i}]` + `basicEventsData[{t,i,f}]`, `colorBoostEvents` + `colorBoostEventsData[{b}]`, `waypoints` + `waypointsData[{x,y,d}]`, `basicEventTypesWithKeywords`, `eventBoxGroups[{b,g,t,e[{f,e,l[{b,i}]}]}]`, `indexFilters[]`, `lightColorEventBoxes[]`, `lightColorEvents[]`, `lightRotationEventBoxes[]`, `lightRotationEvents[]`, `lightTranslationEventBoxes[]`, `lightTranslationEvents[]`, `fxEventBoxes[]`, `floatFxEvents[]`, `useNormalEventsAsCompatibleEvents` (names from the BSMG sample).

### Basic events (lighting) - v2 `_events`, v3 `basicBeatmapEvents`
Type (`_type` / `et`): 0-4, 6, 7, 11 lights; 5 Color Boost (legacy); 8, 9 value/trigger; 10 light / BPM change (legacy); 12, 13 value; 14 early lane rotation (legacy), 15 late lane rotation (legacy); 16-19 value; 40-43 special; 100 BPM change (legacy).
Light values (`_value` / `i`): 0 off; 1-4 secondary color (static/flash/fade/transition); 5-8 primary (static/flash/fade/transition); 9-12 white (static/flash/fade/transition). Color boost: 0 disable, 1 enable. Legacy rotation values: 0 -60, 1 -45, 2 -30, 3 -15 (counter-clockwise), 4 +15, 5 +30, 6 +45, 7 +60 degrees (clockwise). Float value (`_floatValue` / `f`) fine-tunes the effect (v2.5.0+, v3).

## Timing model

Everything is in beats: `seconds = beat * 60 / BPM` at constant BPM (Info `_beatsPerMinute` v2 / `audio.bpm` v4). BPM changes: v3 `bpmEvents` (`b`,`m`); v2 basic event type 100 (`_floatValue` as BPM from 2.5.0; the 2.0.0 sample shows type 10 value 128, legacy). v4 beatmaps have no BPM events: BPM comes from the audio data regions (below), which the Official Editor converts to BPM events. No scroll speed: objects fly at the Info note jump speed (NJS); only the spawn offset and NJS events (4.1.0) change travel. Sub-beat resolution is an arbitrary float (editors snap to 1/N).

## Notes

- Cut notes (`_notes` type 0/1, `colorNotes`): color + cut direction + angle offset on the 4x3 grid; simultaneous notes share `b`.
- Bombs: grid position only. Walls: duration plus x/y/w/h volume.
- Arcs (`sliders`/`arcs`): path between head and tail, curved by control-point multipliers and mid-anchor mode.
- Chains (`burstSliders`/`chains`): head note plus `sc - 1` links toward the tail, with a squish factor.
- Lane rotation (`rotationEvents`, event types 14/15, v4 per-object `r`): for `360Degree` / `90Degree`.
- No holds/mines; mapping to Tap/Hold columns is lossy.

## Audio Data (`BPMInfo.dat` / `AudioData.dat`)
Introduced in 1.22.2 with the Official Editor beta; referenced from v4 Info `audio.audioDataFilename` (v2 Info may point to it, not required).
- v2 (`_version` 2.0.0): `_songSampleCount`, `_songFrequency`, `_regions[{_startSampleIndex,_endSampleIndex,_startBeat,_endBeat}]`.
- v4 (`version` 4.0.0): `songChecksum` (ignored/empty for custom), `songSampleCount`, `songFrequency`, `bpmData[{si,ei,sb,eb}]`, `lufsData[{si,ei,l}]` (loudness normalization per sample range).
The editor converts BPM regions into BPM events in related beatmaps. A region maps sample range [si, ei] to beat range [sb, eb]; seconds for a beat inside a region = (si + (beat - sb) / (eb - sb) x (ei - si)) / songFrequency [inference from field names].

## Audio & images

Not in this file; see Info. Audio: wav or ogg (ogg for BeatSaver).

## Versions & variants

- v1 (1.5.0, `.json`), v2 2.0.0-2.6.0, v3 3.0.0-3.3.0, v4 4.0.0/4.1.0 (BeatSaber-Deno supports v4.1.0, v3.3.0, v2.6.0, v1.5.0).
- v2 -> v3: renamed + abbreviated; free-form walls; `sliders`/`burstSliders`; box-group lighting. v3 -> v4: metadata indexing, lighting in `Lightshow.dat`, per-object rotation, `njsEvents`.
- The game reads older schemas through a compatibility layer. BeatSaber-Deno marks: v2 no angle offset, no chains; v3 vanilla obstacles up to 2y, no NJS event; v4 bomb no direction.
- Mapping Extensions precision coordinates, Noodle Extensions and Chroma live in `customData`.

## Quirks & pitfalls

- v2 bombs are `_notes` with `_type` 3: filter before counting notes.
- v2 event type 10 is both a light and a legacy BPM change; type 100 is BPM change.
- v4 chain head cut direction 8 = Down (BSMG).
- Absent `x`, `y`, `c`, `d`, `a` default to 0 (BSMG: `{ "b": 10.0 }` equals `x:0,y:0`).
- v4 index fields must be in range of the `*Data` array; editing a shared entry affects every referencing object.
- Mods may write line index/layer values < 0 or > 3 via customData / precision values.

## Example
BSMG v3.2.0 sample (trimmed to notes/walls):
```json
{ "version": "3.2.0",
  "colorNotes": [ { "b": 10, "x": 1, "y": 0, "c": 0, "d": 1, "a": 0 } ],
  "bombNotes":  [ { "b": 10, "x": 1, "y": 0 } ],
  "obstacles":  [ { "b": 10, "d": 5, "x": 1, "y": 0, "w": 1, "h": 5 } ],
  "sliders":    [ { "c": 0, "b": 10, "x": 1, "y": 0, "d": 1, "mu": 1, "tb": 15, "tx": 2, "ty": 2, "tc": 0, "tmu": 1, "m": 0 } ],
  "burstSliders": [ { "c": 0, "b": 10, "x": 1, "y": 0, "d": 1, "tb": 15, "tx": 2, "ty": 2, "sc": 3, "s": 0.5 } ] }
```
Origin: https://bsmg.wiki/mapping/map-format/beatmap.html.

## ROX support

Not read by ROX (no Beat Saber codec in ROX 0.8.1).

## Parsers & tools
- BeatSaber-Deno / `bsmap` (TypeScript): https://github.com/KivalEvan/BeatSaber-Deno (schemas v1 to v4, converter, validator)
- ChroMapper (C#): https://github.com/Caeden117/ChroMapper
- MediocreMapAssistant2 (Java): https://git.bsmg.dev/Top_Cat/MediocreMapAssistant2
- ReMapper (TypeScript): https://github.com/Swifter1243/ReMapper
- Converters: https://converter.stormpacer.xyz, https://github.com/benzhenwen/V4-to-V3-lighting
- SimSaber (Python): https://github.com/MetaGuard/SimSaber

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: BeatSaver (https://beatsaver.com; API `https://api.beatsaver.com/search/text/0?q=<term>`, `https://api.beatsaver.com/maps/latest`, zips at `https://cdn.beatsaver.com/<hash>.zip`); searching `cc0` finds maps whose author states a licence. BeatSaber-Deno (`tests/resources/`) has more fixtures. BSMG wiki snippets: `bsmgwiki_*.dat`.

## Sources
- https://bsmg.wiki/mapping/map-format.html
- https://bsmg.wiki/mapping/map-format/beatmap.html
- https://bsmg.wiki/mapping/map-format/lightshow.html
- https://bsmg.wiki/mapping/map-format/audio.html
- https://bsmg.wiki/mapping/map-format/info.html
- https://raw.githubusercontent.com/KivalEvan/BeatSaber-Deno/main/BEATMAP.md
- https://gist.github.com/MCJack123/892b936ef0d18da43ab2764ba97402be
