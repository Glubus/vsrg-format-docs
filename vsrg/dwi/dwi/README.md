# Dance With Intensity step file (`.dwi`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (ASCII/UTF-8/Latin-1, no declaration)

## Overview

`.dwi` is the step-file format of the DDR simulator Dance With Intensity (SimWolf, 2000-). It is an MSD derivative: `#TAG:param:param;` tags, but with new tags (`#FREEZE`, `#CHANGEBPM`, `#BACKGROUND` scripts...) and a compact, notorious **step-string notation** in which every character encodes the panels pressed in an 8th-note slot. One `.dwi` holds the metadata and **all charts of a song** (single/double/couple/solo, up to four difficulties each) because it is one file per song folder. It is the most common pre-`.sm` format and is read by StepMania (all versions up to 5.x/Etterna/OutFox), pydance and Raindrop-style engines. Official text: the DWI readme section "4. DWI FILE FORMAT", mirrored in StepMania's [`Docs/SimfileFormats/DWI/DWI.txt`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt).

## Container & encoding

- Plain text, one `.dwi` per song folder (StepMania refuses a folder with more than one: "has more than one DWI file. There should be only one!"). Audio, banner and background are separate files in the folder.
- MSD tokenizer (`#NAME:param:param;`, `//` comments), **without** backslash unescaping (`MsdFile::ReadFile(path, false)`), so a literal `\` is kept. `:` is a parameter separator also inside step data (it separates the two pads of doubles), and `#` ends an unterminated value when it starts a line.
- Encoding is undeclared ("no encoding information" per pydance's authors); StepMania converts titles/artist/genre with `ConvertString(.., "utf-8,english")`, i.e. UTF-8 with a Latin-1-like fallback.

## Structure / metadata

| Tag | Value | Notes |
|---|---|---|
| `#TITLE` | `Title` or `Title - subtitle` | StepMania splits main/sub title at the first of `\t`, ` -`, ` ~`, ` (`, ` [` (`NotesLoader::GetMainAndSubTitlesFromFullTitle`) |
| `#ARTIST` | text | |
| `#GAP` | integer **milliseconds** | time before beat 0 starts counting: `offset_sm = -GAP/1000` (DWI's GAP is "calculated differently" from MSD sims, per the readme) |
| `#BPM` | float | the starting BPM (must be > 0) |
| `#DISPLAYTITLE` `#DISPLAYARTIST` | text with `{file.png}` special-character images (50 px high, black&white, baseline 34 px) | StepMania only blacklists the image names |
| `#DISPLAYBPM` | `*` (random) / `a` / `a..b` | display only |
| `#FILE` | audio path | if missing, a `.wav`/`.mp3` in the folder is used |
| `#MD5` | MD5 of the music | consistency check |
| `#FREEZE` | `BBB=sss,BBB=sss` | at "beat" BBB freeze the arrows for sss **milliseconds** (StepMania: `row = beat/4` converts DWI's counter to SM beats: **divide by 4**) |
| `#CHANGEBPM` (alias `#BPMCHANGE`) | `BBB=nnn,...` | at beat BBB the BPM becomes nnn (also divided by 4 by StepMania) |
| `#STATUS` | `NEW` / `NORMAL` | song-select badge |
| `#GENRE` | text, comma separated | |
| `#CDTITLE` | image path | 64x40 CD logo, top-left pixel transparent |
| `#SAMPLESTART` | ms (`5230`), seconds (`5.23`), or `m:ss.ss`; `+` prefix = add GAP | preview start |
| `#SAMPLELENGTH` | same units | preview length (StepMania multiplies a value in (0,1) by 1000 as some versions stored seconds in thousands) |
| `#RANDSEED` `#RANDSTART` `#RANDFOLDER` `#RANDLIST` | background-animation randomizer | ignored by StepMania |
| `#BACKGROUND` | multi-line script `... SCRIPT: ... #END;`; effect letters with `FILE: MOVIE: VIS: OFF LAYER: STARTAT: MULT: ANIMATE: MOVE: SPACING: SIZE: KEEPPOS KEEPTIME` | background-animation scripting (movies, Sonique visualizations, layered image effects); not read by StepMania |
| `#SINGLE` `#DOUBLE` `#COUPLE` `#SOLO` | chart: `#STYLE:DIFFICULTY:RATING:steps[:steps2]` | see below |

### Chart tag

```
#SINGLE:BASIC:5:<steps>;
#DOUBLE:ANOTHER:9:<steps pad 1>:<steps pad 2>;
```

- Style: `SINGLE` (4 panels), `DOUBLE` (8 = two pads), `COUPLE` (8, battle/two players with different steps), `SOLO` (6 panels).
- Difficulty: `BASIC`, `ANOTHER`, `MANIAC`, `SMANIAC` (DWI); StepMania also accepts `BEGINNER`, `LIGHT`, `TRICK`, `STANDARD`, `DIFFICULT`, `HEAVY`, `SSR`, `EXPERT`, `ONI`, `CHALLENGE`, `EDIT` and maps them to Easy (basic/light), Medium (another/trick/standard/difficult), Hard (maniac/heavy/ssr), Challenge (smaniac/challenge/expert/oni) (`DwiCompatibleStringToDifficulty`).
- Rating: integer feet ("1 or higher"; empty => 1).
- For `DOUBLE`/`COUPLE`: the left pad's steps first, then `:`, then the right pad's.
- A song folder normally has one `#SINGLE`, `#DOUBLE`, ... per difficulty.

### Courses and lyrics (companions)

`.crs` (DWI Nonstop courses: `#COURSE`, `#DISPLAYCOURSE`, `#SONG:BEST1:BASIC;` / `#SONG:*:5..7;` / `#SONG:folder\Title:MANIAC:2.0x,LEFT;`, `#REPEAT`, `#COMBO:PERFECT`, `#COMBOMODE`, `#LIVES`) and `.lrc` lyrics (`[MM:SS.ss]text`, `[offset:ms]`, `[COLOUR]0xffff00`, `{c0}`..`{c9}`, `|` = line break) have their own small grammars described in the readme sections 5-6 ([DWI.txt](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt)).

## Timing model

- `time(beat 0) = GAP ms` into the audio (positive GAP delays the chart; **opposite sign of `.sm #OFFSET`**, see [`.sm`](../../stepmania/sm/README.md#timing-model)).
- Positions come from the **order of characters**, not from explicit beats: the cursor starts at 0 and advances after each note character by the current increment. A measure is 4 beats ("All DWI files use 4 beats per measure"). Default increment: **one character = 1/8 of a measure = 0.5 beat** (an 8th note).
- Brackets change the increment for the characters inside them:

| Open / close | Increment | StepMania beats per char |
|---|---|---|
| (default) | 1/8 measure | 0.5 |
| `(` ... `)` | 1/16 measure | 0.25 |
| `[` ... `]` | 1/24 measure | 1/6 |
| `{` ... `}` | 1/64 measure | 1/16 |
| `` ` `` ... `'` | 1/192 measure | 1/48 |

  Any closing character (`)` `]` `}` `'` `>`) resets to 1/8. Because the reset happens at *any* closer, `(` blocks cannot nest.
- `0` is an empty slot (still advances time). The `<...>` form groups notes that share one slot (a jump/hand); it does **not** advance time per inner character.
- `#BPM` is the BPM at beat 0; `#CHANGEBPM` and `#FREEZE` add changes; positions in these tags use DWI's own counter (divide by 4 for SM beats, see the table above). `#FREEZE` values are **milliseconds** (StepMania: `/1000`).
- Time of a note: standard beat/BPM/stop integration plus `-GAP`.

## Notes

Step characters (numeric-keypad layout) for the 4-panel styles:

```
 7 = U+L    8 = U    9 = U+R
 4 = L               6 = R
 1 = D+L    2 = D    3 = D+R         A = U+D      B = L+R      0 = none
```

(Digit `5` is also accepted and means "no step".) Solo (6-panel) adds `C`..`M`:

| Char | Panels | Char | Panels |
|---|---|---|---|
| `C` | Up-Left | `I` | Left + Up-Right |
| `D` | Up-Right | `J` | Down + Up-Right |
| `E` | Left + Up-Left | `K` | Up + Up-Right |
| `F` | Up-Left + Down | `L` | Up-Right + Right |
| `G` | Up-Left + Up | `M` | Up-Left + Up-Right |
| `H` | Up-Left + Right | | |

(From `NotesLoaderDWI.cpp` `DWIcharToNote`; the readme draws the same table.)

- **Jumps/hands** of 3+ panels: `<...>` joins codes; `<MB>` (= UL+UR+L+R), `<LE>`, `<IH>`, `<46M>` are equivalent spellings. Old DWI versions used `<...>` as a 1/192 marker; StepMania guesses (`Is192`): if a `0` appears before the next `>` it is a 192nd marker, otherwise a jump.
- **Holds (freeze arrows)**: `!` means `<show>!<hold>`: `8!8` starts an Up hold; the arrow is released the next time the program meets an Up arrow "by itself or combined with another arrow". `7!4`: U+L shown, only L held. In StepMania's loader the hold head is set on the column(s) of the char after `!`; the tail is the next non-empty tap in that column, which is consumed (so every hold must be closed by a repeated arrow; an unclosed hold is dropped with a log: "failed to close a hold note").
- **Doubles/couples**: two step strings separated by `:`, each string uses the 4-panel codes for its pad (pad 2 columns are columns 4..7); both strings are timed independently from beat 0.
- No mines, rolls, lifts or fakes in the format (StepMania's writer skips mines).
- Whitespace/newlines/tabs inside the string are ignored.

## Audio & images

`#FILE` names the audio (relative or absolute path; `/music/mysongs/abc.mp3` in the readme example); `#MD5` guards it. Banner/background are **auto-detected** by StepMania from file names in the folder (not tags); `#CDTITLE` is explicit; `#DISPLAYTITLE`/`#DISPLAYARTIST` can reference small `.png` glyph images. `#BACKGROUND ... SCRIPT:` references images, AVI movies and SVP visualizations with layers. No keysounds.

## Versions & variants

- Versions: DWI 1.0 (Dec 2000), 1.50 (Feb 2002), 2.0 (Jul 2002; courses, groove radar), 2.50.00.
- `<...>` changed meaning between versions (1/192nd marker -> jump), `` `...' `` became the 192nd marker; both exist in the wild.
- MSD files from other simulators load in DWI "with a change in the GAP value"; DWI does not support BMS.
- pydance reference of bad files: "BPM change at the beat `894.8.3`", `'...B!(60...'`, `'0!B'`, `'4!6'` ([dwi-hall-of-shame.txt](https://github.com/mbenkmann/pydance/blob/master/docs/dwi-hall-of-shame.txt)).

## Quirks & pitfalls

- Time is implicit: one wrong bracket shifts the rest of the song. Different parsers disagree on malformed strings.
- GAP is ms and positive-delay; `#FREEZE`/`#CHANGEBPM` positions are DWI-counter units (4 per SM beat) and freezes are ms.
- `!` followed by a different arrow than the one shown, `!B` after `0` ('0!B'), and a hold whose release char is missing are produced by old StepMania editor bugs.
- `:` appears both as parameter separator and as pad separator; `#` and `:` have "double meanings".
- Charset is unknown; Latin-1 titles occur.
- The loader maps `COUPLE` to `dance-couple`, `SOLO` to `dance-solo`; an unknown style name is an assertion failure in StepMania (`GetTypeFromMode`).
- DWI has no per-chart BPM or timing.

## Example

Hand-built, illustrative (from the rules above; not from a real file):

```
#TITLE:Example Song - demo;
#ARTIST:Someone;
#GAP:-300;
#BPM:150;
#FREEZE:96=500;
#CHANGEBPM:128=180;
#SINGLE:BASIC:4:2020(2424)8!8008060;
```

`2 0 2 0` are four 8th-note slots, `(2424)` four 16th-note slots, `8!8` an Up hold started in a 8th slot, `0 0 8` ... closes it when the next `8` appears.

## ROX support

Read by ROX since Prism's addition of `rox::formats::dwi` (decode only: ROX does not write DWI). `DwiDecoder::variants` lists every playable chart of the file (`#SINGLE` 4 columns, `#SOLO` 6, `#DOUBLE` 8), `decode_variant` / `decode_with_report` (`DwiReport`) decode one, `parse` gives the `.sm` types (`SmFile`) so BPM changes, freezes (as `.sm` stops) and the offset go through the one pipeline of the `.sm` reader; `-GAP` is baked into the times (`metadata.audio_offset_us` is 0), `#FILE` is `metadata.audio_file` as written. The note grammar, the `#GAP` (integer ms), `#CHANGEBPM`/`#FREEZE` (position divided by 4, freezes in ms) and hold rules are those of StepMania's `NotesLoaderDWI.cpp` (ported, MIT). `#COUPLE` charts are skipped with a message (two players' steps), as `dance-couple` is in `.sm`; `<..>` is a jump, or the old 1/192 marker when a `0` comes before the next `>`; a hold is released by the next arrow of its column. Not read: `#DISPLAYBPM`, `#DISPLAYTITLE`/`#DISPLAYARTIST`, `#GENRE`, `#CDTITLE`, `#MD5`, `#STATUS`, `#RAND*`, `#BACKGROUND` scripts, and the `+` prefix of `#SAMPLESTART`. Details: [ROX source: src/formats/dwi/mod.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/dwi/mod.rs).

Read by Prism (`docs/game.md` "Formats de danse"): one entry per playable chart; `#FILE` is reduced to its file name and looked for in the song's folder (any case), else the folder's first audio file, else the chart is listed without sound, marked as missing its audio, and played silent; a `.ssc` or `.sm` of the same folder shadows the `.dwi` (StepMania's loader order); the MP3 is timed like Etterna's reader plays it (StepMania's `RageSoundReader_MP3.cpp` keeps the `Info` frame as silence "to match DWI sync").

## Parsers & tools

- StepMania: [NotesLoaderDWI.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderDWI.cpp), [NotesWriterDWI.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterDWI.cpp) (C++; the writer emits `<...>`-free strings when possible and skips mines).
- pydance `DWIFile` ([fileparsers.py](https://github.com/mbenkmann/pydance/blob/master/fileparsers.py), Python); Etterna `NotesLoaderDWI.cpp`; OutFox (closed); [Stependous](https://stependous.sourceforge.net/) (DWI/DDR/StepMania converter/editor).
- DWI itself (closed source, Windows).

## Getting samples

Committed in [`samples/`](samples/SOURCES.md) (48 REAL files plus one synthetic; per-file origin/sha256 in `SOURCES.md`): the official sample song of DWI (`dwi-official_notmybattle.dwi`, extracted from `NotMyBattle.zip` on dwi.ddruk.com); the four DWI files bundled with StepMania 0.95 (`stepmania-0.95_*.dwi`, `#FILE` with Windows paths); 31 `.dwi` of the StepMix 1.0 pack (`stepmix-1.0/`); five from StepMania-Complete-disc packages (`stepmania-complete-disc/`); DDR 3rdMix/5thMix charts as DWI from noahm/simfile-parser (`ddr-*`), and a community `02 Ants.dwi` (`bhop-ball_`). They cover `#CHANGEBPM`, `#FREEZE`, `#SOLO/#COUPLE/#DOUBLE`, CRLF and LF files. `synthetic-demo.dwi` is hand-written (CC0) and does not count.

More: archive.org (searched 2026-11-09): `DWIExtremeT1`..`T9`, `DWIExtremeF1`..`F9`, `DWIExtremeS1`..`S9`, `DWIExtremeL4`, `DWIExtremeIV`, `dwi-extreme-all` (4.9 GB complete collection of the DWI Extreme song packs; each pack zip holds ~20 `.dwi` + mp3), `DWI-2-50-00` (DWI 2.50.00 and the sample song), `dance-with-intensity` (all DWI program releases: no songs). Also the `packs/3rdMix`, `packs/5thMix` folders of simfile-parser (38 and 40 `.dwi`). StepMania can also *write* `.dwi` (`NotesWriterDWI`).

## Sources

- http://dwi.ddruk.com/history.php (history), http://dwi.ddruk.com/readme.php#4 (format; text mirrored below)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderDWI.cpp, NotesWriterDWI.cpp, NotesLoader.cpp
- https://github.com/stepmania/stepmania/wiki/dwi
- https://github.com/mbenkmann/pydance/blob/master/docs/dwi-hall-of-shame.txt, fileparsers.py
- https://github.com/Anders429/msd (MSD origin)
