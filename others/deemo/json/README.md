# Deemo chart (JSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

Chart of Deemo (Rayark). Distributed as Unity TextAssets (`*.json.txt` after extraction with tools such as disunity); the community has converters to MIDI (water-vapor/deemo-to-midi, Bigstool/deemo-extract) and a Sonolus engine (NonSpicyBurrito/sonolus-deemo-engine, with `dsToDC` = Deemo Source to Deemo Chart converter). The spec below is assembled from those parsers; no official or complete document exists.

## Container & encoding

JSON (UTF-8), one object per difficulty. The `$id`/`$ref` keys look like Json.NET object-reference metadata [inference]. Not encrypted in the sources consulted.

## Structure / metadata

Root: `notes` (array) and `links` (array). Other root fields (e.g. speed or BPM data) were not found in the consulted parsers.

Note (`DSNote` in sonolus-deemo-engine):

| Field | Type | Meaning |
|---|---|---|
| `$id` | string | note identifier, referenced by links |
| `pos` | number, optional | horizontal position; absent means 0; the Sonolus converter skips notes with `pos > 2` (non-playable/special) and maps `lane = pos*4` |
| `size` | number | width; converter uses `size*2` |
| `_time` | number, optional | time in seconds; missing at the very start of the song means 0 |
| `sounds` | array or null, optional | piano sounds triggered by the note (see below) |

`sounds` entries (from the MIDI extractors): `w` (relative delay in seconds on top of `_time`, optional), `d` (duration in seconds; if missing, reuse the previous note's duration), `p` (pitch, mapped directly to a MIDI note number), `v` (velocity; <= 0 means silent and is skipped).

Link: `links[i].notes = [{"$ref": "<$id>"}, ...]`; notes listed in a link form a slide chain (all linked notes become slide notes).

## Timing model

Absolute time in **seconds** per note (`_time`), no BPM map in the format. The Sonolus converter treats `_time` as a beat at a fixed 60 BPM (i.e. seconds) and emits a single `#BPM_CHANGE` of 60. Hold-like notes are not documented in the consulted sources (long notes appear to be expressed via slide links).

## Notes

- Tap notes: any note not referenced by `links`.
- Slide notes: notes whose `$id` appears in a link; the chain order is the order in `links[i].notes`.
- Keysounds: the `sounds` array carries MIDI-like (pitch, velocity, duration, delay) entries; notes without `sounds` (or with `null`) are silent.
- Notes with `pos > 2` are skipped by the Sonolus converter (purpose unknown).

## Audio & images

Not referenced by the chart; the game plays the sounds from the chart's `sounds` through its own piano samples, plus a background music asset [inference].

## Versions & variants

Deemo (I) vs Deemo II: Deemo II (2022) charts were not documented in the consulted sources. Fan engines: Sonolus Deemo engine uses DS (Deemo Source) -> DC (Deemo Chart) -> Level Data.

## Quirks & pitfalls

- `_time` and `pos` can be missing (default 0).
- `sounds` can be missing or `null`; `d` can be missing; `v` can be negative.
- Different difficulties of one song may have different note counts and sound data (deemo-extract reports length/note mismatches).

## Example

Illustrative, hand-built from the fields above (not extracted from the game):

```json
{"notes":[{"$id":"1","_time":1.0,"pos":-0.5,"size":0.5,"sounds":[{"d":0.5,"p":60,"v":80}]},
          {"$id":"2","_time":1.5,"pos":0.0,"size":0.5}],
 "links":[{"notes":[{"$ref":"1"},{"$ref":"2"}]}]}
```

## ROX support

Not read by ROX.

## Parsers & tools

- deemo-to-midi (Python): <https://github.com/water-vapor/deemo-to-midi>
- deemo-extract (Python, MIDI): <https://github.com/Bigstool/deemo-extract>
- sonolus-deemo-engine (TypeScript, `dsToDC`, `dcToLevelData`): <https://www.npmjs.com/package/sonolus-deemo-engine>

## Sources

- <https://raw.githubusercontent.com/Bigstool/deemo-extract/main/extract/extract.py>
- <https://cdn.jsdelivr.net/npm/sonolus-deemo-engine@1.6.4/dist/ds/index.d.ts> and `ds/convert.js`
- <https://github.com/water-vapor/deemo-to-midi>
