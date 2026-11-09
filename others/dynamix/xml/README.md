# Dynamix chart XML (`.xml`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: xml

## Overview
XML chart of Dynamix (C4Cat). Two dialects exist, both loaded by Dynamaker-modified: (A) the `CMap` XML that Dynamaker/Dynamaker-modified saves (elements prefixed `m_`, apparently the serialisation of the game's `CMap` class) and (B) an attribute-based `DynamixMap` XML (the in-game `Center`/`Left`/`Right` layout). Derived from the dynamaker-modified loader/saver (JavaScript) and the DyNode docs; there is no official spec.

## Packaged in
[`dy`](../dy/).

## Container & encoding
UTF-8 XML, one difficulty per file. Dynamaker saves `<MapID> <date>.xml`. DyNode imports `.xml`, `.dyn`, `.dy` and `.osu`. The difficulty is the last letter of the map id (C/N/H/M/G/T/B/D/U = Casual, Normal, Hard, Mega, Giga, Tera, Basic, "Horneee", Custom).

## Structure / metadata

Dialect A (Dynamaker CMap XML), root `CMap` (the saver writes `{CMap: ...}` through an object-to-XML library):

| Element | Meaning |
|---|---|
| `m_path` | song path/id (map id minus its last 2 chars) |
| `m_mapID` | map id (ends with the difficulty letter; real files: `_map_<m_path>_<letter>`, e.g. `_map_Sound Souler - Paradise_H` [observed: camberloid__map_Sound_Souler_-_Paradise.xml]) |
| `m_barPerMin` | tempo in bars per minute |
| `m_timeOffset` | time offset |
| `m_leftRegion`, `m_rightRegion` | `PAD` or `MIXER` for the side areas |
| `m_notes/m_notes/CMapNoteAsset*` | center-area notes |
| `m_notesLeft/m_notes/CMapNoteAsset*`, `m_notesRight/m_notes/CMapNoteAsset*` | side-area notes |
| `m_argument/m_bpmchange/CBpmchange*` | tempo changes: `m_time` (bars), `m_value` (bars per minute) |

`CMapNoteAsset`: `m_id` (int index), `m_type` (`NORMAL`, `CHAIN`, `HOLD`, `SUB`), `m_time` (bars, float), `m_position` (x of the left edge; the editor works with the centre = `m_position + m_width/2` and subtracts `m_width/2` on save), `m_width`, `m_subId` (for a `HOLD` the `m_id` of its `SUB` end note, else -1).

Dialect B (`DynamixMap` XML): root `DynamixMap` with attributes `MapID` (starts with a 5-character prefix, difficulty letter last), `BarPerMinute`, `TimeOffset`; child elements `Center`, `Left`, `Right` (the latter two carry attribute `Type` = `PAD`/`MIXER`), each with `Note` children having attributes `Index`, `SubIndex`, `Position`, `Size`, `Time`, `Type`.

## Timing model

`m_time`/`Time` count bars (not beats or seconds); a bar lasts `60 / BarPerMinute` seconds (Dynamaker: `spu = 60 / bpm`). With `CBpmchange` entries the conversion is piecewise: seconds = sum of `(Δbar) * 60 / value` over segments, then offset. Dynamaker snaps notes to fractions of a bar (e.g. 1/8, 1/4 bar via keys C/V; its internal quantum is 1/32 bar).

## Notes
- `NORMAL`: tap; `CHAIN`: chain note, only in MIXER areas; `HOLD`: hold start, `m_subId` points at its `SUB` end (the SUB note carries the end time and same position/width); `SUB`: hold end.
- Center notes (`m_notes`) fall in the main field; `m_notesLeft`/`m_notesRight` in the side areas (PAD: no chain notes; MIXER: chain notes).
- `m_position` + `m_width`: continuous horizontal placement; Dynamaker snaps to 1/10 and width in tenths (text import divides by 10).

## Audio & images
Unknown (the `.dy` bundle embeds music and background; see `../dy/`).

## Versions & variants
- Dialect A vs B (above).
- Dynamaker text paste format: tokens `n` (NORMAL), `c` (CHAIN), `h` (HOLD, with extra end time), `-` (repeat previous type), `,` (repeat previous value) with `#type`, side switch tokens; positions/widths in tenths.
- `.dy`: JSON `{CMap, remix:{music, bg}}` (see `../dy/`). DyNode's `.dyn` project file is not read.
- [observed: dynode-old-xml-import-test.xml] Dialect B: `<DynamixMap MapID="m_map_songname_H" BarPerMinute="130" TimeOffset="0.15">` with `Center`, `Left Type="PAD"`, `Right Type="MIXER"` children. DyNode's legacy importer derives title and difficulty from `MapID` (title = the part between the 5-character prefix and the last 2 characters; a `f` prefix is also handled).

## Quirks & pitfalls
- Position is the left edge in the XML, the centre in the editor.
- BPM entries are bars-per-minute.
- A single note in a list parses as an object, not an array (XML-to-object libraries collapse single elements): handle both.
- `HOLD`/`SUB` pairs link by `m_subId`; ids are re-assigned on save.

## Example

Illustrative, hand-built from the dialect A field list (not a real chart):

```xml
<CMap>
  <m_path>demo</m_path><m_mapID>demoH</m_mapID>
  <m_barPerMin>30</m_barPerMin><m_timeOffset>0</m_timeOffset>
  <m_leftRegion>PAD</m_leftRegion><m_rightRegion>MIXER</m_rightRegion>
  <m_notes><m_notes>
    <CMapNoteAsset><m_id>0</m_id><m_type>NORMAL</m_type><m_time>1.0</m_time><m_position>1.7</m_position><m_width>0.6</m_width><m_subId>-1</m_subId></CMapNoteAsset>
  </m_notes></m_notes>
  <m_notesLeft><m_notes/></m_notesLeft><m_notesRight><m_notes/></m_notesRight>
  <m_argument><m_bpmchange><CBpmchange><m_time>0</m_time><m_value>30</m_value></CBpmchange></m_bpmchange></m_argument>
</CMap>
```
Time 1.0 bar at 30 bars/minute is 2.0 s.

## ROX support

Not read by ROX.

## Parsers & tools

- Dynamaker-modified (JS/Electron): <https://github.com/jmakxd/dynamaker-modified>
- DyNode (GameMaker): <https://github.com/NagaseIori/DyNode>, <https://dyn.iorinn.moe/en/>
- Dynamaker guide: <https://tlchicken.github.io/dynamaker-guide/>

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: Dynamaker saves `<MapID> <date>.xml` ("Save as XML"); DyNode imports `.xml`, `.dyn`, `.dy`, `.osu` and exports `.xml` (<https://dyn.iorinn.moe/en/guide/import.html>). The fanmade site dye.omegapigame.com (named in the DynamixFanmade README) is dead. Fan charts travel with copyrighted music on community servers/Discord. Official in-game charts: location unknown.

## Sources

- <https://cdn.jsdelivr.net/gh/jmakxd/dynamaker-modified@master/app/src/Script/loadingScene.js>, `function.js`
- <https://dyn.iorinn.moe/en/guide/import.html>
- <https://github.com/TLChicken/dynamaker-guide>
