# StepMania family (StepMania 3.x/4/5, Etterna, ITG, NotITG, ITGmania, Project OutFox)

Category: vsrg: notes scroll vertically along a fixed set of columns (arrow panels/keys) toward a receptor row; a chart is a column count plus taps/holds/mines at beat positions.

## What it is

StepMania is the open-source dance-game engine (Chris Danford, 2001-; a Dance Dance Revolution simulator). Its simfile formats are the lingua franca of the dance/VSRG-keyboard community. This folder documents the simfile family; sibling folders document formats StepMania imports.

| Engine / fork | What it is | Chart files it reads |
|---|---|---|
| StepMania 3.x (3.0, 3.9, 3.95 "CVS") | DDR simulator; introduced `.sm` (3.0) | `.sm`, `.dwi`, `.ksf`, `.bms`, `.msd`-era |
| StepMania 4.0 alpha/beta | experimental branch (shelved) | `.sm` + new tags |
| sm-ssc | fork of the SM4 alpha, introduced `.ssc`, warps, fakes, per-chart timing, rolls, lifts | `.sm`, `.ssc` |
| StepMania 5.0 / 5.1 / 5.2 (master) | merge of sm-ssc into mainline | `.ssc`, `.sm`, `.dwi`, `.ksf`, `.sma`, `.bms/.pms`, `.json` (see below) |
| Etterna | 5.0-based fork for keyboard players (online score site, MSD difficulty calc) | `.sm`, `.ssc`, `.dwi`, `.ksf`, `.sma`, `.bms`, `.osu` (loaders in `src/Etterna/Models/NoteLoaders`) |
| In The Groove / OpenITG / NotITG | arcade game + OpenITG (fork of SM "3.95"), NotITG = OpenITG with mod-scripting | `.sm` (mods through `#FGCHANGES`/`#BGCHANGES` XML/Lua) |
| ITGmania | fork of SM 5.1; adds ITG-theme features, chart hashing for GrooveStats | `.sm`, `.ssc` |
| Project OutFox | multi-game engine derived from SM 5.3 | `.sm`, `.ssc`, `.dwi`, `.ksf`, `.sma`, `.bms` family, `.osu`, `.qua`, `.tja`, `.chart`, `.mid`, `.dtx`, `.gda`, `.mc`, ... |
| StepMania AMX | SM 3.9 fork for Pump It Up, `.sma` | see [../stepmania-amx](../stepmania-amx/README.md) |
| StepF2 / StepP1 | Pump It Up forks of SM5 (note syntax `{note|attr|fake|reserved}`) | `.ssc` with `#VERSION:0.81` |
| Pump It Up Pro / Infinity | official Andamiro titles built on StepMania | `.sm`/`.ssc`-style |

Fork notes (checked against sources): Etterna adds no authored chart extension; it writes derived `#CHARTKEY`/`#MSDVALUES` tags, an unused `.ett` writer and binary `<chartkey>.cache` files, see [`../etterna`](../etterna/README.md). ITGmania (commit `8a3bf8884acdcb69363f7f0ea592138e398c71e4`) loads `.ssc .sm .sma .dwi .json` and courses (`.crs`), and writes `.sm .ssc .dwi .json`: no distinct extension. Project OutFox is closed source (its public repository is a bug tracker), so its extension list is unverified; its community pack uses `.ssc` with extra step types.

Format documents in this repo:

- [`sm`](sm/README.md): the `.sm` simfile (3.x/4/5; basis of everything).
- [`ssc`](ssc/README.md): StepMania 5 `.ssc` (per-chart timing).
- [`edit`](edit/README.md): `.edit` single-chart fragments.
- Etterna extras: [`../etterna`](../etterna/README.md) ([`ett`](../etterna/ett/README.md)).
- Imports: [`../dwi`](../dwi/README.md), [`../kick-it-up`](../kick-it-up/README.md), [`../stepmania-amx`](../stepmania-amx/README.md), [`../pydance`](../pydance/README.md), [`../stepmania-micro`](../stepmania-micro/README.md), [`../ddr`](../ddr/README.md) (`.msd`, `.sdf`, `.ssq`), [`../pump-it-up`](../pump-it-up/README.md), [`../legacy-dance-formats`](../legacy-dance-formats/README.md).

## `.sm` vs `.ssc` at a glance

| | `.sm` | `.ssc` |
|---|---|---|
| Chart container | `#NOTES:a:b:c:d:e:data;` (6 params) | `#NOTEDATA:;` + named chart tags + `#NOTES:data;` |
| Chart metadata | stepstype, description, difficulty, meter, radar | + `#CHARTNAME #CHARTSTYLE #CREDIT #MUSIC #DISPLAYBPM` |
| Timing | song-wide only: `#OFFSET #BPMS #STOPS #DELAYS #TIMESIGNATURES #TICKCOUNTS` | + `#WARPS #FAKES #SPEEDS #SCROLLS #COMBOS #LABELS`, all overridable per chart |
| Warps | encoded as negative stops/BPMs | real `#WARPS:beat=length` |
| Version tag | none | `#VERSION:0.83` |
| Extra song tags | | `#ORIGIN #PREVIEWVID #JACKET #CDIMAGE #DISCIMAGE #PREVIEW #LASTSECONDHINT` |
| Note characters | `0 1 2 3 4 M` + `L F K` | identical |
| Keysound chart tag | `#NOTES2` when keysounds | same |

Common to both: UTF-8 text, `#TAG:value;`, `//` comments, `\` escapes, beats as floats, 48 rows/beat (192 rows per 4-beat measure; `BEATS_PER_MEASURE = 4`), measures separated by `,`, one column character per row.

### `#OFFSET` sign

`#OFFSET` (seconds) is the negative of the audio position of beat 0: beat 0 plays at `-offset` s into the music. `#OFFSET:-0.149` (typical, positive audio lead-in) => first beat 149 ms after audio start. The sign is opposite to DWI `#GAP` (ms, positive = delay), KSF `#STARTTIME` (centiseconds, positive = delay), pydance `gap`, and SSQ `tempo_data[0]` (positive = chart delayed; `tempo_data[0] = -#OFFSET x TPS`).

### Step types and column counts

From `GameManager.cpp` (StepMania master, `g_StepsTypeInfos`); `#STEPSTYPE` / the first `#NOTES` parameter is the name:

| Step type | Columns | Layout / use |
|---|---|---|
| `dance-single` | 4 | L D U R |
| `dance-double` | 8 | two pads, P1 L D U R + P2 L D U R |
| `dance-couple` | 8 | two players with different steps |
| `dance-solo` | 6 | L UL D U UR R |
| `dance-threepanel` | 3 | UL D UR |
| `dance-routine` | 8 | two players, one shared double-width field; parts separated by `&` |
| `pump-single` | 5 | DL UL C UR DR |
| `pump-halfdouble` | 6 | the middle 6 panels of a double |
| `pump-double` | 10 | two pump pads |
| `pump-couple` | 10 | two players, different steps |
| `pump-routine` | 10 | co-op, `&` parts (PIU "Double Performance/Co-op") |
| `kb7-single` | 7 | keyboard 7K (`SDF space JKL`) |
| `ez2-single` / `ez2-double` / `ez2-real` | 5 / 10 / 7 | EZ2Dancer |
| `para-single` | 5 | Para Para Paradise |
| `ds3ddx-single` | 8 | Dancing Stage 3DDX |
| `bm-single5` / `bm-versus5` / `bm-double5` | 6 / 6 / 12 | beatmania 5-key (+scratch) |
| `bm-single7` / `bm-versus7` / `bm-double7` | 8 / 8 / 16 | beatmania 7-key (+scratch) |
| `maniax-single` / `maniax-double` | 4 / 8 | DDR Maniax |
| `techno-single4/5/8`, `techno-double4/5/8` | 4/5/8, 8/10/16 | Dance Techno (9-panel pad) |
| `pnm-five` / `pnm-nine` | 5 / 9 | pop'n music |
| `lights-cabinet` | (cabinet lights) | not playable |
| `kickbox-human` / `-quadarm` / `-insect` / `-arachnid` | 4 / 4 / 6 / 8 | kickbox (incomplete, see wiki) |

OutFox adds game types (`groove`, `smx` 3k/5k, `stepstage` 6k/3k, `beat`, `pop`, ...) absent from stock StepMania ([projectoutfox.com](https://projectoutfox.com/), Steam page). Also seen in the wild: `ez2-single-hard` (rewritten to `ez2-single` by the loader), `para` (=> `para-single`), `smx-*`.

### Note characters

`0` empty, `1` tap, `2` hold head, `3` hold/roll tail, `4` roll head, `M` mine, `L` lift, `F` fake, `K` auto-keysound, `A{mods:sec}` attack note (written, not read), `N` minefield head (commented out), optional `[n]` keysound index suffix. StepF2 (pump) braces `{note|attr|fake|reserved}` with `P1..P4` tap chars `X/Y/Z` and attributes `v s h` are not StepMania. Details in [`sm`](sm/README.md#notes).

### Timing tags in one table

`#BPMS beat=bpm` · `#STOPS beat=sec` (freeze after the beat) · `#DELAYS beat=sec` (freeze before) · `#WARPS beat=lengthBeats` · `#TIMESIGNATURES beat=num=den` (display only) · `#TICKCOUNTS beat=ticks` · `#COMBOS beat=combo[=miss]` · `#SPEEDS beat=ratio=length=unit` (unit 0 beats/1 seconds) · `#SCROLLS beat=ratio` · `#FAKES beat=lengthBeats` · `#LABELS beat=text` · `#ATTACKS TIME=..:LEN=..:MODS=..`. Semantics in [`ssc`](ssc/README.md#timing-model).

### BGCHANGES / FGCHANGES

Both are comma lists of `beat=file=rate=transition=effectFlag1=effectFlag2=effectFile=file2=transitionFile=color1=color2` (1-11 fields; see the [`.sm` structure table](sm/README.md#structure--metadata)). `#BGCHANGES2`, `#BGCHANGES3`.. are extra layers. Stock StepMania refuses `.ini`/`.xml` entries unless quirks mode is on; NotITG/OpenITG use them to load Lua/XML mods: `#FGCHANGES:0.000=lua=1.000=0=0=1=====;` includes `lua/default.xml` at beat 0 ([Lua API for OpenITG/NotITG](https://sm.heysora.net/doc/), [XeroOl/xero-mod-loader](https://github.com/XeroOl/xero-mod-loader)). `-nosongbg-` entries stop StepMania appending the song background.

## Dialect notes

- ITG / OpenITG / NotITG: `.sm`. Difficulty slots are labelled Novice/Easy/Medium/Hard/Expert (internally `Beginner/Easy/Medium/Hard/Challenge`). Mines (`M`) and negative BPM/stop gimmicks are common; NotITG mod charts use `#FGCHANGES`/`#BGCHANGES` XML+Lua and `#ATTACKS`.
- Etterna: SM5 tag set (loaders keep the `ProcessBPMsAndStops` negative-value conversion) and SM step types. `NotesWriterETT.cpp` writes an SSC-layout cache with extra chart tags `#CHARTKEY` and `#MSDVALUES` (the SSC loader reads both). Chart key = `"X" + SHA1(per non-empty row: note type of every column + integer BPM)` (`Steps::GenerateChartKey`). The song cache is a `cache.db` SQLite file (`SongCacheIndex.cpp`). `NotesLoaderETT.h` is an empty stub. Etterna also loads `.osu` (`NotesLoaderOSU.cpp`).
- ITGmania: adds statistics tags to the ssc cache loader (`#TECHCOUNTS`, `#NPSPERMEASURE`, ... `#GROOVESTATSHASH`).
- <a id="grooveStats-chart-hash"></a>GrooveStats chart hash (ITGmania `Steps::CalculateGrooveStatsHash`, hash version 3): take the chart in canonical SM text (`GetSMNoteDataString`), minimize each measure by repeatedly dropping every second line while those lines are all `0`, join measures with `\n,\n`; append the BPM list as `normalize(beat)=normalize(bpm)` joined by `,`; SHA-1; the first 16 hex chars are the key. BPM text is hashed, so 150.01 and 150.00 BPM are different charts. It is a score-site identity, not a file format.
- Project OutFox: dedicated parsers for third-party formats (`QUA`, `OTO` for taiko-from-osu, `NotesLoaderPIU` for StepF2 `.ssc`), `.zip` bundles for modcharts (OutFox Serenity guidelines), many `STEPSTYPE`s. Loaders are closed; behaviour comes from release notes.
- StepMania AMX / DirectMove: [stepmania-amx](../stepmania-amx/README.md), [kick-it-up](../kick-it-up/README.md).
- PIU/DDR custom charts converted by [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (SSC <-> SSQ).

## Other StepMania file types (no folder of their own)

| File | What it is | Source |
|---|---|---|
| `.crs` | Course definition: `#COURSE:`, `#SCRIPTER`, `#METER:Difficulty:n`, `#REPEAT`, `#LIVES`, `#GAINSECONDS`, `#MODS`, and `#SONG:Group/Song:Difficulty:mods;` lines (DWI has its own CRS flavour with `BESTx/WORSTx/*` songs). Not a chart. | [wiki Courses](https://github.com/stepmania/stepmania/wiki/Courses), [DWI.txt §5](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt) |
| `.lrc` | lyrics (`[mm:ss.ss]text`, `[offset:ms]`, `[COLOUR]`) referenced by `#LYRICSPATH` | [wiki lrc](https://github.com/stepmania/stepmania/wiki/lrc), DWI.txt §6 |
| `.smzip` | ZIP-based package. The wiki's `SMPackage` page (a proposal, "likely for StepMania 5.2") describes ZIP files whose folders (`Songs/<Group>/`, noteskins, themes...) "correspond to content type ... similarly to SMZip files", with a JSON `smpackage` manifest. Not a chart | [wiki SMPackage](https://github.com/stepmania/stepmania/wiki/SMPackage); the FFR simfile database also accepts `.smzip` uploads |
| `.edit` | single-chart edit, see [`edit`](edit/README.md) | |
| `.ats` | autosave of an `.sm`/`.ssc` (loader `GetApplicableFiles(load_autosave)`) | `NotesLoaderSM.cpp` |
| `.json` | StepMania's own JSON song/steps (de)serializer = "StepMania Micro" data, see [stepmania-micro](../stepmania-micro/README.md) | `NotesLoaderJson.cpp` |
| `Cache/Songs/*` | binary-free cache files in `.ssc` syntax (`// cache tags:` block, `#STEPFILENAME` instead of `#NOTES`) | `NotesWriterSSC.cpp` |

`.sm5` is not a file type in the StepMania sources consulted (SM5 uses `.ssc`).

## ROX support (family summary)

ROX 0.8.1 reads and writes `.sm` and `.ssc` ([ROX source: src/formats/sm/](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/sm/)). `.dwi` and `.ksf` are decode only (`rox::formats::dwi`, `rox::formats::ksf`, see [dwi](../dwi/dwi/README.md#rox-support), [ksf](../kick-it-up/ksf/README.md#rox-support)). The rest of this family (`.sma`, `.edit`, `.json`, `.ssq`, `.ucs`, ...) is not read. Per-format details: [sm](sm/README.md#rox-support), [ssc](ssc/README.md#rox-support).

- Supported: step types `dance-single/solo/double`, `pump-single/halfdouble`, `kb7-single` (others skipped), stops, delays, warps, fakes, BPM changes, offset (baked into note times), mines, holds, rolls (as bursts), lifts (as taps).
- Not supported: `#SPEEDS`, `#SCROLLS`, `#COMBOS`, `#TICKCOUNTS`, `#LABELS`, `#TIMESIGNATURES` (as a time signature), `#ATTACKS`, keysounds, BGChanges, `dance-couple/routine`, `pump-double`, `techno-*`, `bm-*`, `ez2-*`.

## Parsers & tools (family)

- [stepmania/stepmania](https://github.com/stepmania/stepmania) (C++), [etternagame/etterna](https://github.com/etternagame/etterna) (C++), [itgmania/itgmania](https://github.com/itgmania/itgmania) (C++), [TeamRizu/OutFox](https://github.com/TeamRizu/OutFox) (releases only), [zardoru/raindrop](https://github.com/zardoru/raindrop) (C++ VSRG engine loading `.sm/.ssc`), [Anders429/msd](https://github.com/Anders429/msd) + [Anders429/simfile](https://github.com/Anders429/simfile) (Rust), [simfile](https://docs.simfile.dev/) (Python), [ssc-parser](https://www.npmjs.com/package/ssc-parser) (JS), [PerryAsleep/StepManiaLibrary](https://github.com/PerryAsleep/StepManiaLibrary) (C#), [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (Rust), [XeroOl/mirin-template](https://github.com/XeroOl/notitg-mirin) (NotITG Lua).

## Sources

- https://github.com/stepmania/stepmania/tree/master/Docs/SimfileFormats (README, misc.txt, ssc_msd5.txt, new format draft.txt)
- https://github.com/stepmania/stepmania/wiki (File-Formats/sm, ssc, Timing-Segments, Note-Types, Supported-Game-Modes, Versions, Courses, SMPackage, Note-and-timing-gimmicks)
- StepMania source (`src/`): NotesLoaderSM/SSC/SMA/DWI/KSF/Json, NotesWriterSM/SSC, MsdFile, NoteDataUtil, NoteTypes.h, GameManager.cpp, TimingData.cpp, Song.cpp
- https://github.com/etternagame/etterna, https://github.com/itgmania/itgmania (Steps.cpp `CalculateGrooveStatsHash`), https://projectoutfox.com/news/project-outfox-04151-released, https://stepmania.fandom.com/wiki/Step_formats, https://sm.heysora.net/doc/
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt (CRS/LRC)
- ROX source: `rhythm-open-exchange/src/formats/sm/`

Added format pages: [`crs/`](crs/README.md) (`.crs` course files).
