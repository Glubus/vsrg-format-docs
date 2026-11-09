# Dazzle Dazzle Realization chart (`.d2r`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (Shift-JIS era, ASCII keywords)

## Overview

Dazzle Dazzle Realization (D2R) is, per its description page, "basically a practice program for Konami's Dance Dance Revolution" that also plays your own songs with the DDR system (Windows 95/98/NT + DirectX; 16 MB RAM, Pentium 133 MHz; BGM as PCM WAVE or, from version 2, CD-DA). `*.d2r` is "the chart file of Dazzle Dazzle Realization 2ndMIX".

The format was reverse engineered by the editor's author, dated 1999/07/14 (not official; "contents are my own investigation and analysis; commands may have been added, changed, or removed depending on the period"). The Wayback copy of `paramax.hypermart.net/d2r.html` (2003) is the only grammar source; the upstream list (commit `503382a`) links the site root. The editor D2REDIT reads `*.d2r`, `*.sul`, `*.msd`, `*.ddr` and writes `*.d2r`, `*.ddr`, `*.slo`; charts were registered in the "D2R譜面サーチ" database.

## Container & encoding

Plain text edited with Notepad "or a dedicated editor". A line beginning with `*` is a comment. A file is a definition part followed by one or more chart parts, separated by `*---------` comment lines:

```
*---------
<definition part>
*---------
<chart part (BASIC)>
*---------
<chart part (ANOTHER)>
*---------
<chart part (MANIAC)>
*---------
...
```

Charset not stated (Japanese Windows era: Shift-JIS/CP932 [inference]).

## Structure / metadata

Definition part commands (`KEY=value`):

| Command | Meaning |
|---|---|
| `GAMEMODE=string` | `NORMAL`, `HARD` or `ORIGINAL`; anything else is treated as `ORIGINAL` |
| `ID=n` | song ID number; required when set through `id.def` |
| `TITLE=string` | title shown at selection and play |
| `ARTIST=string` | artist shown at selection |
| `MUSIC=file.wav` | the in-play music; "the better the quality, the longer the load"; too long (> about 3 minutes) gives noise/instability |
| `SHORTCUT=file.wav` | the selection-screen sample (too high quality can stall for lack of memory) |
| `TEMPO10=n` | tempo = BPM x 10, range 320..2559 (quarter notes per minute x 10); fix this if arrows drift out of sync over time |
| `DELAY=n` | arrow-vs-music offset; "increasing/decreasing by about 48 shifts the arrows by one arrow" |
| `CDTRACK=n` | CD audio track (when playing from a CD) |
| `CDTRACKFROM=n`, `CDTRACKTO=n` | start/end CD track for multi-track songs |
| `CDTEMPO10=n`, `CDDELAY=n` | tempo/delay when using the CD (see `TEMPO10`, `DELAY`) |
| `START=n` | when the arrows start to light up; 1 = one measure; default 4 |

Chart part commands:

| Command | Meaning |
|---|---|
| `LEVEL=n` | difficulty feet shown at selection |
| `PLAYER=n` | play style: `1` single (versus), `2` couple, `3` double |
| `MODE=string` | `BASIC`, `ANOTHER`, `MANIAC` (otherwise BASIC) |
| `MUSICSTART` / `MUSICEND` | begin/end of the chart; `LEVEL`, `PLAYER`, `MODE` must come before `MUSICSTART` |

## Timing model

Between `MUSICSTART` and `MUSICEND` each line is `[length]:[1P arrows]:[2P arrows]:[option]` ("do not put extra spaces before it"). `[length]` is one of 16 spellings of 7 effective durations (bold = standard; the one-character forms come from the previous version's `.sul` charts and "should not be used much"):

| Symbols | Name | Meaning |
|---|---|---|
| `1P` | whole (1分) | one measure; equals `4P/4P/4P/4P` |
| `2P` / `1p` | half | half measure; equals `4P/4P` |
| `P` / `2p` / `1.` / **`4P`** | quarter | one arrow's height is a quarter |
| `p` / `8P` / `2.` / **`4p`** | eighth | arrows half-overlapping |
| `Q` / `8p` / **`4.`** | sixteenth | half of an eighth |
| `8.` | 32nd | "cannot be recognised as 32nd (two in a row look like a simultaneous step)" |
| `T` | triplet | "always use in sets of three"; three arrows fit in a quarter |

Tempo changes: the `[option]` field, e.g. `T1900` sets `TEMPO10` to 1900 from that line on. The time of a line is the sum of the preceding durations at the current `TEMPO10/10` BPM, plus `DELAY`/`START`. Stops/freezes are not described.

## Notes

`[1P arrows]` and `[2P arrows]` are 4-character fields using `L`, `D`, `U`, `R` in that fixed left-to-right order, with a half-width space for an empty panel (e.g. ` D  `, `L   `, `   R`). Doubles use both fields separated by `:`. A line with no arrows is a rest (`4P:    :    :`). Examples: `4p:   R:    :` (eighth, right), `4p: D  :    :`, `4P:L   :    :`. No hold/freeze or shock arrows in this spec version.

## Audio & images

`MUSIC=` and `SHORTCUT=` take WAVE (PCM); CD-DA tracks use `CDTRACK*` (version 2 onward). No images.

## Versions & variants

- `.sul`: previous version's chart format (source of the `P`, `p`, `Q`, `T`, ... symbols), see [sul](../sul/README.md). `.slo`: [slo](../slo/README.md). `.ddr`: unknown. D2REDIT also reads `.msd` ([MSD](../../ddr/msd/README.md)).
- `GAMEMODE` = `NORMAL` / `HARD` / `ORIGINAL`; the MSD spec likewise has `NORMAL`/`HARD` (replaced by `BASIC` in MSD 2.0).

## Quirks & pitfalls

- `TEMPO10` is an integer BPM x 10 in 320..2559 (32.0 .. 255.9 BPM), so 256+ BPM cannot be represented.
- Old (`P`, `p`, `Q`) and new (`4P`, `4p`, `4.`) length symbols overlap; `2.` is the eighth, `1.` the quarter.
- Spaces are semantic (empty panel); leading spaces break the line; `*` comments only at line start.
- The minimum unit is 1/16 ("最小単位は１６分" in the editor); 192nd/48th quantizations do not exist.
- WAV files over about 3 minutes are unstable.

## Example

Lines from the format page (comments translated):

```
*----
4P:    :    :
*  a quarter-note rest
*----
4p:   R:    :
4p: D  :    :
4P:L   :    :
*  a "bisistep" pattern
*----
4P:    :    :T1900
*  from here on, TEMPO10 = 1900
```

## ROX support

Not read by ROX. A decoder needs the definition/chart split, the duration alias table, `TEMPO10`/option tempo changes, `DELAY` units (about 48 per arrow; unit unclear) and LDUR fields.

## Parsers & tools

D2R itself (closed, http://gauss.takamatsu-nct.ac.jp/~iguchi/ddr/ddr2.htm, "D2R公式サイト", archive not retrievable), D2REDIT/SLOEDIT (~200 KB each, from the chart-search site), no open-source parser known.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (one synthetic `.d2r`).

No real file was found. The "D2R譜面サーチ" site (paramax.hypermart.net) listed user charts but "does not host any copyrighted data". Its editors are on Wayback: D2REDIT (reads `.d2r`/`.sul`/`.ddr`, writes `.d2r`) at https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/d2redit.zip (224,948 bytes; D2REDIT.exe + Japanese readme) and SLOEDIT (`.slo`) at https://web.archive.org/web/20031219024931id_/http://paramax.hypermart.net/sloedit.zip (176,632 bytes; SloEdit.exe, readme.txt, slohead.txt). Neither holds a sample chart. Run D2REDIT (Windows, `*.exe`) and save a new chart, or look for D2R 2ndMIX charts fans uploaded to their own pages [inference].

## Sources

- http://web.archive.org/web/20030807133410/http://paramax.hypermart.net/d2r.html (format, Japanese; translated above)
- http://web.archive.org/web/20031219031749/http://paramax.hypermart.net/whats.html (what D2R is)
- http://web.archive.org/web/20031219024931/http://paramax.hypermart.net/editor.html (D2REDIT / SLOEDIT: supported files)
- http://web.archive.org/web/20040205071612/http://paramax.hypermart.net/ (site root; frameset "D2R譜面サーチ")
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt (`[D2R, SLO] Obscure old Japanese formats`)
