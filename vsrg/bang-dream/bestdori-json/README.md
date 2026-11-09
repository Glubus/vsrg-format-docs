# Bestdori chart (v2 JSON, `.json`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes; Prism's addition) · Category: vsrg · Encoding: json

## Overview

Bestdori (fan database/chart-sharing site for BanG Dream! Girls Band Party) stores charts as a JSON array of objects ("Bestdori v2"; BanGConverter converts the older v1). Official charts come from the Bestdori API; fan charts use the same shape. No official specification exists; the schema comes from open-source parsers (ayachan Go package `bestdoriChart`).

## Container & encoding
UTF-8 JSON; root is an array (`BestdoriV2Chart = []BestdoriV2Note`). One file = one difficulty (Easy/Normal/Hard/Expert/Special). Notes need not be sorted (parsers sort by beat then lane). No audio inside: the song is selected on the site.

## Structure / metadata
Every element has `type` (string). Note types seen: `"BPM"`, `"Single"`, `"Long"`, `"Slide"`, `"Directional"`.

| Field | Used by | Meaning |
| --- | --- | --- |
| `type` | all | `Single`, `Long`, `Slide`, `Directional`, `BPM`; unknown types are dropped by ayachan |
| `beat` | Single, Directional, BPM | float position in beats (quarter notes) from chart start |
| `lane` | Single, Directional | float lane number (integer lanes 0..6 for the 7 lanes; ayachan clamps to [0, 7]) |
| `flick` | Single, connection nodes | bool flick |
| `hidden` | connection nodes | bool hidden node (slide path point without a visible note) |
| `bpm` | BPM | tempo (absolute value taken by ayachan); the first BPM element anchors beat 0 (notes before it are ignored, beats are shifted so the first BPM is at 0) |
| `connections` | Long, Slide | array of nodes `{beat, lane, flick?, hidden?}`; the first node is the head |
| `direction` | Directional | `"Left"` or `"Right"` |
| `width` | Directional | integer 0..3 per ayachan's check (BanG! Simulator's directional flicks span widths 1..7) |
| `skill`, `charge` | Single / connection nodes | skill-note and fever-charge flags seen in Bestdori API Go types [inference from a search excerpt, not verified] |

## Timing model
`beat` is a float number of beats; BPM list from `BPM` elements: `time(beat) = sum(dBeat * 60 / bpm)` per segment. No offset in the chart (the site/tool handles audio offset).

## Notes
- `Single`: tap at `beat`, `lane`; optional `flick`.
- `Long` (green hold): `connections` with at least 2 nodes, normally same lane; the last node is the release. One node degrades to a single note; zero nodes is invalid (ayachan).
- `Slide`: like Long but nodes may change lane; `hidden` nodes shape the path.
- `Directional`: sideways flick: `direction` Left/Right and `width` (the number of lanes it spans).
- Simultaneous notes: same beat, different lanes.

## Audio & images

Not part of the chart.

## Versions & variants

v1 (older, superseded), v2 (types above). Newer game versions added directional flicks and hidden slide nodes; BanG! Simulator's text format mirrors the type list ([txt](../txt/README.md)).

## Quirks & pitfalls
Fan charts contain negative beats and out-of-range lanes (clamped by ayachan). The first BPM may not be at beat 0. Long/Slide head position lives in `connections[0]`, not in top-level `beat`/`lane`. `hidden` nodes have no judgement.

## Example
Shape given by the ayachan struct definitions (illustrative, hand-built):
```json
[{"type":"BPM","beat":0,"bpm":191},
 {"type":"Single","beat":4,"lane":3},
 {"type":"Long","connections":[{"beat":8,"lane":2},{"beat":10,"lane":2}]}]
```

## ROX support

Decode only (`rox::formats::bandori`, `BestdoriDecoder`, `DetectedFormat::Bestdori`). One chart per file, always 7 columns, lane 0..6 -> column 0..6 (confirmed by `bangbangboom-editor`'s exporter, "from 0 to 6", and by `BanGConverter`, which writes `lane + 1` into the simulator's 1..7). A lane outside 0..6 or not whole is dropped and counted, never clamped.

- `Single` -> Tap. `Long`/`Slide` -> one Hold from the first connection to the last on the first connection's lane (lossy: joints between, hidden ones included, and the cross-lane path are lost, counted). A connection list of length 1 is a Tap, of length 0 invalid.
- `flick`, `Directional` (direction and width), `skill` and `charge` are counted and dropped (the note stays a Tap). An unknown `type` (a v1 chart's `System`/`Note` included) is counted.
- Tempo: the BPM at beat 0 is the last `BPM` at or before it (absolute value); 120 BPM until the first one when there is none (`BanGConverter`'s default). Notes before beat 0 are dropped and counted. No offset, no audio (`audio_file` empty, title = file stem without `.bestdori`).
- Detection (no file-name convention exists, so this is a decision): ROX never claims a plain `.json` (FNF's). `detect` says `Bestdori` for `.bestdori` and `.bestdori.json`. `auto_decode*` also reads `<difficulty>.json` (`easy`, `normal`, `hard`, `expert`, `special`: the last path segment of the site's `/api/charts/<id>/<difficulty>.json`, `bestdori-api-go`) and `<id>.<difficulty>.json` when the content is a JSON array whose first element is an object naming a note type (`rox::formats::is_bestdori_chart_name`, `looks_like_bestdori`, `is_bandori_chart_file`). Rename other files to `*.bestdori.json`.
- Prism (`docs/game.md` "BanG Dream"): playable on the 7K layout; sound is the audio file of the chart's name, else the first of the folder, else silence.
- Sources read: `ayachan`, `BanGConverter`, `bestdori-api-go`, `bangbangboom-editor` (all MIT); nothing copied, no real chart decoded.

## Parsers & tools
ayachan (Go): https://github.com/6QHTSK/ayachan · bestdori-api-go: https://github.com/WindowsSov8forUs/bestdori-api-go · BanGConverter: https://github.com/loader3229/BanGConverter · bangbangboom-editor: https://github.com/K024/bangbangboom-editor · AAO-Editor: https://github.com/wuqiongjin/AAO-Editor · BanGDreamChartRender: https://github.com/WindowsSov8forUs/BanGDreamChartRender

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md): official charts from `/api/charts/<songId>/<difficulty>.json` (byte-exact), community charts (`post.chart` extracted from `/api/post/details?id=<id>`, re-serialised compactly).

- [observed: samples/bestdori-official_song003_special.json] Besides BPM/Single/Long/Slide/Directional there is a `System` object (`{"type":"System","data":"bgm001.wav","beat":0}`), `skill`/`charge` flags on singles, and `Directional` with `direction` ("Right") and `width`. BPM changes are extra `BPM` objects (3 in song 200, 5 in song 400). Official files are compact one-line JSON; `hidden` connection flags appear in song 3 special.
- More: `https://bestdori.com/api/songs/all.5.json` lists songs; any `<songId>/<easy|normal|hard|expert|special>`; community chart ids via the site's post pages.

## Sources
https://pkg.go.dev/github.com/6QHTSK/ayachan/model/bestdoriChart · https://raw.githubusercontent.com/6QHTSK/ayachan/master/model/bestdoriChart/bestdoriV2.go · https://github.com/K024/bangbangboom-editor/issues/3 · https://github.com/loader3229/BanGConverter
