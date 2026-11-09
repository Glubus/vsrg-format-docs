# StepMania simfile (`.sm`)
Kind: chart

Doc status: complete · ROX: reads/writes · Category: vsrg · Encoding: text

## Overview

`.sm` is the main simfile format of StepMania 3.x, 4.x and 5.x, of In The Groove / OpenITG / NotITG, Etterna, ITGmania and Project OutFox (which all load it), and the de-facto interchange format of dance-game charts (Dance Dance Revolution, In The Groove, Pump It Up, Pump Pro, 7-key keyboard charts, ...). It is an MSD-family text file (`#TAG:value;`): the grand-daddy `.msd` format, then `.dwi`, then `.sm`. One `.sm` file holds the song metadata, the song-wide timing, and **every chart** of the song (all difficulties and all step types) as separate `#NOTES` tags. The audio, banner, background, etc. are separate files next to it. In StepMania 5 it is superseded by [`.ssc`](../ssc/README.md) (per-chart timing, more timing tags), but `.sm` is still read everywhere and is still what most packs ship. Samples: [`samples/`](samples/) (10 real files, CRLF line ends).

Related: [StepMania family overview](../README.md), [`.edit`](../edit/README.md), `.dwi` ([../../dwi/dwi](../../dwi/dwi/README.md)), `.msd` ([../../ddr/msd](../../ddr/msd/README.md)).

## Packaged in

- Packaged in [`smzip`](../smzip/).

## Container & encoding

- Plain text; one file per song (all charts inside). The extension is `.sm`. StepMania loads a song folder with the `.ssc` loader first and falls back to the `.sm` loader when there is no `.ssc` (`Song.cpp`: "Try SSCLoader ... No dice? Try SMLoader"), so a folder holding both uses the `.ssc`.
- Charset: StepMania treats the bytes as UTF-8 text (old files in the wild may use other code pages; no declaration exists). ROX requires valid UTF-8 for `.sm` and fails otherwise ([ROX source: src/formats/sm/parser.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/parser.rs) reads `from_utf8`). Line ends are CRLF or LF; both work.
- Tokenizer (shared by all MSD-family formats, `MsdFile::ReadBuf`):
  - `#` starts a value; the first token up to `:` is the tag name (case-insensitive: StepMania upper-cases it), the following `:`-separated tokens are parameters, `;` ends the value.
  - `//` starts a comment up to end of line (also inside a value).
  - `\` escapes the next character when the file is read with "unescape" (`.sm`, `.ssc`, `.edit` are; `.dwi`, `.ksf` are not): `\;`, `\:`, `\#`, `\\`. (`MsdFile::ReadBuf` copies the character after the backslash literally.) Note that an escaped `\//` is the way to keep two slashes in a value.
  - A forgotten `;` is recovered: a `#` that is the first non-blank character of a line while a value is open ends the value (comment in the source: "many of these files are missing ;'s").
  - A trailing value without `;` at end of file is kept.
- Size: ROX refuses files > 100 MiB. StepMania has no such limit for songs (edits: `MAX_EDIT_STEPS_SIZE_BYTES`).

## Structure / metadata

Order is free, last tag wins for scalar tags; each `#NOTES` appends a chart. Tags read by `SMLoader::LoadFromSimfile` ([source](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp), `sm_parser_helper_t`):

| Tag | Value | Notes |
|---|---|---|
| `#TITLE` `#SUBTITLE` `#ARTIST` | text | |
| `#TITLETRANSLIT` `#SUBTITLETRANSLIT` `#ARTISTTRANSLIT` | text | sort/ASCII fallback when native display is off |
| `#GENRE` `#CREDIT` | text | `#CREDIT` = simfile author (also used as chart credit in `.sm`) |
| `#BANNER` `#BACKGROUND` `#CDTITLE` `#LYRICSPATH` | path relative to the song folder | `#LYRICSPATH` = [`.lrc`](https://github.com/stepmania/stepmania/wiki/lrc) |
| `#MUSIC` | audio path | ROX falls back to the first `.ogg/.oga/.mp3/.wav/.flac` of the folder when empty or missing ([ROX source: sm/mod.rs `parse_bytes`](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/mod.rs)) |
| `#INSTRUMENTTRACK` | `Track=file,Track=file` | extra audio tracks (guitar, bass, ...) |
| `#OFFSET` | float seconds | see Timing model; **sign is inverted vs. DWI `#GAP`** |
| `#BPMS` | `beat=bpm,beat=bpm,...` | the **only mandatory timing tag** |
| `#STOPS` (alias `#FREEZES`) | `beat=seconds,...` | |
| `#DELAYS` | `beat=seconds,...` | (SM5 additions also accepted in `.sm`) |
| `#TIMESIGNATURES` | `beat=num=den,...` | stored, no effect on the 4-beat measure grid |
| `#TICKCOUNTS` | `beat=ticks,...` | hold-checkpoint rate, clamped 0..48 |
| `#SAMPLESTART` `#SAMPLELENGTH` | seconds (float) | preview clip in the song wheel |
| `#DISPLAYBPM` | `120` or `90:270` or `*` | display only; `*` = random cycling |
| `#SELECTABLE` | `YES` / `NO` | legacy `ROULETTE`, `ES`, `OMES`, integers are mapped to YES |
| `#BGCHANGES` (+ `#BGCHANGES2`.. layers, `#ANIMATIONS` old alias) | `beat=file=rate=transition=effect1=effect2=effect=file2=transition=color1=color2,...` (1..11 `=`-separated fields) | background timeline, see below |
| `#FGCHANGES` | same syntax as BGCHANGES | foreground layer (NotITG/OpenITG mod files are driven from here, see [family overview](../README.md)) |
| `#KEYSOUNDS` | `file,file,...` | referenced by index from `[n]` suffixes in note data; a leading `#` file name is written `\#name` |
| `#ATTACKS` | `TIME=t:LEN=l:MODS=mods:...` (or `END=`) | per-song modifier script (ITG/SM4 "attacks") |
| `#MENUCOLOR`, `#LASTBEATHINT`, `#MUSICBYTES`, `#FIRSTBEAT`, `#LASTBEAT`, `#SONGFILENAME`, `#HASMUSIC`, `#HASBANNER`, `#MUSICLENGTH`, `#SAMPLEPATH`, `#LEADTRACK` | | legacy / cache tags; ignored (logged as unknown) |
| `#NOTES` (or `#NOTES2`) | 6 parameters, see below | one per chart |

Unknown tags are skipped with a log line.

### `#NOTES` chart parameters

`#NOTES:` is followed by **six** `:`-separated parameters (the loader requires at least 7 tokens counting the tag name):

```
#NOTES:
     <stepstype>:        1  e.g. dance-single
     <description>:      2  free text (chart author / name; for Edit charts it is the edit name)
     <difficulty>:       3  Beginner | Easy | Medium | Hard | Challenge | Edit (legacy names accepted)
     <meter>:            4  integer foot rating
     <radarvalues>:      5  comma list of floats (generated, ignored by loaders)
     <note data>         6  measures, see Notes
;
```

- `stepstype` (case: StepMania compares `StringToStepsType`; write lower-case): see the step-type table in [the family overview](../README.md#step-types-and-column-counts). `ez2-single-hard` is rewritten to `ez2-single`, `para` to `para-single`.
- `difficulty`: `OldStyleStringToDifficulty` accepts (case-insensitive) `beginner`, `easy`/`basic`/`light`, `medium`/`another`/`trick`/`standard`/`difficult`, `hard`/`ssr`/`maniac`/`heavy`, `challenge`/`smaniac`/`expert`/`oni`, `edit`. An unknown string becomes `Edit`. A `Hard` chart whose description is `smaniac` or `challenge` is promoted to `Challenge` (SM 1.x/3.0 hack).
- `meter`: empty => 1 (some Zenius-I-vanisher X-specials have none).
- `radarvalues`: comma list of floats, **generated** by the editor (groove radar). The SM5 `.sm` writer emits 11 categories per player (comment in `NotesWriterSM.cpp`: "OpenITG simfiles use 11 radar categories"), i.e. 22 numbers for two players; older files have 5 per player. Loaders ignore the value (it is recomputed).
- In the file, a chart is usually preceded by a comment `//---------------dance-single - <description>----------------` written by StepMania.

## Timing model

- **Beats and rows.** Everything is expressed in *beats* (quarter notes) from beat 0. Internally StepMania stores 48 rows per beat (`ROWS_PER_BEAT = 48`, [NoteTypes.h](https://github.com/stepmania/stepmania/blob/master/src/NoteTypes.h)); a measure is always **4 beats = 192 rows** whatever `#TIMESIGNATURES` says (`BEATS_PER_MEASURE = 4`). Beat values in tags are rounded to the nearest row (`BeatToNoteRow = lrint(beat*48)`).
- **`#OFFSET`**: beat 0 is located at music time **`-#OFFSET` seconds**. `#OFFSET:-1.5` means beat 0 happens 1.5 s into the audio; a positive offset means the chart starts before the audio (silence cut off). This is the opposite sign of DWI `#GAP` and KSF `#STARTTIME` (which are positive = delay). Conversion: `time(beat0) = -offset`. (Per-chart offset exists only in `.ssc`.) StepMania additionally applies its global offset preference at runtime.
- **BPM**: `#BPMS:0=120,32=180;`. The segment applies from its beat on; `time = sum(dBeat*60/bpm)` between changes. If beat 0 has no entry, the first listed BPM is used ("Using the value from the next BPM change"); no valid BPM at all => 60 BPM default. BPM entries with value 0 are dropped; entries before beat 0 are ignored (except for the starting value).
- **Stops** (`beat=seconds`): the arrows freeze **after** the notes of that beat: a note on the stop beat is hit *before* the pause. **Delays** (`beat=seconds`): freeze **before** the beat: notes on the beat are hit *after* the pause. Stops before beat 0 are folded into the offset.
- **Warps in `.sm` (negative encoding)**: `.sm` has no `#WARPS` tag. SM4/5 emulate warps through **negative or extremely large values**: a negative stop (`beat=-0.5`), a negative BPM, or a BPM above `9999999` (`FAST_BPM_WARP`) means "skip": `SMLoader::ProcessBPMsAndStops` converts them into `WarpSegment`s by tracking the "time deficit" (`timeofs`) and emitting a warp when it is paid back; a warp that never ends covers the rest of the chart (end beat `99999999`). Notes inside a warp cannot be hit. This is the classic "negative stop / negative BPM" gimmick of ITG/SM3.95-era files.
- `#FAKES`, `#WARPS`, `#SPEEDS`, `#SCROLLS`, `#COMBOS`, `#LABELS`: not `.sm` tags in StepMania's `.sm` loader table (except via `SMLoader::ProcessSpeeds/ProcessFakes`, used by SMA/SSC); they exist in [`.ssc`](../ssc/README.md).
- Position -> time: build the list of events sorted by beat with the order *BPM, then warp, then stop (after), delay (before)*; accumulate seconds; subtract `offset` (add `-offset`).

## Notes

The 6th `#NOTES` parameter is the chart. Parsing rules (`NoteDataUtil::LoadFromSMNoteDataStringWithPlayer`, [source](https://github.com/stepmania/stepmania/blob/master/src/NoteDataUtil.cpp)):

1. Remove `//` comments (to end of line).
2. Split on `,` into **measures** (empty segments skipped, so `,,` is one separator, not an empty measure; the last measure is ended by the `;`).
3. Each non-blank line of a measure (trimmed of spaces/tabs/CR) is a **row** of one char per column (extra chars after the column count are ignored; missing chars = empty). `N` lines in a measure divide the 4 beats evenly: row `l` is at beat `(m + l/N) * 4`. Valid quantizations are 4, 8, 12, 16, 24, 32, 48, 64, 192 lines per measure (StepMania writes the smallest of these that holds every note of the measure; the 4-line measure is the minimum). Other counts are loaded but rounded to the 1/192 grid.
4. Cell characters:

| Char | Meaning (StepMania 5) |
|---|---|
| `0` | empty |
| `1` | tap |
| `2` | hold head (freeze) |
| `3` | hold **or roll** tail (closes the hold started in the same column; unmatched `3` => warning and ignored) |
| `4` | roll head (hit repeatedly) |
| `M` | mine (upper-case only in StepMania; ROX also accepts `m`) |
| `L` | lift (release note) |
| `F` | fake (never judged) |
| `K` | auto-keysound row (no visible note; plays its `[n]` sample) |
| `A` | attack note: **written** as `A{mods:seconds}` but the loader has no code for it (the `case 'A'`/`{...}` parsing is under `#if 0`), so such files lose the note or misalign the row [source reading] |
| `N` | minefield head: commented out in the source, not supported |
| other | treated as empty (never an error) |

   Any note char may be followed by `[n]` = keysound index into `#KEYSOUNDS`.
5. Holds: head `2` (or roll `4`) in a column up to the next `3` in the same column. A head without tail is dropped ("unmatched 2"). Hold length = row distance (in 1/48 beats) of head and tail.
6. A chart may contain several **players' parts** separated by `&` (routine/co-op charts: `dance-routine`, `pump-routine`); parts are merged with a player number per note.
7. Column count must match the step type (see table below); StepMania uses the step type's `iNumTracks`.

Column order: for `dance-*` it is Left, Down, Up, Right (`dance-solo`: L, UL, D, U, UR, R; `dance-double`: P1 L,D,U,R then P2 L,D,U,R). For `pump-*` it is DL, UL, C, UR, DR (`pump-double`: two such pads) [StepMania `GameManager` style tables]. `kb7-single`: 7 columns left to right.

## Audio & images

Only `#MUSIC` (and `#INSTRUMENTTRACK`) reference audio, as paths relative to the song folder. Image tags: `#BANNER`, `#BACKGROUND`, `#CDTITLE` (and in `.ssc` also `#JACKET`, `#CDIMAGE`, `#DISCIMAGE`, `#PREVIEWVID`). Video/animations are only reachable through `#BGCHANGES`/`#FGCHANGES` entries (any file name; `.ini`/`.xml` entries are refused unless quirks mode is on, which is how NotITG mod files are bypassed in stock StepMania). If `#BGCHANGES` is non-empty and does not contain `-nosongbg-`, StepMania appends a change back to `#BACKGROUND` at the last beat ("song background hack"); StepMania writes `99999=-nosongbg-=1.000=0=0=0` to suppress that. Keysounds: `#KEYSOUNDS` + `[n]` suffix (rare in `.sm`; StepMania writes `#NOTES2` instead of `#NOTES` when keysounds exist, and the loaders accept both).

## Versions & variants

- No version tag in `.sm` (a `.ssc` has `#VERSION`). Written by StepMania 5 as UTF-8 with `\r\n`.
- Note characters: the wiki lists `0 1 2 3 4 M` as the standard set and `K`, `L`, `F` as "later versions of StepMania" additions. Timing tags beyond `#BPMS/#STOPS` (`#DELAYS`, `#TIMESIGNATURES`, `#TICKCOUNTS`, `#ATTACKS`) are read by the SM5 `.sm` loader; the SM5 `.sm` **writer** has no `#WARPS`/`#FAKES`/`#SPEEDS`/`#SCROLLS`: it saves warps back as **negative stops** (`-(60/BPM)*length` seconds at the warp beat) and delays as stops placed one row (1/48 beat) before the delay beat (`NotesWriterSM.cpp`), and drops the rest.
- Forks: ITG / OpenITG / NotITG (mods in `#FGCHANGES`/`#BGCHANGES`, difficulty slot shown as Novice/Easy/Medium/Hard/Expert), SM AMX ([`.sma`](../../stepmania-amx/sma/README.md)), StepF2/StepP1 pump forks (note syntax `{note|attribute|fake|reserved}`, SSC `#VERSION:0.81`), Etterna (same tags; adds chart keys in its cache), see [family overview](../README.md).
- `#MENUCOLOR` (SM 3.9+ non-standard) appears in the wild; unsupported in SM5.

## Quirks & pitfalls

- `#BPMS` with a stop/BPM at a negative beat and the negative-value warp encoding (see Timing). A parser that ignores them shifts every later note ("every note after the first #STOPS of a file would be early" in the ROX source comment).
- `:` in a value (title like `Re:Zero`) is a **parameter separator** unless written `\:`. For scalar tags a robust reader re-joins the parameters with `:` (ROX `Tag::text`); StepMania uses only parameter 1, so the title is truncated.
- `;` / `#` / `\` / `//` inside text must be escaped; an unescaped `//` (e.g. `http://...` in a `#BGCHANGES` file name or title) starts a comment and truncates the rest of the line.
- Duplicate `#NOTES` with the same type/difficulty are all loaded (edits are told apart by description).
- Hold tail char `3` is shared by holds and rolls; the head decides the kind.
- Row count per measure is arbitrary; do not assume 4/8/16/... or the same count in every measure.
- Trailing spaces, CRLF/LF mixes, blank lines inside measures, comments with `,` or `;` (`// 4,5` is fine because comments are stripped first, but `//` inside `#BGCHANGES` URLs is not).
- `#OFFSET` is in seconds, `#SAMPLESTART` also seconds, `.dwi` `#GAP` is in ms and sign-flipped: converters regularly get this wrong.
- ITG-era files use negative BPMs for "backwards" gimmicks; ROX refuses charts with BPM <= 0 or negative stops/delays rather than playing them wrong ([ROX source: sm/ssc_parser.rs `timing_for`](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/ssc_parser.rs)).

## Example

Excerpt of the real sample [`samples/Earth Angel.sm`](samples/Earth%20Angel.sm) (header trimmed, first measures of the chart):

```
#TITLE:Earth Angel;
#ARTIST:Aero;
#CREDIT:kangalioo;
#MUSIC:music.ogg;
#OFFSET:-1.214275;
#SAMPLESTART:101.254303;
#SAMPLELENGTH:12.000000;
#BPMS:0.000000=180.000000;
#STOPS:;

#NOTES:
     dance-single:
     :
     Challenge:
     1:
     0.116112,0.158992,0.125463,0.000000,0.218196,...:
  // measure 0
0000
0000
0000
0000
,  // measure 1
...
```

Hand-built illustration (from the rules above, not from a real file) with a hold, a roll, a mine and a tap (4 lines per measure = one row per beat):

```
#NOTES:
     dance-single:
     :
     Hard:
     9:
     0,0,0,0,0:
2000
0000
0M10
0000
,
3000
0004
0000
0003
;
```

(column 0: hold head at beat 0 and tail at beat 4; row `0M10` at beat 2 = mine on column 1 and tap on column 2; column 3: roll head at beat 5, tail at beat 7.)

## ROX support

ROX 0.8.1 reads and writes `.sm` ([ROX source: src/formats/sm/](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/)):

- **Read** (`SmDecoder`, `parser.rs`, `ssc_parser.rs`): same MSD tokenizer (comments, `\` escapes, missing `;` recovery). Only **`dance-single` (4), `dance-solo` (6), `dance-double` (8), `pump-single` (5), `pump-halfdouble` (6), `kb7-single` (7)** charts are kept; other step types (`dance-couple`, `pump-double`, `dance-routine`, `techno-*`, ...) go to `SmFile::skipped`. A `#NOTES` with fewer than 6 parameters, rows of the wrong width, a BPM <= 0, or a negative stop/delay/warp refuse that chart. The decoder returns the **first playable chart**; `parse_bytes` exposes all (`SmFile.charts`).
- Timing: `#BPMS`, `#STOPS`, `#DELAYS`, and (if present) `#WARPS`/`#FAKES` through `TimingData` (stop after the beat's notes, delay before, warp = unhittable span; notes in warps/fakes and holds starting there are dropped). `#OFFSET` is **baked into note times** (`shift = -offset`) so `audio_offset_us = 0`. Row position: measure*4 + index*4/lines, rounded to 1/48 beat. `#TIMESIGNATURES` ignored (measure = 4 beats).
- Notes: `1` and `L` => Tap, `2`..`3` => Hold, `4`..`3` => Burst (roll), `M`/`m` => Mine; `F`, `K`, unknown => dropped. `#SPEEDS`, `#SCROLLS`, `#LABELS`, `#COMBOS`, `#TICKCOUNTS`, `#ATTACKS`, `#BGCHANGES`, keysound indices `[n]` are not read.
- Metadata: title, artist, `#CREDIT`, music (with first-audio-file fallback), background, sample start/length. Difficulty name = difficulty (or the description for `Edit`); value = `#METER`.
- **Write** (`SmEncoder`): header (`#TITLE`, `#ARTIST`, `#CREDIT`, `#MUSIC`, `#BACKGROUND`, `#OFFSET`, `#SAMPLESTART/LENGTH`, `#SELECTABLE:YES`), `#BPMS` (derived from BPM timing points; no stops are written), one `#NOTES` chart with step type chosen from the column count: **6 => dance-solo, 8 => dance-double, anything else => dance-single** (so 5- or 7-key ROX charts are *not* given pump/kb7 types in `.sm`; use the `.ssc` encoder for 5/7), `Hard` unless the name is one of Beginner/Easy/Medium/Hard/Challenge/Edit, `1 2 3 4 M` cells, 1/48-beat grid.

## Parsers & tools

- StepMania C++: [NotesLoaderSM.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp), [NotesWriterSM.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSM.cpp), [MsdFile.cpp](https://github.com/stepmania/stepmania/blob/master/src/MsdFile.cpp), [NoteDataUtil.cpp](https://github.com/stepmania/stepmania/blob/master/src/NoteDataUtil.cpp) (C++). Etterna's fork: [etternagame/etterna](https://github.com/etternagame/etterna) (C++).
- [Anders429/msd](https://github.com/Anders429/msd) (Rust, MSD tokenizer via serde); [Anders429/simfile](https://github.com/Anders429/simfile) (Rust); [simfile](https://docs.simfile.dev/) (Python); [raindrop NoteLoaderSM](https://github.com/zardoru/raindrop/blob/master/src/NoteLoaderSM.cpp) (C++); [ssc-parser](https://www.npmjs.com/package/ssc-parser) (JS, PEG, SSC); [PerryAsleep/StepManiaLibrary](https://github.com/PerryAsleep/StepManiaLibrary) (C#); [ArrowVortex](https://arrowvortex.ddrnl.com/) and the StepMania editor (editors); [Stependous](https://stependous.sourceforge.net/) (converter).

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSM.cpp
- https://github.com/stepmania/stepmania/blob/master/src/MsdFile.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NoteDataUtil.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NoteTypes.h
- https://github.com/stepmania/stepmania/blob/master/src/GameManager.cpp
- https://github.com/stepmania/stepmania/blob/master/src/Difficulty.cpp
- https://github.com/stepmania/stepmania/wiki/sm (File-Formats/sm.md), https://github.com/stepmania/stepmania/wiki/Note-Types, https://github.com/stepmania/stepmania/wiki/Timing-Segments
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/ssc_msd5.txt
- https://github.com/etternagame/etterna (loaders under src/Etterna/Models/NoteLoaders)
- https://github.com/Anders429/msd (README: MSD origin and syntax)
- ROX source: `rhythm-open-exchange/src/formats/sm/` (parser.rs, msd.rs, ssc_parser.rs, timing_data.rs, decoder.rs, encoder.rs)
- Repo samples: [samples/](samples/)
