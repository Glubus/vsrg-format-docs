# MUSYNX / Musync chart (`.txt`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text (plaintext) / encrypted variant

## Overview
MUSYNX charts are `.txt` files; the original format list says "including plaintext and encryption". The only public implementation found is **rmstZ** (lrfasd's web converter), which reads and writes MUSYNX `.txt` charts including the encrypted ones. No standalone specification or parser source was found. The changelog of rmstZ mentions record/section names `LongNote` and `LongNoteSub`.

## Container & encoding
Plaintext `.txt` and an encrypted `.txt` variant (encryption algorithm: Unknown; rmstZ handles it).

## Structure / metadata
Unknown. From rmstZ's changelog (20211222): "fixed read of MUSYNX `LongNoteSub` dropping keysounds", "fixed write of `LongNoteSub` missing `LongNote` line", "read/write MUSYNX supports 4K charts". So a long note is expressed by a `LongNote` line plus a `LongNoteSub` line (with keysound), and keysounds exist in the format [inference].

## Timing model
Unknown.

## Notes
4K supported by rmstZ; the game also has 6K [inference: KeyTap says "6-key not yet supported"]. Taps, long notes (`LongNote`/`LongNoteSub`), slides exist in the game; encoding Unknown.

## Audio & images
Unknown.

## Versions & variants
Plaintext vs encrypted. Third-party: the KeyTap project imports its own JSON (`{bpm, gridOffset, duration, notes:[{time, lane, endTime?}]}`, ms times, lane 0-3 = D/F/J/K) into the Steam game through a MelonLoader mod; that JSON is KeyTap's format, not MUSYNX's native one.

## Quirks & pitfalls
Unknown.

## Example
None available.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (JavaScript, web): https://lrfasd.github.io/rmstZ/ · KeyTap (JS/C# mod): https://github.com/dream486/keytap-chart-recorder · bnfour mx-mods (MelonLoader mods, no chart parsing): https://github.com/bnfour/mx-mods

## Sources
https://lrfasd.github.io/rmstZ/WHATSNEW.html · https://lrfasd.github.io/rmstZ/ · https://github.com/dream486/keytap-chart-recorder · https://github.com/bnfour/mx-mods · original README line "Musync chart, including plaintext and encryption".
