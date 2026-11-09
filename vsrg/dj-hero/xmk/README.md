# DJ Hero chart (`.xmk`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview
`.xmk` (fsgmub/xmk) is the internal binary chart format of DJ Hero / DJ Hero 2; early DJ Hero custom songs were authored directly in it. A JSON intermediate (`djhsongjson`, MatteoGodzilla) exists for customs. A Guitar Hero Live XMK 010 Editor template (maxton) also exists, so the format is shared with GHL.

## Container & encoding
Binary; hierarchical structure with hex-coded markers (details only from community guide excerpts). Layout, endianness: Unknown here.

## Structure / metadata
Known fields from the DJ Hero Custom Chart Guide appendix (as excerpted): note types 0-2 taps (green, blue, red), 3-8 directional scratches, 7-8 scratch any-direction, 9-11 crossfader (right/blue, center, left/green), 12-14 effects (green, blue, red), 15 euphoria, 32 freestyle crossfade blue marker; effect type ids `0x05FFFFFF` filter, `0x06000000` beatroll, `...01` bitreduction, `...02` wahwah, `...03` ringmod, `...04` stutter, `...05` flanger, `...06` robot, `...07` beatroll autoadvance, `...09` delay; metadata ids `0x0AFFFFFF` charter, `0x0B000002` BPM (ignored in-game), `0x0B000001` microseconds between beat markers (= 60,000,000 / bpm), `0x09FFFFFF` section/rewind checkpoint, `0xFFFFFFFF` chart start marker. Taps and directional scratches have length between 1/32 and 1/16 beat; each scratch note belongs to a scratch zone.

## Timing model
Tempo markers (`0x0B000001`: microseconds per beat). Rest Unknown.

## Notes
See Structure (note types listed there). Remaining details: Unknown.

## Audio & images
Unknown (audio is separate from the chart).

## Versions & variants
DJ Hero 2 xmk files include BPMs and tempo markers; DJ Hero 1 differences: Unknown.

## Quirks & pitfalls
Unknown.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
djhsongjson: https://github.com/MatteoGodzilla/djhsongjson · GHL XMK 010 template: https://gist.github.com/maxton/e85e56a3a1d74ef04eed398320e8286f · DJ Hero wiki: https://github.com/shockdude/djhwiki

## Getting samples
- Committed in [`samples/`](samples/SOURCES.md): 13 real files taken from the Internet Archive item "DJ HERO CUSTOMS ARCHIVE" (https://archive.org/details/DJ-HERO-CUSTOMS-ARCHIVE): DJ Hero 2 `DJ_Expert.xmk` of five different customs (1.1 KB to 19 KB), the five difficulty files `DJ_Beginner/Easy/Medium/Hard/Expert.xmk` of one custom, a `Visual_Markup.xmk`, and two DJ Hero 1 `.fsgmub` markup files. Only the chart members were read out of the customs' zips (HTTP range requests); audio (`DJ.FSB`) is not stored.
- Observed in the committed files [observed in samples/djh2-customs_CUS_VADERMMT_DJ_Expert.xmk]: big-endian 32-bit words; the first word is `00000002`; the `0B000001` metadata id is followed by `00082355` (= 533333 us per beat = 112.5 BPM) and `0B000002` by the float `42E10009` (= 112.5), consistent with the metadata ids listed above; `0AFFFFFF` (charter) and `FFFFFFFF` (start marker) ids are present; the file ends with an ASCII string (the charter name) padded with a NUL.
- More: the archive item has ~400 more customs (zips under `DJH1_CUSTOMS/`, `DJH2_CUSTOMS_PART_1/`, `DJH2_CUSTOMS_PART_2/`; zip central directories can be read with HTTP range requests); DJ Hero 2 customs install each song as a folder with `DJ.fsb` and `DJ_Expert.xmk` under `Audio/Audiotracks/` (https://github.com/shockdude/djhwiki/wiki/Installing-Custom-Songs-in-DJ-Hero-2); Sharktooth (`v0.2.2-djh2-mubtempo`, https://github.com/shockdude/Sharktooth/releases/tag/v0.2.2-djh2-mubtempo) converts `.mid` to `.fsgmub`/`.xmk`; layout notes: https://anydir.github.io/?a=formats/official/xmkandfsgmub.

## Sources
https://docs.google.com/document/u/0/d/1tLc3qpqnEWP3X6RJJrlkVYKCAqzLCpdpXSBxsfo0-xA/mobilebasic (via search excerpts) · https://github.com/MatteoGodzilla/djhsongjson · https://thenathannator.github.io/GuitarGame_ChartFormats/Implementation-Specific/DJ-Hero-XMK/
