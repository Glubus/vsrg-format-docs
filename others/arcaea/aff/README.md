# Arcaea chart (AFF) (`.aff`)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: text

## Overview
Arcaea chart, one file per difficulty: `0.aff` Past, `1.aff` Present, `2.aff` Future, `3.aff` Beyond, `4.aff` Eternal in the song folder [inference from community usage]. A metadata header is followed by a flat list of `name(args);` events. Source: lexer/parser/checkers of the VS Code AFF extension and ArcCreate's `AffChartReader`, not an official spec.

## Packaged in

- `.arcpkg` (ArcCreate zip: `index.yml`, `*.arcproj`, `.aff` charts, audio, jacket, background).

## Container & encoding
Plain text, one event per line ending with `;`, LF or CRLF. Metadata header, a line of only `-`, then events. ASCII in practice; whitespace between tokens is ignored. In the game package files live as `songs/<song id>/<n>.aff`; ArcCreate sets the chart path in `project.arcproj` (see `../arcpkg/`).

## Structure / metadata

Header: lines `Key:Value` until a line `-`.

| Key | Type | Meaning |
|---|---|---|
| `AudioOffset` | int (ms) | audio offset; 0 if missing; non-int is an error |
| `TimingPointDensityFactor` | float > 0 | multiplier for the density of generated timing (judgement) points of holds/arcs; ArcCreate also accepts the spelling `TimingPointsDensityFactor` |

The game ignores any other header key.

Events (each ends with `;`; values: int, float with decimal point, or bare word):

| Event | Fields | Notes |
|---|---|---|
| `timing(t,bpm,beats);` | `t` int ms, `bpm` float, `beats` float (beats per measure) | non-zero bpm needs non-zero beats; bpm 0 is allowed with beats 0 (a "pause"/reset trick) |
| `(t,lane);` | `t` int ms, `lane` int | Tap on the floor lane |
| `hold(t1,t2,lane);` | start/end int ms, lane | Hold; must have positive length |
| `arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,isVoid[,smoothness])[arctap(t),...];` | see below | Arc and optional Arc Taps in `[...]` |
| `camera(t,tx,ty,tz,rx,ry,rz,kind,duration);` | exactly 9 fields | camera move; `kind` in `l`, `s`, `qi`, `qo`, `reset` |
| `scenecontrol(t,kind[,args...]);` | | scene effect, see below |
| `timinggroup(attrs){ ...events... };` | | group with its own timing, see below |

Arc fields:

- `t1`,`t2`: int ms (`t1 <= t2`). `x1`,`x2`,`y1`,`y2`: floats.
- `easing`: `b`, `s`, `si`, `so`, `sisi`, `siso`, `soso`, `sosi`.
- `color`: int (parser accepts 0..3; 0..4 in the type; solid arcs must not use colour >= 4).
- `hitsound`: `none` or `<name>_wav` (a sound file in the song folder).
- `isVoid`: `true` = trace (void, thin) arc, `false` = solid arc, `designant` = special rendering of void arcs (used by the song of that name).
- Optional 11th field `smoothness` float (ArcCreate: arc resolution multiplier, default 1).

Arc Taps: `arctap(t)` with `t` in `[t1, t2]` of its arc, valid only on arcs with `isVoid` != `false` (an arc with arctaps is treated as non-solid even if declared solid). ArcCreate also accepts `arctap(t,width)`.

Valid ranges (checkers, not game rules): floor lanes are `1..4`; lanes `0` and `5` exist only while `enwidenlanes` is on. Arc points must lie in the "trapezium": `0 <= y <= 1`, `2x + y <= 3`, `2x - y >= -1` (x about -0.5 to 1.5 at y = 0). With `enwidencamera` on: `y <= 1.61`, `161x + 75y <= 322`, `161x - 75y >= -161`. Zero-length arcs must use `s` easing with different start/end points and no arctaps.

Scenecontrol kinds known to the checker: `trackshow`, `trackhide` (no args); `redline`, `arcahvdistort`, `arcahvdebris`, `hidegroup`, `enwidencamera`, `enwidenlanes`, `trackdisplay` (2 args: length float, value int). ArcadeZero documents `scenecontrol(timing, trackdisplay, duration, alpha)`, `hidegroup` (alpha of notes in the same timing group), `enwidenlanes` and `enwidencamera` (0 off / 1 on, ms duration). Other kinds are unknown to the checkers.

Timing group attributes: `noinput`, `fadingholds`, `anglex<digits>`, `angley<digits>`; any other attribute triggers an unknown warning. Allowed inside: timing, tap, hold, arc, scenecontrol, camera. Groups end with `};`. ArcCreate also supports `include(file);` and `fragment(...);` lines.

## Timing model
- Integer milliseconds on the song timeline. `AudioOffset` shifts audio against the chart [sign convention not stated].
- `timing(t,bpm,beats)` sets BPM in the default (base) timing group. A beat lasts `60000/bpm` ms, a measure has `beats` beats. The timing track also spaces hold/arc scoring ticks (scaled by `TimingPointDensityFactor`).
- A `timinggroup` has its own `timing` events; its notes move by that BPM (scroll-speed tricks, `angle*` rotation). Checkers flag hold/arc spans cut by a timing change.
- Arc position: interpolate `(x,y)` from `(x1,y1)` to `(x2,y2)`: `s` linear, `b` Bezier, `si`/`so` sine in/out; `sisi`, `siso`, `soso`, `sosi` combine two [inference: names listed, exact shape not defined]. ArcadeZero notes `so` behaves like `si` (fast then slow) in the real game.

## Notes
- Arc Tap = point on a void arc at time `t`. Colour ids select the blue/red/(green) hand [inference]. Void arcs (`true`) need no taps; solid arcs (`false`) require holding along the curve.
- The only keysound is the per-arc `hitsound`.

## Audio & images
Song audio (`base.ogg`), jacket (`base.jpg`), background and `songlist` entries are outside the `.aff` (see `../songlist/`).

## Versions & variants
- ArcadeZero / Arcade: scripted scenecontrol via Lua channels ("ArcadeScenecontrol"); departs from official scenecontrol arguments.
- ArcCreate: `include`/`fragment`, `arctap(t,width)`, arc resolution (11th arc field); projects in `project.arcproj`, packs `.arcpkg`.
- Converters: Etoile/EtoileResurrection (`.aff` <-> ArcCreate packages), arcfutil (Python), Lanotalium/Layesta (imports `.aff` for Lanota).

## Quirks & pitfalls
- Floats need a decimal point (`1.00`), ints must not (`-?[0-9]+\.[0-9]+` vs `-?(0|[1-9][0-9]*)`).
- The header terminator is a line of exactly `-`; group lines end with `};`.
- Arc taps outside the arc time range are errors in ArcCreate.
- `isVoid` is textual (`true`, `false`, `designant`).
- bpm 0 / beats 0 timing events are special; avoid dividing by zero.

## Example

Hand-built from the event grammar above (not from a real song):

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

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Fan charts are plain text, made with ArcCreate (project folders `0.aff`..`3.aff`, exported as `.arcpkg`). The Suhri archive https://github.com/lzwd66/Suhri-s-Charts-Archive has more (Phigros charts too). Official charts are game data and were not collected.

## Sources

- <https://raw.githubusercontent.com/yojohanshinwataikei/vscode-arcaea-file-format/master/server/src/lexer.ts>, `parser.ts`, `types.ts`, `to-ast.ts`, `checker/metadata.ts`, `checker/value-range.ts`, `checker/arc-position.ts`, `checker/extra-lanes.ts`, `checker/scenecontrol.ts`, `checker/timinggroup-attribute.ts`
- <https://raw.githubusercontent.com/Arcthesia/ArcCreate/trunk/Assets/Scripts/ChartFormat/Aff/AffChartReader.File.cs> and `AffChartReader.Line.cs`
- <https://github.com/Tempestissiman/ArcadeScenecontrol>
