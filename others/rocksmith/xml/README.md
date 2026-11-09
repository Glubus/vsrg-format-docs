# Rocksmith 2014 arrangement XML (`.xml`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: xml

## Overview

Human-readable arrangement format of the Rocksmith Custom Song Toolkit (CST) and custom-DLC tools (EOF, DDC); converted to the binary [`sng`](../sng/README.md) when packaged into a `.psarc`. Also read by RocksmithToTab and rs2ir-converter.

## Container & encoding

UTF-8 XML, one file per arrangement (lead/rhythm/bass/vocals) with difficulty levels inside. Full schema unknown (only excerpts consulted).

## Structure / metadata
Elements (from the toolkit and tool README excerpts): `<note time="29.320" string="3" fret="9" sustain="0.253" bend="1" hammerOn="0" harmonic="0"/>`; note attributes `time` (seconds), `string` (0-5 guitar, 0-3 bass), `fret`, `sustain` (seconds), `linkNext`, technique flags (`bend`, `hammerOn`, `pullOff`, `harmonic`, `harmonicPinch`, `vibrato`, `tremolo`, ...); `bendValues`/`bendValue` children with `time` and `step`. Other elements (ebeats, phrases, sections, chord templates, levels): present in the format, details Unknown here.

## Timing model

Seconds (float); beat grid from `ebeats` [inference].

## Notes

Single notes and chords on strings with frets, sustains, linked notes, techniques.

## Audio & images

Separate `.wem`/`.ogg` in the package.

## Versions & variants

Rocksmith 2012 vs 2014 XML; "Remastered" CDLC guidelines.

## Quirks & pitfalls

Unknown.

## Example

[observed: rocksmith2014net_instrumental.xml] root `<song version="8">` with children in this order: `title`, `arrangement`, `part`, `offset`, `centOffset`, `songLength`, `startBeat`, `averageTempo`, `tuning` (attributes `string0`..`string5`), `capo`, `artistName`, `artistNameSort`, `albumName`, `albumYear`, `crowdSpeed`, `arrangementProperties`, `lastConversionDateTime`, `phrases`, `phraseIterations`, `newLinkedDiffs`, `linkedDiffs`, `phraseProperties`, `chordTemplates`, `ebeats`, `tonebase`, `tonea`..`toned`, `tones`, `sections`, `events`, `transcriptionTrack`, `levels` (each `<level difficulty="0">` with `notes`, `chords`, `anchors`, `handShapes`); a first note is `<note time="11.500" string="1" fret="0" mute="1"/>`. Arrangement files with `version="7"` exist too; vocals files are `<vocals count="67">` with `<vocal time note length lyric/>`, and `<showlights>` files carry the stage lighting. The element from the CST issue excerpt: `<note time="29.320" string="3" fret="9" sustain="0.253" bend="1" hammerOn="0" harmonic="0"/>`.

## ROX support
Not read by ROX.

## Parsers & tools
Rocksmith Custom Song Toolkit (C#): https://github.com/rscustom/rocksmith-custom-song-toolkit · RocksmithToTab: https://github.com/fholger/RocksmithToTab · rs2ir-converter: https://github.com/jermn007/rs2ir-converter

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: arrangements are authored in EOF and post-processed by DDC (the sample XML comments name both), then packed with the Rocksmith Custom Song Toolkit or DLC Builder; RocksmithToTab and rs2ir-converter read them. Official arrangements exist only as compiled `.sng` in retail `.psarc` files [inference].

## Sources
https://github.com/rscustom/rocksmith-custom-song-toolkit/issues/147 · https://github.com/rscustom/rocksmith-custom-song-toolkit/blob/master/RocksmithToolkitCLI/sng2014/Program.cs · https://github.com/jermn007/rs2ir-converter
