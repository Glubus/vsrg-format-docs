# Pocket DDR chart (`.sdf`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (big-endian lengths, embedded PNG images)

## Overview

`.sdf` is the song file of Pocket DDR, a DDR-style program. The converter `SM2SDF.exe` ("SM 2 SCF Converter v.1.0 by Robot2037") turns an `.sm` into an `.sdf`. StepMania's `Docs/SimfileFormats/SDF/` holds the notes and samples (`SDF.txt`, `test.sdf`, `test-1bpm.sdf`, `test.sm`, `ssc-banner.png`, `ssc-bg.png`) and cites the old forum thread (`showthread.php?t=6621`, gone). `SDF.txt`: "Basically a compressed version of a .SM that includes the banner and background in the file as well"; layout `{Banner} {Background} {SDF data}`. This page adds a byte-level inspection of the two samples.

## Container & encoding

- Binary, big-endian numbers, one song per file (all charts inside).
- Layout (verified on both samples): `u32 BE length` + banner PNG; `u32 BE length` + background PNG (the sample images are 97 and 113 bytes; converter log "Converting image ssc-bg.png ... ssc-banner.png"); then the data block.
- Images are standard PNGs (signature `89 50 4E 47 0D 0A 1A 0A`).

## Structure / metadata

Data block observed in `test.sdf` (offset = start of data after the 2 PNGs):

| Offset | Size | Meaning |
|---|---|---|
| 0 | 1 | `01`: unknown (version/flag? [Unknown]); `SDF.txt` starts its offset count after this byte |
| 1..5 | 5 | `00 02 04 06 0A`: per `SDF.txt` "0x00-0x04: [000204060A]"; `02 04 06 0A` equal the four chart meters of `test.sm` (converter log: "difficulty 0..3 ... step difficulty = 2, 4, 6, 10"); the leading `00` is unknown |
| 6.. | 1+n each | four length-prefixed (1-byte) strings: title, subtitle, artist, credit (`test song`, `a remix`, `kurt angle!`, `aj jelly`); `#TITLETRANSLIT`, `#GENRE`, `#MUSIC`, `#CDTITLE`, `#SAMPLE*`, `#TIMESIGNATURES`, `#BGCHANGES`, `#KEYSOUNDS` are "ignored by sm2sdf" |
| next | 3 | offset: sign byte (`00` = +, `01` = -) + `u16 BE` milliseconds. `SDF.txt`: "+1.000 = 0x0003E8. -0.060 = 0x01003C"; `test-1bpm.sdf` has `01 18 8A` = -6.282 s |
| next | 2 | `u16 BE` BPM count N |
| next | 8 N | N entries `{u32 BE beat x 1000, u32 BE bpm x 1000}`: `test.sdf`: `0 / 93810`, `5000 / 187620` (= `0.000=93.810, 5.000=187.62`); `test-1bpm.sdf`: `2000 / 666667` = `#BPMS:2.000=666.667` (the one-BPM test file) |
| rest | | the chart blocks (below). `#STOPS:;` was empty in the samples, so the stop encoding is Unknown |

### Chart blocks

After the BPM table, each chart is `u8 X` + `u24 BE L` + `L` bytes (checked by script on both samples): `(X, L)` = `(00, 39)`, `(3B, 71)`, `(3B, 167)`, `(2F, 233)`, and the two bytes `33 00` remain at the end of the file. Equivalently, each chart is followed by one extra byte `3B`, `3B`, `2F`, `33` and the table starts with a `00`; which reading is right is Unknown. The converter log gives the compression result for the same four charts: "`compressing stepchart 0 [ 576 -> 39 ]`, `1 [ 576 -> 71 ]`, `2 [ 576 -> 167 ]`, `3 [ 576 -> 233 ]`", matching the block lengths exactly. Every chart block begins with `00 24 00 00 00 01 FF` and continues with repeating 4-byte groups such as `4A 00 01 FF`, `32 00 01 FF` ... The compression scheme, what the 576 raw bytes are (the test chart has 4 columns x 4 lines x 8 measures = 128 cells) and the meaning of `X` are Unknown.

## Timing model

The `SM2SDF` log shows the converter keeps `#BPMS`, `#STOPS` and `#OFFSET` ("converting BPMs / stops / offset"). Offset is in ms with an explicit sign; BPM entries are beat x 1000 / BPM x 1000 integers (3 decimals). Position->time is then StepMania's model ([sm](../../stepmania/sm/README.md#timing-model)) [inference]. Only `dance-single` appears in the sample ("difficulty 0 stepchart found"); "Copied from" in the sample `.sm` shows description handling.

## Notes

Unknown (compressed). The source chart is a 4-column `dance-single` `.sm` chart (`0` / `1`, hold/mine characters unknown).

## Audio & images

Banner and background PNGs are embedded. The audio is not in the file (`#MUSIC` is "ignored by sm2sdf"); Pocket DDR gets its music elsewhere.

## Versions & variants

Only SM2SDF v1.0 output is known: `test-1bpm.sdf` has one BPM change and a changed offset, `test.sdf` two BPMs.

## Quirks & pitfalls

- Lengths are big-endian.
- The compressed chart payload is undocumented. A decoder needs reverse engineering of Pocket DDR or `SM2SDF`.
- The leading unknown byte shifts every offset by one relative to `SDF.txt`.
- Strings are 1-byte-length-prefixed (<= 255 bytes), encoding unspecified.

## Example

First bytes of the data block of the real sample `test.sdf` (after the two PNGs), annotated:

```
01 | 00 02 04 06 0A | 09 "test song" 07 "a remix" 0B "kurt angle!" 08 "aj jelly"
   | 01 00 3C        (offset -0.060 s)
   | 00 02           (2 BPM entries)
   | 00 00 00 00  00 01 6E 72     (beat 0.000, bpm 93.810)
   | 00 00 13 88  00 02 DC E4     (beat 5.000, bpm 187.620)
   | 00 00 00 27  ...  (chart 0, 39 bytes: 00 24 00 00 00 01 FF 4A 00 01 FF 32 ...)
```

## ROX support

Not read by ROX (chart compression unknown).

## Parsers & tools

None public besides the original `SM2SDF.exe`/Pocket DDR.

## Getting samples

Committed: see [`samples/`](samples/SOURCES.md). The source `.sm` is `../../stepmania/sm/samples/stepmania-docs_test.sm`. Etterna keeps a copy in `Docs/legacy/SimfileFormats/SDF/`. Real Pocket DDR song files are not in the repositories checked; convert any `.sm` with SM2SDF if you can find the tool.

## Sources

- https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/SDF/SDF.txt
- https://github.com/stepmania/stepmania/tree/master/Docs/SimfileFormats/SDF (test.sdf, test-1bpm.sdf, test.sm, ssc-banner.png, ssc-bg.png)
- http://old.stepmania.com/forums/showthread.php?t=6621 (cited by SDF.txt; not retrieved)
