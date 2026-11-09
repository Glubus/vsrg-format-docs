# MUSYNX / Musync chart (`.txt`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: text (plaintext) / encrypted variant

## Overview

MUSYNX charts are `.txt` files ("including plaintext and encryption" per the original format list). The only public implementation found is rmstZ (lrfasd's web converter), which reads and writes them, encrypted ones included. No standalone specification or parser source exists. rmstZ's changelog mentions record/section names `LongNote` and `LongNoteSub`.

## Container & encoding

Plaintext `.txt` and an encrypted `.txt` variant (algorithm Unknown; rmstZ handles it).

## Structure / metadata
Unknown. From rmstZ's changelog (20211222): "fixed read of MUSYNX `LongNoteSub` dropping keysounds", "fixed write of `LongNoteSub` missing `LongNote` line", "read/write MUSYNX supports 4K charts". So a long note is expressed by a `LongNote` line plus a `LongNoteSub` line (with keysound), and keysounds exist in the format [inference].

## Timing model

Unknown.

## Notes

4K supported by rmstZ; the game also has 6K [inference: KeyTap says "6-key not yet supported"]. Taps, long notes (`LongNote`/`LongNoteSub`) and slides exist in the game; encoding Unknown.

## Audio & images

Unknown.

## Versions & variants

Plaintext vs encrypted. The KeyTap project imports its own JSON (`{bpm, gridOffset, duration, notes:[{time, lane, endTime?}]}`, ms times, lane 0-3 = D/F/J/K) into the Steam game through a MelonLoader mod; that JSON is KeyTap's format, not MUSYNX's.

## Quirks & pitfalls

Unknown.

## Example

None.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (JavaScript, web): https://lrfasd.github.io/rmstZ/ · KeyTap (JS/C# mod): https://github.com/dream486/keytap-chart-recorder · bnfour mx-mods (MelonLoader mods, no chart parsing): https://github.com/bnfour/mx-mods

## Getting samples

Committed: none. Searched: dream486/keytap-chart-recorder (its `charts/*.json` is its own JSON, `{version, keys, title, bpm, duration, notes[{time, lane}]}`) and bnfour/mx-mods (game mods only); neither contains a `.txt` chart.

How to get one: the game MUSYNX (Steam / Switch) stores per-chart `.txt` files in its asset data (plaintext and encrypted); extract them with a Unity asset tool and open with rmstZ (https://lrfasd.github.io/rmstZ/) [inference]. KeyTap (https://github.com/dream486/keytap-chart-recorder) advertises a MUSYNX integration; see its README.

## Sources
https://lrfasd.github.io/rmstZ/WHATSNEW.html · https://lrfasd.github.io/rmstZ/ · https://github.com/dream486/keytap-chart-recorder · https://github.com/bnfour/mx-mods · original README line "Musync chart, including plaintext and encryption".
