# R2Beat note chart (`.xml`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: xml (euc-kr or gb18030 declared; see below)

## Overview

Per-song obstacle chart of R2Beat / QQ Speed: plain XML in the game's `rnr_script` pack (usually `rnr_script\music` or `music_add`), edited by the custom-song community (自制音速) with R2NoteEditor-family tools (Newton wiki). rmstZ lists it as "R2beat chart, read and write". Official online clients serve obstacle data from the server and keep only key-sound info locally; standalone ("单机") builds keep the full XML (Newton wiki). One file = one song/difficulty.

## Packaged in
`rnr_script` `.pak` archives (a `.pak` is a folder-like package) or loose files. The song list is `music.txt` in `rnr_script` (title, difficulty stars, artist, genre, price, image and XML path). Audio is `rnr_music\<id>\<id>.ogg|mp3` (the XML's BGM path is relative to `rnr_music\`). Cover images are 256x128 24-bit BMP in `rnr_image`. (Newton wiki.)

## Container & encoding
XML text. The nyaruhodoo/r2beat-note editor writes `<?xml version="1.0" encoding="euc-kr"?>` and encodes the bytes as EUC-KR; the MCP editor `mcp-r2beat-note-editor` is reported to save gb18030. No BOM or line-ending rule is documented. Files made by r2beat-note have no indentation and write empty elements as `<X ...></X>`.

## Structure
Reconstructed from the TypeScript editor https://github.com/nyaruhodoo/r2beat-note (commit `32e6128edb7ec008019f5e624a8b5c42f3d16e99`, files `src/pages/NewMusic.vue`, `src/components/NoteEditorHeader.vue`, `src/note.ts`) and the Newton wiki header description (title, BPM, BGM path, delay, key-sound info, length; then one entry per obstacle):

```xml
<?xml version="1.0" encoding="euc-kr"?>
<TITLE Name="song name">
<BPM Frame="0" BPM="175" OriginalBPM="175"></BPM>
<BGM Name="path\song.ogg" Volume="1.00"></BGM>
<DELAY Value="0"></DELAY>
<LENGTH Value="6666"></LENGTH>
<AREA Coord="12" Kind="16" Level="3" FxSndIndex="0"></AREA>
</TITLE>
```

| Element | Attributes |
|---|---|
| `TITLE` (root) | `Name` |
| `BPM` (one per tempo/speed change) | `Frame`, `BPM`, `OriginalBPM` (as written by r2beat-note); R2Note Studio's change-speed window writes `<BPM Frame BPM Speed>` (release notes v1.6). |
| `BGM` | `Name` (relative to `rnr_music\`), `Volume` |
| `DELAY` | `Value`: frames of silence before the main track |
| `LENGTH` | `Value`: r2beat-note writes the last note's `Coord` at export and defaults to `6666` ("only for other editors") |
| `AREA` (one per obstacle) | `Coord`, `Kind`, `Level`, `FxSndIndex` |

Key-sound entries ("Key音") exist in official files; their element layout is Unknown.

[observed in samples/r2beat-viewer_e_song926.xml] Key sounds are `<EFFECT Snd="e_song926/z.mp3" Volume="1.00"></EFFECT>` elements (6 in that file, after `LENGTH`, before the `AREA` list). Each `AREA` references one with `FxSndIndex` (0 = none, 1.. = index of the EFFECT [inference]). [observed in samples/dzsfo_Fight.xml] `BPM` entries use `OriginalBPM` only when it differs from the played BPM. A chart can hold many `BPM` entries (speed changes by `Frame`). `Coord` may be fractional (`130.5`). The declared encoding is `gb18030` there and `euc-kr` in the r2beat-viewer files. `TITLE Name` may be non-ASCII bytes in the declared encoding. The BGM path is `<song>/<song>.mp3`.

## Timing model
`Coord` is the position in beats: 12 coords per beat, 48 per 4/4 measure at standard spacing; 16th notes are 3 coords apart (Newton wiki). The game runs at 60 fps: `Frame = Coord * 300 / BPM` and `Coord = Frame * BPM / 300` (mcp-r2beat-note-editor README; consistent with 12 coords/beat at 60 fps). `DELAY` and `BPM Frame` are in frames. A speed change (变速) is written through the `BPM` frame entries, not through `Coord` (Newton wiki). "Manual speed adjustment" multiplies all coords and edits BPM to change the apparent speed without changing the obstacle kinds.

## Notes
`Kind` / `Level` pairs (Newton wiki table, matching r2beat-note's `NoteType`):

| Obstacle | Up | Down | Left | Right | Up-left | Up-right | Down-left | Down-right | Platform | Left star | Right star |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kind | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 26 | 27 |
| Level | 3 | 3 | 2 | 2 | 5 | 5 | 4 | 4 | 4 | 1 | 1 |

Long obstacles (Level always 5): start / continue / end: up 134/135/136, down 137/138/139, left 140/141/142, right 143/144/145, up-left 128/129/130, up-right 131/132/133. The editor also knows Kind 161 (Level 0, "random"). Other Kinds are read as defaults; some unreleased obstacle models exist (Newton wiki). Early songs used "mosaic" left/right obstacles with Level 3, now disused.

## Audio & images

Not in the chart; see Packaged in. Key sounds are separate audio entries ([inference]).

## Versions & variants

Chinese (QQ Speed), Korean, international, Japanese, HK/TW, Thai, Latin American and Brazilian servers existed (Newton wiki). Whether their XML differ is Unknown.

## Quirks & pitfalls

BGM paths are relative to `rnr_music\`. Encoding is a legacy Korean/Chinese code page. BPM and coords are decoupled from real tempo. Official online obstacle data is not in the client.

## Example

`samples/synthetic-r2beat.xml` (hand-written from the structure above).

## ROX support

Decode only (`rox::formats::r2beat::R2BeatDecoder`, told by content: a `TITLE` root with `BPM Frame` entries). 4 columns, the arrow keys left/down/up/right: Kind 18/17/16/19 taps, diagonals 20-23 two keys, long kinds holds; platform (24), stars (26, 27), random (161) dropped and counted. Time as r2beat-note's `MusicPlayer.vue`: tempo point `i` at `(Frame + DELAY) / 60` s (the first also from 0), `Coord` grows by `BPM / 5` a second from 0 [observed in source: `bpmTimePoints`, `calculatedCoord`; a note's time `(frame + delay) / 60`]. Title decoded with the declared code page; audio = the file name of `BGM`. All 10 corpus charts and the synthetic one decode. Note: r2beat-note's `note.ts` names 18 "rightSpike" and 19 "leftSpike" (the side of the obstacle); the key mapping follows this page's table (18 left, 19 right).

## Parsers & tools
- r2beat-note (Vue/TypeScript editor): https://github.com/nyaruhodoo/r2beat-note
- CustomR2BeatPlugin (VB, plugin system with NoteConvert): https://github.com/Eronana/CustomR2BeatPlugin
- R2Note Studio updates: https://github.com/Hysteria-xyz/R2NoteStudio-Updates ; rmstZ https://lrfasd.github.io/rmstZ/

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: tablez/r2beat-viewer (https://github.com/tablez/r2beat-viewer, viewer https://r2.zako.cc; `res/note_music/e_song<id>/*.xml` and `res/note_music2/<id>/<id>.xml`, 5 charts per pack, 5680 files); dzsfo/r2beat (`rnr_music/<song>/<song>.xml` next to a `.txt` song entry); standalone "R2Beat single" distributions (Newton wiki).

## Sources
- https://www.newton.com.tw/wiki/%E8%87%AA%E8%A3%BD%E9%9F%B3%E9%80%9F (R2Beat custom-song wiki: files, XML parts, Coord, Kind/Level, Frame, Delay)
- https://github.com/nyaruhodoo/r2beat-note (`NewMusic.vue`, `NoteEditorHeader.vue`, `note.ts`)
- https://github.com/Hysteria-xyz/R2NoteStudio-Updates/releases/tag/v1.6 (BPM Frame/Speed, Coord)
- mcp-r2beat-note-editor README (coord/frame formulas, gb18030), seen only through search excerpts (repo page returned 404)
- https://lrfasd.github.io/rmstZ/
