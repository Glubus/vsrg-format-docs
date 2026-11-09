# DanceRail chart (`.drb`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview

`.drb` is the chart file made by DanceRail's editor DRMaker and imported into the Android game (Dancerail_Import: "your files (ogg and drb)"). No official spec exists. The only open grammar is the text chart format that DR3Editor reads/writes ("official format", exported as `.txt`; its `levelFormat.ts` parser and validator). Whether `.drb` is byte-identical to that `.txt` is **[inference]**, not verified.

## Container & encoding

Text, one record per line, `;`-terminated header lines; note lines are bracket groups. Companion: `.ogg` audio (required by DanceRail3).

## Structure / metadata

```
#OFFSET=<float seconds>;      (DR3Editor: stored as -offset_ms/1000)
#BEAT=1;
#BPM_NUMBER=<n>;
#BPM [i]=<bpm>;
#BPMS[i]=<position>;          (position of the change, in measures)
#SCN=<n>;                     speed-change count
#SC [i]=<ratio>;
#SCI[i]=<position>;
<id><type><pos><x><width><speed><parentId>[<appearMode>]
```

Note line (e.g. `<12><1><3.5><0.5><1><1><0>`): `id` int; `type` int; `pos` = measure + beat/beatsPerMeasure (float, measures); `x` float horizontal lane position; `width` float; `speed` string/number; `parentId` (0 for non-linked; hold center/end notes point to their parent); optional `appearMode` in `L R H P N`.

Note types (DR3Editor names): 1 Blue Tap, 2 Yellow Tap, 3 Orange Hold Start, 4 Orange Hold End, 5 Blue Hold Start, 6 Blue Hold Center, 7 Blue Hold End, 9 Circle Flick, 10 Damage, 11 Orange Hold Center, 13-16 Flick Left/Right/Up/Down, 17 Damage Middle, 18 Damage End, 19/20 Green Hold Center/End, 21/22 Yellow, 23/24 Pink, 25/26/27 2/3/4-Finger Tap.

## Timing model

BPM list with change positions in measures; the editor converts `pos*4` beats to time through the BPM table. Speed changes (`#SC/#SCI`) alter note scroll speed. Offset negated seconds.

## Notes

Continuous x position + width, holds as start/center/end chains linked by `parentId`, flicks, damage notes, multi-finger taps. This does not fit a fixed-column model.

## Audio & images

`.ogg` only; illustration separate (editor manifest `manifest.json` in zip bundles, not part of the chart).

## Versions & variants

DRMaker official format with 25 note types ("new 25-27 note types" per DR3Editor); DR3FP/viewer exports.

## Quirks & pitfalls

Validator requires 7 or 8 bracket groups; header keys have a space before `[` for `#BPM [i]` and `#SC [i]`.

## Example

Illustrative from the grammar above:

```
#OFFSET=0;
#BEAT=1;
#BPM_NUMBER=1;
#BPM [0]=120;
#BPMS[0]=0;
#SCN=0;
<0><1><1><0.5><1><1><0>
```

## ROX support

Not read by ROX; lossy conversion (free x/width).

## Parsers & tools

DR3Editor (TypeScript), DanceRail3Viewer (C#), Dancerail_Import (Python).

## Getting samples

- **Committed**: 3 real charts (`bluemelody.N.txt` from DanceRail3Viewer, no licence) plus 1 synthetic in [`samples/`](samples/). Origin, author, date, sha256 and licence/terms of each file are in [`samples/SOURCES.md`](samples/SOURCES.md).
- **More samples**: install DanceRail3 (Android) and use the DRMaker editor (`DRmaker(3.13).exe` is in the DanceRail3Viewer repo under `Assets/Resources/`); DR3Editor (https://github.com/swordalt/DR3Editor) reads/writes the same text grammar.

## Sources

- https://github.com/swordalt/DR3Editor (src/utils/levelFormat.ts, src/lang/en.ts, PROJECT_OVERVIEW.md)
- https://github.com/Krydar/Dancerail_Import
- https://github.com/lucarioex/DanceRail3Viewer
