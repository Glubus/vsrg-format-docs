# Taiko no Tatsujin (and Taiko simulators)

Namco / Bandai Namco drum rhythm game (arcade since 2001, then consoles and mobile). Two notes (red "don" = drum surface, blue "ka" = drum rim) scroll from the right to a fixed judgement circle on the left. Drumrolls and balloons are time-spans of repeated hits. Fan simulators include TaikoJiro, TJAPlayer2/3, OpenTaiko, taiko-web and TaikøNauts.

Category: others. Notes move horizontally along a single track with no column count, and charts have gimmicks (per-note scroll speed, negative scroll, branches, per-bar speed) that a fixed-column model cannot hold. A 4K or "2 notes" conversion is lossy. ROX only imports osu!taiko, in a converted 4-column layout.

## Formats in this folder

| Folder | Format | Notes |
|---|---|---|
| [tja/](tja/README.md) | `.tja` text chart (TaikoJiro / TJAPlayer / OpenTaiko / taiko-web / OutFox) | de-facto fan standard; also hosts a `GAME:Jube` / `GAME:Konga` mode |
| [fumen/](fumen/README.md) | `.bin` official binary "fumen" (arcade/console), little- or big-endian | reverse engineered (tja2fumen, OpenLibTaiko) |
| [tjf/](tjf/README.md) | `.tjf` Taikosan / TJF EDIT text chart | historic ancestor of TJA, stub |
| [tcc/](tcc/README.md) | `.tci` + `.tcc` Open Taiko Chart (JSON), `.tcm` medley | AioiLight's JSON replacement for TJA |

Related formats elsewhere in this repo: `.osu` taiko mode (`../osu-taiko/`), Malody `.mc` taiko mode (Malody docs), Donkey Konga charts (`../donkey-konga/`). The TJAPlayer3 documentation only mentions (with first-release dates and links): `.tps` (taikopsp), `ot_data.txt` (OniTaiko DS), `data.txt` (owatatsujin, notation similar to simai), `.tmg` (TaikoManyGimmicks), and the set-level files `.tjc` / `genre.ini` / `box.def` / `.t3u8` / `folder.json` / `dan.json`.

## Links

- TJAPlayer3 "TJA Format and on" (simulator-by-simulator): <https://iepiweidieng.github.io/TJAPlayer3/tja>
- taiko-web TJA format page: <https://github.com/269Seahorse/Better-taiko-web/blob/master/TJA-format.mediawiki>
- tja2fumen (fumen reverse engineering): <https://github.com/vivaria/tja2fumen>
