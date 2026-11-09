# Deemo chart (JSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview
Deemo (Rayark) chart, distributed as Unity TextAssets (`*.json.txt` after extraction, e.g. with disunity). Spec assembled from community parsers: MIDI converters (water-vapor/deemo-to-midi, Bigstool/deemo-extract) and the Sonolus engine (NonSpicyBurrito/sonolus-deemo-engine; `dsToDC` = Deemo Source to Deemo Chart). No official document exists.

## Container & encoding
JSON (UTF-8), one object per difficulty. `$id`/`$ref` look like Json.NET object-reference metadata [inference]. Not encrypted in the sources consulted.

## Structure / metadata

Root: `notes` (array) and `links` (array). The consulted parsers show no other root fields. [observed in samples/deenote_finale.hard.json and samples/deenote_12.Magnolia.hard.txt: the root also carries `speed` (e.g. 6.0, 10.0) and, in `finale.hard.json`, `oriVMin`, `oriVMax`, `remapVMin`, `remapVMax`; notes there also carry `speed`, `eventID` and a duplicate `time` next to `_time`.]

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
Absolute seconds per note (`_time`), no BPM map. The Sonolus converter reads `_time` as a beat at a fixed 60 BPM and emits one `#BPM_CHANGE` of 60. Hold-like notes are undocumented (long notes appear to be slide links).

## Notes
- Tap notes: notes not referenced by `links`. Slide notes: notes whose `$id` appears in a link, in `links[i].notes` order.
- `sounds` holds MIDI-like (pitch, velocity, duration, delay) entries; no `sounds` or `null` is silent.
- The Sonolus converter skips notes with `pos > 2` (purpose unknown).

## Audio & images
Not referenced by the chart. The game plays `sounds` through its own piano samples plus a background music asset [inference].

## Versions & variants
Deemo II (2022) charts are undocumented in the sources. Sonolus engine pipeline: DS -> DC -> Level Data.

## Quirks & pitfalls
- `_time` and `pos` can be missing (default 0); `sounds` can be missing or `null`; `d` can be missing; `v` can be negative.
- Difficulties of one song can differ in note counts and sound data (deemo-extract reports mismatches).

## Example

Hand-built from the fields above (not extracted from the game):

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

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: https://github.com/LibrarristShalinward/Deemo-I-Charts has ~450 interactive-chart and ~1300 original-chart JSON files (and two zips under `下载/`). Extraction tools: deemo-extract, disunity.

## Sources

- <https://raw.githubusercontent.com/Bigstool/deemo-extract/main/extract/extract.py>
- <https://cdn.jsdelivr.net/npm/sonolus-deemo-engine@1.6.4/dist/ds/index.d.ts> and `ds/convert.js`
- <https://github.com/water-vapor/deemo-to-midi>
