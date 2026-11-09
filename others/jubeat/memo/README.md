# jubeat analyser "memo" formats (`.txt`: `#memo`, `#memo1`, `#memo2`, `#boogie`, mono-column, youbeat)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (Shift-JIS / shift-jis-2004, byte-level)

## Overview

**jubeat analyser** is a Japanese fan jubeat simulator; its charts are hand-written text files ("memo" files) whose note area is a **drawing of the 4×4 panel grid**: you write the panel states for each frame, with a column giving the timing. Several dialects exist and are all handled by jubeatools: `#memo` (youbeat-like but a bar division always means a 1/4 note), `#memo1` (youbeat-like without BPM changes in the bar), `#memo2` (double-width), `#boogie` (youbeat-like), the headerless **mono-column** (1列形式) format, plus the **youbeat/yubiosi** (v1.0, 1.5, 2.0) dialects and "iboogie". File extension is typically `.txt`. The usage notes at yuisin.com show the minimal file: `t=1`, `o=1000`, `m=""`, `#memo1`.

Category: **others** — grid positions, not lanes.

## Container & encoding

- Plain text, **Shift-JIS(-2004)**; jubeat analyser works at the byte level and jubeatools decodes with `shift-jis-2004` + `surrogateescape` for the occasional undecodable bytes.
- `//` starts a comment; empty lines separate / are ignored.
- Mono-column files use `--` separator lines; the double-column formats must not contain them.
- One file = one chart (difficulty in `#dif`). Metadata and chart are in the same file.

## Structure / metadata

Commands, one per line (jubeatools grammar: `#key[=value]` or `letter=value`, string values in double quotes, numbers may be negative decimals):

| Command | Meaning |
|---|---|
| `t=<decimal>` | tempo (BPM), may change between sections |
| `o=<int>` | offset in ms (100 by default; time between audio start and chart start) |
| `m="<path>"` | music file |
| `b=<decimal>` | beats per measure ("section"), 4 by default |
| `r=<int>` | "increase the offset?" in ms — unsupported in jubeatools, purpose unknown |
| `#memo`, `#memo1`, `#memo2`, `#boogie` | select dialect (a dialect command in the wrong parser raises "wrong format") |
| `#pw=<int>`, `#ph=<int>` | panels horizontally/vertically (4 by default) |
| `#lev=<int>` | chart level (1–10) |
| `#dif=<n>` | difficulty: 1 BSC, 2 ADV, 3 EXT |
| `#title="…"`, `#artist="…"`, `#jacket="<path>"`, `#prevpos=<int>` (preview start ms) | metadata |
| `#bpp` | bytes per panel symbol (default 2) |
| `#circlefree=<0 or 1>` | "circle-free" timing symbols (only with `#bpp=2`) |
| symbol definitions | user-defined timing symbols (`symbol_definition` lines; the symbol's byte length must equal `#bpp`, and its beat position must not exceed the section length) |

### Chart section (double-column formats)

The chart is a series of **frames**: left, 4 text lines (one per panel row) of 4 panel symbols each (an empty marker or a timing symbol); right, a timing column `|…|` whose symbols give the position in beats. Timing symbols are the circled numbers `①`…`㊿` (50 symbols; in `#circlefree` mode `１`–`９`, `10`–`20`); jubeatools maps symbol index `i` (0-based) to beat `i/4` (`SYMBOL_TO_BEATS_TIME = 1/4 · i`), so `①` = beat 0, `②` = beat 1/4 … (`#memo`: each symbol = 1/4 beat; `#memo1`: each timing line = 1 beat, i.e. no sub-beat divisions). Long notes are drawn by writing a timing symbol on the head panel and an arrow (`>`, `<`, `V`/`v`/`∨`/`Ｖ`/`ⅴ`, `^`/`∧`, and full-width variants) on the panels towards the tail; the tail-end panel carries the end symbol [inference from `LONG_ARROWS` and `find_long_note_candidates`]. Characters like `一ー－─―━–‐-−` in the timing part count as "empty beat".

## Timing model

Frames/sections are measured in beats; `b` = beats per section (4 default); tempo `t` and offset `o` (ms). Each timing symbol maps to a beat fraction (`1/4` beat per symbol index for `#memo`). Absolute time = integral of tempo over the beats + `o`/1000. `#memo` is the original; `#memo1` forbids BPM changes within a bar. jubeatools notes that for decimal-length sections (not multiple of 1/4) the last frame's duration is mis-computed ("wrong for the last frame").

[observed in manifest samples jubeatools_MTC_Mimi_EXT.txt, jubeatools_MTC_Nageki_no_Ki_EXT.txt, jubeatools_RorataJin_example.txt, jubeatools_Booths_of_Fighters_memo.txt] Real files use CRLF; `#memo2` frames look like `□□①□　　　|①−−−|` (4 panel cells, then the timing column); community files declare their own timing symbols with `*01:0`, `*02:0.25`, `*a2:0.166667` lines (symbol name, beat position), set `#holdbyarrow=1`, put `//` comment headers (which may be in a non-Shift-JIS encoding such as EUC-KR) before `t=`/`m=`/`o=`, and a `#memo` file may separate its frames with `--------` lines.

## Notes

Taps = a symbol on a panel; long notes = symbol + arrow(s) + end symbol; up to 4×4 positions (pw/ph can enlarge the grid). No keysounds. Holds only straight.

## Audio & images

`m=` music path, `#jacket=` cover, `#prevpos=` preview start.

## Versions & variants

`#memo`/`#memo1`/`#memo2`/`#boogie`, **mono-column** (1列形式, headerless, no `#memo*` command; uses `--` separator lines), **youbeat/yubiosi v1.0/1.5/2.0**, **iboogie**. jubeatools implements all of them (module list `jubeat_analyser/…` and `formats/format_names.py`).

## Quirks & pitfalls

- Shift-JIS bytes: a panel symbol can be 1 or 2 bytes (`#bpp`); length is measured in shift-jis-2004 bytes, not characters.
- Symbols beyond 50 slots exist via custom definitions only.
- Long-note arrows are ambiguous when several notes surround a panel: jubeatools resolves candidates with a constraint solver (`find_long_note_candidates`).
- Offset/`o` and `r` semantics are historic.
- Files in the wild may mix dialects or have wrong commands.

## Example

From the memo-format minimal file in the jubeat analyser usage notes (yuisin.com):

```
t=1
o=1000
m=""
#memo1
```

(Only the metadata skeleton is documented in the sources opened; I did not open a full sample of the 4×4 drawing.)

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [Stepland/jubeatools](https://github.com/Stepland/jubeatools) (Python, loaders and dumpers for memo, memo1, memo2, mono-column, youbeat, boogie)
- jubeat analyser (Windows simulator), [narze/jubeat-memo-analyser](https://github.com/narze/jubeat-memo-analyser) (Ruby, search result), F.E.I.S (editor, memon)

## Getting samples

**Committed:** none (no source with a clear licence was found; see [`samples/SOURCES.md`](samples/SOURCES.md)). **Manifest:** four jubeatools test files (`#memo2`, two community "MTC" charts with custom symbols and non-Shift-JIS bytes, and a `#memo` single-column file), pinned to a jubeatools commit; the repository has no LICENSE.

**How to get more**: jubeat analyser charts are community-written `.txt` files; the jubeat analyser site (<https://yuisin.com/jubeat/analyser/jubeatmemo_use.html>, quoted in the README) documents the format, and F.E.I.S. / jubeatools can convert memon to the memo dialects (jubeatools writes `memo`, `memo1`, `memo2`, `mono-column`, `youbeat`, `boogie`). Community charts for the Windows simulator circulate on Japanese jubeat analyser sites and Korean communities (the MTC fixtures are by "Mintice", 2019) [inference from the fixtures]; their licence is rarely stated.

## Sources

- <https://raw.githubusercontent.com/Stepland/jubeatools/master/jubeatools/formats/jubeat_analyser/command.py>, `symbols.py`, `load_tools.py` (read)
- <https://yuisin.com/jubeat/analyser/jubeatmemo_use.html> (search snippet)
- <https://davidobot.net/2020/05/03/jubeat-pc> (search snippet)
