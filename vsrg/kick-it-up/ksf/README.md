# Kick It Up step file (`.ksf`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (CP949/KS C 5601 or EUC-KR, CRLF)

## Overview

`.ksf` is the chart format of the Kick It Up Pump-It-Up simulator ("the KSF format is designed for representing steps for 5 panel diagonal dancing games, such as Pump It Up") and of Direct Move, which extended it. **One `.ksf` = one chart (one difficulty of one play style)**; a song is a folder with several `.ksf` files plus `song.mp3|ogg|wav`, an intro clip and images. The author of the reference text (Joe Wreschnig / pydance, based on work by Matt Reppert and on StepMania's `NotesLoaderKSF.cpp`) calls the format "broken" and advises against creating new ones. It is nevertheless the exchange format of a large Korean/Latin-American Pump It Up chart scene and is read by StepMania 3.9+/4/5, Etterna, OutFox, pydance.

## Container & encoding

- Directory layout (`ksf-format.txt`): at least one `*.KSF` (case-insensitive names); `SONG.MP3|WAV|OGG` (the full song); `INTRO.MP3|WAV|OGG` (preview clip); `Disc.bmp` (300x200, song selector image); `Back.bmp` or `Title.bmp` (640x480 background). The directory name may encode metadata: `Title`, `Title - Artist`, `Title - Artist - Difficulty`.
- Text with MSD-like tags `#TAG:VALUE;` (StepMania reads with `MsdFile` **without** unescape), CRLF line ends, mostly **CP949 / KS C 5601** ("CP942/KSC 5601" in the original note), some EUC-KR. StepMania converts titles with `ConvertString(.., "korean")`.
- The `#STEP:` tag is special: its value starts on the next line and runs until a line `2222222222222` (13 twos).
- **File name = chart type and difficulty** (no tag says it). StepMania (`LoadFromKSFFile`) lower-cases the base name and maps substrings:

| Name contains | Difficulty (default meter) |
|---|---|
| `another` | Edit (25) |
| `wild`, `wd`, `crazy+`, `cz+`, `hardcore` | Challenge (20) |
| `crazy`, `cz`, `nightmare`, `nm`, `crazydouble` | Hard (14) |
| `hard`, `hd`, `freestyle`, `fs`, `double` | Medium (8) |
| `easy`, `ez`, `normal` | Easy (4) |
| `beginner`, `practice`, `pr` | Beginner (4) |
| (none) | Hard (10) |

  and the step type: `halfdouble`/`half-double`/`h_double`/`hdb` => `pump-halfdouble` (6 columns); `double`/`nightmare`/`freestyle`/`db`/`nm`/`fs` or `#PLAYER` containing `double` => `pump-double` (10); `_1` => `pump-single` (5); `_2` => `pump-couple` (10); default `pump-single`. The reference note: `Double.ksf` = double mode, `Halfdouble.ksf` = the inner 6 columns of the 10, `<difficulty>_1.ksf` = single ("unison") steps, `<difficulty>_2.ksf` = couple steps.

## Structure / metadata

| Tag | Meaning |
|---|---|
| `#TITLE` | `Title`, `Artist - Title`, or `Artist - Title - Difficulty` (separator ` - `); StepMania fills missing parts from the folder name |
| `#BPM` | starting BPM (a StepMania source comment: "According to Aldo_MX, there is a default BPM and it's 60") |
| `#STARTTIME` | **centiseconds** of delay before the chart starts (positive = delay; StepMania `offset = -STARTTIME/100`) |
| `#TICKCOUNT` | step lines per beat: each line is `1/TICKCOUNT` beat (`4` => sixteenth lines; `2` => 8ths; `1` => quarters). Missing: StepMania defaults to 4 with a warning; values <= 0 reject the file |
| `#DIFFICULTY` | meter (integer, clamped >= 1; Direct Move uses it as the foot level) |
| `#PLAYER` | `SINGLE` / `DOUBLE` ... (Direct Move: `double` flags a double chart) |
| `#BPM2` `#BPM3` | second and third BPM (KIU/Direct Move) |
| `#BUNKI` `#BUNKI2` | **centiseconds** at which BPM2/BPM3 take over (decimals allowed) |
| `#STARTTIME2` `#STARTTIME3` | offsets in effect at the BUNKI points (`STARTTIME3` also marks a KIU-compliant file) |
| `#INTROFILE` `#SONGFILE` `#DISCFILE` `#TITLEFILE` `#MUSICINTRO`(`#INTRO`) | file references (song, intro clip = preview start in seconds for StepMania, disc image => banner, title image => background) |
| `#STEP` | the step lines (see Notes) |

Direct Move adds the pipe control rows inside `#STEP` (Notes below).

## Timing model

- Position is **implicit**, one line = `1/TICKCOUNT` beat; beat 0 = `#STARTTIME`. StepMania: `curBeat += 1/tickcount` after each normal step line; the file ends at the row `2222222222222`.
- **KSF BPM changes** (original KIU method): the headers `#BPM`, `#BPM2`, `#BPM3` with `#BUNKI`, `#BUNKI2` = the *time in centiseconds* at which each change happens (not a beat): "BPMn+1 starts at the time specified in centiseconds by BUNKIn". StepMania converts to a beat with `HandleBunki`: `beat = (BUNKI + gap) * (BPM_early/60)`, where `gap = -STARTTIME/100`. In the reference example, `#BPM:146.10; #BPM2:180.20; #BPM3:195.00; #BUNKI:4200; #BUNKI2:10000` => 42 s: 180.2 BPM, 100 s: 195.
- **STARTTIME2/STARTTIME3**: offsets applied at the BUNKI points ("the chart position is moved as if the chart started at that offset"): permits warps and visual tricks; Direct Move and StepMania do not implement it correctly.
- **Direct Move rows** (StepMania `LoadFromKSFFile`, lines beginning with `|`): `|T<n>|` tickcount change; `|B<n>|` BPM change at the current beat; `|E<n>|` delay of `n` ticks at the current BPM (adds to the existing delay); `|D<ms>|` delay in milliseconds; `|M<n>|` or `|C<n>|` combo/multiplier; `|S..|` speed and `|F..|` fakes (parsed but unimplemented in StepMania); `|X<ratio>|` scroll segment. The text between `|x` and the final `|` is a number. (Parsed as `substr(2, size-3)`.) A file is considered "KIU compliant" if it has `#STARTTIME3`/BPM2/BUNKI headers or ends with `2222222222222` and has no `|` rows; "DM required" otherwise.
- Negative or sub-1 BPMs and "rapid" ticks (TICKCOUNT up to thousands) are used by Direct Move gimmicks; a negative BPM makes Direct Move scroll top-to-bottom (a known quirk used for trick charts).
- Position -> time: standard beat/BPM integration; add `-STARTTIME/100`.

## Notes

Each step line has **13 characters**; only the first 5 (single/unison) or 10 (double, couple) matter. The 13-character width is shared by all modes; `halfdouble` uses a `0011111100000` layout and StepMania drops the first 2 columns (the middle 6).

- Column order: **Down-Left, Up-Left, Center, Up-Right, Down-Right** (pad 1), then the same five for pad 2 in columns 6-10 (doubles/couples).
- `0` no step; `1` normal step; `4` hold: "A 4 indicates a hold, for as long as a 4 is found in that column. The hold ends on the beat of the last 4, not on the first 0." StepMania: the head row = first `4`, the tail row = previous line (the last `4`); a hold of one line becomes a tap. Repeated `1`s in consecutive lines used as a hold also exist in some files; no known simulator supports that.
- `2` / `2222222222222`: end of pattern (a line of 13 twos).
- StepMania additionally accepts `M`/`m` (mine), `F`/`f` (fake), `L`/`l` (lift) in step lines (Direct Move era); any other character gives "invalid row; corrupt notes ignored".
- The last 3 characters (columns 11-13) "are probably light control columns" and are not always 0; nothing uses them.

## Audio & images

`SONG.MP3|WAV|OGG` is the song (StepMania also finds `song.oga`); `INTRO.*` is the preview clip (StepMania sets sample length 7 s: "intro length in piu mixes is generally 7 seconds"); `Disc.bmp` => banner, `Back.bmp`/`Title.bmp` => background; names can be overridden by `#SONGFILE`, `#DISCFILE`, `#TITLEFILE`, `#INTROFILE`. No keysounds, no video.

## Versions & variants

- **Old KSF** (KIU): `#BPM/#BPM2/#BPM3 + #BUNKI`, `#STARTTIME/2/3`, `#TICKCOUNT` header, 13-wide lines. Max 3 BPMs.
- **New grammar / Direct Move**: `|`-rows (above). Limit of 3 shifts removed (per community history).
- A KSF dir with both styles loads partially in StepMania; the loader comment explains that a "KIU compliance" flag decided from the last (easiest) file wrecked files whose KSFs mixed both.
- Related: `STX` (Pump It Up arcade step data) -> `.ksf` via STX2DM; [pump-it-up/ucs](../../pump-it-up/ucs/README.md); [`.sma`](../../stepmania-amx/sma/README.md).

## Quirks & pitfalls

- Everything is implicit (file name, line count, centisecond BPM changes): a parser must know the step type from the **file name**.
- BPM changes are in **time**, not beats; they depend on `#STARTTIME`; "STARTTIME2/3" offsets move the chart at the change.
- Hold end is the **last** `4` line; the first `0` after it is not part of the hold.
- Titles/artist in Korean code pages (CP949/EUC-KR), CRLF.
- `|`-rows do not advance the beat; normal lines do.
- Half-double charts use the middle 6 of 10 columns.
- A `#TICKCOUNT` > 48 cannot sit on the 48-rows-per-beat StepMania grid; StepMania clamps tickcount *segments* (`|T`, header processing) to 0..48 but the per-line beat step `1/TICKCOUNT` is not clamped in `LoadFromKSFFile`, so the rows get rounded by `BeatToNoteRow`.

## Example

Real sample from StepMania's docs ([`Docs/SimfileFormats/KSF/sample.ksf`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/KSF/sample.ksf)):

```
#TITLE:***;
#BPM:150;
#STARTTIME:0;
#PLAYER:SINGLE;
#TICKCOUNT:4;
#INTROFILE:;
#SONGFILE:;
#DISCFILE:;
#TITLEFILE:;
#DIFFICULTY:;
#STEP:
1000000000000
0100000000000
0010000000000
0001000000000
0000100000000
0040000000000
0040000000000
0040000000000
0040000000000
0000000000000
2222222222222
```

(four taps DL, UL, C, UR, a DR tap, then a 4-line hold on the centre column = beats 1.25..2.0 at 4 lines/beat, and the closing row.)

## ROX support

Read by ROX since Prism's addition of `rox::formats::ksf` (decode only: ROX does not write KSF). One file is one chart: `KsfDecoder::decode_named(bytes, file_name)` / `decode_with_report(bytes, &KsfContext { file_name, folder_name })` (`KsfReport`) read it with its FILE NAME (the step type and difficulty come from it, by the loader's rules above; the folder name fills the title and artist `#TITLE` lacks), `parse` gives the `.sm` types. Played: `pump-single` (5 columns) and `pump-halfdouble` (6, the middle six of the ten). `pump-double` and `pump-couple` (10 columns) are refused with a message, as the `.sm` reader plays no 10-column step type. Read: `#BPM`, `#BPM2`/`#BPM3` with `#BUNKI`/`#BUNKI2` (the loader's `HandleBunki`, its approximation kept), `#STARTTIME` (baked into the times), `#STARTTIME2` (as the second gap), `#TICKCOUNT`, `#DIFFICULTY`, `#PLAYER`, `#TITLE`, `#SONGFILE` (`metadata.audio_file`, empty when absent: the caller finds `song.*` of the folder), `#TITLEFILE`, `#DISCFILE`, `#MUSICINTRO`/`#INTRO`; rows `0` `1` `4` (first to last `4` is a hold) `M` mine `L` lift (a tap) `F` (not played); Direct Move rows `|T` `|B` `|E` `|D` (`|M` `|C` `|S` `|F` `|X` are counted and ignored); text in UTF-8 or EUC-KR/CP949. Not applied: the mid-song offset jumps of `#STARTTIME2`/`#STARTTIME3`. Details: [ROX source: src/formats/ksf/mod.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/ksf/mod.rs).

Read by Prism (`docs/game.md` "Formats de danse"): each `.ksf` of a folder is one entry (they are siblings, never shadowing each other); `#SONGFILE` is reduced to its file name and looked for in the folder, else the first audio file of the folder, else the chart is listed without sound, marked as missing its audio, and played silent; a `.ssc`, `.sm` or `.dwi` of the folder shadows the `.ksf` files; the MP3 is timed gapless (nothing says the original players decode it like StepMania). `pump-double`/`pump-couple` charts are not listed.

## Parsers & tools

- StepMania [NotesLoaderKSF.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderKSF.cpp) (C++; there is **no KSF writer**: `NotesWriterKSF.cpp`, linked from the original repo README, returns 404 at master, 5_1-new and the pinned commit); Etterna `NotesLoaderKSF.cpp`; pydance `KSFFile` ([fileparsers.py](https://github.com/mbenkmann/pydance/blob/master/fileparsers.py), Python); OutFox (pump mode lists `.ksf`).
- Direct Move / KSFCreator: https://github.com/syspro86/directmove (releases); converter STX -> KSF: https://github.com/StepMania-AMX/STX2DM (MFC).

## Sources

- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/KSF/ksf-format.txt (+ `sample.ksf`, `_src.txt`)
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderKSF.cpp
- https://github.com/stepmania/stepmania/wiki/Note-Types and https://stepmania.fandom.com/wiki/Step_formats
- https://github.com/mbenkmann/pydance/blob/master/docs/ksf-format.txt
- Community summaries (search results, not opened as pages: NamuWiki "KSF(Kick it up)", team-stepmasters.com, github.com/StepMania-AMX/STX2DM)
