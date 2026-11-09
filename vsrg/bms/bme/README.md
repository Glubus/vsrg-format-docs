# Be-Music Extend format (`.bme`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

The syntax, header commands, timing and note rules are identical to [`.bms`](../bms/README.md); this page covers only what the `.bme` extension means. Read the BMS page first.

## Overview

- `.bme` ("Be-Music Extend format") is the extension used for BMS charts that need **7 keys + scratch** (beatmania IIDX layout), i.e. channels `18`/`19` (1P) and `28`/`29` (2P) in addition to the BMS 5-key channels.
- History from the hitkey memo: beatmania IIDX started in 1999-02-26. To support 7 keys, *Project2DX* (proposed by Urami) used channels `21`/`22` as "1P key 6/7" together with BM98's proprietary `#ExtChr` to redraw the screen (pseudo-7K, only portable to BM98). *FlashTerminal* (Tomohiro Fujii) reserved channels `18-19`, `28-29`. TIX proposed **BME** to unify FlashTerminal's channels with BMS and make them editable in BMS Creator (BMSC); the extension was a filter so that old players without those channels would not read the file.
- "Strict BME" is a file that uses nothing BMSC cannot edit (no `#STOPxx`, `#BPMxx`, `#WAV01-FZ`, `#BMP00-FZ`, `#xxx51-69`...). The memo's author considers the strict/loose distinction obsolete: in practice `.bme` simply means "7K chart" and all modern players read every extension identically. Most BMS in the wild with 7 keys are `.bme` (or `.bms`; the repo sample `../bms/samples/beginner.bms` is a 7K chart in a `.bms`).
- Samples in this repo: [`samples/`](samples/) (10 files; e.g. `HYPER.bme`: `#PLAYLEVEL 5000`, `#TOTAL 1200`, hundreds of `#WAVxx` lines).

## Container & encoding

Same as BMS: text, lines starting with `#`, Shift_JIS usual, one chart per file, folder per song. See [`../bms`](../bms/README.md#container--encoding).

## Structure / metadata

Same headers as BMS. BME adds (per the memo): `#STAGEFILE` (BM98k), `#BPMxx` (bemaniaDX), `#BGAxx` (BM98de) as extended commands that most implementations support; BMSC-only editing was the historical limit.

Channel additions over BMS (memo, "BME" section):

| Channel | Object | Origin |
| --- | --- | --- |
| `#xxx07` | BGA layer (over `04`) | BM98k |
| `#xxx08` | Extended (real-number) BPM, uses `#BPMxx` | bemaniaDX |
| `#xxx18`, `#xxx19` | 1P visible key 6, key 7 | FlashTerminal |
| `#xxx28`, `#xxx29` | 2P visible key 6, key 7 | FlashTerminal |
| `#xxx38`, `#xxx39` | 1P invisible key 6, 7 | FlashTerminal |
| `#xxx48`, `#xxx49` | 2P invisible key 6, 7 | FlashTerminal |

(`#xxx[1-4]7` free-zone/foot-pedal channels are a de facto non-standard command.)

## Timing model

Identical to BMS (measure + fraction, channel `02` length, `03`/`08` BPM, `09` STOP in 1/192 whole notes).

## Notes

Lane mapping (memo KEYMAP table; left to right on screen):

| Mode | Lanes | Channels |
| --- | --- | --- |
| BME SP | scratch, key1..key7 | `16 11 12 13 14 15 18 19` |
| BME DP | 1P: scratch, key1..key7; 2P: key1..key7, scratch | `16 11 12 13 14 15 18 19` , `21 22 23 24 25 28 29 26` |
| BME + foot pedal (nanasi) | + pedal | `17` |
| BME + foot pedal (Angolmois) | 2P keys 6/7 labelled KEY8/KEY9 | `17` / `27` |
| DSC/FPP (double scratch) | scratch, 1..7, scratch | `16 11 12 13 14 15 18 19 26` |
| OCT (nanasi `#OCT/FP`) | 13 keys per side | see memo |
| Project2DX (historical) | scratch, 1..7 | `16 11 12 13 14 15 21 22` |

Long notes: BME has none by itself (BML adds them, see [`../bml`](../bml/README.md)); modern players read `51-69`/`#LNOBJ` in any extension. Invisible objects `3x/4x` and landmines `D1-E9` as in BMS.

## Audio & images

As BMS.

## Versions & variants

BM98 (5K) → Project2DX / FlashTerminal (7K variants) → BME (TIX / BMSC) → every player accepts all channels. LR2 and others show the 7K layout from the channels used, not from the extension.

## Quirks & pitfalls

- A `.bms` can legitimately be a 7K chart (like the repo sample) and a `.bme` can be 5K; never trust the extension for the key count - count channels `18/19/28/29`.
- Project2DX pseudo-7K charts use `21`/`22` as 1P keys 6/7 and look like 2P notes; the `#ExtChr` header tells the difference (BM98 only).
- Strict BME predates `#STOPxx` and `#BPMxx`; many `.bme` files in the wild contain them.

## Example

Header start of [`samples/HYPER.bme`](samples/HYPER.bme) (Shift_JIS; displayed re-encoded, trimmed):

```
#PLAYER 1
#GENRE 東方妖々夢
#TITLE 幽雅に咲かせ、墨染の桜[HYPER]
#ARTIST zun
#BPM 143
#PLAYLEVEL 5000
#RANK 3
#TOTAL 1200
#STAGEFILE 

#WAV01 01.wav
#WAV02 02.wav
```

## ROX support

Read by ROX since Prism's addition of `rox::formats::bms` (decode only: ROX does not write BMS). Source: `rhythm-open-exchange/src/formats/bms/` (documented in its module, tests in `bms/tests.rs`, hand-written charts `assets/bms/features.bms` and `assets/bms/nine.pms`).

- Extensions: `.bms`, `.bme`, `.bml` go to `BmsDecoder`, `.pms` to `PmsDecoder` (the extension is the only thing that says nine buttons). `auto_decode`, `auto_decode_bytes` and `auto_decode_variant` detect them; `auto_encode` refuses them.
- **Layout = the lanes the chart uses** (`#PLAYER` is ignored, like most players). One side: `[scratch] key1..key5` or `key1..key7` (keys 6 and 7 are channels `x8`/`x9`; the scratch column exists only when channel `x6`/`5x`/`6x` lanes use it) = 5, 6, 7 or 8 columns. Double play (1P and 2P lanes both used): `[scratch1] 1P keys | 2P keys [scratch2]` = 10, 12, 14 or 16 columns (a scratch column on both sides as soon as either side uses it). A chart with only 2P lanes is a single chart. PMS: nine columns, buttons `11 12 13 14 15 22 23 24 25`, or `11 12 13 14 15 18 19 16 17` (BME-type) when there is no 2P lane and channels 16-19 are used. Channel `x7` (free zone / foot pedal) and lanes outside the layout are dropped.
- **Time**: measure length (`02`), BPM (`03` hex, `08` through `#BPMxx`/`#EXBPMxx`; a non-positive or undefined BPM is ignored; at one position `03` then `08`), STOP (`09`, 1/48 beat units, not scaled by the measure length, computed with the BPM that follows a BPM change at the same position, a note on a STOP is at the start of the pause; stops are baked into the note times like `.sm`, ROX has no stop point). Missing `#BPM` = 130.
- **Long notes**: `#LNTYPE 1` channels (head/tail pairs; an odd last head is a tap), `#LNOBJ` (the terminator closes the previous note of the lane and is not a note; an orphan terminator is dropped), `#LNTYPE 2` runs (consecutive slots up to the first empty slot, across a bar line when the last and first slots are both filled). Mines `D1-E9` become ROX mines. Invisible objects (`3x`/`4x`) are ignored. A note inside a long note, or on the same time and column as the previous note, is dropped.
- **`#RANDOM`**: always 1 (reproducible); `#SETRANDOM n` forces `n`; `#IF`/`#ELSEIF`/`#ELSE`/`#ENDIF`/`#ENDRANDOM` nest; an `#IF` without `#RANDOM` is 1; content inside `#RANDOM` but outside `#IF` is kept. `#SWITCH` is not supported.
- **Keysounds and audio**: each playable note's `#WAVxx` goes to `chart.hitsounds` (file names with `\` become `/`, ids are case-insensitive base 36). Channel-01 background sounds are not part of a ROX chart. When the chart has exactly ONE defined background sound, that file is `metadata.audio_file` and every time is moved back by its position (earlier notes get negative times); otherwise `audio_file` is empty and Prism refuses the chart as "audio missing" (the sounds would have to be mixed into one track, not done).
- **Text**: BOM UTF-8/UTF-16, else valid UTF-8, else Shift_JIS, else EUC-KR (`encoding_rs`).
- **Metadata**: `#TITLE`, `#ARTIST`, `#GENRE`, `#MAKER` (creator), `#PLAYLEVEL` (difficulty value), difficulty name from `#DIFFICULTY` (1-5: Beginner, Normal, Hyper, Another, Insane) else `#SUBTITLE` else `Normal`, background from `#STAGEFILE` (else `#BACKBMP`).
- **Audio plan**: `decode_with_audio_plan` also returns the sounds (every channel-01 object and the keysound of every playable object, at chart time) beside the chart; Prism mixes them into one Opus track when the chart has no single audio file (`docs/rendu-audio.md` in the Prism repo).
- Not handled: `#SCROLLxx`/`#SPEEDxx`, `#STP`, `#SWITCH`, `#CHARSET`, base-62 files, BGA, `#LNMODE`, `#EXRANKxx`, and the hexadecimal-letter channels `1A-1Z` (MGQ/pomu).
- Verification: the decoder agrees note for note (count, time, column, long notes) with Bemuse's `bms-js` (MIT) on the 21 sample charts of this repository (`bme/samples`, `bms/samples`), and by note count with `bms-rs` (Apache-2.0; it differs in time on the 8 of these 21 charts that use channel `02` or `03`, a difference not investigated further: for a shortened or lengthened measure it spaces the objects by the fraction of a 4/4 measure, where Bemuse and ROX use the fraction of the measure's own length). The sample charts are community files with no licence and are not shipped inside ROX; ROX's tests use the hand-written synthetic charts above.

## Parsers & tools

Same as [BMS](../bms/README.md#parsers--tools): bms-js, bms-rs, StepMania `NotesLoaderBMS`, Raindrop `NoteLoaderBMS` (translates `18`,`19` to keys 6,7), beatoraja, LR2; editors BMSE, iBMSC, BMSC.

## Getting samples

Details and per-file licences: [`samples/SOURCES.md`](samples/SOURCES.md). General sources (BMS Search, BMS events, starter packs, editors): see "Getting samples" in [`../bms`](../bms/README.md).

- **Committed** ([`samples/`](samples/)): the 10 community 7K+scratch charts that came with the upstream repository (origin and licence unknown; Shift_JIS or ASCII, CRLF, invisible objects, `#LNOBJ ZV` + `#LNTYPE 1`, ch 08 `#BPM01`), plus from open-source repositories: bms-rs `nc_mx.bme` (Apache-2.0; UTF-8 with BOM, LF, `#STOP01`, ch 08/09/03/02), bms-rs `dive_withblank.bme` (tab and blank values in `#WAV`/`#BMP`), rparser's MIT kusofumen `L9^.bme` (`#BPM 721`, Shift_JIS, 212 KB) and sappho192/BMSParser's `05.bon_voyage_7hyper.bme` (MIT repository; a full 7K chart, ASCII).
- **Manifest** (`samples.manifest.json`): 41 `.bme` charts from https://github.com/bemusic/music at the pinned commit `472b0f3cc433c39b0a7e9849705b34af68bf5400`, including real double-play `.bme` charts (`#PLAYER 3`, 14K, e.g. litmus `litmus_allisfair_14a.bme` with a lowercase `#LNOBJ zz`, `litmus_scorpiondance_DP*.bme`, ym1024 `starless_dp*_kero.bme` in CP932) and `#PLAYER 2` ones (`snack/dddd_dp*.bme`, `sobrem/_encrux_d2.bme`), CP932 and EUC-KR charts, and mines/STOP/BPM-999913 (`litmus_latch_7a.bme`). Not redistributable ("Each song is copyrighted by respective author"), so manifest-only.
- **How to get more**: 7K IIDX-style BMS packs commonly contain `.bme` files (87 of the 221 chart files in `bemusic/music` are `.bme`, 109 `.bms`, 15 `.pms`, 10 `.bml`; BMS Search, BMS of Fighters event pages and GENOSIDE starter packages are the places to look, see the `.bms` page). Converters that emit `.bme`: iidx2bms (`.1` -> `.bme`, see [`../../beatmania-iidx/1`](../../beatmania-iidx/1/README.md)); PMStoBMEConverter (PMS to BME, per the pms fiche). Editors: iBMSC, BMSE, BMS Creator, GDA Creator.

## Sources

- hitkey BMS command memo, sections "BME", "Channel Mapping Table", "KEYMAP Table": https://hitkey.nekokan.dyndns.info/cmds.htm
- Raindrop `NoteLoaderBMS.cpp`: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
- bms-js `notes/channels.js`: https://github.com/bemusic/bms-js
- Wikipedia "Be-Music Source": https://en.wikipedia.org/wiki/Be-Music_Source
- Repo samples `samples/`.
