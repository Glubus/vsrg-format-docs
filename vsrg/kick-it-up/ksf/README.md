# Kick It Up step file (`.ksf`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (CP949/KS C 5601 or EUC-KR, CRLF)

## Overview

`.ksf` is the chart format of the Kick It Up Pump-It-Up simulator ("designed for representing steps for 5 panel diagonal dancing games, such as Pump It Up") and of Direct Move, which extended it. One `.ksf` is one chart (one difficulty of one play style); a song is a folder with several `.ksf` files plus `song.mp3|ogg|wav`, an intro clip and images. The reference text (Joe Wreschnig / pydance, from Matt Reppert and StepMania's `NotesLoaderKSF.cpp`) calls the format "broken". It is still the exchange format of a large Korean/Latin-American Pump It Up chart scene, read by StepMania 3.9+/4/5, Etterna, OutFox, pydance.

## Container & encoding

- Directory layout (`ksf-format.txt`): at least one `*.KSF` (case-insensitive names); `SONG.MP3|WAV|OGG` (the full song); `INTRO.MP3|WAV|OGG` (preview clip); `Disc.bmp` (300x200, song selector image); `Back.bmp` or `Title.bmp` (640x480 background). The directory name may encode metadata: `Title`, `Title - Artist`, `Title - Artist - Difficulty`.
- Text with MSD-like tags `#TAG:VALUE;` (StepMania reads with `MsdFile` without unescape), CRLF line ends, mostly CP949 / KS C 5601 ("CP942/KSC 5601" in the original note), some EUC-KR. StepMania converts titles with `ConvertString(.., "korean")`.
- The `#STEP:` tag is special: its value starts on the next line and runs until a line `2222222222222` (13 twos).
- The file name gives chart type and difficulty (no tag does). StepMania (`LoadFromKSFFile`) lower-cases the base name and maps substrings:

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
| `#STARTTIME` | centiseconds of delay before the chart starts (positive = delay; StepMania `offset = -STARTTIME/100`) |
| `#TICKCOUNT` | step lines per beat: each line is `1/TICKCOUNT` beat (`4` => sixteenth lines; `2` => 8ths; `1` => quarters). Missing: StepMania defaults to 4 with a warning; values <= 0 reject the file |
| `#DIFFICULTY` | meter (integer, clamped >= 1; Direct Move uses it as the foot level) |
| `#PLAYER` | `SINGLE` / `DOUBLE` ... (Direct Move: `double` flags a double chart) |
| `#BPM2` `#BPM3` | second and third BPM (KIU/Direct Move) |
| `#BUNKI` `#BUNKI2` | centiseconds at which BPM2/BPM3 take over (decimals allowed) |
| `#STARTTIME2` `#STARTTIME3` | offsets in effect at the BUNKI points (`STARTTIME3` also marks a KIU-compliant file) |
| `#INTROFILE` `#SONGFILE` `#DISCFILE` `#TITLEFILE` `#MUSICINTRO`(`#INTRO`) | file references (song, intro clip = preview start in seconds for StepMania, disc image => banner, title image => background) |
| `#STEP` | the step lines (see Notes) |

Direct Move adds the pipe control rows inside `#STEP` (Notes below).

## Timing model

- Position is implicit: one line = `1/TICKCOUNT` beat; beat 0 = `#STARTTIME`. StepMania does `curBeat += 1/tickcount` after each normal step line; the file ends at `2222222222222`.
- BPM changes (original KIU): `#BPM`, `#BPM2`, `#BPM3` with `#BUNKI`, `#BUNKI2` give the time in centiseconds of each change, not a beat: "BPMn+1 starts at the time specified in centiseconds by BUNKIn". StepMania converts with `HandleBunki`: `beat = (BUNKI + gap) * (BPM_early/60)`, `gap = -STARTTIME/100`. Reference example: `#BPM:146.10; #BPM2:180.20; #BPM3:195.00; #BUNKI:4200; #BUNKI2:10000` => 42 s: 180.2 BPM, 100 s: 195.
- `STARTTIME2`/`STARTTIME3` offsets apply at the BUNKI points ("the chart position is moved as if the chart started at that offset"); this allows warps and visual tricks. Direct Move and StepMania do not implement it correctly.
- Direct Move rows (StepMania `LoadFromKSFFile`, lines beginning with `|`): `|T<n>|` tickcount change; `|B<n>|` BPM change at the current beat; `|E<n>|` delay of `n` ticks at the current BPM (adds to the existing delay); `|D<ms>|` delay in ms; `|M<n>|` or `|C<n>|` combo/multiplier; `|S..|` speed and `|F..|` fakes (parsed, unimplemented in StepMania); `|X<ratio>|` scroll segment. The text between `|x` and the final `|` is a number (`substr(2, size-3)`). A file is "KIU compliant" if it has `#STARTTIME3`/BPM2/BUNKI headers or ends with `2222222222222` and has no `|` rows; "DM required" otherwise.
- Negative or sub-1 BPMs and "rapid" ticks (TICKCOUNT up to thousands) are Direct Move gimmicks; a negative BPM scrolls top-to-bottom (a trick-chart quirk).
- Time: standard beat/BPM integration plus `-STARTTIME/100`.

## Notes

Each step line has 13 characters; only the first 5 (single) or 10 (double, couple) matter. `halfdouble` uses a `0011111100000` layout and StepMania drops the first 2 columns (the middle 6).

- Column order: Down-Left, Up-Left, Center, Up-Right, Down-Right (pad 1), then the same five for pad 2 in columns 6-10.
- `0` no step; `1` normal step; `4` hold: "A 4 indicates a hold, for as long as a 4 is found in that column. The hold ends on the beat of the last 4, not on the first 0." StepMania: head row = first `4`, tail row = previous line (the last `4`); a one-line hold becomes a tap. Repeated `1`s as a hold appear in some files; no known simulator supports that.
- `2` / `2222222222222`: end of pattern (13 twos).
- StepMania also accepts `M`/`m` (mine), `F`/`f` (fake), `L`/`l` (lift) (Direct Move era); anything else gives "invalid row; corrupt notes ignored".
- The last 3 characters (columns 11-13) "are probably light control columns", not always 0; nothing uses them.

## Audio & images

`SONG.*` is the song (StepMania also finds `song.oga`); `INTRO.*` the preview clip (StepMania sets sample length 7 s: "intro length in piu mixes is generally 7 seconds"); `Disc.bmp` is the banner, `Back.bmp`/`Title.bmp` the background. `#SONGFILE`, `#DISCFILE`, `#TITLEFILE`, `#INTROFILE` override names. No keysounds, no video.

## Versions & variants

- Old KSF (KIU): `#BPM/#BPM2/#BPM3 + #BUNKI`, `#STARTTIME/2/3`, `#TICKCOUNT` header, 13-wide lines, max 3 BPMs.
- New grammar / Direct Move: `|`-rows (above); the limit of 3 shifts was removed.
- A directory mixing both styles loads partially in StepMania: a "KIU compliance" flag decided from the last (easiest) file wrecked files whose KSFs mixed both (loader comment).
- Related: `STX` (Pump It Up arcade step data) -> `.ksf` via STX2DM; [pump-it-up/ucs](../../pump-it-up/ucs/README.md); [`.sma`](../../stepmania-amx/sma/README.md).

## Quirks & pitfalls

- The step type comes from the file name; BPM changes are in time (centiseconds), not beats, and depend on `#STARTTIME`.
- Hold end is the last `4` line; the first `0` after it is not part of the hold.
- Titles/artist in CP949/EUC-KR, CRLF.
- `|`-rows do not advance the beat; normal lines do.
- `#TICKCOUNT` > 48 does not fit StepMania's 48-rows-per-beat grid: tickcount segments (`|T`, header processing) clamp to 0..48, but the per-line step `1/TICKCOUNT` in `LoadFromKSFFile` is not clamped, so `BeatToNoteRow` rounds the rows.

## Example

Sample from StepMania's docs ([`Docs/SimfileFormats/KSF/sample.ksf`](https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/KSF/sample.ksf)):

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

Decode only, `rox::formats::ksf`: `KsfDecoder::decode_named(bytes, file_name)` / `decode_with_report(bytes, &KsfContext { file_name, folder_name })` (`KsfReport`); `parse` gives the `.sm` types. The file name sets step type and difficulty (rules above); the folder name fills a missing title and artist.

- Played: `pump-single` (5) and `pump-halfdouble` (6, middle six of ten). `pump-double` and `pump-couple` (10) are refused with a message (the `.sm` reader has no 10-column type).
- Read: `#BPM`, `#BPM2`/`#BPM3` with `#BUNKI`/`#BUNKI2` (`HandleBunki`, approximation kept), `#STARTTIME` (baked into times), `#STARTTIME2` (as the second gap), `#TICKCOUNT`, `#DIFFICULTY`, `#PLAYER`, `#TITLE`, `#SONGFILE` (`metadata.audio_file`, empty when absent), `#TITLEFILE`, `#DISCFILE`, `#MUSICINTRO`/`#INTRO`.
- Rows: `0` `1` `4` (first to last `4` is a hold), `M` mine, `L` lift (a tap), `F` (not played); Direct Move `|T` `|B` `|E` `|D` applied, `|M` `|C` `|S` `|F` `|X` counted and ignored. UTF-8 or EUC-KR/CP949 text. Not applied: mid-song offset jumps of `#STARTTIME2`/`#STARTTIME3`.
- Prism (`docs/game.md` "Formats de danse"): each `.ksf` of a folder is one entry; `#SONGFILE` is reduced to its file name and looked up in the folder, else the first audio file, else the chart is listed silent and marked missing audio. A `.ssc`, `.sm` or `.dwi` in the folder shadows the `.ksf` files. MP3 is timed gapless. `pump-double`/`pump-couple` are not listed.

Source: [src/formats/ksf/mod.rs](https://github.com/Glubus/rhythm-open-exchange/blob/main/src/formats/ksf/mod.rs).

## Parsers & tools

- StepMania [NotesLoaderKSF.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderKSF.cpp) (C++; there is no KSF writer: `NotesWriterKSF.cpp`, linked from the original repo README, returns 404 at master, 5_1-new and the pinned commit); Etterna `NotesLoaderKSF.cpp`; pydance `KSFFile` ([fileparsers.py](https://github.com/mbenkmann/pydance/blob/master/fileparsers.py), Python); OutFox (pump mode lists `.ksf`).
- Direct Move / KSFCreator: https://github.com/syspro86/directmove (releases); converter STX -> KSF: https://github.com/StepMania-AMX/STX2DM (MFC).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). The KickItUp repo ([StepMania-AMX/KickItUp](https://github.com/StepMania-AMX/KickItUp), commit `80a1e1ad36cdfb335a58afc688bdf249db55da41`) also holds the KIU-variant note `docs/KSF-Notes.md`.

More: community song folders (one `.ksf` per difficulty and player: `Easy_1.ksf`, `Crazy_2.ksf`, `Double.ksf`...); StepMania, Etterna and ITGmania read them. [StepMania-AMX/directmove](https://github.com/StepMania-AMX/directmove) and `STX2DM` convert KSF but ship no sample. archive.org (searched 2026-11-09) has no Kick It Up/DirectMove item. Real files are CP949/EUC-KR with CRLF (`sample.ksf` is CRLF).

## Sources

- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/KSF/ksf-format.txt (+ `sample.ksf`, `_src.txt`)
- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderKSF.cpp
- https://github.com/stepmania/stepmania/wiki/Note-Types and https://stepmania.fandom.com/wiki/Step_formats
- https://github.com/mbenkmann/pydance/blob/master/docs/ksf-format.txt
- Community summaries (search results, not opened as pages: NamuWiki "KSF(Kick it up)", team-stepmasters.com, github.com/StepMania-AMX/STX2DM)
