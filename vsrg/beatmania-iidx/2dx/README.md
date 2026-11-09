# beatmania IIDX sound archive (`.2dx`)
Kind: audio

Doc status: partial · ROX: no · Category: vsrg · Encoding: archive (binary container of audio files)

Not a chart format: the keysound container for the [`.1` chart](../1/README.md), whose events reference its samples by index.

## Overview
- IIDX ships each song's keysounds as one `.2dx` file (plus a `_pre.2dx` 10-second preview in mon/2dxTools' terms). Files are not encrypted; entries are WAV data (MS-ADPCM in 2dxTools' conversion). Other Konami games on the same engine use it (the SDVX extractor `bm2dx.py` that popntowav adapted reads it; pop'n music keysounds are `.2dx` too, see [`../../pop-n-music`](../../pop-n-music/README.md)).
- Reverse-engineered by iDestyKK/2dx_extract (C), mon/2dxTools (C: 2dxDump/2dxBuild/2dxMerge/2dxWavConvert), Gi-z/popntowav `twodx.js` (JS), SaxxonPike/iidx-datatools `2dxfix`.

## Container & encoding

- Binary, little-endian. File header followed by an offset table, then entries each starting with the magic `2DX9`.
- Header (from `twodx.js`): 16 bytes ASCII name, `u32` header length at +16, `u32` file count at +20, then the offset table begins at +72 (`offset += 52` after reading the count): `file_count` x `u32` absolute offsets of the entries.
- Entry (`Sample` class in `twodx.js`, offsets from the start of the entry):

| Offset | Size | Meaning |
| --- | --- | --- |
| +0 | 4 | magic `2DX9` (0x32 0x44 0x58 0x39) |
| +4 | 4 | `u32` entry header length, must be 24 |
| +8 | 4 | `u32` size of the audio data |
| +12 | 2 | unknown (skipped) |
| +14 | 2 | `0000` on tracks used as background tracks in pop'n files |
| +16 | 2 | `u16` unknown (attenuation in SDVX files) |
| +18 | 2 | `u16` unknown (loop point in SDVX files) |
| +20 | 4 | unknown |
| +24 | size | audio data (a complete WAV file) |

  (The iDestyKK description is equivalent: "skip 8 bytes from the `2DX9` header to get the 32-bit file size; the actual file starts 12 bytes after the size".)
- Extraction by scanning for `2DX9` works because the scanner skips over each file's data once its size is known.
- 2dxTools converts input audio to MS-ADPCM WAV with block size 256; preview files are clipped to exactly 10 s. After CS-era IIDX (CB), the engine is "a lot more sensitive to audio files that aren't 44.1 kHz stereo" (2dxfix README).

## Structure / metadata
Only the fields above. Samples have no names and are addressed by index (position in the offset table). Some games stored the keysound number in the entry header; pop'n files do not (sequential samples, per `twodx.js`).

## Timing model

Loop point/volume fields exist but are only partially understood.

## Notes

Chart `02`/`03`/`07` events index into this table. In pop'n music files the BGM track (`is_bg`) may be placed at the end of the container, so indices are shifted by one (popntowav's `offsetKeysounds`).

## Audio & images

WAV payloads (PCM/MS-ADPCM). No images.

## Versions & variants
`2DX9` is the entry magic seen in IIDX up to PENDUAL (22) per 2dx_extract; no other magics are documented. `.s3p` is a related keysound archive written by SaxxonPike's 2dxfix for newer engine versions (undocumented).

## Quirks & pitfalls
- Newer IIDX engines need 44.1 kHz stereo audio.
- Entry order matters; BGM may be first or last.
- Preserve the header length field and unknown bytes when rewriting (2dxMerge keeps loop point/volume metadata).

## Example

No binary sample is stored. First entry's magic (from the table): `32 44 58 39 | 18 00 00 00 | <size u32> | ...` (`18` = 24).

## ROX support

Not read by ROX. Keysound extraction needs a 2DX9 reader plus a WAV/MS-ADPCM decoder.

## Parsers & tools

- https://github.com/iDestyKK/2dx_extract (C)
- https://github.com/mon/2dxTools (C)
- https://github.com/Gi-z/popntowav (`twodx.js`, JS)
- https://github.com/SaxxonPike/iidx-datatools (`2dxfix`)

## Getting samples
No sample committed: searches on 2026-11-09 (Sourcegraph GitHub path search for `*.2dx`, `<id>.1`, `*_op.bin`/`*_hp.bin`/`*.ifs`; the parser/converter repositories named below; archive.org; web) found no public copy. The tools ship no fixtures and archive.org only has whole-game dumps (above the 20 MB limit) or soundtracks. A `.2dx` holds copyrighted audio from game installs, which this repository does not accept.

Real files need your own copy of the game:
- IIDX: iidx2bms (https://github.com/Glebsin/iidx2bms, commit 893a6a94b0bc442356be88852188cd5e05fe1b8e, `conversion.py`) looks for `<id>.2dx` and `<id>_pre.2dx` next to `<id>.1` in `\contents\data\sound\<id>\`, loose or inside `<id>.ifs` (unpack with mon/ifstools). Newer games use `<id>.s3p` instead of `<id>.2dx` (the code needs `.1` + `.s3p` + `_pre.2dx`). It bundles `2dx_extract` to split the container into WAV files.
- pop'n music: `popntowav.js` (Gi-z/popntowav, commit 469b6de82c6e5654eae42d130341d4c4d8b963a9) runs `ifstools` on a game `.ifs` and reads `<ifsname>_ifs/<ifsname>.2dx` (lines 21-22), so the `.2dx` is inside each song's pop'n `.ifs`.
- Readers: iDestyKK/2dx_extract, mon/2dxTools (`2dxDump`), SaxxonPike/iidx-datatools `2dxfix`.

## Sources

- https://raw.githubusercontent.com/iDestyKK/2dx_extract/master/README.md
- https://raw.githubusercontent.com/mon/2dxTools/master/README.md
- https://raw.githubusercontent.com/Gi-z/popntowav/master/twodx.js
- https://raw.githubusercontent.com/SaxxonPike/iidx-datatools/master/2dxfix/README.md
