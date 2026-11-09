# O2Jam music/sample container (`.ojm`)
Kind: audio

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: binary (little-endian), obfuscated/encrypted audio payloads

## Overview
OJM is the sample bank paired with an OJN of the same base name (`o2ma100.ojn` + `o2ma100.ojm`; the OJN header field `ojm_file` names it). It contains every key sound (referenced by note `value`) and background sound of the song. The client also ships OJMs that are not songs (`BGM.ojm`, `BgEffect.ojm`, `Planet.ojm`, `O2PlanetNPC.ojm`, per CXO2). Three container variants exist: **M30**, **OMC** and **OJM** (the latter two share a layout). The reference is the Open2Jam OJM documentation and `OJMParser.java`.

## Container & encoding
- Little-endian. 4-byte signature: `"M30\0"` (int `0x0030334D`), `"OMC\0"` (`0x00434D4F`) or `"OJM\0"` (`0x004D4A4F`).
- No compression. Audio payloads are OGG (M30; OMC/OJM OGG section) or headerless PCM (OMC/OJM WAV section), possibly obfuscated.

### M30
28-byte header (Open2Jam doc and parser):

| Offset | Type | Field |
|---|---|---|
| 0 | char[4] | `"M30\0"` |
| 4 | int32 | file_format_version |
| 8 | int32 | encryption_flag |
| 12 | int32 | sample_count (do not trust: counts differ from the real number of samples) |
| 16 | int32 | samples_offset (usually 28) |
| 20 | int32 | payload_size (usually file size - 28) |
| 24 | int32 | padding |

Then, per sample, a 52-byte header followed by `sample_size` bytes:

| Offset | Type | Field |
|---|---|---|
| 0 | char[32] | sample_name (if no `.`, Open2Jam appends `.ogg`) |
| 32 | int32 | sample_size |
| 36 | int16 | codec_code: 5 = key sound (W###), 0 = background sound (M###) |
| 38 | int16 | unk_fixed (2nd half of what MrKishi calls an int codec) |
| 40 | int32 | music_flag (unknown) |
| 44 | int16 | ref: the sample id |
| 46 | int16 | unk_zero |
| 48 | int32 | pcm_samples (total PCM samples of the OGG) |

Open2Jam id mapping: `id = ref` for codec 5, `id = 1000 + ref` for codec 0. This matches the OJN rule: note `value-1`, plus 1000 when the note type has bit 2 (see [ojn](../ojn/README.md)). Stop when fewer than 52 bytes remain.

`encryption_flag` (documented values: 1 scramble1, 2 scramble2, 4 decode, 8 decrypt, 16 nami; found via disassembly by "vittee" per the comments; parser acts on):
- `0`: plain OGG.
- `16`: XOR with `"nami"` (`6E 61 6D 69`), repeated every 4 bytes; trailing bytes (len % 4) are not XORed.
- `32`: XOR with `"0412"` (`30 34 31 32`), same procedure (Open2Jam parser `mask_0412`; flag 32 is not in the blog doc).
- other: logged unknown. render-ojn lists support for flags 0/16/32.
After XOR the data is a normal OGG Vorbis stream.

### OMC / OJM
20-byte header:

| Offset | Type | Field |
|---|---|---|
| 0 | char[4] | `"OMC\0"` or `"OJM\0"` |
| 4 | int16 | wav_count |
| 6 | int16 | ogg_count |
| 8 | int32 | wav_start (usually 20) |
| 12 | int32 | ogg_start |
| 16 | int32 | filesize |

WAV section (from 20 to `ogg_start`): repeated 56-byte header + `chunk_size` bytes:

| Offset | Type | Field |
|---|---|---|
| 0 | char[32] | sample_name (default `.wav`) |
| 32 | int16 | audio_format |
| 34 | int16 | num_channels |
| 36 | int32 | sample_rate |
| 40 | int32 | bit_rate (byte rate) |
| 44 | int16 | block_align |
| 46 | int16 | bits_per_sample |
| 48 | int32 | data (unknown) |
| 52 | int32 | chunk_size |

If `chunk_size` is 0 the slot is empty but still consumes an id (`sample_id++`; WAV ids start at 0). Payload is raw PCM without WAV header: build the WAV header from the fields above. In **OMC** (signature `OMC`) payload is obfuscated; in **OJM** it is not (Open2Jam: `parseOMC(f, decrypt = signature==OMC)`).

OGG section (from `ogg_start` to `filesize`): repeated 36-byte header (`char[32] name` default `.ogg`, `int32 sample_size`) + OGG bytes, no obfuscation. Ids start at 1000, `sample_size == 0` also consumes an id.

OMC deobfuscation (two steps, per chunk; both from `OJMParser.java`):
1. `rearrange` (verified in the parser source): `length = chunk size`, `key = ((length % 17) << 4) + (length % 17)`, `block_size = length / 17`. Start from a copy of the encoded chunk (remainder bytes beyond 17*block_size stay in place). For `block = 0..16`: copy `block_size` bytes from encoded offset `block_size*block` to plain offset `block_size * REARRANGE_TABLE[key]`, then `key++`. `REARRANGE_TABLE` is a fixed byte table of values 0..16 hard-coded in `OJMParser.java` (a dump from debugging NoteTool); copy it from there.
2. `OMC_xor` ("acc xor", not a true XOR; state `acc_keybyte = 0xFF`, `acc_counter = 0` initialised once per file and carried across samples): for each byte `b`: `t = b; if ((acc_keybyte << acc_counter) & 0x80) b = ~b; acc_counter++; if (acc_counter > 7) { acc_counter = 0; acc_keybyte = t }`. MrKishi in the blog comments notes it is not symmetric, the repo version is the encoder, and the state must be carried correctly across the loop end.

## Structure / metadata
No metadata beyond sample names, ids and (WAV) audio format. All ids are given by position/`ref`, see above. Key samples are W###; background (autoplay) samples are M###.

## Timing model
Not applicable (no timing).

## Notes
Not applicable. The OJN event `value` indexes this bank.

## Audio & images
Audio only: OGG Vorbis or PCM WAV (rebuilt). No images.

## Versions & variants
M30 flags 0/16/32 (+ `1,2,4,8` documented as scramble/decode/decrypt by disassembly, support status unknown), OMC (obfuscated WAV) and OJM (plain WAV) containers, O2Jam China songs possibly Blowfish encrypted (Open2Jam doc: "the new o2china songs, which apparently uses blowfish encryption?"). render-ojn also mentions sparse OMC/OJM directory slots.

## Quirks & pitfalls
- `sample_count`/`wav_count`/`ogg_count` are unreliable; use offsets and `filesize`.
- Empty slots still consume ids.
- XOR masks apply only to full 4-byte groups.
- `acc_xor` state must be kept across samples of the same file.

## Example
Not applicable: binary; no hand-built example to avoid inventing bytes.

## ROX support
Read by ROX since Prism's addition of `rox::formats::o2jam::OjmContainer` (M30 flags 0/16/32, OMC, OJM; the WAV samples come out as complete RIFF files; no audio decoding in ROX). Other M30 flags are an error. The rearrangement table was compared entry by entry between Open2Jam's parser and CXO2's `OmcArchive` (identical, 290 entries). Tested only on containers built in memory: this repository has no `.ojm` file and none with a licence that allows it was found, so the scrambles are verified by hand-computed vectors and round trips, not on a real file. Source: `rhythm-open-exchange/src/formats/o2jam/ojm.rs`. In Prism the container is read by `crates/chart_audio` (`docs/rendu-audio.md`, "Conteneurs"): each sample a `.ojn` plays is decoded from its bytes (WAV or Ogg) and mixed into the chart's rendered track; the container is found by the header's name (any case) or the same stem with `.ojm`.

## Parsers & tools
- Open2Jam OJM parser (Java): https://github.com/open2jamorg/open2jam/blob/master/parsers/src/org/open2jam/parsers/OJMParser.java ; ojm_dumper (Java): https://github.com/open2jamorg/open2jam/tree/master/tools/ojm_dumper
- render-ojn (Node): https://github.com/djzmo/render-ojn ; o2jam_utils (Python): https://github.com/djask/o2jam_utils ; CXO2: https://github.com/SirusDoma/CXO2

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): eleven tiny **synthetic** containers from djzmo/render-ojn (GPL-3.0): M30 with flags 0/16/32 and malformed variants, an `OJM\0` file with a zero-length PCM slot and one with trailing empty OGG records. They carry no real audio.
- **Not committed**: real OJM files hold the game's audio (copyright); none is listed in the manifest. No `OMC\0` example is available.
- **How to get real ones**: every OJN has a sibling `o2ma<id>.ojm` in the client's `Music/` folder (and the client's `BGM.ojm`, `BgEffect.ojm`, `Planet.ojm`, `O2PlanetNPC.ojm`, fiche); the Server Two music pack in [ojn samples](../ojn/samples/README.md) is the community source of OJN+OJM pairs. Extract with https://github.com/SirusDoma/CXO2 (`OjmArchive`, `OmcArchive`, `M30Archive` headers), the Open2Jam `OJMParser.java`, or `render-ojn` (renders OJN+OJM to audio). The render-ojn private-fixture notes report that real packs mix M30 (most), OMC and OJM variants.

## Sources
- https://open2jam.wordpress.com/the-ojm-documentation/
- https://raw.githubusercontent.com/open2jamorg/open2jam/master/parsers/src/org/open2jam/parsers/OJMParser.java
- https://github.com/SirusDoma/CXO2/blob/develop/docs/file-format/FileFormat.md
- https://github.com/djzmo/render-ojn
