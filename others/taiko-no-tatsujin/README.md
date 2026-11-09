# Taiko no Tatsujin (and Taiko simulators)

Namco / Bandai Namco drum-hitting rhythm game (arcade since 2001, then consoles and mobile). Two notes (red "don" = drum surface, blue "ka" = drum rim) scroll horizontally from the right towards a fixed judgement circle on the left; drumrolls and balloons are time-spans of repeated hits. Many fan simulators exist (TaikoJiro, TJAPlayer2/3, OpenTaiko, taiko-web, TaikøNauts...).

**Category: others.** Notes move horizontally (not vertically) along a single track, there is no column/key count, and the chart has gimmicks (per-note scroll speed, negative scroll, branches, per-bar speed) that do not fit a fixed-column model. A 4K/"2 notes" conversion is possible but lossy; ROX itself only imports osu!taiko in a converted 4-column layout.

## Formats in this folder

| Folder | Format | Notes |
|---|---|---|
| [tja/](tja/README.md) | `.tja` text chart (TaikoJiro / TJAPlayer / OpenTaiko / taiko-web / OutFox) | de-facto fan standard; also hosts a `GAME:Jube` / `GAME:Konga` mode |
| [fumen/](fumen/README.md) | `.bin` official binary "fumen" (arcade/console), little- or big-endian | reverse engineered (tja2fumen, OpenLibTaiko) |
| [tjf/](tjf/README.md) | `.tjf` Taikosan / TJF EDIT text chart | historic ancestor of TJA, stub |
| [tcc/](tcc/README.md) | `.tci` + `.tcc` Open Taiko Chart (JSON), `.tcm` medley | AioiLight's JSON replacement for TJA |

Related formats documented elsewhere in this repo: `.osu` taiko mode (see `../osu-taiko/`) and Malody `.mc` taiko mode (see the Malody docs). Only mentioned in the TJAPlayer3 documentation (with first-release dates and links): `.tps` (taikopsp), `ot_data.txt` (OniTaiko DS), `data.txt` (owatatsujin, notation similar to simai), `.tmg` (TaikoManyGimmicks), `.tjc` / `genre.ini` / `box.def` / `.t3u8` / `folder.json` / `dan.json` set-level files. Donkey Konga charts are in `../donkey-konga/`.

## Links

- TJAPlayer3 "TJA Format and on" (very complete, simulator-by-simulator): <https://iepiweidieng.github.io/TJAPlayer3/tja>
- taiko-web TJA format page: <https://github.com/269Seahorse/Better-taiko-web/blob/master/TJA-format.mediawiki>
- tja2fumen (fumen reverse engineering): <https://github.com/vivaria/tja2fumen>
