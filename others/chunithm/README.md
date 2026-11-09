# CHUNITHM

SEGA arcade rhythm game (2015-) played on a 16-cell touch slider plus two sets of infrared sensors ("air") above it. Notes fall from the top towards the judgement line over 16 horizontal cells (columns 0–15, notes can be several cells wide); beyond taps there are holds, slides that move sideways, flicks, mines (damage), air notes (raise the hand), air-holds/air-slides/air-crush (v. "NEW"/"VERSE"-era additions).

**Category: others (borderline).** The playfield is vertical-scrolling with a fixed judgement line and discrete cells, like a 16-key VSRG, **but** notes have variable width and position, slides change position and width over time, air notes are a second, independent input plane, and tracks have per-section speed changes ("SFL") and per-note speed. A fixed-column model (ROX) can only represent tap/hold/flick/mine and loses slides/air. So it is filed under `others/` rather than `vsrg/`.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [c2s/](c2s/README.md) | `.c2s` official text chart (tab-separated, tick-based) | reverse-engineered; used by the arcade and simulators (UMIGURI can't read it directly) |
| [ugc/](ugc/README.md) | `.ugc` UMIGURI Chart v8 (Margrete editor) | documented by its author (inonote) |
| [sus/](sus/README.md) | `.sus` Sliding Universal Score rev2 | Seaurchin-originated community format, also read by UMIGURI, ched, Project Sekai tools |

Other community items: `.mgxc` (Margrete's own format, converted by `mgxc2s`/Margrete2S; its text dump is touched on in the UGC page), `UMIGURI Chara Skill Language` (not a chart). Converters: MuNET ChuChartManager / "新一代多功能音游转谱器" (UGC↔C2S), `mgxc2s`.

## Links

- Suprnova Chunithm-Research (charting): <https://github.com/Suprnova/Chunithm-Research/blob/main/Charting.md>
- UMIGURI + Margrete: <https://umgr.inonote.jp/en>
- Chunithm wiki (gameplay): <https://chunithm.fandom.com/wiki/Game_Mechanics>
