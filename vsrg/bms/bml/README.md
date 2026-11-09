# Be-Music Longnote format (`.bml`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

Same syntax as [`.bms`](../bms/README.md). `.bml` is a filename filter for charts with `#LNOBJ` long notes (LN). It is unreliable: the Angolmois `.bml` tests use `#LNTYPE 1` channel-51 LN [observed: longnote-lntype1-last.bml].

## Overview

- RDM 1.61 (2002-02-22) added `#LNOBJ xx`. Players without it would show the LN terminator as a normal note, so the hitkey memo introduced `.bml` as a filter ("a player without `#LNOBJ` support will not open it").
- Strict BML: `#LNOBJ xx` is the only LN mechanism (no channels `51-69`). BMSC can edit it if renamed (all ids hexadecimal): "strict BML is a subset of BME".
- LN comes from games like EZ2DJ (1999-04-20) and Keyboardmania; the memo's LN-kind table also lists pop'n music "Keep-kun", DDR freeze arrows, IIDX 17 Charge Notes and Backspin Scratch.
- Modern players read LN in any extension; many authors name `#LNOBJ` charts `.bms`/`.bme`. The memo says PMS-capable players must interpret LN even in `.pms`.

## Container & encoding

As BMS.

## Structure / metadata

Headers as BMS. LN-specific: `#LNTYPE 1|2`, `#LNOBJ xx`, and beatoraja's `#LNMODE 1|2|3`.

## Timing model

As BMS.

## Notes

Long-note notations (details and examples in [`../bms`](../bms/README.md#notes)):

| Notation | Syntax | Where |
| --- | --- | --- |
| RDM type #1 | channels `51`..`59` (1P), `61`..`69` (2P): objects alternate start/end; `#LNTYPE 1` is the default (RDM 1.7, 2003-08-17) | MGQ idea (2001), simplified by RDM 1.21 (2001-09-29) |
| RDM type #2 | `#LNOBJ xx`: an object `xx` on `11`-`29` ends the LN whose start is the previous visible object of the lane | RDM 1.61 |
| MGQ type | `#LNTYPE 2`: runs of non-`00` objects on channels `51`..`8C`; obsolete | MGQ (quest, 2001) |

- With `#LNOBJ`, the keysound `xx` is conventionally an empty wav, because some players play it as BGM.
- Key-up sounding (HDX, IIDXv, TechnicalGroove): the end object's id, if different from the start id, plays on release.
- beatoraja `#LNMODE 1/2/3` (LN, CN, HCN) forces the long-note type; bmson has `t` per note for the same purpose.

## Audio & images

As BMS.

## Versions & variants

RDM-LN (`51-69`), then `#LNOBJ` (BML), then beatoraja `#LNMODE`. MGQ-LN is obsolete.

## Quirks & pitfalls

- With `#LNTYPE` channels and `#LNOBJ` together, priority is unspecified (pomu2 converts `51-69` into `11-29`; LR2 can depend on `#LNTYPE`).
- `#LNOBJ` ids should be uppercase for nanasi / fgt++.
- An LN never closed: DDR gives a compile error; others unspecified.
- BMSE crashes if a `51-69` object is moved to the BGM area, so many authors use `#LNOBJ`.

## Example

From the hitkey memo (LN from measure 001 to 064 in both notations):

```
#LNTYPE 1
#00151:00220000
#06451:000000000033

#LNOBJ ZZ
#00111:00220000
#06411:0000000000ZZ
```

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

See [BMS parsers](../bms/README.md#parsers--tools). LN handling: bms-js `notes`, bms-rs, Raindrop (`LNObj` set), beatoraja (`LNMODE`).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Any BMS pack can hold `.bml` files; see "Getting samples" in [`../bms`](../bms/README.md). Search a pack for `*.bml` and file contents for `#LNOBJ`. The Bemuse songs come from https://github.com/bemusic/music at commit `472b0f3cc433c39b0a7e9849705b34af68bf5400` (olivia `#LNOBJ ZZ` in CP932, caelumize `#LNOBJ 04`, starless `was`/`waslight` `#LNOBJ G0`).

## Sources

- https://hitkey.nekokan.dyndns.info/cmds.htm (sections "BML", "#LNTYPE 1/2", "#LNOBJ xx")
- beatoraja wiki: https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- Raindrop `NoteLoaderBMS.cpp`: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
