# QQ Dance mobile chart (`.xml`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: xml (official files also wrapped as `xml.bytes`)

## Overview
XML chart of QQ炫舞手游 (all five modes), documented from the Java project QQX5Tools / qqx5-console (X5DIY / MengLeiFudge), which parses these files to compute "burst" points, and from the rmstZ feature list (read/write "xml (QQ炫舞手游), including star motion, crescent, pinball, traditional, bubble modes"). Only attributes used by those tools are known; the engine's DTD is not public. Star motion and traditional are lane charts (vsrg); crescent (angles), pinball (landing areas) and bubble (free positions) are not column based (others).

## Container & encoding
XML text (UTF-8 presumably). Official 2019 builds stored charts as `*.xml.bytes` (compressed; the qqx5-console tool "converts bytes files of star/pinball/bubble/crescent"; compression undocumented in the pages read). Later builds download charts and the apk has none.

## Structure / metadata
Star motion ("Idol") root element `<Level>` (IdolMapInfo.java in QQX5Tools):

| Element | Content |
|---|---|
| `LevelInfo` | `BPM`, `BeatPerBar` (asserted 4), `BeatLen` (asserted 16), `EnterTimeAdjust`, `NotePreShow`, `LevelTime`, `BarAmount`, `BeginBarLen`, `TrackCount`, `LevelPreTime` (asserted 4000), optional `Star` (difficulty) |
| `MusicInfo` | `Author` (optional), `Title`, `Artist`, `FilePath` (e.g. `audio/bgm/<id>...`) |
| `SectionSeq` | `Section` elements with attributes `type` (`previous`, `begin`, `note`, `showtime`), `startbar`, `endbar`, `mark`, `param1`: structure of the song: previous (endbar 0), begin (startbar 1, endbar 4 or 8), note (A section), showtime (4 bars), optional second note + showtime |
| `IndicatorResetPos` | attribute `PosNum="64"` |
| `NoteInfo/Normal` | `Note` elements and `CombineNote` (group of Note) |
| `ActionSeq` | `Action` attributes `start_bar`, `dance_len`, `seq_len`, `level`, `type` (dance choreography) |
| `CameraSeq` | `Camera` attributes `name`, `bar`, `pos`, `end_bar`, `end_pos` |
| `DancerSort` | list of ints |
| `StageEffectSeq` | `StageEffect` elements with `name` (e.g. `wutai_scene_global_script`, `wutai_scene_note_biaozhun_01`), `bar`, `length` |

Note attributes (from the line-based parsers in `SetBasicInfo.java`):
- star motion: `<Note Bar=".." Pos=".." from_track=".." target_track=".." note_type="short|long|slip|..." EndBar=".." EndPos=".." />`; a long note ends at (`EndBar`,`EndPos`); a slide (`slip`) uses `target_track`.
- crescent (弦月): `<Note Bar Pos track note_type="short|pair|light|long|slip" target_track length>`: `track` is an angle, not a lane; `pair` = two simultaneous notes (`track` and `target_track`), `light` = glide point, `long` has `length` in `Pos` units, `slip` has comma-separated `target_track` and `length` lists.
- pinball (弹珠): `<Note ID Bar Pos Son EndBar EndPos EndArea MoveTime note_type="PinballSingle|PinballSeries|PinballSlip|PinballLong">`: `EndArea` = landing area, `Son` = next note id in a series (`PinballSeries`), empty `Son` on `PinballSlip` = white ball, `PinballLong` = hold.
- bubble (泡泡): `<Pos Bar BeatPos />` (number reset marker) and `<Note Bar BeatPos Track ... EndBar EndPos ID>` (single, green/blue holds).

## Timing model
Bar-based: bar index `Bar` plus `Pos` inside the bar (BeatPerBar 4 beats, `Pos` in sub-beat units; QQX5Tools divides Pos by 2 to get its "box" cells [meaning of the unit: Unknown]). BPM is constant in `LevelInfo` (the AdjustBpm tool rewrites bars/pos for BPM changes; variable BPM inside a chart not observed). Time = bar_start + pos; bar length = 4 beats * 60/BPM [inference]; `EnterTimeAdjust` is a start offset (ms).

## Notes
`TrackCount` lanes in star motion (4 or 5 per the community "5K" previews); `from_track`/`target_track`/`track` give lane indices; holds use `EndBar/EndPos`, slides `target_track`.

## Audio & images
`MusicInfo/FilePath` names the bgm file; no audio in the XML.

## Versions & variants
Per mode (Idol/Classic/Crescent/Pinball/Bubble/Rhythm in QQX5Tools `QQX5MapType`), plus the `xml.bytes` wrapper. PC QQ Dance probably uses a similar `Level` schema [inference].

## Quirks & pitfalls
The line-based parsers rely on attribute order (do not reformat). Official charts are no longer extractable. Free-position modes are lossy in a column model.

## Example
Unknown (no sample file; the tags above come from the cited source code).

## ROX support
Not read.

## Parsers & tools
QQX5Tools (Java/JavaFX): https://github.com/X5DIY/QQX5Tools ; qqx5-console: https://github.com/X5DIY/qqx5-console ; rmstZ: https://lrfasd.github.io/rmstZ/ ; QQX5FireTableGenerator (referenced, repo not reachable).

## Getting samples

None committed: QQX5Tools and qqx5-console hold only Java converters. Per the QQX5Tools README, 2019 APKs store charts as `*.xml.bytes` (compressed); its `BytesToXml` model converts them to XML (star motion, quarter moon, marble, traditional, bubble). Later builds download charts on demand [fiche]. Run QQX5Tools / qqx5-console (https://github.com/X5DIY/QQX5Tools, https://github.com/X5DIY/qqx5-console) on a 2019 APK, or open charts with rmstZ.

## Sources
- https://github.com/X5DIY/QQX5Tools (README, `bean/IdolMapInfo.java`, `model/SetBasicInfo.java`)
- https://github.com/X5DIY/qqx5-console
- https://lrfasd.github.io/rmstZ/
