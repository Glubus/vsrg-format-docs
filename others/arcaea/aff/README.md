# Arcaea chart (AFF) (`.aff`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text

## Overview

The chart file of Arcaea (lowiro), one file per difficulty (`0.aff` Past, `1.aff` Present, `2.aff` Future, `3.aff` Beyond, `4.aff` Eternal in the song folder [inference from community usage; the consulted parser sources do not name the files]). The format is a metadata header followed by a flat list of `name(args);` events; it is also the base of the ArcCreate and ArcadeZero editors, which extend it. The description below comes from the lexer/parser/checkers of the VS Code AFF extension (yojohanshinwataikei) and ArcCreate's `AffChartReader` source, not from an official spec.

## Packaged in

- Packaged in [`arcpkg`](../arcpkg/).

## Container & encoding

Plain text, one event per line ending with `;`, newline LF or CRLF. Metadata header, then a line containing only `-`, then events. Charset not specified (ASCII in practice). Whitespace between tokens is ignored in the main part. In the game package the files live as `songs/<song id>/<n>.aff`; in ArcCreate the chart path is configured in `project.arcproj` (see `../arcpkg/`).

## Structure / metadata

Header: lines `Key:Value` until a line `-`.

| Key | Type | Meaning |
|---|---|---|
| `AudioOffset` | int (ms) | audio offset; if missing, treated as 0; non-int is an error |
| `TimingPointDensityFactor` | float > 0 | multiplier for the density of generated timing (judgement) points of holds/arcs; ArcCreate also accepts the spelling `TimingPointsDensityFactor` |

Any other header key is ignored by the game.

Events (every event ends with `;`; values: int, float with decimal point, or bare word):

| Event | Fields | Notes |
|---|---|---|
| `timing(t,bpm,beats);` | `t` int ms, `bpm` float, `beats` float (beats per measure) | a timing event with non-zero bpm must have non-zero beats; bpm 0 is allowed with beats 0 (used as a "pause"/reset trick) |
| `(t,lane);` | `t` int ms, `lane` int | Tap on the floor lane |
| `hold(t1,t2,lane);` | start/end int ms, lane | Hold; must have positive length |
| `arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,isVoid[,smoothness])[arctap(t),...];` | see below | Arc and optional Arc Taps in `[...]` |
| `camera(t,tx,ty,tz,rx,ry,rz,kind,duration);` | exactly 9 fields | camera move; `kind` in `l`, `s`, `qi`, `qo`, `reset` |
| `scenecontrol(t,kind[,args...]);` | | scene effect, see below |
| `timinggroup(attrs){ ...events... };` | | group with its own timing, see below |

Arc fields: `t1`,`t2` int ms (`t1 <= t2`); `x1`,`x2`,`y1`,`y2` floats; `easing` word in `b`, `s`, `si`, `so`, `sisi`, `siso`, `soso`, `sosi`; `color` int (parser accepts 0..3; 0..4 in the type; solid arcs must not use colour >= 4); `hitsound` word `none` or `<name>_wav` (a sound file in the song folder); `isVoid` word `true`/`false`/`designant`: `true` = trace (void, thin) arc, `false` = solid arc, `designant` = a special rendering of void arcs (used by the song of that name); optional 11th field `smoothness` float (ArcCreate calls it arc resolution multiplier, default 1).

Arc Taps: `arctap(t)` with `t` in `[t1, t2]` of its arc, only valid on arcs with `isVoid` != `false` (an arc with arctaps is treated as non-solid even if declared solid). ArcCreate also accepts `arctap(t,width)`.

Valid ranges (checkers, not game rules): floor lanes are `1..4`; lanes `0` and `5` exist only while `enwidenlanes` is on. Arc points must lie in the "trapezium": `0 <= y <= 1`, `2x + y <= 3`, `2x - y >= -1` (i.e. x from about -0.5 to 1.5 at y = 0); with `enwidencamera` on the limits are `y <= 1.61`, `161x + 75y <= 322`, `161x - 75y >= -161`. Arcs of zero length must be `s` easing with different start/end points and no arctaps.

Scenecontrol kinds known to the checker: `trackshow`, `trackhide` (no args); `redline`, `arcahvdistort`, `arcahvdebris`, `hidegroup`, `enwidencamera`, `enwidenlanes`, `trackdisplay` (2 args: length float, value int). ArcadeZero documents `scenecontrol(timing, trackdisplay, duration, alpha)`, `hidegroup` (alpha of notes in the same timing group), `enwidenlanes` and `enwidencamera` (0 off / 1 on, ms duration). Other kinds are unknown to the checkers.

Timing group attributes: `noinput`, `fadingholds`, `anglex<digits>`, `angley<digits>`; all other attributes trigger a warning (unknown). Items allowed inside: timing, tap, hold, arc, scenecontrol, camera. Groups end with `};`. ArcCreate additionally supports `include(file);` and `fragment(...);` lines.

## Timing model

- Times are integer milliseconds on the song timeline; `AudioOffset` shifts audio vs chart [sign convention not stated in the consulted sources].
- `timing(t,bpm,beats)` events define BPM; the default (base) timing group is the main timeline. A beat lasts `60000/bpm` ms and a measure has `beats` beats; the timing track also determines the spacing of the scoring ticks of holds and arcs (scaled by `TimingPointDensityFactor`).
- A `timinggroup` contains its own `timing` events: notes inside move independently according to that group's BPM (used for scroll-speed tricks, `angle*` rotation of the group etc.). Hold/arc spans cut by a timing change are flagged by checkers (cut-by-timing).
- Arc position along its duration: interpolate `(x,y)` from `(x1,y1)` to `(x2,y2)` using the easing: `s` straight (linear), `b` Bezier curve, `si`/`so` sine in/out; the four-letter variants `sisi`, `siso`, `soso`, `sosi` combine two of these [inference: the consulted sources list the names but do not define the exact x/y shape]; ArcadeZero notes that `so` actually behaves like `si` (fast then slow) in the real game.

## Notes

- Floor Tap `(t,lane)`; Hold `hold(t1,t2,lane)`; Arc Tap = point on a void arc at time `t` (its position is interpolated from the arc).
- Arc colour ids select the blue/red/(green) hand [inference]; void arcs (`true`) do not require taps and can carry arctaps; solid arcs (`false`) require holding along the curve.
- No keysounds except the per-arc `hitsound` (`none` or `<name>_wav`).
- Simultaneous notes: same `t` on several events; no special flag.

## Audio & images

The chart references only hitsound names of arcs. Song audio (`base.ogg`), jacket (`base.jpg`), background and `songlist` entries are outside the `.aff` (see `../songlist/`).

## Versions & variants

- Official game dialect (scenecontrol, timinggroup, camera were added over versions).
- **ArcadeZero / Arcade** editor: adds scripted scenecontrol via Lua channels ("ArcadeScenecontrol"), departs from official scenecontrol arguments for consistency.
- **ArcCreate**: reads `.aff` plus `include`/`fragment` extensions, `arctap(t,width)`, arc resolution (11th arc field); stores projects in `project.arcproj` / packs `.arcpkg`.
- Converters: Etoile/EtoileResurrection (`.aff` <-> ArcCreate packages), arcfutil (Python, `.aff` toolkit), Lanotalium/Layesta imports `.aff` for Lanota.

## Quirks & pitfalls

- Floats must contain a decimal point (`1.00`), ints must not; the lexer distinguishes them (`-?[0-9]+\.[0-9]+` vs `-?(0|[1-9][0-9]*)`).
- The header terminator is a line consisting of `-` exactly.
- Timing group lines end with `};`; nested events are indented but whitespace is not significant.
- Arc taps outside the arc time range are errors in ArcCreate.
- `isVoid` is textual (`true`, `false`, `designant`), not boolean 0/1.
- bpm 0 / beats 0 timing events have special meaning; do not divide by zero.

## Example

Illustrative, hand-built from the event grammar above (not taken from a real song):

```text
AudioOffset:0
TimingPointDensityFactor:1
-
timing(0,120.00,4.00);
(1000,2);
hold(2000,2500,3);
arc(3000,3500,0.00,1.00,s,1.00,1.00,0,none,false);
arc(3000,3500,0.50,0.50,s,0.00,0.00,1,none,true)[arctap(3250)];
```

## ROX support

Not read by ROX.

## Parsers & tools

- VS Code AFF extension (TypeScript, chevrotain lexer/parser, checkers): <https://github.com/yojohanshinwataikei/vscode-arcaea-file-format>
- ArcCreate editor/player (C#, Unity): <https://github.com/Arcthesia/ArcCreate> (`Assets/Scripts/ChartFormat/Aff/`)
- ArcadeZero scenecontrol docs: <https://github.com/Tempestissiman/ArcadeScenecontrol>
- arcfutil (Python): <https://pypi.org/project/arcfutil>
- ArcaeaChartRender (Python, preview): <https://github.com/Arcaea-Infinity/ArcaeaChartRender>
- EtoileResurrection (Kotlin/Java, .aff <-> ArcCreate): <https://github.com/freeze-dolphin/EtoileResurrection>
- AFFKit (.NET): listed in search results, not inspected.

## Sources

- <https://raw.githubusercontent.com/yojohanshinwataikei/vscode-arcaea-file-format/master/server/src/lexer.ts>, `parser.ts`, `types.ts`, `to-ast.ts`, `checker/metadata.ts`, `checker/value-range.ts`, `checker/arc-position.ts`, `checker/extra-lanes.ts`, `checker/scenecontrol.ts`, `checker/timinggroup-attribute.ts`
- <https://raw.githubusercontent.com/Arcthesia/ArcCreate/trunk/Assets/Scripts/ChartFormat/Aff/AffChartReader.File.cs> and `AffChartReader.Line.cs`
- <https://github.com/Tempestissiman/ArcadeScenecontrol>
