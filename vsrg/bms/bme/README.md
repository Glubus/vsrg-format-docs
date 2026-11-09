# Be-Music Extend format (`.bme`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

Syntax, headers, timing and note rules are those of [`.bms`](../bms/README.md); this page covers the `.bme` extension only.

## Overview

`.bme` marks BMS charts with 7 keys + scratch (beatmania IIDX layout): channels `18`/`19` (1P) and `28`/`29` (2P) on top of the 5-key channels. TIX proposed it so BMS Creator (BMSC) could edit FlashTerminal's channels (the earlier Project2DX used `21`/`22` as 1P keys 6/7 with BM98's `#ExtChr`, pseudo-7K, BM98 only). "Strict BME" (no `#STOPxx`, `#BPMxx`, `#WAV01-FZ`, `#BMP00-FZ`, `#xxx51-69`...) is obsolete: `.bme` now just means "7K chart" and players read all extensions alike (`../bms/samples/beginner.bms` is 7K in a `.bms`). Samples: [`samples/`](samples/) (e.g. `HYPER.bme`: `#PLAYLEVEL 5000`, `#TOTAL 1200`).

## Container & encoding

As BMS (text, lines starting with `#`): [`../bms`](../bms/README.md#container--encoding).

## Structure / metadata

Same headers as BMS, plus `#STAGEFILE` (BM98k), `#BPMxx` (bemaniaDX), `#BGAxx` (BM98de).

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

As BMS (channel `02` length, `03`/`08` BPM, `09` STOP in 1/192 whole notes).

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

No long notes of its own (BML adds them, see [`../bml`](../bml/README.md)); modern players read `51-69`/`#LNOBJ` in any extension. Invisible objects `3x/4x` and landmines `D1-E9` as in BMS.

## Audio & images

As BMS.

## Versions & variants

BM98 (5K), Project2DX / FlashTerminal (7K variants), BME (TIX / BMSC); now every player accepts all channels and picks the layout from the channels used.

## Quirks & pitfalls

- Count channels `18/19/28/29` for the key count: a `.bms` can be 7K and a `.bme` can be 5K.
- Project2DX pseudo-7K charts use `21`/`22` as 1P keys 6/7 and look like 2P notes; only `#ExtChr` (BM98) tells them apart.
- Many `.bme` files contain `#STOPxx` and `#BPMxx`.

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

Decode only (`rox::formats::bms`, `rhythm-open-exchange/src/formats/bms/`; tests `bms/tests.rs`, charts `assets/bms/features.bms`, `assets/bms/nine.pms`). `.bms`, `.bme`, `.bml` go to `BmsDecoder`, `.pms` to `PmsDecoder`; `auto_decode`, `auto_decode_bytes`, `auto_decode_variant` detect them, `auto_encode` refuses them.

- Layout follows the lanes used (`#PLAYER` ignored). One side: `[scratch] key1..key5` or `key1..key7` (keys 6/7 are channels `x8`/`x9`; scratch column only if `x6`/`5x`/`6x` lanes use it) = 5, 6, 7 or 8 columns. Double play: `[scratch1] 1P keys | 2P keys [scratch2]` = 10, 12, 14 or 16 columns (scratch on both sides once either uses it). A 2P-only chart is single. PMS: nine columns, `11 12 13 14 15 22 23 24 25`, or `11 12 13 14 15 18 19 16 17` (BME-type) with no 2P lane and channels 16-19 used. Channel `x7` and out-of-layout lanes are dropped.
- Time: `02`, `03` (hex), `08` via `#BPMxx`/`#EXBPMxx` (non-positive or undefined BPM ignored; at one position `03` then `08`). STOP `09` in 1/48 beat units, not scaled by measure length, uses the BPM after a same-position change; a note on a STOP is at the pause start. Stops are baked into note times like `.sm`. Missing `#BPM` = 130.
- Long notes: `#LNTYPE 1` pairs (odd last head is a tap), `#LNOBJ` (terminator closes the lane's previous note, is not a note; orphan dropped), `#LNTYPE 2` runs (up to the first empty slot, across a bar line if last and first slots are filled). Mines `D1-E9` become mines. `3x`/`4x` ignored. A note inside an LN or at the same time and column as the previous note is dropped.
- `#RANDOM` is always 1; `#SETRANDOM n` forces `n`; `#IF`/`#ELSEIF`/`#ELSE`/`#ENDIF`/`#ENDRANDOM` nest; `#IF` without `#RANDOM` is 1; content in `#RANDOM` outside `#IF` is kept. `#SWITCH` unsupported.
- Audio: each playable note's `#WAVxx` goes to `chart.hitsounds` (`\` becomes `/`, ids case-insensitive base 36). Channel-01 sounds are not in the chart. With exactly ONE background sound, it is `metadata.audio_file` and all times shift back by its position (negative times possible). Otherwise `audio_file` is empty and Prism refuses the chart as "audio missing" unless `decode_with_audio_plan` is used: it returns every channel-01 object and playable keysound at chart time, and Prism mixes them into one Opus track (`docs/rendu-audio.md` in the Prism repo).
- Text: BOM UTF-8/UTF-16, else UTF-8, else Shift_JIS, else EUC-KR (`encoding_rs`).
- Metadata: `#TITLE`, `#ARTIST`, `#GENRE`, `#MAKER` (creator), `#PLAYLEVEL`, difficulty name from `#DIFFICULTY` (1-5: Beginner, Normal, Hyper, Another, Insane) else `#SUBTITLE` else `Normal`, background `#STAGEFILE` (else `#BACKBMP`).
- Not handled: `#SCROLLxx`/`#SPEEDxx`, `#STP`, `#SWITCH`, `#CHARSET`, base-62 files, BGA, `#LNMODE`, `#EXRANKxx`, channels `1A-1Z` (MGQ/pomu).
- Verified note for note (count, time, column, long notes) against Bemuse's `bms-js` (MIT) on the 21 sample charts of `bme/samples` and `bms/samples`; by note count against `bms-rs` (Apache-2.0), which differs in time on the 8 charts using channel `02` or `03` (not investigated; it spaces objects of a shortened or lengthened measure by the fraction of a 4/4 measure, Bemuse and ROX by the fraction of the measure's own length). The sample charts have no licence and are not shipped in ROX; ROX tests use synthetic charts.

## Parsers & tools

Same as [BMS](../bms/README.md#parsers--tools): bms-js, bms-rs, StepMania `NotesLoaderBMS`, Raindrop `NoteLoaderBMS` (translates `18`,`19` to keys 6,7), beatoraja, LR2; editors BMSE, iBMSC, BMSC.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: BMS Search, BMS of Fighters event pages and GENOSIDE starter packs (see [`../bms`](../bms/README.md)). 87 of the 221 chart files in `bemusic/music` (https://github.com/bemusic/music, https://bemuse.ninja/music/) are `.bme` (109 `.bms`, 15 `.pms`, 10 `.bml`). Converters that emit `.bme`: iidx2bms (`.1` -> `.bme`, see [`../../beatmania-iidx/1`](../../beatmania-iidx/1/README.md)); PMStoBMEConverter (PMS to BME, per the pms fiche). Editors: iBMSC, BMSE, BMS Creator, GDA Creator.

## Sources

- hitkey BMS command memo, sections "BME", "Channel Mapping Table", "KEYMAP Table": https://hitkey.nekokan.dyndns.info/cmds.htm
- Raindrop `NoteLoaderBMS.cpp`: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
- bms-js `notes/channels.js`: https://github.com/bemusic/bms-js
- Wikipedia "Be-Music Source": https://en.wikipedia.org/wiki/Be-Music_Source
- Repo samples `samples/`.
