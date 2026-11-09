# simai / `maidata.txt` ("simai language")
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text (UTF-8 in modern tools; original Flash tool: text with escape rules)

## Overview

**simai** (simulator of maimai) is a Flash chart simulator by **Celeca**, released 2013-02-05 and shut down 2023-02-05. Its chart notation, the **"simai language"** (simai語, defined by Celeca in 2013), is a compact text notation for every maimai note and is now the *de-facto* interchange format of the maimai custom-chart scene. It lives in a text file named **`maidata.txt`** (one song, up to 7 difficulties) next to `track.mp3`/`bg.png`/`pv.mp4`. Successor tools: **2simai/3simai**, **MajdataEdit / MajdataPlay** (editor + player), many converters. The specification of the notation was moved to wiki pages *simai語の譜面書式* / *Notations of simai* when simai closed; the rights to the language are held by Celeca. The notation is inspired by D4U's CIRRING-S/CarmBeat maker notation, shared by the owatatsujin `data.txt` too (see the Taiko TJA docs).

## Container & encoding

- `maidata.txt`: a text file of `&key=value` fields. A field starts with `&` at the beginning of a line; a value runs until the next field and may span many lines (chart bodies do). If a field appears twice the first wins (maidata-parser).
- Charset: modern tools read UTF-8. The Flash original required escaping characters that break Flash variables: `&` → `\＆`, `+` → `\＋`, `%` → `\％`, `\` → `\￥` (first char ASCII backslash, second full-width).
- Comments: `||` to end of line (maidata-rs list); newlines/spaces/tabs inside a chart body are skipped.
- A chart body ends at the next field or at a standalone `E`.
- Related: `track.mp3`, `bg.jpg/png`, `pv.mp4` (MajdataEdit convention [not opened]).

## Structure / metadata

Fields (3simai variable list):

| Field | Meaning |
|---|---|
| `&title=` | song title; `┃` splits main/sub title (right side drawn smaller); a title of the form `[X]Name` marks a utage chart (maidata-parser) |
| `&artist=` | artist |
| `&smsg=` | SINGLE MESSAGE (up to 3 lines using `┓` as line break) |
| `&des=` | notes designer (also per difficulty `&des_N=`) |
| `&first=` | seconds from audio start to the chart start; per-difficulty `&first_N=` override |
| `&lv_1=` … `&lv_7=` | level text per difficulty (`13+`, or `※X` = custom single char) |
| `&inote_1=` … `&inote_7=` | chart bodies: 1 EASY, 2 BASIC, 3 ADVANCED, 4 EXPERT, 5 MASTER, 6 Re:MASTER, 7 ORIGINAL |
| `&amsg_first=`, `&amsg_time=`, `&amsg_content=` | ACTIVE MESSAGE timeline (timing like a chart body) |
| `&answer=` (alias `&clock_count=`), `&des=` | count-in clicks (default 4), designer (global or per chart `&answer_5=4`, not both) — maidata-parser |
| `###` markers | two `###` in a chart mark the preview window (maidata-parser) |

Difficulty mapping to `.ma2` in maidata-parser: `inote_2..7` → `000000_00 … 000000_05`; `inote_1` has no slot.

## Timing model

A chart body is a sequence of **comma-terminated slots**; each comma advances time by the current "note length". Notes are written before the comma that places them; an empty slot is a rest.

- `(174)` sets BPM; `{16}` sets the comma length to a 16th note at the current BPM; `{#0.35}` fixes each comma at 0.35 s. BPM must be set before the divisor. Both may change anywhere in the chart and take decimals.
- Comma duration = `60/bpm · 4/n` s for `{n}`.
- `first` sets where the first slot starts in the audio.
- `E` ends the chart (the last comma still has duration).
- Durations of holds and slides use a bracket `[n:m]` = `m` notes of length 1/`n` (at the active BPM), or absolute forms: `[#s]` (seconds), `[bpm#n:m]` (alternate BPM), slides: `[wait##dur]` forms (see below).
- A special "pseudo-each" separator `` ` `` offsets the following note by 0.001 s (`1`2,` = note 2 is 0.001 s after note 1, not counted as EACH).

## Notes

Buttons are numbered 1–8 clockwise from 1 o'clock. Slots can contain several notes separated by `/` (EACH/BOTH, any number in 3simai; for plain taps a short form `12` or `38` is allowed).

| Notation | Meaning |
|---|---|
| `1,` | TAP at button 1; `1b,` BREAK TAP; `1x,` EX TAP; `1bx,` EX BREAK (letters `b`,`x`,`$`,`@` in any order) |
| `5h[2:1],` | HOLD on 5, length one half note; `5hb[..]` BREAK HOLD, `5hx[..]` EX HOLD; `4h[#5.678]`; `4h[150#2:1]` |
| `3h,` | HOLD without duration = pseudo-TAP (internally `[1280:1]`) |
| `1-4[8:3],` | SLIDE from 1 to 4, straight, 3 eighth notes; `b` after `]` makes it a BREAK slide |
| `1$,` / `1$$,` | star-shaped TAP / rotating star; `1@-5[8:1],` turns the automatic star of a slide into a normal tap |
| `1?-5[2:1],` / `1!-5[2:1],` | slide without star: `?` keeps the fade-in of the moving star, `!` drops it |
| `B1,` `D4,` `C,` | TOUCH on sensor (A–E + 1–8; `C` centre, `C1`/`C2` ≡ `C`); `B7f,` adds the fireworks effect; `Ch[4:3],` TOUCH HOLD (`Chf`/`Cfh` both ok) |
| `1/8h[2:1],` | EACH of a TAP and a HOLD |

Slide shapes (written between start and end button): `-` straight, `<` `>` `^` along the ring (counter-/clockwise, `^` when the distance < half), `v` V via centre, `p` `q` arcs around the centre, `s` `z` lightning (zigzag), `pp` `qq` big arcs (diameter centre-to-ring), `V` big V via a pass-through button (`1V35` = 1→3→5), `w` fan (one start, three ends). Constraints between start and end buttons are tabulated on the original wiki (image `slides.png`).

- **Same-start slides**: `1-4[4:3]*-6[8:5],` (one star, several tracks, each with its own speed → EACH).
- **Connected slides**: `1-4q7-2[1:2],` one star over several segments with one duration; per-segment durations `1-4[2:1]q7[2:1]-2[1:1],` (must be given for all segments).
- **Slide timing**: the star waits one beat of the current BPM, then travels; explicit: `[160#8:3]` (wait = one beat at BPM 160, travel = 3 eighths), `[160#2]` (wait at BPM 160, then 2 s), `[3##1.5]` (3 s wait, 1.5 s travel), `[3##8:3]`, `[3##160#8:3]`.
- Break/EX apply to the whole connected slide (a `b` after the last `]` only).

## Audio & images

Audio is not referenced by the data file (`track.mp3` convention); `&first=` positions the chart. ACTIVE MESSAGE texts are separate timeline fields.

## Versions & variants

`2simai` (up to EXpand) used a smaller variable set ("maidata.txtのひな形 (2simai EXまで)"); `3simai` adds the 7 difficulties, DX notes (TOUCH, TOUCH HOLD, fireworks, connected slides, `x` EX, `$`/`@` star control, `?`/`!`). MajdataEdit/MajdataPlay and `maidata-parser` extend or validate it (utage `[X]` titles, `###` preview markers, answer count, sensor-conflict validation). PRiSM PLUS (2026-03-24 note on the wiki) added touch holds on sensors other than C.

## Quirks & pitfalls

- Commas define time; forgetting one shifts everything. BPM `(..)` before divisor `{..}`.
- EXTREMELY dependent on the order of EACH/`/` elements for z-order of slides (earlier = in front).
- Slide start star always appears unless `?`/`!`.
- `h` without length equals `[1280:1]`.
- `C1`/`C2` are accepted as `C`.
- Tools differ on unsupported DX features (maidata-rs: star modifiers, DX parts not implemented).
- Escapes (`\＆` …) apply to titles/messages, not to chart bodies.
- Converting to `.ma2` needs a chosen RESOLUTION: maidata-parser chooses the smallest multiple of the chart's timing grid ≥ 384 (up to 1920) and warns when rounding.

## Example

From the simai wiki (maidata.txt variable page), a minimal chart (as written there):

```
&inote_1=
(120){4}
1,2,3,4,
5b,6b,7-4[8:1],,

{1}
,
E
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

- [xen0n/maidata-rs](https://github.com/xen0n/maidata-rs) (Rust, WIP)
- [lcebot/maidata-parser](https://github.com/lcebot/maidata-parser) (simai → ma2, binaries only), [lcebot/ma2-parser](https://github.com/lcebot/ma2-parser) (ma2 → simai)
- [donmai-me/MaiConverter](https://github.com/donmai-me/MaiConverter) (Python, Lark grammar)
- [Neskol/MaiLib](https://github.com/Neskol/MaiLib) / [MaichartConverter](https://github.com/Neskol/MaichartConverter) (C#)
- MajdataEdit / MajdataPlay (editor/player), sinmai-mods MoreChartFormats (loads simai and sdt in-game)

## Getting samples

**Committed** ([`samples/`](samples/SOURCES.md)): `synthetic-maidata.txt` (parsed by MaiConverter) and `synthetic-maidata-3simai-extras.txt` (connected slides and absolute durations, not accepted by MaiConverter, written from the wiki). **Manifest:** five `maidata.txt` files from the CC0 `MaichartConverterUnitTest` repo (converted official charts or excerpts; `[SD]` and `[DX]`, hundreds of BPM changes, touch notes).

**How to get more**: the simai wiki (<https://w.atwiki.jp/simai/>) documents the language; MajdataEdit / MajdataPlay (<https://github.com/LingFeng-bbben/MajdataEdit>, GPL-3) edit and play `maidata.txt` (their repositories contain no chart); MaichartConverter writes `maidata.txt` from `.ma2` (it is how the manifest files were made); the community shares charts as folders (`maidata.txt`, `track.mp3`, `bg.*`, `pv.mp4`) with copyrighted audio.

## Sources

- <https://w.atwiki.jp/simai/pages/1002.html> (simai語の譜面書式, read in full)
- <https://w.atwiki.jp/simai/pages/510.html> (variables, read) and pages 18, 25, 1003 (listed)
- <https://github.com/xen0n/maidata-rs> README.en.md, <https://github.com/lcebot/maidata-parser> README (read)
- <https://iepiweidieng.github.io/TJAPlayer3/tja> (owatatsujin / simai relationship)
