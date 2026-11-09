# jubeat analyser "memo" formats (`.txt`: `#memo`, `#memo1`, `#memo2`, `#boogie`, mono-column, youbeat)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text (Shift-JIS / shift-jis-2004, byte-level)

## Overview

jubeat analyser is a Japanese fan jubeat simulator. Its charts are hand-written text files ("memo") whose note area is a drawing of the 4×4 panel grid: panel states per frame, with a column for timing. jubeatools handles all dialects: `#memo` (youbeat-like, a bar division always means a 1/4 note), `#memo1` (youbeat-like, no BPM changes in the bar), `#memo2` (double-width), `#boogie` (youbeat-like), the headerless mono-column (1列形式) format, youbeat/yubiosi (v1.0, 1.5, 2.0) and "iboogie". Extension typically `.txt`. The yuisin.com usage notes show the minimal file: `t=1`, `o=1000`, `m=""`, `#memo1`.

Category: others. Grid positions, not lanes.

## Container & encoding

- Plain text, Shift-JIS(-2004). jubeat analyser works at byte level; jubeatools decodes with `shift-jis-2004` + `surrogateescape` for undecodable bytes.
- `//` starts a comment; empty lines are ignored.
- Mono-column files use `--` separator lines; double-column formats must not contain them.
- One file = one chart (difficulty in `#dif`), metadata included.

## Structure / metadata

Commands, one per line (jubeatools grammar: `#key[=value]` or `letter=value`, string values in double quotes, numbers may be negative decimals):

| Command | Meaning |
|---|---|
| `t=<decimal>` | tempo (BPM), may change between sections |
| `o=<int>` | offset in ms (100 by default; time between audio start and chart start) |
| `m="<path>"` | music file |
| `b=<decimal>` | beats per measure ("section"), 4 by default |
| `r=<int>` | "increase the offset?" in ms: unsupported in jubeatools, purpose unknown |
| `#memo`, `#memo1`, `#memo2`, `#boogie` | select dialect (a dialect command in the wrong parser raises "wrong format") |
| `#pw=<int>`, `#ph=<int>` | panels horizontally/vertically (4 by default) |
| `#lev=<int>` | chart level (1–10) |
| `#dif=<n>` | difficulty: 1 BSC, 2 ADV, 3 EXT |
| `#title="…"`, `#artist="…"`, `#jacket="<path>"`, `#prevpos=<int>` (preview start ms) | metadata |
| `#bpp` | bytes per panel symbol (default 2) |
| `#circlefree=<0 or 1>` | "circle-free" timing symbols (only with `#bpp=2`) |
| symbol definitions | user-defined timing symbols (`symbol_definition` lines; the symbol's byte length must equal `#bpp`, and its beat position must not exceed the section length) |

### Chart section (double-column formats)

The chart is a series of frames: on the left, 4 text lines (one per panel row) of 4 panel symbols each (empty marker or timing symbol); on the right, a timing column `|…|` giving the position in beats. Timing symbols are the circled numbers `①`…`㊿` (50 symbols; in `#circlefree` mode `１`–`９`, `10`–`20`). jubeatools maps symbol index `i` (0-based) to beat `i/4` (`SYMBOL_TO_BEATS_TIME = 1/4 · i`), so `①` = beat 0, `②` = beat 1/4 (`#memo`: each symbol = 1/4 beat; `#memo1`: each timing line = 1 beat, no sub-beat divisions). Long notes are drawn by writing a timing symbol on the head panel and an arrow (`>`, `<`, `V`/`v`/`∨`/`Ｖ`/`ⅴ`, `^`/`∧`, and full-width variants) on the panels towards the tail; the tail-end panel carries the end symbol [inference from `LONG_ARROWS` and `find_long_note_candidates`]. Characters like `一ー－─―━–‐-−` in the timing part count as "empty beat".

## Timing model

Frames/sections are measured in beats; `b` = beats per section (4 default); tempo `t` and offset `o` (ms). Each timing symbol maps to a beat fraction (1/4 beat per symbol index for `#memo`). Time = integral of tempo over beats + `o`/1000. `#memo1` forbids BPM changes within a bar. jubeatools notes that for decimal-length sections (not a multiple of 1/4) the last frame's duration is wrong.

[observed: jubeatools_MTC_Mimi_EXT.txt, jubeatools_MTC_Nageki_no_Ki_EXT.txt, jubeatools_RorataJin_example.txt, jubeatools_Booths_of_Fighters_memo.txt] Real files use CRLF; `#memo2` frames look like `□□①□　　　|①−−−|` (4 panel cells, then the timing column). Community files declare timing symbols with `*01:0`, `*02:0.25`, `*a2:0.166667` lines (symbol name, beat position), set `#holdbyarrow=1`, put `//` comment headers (possibly non-Shift-JIS, e.g. EUC-KR) before `t=`/`m=`/`o=`, and a `#memo` file may separate frames with `--------` lines.

## Notes

Tap = a symbol on a panel; long note = symbol + arrow(s) + end symbol, straight only. Up to 4×4 positions (`pw`/`ph` can enlarge the grid). No keysounds.

## Audio & images

`m=` music path, `#jacket=` cover, `#prevpos=` preview start.

## Versions & variants

`#memo`/`#memo1`/`#memo2`/`#boogie`, mono-column (headerless, `--` separators), youbeat/yubiosi v1.0/1.5/2.0, iboogie. jubeatools implements all (`jubeat_analyser/...`, `formats/format_names.py`).

## Quirks & pitfalls

- A panel symbol is 1 or 2 bytes (`#bpp`), measured in shift-jis-2004 bytes.
- Symbols beyond 50 exist only via custom definitions.
- Long-note arrows are ambiguous when several notes surround a panel; jubeatools resolves candidates with a constraint solver (`find_long_note_candidates`).
- `o` and `r` semantics are historic.
- Files in the wild may mix dialects or have wrong commands.

## Example

Minimal file from the jubeat analyser usage notes (yuisin.com); no full 4×4 drawing was opened:

```
t=1
o=1000
m=""
#memo1
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [Stepland/jubeatools](https://github.com/Stepland/jubeatools) (Python, loaders and dumpers for memo, memo1, memo2, mono-column, youbeat, boogie)
- jubeat analyser (Windows simulator), [narze/jubeat-memo-analyser](https://github.com/narze/jubeat-memo-analyser) (Ruby, search result), F.E.I.S (editor, memon)

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: the jubeat analyser site (<https://yuisin.com/jubeat/analyser/jubeatmemo_use.html>, needs a browser User-Agent) documents the format; jubeatools writes the memo dialects from memon; community charts circulate on Japanese/Korean fan sites (licence rarely stated) [inference].

## Sources

- <https://raw.githubusercontent.com/Stepland/jubeatools/master/jubeatools/formats/jubeat_analyser/command.py>, `symbols.py`, `load_tools.py` (read)
- <https://yuisin.com/jubeat/analyser/jubeatmemo_use.html> (search snippet)
- <https://davidobot.net/2020/05/03/jubeat-pc> (search snippet)
