# Be-Music Longnote format (`.bml`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (Shift_JIS in practice)

Same syntax as [`.bms`](../bms/README.md). `.bml` is a *filename filter* for charts that use long notes (LN) in the `#LNOBJ` form. Samples: see [Getting samples](#getting-samples); the three Angolmois `.bml` test files use `#LNTYPE 1` channel-51 long notes rather than `#LNOBJ` [observed in samples/longnote-lntype1-last.bml], so the extension is not a reliable indicator of the LN notation.

## Overview

- `.bml` = "Be-Music Longnote format". The hitkey memo's history: RDM 1.61 (2002-02-22) added `#LNOBJ xx`. Players that did not support it would show the LN terminator as an ordinary note, so the extension BML was prepared as a filter ("a player without `#LNOBJ` support will not open it").
- **Strict BML** = a chart whose only LN mechanism is `#LNOBJ xx`. LN on channels `51-69` (RDM notation) is *not* part of the strict definition. A strict BML can be edited in BMSC if renamed (all ids hexadecimal): BML was defined to edit LN in BMSC, so "strict BML is a subset of BME".
- In practice every modern player reads LN in any extension; people name 5K/7K LN charts `.bms`/`.bme` as well. The memo recommends `.bml` for `#LNOBJ` charts and says pomu2 supports `.bml`, and that PMS-capable players must interpret LN even in `.pms`.
- Context: the Long Note feature comes from games like EZ2DJ (1999-04-20) and Keyboardmania; the memo's table of long-note kinds also lists pop'n music "Keep-kun", DDR freeze arrows, IIDX 17 Charge Notes and Backspin Scratch.

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

- With `#LNOBJ`, the keysound `xx` is conventionally an *empty* wav; the memo notes some players play it as BGM, so defining an empty file keeps compatibility.
- LN count: 1 or 2 notes depending on the game.
- Key-up sounding (HDX, IIDXv, TechnicalGroove): the id of the end object, if different from the start id, is played on release.
- beatoraja `#LNMODE 1/2/3` (LN, CN, HCN) forces the long-note type; bmson has `t` per note for the same purpose.

## Audio & images

As BMS.

## Versions & variants

RDM-LN (`51-69`) → `#LNOBJ` (BML) → beatoraja `#LNMODE`. MGQ-LN is obsolete.

## Quirks & pitfalls

- If `#LNTYPE`-style channels and `#LNOBJ` coexist, priority is unspecified (pomu2 converts `51-69` into `11-29`; LR2 result can depend on whether `#LNTYPE` exists).
- `#LNOBJ` ids should be uppercase for nanasi / fgt++.
- A LN end object never closed (no terminator): DDR returns a compile error; behaviour in other players is unspecified.
- BMSE crashes if a `51-69` object is moved to the BGM area; that is the reason many authors use `#LNOBJ`.

## Example

Quoted from the hitkey memo (LN from measure 001 to 064 in both notations):

```
#LNTYPE 1
#00151:00220000
#06451:000000000033

#LNOBJ ZZ
#00111:00220000
#06411:0000000000ZZ
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

See [BMS parsers](../bms/README.md#parsers--tools). LN handling: bms-js `notes`, bms-rs, Raindrop (`LNObj` set), beatoraja (`LNMODE`).

## Getting samples

Details and per-file licences: [`samples/SOURCES.md`](samples/SOURCES.md).

- **Committed** ([`samples/`](samples/)): three public-domain Angolmois test charts (`longnote-followed-by-bomb.bml`, `longnote-lntype1-interleaved.bml`, `longnote-lntype1-last.bml`; these three use `#LNTYPE 1` channel-51 long notes, not `#LNOBJ`, despite the extension) and one hand-written CC0 strict-BML chart (`synthetic-lnobj.bml`, `#LNOBJ ZZ` only, UTF-8, LF).
- **Real Bemuse default songs** (committed, `bemuse-*` files): all 10 `.bml` files of https://github.com/bemusic/music at commit `472b0f3cc433c39b0a7e9849705b34af68bf5400` (olivia by 葵 with `#LNOBJ ZZ` in CP932, caelumize by void with `#LNOBJ 04`, starless `was`/`waslight` with `#LNOBJ G0`, ...). The repository README says "Each song is copyrighted by respective author" (accepted-risk, chart files only).
- **How to get more**: any BMS pack can contain `.bml` files (a `.bml` is a `.bms` with `#LNOBJ`): see "Getting samples" in [`../bms`](../bms/README.md). Per the hitkey memo the extension was created as a filter for `#LNOBJ` charts, so search a pack folder for `*.bml`; many authors name `#LNOBJ` charts `.bms`/`.bme` instead, so also search file contents for `#LNOBJ`.

## Sources

- https://hitkey.nekokan.dyndns.info/cmds.htm (sections "BML", "#LNTYPE 1/2", "#LNOBJ xx")
- beatoraja wiki: https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- Raindrop `NoteLoaderBMS.cpp`: https://raw.githubusercontent.com/zardoru/raindrop/master/src/NoteLoaderBMS.cpp
