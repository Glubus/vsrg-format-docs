# pydance step file (`.dance`)
Kind: chart

Doc status: complete · ROX: no · Category: vsrg · Encoding: text (UTF-8, no BOM)

## Overview

`.dance` is the native step-file format of the open-source dance game pydance. Its goals, from the spec: "easy parsability, easy human readability, brevity, and disambiguity". One `.dance` file holds the song metadata, optional description and lyrics, and **any number of step sections** (one per game mode x difficulty). It is line-oriented (not MSD), has explicit note-length letters instead of implicit slots, and uses explicit commands for BPM changes and stops. Spec: `dance-spec.txt` (version 1.2, 2004-03-01, shipped with pydance 1.0, mirrored in StepMania's `Docs/SimfileFormats/`); implementation: `DanceFile` in pydance's `fileparsers.py`. StepMania does **not** read `.dance`; it only keeps the document.

## Container & encoding

- One file per song, named anything with extension `.dance`; the audio, banner, background, cd title are separate files **named explicitly** in the metadata ("songs in this format will NOT have any files autodetected"). Place the `.dance` and its `.ogg` in the same folder.
- "All text is encoded in UTF-8. Byte-order marking is not allowed." Strings and file names are case-sensitive; the directory separator is `/` on every platform. Newlines `\n`, `\r\n` or `\r`.
- Line oriented: `#` as the first character of a (stripped) line is a comment; blank lines ignored; the keyword `end` on a line ends the current section.
- Designed to be parsed by a table-driven DFA ("as in pydance's fileparsers.py"): states `WAITING, METADATA, DESCRIPTION, LYRICS, BACKGROUND, GAMETYPE, STEPS`.

## Structure / metadata

File grammar (EBNF from the spec, simplified): `File ::= Metadata [TextSection+] StepSection+`.

### Metadata section (first; ends with `end`)

Lines of `key value...` (value is the rest of the line, internal spaces kept). Mandatory: `filename`, `title`, `artist`, `bpm`.

| Key | Value | Meaning / default |
|---|---|---|
| `filename` | audio path | audio file to play |
| `title` | text | name of the song (without "Foo Mix") |
| `subtitle` | text | "Foo Mix", "Crazy Version"; default none |
| `artist` | text | artists and remixers |
| `mix` | text | mix/game of origin (default "No Mix" in pydance) |
| `bpm` | float | starting BPM |
| `bpmdisplay` | floats separated by spaces, or `*` | values cycled in the song selector; `*` = constantly changing |
| `gap` | integer ms | "The millisecond offset into the song at which the arrows should start. If the first beat is 0.3 seconds into the song, for example, this should be -300"; may be negative; default 0 |
| `startat`, `endat` | seconds | start/end the music at these positions; `gap` and steps are relative to `startat`; defaults 0.0 and song length |
| `background` | image path | in-song background; default none |
| `banner` | image path | song-select banner |
| `cdtitle` | image path | 64x40 CD title, relative to a special cd-title directory or the file's directory |
| `preview` | `start length` (two floats, seconds) | song-select preview; defaults 45.0 and 10.0 |
| `md5sum` | hex | checksum of the audio; warn on mismatch |
| `author` | text | file author; default none |
| `revision` | `YYYY.MM.DD` | last revision date; default `1970.01.01` |
| `movie` | path | background movie; default none |
| `valid` | `1` / `0` | if 0, excluded from random play (unfinished/untimed); default 1 |

### Text sections

- `DESCRIPTION ... end`: lines starting with a space, DPKG-style; whitespace/newlines folded; a line holding a single `.` (preceded by a space) is a paragraph separator.
- `LYRICS ... end`: each line `<float time> <int channel> <text>` (time in seconds into the song, irrespective of `gap`; same-channel lyrics overwrite each other).
- A `BACKGROUND` section token exists in the implementation (parsed and skipped: "We don't actually parse the background change data yet"); the spec changelog mentions a "(currently unexplained) BACKGROUNDS section".

### Step sections

A step section begins when an unknown section token is read. Lines:

```
<GameMode>                 e.g. SINGLE
<Difficulty> <PosInt>      e.g. BASIC 0   (difficulty name and numeric rating)
<sequence lines...>
end
```

Standard game modes: `SINGLE`, `VERSUS` (two players, same steps), `COUPLE` (two players, different steps), `DOUBLE` (one player on two pads), `5PANEL`, `5VERSUS`, `5COUPLE`, `5DOUBLE`, `6PANEL` (UL, UR, U, D, L, R), `6VERSUS`, `6COUPLE`, `6DOUBLE`, `8PANEL` etc. (all directions except centre), `9PANEL` etc. (all directions including centre, added 2004.03.01), `3PANEL` etc. (UL, D, UR). A `SINGLE` without a `VERSUS` section is used for versus mode.

## Timing model

- `bpm` at the start; `B <float>` changes the BPM at that point. Time passes only through note lines, `W`, `S` and `D`.
- **Note-length letters** set how long the line lasts. The base `q` = the quarter note = **one beat**:

| Letter | Note | Beats | pydance internal value (`DanceFile.BEATS`, 4 per beat) |
|---|---|---|---|
| `o` | whole | 4 | 16 |
| `h` | 1/2 | 2 | 8 |
| `q` | 1/4 | 1 | 4 |
| `e` | 1/8 | 1/2 | 2 |
| `w` | 1/12 | 1/3 | 4/3 |
| `s` | 1/16 | 1/4 | 1 |
| `f` | 1/24 | 1/6 | 2/3 |
| `t` | 1/32 | 1/8 | 1/2 |
| `u` | 1/48 | 1/12 | 1/3 |
| `x` | 1/64 | 1/16 | 1/4 |
| `n` | 1/192 | 1/48 | 1/12 |

  (`x` 64th and the 1/192 `n` were added in spec 1.1, 2003-06-03, with `u` the 48th). Beat = cumulative sum of these durations; the line **plays at the position before** its own duration is added [inference from the "wait/step" semantics: the line's note comes first, then the time advances; the spec says "the 'base' is q, the quarter note, which represents one beat"].
- **Commands** (uppercase single letters): `B <Float>` change BPM; `R` "Ready? Go!" graphics/sound; `W <Float>` wait this many seconds before the next event (audio time passes, notes do not); `S <Float>` stop scrolling for this many seconds before the next event; `D <Float>` the same as a sequence of 0-note strings for this many beats; `L <PosInt> <LongString>` display lyrics at this point (the EBNF writes `L <Float> <PosInt> <LongString>`, the command list and the implementation use `L <channel> <text>`: an inconsistency in the spec).
- `gap` positions beat 0 in the audio; with `startat` the audio is trimmed first and gap/steps are relative to `startat`.
- Conversion of a position to time: integrate beats at the current BPM, add `S`/`W` seconds, add `gap/1000`.

## Notes

A note line: `<letter> <buttons> [<buttons> ...]`, e.g. `q 1010` (4-character button string in SINGLE) or `e 1000 0010` for COUPLE (one button string per player, separated by whitespace). "All these strings should be the same length across game modes" (length = panel count).

Button characters (spec): 

| Char | Meaning |
|---|---|
| `0` | no button |
| `1` | regular press |
| `3` | "must be pressed here and held down until a 1 is encountered" (hold start; the hold ends at the next `1` in that column... "until a 1 is encounted") |
| `5` | secret step |
| `7` | secret step and hold |

(bit view in the spec: `num & 1` pressed, `num & 2` hold, `num & 4` secret; "not necessarily guaranteed for future additions").

Game-mode button order: for `SINGLE` the four characters are L, D, U, R (inferred from the example `q 1010`, `q 0101`; the spec does not list the order) [inference]; the other modes follow the panel orders given in the Standard Game Modes list.

Unknown note types are treated as `0` ("treat unknown note types as 0s, and hope for the best"); unknown sections/metadata keys are skipped to the next `end`.

## Audio & images

Audio: `filename` (+ optional `startat/endat`, `md5sum`). Images: `background`, `banner`, `cdtitle`; `movie` for a background video. Everything must be explicit paths (case-sensitive). No keysounds.

## Versions & variants

Spec versions: 1.0 (2003-06-01: "No more I command"), 1.1 (2003-06-03: 192nd `n`, 48th `u`), 1.2 (2004-03-01 with pydance 1.0: 9-panel mode); intermediate changes: 2003-06-26 BACKGROUNDS section note, 2003-06-27 EBNF for COUPLE-style modes, 2003-07-30 gap example, 2003-08-15 note types and VERSUS mode, 2003-12-22 `cdtitle`, 2003-12-23 3-panel modes and `bpmdisplay`. The earlier pyDDR **`.step`** format is the format this one generalizes ("The dance format is basically the step format, but generalized, smaller, and more readable. A script to convert .step files to .dance files is forthcoming") and is documented only as a stub in [legacy-dance-formats/step](../../legacy-dance-formats/step/README.md).

## Quirks & pitfalls

- Holds are `3 ... 1`, so a lone `3` is a hold start with no explicit tail character; a parser must close it when it sees the next `1`/`3` in the column [semantics from the spec text, not verified in the engine].
- `gap` is a signed millisecond offset with the same orientation as StepMania `#OFFSET` expressed in ms (first beat at 0.3 s => `gap -300`) [inference]; it is the opposite sign of DWI `#GAP`.
- Lyrics ignore `gap`.
- There is no per-chart BPM: BPM changes are part of the step stream of each section.
- `L` argument order inconsistency (above).
- The format defines "secret" notes (`5`, `7`) that no other format has.

## Example

Verbatim example from the spec (`dance-spec.txt`):

```
filename asong.ogg
title A Song
subtitle Crazy Mix
artist Someone
# This is a comment
end
DESCRIPTION
 This is an example song.
 It's pretty uninteresting.
end
SINGLE
BASIC 0
q 1010
# This is another comment.
q 0101
q 3030
q 1010
end
```

## ROX support

Not read by ROX. A decoder would need: beat accumulation from letters, `B/S/W/D` commands, `gap` baked into times, game-mode -> key count (3/4/5/6/8/9 and doubles), and a hold rule for `3`.

## Parsers & tools

- pydance `fileparsers.py` ([DanceFile](https://github.com/mbenkmann/pydance/blob/master/fileparsers.py), Python 2); the reference implementation also contains `MSDFile`, `DWIFile`, `SMFile`, `KSFFile`.
- Text Text Revolution (ncurses clone) reads the earlier `.step`.

## Sources

- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/dance-spec.txt (also at http://kai.vm.bytemark.co.uk/svn/pydance/trunk/pydance/docs/dance-spec.txt per misc.txt)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt
- https://github.com/mbenkmann/pydance (fileparsers.py, docs/, README)
- https://icculus.org/pyddr/manual.php, https://icculus.org/pyddr/faq.php
- https://ttr.sourceforge.net/
