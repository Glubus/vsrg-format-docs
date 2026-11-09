# StepMania course file (`.crs`)
Kind: metadata

Doc status: complete · ROX: no · Category: vsrg · Encoding: text

## Overview

A `.crs` file is a **course**: an ordered playlist of song entries ("play these N songs back to back, at this difficulty, with these modifiers"). It contains no notes and no timing; every entry points at songs/charts that already exist in the player's song library. It is the StepMania/ITG/OpenITG/OutFox/NotITG equivalent of the arcade games' Nonstop, Oni, Endless and Survival modes (DDR "Challenge"/"Nonstop", ITG "Marathon"). StepMania loads courses from `Courses/<Group>/*.crs` (and `Courses/*.crs`), and per-profile *edit courses* from `<profile>/EditCourses/*.crs` (at most 20 per profile, each at most 32 KB). The format shares its tokenizer (MSD: `#TAG:param:param;`) with [`.sm`](../sm/README.md) and [`.ssc`](../ssc/README.md). Etterna dropped it ("legacy course formats aren't supported anymore, see playlists", `Docs/legacy/CourseFormat.txt` in the Etterna repo). The authoritative documentation is `Docs/CourseFormat.txt` of the StepMania repository plus `CourseLoaderCRS.cpp`/`CourseWriterCRS.cpp`.

## Packaged in

- Packaged in [`smzip`](../smzip/).

## Container & encoding

- Plain text, MSD syntax: `#NAME:value1:value2:...;` Whitespace/newlines between tags are free. `//` starts a comment to end of line.
- The loader reads the buffer with **unescape disabled** (`msd.ReadFromString(buffer, false)` / `msd.ReadFile(path, false)`), unlike `.sm` where `\:` and `\;` are unescaped. [inference: for `.crs` only `#SONGSELECT` documents its own `\,` `\#` `\;` `\=` `\:` escaping, see below; the MSD layer leaves them in place.]
- Charset: the same as StepMania text files (UTF-8 in StepMania 5; legacy files may be CP1252/Shift-JIS and are handled by the file layer, not by the course parser). [inference]
- One file = one course. `Courses/<Group>/<name>.crs`; the parent directory name becomes the course's group name (`m_sGroupName`, taken from the second last path component when the path has at least 4 parts).
- **Cache**: StepMania also writes a cache copy of each course (under `Cache/`, sub-directory `Courses`, via `SongCacheIndex::GetCacheFilePath("Courses", path)`) that contains extra `#RADAR:` tags and `// cache tags:` comments (see below). Treat these as runtime artefacts, not as authored data.

## Structure / metadata

### Header tags (course-wide)

| Tag | Params | Meaning (from `CourseLoaderCRS::LoadFromMsd` / `CourseFormat.txt`) |
|---|---|---|
| `#COURSE` | title | Main title. |
| `#COURSETRANSLIT` | title | Transliterated title. |
| `#SCRIPTER` | text | Author/credit. |
| `#DESCRIPTION` | text | Free description. |
| `#REPEAT` | `YES` | Endless course. True when the lower-cased value contains `yes`. |
| `#BANNER` | path | Banner image. If absent, the loader looks for `<course file name without ext>*.png/jpg/jpeg/bmp/gif` next to the file and takes the first match. |
| `#BACKGROUND` | path | Background image (StepMania 5 / sm-ssc only). |
| `#LIVES` | n | Life count, `max(n, 0)`. Any positive value turns the course into an **Oni** course (documented: "automatically force your course into an Oni course"). |
| `#STYLE` | `SINGLE,VERSUS,...` | Comma separated list of styles the course may be played in (used to clone courses for singles/doubles). Stored as a set of style names. |
| `#METER` | `Difficulty:n` (or just `n`) | Custom displayed meter for a course difficulty. Difficulty names: `Beginner`, `Easy`, `Regular` (= Medium), `Difficult` (= Hard), `Challenge`, `Edit` in files **written** by StepMania (`g_CRSDifficultyNames`); the loader matches those names case-insensitively against the `Difficulty` enum order. With one param only (`#METER:7;`) the value is applied to Medium (legacy compatibility). An unknown name is logged and skipped. |
| `#DISPLAYCOURSE`, `#COMBO`, `#COMBOMODE` | | Accepted and **ignored**. |
| `#RADAR` | `stepstype:coursedifficulty:v,v,...` | **Cache files only** (`bFromCache`): radar values per trail, `%.3f` each, one per radar category. Not for authoring. |

### Entry tags (position matters)

Entries are built in file order. Two "pending" values are carried to the **next** entry tag and then cleared/consumed:

| Tag | Params | Meaning |
|---|---|---|
| `#MODS` | `TIME=t:LEN=l:MODS=mods` ... | Timed modifier ("attack") block attached to the **next** `#SONG`/`#SONGSELECT`. Per attack the parser reads sub-params of the form `KEY=value` in order: `TIME` (start second, min 0), `LEN` (seconds) or `END` (end second; `LEN` = `END - TIME`), then `MODS` finalises one attack. Several attacks can be chained in one tag (`:`-separated) or the tag repeated. A non-positive length is logged and clamped to 0. |
| `#GAINSECONDS` | seconds | Seconds gained before the next `#SONG` (Survival). Applied to the next `#SONG` entry only; mutually exclusive with `#LIVES` per `CourseFormat.txt`. (`#SONGSELECT` has its own `GAINSECONDS=` key instead.) |
| `#SONG` | `songspec:difficulty:mods` | One course entry (below). |
| `#SONGSELECT` | `KEY=value:KEY=value...` | StepMania 5.1 keyed alternative to `#SONG` (below). |

### `#SONG:songspec:difficulty:mods;`

`songspec` (first param):

| Value | Meaning |
|---|---|
| `BEST<n>` / `WORST<n>` | n-th most / least played song on the machine (index `n-1`, clamped 0..500; ignored with a warning if `n` exceeds the number of installed songs). |
| `GRADEBEST<n>` / `GRADEWORST<n>` | n-th top / lowest-graded song. |
| `*` | Completely random song. |
| `<Group>/*` | Random song within a group (`\` is normalised to `/`; group must exist or the entry is dropped and the course flagged incomplete). |
| `<Group>/<Song folder>` | Exact song directory. |
| `<Song>` | Song looked up by title/folder name (`FindSong("", name)`); if not found the entry is skipped and the course marked incomplete. |

`difficulty` (second param): first tried as an "old style" name (case-insensitive: `beginner`; `easy`/`basic`/`light` = Easy; `medium`/`another`/`trick`/`standard`/`difficult` = Medium; `hard`/`ssr`/`maniac`/`heavy` = Hard; `smaniac`/`challenge`/`expert`/`oni` = Challenge; `edit` = Edit), then as a StepMania 5 `Difficulty` name; otherwise as a meter range `low..high` (`%d..%d`; a single number `n` means `n..n`; invalid text falls back to `3..6`; low is clamped to at least 1, high to at least low).

`mods` (third param, comma separated): `showcourse` (never hide the entry), `noshowcourse` (hide: secret entry), `nodifficult` (player may not change difficulty), `award<n>` (lives gained on completion in Oni mode); everything else is kept as the entry's player-option string (`2x`, `C150`, `Overhead`, ...).

### `#SONGSELECT:KEY=value:KEY=value...;`

Keys (order and combination free; with no selector keys a random song+difficulty is chosen): `TITLE`, `GROUP`, `ARTIST`, `GENRE` (comma lists, exact match; control chars `#` `;` `=` `:` `,` escaped with `\`), `DIFFICULTY` (comma list), `METER` (`min-max`, inclusive), `BPMRANGE` (`min-max` against the displayed BPM), `DURATION` (`min-max` seconds; uses `#MUSICLENGTH` if present), `SORT` (`<sort>,<n>`; sort = `MostPlays|FewestPlays|TopGrades|LowestGrades` or old `Best|Worst|GradeBest|GradeWorst`, n in 1..500), `MODS` (list; `showcourse`/`noshowcourse`/`nodifficult` are extracted, the rest are player options; does **not** replace timed `#MODS`), `GAINSECONDS`, `GAINLIVES`. If the criteria match no song the entry is skipped.

## Timing model

Not applicable: the file has no chart timing. The only time values are **seconds** inside `#MODS` (`TIME`/`LEN`/`END`) and `#GAINSECONDS`, measured from the start of the song entry they are attached to.

## Notes

Not applicable (no note data). Course trails are assembled at runtime from the referenced songs' charts, with `Difficulty`/meter filters applied to each song's chart list.

## Audio & images

Only `#BANNER` and `#BACKGROUND` (paths relative to the course file or the StepMania data dirs). Audio comes from the songs.

## Versions & variants

- StepMania 3.9/4.0: `#COURSE`, `#REPEAT`, `#LIVES`, `#SONG`, `#MODS`, `#BANNER`, old-style difficulty names (`Another`, `Maniac`, `SManiac`, `Oni`...).
- sm-ssc / StepMania 5: adds `#BACKGROUND`, `#STYLE`, `#METER:<difficulty>:n`, `#SCRIPTER`, `#DESCRIPTION`, full `Difficulty` names, `award<n>`.
- StepMania 5.1 (`5_1-new` branch): adds `#SONGSELECT` and its keys. Older builds report it as an unknown tag.
- Etterna: `.crs` no longer supported (playlists in its own format instead).
- Engine-specific hacks: `extra1.crs`/`extra2.crs` in a group (or in `Songs/`) are used by the "extra stage" logic (`SongManager`).

## Quirks & pitfalls

- Order dependence: `#MODS` and `#GAINSECONDS` bind to the *following* entry; a trailing `#MODS` with no entry after it is lost.
- `#SONG` has fixed positional params (songspec, difficulty, mods); a missing third param is read as empty.
- Difficulty names are not symmetrical: written files use `Regular`/`Difficult`, while old-style parsing maps `difficult` to **Medium**.
- Song resolution depends on the installed library; an unresolved song silently marks the course incomplete rather than failing.
- The `DISPLAYCOURSE/COMBO/COMBOMODE` branch condition in the 5_1 loader is written with `!EqualsNoCase(...) || ...` (always true), so every unrecognised tag is silently ignored there. [inference from `CourseLoaderCRS.cpp` 5_1-new]
- Edit courses over 32 KB are refused; more than 20 per profile are ignored.

## Example

From the StepMania repository (`Docs/CourseFormat.txt`, final example):

```
#COURSE:My Awesome Course - The Revenge;
#METER:Medium:8;

#MODS:
	TIME:1.00:END:50.00:MODS:C150;
#SONGSELECT:GROUP=Stepmania 5:MODS=Overhead;
#SONGSELECT:ARTIST=Kommisar:MODS=2x;
#SONGSELECT:GROUP=In The Groove:TITLE=Mouth;
#SONGSELECT:BPMRANGE=110-160:DIFFICULTY=Medium;
```

Illustrative, hand-built from the rules above (classic `#SONG` form):

```
#COURSE:Survival;
#LIVES:4;
#SONG:BEST1:Medium:2x;
#SONG:My Pack/*:5..7:noshowcourse;
```

## ROX support

Not read by ROX (no chart data; ROX 0.8.1 models charts, not playlists).

## Parsers & tools

- StepMania (C++): [`CourseLoaderCRS.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/CourseLoaderCRS.cpp), [`CourseWriterCRS.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/CourseWriterCRS.cpp), [`Course.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/Course.cpp). ITGmania/OutFox/OpenITG share the code lineage.
- `CourseUtil.cpp` saves edit courses to `<machine profile>/EditCourses/<name>.crs` (the in-game course editor path).

## Sources

- https://github.com/stepmania/stepmania/blob/5_1-new/Docs/CourseFormat.txt
- https://github.com/stepmania/stepmania/blob/5_1-new/src/CourseLoaderCRS.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/CourseWriterCRS.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/Difficulty.cpp (`OldStyleStringToDifficulty` map)
- https://github.com/stepmania/stepmania/blob/5_1-new/src/SongManager.cpp (`Courses/` scan, `EditCourses/` (`Profile.cpp`), `MAX_EDIT_COURSES_PER_PROFILE = 20` in `SongManager.h`)
- https://raw.githubusercontent.com/etternagame/etterna/develop/Docs/legacy/CourseFormat.txt
