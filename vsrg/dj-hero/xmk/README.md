# DJ Hero chart (`.xmk`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: binary (big-endian)

## Overview
`.xmk` (fsgmub/xmk) is the internal binary chart format of DJ Hero / DJ Hero 2, shared with Guitar Hero Live (maxton's XMK 010 Editor template). Early customs were authored in it directly; `djhsongjson` (MatteoGodzilla) is a JSON intermediate.

## Container & encoding
Big-endian (AnyDir wiki "XMK and FSGMUB", checked on the 13 samples): `u32 version` (2), `u32 crc32` of the bytes from offset 8 to the end of the strings, `u32 entry count`, `u32 string length`, then the entries of 16 bytes `{f32 measure, u32 type, f32 length in measures, u32 extra}`, then NUL-separated strings (the charter's name, the section names). A string is pointed at by an entry's `extra`, counted from the first entry (offset 16): `extra 0x3060` of `CUS_BINTA_DJ_Expert.xmk` is `jummy0` at file offset 0x3070. `.fsgmub` (DJ Hero) has the same layout: `djh1-customs_CUS_BINTA_Markup_Main_P1_4.fsgmub` and `djh2-customs_CUS_BINTA_DJ_Expert.xmk` hold the same 608 notes.

## Structure / metadata
From the DJ Hero Custom Chart Guide appendix (excerpted): note types 0-2 taps (green, blue, red), 3-8 directional scratches, 7-8 scratch any-direction, 9-11 crossfader (right/blue, center, left/green), 12-14 effects (green, blue, red), 15 euphoria, 32 freestyle crossfade blue marker; effect type ids `0x05FFFFFF` filter, `0x06000000` beatroll, `...01` bitreduction, `...02` wahwah, `...03` ringmod, `...04` stutter, `...05` flanger, `...06` robot, `...07` beatroll autoadvance, `...09` delay; metadata ids `0x0AFFFFFF` charter, `0x0B000002` BPM (ignored in-game), `0x0B000001` microseconds between beat markers (= 60,000,000 / bpm), `0x09FFFFFF` section/rewind checkpoint, `0xFFFFFFFF` chart start marker. Taps and directional scratches have length between 1/32 and 1/16 beat; each scratch note belongs to a scratch zone.

## Timing model
Positions and lengths are in measures (4 beats). `0x0B000001` entries give the beat length in microseconds (their `extra`) from their measure on (`CUS_MAXXUNLIMITED` has 6); `0x0B000002` holds the BPM as a float and is unused by the game.

## Notes
Note types: see Structure (AnyDir's table also lists 16 sample zone, 17 freestyle crossfade zone, 20/21 green/blue scratch zones (48/49 in DJ Hero), 22 all-lane effector (50), 23 forced centre crossfade (51), 26 battle event, 27/28/29 green/blue/centre crossfade spikes, 30 megamix transition, 31/32 freestyle markers). Taps carry a nominal length of 1/32 measure; scratches in any direction and crossfader moves carry their real length. `_Visual_Markup.xmk` files hold only `0x02xxxxxx`/`0x03xxxxxx`/`0x07xxxxxx` entries (venue markup), no notes.

## Audio & images
Unknown (audio is separate).

## Versions & variants
DJ Hero 2 xmk files include BPMs and tempo markers. DJ Hero 1 differences: Unknown.

## Quirks & pitfalls
Unknown.

## Example
Unknown.

## ROX support
Decode only, `rox::formats::djhero` (`XmkDecoder`, `DetectedFormat::Xmk`, `.xmk` and `.fsgmub`). One chart per file on 5 columns, the turntable as played: crossfader left, green, red, blue, crossfader right. Taps are taps; scratches up or down are taps on their lane (direction lost), scratches in any direction are holds over their length; crossfader moves left/right are holds on the side column, spikes taps there, the centre no note. Effectors, euphoria, zones, sections and markers are dropped and counted. Title and difficulty come from the file name (`<song>_DJ_<Difficulty>.xmk`), the charter's name is the creator. The music (`DJ.fsb`, an FMOD bank) is not read.

## Parsers & tools
djhsongjson: https://github.com/MatteoGodzilla/djhsongjson · GHL XMK 010 template: https://gist.github.com/maxton/e85e56a3a1d74ef04eed398320e8286f · DJ Hero wiki: https://github.com/shockdude/djhwiki

## Getting samples
Committed: see [samples/SOURCES.md](samples/SOURCES.md) (DJ Hero 1 `.fsgmub` and DJ Hero 2 `.xmk` customs from https://archive.org/details/DJ-HERO-CUSTOMS-ARCHIVE; chart members only, no `DJ.FSB` audio).
- [observed: djh2-customs_CUS_VADERMMT_DJ_Expert.xmk] Big-endian 32-bit words; the first word is `00000002`; `0B000001` is followed by `00082355` (= 533333 us per beat = 112.5 BPM) and `0B000002` by the float `42E10009` (= 112.5); `0AFFFFFF` (charter) and `FFFFFFFF` (start marker) are present; the file ends with the charter name as an ASCII string padded with a NUL.
- More: the archive item has ~400 more customs (zips under `DJH1_CUSTOMS/`, `DJH2_CUSTOMS_PART_1/`, `DJH2_CUSTOMS_PART_2/`; zip directories can be read with HTTP range requests). DJ Hero 2 customs install each song as a folder with `DJ.fsb` and `DJ_Expert.xmk` under `Audio/Audiotracks/` (https://github.com/shockdude/djhwiki/wiki/Installing-Custom-Songs-in-DJ-Hero-2). Sharktooth (`v0.2.2-djh2-mubtempo`, https://github.com/shockdude/Sharktooth/releases/tag/v0.2.2-djh2-mubtempo) converts `.mid` to `.fsgmub`/`.xmk`. Layout notes: https://anydir.github.io/?a=formats/official/xmkandfsgmub.

## Sources
https://docs.google.com/document/u/0/d/1tLc3qpqnEWP3X6RJJrlkVYKCAqzLCpdpXSBxsfo0-xA/mobilebasic (via search excerpts) · https://github.com/MatteoGodzilla/djhsongjson · https://thenathannator.github.io/GuitarGame_ChartFormats/Implementation-Specific/DJ-Hero-XMK/
