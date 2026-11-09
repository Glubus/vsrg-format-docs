# feeling-PoMu Script (`.pms`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

BMS-compatible text format for 9-button pop'n-music-style play. Syntax = [`.bms`](../bms/README.md). Unrelated to arcade pop'n music data ([`../../pop-n-music`](../../pop-n-music/README.md)).

## Overview

- Origin (hitkey memo): on 2000-04-28 Koutaro Izumi's *doremimania* (a KEYBOARDMANIA trainer) used `.pms` for a notation "completely different from BMS" (probably "Piano-Music-Script"). On 2000-09-05 Nekomi's feeling pomu 1.41 Test5 defined PMS as a subset of BMS for 9 buttons. The two PMS are unrelated.
- 2002-09-23 feeling pomu second (pomu2) 0.60 added LN (RDM and `#LNOBJ`) and an 18-button mode (PMS-DP, not in the arcade game). 2009-09-16 LR2 beta3 extended the channels read for `.pms`. 2014 `lr2_pmsview_helper` (Misty.ls04) fixes the LR2 preview from editors.
- "9KEYS is BMS-DP substantially": nothing in the file says 9-key, so the extension is the only signal. PMS-capable players must read LN even in `.pms`.
- Supported by: pomu2, WAview, in_bm2, LR2, nanasi, fgt++/#, GDAC2, BMSE, uBMplay, PMSee-V, bmx2wav, iBMSC 3.0+, Angolmois 2.0a2+; BME-SP-style by pomu2, LR2, GDAC2 (774gsc), PMSee-V, bmx2wav, Angolmois; 18-key by pomu2, nanasi, GDAC2 (774gsc), bmx2wav, Angolmois (`--key-spec`). beatoraja plays `.pms`. "PMStoBMEConverter" (GitHub, search result, not inspected) converts PMS to single-player BME.

## Container & encoding

As BMS. "pms3/pmse" is undefined in any source [inference: 3-button battle, extended]; the memo lists "PMS (5button)" and "PMS (pomu-battle)" mappings.

## Structure / metadata

BMS headers. `#PLAYER 3` is recommended "to maintain compatibility".

## Timing model

As BMS.

## Notes

Lane mapping (hitkey KEYMAP table; buttons are numbered 1..9 left to right):

| Mode | Buttons 1..9 | Remarks |
| --- | --- | --- |
| PMS standard 9 keys (BMS-DP style) | `11 12 13 14 15 22 23 24 25` | standard PMS |
| PMS BME-type 9 keys (BME-SP) | `11 12 13 14 15 18 19 16 17` | accepted by LR2 beta3 090916+, pomu2; nanasi reads it as foot-pedal mode; "not well known" |
| PMS 18 keys (BME-DP) | 1P `11 12 13 14 15 18 19 16 17`, 2P `21 22 23 24 25 28 29 26 27` | pomu2 original feature |
| PMS 5 buttons | `13 14 15 22 23` (buttons 1,2,8,9 unused) | memo, "PMS (5button)" |
| PMS pomu-battle | `11 12 13` per side | memo, "PMS (pomu-battle)" |

- Invisible objects `31-49`, LN `51-69` and landmines `D1-E9` follow the mapping of the visible channels. The old free-zone channel `#xxx17` is a key in BME-type mode.
- BMSE throws away `#xxxX7`, so it cannot edit BME-type PMS; the memo prefers GDAC2 + 774gsc (BMSC "can be begun most quickly").
- Raindrop's `TranslateTrackPMS` maps P1 channel offsets 0-4 to lanes 0-4, 5/6 to lanes 7/8 and 7/8 to lanes 5/6 (and P2 offsets 0-3 to themselves).
- bmson uses `mode_hint` `popn-5k` and `popn-9k` (x = 1..5 or 1..9) for the same purpose, see [`../bmson`](../bmson/README.md).
- Button colour is not stored; [inference] players colour by lane.

## Audio & images

As BMS.

## Versions & variants

pomu (2000, 9-key), pomu2 (2002, + LN + 18 keys), LR2 beta3 (2009, BME-SP read as PMS), beatoraja (PMS play mode).

## Quirks & pitfalls

- A `.bms` with channels `11-15,22-25` is read as 2P/DP, not 9-key.
- LR2 does not apply 9-key display when previewing from editors.
- Channel `17`: free zone / foot pedal in other modes, a key here.

## Example

Hand-built: buttons 1, 5, 9 in sequence.

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

Decode only (`rox::formats::bms`, source `rhythm-open-exchange/src/formats/bms/`; tests `bms/tests.rs`, charts `assets/bms/features.bms`, `assets/bms/nine.pms`). `.bms`, `.bme`, `.bml` go to `BmsDecoder`, `.pms` to `PmsDecoder` (the extension alone selects nine buttons); `auto_encode` refuses them.

- Layout = the lanes the chart uses (`#PLAYER` ignored). One side: `[scratch] key1..key5` or `key1..key7` (keys 6/7 are channels `x8`/`x9`; scratch column only if `x6`/`5x`/`6x` lanes use it) = 5 to 8 columns. Double play: `[scratch1] 1P keys | 2P keys [scratch2]` = 10 to 16 columns (both scratches once either is used). Only-2P charts are single. PMS: nine columns `11 12 13 14 15 22 23 24 25`, or `11 12 13 14 15 18 19 16 17` (BME-type) with no 2P lane and channels 16-19 in use. Channel `x7` and lanes outside the layout are dropped.
- Time: `02` measure length, `03` hex BPM, `08` via `#BPMxx`/`#EXBPMxx` (non-positive or undefined BPM ignored; `03` then `08` at one position), `09` STOP (1/48 beat units, not scaled by measure length, uses the BPM after a same-position BPM change; a note on a STOP sits at the start of the pause). Stops are baked into note times like `.sm`. Missing `#BPM` = 130.
- Long notes: `#LNTYPE 1` pairs (odd last head is a tap), `#LNOBJ` (terminator closes the lane's previous note; orphan dropped), `#LNTYPE 2` runs (up to the first empty slot, across a bar line when last and first slots are filled). Mines `D1-E9` become mines. Invisible objects (`3x`/`4x`) ignored. A note inside a long note, or at the same time and column as the previous note, is dropped.
- `#RANDOM` is always 1; `#SETRANDOM n` forces `n`; `#IF`/`#ELSEIF`/`#ELSE`/`#ENDIF`/`#ENDRANDOM` nest; an `#IF` without `#RANDOM` is 1; content in `#RANDOM` outside `#IF` is kept. `#SWITCH` unsupported.
- Audio: playable notes' `#WAVxx` go to `chart.hitsounds` (`\` becomes `/`, ids case-insensitive base 36). Channel-01 sounds are not chart notes. With exactly ONE background sound, that file is `metadata.audio_file` and all times shift back by its position (earlier notes go negative). Otherwise `audio_file` is empty and Prism refuses the chart as "audio missing". `decode_with_audio_plan` also returns every channel-01 object and playable keysound at chart time; Prism mixes them into one Opus track (`docs/rendu-audio.md` in the Prism repo).
- Text: BOM UTF-8/UTF-16, else valid UTF-8, else Shift_JIS, else EUC-KR (`encoding_rs`).
- Metadata: `#TITLE`, `#ARTIST`, `#GENRE`, `#MAKER` (creator), `#PLAYLEVEL`, difficulty name from `#DIFFICULTY` (1-5: Beginner, Normal, Hyper, Another, Insane) else `#SUBTITLE` else `Normal`, background from `#STAGEFILE` else `#BACKBMP`.
- Not handled: `#SCROLLxx`/`#SPEEDxx`, `#STP`, `#SWITCH`, `#CHARSET`, base-62 files, BGA, `#LNMODE`, `#EXRANKxx`, channels `1A-1Z` (MGQ/pomu).
- Verification: note-for-note agreement with Bemuse's `bms-js` (MIT) on the 21 sample charts of `bme/samples` and `bms/samples`; note-count agreement with `bms-rs` (Apache-2.0), which differs in time on the 8 charts using channel `02` or `03` (not investigated): it spaces objects in a shortened or lengthened measure by the fraction of a 4/4 measure, where Bemuse and ROX use the measure's own length. Sample charts are unlicensed community files and are not shipped in ROX.

## Parsers & tools

BMS parsers with a PMS mode: Raindrop `NoteLoaderBMS.cpp`, beatoraja, Project OutFox (https://outfox.wiki/en/dev/mode-support/bms-pms-support), bmx2wav, PMSee-V, PMChr-V; conversion: PMStoBMEConverter (https://github.com/pablovirus/PMStoBMEConverter).

## Parsers & tools

BMS parsers with a PMS mode: Raindrop `NoteLoaderBMS.cpp`, beatoraja, Project OutFox (https://outfox.wiki/en/dev/mode-support/bms-pms-support), bmx2wav, PMSee-V, PMChr-V; conversion: PMStoBMEConverter (https://github.com/pablovirus/PMStoBMEConverter).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Real PMS songs are fan works with no stated licence; check terms before redistributing.

- Bemuse default songs: https://github.com/bemusic/music at commit `472b0f3cc433c39b0a7e9849705b34af68bf5400`.
- PMS Database release zips https://github.com/pmsdatabase/pmsdatabase.github.io/releases (`BOF2013PMS`, `BOFU2015PMS`, `BOFU2017PMS`, `G2R2014PMS`, `G2R2018PMS` `*_FullPackage_Team_sort*.zip`; `.noaudio.zip` ones were rewritten without audio/image members): BOF 2013 (283 `.pms`), BOFU2015 (460), BOFU2017 (380), G2R2014 (449), G2R2018 (294). They hold standard 9-button charts with `#PLAYER 3` (a few `#PLAYER 2`), `#LNTYPE`/`#LNOBJ`/`#LNMODE`, `#RANDOM`, ch 02/03/08/09, CP932 with some UTF-8 BOM and mixed line endings, and a few BME-type files using channels 16/18/19.
- More packages: the PMS Database (https://pmsdifficulty.xxxxxxxx.jp/); release tags `bofu2016pms-20161201` (21.7 MB), `bofxv19pms-20200526`, `bofxvipms-20210516`, `bofxviipms-20220830`, `bofetpms-20230712`, `bofntpms-20240509`, `bofttpms-20250426`, `bof21pms-20260512`, `g2r2014pms-20180325`. Its guide "創作譜面 (自作差分) の作成" (https://pmsdifficulty.xxxxxxxx.jp/guide_chart.html) says `.pms` is the extension for all PMS differences and names pBMSC; the BMS EVENT 2016 page (https://bms.ms/~hitkey/evt/2016) lists "BOFU2016PMS差分企画". Search terms: `PMS差分`, `PMS Database`, `BOF PMS`, `ポップン BMS`.
- Parser stubs: asdfghjkoiuy/iBMSCPP `ibmscpp-pms-9k.pms`, `ibmscpp-pms-5k.pms`.

## Sources

- https://hitkey.nekokan.dyndns.info/cmds.htm (section "PMS", KEYMAP table)
- https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- bmson spec (mode hints): https://bmson-spec.readthedocs.io/en/master/doc/index.html
- Raindrop: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
- PMStoBMEConverter (search result only): https://github.com/pablovirus/PMStoBMEConverter
- PMS Database: https://pmsdifficulty.xxxxxxxx.jp/ (pages about.html, guide_chart.html, BOFU2017PMS.html) and release assets https://github.com/pmsdatabase/pmsdatabase.github.io/releases
