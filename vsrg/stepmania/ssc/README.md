# StepMania 5 simfile (`.ssc`)
Kind: chart

Doc status: complete · ROX: reads/writes · Category: vsrg · Encoding: text

## Overview

`.ssc` is the StepMania 5 successor of [`.sm`](../sm/README.md), created in the sm-ssc fork (expanded "Spinal Shark Collective" in community usage) and merged into StepMania 5.0. It keeps the MSD syntax (`#TAG:value;`) but organizes a file as **song header tags + one `#NOTEDATA` block per chart**; each chart carries its own metadata (`#STEPSTYPE`, `#DESCRIPTION`, `#DIFFICULTY`, `#METER`, `#CREDIT`, `#CHARTNAME`...) and may carry **its own timing** (`#OFFSET`, `#BPMS`, `#STOPS`, `#DELAYS`, `#WARPS`, `#FAKES`, `#SPEEDS`, `#SCROLLS`, ...). It is the format written by StepMania 5, Etterna (cache), ITGmania, Project OutFox (preferred submission format of "OutFox Serenity", per projectoutfox.com) and the editors ArrowVortex/SM5. Many packs ship both `.sm` and `.ssc`. Samples: [`samples/`](samples/) (10 real files).

See also: [family overview](../README.md), [`.sm`](../sm/README.md), [`.edit`](../edit/README.md).

## Packaged in

- Packaged in [`smzip`](../smzip/).

## Container & encoding

- Text, UTF-8 (SM5 writes `\r\n` line ends; LF also read). A UTF-8 BOM may appear; ROX strips it and decodes lossily (undecodable bytes become U+FFFD in text fields only; `.sm` in ROX is strict UTF-8).
- One file per song containing all charts. Same tokenizer as `.sm`: `//` comments, `\` escapes, `;` terminator with recovery of a missing `;` before a line starting with `#`, `:`-separated parameters (see the [`.sm` doc](../sm/README.md#container--encoding)).
- StepMania loads `*.ssc` before `*.sm` in the same folder ([Song.cpp](https://github.com/stepmania/stepmania/blob/master/src/Song.cpp)); SM5 also caches `.ssc`-style files (`Cache/Songs/...`, with extra tags, see Versions).

## Structure / metadata

Two states in the loader (`SSCLoader::LoadFromSimfile`): *song info* until a `#NOTEDATA` tag, then *chart info* until the `#NOTES`/`#NOTES2` tag that ends the chart and returns to song state. Tags written by `NotesWriterSSC` in this order (global tags first):

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
| `#NOTEDATA` | **empty tag `#NOTEDATA:;`**, starts a chart block |
| `#CHARTNAME` | chart name (introduced by `#VERSION` 0.74 = `VERSION_CHART_NAME_TAG`; before that the name was stored in `#DESCRIPTION`) |
| `#STEPSTYPE` | `dance-single`, `pump-single`, ... ([step types](../README.md#step-types-and-column-counts)) |
| `#DESCRIPTION` | free text (edit name / style); from `#VERSION` 0.74 distinct from `#CHARTNAME` |
| `#CHARTSTYLE` | custom style name |
| `#DIFFICULTY` | `Beginner`, `Easy`, `Medium`, `Hard`, `Challenge`, `Edit` (`StringToDifficulty`; empty => `Edit`) |
| `#METER` | integer foot rating |
| `#MUSIC` | per-chart audio override |
| `#RADARVALUES` | comma list, 14 categories per player (`Stream,Voltage,Air,Freeze,Chaos,Notes,TapsAndHolds,Jumps,Holds,Mines,Hands,Rolls,Lifts,Fakes` = `RadarCategory`), two players concatenated; values are recomputed unless loading cache/edit |
| `#CREDIT` | chart author |
| timing tags | `#OFFSET #BPMS #STOPS #DELAYS #WARPS #TIMESIGNATURES #TICKCOUNTS #COMBOS #SPEEDS #SCROLLS #FAKES #LABELS` and `#DISPLAYBPM`, `#ATTACKS`: **only present when the chart has its own timing** |
| `#STEPFILENAME` | cache files only (instead of `#NOTES`) |
| `#NOTES` / `#NOTES2` | the measures (only the measures; no parameters). `#NOTES2` is written instead of `#NOTES` when the song has `#KEYSOUNDS`; loaders accept both |

Writer comment before each chart: `//---------------<stepstype> - <description>----------------`.

## Timing model

Identical beat/row/offset model as `.sm` (48 rows per beat, 4 beats per measure, offset sign: beat 0 at `-#OFFSET` s; see the [`.sm` timing section](../sm/README.md#timing-model)), plus real segment tags. All are `beat=value` lists separated by commas; "beat" is a float; rows are `lrint(beat*48)`:

| Tag | Entry | Meaning |
|---|---|---|
| `#BPMS` | `beat=bpm` | `beat >= 0`, `bpm > 0` required (SSC loader ignores others with a log) |
| `#STOPS` | `beat=seconds` | freeze **after** the notes of the beat; `seconds > 0` |
| `#DELAYS` | `beat=seconds` | freeze **before** the beat's notes; `seconds > 0` |
| `#WARPS` | `beat=length_in_beats` | the covered beats are skipped instantly; notes inside cannot be hit. Version < 0.7 stored the *destination beat*, which the loader converts (`new - start`) |
| `#TIMESIGNATURES` | `beat=numerator=denominator` | only affects measure-line display, not timing (`TimeSignatureSegment`) |
| `#TICKCOUNTS` | `beat=ticks` | hold-checkpoint ticks per beat, clamped 0..48 (pump-style hold ticks) |
| `#COMBOS` | `beat=combo[=miss]` | combo increment per hit (and per miss, defaults to the hit value) |
| `#SPEEDS` | `beat=ratio=length=unit` | scroll-speed multiplier `ratio`, reached over `length` (beats if `unit=0`, seconds if `1`); `.sm`-style 2-value entries get defaults |
| `#SCROLLS` | `beat=ratio` | changes the note spacing/position factor (visual only; `0` stacks notes on one line) |
| `#FAKES` | `beat=length_in_beats` | notes inside are "fake": drawn but not judged |
| `#LABELS` | `beat=text` | named marker, no gameplay effect |

**Song vs chart timing ("split timing")**: from `#VERSION` >= 0.7 (`VERSION_SPLIT_TIMING`), if a chart contains **any** timing tag, StepMania builds a fresh `TimingData` for that chart from *only the chart's tags* (starting with the song's offset) and uses it *instead of* the song timing (`pNewNotes->m_Timing = stepsTiming` when `has_own_timing`); charts without timing tags use the song's. So a chart-level `#BPMS` replaces the whole song timing; a chart should repeat everything it needs. (ROX's rule: a chart with its own non-empty `#BPMS` uses its own `#STOPS/#DELAYS/#WARPS/#FAKES` too, even empty; a chart with only some of them falls back per tag to the song's. That is a superset of StepMania's behaviour for the usual cases.)

Position -> time: per chart, sort BPM/stop/delay/warp events by beat; seconds = sum of `dBeats*60/bpm` + stops/delays; beats covered by a warp add 0 seconds; finally `time_in_audio = time - offset`. Same tie rule as `.sm`: stop after, delay before, a BPM change on the same beat applies first.

## Notes

The `#NOTES` value is the same measure grammar as `.sm` ([details](../sm/README.md#notes)): measures separated by `,`, rows of one character per column, 4..192 lines per measure, last measure ended by `;` of the tag.

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
| `A{mods:secs}` | attack note, written by `NoteDataUtil::GetSMNoteDataString` but **not parsed back** (loader branch is `#if 0`) |

Optional `[n]` after any char = keysound index into `#KEYSOUNDS`. `&` separates player parts in routine charts. Column count and order follow `#STEPSTYPE`. Note position inside the 4-beat measure of a `n`-line measure: `(measure + line/n)*4` beats.

Unsupported-by-StepMania but seen: StepF2 `{note|attr|fake|reserved}` braces (OutFox parses them with a dedicated PIU loader when `#VERSION:0.81`).

## Audio & images

Paths relative to the song directory: `#MUSIC` (song or per-chart), `#PREVIEW` (clip), `#INSTRUMENTTRACK`, `#BANNER`, `#BACKGROUND`, `#JACKET`, `#CDIMAGE`, `#DISCIMAGE`, `#CDTITLE`, `#PREVIEWVID`, `#LYRICSPATH` (`.lrc`), plus anything referenced by `#BGCHANGES`/`#FGCHANGES` (images, videos, folders of images, `.ini`/`.xml` effects). Keysound samples via `#KEYSOUNDS` + `[n]`. No audio is ever embedded. `#SAMPLESTART/#SAMPLELENGTH` define the wheel preview unless `#PREVIEW` is set.

## Versions & variants

`#VERSION` constants in `NotesLoaderSSC.h`: 0.53 fake radar value, 0.56 warp segments, **0.7 split timing** (chart-level timing allowed), 0.72 chart offset moved before attacks, **0.74 `#CHARTNAME` tag introduced** (earlier `#DESCRIPTION` held the name), 0.77 cache switch tag, 0.83 note-count radar (current). Dialects:

- **StepMania 5.0/5.1/5.2, ITGmania**: the ITGmania loader accepts the extra chart tags `#TECHCOUNTS`, `#NPSPERMEASURE`, `#NOTESPERMEASURE`, `#PEAKNPS`, `#NOTEANNOTATIONS`, `#GROOVESTATSHASH`, `#GROOVESTATSHASHVERSION` ([itgmania NotesLoaderSSC.cpp](https://github.com/itgmania/itgmania/blob/release/src/NotesLoaderSSC.cpp)); they are computed statistics / the [GrooveStats](../README.md#grooveStats-chart-hash) key, so they belong to cache files, not to authored charts [inference]. The tags are absent from stock StepMania.
- **Etterna**: reads/writes the same tags and adds `#CHARTKEY` (`X` + SHA-1 hex of the chart's note types and integer BPM per non-empty row) and `#MSDVALUES` (its difficulty calculator output) in its cache ([etterna Steps.cpp/NotesWriterETT.cpp](https://github.com/etternagame/etterna)). `.osu` is also loadable in Etterna.
- **Project OutFox**: `.ssc` plus the extra game types (`dance`, `groove`, `pump`, `techno`, `smx`, `stepstage`, ...), a dedicated PIU loader triggered by `#VERSION:0.81` (or a `ForcePIU` file in the group folder).
- Early sm-ssc / draft documents: [`new format draft.txt`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/new%20format%20draft.txt) (a "less conservative" never-used MSD5 layout with `$TAGS` and `#NOTEDATA#`) and [`ssc_msd5.txt`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/ssc_msd5.txt) (the actual tag list; "hacky file format doc").
- Per-file `//---` comments and blank lines are not significant.

## Quirks & pitfalls

- `#NOTEDATA:;` has an **empty value**; scanning for `#NOTEDATA:` is the reliable chart delimiter. Everything between two `#NOTEDATA` tags is that chart; the chart ends at its `#NOTES`/`#NOTES2` tag (tags after it, before the next `#NOTEDATA`, belong to the song again in StepMania's state machine).
- A chart whose timing tags are partial: StepMania's chart `TimingData` starts empty (only the offset is copied); chart-level `#BPMS` is then effectively mandatory. ROX falls back to the song's.
- `#OFFSET` per chart is allowed: two charts of the same song can have different audio sync.
- `#VERSION` < 0.7: chart timing tags are ignored by the loader (only song timing).
- Warps: `beat=length` (new) vs `beat=destination` (version < 0.7). Negative warps are invalid.
- `#TIMESIGNATURES` does **not** change the 192-row measure in the note data; measure lines are drawn according to it but note placement is always 4 beats/measure.
- `#SPEEDS`/`#SCROLLS` change only the visual position of notes; the judgement time is unchanged.
- Chart-level `#CREDIT` vs song `#CREDIT`; `#DESCRIPTION` of Edit charts is their name.
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

ROX 0.8.1 reads and writes `.ssc` ([ROX source: src/formats/sm/ssc_parser.rs, ssc_decoder.rs, ssc_encoder.rs, timing_data.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/)):

- **Read**: song tags (`#TITLE`, `#ARTIST`, `#CREDIT`, `#MUSIC` + first-audio fallback, `#BANNER`, `#BACKGROUND`, `#SAMPLESTART/#SAMPLELENGTH`, `#OFFSET`), one chart per `#NOTEDATA`: `#STEPSTYPE` (**kept: `dance-single` 4, `pump-single` 5, `dance-solo` 6, `pump-halfdouble` 6, `kb7-single` 7, `dance-double` 8**; others skipped with a reason), `#DESCRIPTION`, `#DIFFICULTY`, `#METER`, `#CREDIT`, `#NOTES`/`#NOTES2`, and chart-level `#BPMS/#STOPS/#DELAYS/#WARPS/#FAKES/#OFFSET` with split-timing semantics (see above). Stops, delays and BPM changes move the notes; warped notes, notes inside `#FAKES` (and holds starting there) are dropped; `#OFFSET` is baked into times. **Not read**: `#SPEEDS`, `#SCROLLS`, `#TIMESIGNATURES` (display only), `#LABELS`, `#COMBOS`, `#TICKCOUNTS`, `#ATTACKS`, `#BGCHANGES`, `#KEYSOUNDS`/`[n]`, `#CHARTNAME`. A chart with BPM <= 0 or a negative stop/delay/warp is refused ([ROX source: ssc_parser.rs `timing_for`]); a file without `#NOTEDATA` errors. The decoder returns the first playable chart; the library exposes all charts.
- **Notes**: `1`, `L` => Tap; `2`..`3` => Hold; `4`..`3` => Burst (roll); `M` => Mine; `F`/`K` => not played.
- **Write** (`SscEncoder`): `#VERSION:0.83`, header (same as `.sm` encoder), `#BPMS`, a single `#NOTEDATA` with `#STEPSTYPE` by column count (**4 dance-single, 5 pump-single, 6 dance-solo, 7 kb7-single, 8 dance-double; any other count is an error**), `#DESCRIPTION` = difficulty name, `#DIFFICULTY`, `#METER`, `#CREDIT`, then `#NOTES` on the 1/48-beat grid. No stops/warps/per-chart timing are written.

## Parsers & tools

- StepMania C++: [NotesLoaderSSC.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSSC.cpp), [NotesWriterSSC.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterSSC.cpp), [TimingData.cpp](https://github.com/stepmania/stepmania/blob/master/src/TimingData.cpp), [Song.h](https://github.com/stepmania/stepmania/blob/5_1-new/src/Song.h), [Steps.h](https://github.com/stepmania/stepmania/blob/5_1-new/src/Steps.h).
- Etterna: [etternagame/etterna](https://github.com/etternagame/etterna) (C++). ITGmania: [itgmania/itgmania](https://github.com/itgmania/itgmania) (C++). OutFox: [TeamRizu/OutFox](https://github.com/TeamRizu/OutFox) (C++, closed core; binary releases).
- [Anders429/simfile](https://github.com/Anders429/simfile) (Rust), [simfile](https://docs.simfile.dev/) (Python), [ssc-parser](https://www.npmjs.com/package/ssc-parser) (JS PEG), [raindrop](https://github.com/zardoru/raindrop) `NoteLoaderSM` (C++, SSC with warps; "no keysounds or delays"), [PerryAsleep/StepManiaLibrary](https://github.com/PerryAsleep/StepManiaLibrary) (C#), [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (Rust, SSC<->SSQ), [PerryAsleep/StepManiaChartGenerator](https://github.com/PerryAsleep/StepManiaChartGenerator) (C#).
- Editors: StepMania 5 editor, [ArrowVortex](https://arrowvortex.ddrnl.com/), [Stependous](https://stependous.sourceforge.net/).

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
