# memon (`.memon`, jubeat chart set, JSON)
Kind: chart

Doc status: complete · ROX: no · Category: others · Encoding: json (UTF-8, JSON Schema 2020-12 provided)

## Overview

JSON jubeat chart-set format created by Stepland as an easier-to-parse alternative to the memo-like text formats ([memo](../memo/README.md), youbeat). One file holds a song: metadata, shared timing and several charts keyed by difficulty name. Used by the simulator jujube, the editor F.E.I.S, the converter jubeatools, and a C++ parser (`memoncpp`). Versions: legacy, `0.1.0`, `0.2.0`, `0.3.0`, `1.0.0` (schema below is 1.0.0). `Jubeat-MemonEveConverter` turns memon into `.eve`.

Category: others. 4×4 grid (position = panel index 0–15).

## Container & encoding

JSON text, UTF-8. Decimal values may be JSON numbers or numeric strings (`"^-?\d+(\.\d+)?$"`) to avoid float rounding. Extension `.memon`. One file = one song with N charts.

## Structure / metadata

Root object (`version` and `data` required):

| Key | Type | Meaning |
|---|---|---|
| `version` | const `"1.0.0"` | schema version |
| `metadata` | object | `title`, `artist`, `audio` (path relative to the memon file), `jacket` (path), `preview` = either `{start, duration}` in seconds (a sample of the music file) or a string path to a separate preview file. No extra keys allowed |
| `timing` | timing object | default timing for every chart |
| `data` | object | maps difficulty names (free strings, e.g. `BSC`, `ADV`, `EXT`) to chart |

Chart: `level` (decimal, "typically 1 to 10.9"), `resolution` (ticks per beat for the notes, default 240), `timing` (optional chart-specific timing object that replaces the default), `notes` (required array).

Timing object: `offset` (seconds, time at which the first beat occurs in the music file, default 0), `resolution` (ticks per beat for bpms and hakus, default 240), `bpms` (≥ 1 events `{beat, bpm}`, default `[{beat:0,bpm:120}]`), `hakus` (array of times in beats marking the "bounce" pattern when not regular 4/4).

Note object: `n` (position 0–15, **left to right, top to bottom**), `t` (time), optional `l` (long-note duration) and `p` (tail starting position, "6-notation": `0,1,2` horizontal tails from left to right, `3,4,5` vertical tails from top to bottom); `l` and `p` must appear together; no other keys.

## Timing model

Beat-based: `t`, `l`, `beat`, and haku values are either an **integer number of ticks** (`resolution` ticks per beat) or a **symbolic fraction array `[integer part, numerator, denominator]`** (e.g. `[1,1,2]` = 1.5 beats; a strictly positive duration cannot be `[0,0,x]`). Time in seconds = beats integrated over the `bpms` events plus `offset` (first beat location in the audio). Chart-level `timing` replaces the global one entirely.

## Notes

Tap = note without `l`/`p`. Long = `l` (duration) + `p` (tail start in 6-notation; the tail goes outward from the head). `n` is row-major over 16 panels. Notes must be unique and must not overlap hitboxes or marker animations (spec "Other things to look out for": uniqueness, hitbox/marker overlap, duplicate BPMs/HAKUs, multiple timing objects).

## Audio & images

`metadata.audio`, `metadata.jacket`, `metadata.preview` (sample or file), relative to the memon file.

## Versions & variants

legacy (pre-0.1.0), 0.1.0, 0.2.0, 0.3.0, 1.0.0. jubeatools reads and writes all (`memon:legacy`, `memon:v0.1.0`, ... `memon:v1.0.0`).

[observed: jubeatools_Sky_Bus_For_Hire_*.memon] Legacy `0.1.0` files have no `timing` object: metadata keys are `song title`, `music path`, `album cover path`, `BPM` (float), `offset` (float seconds); each chart is `{level, resolution, notes}` with notes `{n, t, l, p}` (no tail = `l: 0, p: 0`).

## Quirks & pitfalls

- Time is an integer (ticks) or a 3-element array; accept both.
- Decimals may be strings.
- Long-note `p` uses 6-notation, unlike the `.eve` direction bits.
- A chart's `timing` replaces, not merges.
- Duplicate BPM/haku events are discouraged (spec rules).

## Example

Hand-built from the JSON schema:

```json
{
  "version": "1.0.0",
  "metadata": {"title": "demo", "artist": "me", "audio": "song.ogg"},
  "timing": {"offset": 0.5, "resolution": 240, "bpms": [{"beat": 0, "bpm": 140}]},
  "data": {
    "BSC": {"level": 3, "notes": [{"n": 0, "t": 0}, {"n": 5, "t": [1, 1, 2], "l": 240, "p": 0}]}
  }
}
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

[Stepland/memon](https://github.com/Stepland/memon) (spec + schema), [jubeatools](https://github.com/Stepland/jubeatools), [jujube](https://github.com/Stepland/jujube) (simulator), [F.E.I.S.](https://github.com/Stepland/F.E.I.S.) (editor), [memoncpp](https://github.com/Stepland/memoncpp) (C++).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: F.E.I.S. (<https://github.com/Stepland/F.E.I.S.>) writes memon; jubeatools converts to/from it; the spec repo <https://github.com/Stepland/memon> has about 70 schema fixtures in `tests/data`.

## Sources

- <https://raw.githubusercontent.com/Stepland/memon/master/schema.json> (read), <https://github.com/Stepland/memon> README (read), <https://memon-spec.readthedocs.io/en/latest/> (table of contents read)
