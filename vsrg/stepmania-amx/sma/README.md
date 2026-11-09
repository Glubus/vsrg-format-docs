# StepMania AMX simfile (`.sma`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text

## Overview

`.sma` is the simfile format of StepMania AMX, a Pump-It-Up-oriented fork of StepMania 3.9. It is an `.sm` superset (same MSD syntax, same `#NOTES:` six-parameter chart tag, same note characters) that adds **row-based time values**, **per-chart timing** after each `#NOTES`, and a few Pump-specific tags (`#SPEED`, `#MULTIPLIER`, `#TICKCOUNT`, `#BEATSPERMEASURE`). There is **no formal specification**: everything below comes from reading the only open implementation, StepMania's `NotesLoaderSMA.cpp` (authors Aldo Fregoso and Jason Felds, 2009-2011), and from the community description ("sma is a middle ground between .sm and .ssc", "allows to use ROW for time, ... no other format uses this convention"). No writer exists in the StepMania tree.

## Container & encoding

Text, MSD tokenizer with unescape (`MsdFile::ReadFile(path, true)`), same as [`.sm`](../../stepmania/sm/README.md#container--encoding). StepMania's loader priority in a song folder is `.ssc`, then `.sma`, then `.sm`, `.dwi`, `.bms`, `.ksf` (`NotesLoader::LoadFromDir`), so a folder with an `.sma` hides `.sm` files.

## Structure / metadata

Tags handled by `SMALoader::LoadFromSimfile` (case-insensitive):

| Tag | Handling |
|---|---|
| `#TITLE #SUBTITLE #ARTIST #TITLETRANSLIT #SUBTITLETRANSLIT #ARTISTTRANSLIT #GENRE #CREDIT #BANNER #BACKGROUND #LYRICSPATH #CDTITLE #MUSIC #INSTRUMENTTRACK` | as `.sm` |
| `#PREVIEW` | stored as the song's **preview video** file (`m_sPreviewVidFile`) |
| `#SAMPLESTART #SAMPLELENGTH #DISPLAYBPM #SELECTABLE #BGCHANGES* #ANIMATIONS #FGCHANGES #KEYSOUNDS #ATTACKS` | as `.sm` |
| `#SMAVERSION` | ignored |
| `#ROWSPERBEAT` | **first occurrence** sets the number of rows per beat used to interpret `…r` values (the code splits the value by `,` then `=` and reads the second field of the first entry, e.g. `0=48`); every **later occurrence** calls `ProcessBPMsAndStops` on the pending BPM/stop lists into the current timing: the source comment says the second appearance "delimits NoteData" [so presumably the tag is repeated around each chart; inference] |
| `#BEATSPERMEASURE` | `beat=numerator,...` -> time signature segments (numerator only) |
| `#OFFSET` | applied to the current chart's timing if a `#NOTES` was already read, else to the song timing |
| `#BPMS` `#STOPS`(`#FREEZES`) | collected in lists (values may be rows, see below), converted at the next `#ROWSPERBEAT`/`#NOTES` with the `.sm` negative-value warp rules |
| `#DELAYS` `#TICKCOUNT` `#SPEED` `#MULTIPLIER` `#FAKES` | go to chart timing if after a `#NOTES`, else song timing |
| `#METERTYPE` | ignored ("We don't use this...yet") |
| `#LISTSORT`, cache tags (`#FIRSTBEAT #LASTBEAT #SONGFILENAME #HASMUSIC #HASBANNER #MUSICBYTES #LASTBEATHINT #MUSICLENGTH`), `#TIMESIGNATURES`, `#LEADTRACK` | ignored |
| `#NOTES` / `#NOTES2` | six parameters as `.sm` (`stepstype:description:difficulty:meter:radar:notes`); creates a chart whose timing starts empty and is filled by the following tags |

## Timing model

- **Beats or rows**: BPM/stop/delay/tickcount/speed/multiplier/fake entries are `position=value`. A position ending in `r` or `R` is a **row index** and is divided by `#ROWSPERBEAT` (`RowToBeat`: `value / rowsPerBeat`); without the suffix it is a beat (float) as in `.sm`. The community description: "sma allows to use ROW for time, which is quite annoying because no other format uses this convention".
- BPMs and stops use the `.sm` rules including negative-value warps (`ProcessBPMsAndStops`), then are added to the current chart's timing.
- **`#SPEED`** (`ProcessSpeeds`): `position=ratio=length[S]` (a trailing `S`/`s` on the length means seconds, otherwise beats); a 2-value entry gets default length `0` for the first entry and `4` for the later ones ("4 is the default value in SMA, although SM5 requires 0 for the first segment"). Maps to SM5 speed segments.
- **`#MULTIPLIER`**: `position=hit[=miss...]` -> SM5 combo segments; "SMA files can use 6 values after the row/beat" (entries of size 2 or 4 use the hit value for misses).
- **`#BEATSPERMEASURE`** -> time-signature numerators (affects the measure lines only).
- `#OFFSET`: sign as `.sm` (beat 0 at `-offset` s).
- Conversion of a position to time: as `.sm`/`.ssc` after resolving rows to beats.

## Notes

Same chart data as `.sm` ([notes grammar](../../stepmania/sm/README.md#notes)): `0 1 2 3 4 M L F K`, `[n]` keysounds, measures separated by commas; step types are whatever `#NOTES` names (Pump `pump-single` 5, `pump-halfdouble` 6, `pump-double` 10, `pump-couple` 10, and the dance types; see [step types](../../stepmania/README.md#step-types-and-column-counts)). The wiki lists SMA as a chart format for both the `dance` and `pump` game modes.

## Audio & images

As `.sm`: `#MUSIC`, `#BANNER`, `#BACKGROUND`, `#CDTITLE`, `#KEYSOUNDS`; `#PREVIEW`/`#SAMPLESTART`.

## Versions & variants

`#SMAVERSION` exists in the files but is ignored by StepMania's loader. The behaviour described is that of the loader as merged into StepMania 5 (`5_1-new`/master); AMX's own engine may support more [unknown].

## Quirks & pitfalls

- Position values may be rows (`123r`) or beats; the meaning of `#ROWSPERBEAT` depends on its **order in the file** (first = definition, next = trigger).
- Timing tags **after** a `#NOTES` belong to that chart; a parser that treats them as song tags will mix charts.
- `#SPEED` default lengths differ from SM5's.
- `.sma` shadows `.sm` in StepMania's folder loader.
- The loader ends with `TidyUpData`; no per-version handling.
- Few third-party editors/converters know the format; some songs "can't be converted correctly to .ssc".

## Example

No real `.sma` file is vendored in this repo and none was retrieved. The structure implied by the loader (illustrative, hand-built from the handler table above, not a real file):

```
#SMAVERSION:1;
#TITLE:Example;
#ROWSPERBEAT:0=48;
#OFFSET:-0.05;
#BPMS:0r=150,2304r=170;
#STOPS:;
#NOTES:
     pump-single:
     NORMAL:
     Hard:
     10:
     0,0,0,0,0:
10000
00100
;
#ROWSPERBEAT:0=48;
```

## ROX support

Not read by ROX (no `.sma` in [ROX source: src/formats/auto/detect.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/auto/detect.rs)). Because the chart/notes layout is `.sm`, a decoder could reuse the ROX `.sm` pipeline after resolving `r` positions and chart-level timing.

## Parsers & tools

- StepMania [NotesLoaderSMA.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp) (C++; no `.sma` writer exists in the repository); Etterna `NotesLoaderSMA.cpp`; OutFox (pump mode lists `.sma`).
- StepMania AMX itself (https://github.com/StepMania-AMX, binaries and tutorials on stepmania.amx.io).

## Getting samples

No `.sma` file is committed or in the manifest: none was found in any repository checked (StepMania-AMX/StepMania-AMX at commit `6423c41f8c0efe79599e1004a5171a22ba61b910` ships `Courses/Samples/*.crs` and one `ScreenHowToPlay steps.sm` only; StepMania-AMX/ssc2sma.amx.io has TypeScript loaders `src/loaders/ssc`, `sma`, `sm` and no fixtures; StepMania, ITGmania, Etterna ship the loader but no sample). A hand-written file was not produced because the loader's row/beat and `#ROWSPERBEAT` trigger semantics are not specified well enough to validate one.

How to get one: (1) convert any `.ssc` with the AMX web converter ssc2sma.amx.io (source: https://github.com/StepMania-AMX/ssc2sma.amx.io; "Step converter from .ssc to .sma; supports StepMania 5 (Official), PIU Infinity, StepF2" per the organisation page) [the output format is the `.sma` of this page]; for example convert `../../stepmania/ssc/samples/Springtime.ssc` (pump-single charts) or the StepF2-style manifest file `piu-simfiles_308-Free-Style.ssc`; (2) install StepMania AMX (builds listed on the live index https://download.stepmania.amx.io/, 2.8 MB to 256 MB archives; the project site http://stepmania.amx.io) and look for `.sma` files in its song folders; the AMX forks of PIU simfile packs ([StepMania-AMX/PIU-Simfiles](https://github.com/StepMania-AMX/PIU-Simfiles)) are `.ssc`.

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp, NotesLoaderSMA.h, NotesLoader.cpp
- https://stepmania.fandom.com/wiki/Step_formats (SM vs SMA section)
- https://github.com/stepmania/stepmania/issues/1125 (".sma file support", cited by the wiki)
- https://github.com/StepMania-AMX
- https://github.com/stepmania/stepmania/wiki/Supported-Game-Modes (SMA listed for dance and pump)
