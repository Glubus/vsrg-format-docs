# StepMania AMX simfile (`.sma`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text

## Overview

`.sma` is the simfile format of StepMania AMX, a Pump-It-Up-oriented StepMania 3.9 fork. It is an `.sm` superset (same MSD syntax, `#NOTES:` six-parameter chart tag and note characters) with row-based time values, per-chart timing after each `#NOTES`, and Pump tags (`#SPEED`, `#MULTIPLIER`, `#TICKCOUNT`, `#BEATSPERMEASURE`). No formal specification exists: this page reads the only open implementation, StepMania's `NotesLoaderSMA.cpp` (Aldo Fregoso, Jason Felds, 2009-2011), plus the community description ("sma is a middle ground between .sm and .ssc", "allows to use ROW for time, ... no other format uses this convention"). No writer exists in the StepMania tree.

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

- Beats or rows: BPM/stop/delay/tickcount/speed/multiplier/fake entries are `position=value`. A position ending in `r` or `R` is a **row index** and is divided by `#ROWSPERBEAT` (`RowToBeat`: `value / rowsPerBeat`); without the suffix it is a beat (float) as in `.sm`. The community description: "sma allows to use ROW for time, which is quite annoying because no other format uses this convention".
- BPMs and stops use the `.sm` rules including negative-value warps (`ProcessBPMsAndStops`), then are added to the current chart's timing.
- `#SPEED` (`ProcessSpeeds`): `position=ratio=length[S]` (a trailing `S`/`s` on the length means seconds, otherwise beats); a 2-value entry gets default length `0` for the first entry and `4` for the later ones ("4 is the default value in SMA, although SM5 requires 0 for the first segment"). Maps to SM5 speed segments.
- `#MULTIPLIER`: `position=hit[=miss...]` -> SM5 combo segments; "SMA files can use 6 values after the row/beat" (entries of size 2 or 4 use the hit value for misses).
- `#BEATSPERMEASURE` -> time-signature numerators (affects the measure lines only).
- `#OFFSET`: sign as `.sm` (beat 0 at `-offset` s).
- Conversion of a position to time: as `.sm`/`.ssc` after resolving rows to beats.

## Notes

Chart data as `.sm` ([notes grammar](../../stepmania/sm/README.md#notes)): `0 1 2 3 4 M L F K`, `[n]` keysounds, measures separated by commas. Step types are whatever `#NOTES` names (Pump `pump-single` 5, `pump-halfdouble` 6, `pump-double` 10, `pump-couple` 10, and the dance types; see [step types](../../stepmania/README.md#step-types-and-column-counts)). The wiki lists SMA for both `dance` and `pump` game modes.

## Audio & images

As `.sm`: `#MUSIC`, `#BANNER`, `#BACKGROUND`, `#CDTITLE`, `#KEYSOUNDS`, `#PREVIEW`/`#SAMPLESTART`.

## Versions & variants

`#SMAVERSION` appears in files but StepMania's loader ignores it. This page describes the loader as merged into StepMania 5 (`5_1-new`/master); AMX's own engine may support more [unknown].

## Quirks & pitfalls

- Positions may be rows (`123r`) or beats; `#ROWSPERBEAT` means definition on first occurrence, trigger on later ones.
- Timing tags after a `#NOTES` belong to that chart; a parser treating them as song tags mixes charts.
- `#SPEED` default lengths differ from SM5's.
- `.sma` shadows `.sm` in StepMania's folder loader.
- The loader ends with `TidyUpData`; no per-version handling.
- Few third-party editors/converters know the format; some songs "can't be converted correctly to .ssc".

## Example

No real `.sma` file was found. Structure implied by the loader (illustrative, hand-built from the handler table above):

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

Not read by ROX (no `.sma` in [src/formats/auto/detect.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/auto/detect.rs)). A decoder could reuse the `.sm` pipeline after resolving `r` positions and chart-level timing.

## Parsers & tools

- StepMania [NotesLoaderSMA.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp) (C++; no `.sma` writer exists in the repository); Etterna `NotesLoaderSMA.cpp`; OutFox (pump mode lists `.sma`).
- StepMania AMX itself (https://github.com/StepMania-AMX, binaries and tutorials on stepmania.amx.io).

## Getting samples

No `.sma` committed: none found. Searched 2026-11-09: StepMania-AMX repositories (StepMania-AMX/StepMania-AMX at commit `6423c41f8c0efe79599e1004a5171a22ba61b910`: only `Courses/Samples/*.crs` and `Themes/default/Other/ScreenHowToPlay steps.sm`; ssc2sma.amx.io: TypeScript loaders, no fixtures); AMX builds on https://download.stepmania.amx.io/ (`3.9+_final-WIN.zip`, `SMA-Touch-Beta5.9.2`, `SMA-Beta3.1.7z`, `SMA-Beta5.9.2-20140524.7z`: themes, courses and `.sm` how-to-play steps, no `.sma`/songs); archive.org (no AMX item); PIU-Simfiles forks (`.ssc`). No hand-written file: the row/beat and `#ROWSPERBEAT` trigger semantics are too loosely specified to validate one.

How to get one: convert any `.ssc` with the AMX web converter ssc2sma.amx.io (source https://github.com/StepMania-AMX/ssc2sma.amx.io; "Step converter from .ssc to .sma; supports StepMania 5 (Official), PIU Infinity, StepF2" per the organisation page), e.g. a committed `../../stepmania/ssc/samples/*Springtime*` pump chart; or install StepMania AMX and look for `.sma` in song folders of AMX-targeted packs.

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp, NotesLoaderSMA.h, NotesLoader.cpp
- https://stepmania.fandom.com/wiki/Step_formats (SM vs SMA section)
- https://github.com/stepmania/stepmania/issues/1125 (".sma file support", cited by the wiki)
- https://github.com/StepMania-AMX
- https://github.com/stepmania/stepmania/wiki/Supported-Game-Modes (SMA listed for dance and pump)
