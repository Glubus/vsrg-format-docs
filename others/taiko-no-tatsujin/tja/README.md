# TJA (`.tja`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text (Shift-JIS or UTF-8, line-based)

## Overview

`.tja` is the plain-text chart format of the fan "Taiko no Tatsujin" simulators. It was created by toach for **TaikoJiro** (太鼓さん次郎, first release v0.80, 2008-12-08) as an evolution of the simpler `.tjf` format of Taikosan/TJF EDIT, and borrows ideas from BMS, SM/DWI/MSD (see [TJAPlayer3 doc](https://iepiweidieng.github.io/TJAPlayer3/tja), "About TJA"). It is now read by TaikoJiro 1/2, TJAPlayer2 for.PC, TJAPlayer3 (and forks), OpenTaiko (0auBSQ), taiko-web, Malody (import), Project OutFox (taiko mode), TaikoManyGimmicks, TaikøNauts, and is the input of `tja2fumen` (conversion to the official binary [fumen](../fumen/README.md)).

One `.tja` file holds **all difficulties** (Easy/Normal/Hard/Oni/Ura/Tower/Dan) of one song, plus optionally per-player (2P) variants and branch ("diverge") paths. The audio is an external file named by `WAVE:`. The original README of this repo says the format covers "taiko and jube modes": `GAME:Jube` (and the undocumented `GAME:Bm`) switches the note alphabet to groups of four hexadecimal digits that encode a whole button panel (see [Notes](#notes)). Simulators also support `GAME:Konga` (Donkey Konga style: left/right/clap).

There is no single normative spec: TaikoJiro's `readme.txt` is historically the reference, then every simulator added headers/commands. The most thorough comparative write-up is the TJAPlayer3 "TJA Format and on" page (>5800 lines, with per-simulator behaviour and "OpenTaiko-OutFox standard" proposals); the shortest practical one is the taiko-web wiki page. This README is built from these two plus the TJAPlayer3/tja2fumen parsers.

## Container & encoding

- Plain text, one file per song (all courses inside). Extension `.tja`. In taiko-web hosting the files are renamed `main.tja` + `main.mp3`.
- Charset: historically **Shift-JIS** (or the local ANSI code page: Big5, GBK for some Chinese charts); modern files are **UTF-8 (with or without BOM)**. Support varies: TaikoJiro/TJAP2fPC use the system code page; TJAPlayer3 ≥1.5.2 reads Shift-JIS and UTF-8-BOM; taiko-web reads Shift-JIS, UTF-8 and UTF-8-BOM. Parsers commonly try UTF-8 (BOM) first and fall back to Shift-JIS (tja2fumen does exactly that). tja-tools offers Auto/UTF-8/Shift-JIS/GB18030.
- Line ends: LF or CR+LF. Empty/whitespace-only lines are ignored. `//` starts a comment to end of line (comments never existed in TJF). Leading whitespace is only allowed inside `#START … #END`.
- Companion files (not part of the chart): audio (`.ogg/.wav/.mp3`), `BGIMAGE`/`BGMOVIE`, `.vtt` lyrics, `genre.ini` / `box.def` / `.t3u8` / `.tjc` set-level files.

## Structure / metadata

A file is: **header lines** `NAME:value` (global or per-course), then for each course a block `#START … #END` containing note lines and `#` commands. Course headers (`COURSE:`, `LEVEL:`, `BALLOON:`, `SCOREINIT:`, `SCOREDIFF:`, `STYLE:` …) are placed before the `#START` they belong to; **values carry over to the next course unless redefined** (taiko-web), so a typical file is `…global headers…, COURSE:Oni, LEVEL:8, BALLOON:…, #START … #END, COURSE:Hard, LEVEL:5, …, #START … #END`.

Value syntax: `NAME:value` (optional space after the colon; TaikoJiro keeps trailing spaces of raw strings, TJAP2fPC strips them). Header names are case-insensitive in the parsers inspected (tja2fumen upper-cases them).

### Global headers (taiko-web page; `(i)` = ignored by taiko-web when hosted, `(?)` = unsupported there)

| Header | Meaning |
|---|---|
| `TITLE` (i), `TITLEEN/JA/CN/TW/KO` | song title and translations |
| `SUBTITLE` (i), `SUBTITLEEN…` | subtitle; leading `--` hides, `++` shows it on the result screen |
| `BPM` | initial BPM (float; default 120 in TaikoJiro 1, 0 in TaikoJiro 2); the first-measure tempo |
| `WAVE` (i) | audio file in the same directory |
| `OFFSET` | seconds, float; see [Timing model](#timing-model) |
| `DEMOSTART` (i) | preview start in seconds |
| `GENRE` (i) | J-POP, アニメ, どうよう, バラエティ, ボーカロイド/VOCALOID, クラシック, ゲームミュージック, ナムコオリジナル (taiko-web also accepts other languages / directory names) |
| `SCOREMODE` | 0 = AC1–7 scoring, 1 = AC8–14 (default), 2 = AC0 |
| `MAKER` (i), `LYRICS` (i), `SONGVOL` (?), `SEVOL` (?) | chart author, WebVTT lyrics file, music/SE volume % |
| `SIDE` (?) | `Normal`/1, `Ex`/2, `Both`/3 song-select side |
| `LIFE` (?) | allowed misses before stage failure (0 = unlimited) |
| `GAME` (?) | `Taiko` (default) or `Jube` (forces autoplay in TaikoJiro); OpenTaiko/OutFox add `Konga`; TaikoJiro 1 also knows undocumented `Bm` |
| `HEADSCROLL` (?) | initial scroll speed; `#SCROLL` multiplies it |
| `BGIMAGE`, `BGMOVIE`, `MOVIEOFFSET` (?) | background image/video; video start offset in seconds ≥ 0 |
| `TAIKOWEBSKIN` (i) | taiko-web only: `dir`, `name`, `song`, `stage`, `don` comma-separated name/value pairs |
| `HIDDENBRANCH` (?) | hide branch indication until the branch actually starts |

### Course headers

| Header | Meaning |
|---|---|
| `COURSE` | `Easy`/0, `Normal`/1, `Hard`/2, `Oni`/3, `Edit`/4 (= `Ura`), `Tower`/5, `Dan`/6 (case-insensitive; default Oni). Tower and Dan are unsupported by taiko-web |
| `LEVEL` | stars 1–10 (floored, clipped) |
| `BALLOON` | comma-separated hit counts, one per `7`/`9` note **in order of appearance** |
| `BALLOONNOR/EXP/MAS` (?) | per-branch balloon lists (Normal/Advanced/Master) |
| `SCOREINIT`, `SCOREDIFF` | score "INIT" and "DIFF" of the scoring formula (tja2fumen takes the last comma-separated value) |
| `STYLE` (?) | `Single`/1 (default) or `Double`/`Couple`/2; for Double use `#START P1` / `#START P2` |
| `EXAM1..3` (?) | Dan-mode gauges: `condition,red,gold,scope` (g gauge %, jp GOOD, jg OK, jb BAD, s score, r drumroll hits, h hits, c max combo; scope m = more / l = less) |
| `GAUGEINCR` (?) | `Normal`/`Floor`/`Round`/`NotFix`/`Ceiling` gauge rounding |
| `TOTAL` (?) | gauge multiplier in % |

TJAPlayer3 / OpenTaiko add many more (`ARTIST`, `AUTHOR`, `COVER`, `PREIMAGE`, `SIDEREV`, `EXPLICIT`, `SCENEPRESET`, `SONGGENREID`, `TOWERTYPE`, `DANTICK`, `DANTICKCOLOR`, `SELECTBG`, `BGOFFSET`, `COMPAT`, `LIFE` for towers, `SONG`…): see TJAPlayer3 page.

### Scoring formulas (SCOREMODE)

All scores are divided by 10, rounded toward −∞, then multiplied by 10. `SCOREMODE:0`: `INIT` per note below combo 200, `INIT+DIFF` from 200. `SCOREMODE:1`: `INIT + max(0, DIFF·floor((min(COMBO,100)−1)/10))`. `SCOREMODE:2`: `INIT + DIFF·{COMBO≥100:8, ≥50:4, ≥30:2, ≥10:1, else 0}`. Go-go time multiplies by 1.2.

## Timing model

Position-based (beat/measure), like BMS: notes carry no time stamp; time is derived from BPM, measure length, delays and the order of symbols.

1. A measure is the text between two `,` terminators (the `,` can follow the last note symbol or be alone). Any number of note symbols is allowed (TaikoJiro crashes above 511). The measure's beat length is `4 × numerator / denominator` beats (`#MEASURE n/d`, default 4/4).
2. The measure is divided **equally by its number of symbols** (`12,` ≡ `1020,` ≡ `10002000,`). Each symbol has division weight 1; the terminating `,` has weight 0 if the measure has ≥1 symbol, else 1 — so `,` alone is one empty measure of 4/4, and an empty line with just `,` advances a whole measure (TJAPlayer2 for.PC before 2018-04-06 and indented-`,` handling in TJAPlayer3 differ: see Quirks).
3. Time of a measure: `60000 × measure_beats / BPM` ms, i.e. `60000·MEASURE·4 / BPM` with MEASURE = n/d. A symbol at index `i` of `N` symbols occurs at `measure_start + i/N · measure_duration`.
4. `#BPMCHANGE x` may appear **mid-measure** (between two note lines of the same measure); subsequent divisions use the new BPM. `#MEASURE` may only be placed between measures. `#DELAY s` (seconds, float, may be negative) shifts the cursor; it may be mid-measure. `#SCROLL` and `#GOGO*` do not affect timing.
5. **OFFSET**: `OFFSET = time_of_audio_start − time_of_chart_start` (seconds). The chart start (`#START`, first measure) is therefore at `−OFFSET` seconds on the audio timeline: `OFFSET:-2.077` → first bar at 2.077 s of the audio. (taiko-web: summed with the database `offset`.)
6. A branch path (`#N/#E/#M`) is parsed from the same start cursor; all paths must end at the same time.
7. Negative/zero BPM, MEASURE or DELAY (overlapping notes) exist in advanced charts and behave per simulator; the OpenTaiko-OutFox draft standardises some of it. TaikoJiro rounds the cursor to 1 ms after a `#BPMCHANGE` (TaikoJiro 1), which creates uneven spacing at extreme BPM.

Position to time (pseudo-code):

```
t = -OFFSET ; bpm = BPM ; meas = 4/4
for each measure:
    n = count of note symbols (≥1; empty measure counts 1 slot)
    for each line in measure: process commands in order (#BPMCHANGE → bpm, #DELAY → t += s, #MEASURE only before measure)
    dur = 60 * 4*meas / bpm          # re-evaluated if #BPMCHANGE occurs mid measure for the remaining slots
    symbol k occurs at t + k/n * dur
    t += dur
```

## Notes

Symbols (Taiko mode, `GAME:Taiko`, first seen in TaikoJiro v0.80 unless stated). Digits are universal; letters are extensions:

| Char | Note |
|---|---|
| `0` | blank |
| `1` | don (red, small) |
| `2` | ka (blue, small) |
| `3` | DON (red, big; strong hit) |
| `4` | KA (blue, big) |
| `5` | drumroll head (small, yellow) |
| `6` | DRUMROLL head (big) |
| `7` | balloon (burst) head; hit count from `BALLOON:` |
| `8` | explicit end of a roll/balloon (otherwise blank) |
| `9` | kusudama / special balloon (same as `7` in TJAP2fPC and OpenTaiko ≤0.6.0; in the AC games a shared-count party-popper) |
| `A`, `B` | multiplayer "hands" DON / KA (hit by both players) |
| `C` | bomb / mine (don't hit) |
| `D` | fuse/"time bomb" roll (OpenTaiko) |
| `F` | AD-LIB hidden note (combo-neutral, never BAD) |
| `G` | swap note: surface + rim (green in taiko-web plugin, purple in OpenTaiko) |
| `H`, `I` | OpenTaiko: `I` ≡ `5` (rim roll in the OutFox draft), `H` ≡ `6` (don roll in the draft) |
| `E`, `J`… | parsed by OutFox/OpenTaiko in some modes; `tja2fumen` maps `E`→DON2(hands), `G`→KA2, `H`→big roll, `I`→roll, `C` blank (see below) |

- **Rolls/balloons** end at the first `8`, or (TaikoJiro) at the next hit-type symbol (50 ms before it in charts without branches; 8/53 s ≈ 150.9 ms before in the Normal path of branched charts; 0 ms in other paths), or at the last symbol of the chart. Between head and `8` either `0` or repeats of the head may appear: `5008` ≡ `5558`. In TJAPlayer2 for.PC, rolls must end with `8`. Official games end rolls 1/48 note early; a `7` ended by a hit-type note makes that note unhittable until the balloon is popped (TaikoJiro ≥2.36, OpenTaiko ≥0.6.0.93).
- **Balloon count order**: one entry of `BALLOON:` per `7`/`9`, in the order they occur **including notes in non-played branches** (values must be repeated for branches); `#N/#E/#M` skipped paths still advance the iterator.
- **Konga mode** (`GAME:Konga`, OpenTaiko ≥0.5.4 / OutFox / taiko-web plugin): `1` right bongo, `2` left bongo, `3` both, `4` clap, `5` right roll, `I` left roll, `6` both roll, `H` clap roll, `7` balloon, `9` special, `C` bomb, `F` ad-lib, `G`≡`3`, `J`≡`4`, `A`/`B` hands. OutFox additionally drafts `GAME:Beatz` (Squid Beatz layout: `1`/`2` single, `3`/`4` double, `G L K J` combinations).
- **Jube mode** (`GAME:Jube`, TaikoJiro v2.13, non-standard, forces autoplay): unlike the other modes, **every 4 hexadecimal digits form one note combination (one time slot)**: one digit per row of the 4×4 panel, each digit being the 4-bit on/off pattern of that row (`■■□■` = 1101 = `D`). The layout `■■□■ / □■■□ / □□□■ / □□□□` is written `D610`. All whitespace is ignored by TaikoJiro; by convention a space is written every 4 digits. Tap notes only (no holds). Example from TaikoJiro's readme. `GAME:Bm` (TaikoJiro 1, never documented) works the same way with a BMS-style layout (P1 scratch + keys, P2 keys; `D600` example), tap/scratch only, no hold, no keysounds.
- Hit windows are not in the chart; official: GOOD ±25/±41.7 ms, OK ±75/±108.3 ms, BAD ±108.3/±125 ms (Oni-Hard / Easy-Normal).

## Commands (inside `#START … #END`)

| Command | Effect |
|---|---|
| `#START` / `#START P1` / `#START P2` / `#END` | chart start/end; `P1`/`P2` select 2-player charts (tja2fumen also tolerates `1P`/`2P`) |
| `#MEASURE n/d` | time signature; only between measures |
| `#BPMCHANGE x` | tempo, may be mid-measure |
| `#DELAY s` | shift following notation by s seconds, may be mid-measure |
| `#SCROLL x` | note speed multiplier (visual only, x≠0, negative = from the left; TJAPlayer3/OutFox/OpenTaiko accept complex numbers `a+bi` for vertical scroll) |
| `#GOGOSTART` / `#GOGOEND` | Go-Go Time (score ×1.2) |
| `#BARLINEOFF` / `#BARLINEON` | hide/show bar lines |
| `#BARLINE` (draft 1.2), `#BARLINESCROLL`, `#HISPEED`, `#DIRECTION n`, `#SUDDEN a b`, `#JPOSSCROLL t px dir`, `#NOTESPAWN`, `#JUDGEDELAY` | simulator gimmicks; `#DIRECTION` 0 right … 7 bottom-left; unsupported in taiko-web |
| `#BMSCROLL` / `#HBSCROLL` / `#NMSCROLL` | scroll mode (before `#START` in TaikoJiro): BMS-like constant spacing, `#BPMCHANGE` changes speed suddenly, `#DELAY` stops scrolling |
| `#BRANCHSTART type,adv,master` | start a branch section (see below) |
| `#N`, `#E`, `#M` | Normal / Advanced (Professional) / Master path |
| `#BRANCHEND` | end branching (visual state retained) |
| `#SECTION` | reset accuracy counters at the next measure |
| `#LEVELHOLD` | freeze the currently played branch until song end |
| `#LYRIC text` | lyric line (`\n` line break); ignored if `LYRICS:` is set |
| `#SENOTECHANGE n` | force the note vocal (1 ドン 2 ド 3 コ 4 カッ 5 カ 6 ドン(大) 7 カッ(大) 8 連打 9 ー 10 ーっ!! 11 連打(大) 12 ふうせん) for the next don/ka |
| `#NEXTSONG title,sub,genre,wave,scoreinit,scorediff` | Dan course: switch song (escape `,` as `\,`) |
| `#GAMETYPE`, `#GIANTNOTE`, `#PARTNERNOTE`, `#ENABLEDORON`/`#DISABLEDORON`, `#DUMMYSTART/END`, `#GRADATION`, `#INCLUDE`, `#SPLITLANE/#MERGELANE`, `#BORDERCOLOR`, `#CHANGETEXTURE/#RESETTEXTURE`, `#SETCONFIG`, `#BGAON/OFF`, `#LUAMOD`… | TJAPlayer3 / OpenTaiko / OutFox extensions (draft standard "Komi spec" 1.0–2.0): see TJAPlayer3 page |

### Branches (diverge)

`#BRANCHSTART p,75,85` — type `p` = accuracy percentage (GOOD = 1, OK = 0.5, BAD = 0; all missable notes since the last `#SECTION` up to the measure **before** the branch point); `r` = drumroll + balloon hit count; (OpenTaiko 0.6 adds `P`, `pp`, `PP`, `jp`, `jg`, `jb`, `lc:`, `lt` and range suffix `l/le/m/me`). The two numbers are the minimum value for Advanced and Master; an impossible threshold (>100 or negative, or Advanced > Master) disables a path. Each path is written `#N`/`#E`/`#M` followed by its measures; skipped paths are ignored during play but their `BALLOON` counts still count. The determining point is one measure before `#BRANCHSTART` in simulators; in the official games it is exactly 4 beats before the branch point. The first bar line after `#BRANCHSTART` is yellow. All paths must have equal duration.

## Audio & images

`WAVE:` filename (relative to the TJA), `DEMOSTART:` preview start (s), `OFFSET:` as above, `SONGVOL`/`SEVOL` %, `BGIMAGE:`/`BGMOVIE:`/`MOVIEOFFSET:`, `LYRICS:` (WebVTT file with optional `Offset:` and `<ruby>`/`<lang xx>` tags). There are **no keysounds**: only one music file. `COVER:`/`PREIMAGE:` jackets in TJAPlayer3/OpenTaiko; taiko-web uses its own database for these.

## Versions & variants

- **TJF** (Taikosan/TJF EDIT, 2004-2007): `0-7` per 1/16 note, no `,`, no `8`, no comments, command `#GOMUSIC`; see [../tjf](../tjf/README.md).
- **TaikoJiro 1 / 2** (2008-2013): the "standard"; v1.63 added branches; v1.29 float BPM; v2.13 `GAME:Jube`.
- **TJAPlayer2 for.PC / TJAPlayer3 / TJAPlayer3-f / OpenTaiko**: add many headers/commands; OpenTaiko (0auBSQ) adds Konga mode, `#BRANCHSTART lc:`..., `#GAMETYPE`, Lua. The OpenTaiko-OutFox "standard" (Komi spec 1.0 → 2.0) tries to unify.
- **taiko-web**: subset (no `Tower/Dan`, `STYLE`, `EXAM`, `BALLOONNOR…`, `LEVELHOLD`, negative `#SCROLL`…). Level of branch songs is stored with a " B" suffix in its database.
- **TMG** (TaikoManyGimmicks 0.6.1α+): TJA-like syntax with `#COMMAND(args)` parentheses and math expressions; converts TJA automatically.
- **Official fumen `.bin`** and **`.osu`/`.mc` taiko mode** are different formats (see [fumen](../fumen/README.md), osu docs).

## Quirks & pitfalls

- Encoding must be detected (Shift-JIS vs UTF-8); BOM may be present; `//` in titles (URLs) is a comment unless the value is a raw string for the simulator.
- Typos are common in the wild and silently ignored by lenient parsers: the repository samples contain `#BPMCANHE` and `#BPMCAHNGE` (ignored by TaikoJiro-like parsers, so the tempo change is lost); a strict parser must decide to accept or reject.
- The terminating `,` is part of the note line (`1020,`) but may also be on its own line; a line like `,` is an empty measure; commands may sit between lines of the same measure; a measure is not terminated until `,`.
- TJAP2fPC ≥2018040600 and TJAPlayer3 treat an *indented* `,` as weight 0 and unindented as weight 1; OpenTaiko ≥0.6.0.12 does not. Before 2018-04-06 an empty measure had 0 duration in TJAP2fPC.
- `BALLOON:` counts: the list must have one value per `7`/`9` note in file order; with branches the values of every path are consumed in order (skipped paths still iterate the list), so they must be repeated per path.
- `OFFSET` sign is the opposite of DWI `#GAP` and the same as SM `#OFFSET`.
- Negative `BPM:` / `#BPMCHANGE` / `#DELAY` / `#MEASURE`, `#SCROLL` 0, complex scroll and overlapping rolls are simulator-defined; TaikoJiro 2 freezes on negative `BPM:`.
- Dan charts and Towers use `COURSE` 5/6 and several `#NEXTSONG`; STYLE:Double charts contain two `#START P1/P2` blocks per course.
- Header values can contain `:` (titles) — split on the first colon only. A header may legally appear without a following course (global defaults).
- Chart content before the first `COURSE:` header: tja2fumen warns and drops it; default course is Oni.

## Example

Real data: first lines of `samples/Advance Adventure.tja` (from this repo; a Taiko Jiro sample chart):

```
TITLE:Advance Adventure
LEVEL:5
BPM:168
WAVE:Advance Adventure.ogg
OFFSET:-5.885
BALLOON:5,5,6,8,13
SONGVOL:100
SEVOL:100

#START
#GOGOSTART
3000102000200030,
0010200020002000,
3000102000200030,
0010200020000000,
#GOGOEND
1000101020101110,
```

Other samples in [`samples/`](samples/) exercise `#MEASURE`, `#BPMCHANGE`, `#SCROLL`, `#DELAY`, `#BARLINEOFF`, `SCOREMODE`, `COURSE`. None of the bundled samples contains `#BRANCHSTART` or `GAME:Jube`. A hand-built illustration of the timing rule (illustrative, hand-built from the rules above): at `BPM:120`, `OFFSET:-1`, the line `10,` (2 symbols, 4/4) places a don at t = 1.000 s and a blank at 2.000 s; the next measure starts at 3.000 s.

## ROX support

Not read by ROX (0.8.1): there is no TJA codec in `src/formats` (only `taiko` for the `.osu` taiko decoder, which converts to a 4-column layout). A TJA→ROX conversion would need the same lossy 2-note→column mapping as the osu!taiko decoder.

## Parsers & tools

- [taiko-web](https://github.com/bui/taiko-web) (JavaScript) — `parsetja.js`; fork with docs: [Better-taiko-web](https://github.com/269Seahorse/Better-taiko-web)
- [WHMHammer/tja-tools](https://github.com/WHMHammer/tja-tools) (JavaScript, `parseTJA.js`, chart visualiser / editor, fork of Snack)
- [jozsefsallai/tja-js](https://github.com/jozsefsallai/tja-js) (TypeScript/JS parser lib)
- [vivaria/tja2fumen](https://github.com/vivaria/tja2fumen) (Python; `parse_tja`, TJA→fumen) — mirror at <https://gitea.tendokyu.moe/vivaria/tja2fumen>
- [AioiLight/TJAPlayer3](https://github.com/AioiLight/TJAPlayer3) (C#, `CDTX.cs` is the reference implementation); [OpenTaiko](https://github.com/0auBSQ/OpenTaiko) (C#)
- TaikoJiro (Windows, closed), TJAPlayer2 for.PC; [Yonokid/PyTaiko](https://github.com/Yonokid/PyTaiko) and YataiDON (Python, TJAParser, see DeepWiki pages below)
- TJA Editor (<https://keishispl.github.io/tja-editor/>), TJA Tools web (<https://whmhammer.github.io/tja-tools>)
- Converters: mc2tja, kongamidtotja (Donkey Konga MIDI → TJA), TakoTako/TJAConvert (TJA+audio → official game mod)

## Sources

- <https://github.com/269Seahorse/Better-taiko-web/blob/master/TJA-format.mediawiki> (opened in full)
- <https://iepiweidieng.github.io/TJAPlayer3/tja> (opened: formats table, lexical rules, BPM/OFFSET/BRANCHSTART/note symbol/Jube/Bm/Konga sections)
- <https://raw.githubusercontent.com/vivaria/tja2fumen/main/README.md> and `src/tja2fumen/parsers.py` / `constants.py` (opened)
- <https://deepwiki.com/Yonokid/PyTaiko/4.1-tja-chart-file-processing>, <https://deepwiki.com/Yonokid/YataiDON/4.1-tja-chart-format> (search results only)
- <https://wikiwiki.jp/jiro/太鼓さん次郎> and <https://web.archive.org/web/20190914085205/https://aioilight.space/taiko/tjap3/doc/tja/> (cited by the above, not opened)
- Repo samples: `samples/*.tja`; `ORIGINAL_README.md` line "tja: Taiko Jiro chart, including taiko and jube modes"
