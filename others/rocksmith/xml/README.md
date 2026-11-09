# Rocksmith 2014 arrangement XML (`.xml`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: xml

## Overview
The human-readable arrangement format used by the Rocksmith Custom Song Toolkit (CST) and custom-DLC authoring tools (EOF, DDC); converted to the binary [`sng`](../sng/README.md) when packaged into a `.psarc`. Also read by converters (RocksmithToTab, rs2ir-converter).

## Container & encoding
XML, UTF-8; one file per arrangement (lead/rhythm/bass/vocals) and difficulty levels inside it. Full schema: Unknown here (only excerpts consulted).

## Structure / metadata
Elements (from the toolkit and tool README excerpts): `<note time="29.320" string="3" fret="9" sustain="0.253" bend="1" hammerOn="0" harmonic="0"/>`; note attributes `time` (seconds), `string` (0-5 guitar, 0-3 bass), `fret`, `sustain` (seconds), `linkNext`, technique flags (`bend`, `hammerOn`, `pullOff`, `harmonic`, `harmonicPinch`, `vibrato`, `tremolo`, ...); `bendValues`/`bendValue` children with `time` and `step`. Other elements (ebeats, phrases, sections, chord templates, levels): present in the format, details Unknown here.

## Timing model
Times are in seconds (floating point), beat grid from `ebeats` [inference]. 

## Notes
Single notes and chords on strings with fret numbers, sustains, linked notes, techniques. 

## Audio & images
Audio is a separate `.wem`/`.ogg` in the package. Unknown.

## Versions & variants
Rocksmith 2012 vs 2014 XML; "Remastered" CDLC guidelines. Unknown.

## Quirks & pitfalls
Unknown.

## Example
Single element from the CST issue excerpt: `<note time="29.320" string="3" fret="9" sustain="0.253" bend="1" hammerOn="0" harmonic="0"/>`.

## ROX support
Not read by ROX.

## Parsers & tools
Rocksmith Custom Song Toolkit (C#): https://github.com/rscustom/rocksmith-custom-song-toolkit · RocksmithToTab: https://github.com/fholger/RocksmithToTab · rs2ir-converter: https://github.com/jermn007/rs2ir-converter

## Sources
https://github.com/rscustom/rocksmith-custom-song-toolkit/issues/147 · https://github.com/rscustom/rocksmith-custom-song-toolkit/blob/master/RocksmithToolkitCLI/sng2014/Program.cs · https://github.com/jermn007/rs2ir-converter
