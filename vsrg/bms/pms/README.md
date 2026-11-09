# feeling-PoMu Script (`.pms`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

BMS-compatible text format specialised for 9-button pop'n-music-style play. Syntax = [`.bms`](../bms/README.md). Not to be confused with the official arcade pop'n music chart data (see [`../../pop-n-music`](../../pop-n-music/README.md)) nor with the older, unrelated doremimania `.pms`.

## Overview

- Origin (hitkey memo): 2000-04-28 Koutaro Izumi's *doremimania* (a KEYBOARDMANIA trainer) used a `.pms` extension for a notation "completely different from BMS" (probably "Piano-Music-Script"); 2000-09-05 Nekomi released **feeling pomu** 1.41 Test5, specialised in 9 buttons, which auto-spreads BMS/BME charts over nine lanes and defined **PMS as a subset of BMS** for 9 buttons. The memo states the two PMS are unrelated.
- 2002-09-23 **feeling pomu second** (pomu2) 0.60 added LN support (both RDM notation and `#LNOBJ`) and also an 18-button mode (PMS-DP, not in the arcade game). 2009-09-16 LR2 beta3 extended the channels read when the extension is `.pms`. 2014 `lr2_pmsview_helper` (Misty.ls04) fixes the LR2 preview from editors.
- Why an extension: "9KEYS is BMS-DP substantially" - nothing in the file says it is 9-key. The *only* way to distinguish 9-button from double-play is the extension, so a 9-key chart must be `.pms`. Players that support PMS must read LN even in `.pms`.
- Supported by: pomu2, WAview, in_bm2, LR2, nanasi, fgt++/#, GDAC2, BMSE, uBMplay, PMSee-V, bmx2wav, iBMSC 3.0+, Angolmois 2.0a2+; BME-SP-style by pomu2, LR2, GDAC2 (774gsc), PMSee-V, bmx2wav, Angolmois; 18-key by pomu2, nanasi, GDAC2 (774gsc), bmx2wav, Angolmois (`--key-spec`). beatoraja lists `.pms` as a playable format. A GitHub script "PMStoBMEConverter" converts PMS charts into single-player BME (search result, not inspected).

## Container & encoding

Same as BMS (Shift_JIS text, `#` commands). One chart per file. The task description mentions "pms, pms3, pms5, pmse keys": these are informal names for key variants (see below) and not separate formats; no source defines "pms3/pmse" - [inference: 3-button battle, 5-button, extended]. The memo does list "PMS (5button)" and "PMS (pomu-battle)" mappings.

## Structure / metadata

All BMS headers. Special: `#PLAYER 3` is recommended for PMS "to maintain compatibility". `#TOTAL`, `#RANK` etc. as BMS.

## Timing model

As BMS (measure + fraction, `02` length, `03/08` BPM, `09` STOP).

## Notes

Lane mapping (hitkey KEYMAP table; buttons are numbered 1..9 left to right):

| Mode | Buttons 1..9 | Remarks |
| --- | --- | --- |
| PMS standard 9 keys (BMS-DP style) | `11 12 13 14 15 22 23 24 25` | standard PMS |
| PMS BME-type 9 keys (BME-SP) | `11 12 13 14 15 18 19 16 17` | accepted by LR2 beta3 090916+, pomu2; nanasi reads it as foot-pedal mode; "not well known" |
| PMS 18 keys (BME-DP) | 1P `11 12 13 14 15 18 19 16 17`, 2P `21 22 23 24 25 28 29 26 27` | pomu2 original feature |
| PMS 5 buttons | `13 14 15 22 23` (buttons 1,2,8,9 unused) | memo, "PMS (5button)" |
| PMS pomu-battle | `11 12 13` per side | memo, "PMS (pomu-battle)" |

- Invisible objects `31-49`, LN `51-69` and landmines `D1-E9` follow the mapping of the visible channels. The old free-zone channel `#xxx17` is used as a key in BME-type mode.
- BMSE throws away `#xxxX7`, so editing BME-type PMS there is difficult; GDAC2 + 774gsc is the best editor per the memo; BMSC "can be begun most quickly".
- Raindrop's `TranslateTrackPMS` maps P1 channel offsets 0-4 to lanes 0-4, 5/6 to lanes 7/8 and 7/8 to lanes 5/6 (and P2 offsets 0-3 to themselves).
- bmson uses `mode_hint` `popn-5k` and `popn-9k` (x = 1..5 or 1..9) for the same purpose, see [`../bmson`](../bmson/README.md).
- The file does not encode button colour (the arcade buttons are colour-coded; [inference] players colour by lane).

## Audio & images

As BMS (keysounds `#WAVxx`).

## Versions & variants

pomu (2000, 9-key), pomu2 (2002, + LN + 18 keys), LR2 beta3 (2009, BME-SP read as PMS), beatoraja (PMS play mode). The "pop'n music" arcade charts themselves are not PMS.

## Quirks & pitfalls

- Extension decides the layout; a `.bms` with channels `11-15,22-25` is read as 2P/DP, not 9-key.
- LR2 does not apply 9-key display when previewing from editors (hence lr2_pmsview_helper).
- Two unrelated "PMS" (doremimania vs pomu); only the pomu one is BMS-compatible.
- Channel `17` conflicts: free zone / foot pedal in other modes, a key here.

## Example

Illustrative, hand-built from the table above (not a real file): a one-measure PMS chart pressing buttons 1, 5, 9 in sequence.

```
#PLAYER 3
#TITLE example
#BPM 120
#WAV01 a.wav
#00111:01000000
#00115:00000100
#00125:00000001
```

(Standard 9-key mapping: `11`=button 1, `15`=button 5, `25`=button 9.)

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

BMS parsers with a PMS mode: Raindrop `NoteLoaderBMS.cpp`, beatoraja, Project OutFox (https://outfox.wiki/en/dev/mode-support/bms-pms-support), bmx2wav, PMSee-V, PMChr-V; conversion: PMStoBMEConverter (https://github.com/pablovirus/PMStoBMEConverter).

## Sources

- https://hitkey.nekokan.dyndns.info/cmds.htm (section "PMS", KEYMAP table)
- https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- bmson spec (mode hints): https://bmson-spec.readthedocs.io/en/master/doc/index.html
- Raindrop: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
- PMStoBMEConverter (search result only): https://github.com/pablovirus/PMStoBMEConverter
