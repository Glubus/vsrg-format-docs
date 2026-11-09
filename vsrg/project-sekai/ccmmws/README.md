# MikuMikuWorld binary layout and fork variants (`.mmws`, `.ccmmws`, `.unchmmws`)
Kind: project

Doc status: partial (chart content decoded; jacket and waypoint sections unknown) · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview

[`../mmws`](../mmws/README.md) introduces the MikuMikuWorld (MMW) score file. This page gives its binary layout, reconstructed from the C++ loader (`mmws/loader.cpp`) and shared header `mmw_io.hpp` of `UntitledCharts/rg_converters`, which implements three variants (credited to `@YarNix`; the authors do not document the format). All files are little-endian, strings NUL-terminated.

| Signature | Extension | Program | Version fields |
|---|---|---|---|
| `MMWS` | `.mmws` | MikuMikuWorld | one `int32` version (1..4+) |
| `CCMMWS` | `.ccmmws` | MikuMikuWorld for Chart Cyanvas (MMW4CC) | `int16` version + `int16` "cc version" |
| `UCMMWS` | `.unchmmws` | MikuMikuWorld for Untitled Charts | one `int32` "uc version" |

## Container & encoding

- Raw binary, no compression.
- The detector (`mmws/detector.cpp`) tests the file prefix in this order: `MMWS`, `CCMMWS`, `UCMMWS` ("first `startswith` match wins").
- Strings (`read_cstr`): bytes up to the next NUL (charset not stated: UTF-8 assumed [inference]).
- Integers `int32` unless a field says otherwise; floats are IEEE-754 `float32`.

## Structure / metadata

### Header

1. `cstr signature` (`"MMWS"`, `"CCMMWS"` or `"UCMMWS"`, NUL included).
2. Version field(s) per variant (table above).
3. If `version >= 3` (`has_address`): an address table of absolute file offsets: `metadata`, `events`, `taps`, `holds`; then `damages` (if `cc_version >= 1`), `layers` (if `cc_version >= 4`), and one more `int32` that is read and ignored (if `cc_version >= 5`, "waypoints"). Each section is read after seeking to its address. For `version < 3` the sections follow each other with no table.

Feature flags derived from the versions (`Version` in `mmw_io.hpp`; `version` = base, `cc` = Chart Cyanvas, `uc` = Untitled Charts):

| Flag | Condition | Effect |
|---|---|---|
| `has_skill_fever`, `has_jacket` | `version >= 2` | skill/fever events; a `has_jacket` flag exists in the code but the loader never reads jacket data |
| `has_address`, `has_hispeed` | `version >= 3` | address table; hi-speed events |
| `has_guideNote` | `version >= 4` | per-hold flag word (guides, hidden ends, fake) |
| `has_damageNote`, `has_laneExtension` | `cc >= 1` | damage-note list; lane range extended beyond 12 |
| `has_fadeType` | `cc >= 2` | guide fade type |
| `has_guideColor` | `cc >= 3` | guide colour |
| `has_layers` | `cc >= 4` | layers (time scale groups) |
| `has_waypoints` | `cc >= 5` | waypoint section (address read, content unknown) |
| `has_floatLaneWidth` | `cc >= 6` | lane/width stored as `float32` |
| `has_dummyNote` | `cc >= 6` and `uc >= 1` | dummy (fake) flag in notes |

For `MMWS` files `cc = 0`; for `UCMMWS` files the constructor defaults `cc = 6` and `version = 4` (all features).

### Metadata section

`cstr title`, `cstr designer`, `cstr artist`, `cstr musicFile` (discarded by the converter), `float32 offset` (milliseconds; the converter stores `waveoffset = offset / -1000` seconds, sign inverted). With `has_jacket`, more data (jacket path etc.) may follow; it is not read: Unknown.

### Layers (time-scale groups)

`int32 layerCount` at the `layers` address; otherwise a single group. Hi-speed events refer to a layer index.

### Events section

1. `int32 timeSignatureCount`, then `timeSignatureCount * 3` `int32` values (3 ints per entry: measure/numerator/denominator [inference]); the converter skips them.
2. `int32 tempoCount`; each `{ int32 tick; float32 bpm }`.
3. If `has_hispeed`: `int32 count`; each `{ int32 tick; float32 timeScale; [int32 layer if has_layers] }`.
4. If `has_skill_fever`: `int32 skillCount` then `skillCount * int32 tick`; then `int32 feverChanceTick` (signed) and `int32 feverStartTick` (signed); `> 0` means present.

### Note data record

Used by taps, hold nodes and damage notes (order of fields):

| Field | Type | Condition |
|---|---|---|
| tick | int32 | |
| lane | int32 (or float32 if `has_floatLaneWidth`) | |
| width | int32 (or float32) | |
| layer | int32 | `has_layers` |
| flick | int32 | only when the record is a tap or a hold end (not start/mid) |
| flag | int32 | bit `1` critical, `2` friction (trace), `4` dummy/fake (`has_dummyNote`) |
| holdStepType | int32 | only for hold mid nodes: `0` normal (tick, shape + combo), `1` hidden (shape, no combo, critical = none), `2` skip (attach; combo, no shape change) |
| ease | int32 | for hold start and mid nodes |

Flick types: `0` none, `1` up (default), `2` left, `3` right. Ease types: `0` linear, `1` ease-in, `2` ease-out, `3` ease-in-out, `4` ease-out-in.

### Taps / damages

`int32 count` followed by `count` note data records (type "tap"). The `damages` section (address, `cc >= 1`) has the same layout and yields damage (hazard) notes.

### Holds

`int32 holdCount`; each hold:

1. `int32 holdFlag` (only if `has_guideNote`): `1` start hidden, `2` end hidden, `4` guide (the hold is a guide line, not a slide), `8` fake.
2. note data record (type "start": no flick, with ease).
3. `int32 fadeType` if `has_fadeType` (`0` out, `1` none, `2` in; default out).
4. `int32 guideColor` if `has_guideColor` (`0` neutral, `1` red, `2` green, `3` blue, `4` yellow, `5` purple, `6` cyan, `7` black; if absent: yellow when critical else green).
5. `int32 stepCount`, then `stepCount` note data records (type "mid").
6. note data record (type "end": with flick, no ease).

## Timing model

480 ticks per beat (`tick_to_beat(tick, 480)`), with tempo and per-layer hi-speed events as above. The converter skips the time signature list. The metadata offset is the audio offset in ms.

## Notes

`lane` is the left edge on the MMW lane grid (0..11, wider with lane extension), `width` the width. Converter geometry: centre = `lane - 6 + width/2`, half-size = `width/2` (0-centred, 12-lane board).

## Audio & images

`musicFile` path (NUL-string) in the metadata. The loader does not read the jacket data flagged from version 2 (Unknown).

## Versions & variants

See the flag table. CCMMWS adds the `cc` capabilities, UCMMWS the `uc` version and dummy notes (the converter's default `Version()` enables all features).

## Quirks & pitfalls

- Sections are addressed by absolute offsets (`seek_set`), not necessarily in file order.
- `flick` is absent in start/mid records; reading it unconditionally desynchronises the stream.
- `feverChanceTick` and `feverStartTick` are signed; <= 0 means absent.
- The offset is in ms, negated relative to `waveoffset`.

## Example

Hand-built header for a minimal `MMWS` version-1 file: `4D 4D 57 53 00` (`MMWS\0`) then `01 00 00 00` (int32 version 1); sections then follow without an address table (version < 3).

## ROX support

Not read by ROX (wide notes, eased slides, guides, damage notes and layers do not map to columns).

## Parsers & tools

- `rg-converters` (C++ core + Python): https://github.com/UntitledCharts/rg_converters (`cpp/src/converters/mmws/loader.cpp`, `exporter.cpp`, `detector.cpp`, `cpp/include/rg/converters/mmw_io.hpp`, `mmws.hpp`).
- Editors: MikuMikuWorld and forks (see [`../mmws`](../mmws/README.md)).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). All are converted with rg-converters (`mmw.ccmmws.export`, `mmw.unchmmws.export`); no public `.ccmmws`/`.unchmmws` was found.

- [observed: rgconv_sekaibest_0001_01_easy.ccmmws, ..unchmmws] magic `CCMMWS` + `00 04 00 06 00 27 ...` (Chart Cyanvas) and `UCMMWS` + `00 01 00 00 00 27 ...` (Untitled Charts); same length for the same chart.
- Native files: MMW4CC / MMW4UC (https://github.com/UntitledCharts/MikuMikuWorld4UC) File > Save.

## Sources

- https://github.com/UntitledCharts/rg_converters (commit `673710dcc441aea97ac89e113f811d5c169763d4`): `README.md`, `cpp/src/converters/mmws/*.cpp`, `cpp/include/rg/converters/mmw_io.hpp`
