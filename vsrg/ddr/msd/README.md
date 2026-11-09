# MSD step script (`.msd`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: text (Shift-JIS-era Japanese origin; charset undeclared)

## Overview

`.msd` is the text chart script of an early Windows DDR simulator, the "grand daddy" (StepMania, `Docs/SimfileFormats/misc.txt`) of the `#TAG:param:param;` family: `.msd` -> `.dwi` -> `.sm` -> `.ssc`. It is not a Konami format. The earliest spec is the Japanese page "MSDファイル書式 Ver2.0β1" (archived 2007 copy of `doremi.kalin.to/ddr/msd_format.html`): "an MSD file is a chart script developed for DDR'99; DDR'99 loads files written in this script". The `msd` Rust crate: "The first known use of the MSD format is from the rhythm dance game DDR'99 (DDR here standing for 'Delight Delight Reduplication')". Files were made by hand or converted from BMS; DWI's author "was using MSD files I had found online as a basis" in 2000 (The History of DWI). D2REDIT also reads `*.msd` ([legacy-dance-formats/d2r](../../legacy-dance-formats/d2r/README.md)).

## Container & encoding

- Plain text `#TAG:PARAM0:PARAM1:PARAM2;` records ("The first field is typically an identifier but doesn't have to be", `MsdFile.cpp`), `//` comments in StepMania's reader. The semicolon is required, but StepMania recovers a missing `;` when `#` starts a new line.
- `\` escapes of `:`, `;`, `#`, `\` exist in today's generalized MSD ([Anders429/msd](https://github.com/Anders429/msd)); whether the DDR'99 sim processed them is Unknown.
- Charset undeclared; Japanese files are Shift-JIS in practice [inference] (the spec page is CP932).
- One file per song, all play modes inside.

## Structure / metadata

From the Ver 2.0 beta 1 spec (translated):

| Command | Meaning |
|---|---|
| `#FILE:string;` (marked "to be changed") | default file name for BMP and WAVE; no extension |
| `#TITLE:string;` | song title, up to 64 characters |
| `#ARTIST:string;` | song author, up to 64 characters |
| `#BPM:number;` | BPM, decimals supported |
| `#GAP:number;` | corrects the offset of the step marks "in dot (pixel) units"; negative allowed; DWI notes that other MSD sims use a different GAP unit/calculation than DWI's milliseconds |
| `#BACK:string;` ("to be added") | background BMP for play; falls back to `#FILE` |
| `#BGM:string;` ("to be added") | WAVE for play; falls back to `#FILE` |
| `#SELECT:string;` ("to be added") | menu title BMP; falls back to `#FILE` |
| `#SINGLE:level:mode:steps;` | single-play level, game mode, steps |
| `#DOUBLE:level:mode:steps1:steps2;` | double-play level, mode, steps (1P : 2P) |
| `#COUPLE:level:mode:steps1:steps2;` | couple-play level, mode, steps (1P : 2P) |

Note the parameter order **level first, then mode**; DWI reversed it (`#SINGLE:BASIC:5:...`). **Real files disagree with the spec page:** the seven real `.msd` files of the Doremi DDR fan page all write `#SINGLE:BASIC:<level>:<steps>;` (mode first, level second, like DWI) and carry a `#MSD:<author>;` credit tag, `#FILE:<name>.wav;`, a `#GAP` in plain integers (e.g. `#GAP:8`, `#GAP:-10`), CP932 text and CRLF [observed in `samples/doremi-ddr_banban.msd`, `samples/doremi-ddr_densya.msd`; they target the freeware sim Delight Delight Reduplication per the host page].

Predefined mode strings: `NORMAL` and `HARD` (**removed in Version 2.0**), `BASIC` (**added in 2.0**; "the combination of Normal and Hard"), `ANOTHER`, `MANIAC`.

## Timing model

- One character of step data = an **8th-note** step, so a measure is 8 characters (`00000000`). `(` ... `)` distributes the enclosed step info evenly over a shorter span (e.g. `(XXXX)` for 16th notes); `[` ... `]` distributes evenly over a longer span (mainly half-note triplets); `{` ... `}` outputs every step "2 dots" apart for fixing arrow misalignment. The exact fractions of the original groups are not spelled out in the page; DWI, which inherited the syntax, defines `( )` = 1/16, `[ ]` = 1/24 and `{ }` = 1/64 of a measure [inference]. See [DWI](../../dwi/dwi/README.md#timing-model).
- Time is `#BPM`-based; `#GAP` is a pixel/dot-unit alignment value, not seconds, in the DDR'99 sim (no tempo-change or stop commands exist in Ver 2.0 beta 1; DWI added `#FREEZE` and `#CHANGEBPM`, "additions to the MSD format to allow for speed-changes and pauses").
- To convert to time: advance the cursor per character/bracket group at `60/BPM` per beat (4 beats per measure), then apply the sim-specific GAP.

## Notes

"The numeric keypad corresponds to the foot panels. The arrows left/down/up/right correspond to `4 2 8 6`. A 90-degree step is the keypad corner: `7` for left+up, `9` for up+right. Down+up is `A`; left+right is `B`." So: `1 2 3 4 6 7 8 9 A B` and `0`, the alphabet DWI kept (adding `<>` groups, `!` holds and `C..M` for 6-panel). Ver 2.0 beta 1 has no hold/freeze arrows (freezes came with DDRMAX; DWI added `!`). The spec says "MSD scripts are still in development, so major specification changes are possible".

## Audio & images

`#FILE` (BMP + WAVE share a base name, no extension), optional `#BACK` (BMP), `#BGM` (WAVE), `#SELECT` (menu BMP). Bitmaps and PCM WAVE only.

## Versions & variants

Only Ver 2.0 beta 1 is documented (it replaced `NORMAL`/`HARD` with `BASIC`). StepMania's `MsdFile` generalizes the tag syntax and still reads `.sm`, `.ssc`, `.dwi`, `.ksf`, `.sma`, `.edit`. Converters from BMS to MSD and DWI existed. Other simulators' MSD charts load in DWI after a GAP change.

## Quirks & pitfalls

- Level precedes mode (DWI reverses it).
- `#GAP` is in the simulator's own unit, unlike DWI's milliseconds.
- Only 8th-note slots plus bracket groups, no beat numbers.
- No unescape/charset standard; a `.msd` found today may be DWI or SM text with the old extension.

## Example

Hand-built from the translated rules (the spec has no sample):

```
#TITLE:Example;
#ARTIST:Someone;
#BPM:140;
#GAP:0;
#SINGLE:4:BASIC:2468(2468)B0A0;
```

## ROX support

Decode only, `rox::formats::dwi` (`MsdDecoder`, `DetectedFormat::Msd`): the DWI reader in its MSD dialect. Every playable `#SINGLE`/`#DOUBLE`/`#SOLO` tag is a variant (`#COUPLE` is skipped, as for `.dwi`); a tag whose first parameter is a number and second is not is read in the spec's level-first order, otherwise mode first as the real files write it. `#GAP` is not applied (the simulator's dots, not milliseconds; warned). Text is Shift-JIS when it is not UTF-8.

## Parsers & tools

- StepMania `MsdFile` ([MsdFile.cpp](https://github.com/stepmania/stepmania/blob/master/src/MsdFile.cpp)), [Anders429/msd](https://github.com/Anders429/msd) (Rust/serde), [msdparser](https://pypi.org/project/msdparser/) (Python), pydance `MSDFile` (Python); D2REDIT reads/writes `.msd`-family files (see D2R).

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md) (fan charts from the Wayback copy of http://doremi.kalin.to/ddr/ captured 2006-04-17, plus one hand-written synthetic file). The real dialect writes `#SINGLE` mode first (see Structure). More: other Wayback captures of the site (`doremi.kalin.to/ddr/first.html` ... `fifth.html` list the charts; only those seven `.msd` URLs returned 200); the 'Delight Delight Reduplication' program by Nickle (http://nickle.hey.to/, nothing downloadable in Wayback); D2REDIT reads `*.msd` ([`../../legacy-dance-formats/d2r`](../../legacy-dance-formats/d2r/README.md)).

## Sources

- https://web.archive.org/web/20070606025338/http://doremi.kalin.to/ddr/msd_format.html (MSD Ver 2.0β1, Japanese; translated above)
- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/misc.txt (`[MSD]`)
- https://github.com/Anders429/msd (origin: DDR'99; syntax)
- http://dwi.ddruk.com/history.php (DWI built on MSD), https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/DWI/DWI.txt
- https://github.com/stepmania/stepmania/blob/master/src/MsdFile.cpp
