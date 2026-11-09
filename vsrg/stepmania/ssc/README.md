# StepMania 5 simfile (`.ssc`)
Kind: chart

Doc status: complete · ROX: reads/writes · Category: vsrg · Encoding: text

## Overview

`.ssc` is the StepMania 5 successor of [`.sm`](../sm/README.md), from the sm-ssc fork. Same MSD syntax, but a file is song header tags plus one `#NOTEDATA` block per chart. Each chart has its own metadata and may have its own timing. StepMania 5, Etterna (cache), ITGmania, Project OutFox and the editors ArrowVortex/SM5 write it. Many packs ship both `.sm` and `.ssc`. Samples: [`samples/`](samples/).

## Packaged in

- Shipped in: `.smzip` (zip with install-relative paths `Songs/<Group>/<Song>/` holding `.sm`/`.ssc` and audio, optional `smzip.ctl`; plain `.zip` packs have the same layout).

## Container & encoding

- Text, UTF-8 (SM5 writes `\r\n`; LF also read). ROX strips a UTF-8 BOM and decodes lossily (undecodable bytes become U+FFFD in text fields only; `.sm` in ROX is strict UTF-8).
- One file per song with all charts. Same tokenizer as `.sm`: `//` comments, `\` escapes, `;` terminator with recovery of a missing `;` before a line starting with `#`, `:`-separated parameters (see the [`.sm` doc](../sm/README.md#container--encoding)).
- StepMania loads `*.ssc` before `*.sm` in a folder ([Song.cpp](https://github.com/stepmania/stepmania/blob/master/src/Song.cpp)) and caches `.ssc`-style files in `Cache/Songs/...` with extra tags (see Versions).

## Structure / metadata

The loader (`SSCLoader::LoadFromSimfile`) has two states: song info until a `#NOTEDATA` tag, then chart info until the `#NOTES`/`#NOTES2` tag that ends the chart and returns to song state. `NotesWriterSSC` writes tags in this order (global tags first):

### Song tags

| Tag | Value |
|---|---|
| `#VERSION` | float, `.ssc` format version (SM5 writes `0.83`, `STEPFILE_VERSION_NUMBER` in `Steps.h`) |
| `#TITLE` `#SUBTITLE` `#ARTIST` `#TITLETRANSLIT` `#SUBTITLETRANSLIT` `#ARTISTTRANSLIT` `#GENRE` | text |
| `#ORIGIN` | text, source game of a crossover song (no known theme uses it) |
| `#CREDIT` | simfile author |
| `#BANNER` `#BACKGROUND` `#PREVIEWVID` `#JACKET` `#CDIMAGE` `#DISCIMAGE` `#CDTITLE` `#LYRICSPATH` | paths relative to the song folder |
| `#MUSIC` | audio path |
| `#PREVIEW` | separate preview audio file (replaces `#SAMPLESTART/#SAMPLELENGTH` in the wheel when set) |
| `#INSTRUMENTTRACK` | `Track=file,...` |
| `#OFFSET` | float seconds, beat 0 at music time `-offset` |
| `#SAMPLESTART` `#SAMPLELENGTH` | seconds |
| `#SELECTABLE` | `YES`/`NO` |
| `#DISPLAYBPM` | `n`, `min:max`, or `*` |
| `#BPMS` `#STOPS` `#DELAYS` `#WARPS` `#TIMESIGNATURES` `#TICKCOUNTS` `#COMBOS` `#SPEEDS` `#SCROLLS` `#FAKES` `#LABELS` | song-wide timing (see Timing model) |
| `#LASTSECONDHINT` | float; song end hint (needed when a song has only Edit charts) |
| `#BGCHANGES`, `#BGCHANGES2`.., `#FGCHANGES` | `beat=file=rate=transition=effectflag1=effectflag2=effectfile=file2=transitionfile=color1=color2,...` (1..11 fields); a `99999=-nosongbg-=...` sentinel entry is written and removed on load |
| `#KEYSOUNDS` | `file,file,...`; written `#KEYSOUNDS:\bgm.wav,01.wav,...` when the first name starts with `#` |
| `#ATTACKS` | `TIME=t:LEN=l:MODS=m:...` |
| cache-only: `#FIRSTSECOND` `#LASTSECOND` `#SONGFILENAME` `#HASMUSIC` `#HASBANNER` `#MUSICLENGTH` | written between `// cache tags:` and `// end cache tags` in `Cache/` files |

### Chart tags (inside a `#NOTEDATA` block)

| Tag | Value |
|---|---|
| `#NOTEDATA` | empty tag `#NOTEDATA:;`, starts a chart block |
| `#CHARTNAME` | chart name (introduced by `#VERSION` 0.74 = `VERSION_CHART_NAME_TAG`; before that the name was stored in `#DESCRIPTION`) |
| `#STEPSTYPE` | `dance-single`, `pump-single`, ... ([step types](../README.md#step-types-and-column-counts)) |
| `#DESCRIPTION` | free text (edit name / style); from `#VERSION` 0.74 distinct from `#CHARTNAME` |
| `#CHARTSTYLE` | custom style name |
| `#DIFFICULTY` | `Beginner`, `Easy`, `Medium`, `Hard`, `Challenge`, `Edit` (`StringToDifficulty`; empty => `Edit`) |
| `#METER` | integer foot rating |
| `#MUSIC` | per-chart audio override |
| `#RADARVALUES` | comma list, 14 categories per player (`Stream,Voltage,Air,Freeze,Chaos,Notes,TapsAndHolds,Jumps,Holds,Mines,Hands,Rolls,Lifts,Fakes` = `RadarCategory`), two players concatenated; values are recomputed unless loading cache/edit |
| `#CREDIT` | chart author |
| timing tags | `#OFFSET #BPMS #STOPS #DELAYS #WARPS #TIMESIGNATURES #TICKCOUNTS #COMBOS #SPEEDS #SCROLLS #FAKES #LABELS` and `#DISPLAYBPM`, `#ATTACKS`: only present when the chart has its own timing |
| `#STEPFILENAME` | cache files only (instead of `#NOTES`) |
| `#NOTES` / `#NOTES2` | the measures only, no parameters. `#NOTES2` is written instead of `#NOTES` when the song has `#KEYSOUNDS`; loaders accept both |

Writer comment before each chart: `//---------------<stepstype> - <description>----------------`.

## Timing model

Same beat/row/offset model as `.sm` (48 rows per beat, 4 beats per measure, beat 0 at `-#OFFSET` s; see the [`.sm` timing section](../sm/README.md#timing-model)), plus real segment tags. All are comma-separated `beat=value` lists; beat is a float; rows are `lrint(beat*48)`:

| Tag | Entry | Meaning |
|---|---|---|
| `#BPMS` | `beat=bpm` | `beat >= 0`, `bpm > 0` required (SSC loader ignores others with a log) |
| `#STOPS` | `beat=seconds` | freeze after the notes of the beat; `seconds > 0` |
| `#DELAYS` | `beat=seconds` | freeze before the beat's notes; `seconds > 0` |
| `#WARPS` | `beat=length_in_beats` | the covered beats are skipped instantly; notes inside cannot be hit. Version < 0.7 stored the destination beat, which the loader converts (`new - start`) |
| `#TIMESIGNATURES` | `beat=numerator=denominator` | only affects measure-line display, not timing (`TimeSignatureSegment`) |
| `#TICKCOUNTS` | `beat=ticks` | hold-checkpoint ticks per beat, clamped 0..48 (pump-style hold ticks) |
| `#COMBOS` | `beat=combo[=miss]` | combo increment per hit (and per miss, defaults to the hit value) |
| `#SPEEDS` | `beat=ratio=length=unit` | scroll-speed multiplier `ratio`, reached over `length` (beats if `unit=0`, seconds if `1`); `.sm`-style 2-value entries get defaults |
| `#SCROLLS` | `beat=ratio` | changes the note spacing/position factor (visual only; `0` stacks notes on one line) |
| `#FAKES` | `beat=length_in_beats` | notes inside are "fake": drawn but not judged |
| `#LABELS` | `beat=text` | named marker, no gameplay effect |

Split timing: from `#VERSION` >= 0.7 (`VERSION_SPLIT_TIMING`), if a chart contains any timing tag, StepMania builds a fresh `TimingData` for that chart from only the chart's tags (starting with the song's offset) and uses it instead of the song timing (`pNewNotes->m_Timing = stepsTiming` when `has_own_timing`). Charts without timing tags use the song's. A chart-level `#BPMS` therefore replaces the whole song timing, and a chart should repeat everything it needs. ROX: a chart with its own non-empty `#BPMS` uses its own `#STOPS/#DELAYS/#WARPS/#FAKES` too, even empty; a chart with only some of them falls back per tag to the song's. That is a superset of StepMania's behaviour for the usual cases.

Position to time: per chart, sort BPM/stop/delay/warp events by beat; seconds = sum of `dBeats*60/bpm` + stops/delays; beats covered by a warp add 0 seconds; finally `time_in_audio = time - offset`. Tie rule as in `.sm`: stop after, delay before, a BPM change on the same beat applies first.

## Notes

The `#NOTES` value uses the `.sm` measure grammar ([details](../sm/README.md#notes)): measures separated by `,`, one character per column, 4..192 lines per measure, last measure ended by the tag's `;`.

| Char | Meaning |
|---|---|
| `0` | empty |
| `1` | tap |
| `2` | hold head |
| `3` | hold/roll tail |
| `4` | roll head |
| `M` | mine |
| `L` | lift |
| `F` | fake |
| `K` | autokeysound (empty row sound) |
| `A{mods:secs}` | attack note, written by `NoteDataUtil::GetSMNoteDataString` but not parsed back (loader branch is `#if 0`) |

Optional `[n]` after any char = keysound index into `#KEYSOUNDS`. `&` separates player parts in routine charts. Columns follow `#STEPSTYPE`. A line in an `n`-line measure sits at `(measure + line/n)*4` beats. StepF2 `{note|attr|fake|reserved}` braces are not StepMania (OutFox parses them with its PIU loader at `#VERSION:0.81`).

## Audio & images

Paths relative to the song directory: `#MUSIC` (song or per-chart), `#PREVIEW`, `#INSTRUMENTTRACK`, `#BANNER`, `#BACKGROUND`, `#JACKET`, `#CDIMAGE`, `#DISCIMAGE`, `#CDTITLE`, `#PREVIEWVID`, `#LYRICSPATH` (`.lrc`), plus anything in `#BGCHANGES`/`#FGCHANGES` (images, videos, image folders, `.ini`/`.xml` effects). Keysounds via `#KEYSOUNDS` + `[n]`. No audio is embedded. `#SAMPLESTART/#SAMPLELENGTH` define the wheel preview unless `#PREVIEW` is set.

## Versions & variants

`#VERSION` constants in `NotesLoaderSSC.h`: 0.53 fake radar value, 0.56 warp segments, 0.7 split timing (chart-level timing), 0.72 chart offset moved before attacks, 0.74 `#CHARTNAME` (earlier `#DESCRIPTION` held the name), 0.77 cache switch tag, 0.83 note-count radar (current).

- StepMania 5.x, ITGmania: the ITGmania loader accepts chart tags `#TECHCOUNTS`, `#NPSPERMEASURE`, `#NOTESPERMEASURE`, `#PEAKNPS`, `#NOTEANNOTATIONS`, `#GROOVESTATSHASH`, `#GROOVESTATSHASHVERSION` ([itgmania NotesLoaderSSC.cpp](https://github.com/itgmania/itgmania/blob/release/src/NotesLoaderSSC.cpp)). They are computed statistics / the [GrooveStats](../README.md#grooveStats-chart-hash) key, so cache files only [inference]. Stock StepMania lacks them.
- Etterna: same tags plus `#CHARTKEY` (`X` + SHA-1 hex of note types and integer BPM per non-empty row) and `#MSDVALUES` (difficulty calculator output) in its cache ([etterna Steps.cpp/NotesWriterETT.cpp](https://github.com/etternagame/etterna)). It also loads `.osu`.
- Project OutFox: extra game types (`dance`, `groove`, `pump`, `techno`, `smx`, `stepstage`, ...) and a PIU loader triggered by `#VERSION:0.81` (or a `ForcePIU` file in the group folder).
- Drafts: [`new format draft.txt`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/new%20format%20draft.txt) (never-used MSD5 layout with `$TAGS` and `#NOTEDATA#`) and [`ssc_msd5.txt`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/ssc_msd5.txt) (the actual tag list; "hacky file format doc").
- `//---` comments and blank lines are not significant.

## Quirks & pitfalls

- `#NOTEDATA:;` has an empty value; scan for `#NOTEDATA:` to delimit charts. A chart ends at its `#NOTES`/`#NOTES2`; tags after it (before the next `#NOTEDATA`) belong to the song again.
- With partial chart timing tags, StepMania's chart `TimingData` starts empty (only the offset is copied), so chart-level `#BPMS` is effectively mandatory. ROX falls back to the song's.
- `#OFFSET` per chart is allowed: charts of one song can have different audio sync.
- `#VERSION` < 0.7: chart timing tags are ignored. Warps are `beat=length` (new) vs `beat=destination` (< 0.7); negative warps are invalid.
- `#TIMESIGNATURES` leaves the 192-row measure alone: measure lines follow it, note placement is always 4 beats/measure. `#SPEEDS`/`#SCROLLS` change only visual position, not judgement time.
- `#RADARVALUES` count differs per version (cache/edit loaders split the list evenly across 2 players).
- Mixed line endings, trailing whitespace and `//` comments inside `#NOTES` are normal.

## Example

Real excerpt from [`samples/Tokimeki Experience.ssc`](samples/Tokimeki%20Experience.ssc) (header + start of the first chart):

```
#VERSION:0.83;
#TITLE:Tokimeki Experience;
#ARTIST:Poppin' Party;
#MUSIC:Tokimeki Experience.ogg;
#OFFSET:-0.149002;
#SAMPLESTART:33.482334;
#SAMPLELENGTH:12.000000;
#BPMS:0.000=180.000;
#TIMESIGNATURES:0.000=4=4;
#TICKCOUNTS:0.000=4;
#COMBOS:0.000=1;
#SPEEDS:0.000=1.000=0.000=0;
#SCROLLS:0.000=1.000;
#LABELS:0.000=Song Start;

//---------------dance-single - ----------------
#NOTEDATA:;
#STEPSTYPE:dance-single;
#DIFFICULTY:Medium;
#METER:7;
#RADARVALUES:0.741650,0.894701,...;
#NOTES:
0000
0000
...
```

## ROX support

ROX 0.8.1 reads and writes `.ssc` ([ROX source: src/formats/sm/ssc_parser.rs, ssc_decoder.rs, ssc_encoder.rs, timing_data.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/)).

- Read: song tags (`#TITLE`, `#ARTIST`, `#CREDIT`, `#MUSIC` + first-audio fallback, `#BANNER`, `#BACKGROUND`, `#SAMPLESTART/#SAMPLELENGTH`, `#OFFSET`); per `#NOTEDATA` chart: `#STEPSTYPE` (kept: `dance-single` 4, `pump-single` 5, `dance-solo` 6, `pump-halfdouble` 6, `kb7-single` 7, `dance-double` 8; others skipped with a reason), `#DESCRIPTION`, `#DIFFICULTY`, `#METER`, `#CREDIT`, `#NOTES`/`#NOTES2`, and chart-level `#BPMS/#STOPS/#DELAYS/#WARPS/#FAKES/#OFFSET` with split-timing semantics. Stops, delays and BPM changes move the notes; warped notes, notes inside `#FAKES` (and holds starting there) are dropped; `#OFFSET` is baked into times.
- Not read: `#SPEEDS`, `#SCROLLS`, `#TIMESIGNATURES`, `#LABELS`, `#COMBOS`, `#TICKCOUNTS`, `#ATTACKS`, `#BGCHANGES`, `#KEYSOUNDS`/`[n]`, `#CHARTNAME`. A chart with BPM <= 0 or a negative stop/delay/warp is refused ([ROX source: ssc_parser.rs `timing_for`]); a file without `#NOTEDATA` errors. The decoder returns the first playable chart; the library exposes all.
- Notes: `1`, `L` => Tap; `2`..`3` => Hold; `4`..`3` => Burst (roll); `M` => Mine; `F`/`K` not played.
- Write (`SscEncoder`): `#VERSION:0.83`, header as the `.sm` encoder, `#BPMS`, one `#NOTEDATA` with `#STEPSTYPE` by column count (4 dance-single, 5 pump-single, 6 dance-solo, 7 kb7-single, 8 dance-double; other counts error), `#DESCRIPTION` = difficulty name, `#DIFFICULTY`, `#METER`, `#CREDIT`, `#NOTES` on the 1/48-beat grid. No stops, warps or per-chart timing written.

## Parsers & tools

- StepMania C++: [NotesLoaderSSC.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSSC.cpp), [NotesWriterSSC.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSSC.cpp), [TimingData.cpp](https://github.com/stepmania/stepmania/blob/master/src/TimingData.cpp), [Song.h](https://github.com/stepmania/stepmania/blob/5_1-new/src/Song.h), [Steps.h](https://github.com/stepmania/stepmania/blob/5_1-new/src/Steps.h).
- Etterna: [etternagame/etterna](https://github.com/etternagame/etterna) (C++). ITGmania: [itgmania/itgmania](https://github.com/itgmania/itgmania) (C++). OutFox: [TeamRizu/OutFox](https://github.com/TeamRizu/OutFox) (C++, closed core; binary releases).
- [Anders429/simfile](https://github.com/Anders429/simfile) (Rust), [simfile](https://docs.simfile.dev/) (Python), [ssc-parser](https://www.npmjs.com/package/ssc-parser) (JS PEG), [raindrop](https://github.com/zardoru/raindrop) `NoteLoaderSM` (C++, SSC with warps; "no keysounds or delays"), [PerryAsleep/StepManiaLibrary](https://github.com/PerryAsleep/StepManiaLibrary) (C#), [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (Rust, SSC<->SSQ), [PerryAsleep/StepManiaChartGenerator](https://github.com/PerryAsleep/StepManiaChartGenerator) (C#).
- Editors: StepMania 5 editor, [ArrowVortex](https://arrowvortex.ddrnl.com/), [Stependous](https://stependous.sourceforge.net/).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). The OutFox Serenity charts are chart text only. Some third-party files have unknown licence or are Konami/Andamiro charts (noted in `SOURCES.md`).

More: the remaining `.ssc` of the OutFox Serenity community pack ([TeamRizu/OutFox-Serenity](https://github.com/TeamRizu/OutFox-Serenity), 39 `.ssc` at commit `e92f5439f563285dbf26399a88d4b2ada5c46247`; charts must be CC-BY 3.0/4.0 per its [guidelines](https://projectoutfox.com/outfox-serenity/guidelines)); `Songs/StepMania 5/`; the [StepMania-AMX/PIU-Simfiles](https://github.com/StepMania-AMX/PIU-Simfiles) fork of rayden-61/PIU-Simfiles (1,624 files, Pump It Up simfiles from StepF2/StepP1 as `.ssc`, no licence, Andamiro charts); [Etterna](https://github.com/etternagame/etterna) and [ITGmania](https://github.com/itgmania/itgmania) theme folders (`Themes/_fallback/Other/*.ssc`). Not found in the open: `lights-cabinet` charts, Shift-JIS `.ssc`. ITGmania (commit `8a3bf8884acdcb69363f7f0ea592138e398c71e4`) loads `.ssc`, `.sm`, `.sma`, `.dwi`, `.json`, writes `.sm`, `.ssc`, `.dwi`, `.json` plus `CourseLoaderCRS`/`CourseWriterCRS`: no chart extension of its own. Project OutFox is closed source (the public [TeamRizu/OutFox](https://github.com/TeamRizu/OutFox) repository holds only a README, licence and issue-tracker docs); its community packs use `.ssc` (plus `.bms/.pms/.dtx` for keysounded charts, per the Serenity guidelines). NotITG is closed source; no open-licensed NotITG mod chart was found.

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSSC.cpp (and .h for `VERSION_*`)
- https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSSC.cpp
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp (shared `ProcessSpeeds/Fakes/TimeSignatures/Tickcounts`)
- https://github.com/stepmania/stepmania/blob/master/src/TimingData.cpp
- https://github.com/stepmania/stepmania/blob/master/src/GameConstantsAndTypes.h (`RadarCategory`)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/ssc_msd5.txt, `new format draft.txt`
- https://github.com/stepmania/stepmania/wiki/ssc (ssc.md), Timing-Segments, Note-Types
- https://github.com/etternagame/etterna (Steps.cpp `GenerateChartKey`, NotesWriterETT.cpp)
- https://github.com/itgmania/itgmania/blob/release/src/NotesLoaderSSC.cpp
- https://projectoutfox.com/news/project-outfox-04151-released (PIU loader / `#VERSION:0.81`)
- ROX source: `rhythm-open-exchange/src/formats/sm/`
- Repo samples: [samples/](samples/)
