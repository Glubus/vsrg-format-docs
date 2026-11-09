# SPH chart (`.sph`, rizu / soundsphere)
Kind: chart

Doc status: partial (parser-derived; some visual fields unverified) · ROX: no · Category: vsrg · Encoding: text

## Overview

`.sph` is the native text chart format of the rizu engine (`semyon422/rizu`, Lua/LuaJIT; chart code in `chart/`, format tag `sphere` in chart metadata [inference: same lineage as soundsphere]). The engine stores charts converted from osu!mania, BMS, O2Jam, Quaver, StepMania, K-Shoot Mania, IIDX and MIDI sources in it. The repository spec (`chart/format/sph/spec.md`) calls itself "intentionally incomplete"; this page is reconstructed from the decoder/encoder source (`Sph.lua`, `lines/TextLines.lua`, `lines/template_key.lua`, `SphLines.lua`, `ChartDecoder.lua`, `Metadata.lua`).

## Container & encoding

- UTF-8 text, `\n` line endings (the decoder normalises `\r\n`). Empty lines are skipped.
- One file is one chart (the decoder returns a single `{chart, chartmeta}`).
- Sections start with `# <name>`: `# metadata`, `# sounds`, `# notes`. The encoder writes them in that order with a blank line between.
- No compression. `chart/transform/NanoChart` stores charts in a compact binary form for replays (`.nanochart` exports, wire format versions 1 and 2, per the rizu spec); not documented here.

## Structure / metadata

### `# metadata`

Lines `<key> <value>` (key `%w+`, a space, then the rest). Known keys (`Metadata.lua`, written in this order, then custom keys sorted alphabetically):

| Key | Meaning |
|---|---|
| `title`, `artist` | Song title / artist. |
| `name` | Difficulty name. |
| `creator` | Mapper/charter. |
| `source` | Source (album/game). |
| `level` | Numeric level (`tonumber`). |
| `tags` | Tags. |
| `audio` | Audio file path. |
| `background` | Background image path. |
| `preview` | Preview start time (number). |
| `input` | Input mode string such as `4key` (see below); required (`assert(sph.metadata:get("input"))`). |

Keys `format`, `duration`, `tempo`, `start_time` are ignored when copying chart metadata. A new chart gets default metadata `preview 0`, `input 4key`.

Input mode string: `<count><type>` groups, e.g. `4key`. The decoder parses `([0-9]+)([a-z]+)` groups and requires the string to equal its canonical re-serialisation (types ordered by count descending, then name), otherwise "invalid InputMode string". Columns are named `<type><index>` (`key1`..`key4`, `scratch1`, ...), assigned in canonical order. [the type list is open: any lower-case word is accepted; concrete types seen in this repo are not enumerated]

### `# sounds`

Lines `<key> <path>` where `key` is a 2-character base-85 number using the Z85 alphabet of ZeroMQ RFC 32 (`0-9 a-z A-Z . - : + = ^ ! / * ? & < > ( ) [ ] { } @ % $ #`; `00` = 0, `01` = 1, `10` = 85, `##` = 7224). Note lines reference them with `:` sound lists.

### `# notes`

One line per time point, space-separated tokens:

```
<notes> [=<seconds>] [+<n>/<d>] [^] [v<name>] [e<number>] [x<v1>[,<v2>[,<v3>]]] [#<n>/<d>] [:<soundkeys>] [.<volumes>] [// comment]
```

| Token | Meaning |
|---|---|
| `<notes>` (first token) | One character per column (`0` = none), or `-` for "no notes". Note characters: `1` tap, `2` hold start, `3` hold end, `4` "shade" (non-playable/visual note). |
| `=<t>` | Absolute time in seconds of this line (an interval vertex / time anchor). |
| `+<n>/<d>` | Position inside the current beat as a fraction. |
| `^` | Same time as the previous line (stacks several lines at one time point). |
| `v<name>` | Visual layer name (separate scroll-velocity "visual"). |
| `e<number>` | Expand value (visual expansion at this point). |
| `x<a>[,<b>[,<c>]]` | Velocity: up to three numbers (missing ones default to 1). |
| `#<n>/<d>` | Measure marker (fraction). |
| `:<keys>` | Keysound list: 2-char base-85 keys from `# sounds`, one per note in order; extra keys beyond the number of notes become auto-played samples on columns `auto1`, `auto2`... |
| `.<vols>` | Volumes: 2 decimal digits per sound, percent (`00` is read as 100). |
| `// ...` | Comment. |

## Timing model

SPH has no explicit tempo: the spec states "SPH does not support explicit tempo declarations. Tempo is inferred from the time difference between note lines, so parser or engine changes must preserve that assumption", and "the engine requires at least two note lines to determine timing and average beat duration". Mechanics (`SphLines.lua`): the decoder keeps a running beat counter. Each line without `+` and without `^` advances the beat by 1; `+n/d` puts the line at that fraction of the current beat; `^` keeps the previous time. Lines with `=t` assign an absolute time in seconds to their beat position (the vertices of the interval layer); times between anchors follow from them. The first `=` line's integer beat becomes the global origin (`recalcGlobalTime` subtracts it). The chart tempo reported to the game is `60 / ((last time - first time) / beats)`. An encoder must keep standalone vertices and measure markers, otherwise a decoder extrapolates from a short interval and compresses the chart (spec). [linear interpolation between anchors is inferred from the interval layer design, not from a stated rule]

## Notes

Hold = `2` start and `3` end on the same column. Shade `4` is non-playable. The column count grows with the widest line. Visual data (`x`, `e`, `v`) is separate from gameplay timing.

## Audio & images

`audio` and `background` metadata paths; per-note sounds in `# sounds`.

## Versions & variants

No version field is read (an ignored `format` key exists). `chartmeta.format` is set to `sphere` on decode; converted charts get `mode = "mania"`.

## Quirks & pitfalls

- No BPM lines; tempo comes from the line timing.
- The first token is positional (note characters) or `-`.
- Sound keys are 2 characters in base 85 (BMS uses base 36). Volume `00` means 100 %.
- `input` must equal its canonical form.

## Example

Hand-built from the Lua default template (`Sph:getDefault`, which writes `0000 =0` and `0000 =1` after `preview 0` / `input 4key`); the note lines are hand-built from the token rules above:

```
# metadata
title Example
input 4key

# notes
1000 =0
0100 =0.5
0010 =1
0001 =1.5
```

## ROX support

Not read by ROX. SPH fits ROX's column model (taps/holds/keysounds) but has no BPM; a decoder would derive timing from the `=` anchors and beat counter.

## Parsers & tools

rizu (Lua): https://github.com/semyon422/rizu (`chart/format/sph/`: `Sph.lua`, `ChartDecoder.lua`, `ChartEncoder.lua`, `SphLines.lua`, `lines/TextLines.lua`, `lines/template_key.lua`, `Metadata.lua`; tests in `chart/format/sph/tests`). `chart/format/` also holds decoders for osu!, BMS, O2Jam, Quaver, StepMania, KSM, IIDX and MIDI.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: run rizu / soundsphere and import any osu!mania, BMS, Quaver or StepMania chart; the engine writes SPH through `chart/format/sph/ChartEncoder.lua` [inference: export UI path not run]. No public archive of `.sph` files was found.

## Sources

- https://github.com/semyon422/rizu (commit `37df09654581800fa30df613385080b99c795c9a`): `chart/spec.md`, `chart/format/sph/spec.md`, `chart/format/sph/*.lua`, `chart/format/sph/lines/*.lua`, `chart/core/InputMode.lua`
- https://rfc.zeromq.org/spec/32/ (Z85 alphabet referenced by `template_key.lua`)
