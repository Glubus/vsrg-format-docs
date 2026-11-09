# FNF Maru Funkin' chart (legacy-like JSON with `sectionEvents`, `offsets`, `players`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

Chart layout of "Maru Funkin'", an FNF engine Moonchart marks `@:deprecated("Maru Funkin' engine is dead.")` ("Like FNF Legacy but worse"; "pretty similar to FNFLegacy although with enough changes to need a seperate implementation"). Source: Moonchart's `FNFMaru.hx` (commit `5d9fbc2cb2afed76dd325134c6f9edb757c090a1`); the engine was not seen.

## Packaged in

Loose JSON.

## Container & encoding

UTF-8 JSON `{ "song": { ... } }`. File name (`formatFile`): the lower-cased difficulty name. Meta file "possible" (`hasMetaFile: POSSIBLE`). Moonchart detects the format by the special values `"offsets":`, `"stage":`, and optionally `"players":` / `"player3":`.

## Structure / metadata

`FNFMaruJsonFormat`: `song` (string), `notes` (array of sections), `bpm` (float), `speed` (float), `offsets` (array of int: `[instrumental offset, vocals offset]`), `stage` (string), `players` (array of three strings: bf, dad, gf), plus optional backward-compatible `player1`, `player2`, `player3` (Moonchart builds `players` from them when missing; defaults `bf`, `dad`, `gf`).

`FNFMaruSection`: `sectionNotes` (legacy notes `[time, lane, sustain]`), `sectionEvents` (array of events), `mustHitSection`, `bpm`, `changeBPM`. No `lengthInSteps`, `typeOfSection` or `altAnim` in the typedef.

`sectionEvents[i]` = `[time, name, values]` (`values` an array). Moonchart lists no event names; `addZoom` appears in a real chart (see Observed in real files).

## Timing model

As legacy ([../legacy-json/README.md](../legacy-json/README.md)): absolute ms for notes and events; BPM changes through section `changeBPM`/`bpm`. `offsets[0]` is the chart offset (`getChartMeta` returns it as the offset).

## Notes

Legacy rule: `[strumTime, noteData, sustainLength]`, `noteData` 0-7, side decided with `mustHitSection`. Note-type strings used by Moonchart's resolver: `default`, `default-hey`, `default-alt`, `fire` (mapped to default, cheer, alt animation, mine). A fourth slot with one of these strings is expected [inference from the resolver registration; no file seen].

## Audio & images

Not in the chart.

## Versions & variants

Unknown.

## Quirks & pitfalls

- The writer (`optimizedOutput`) removes section defaults: `mustHitSection: true`, `changeBPM: false`, `bpm: 0` are omitted; the reader re-adds them (`fromJson`), so a missing `mustHitSection` means true.
- `players` is an array replacing `player1/player2`.

## Example

Synthetic, from the typedefs, in the optimised form:

```json
{ "song": { "song": "Demo", "bpm": 120, "speed": 2.0, "offsets": [0, 0], "stage": "stage",
  "players": ["bf", "dad", "gf"],
  "notes": [ { "sectionNotes": [[0, 0, 0], [1000, 2, 250]], "sectionEvents": [] },
             { "sectionNotes": [[2000, 0, 0]], "sectionEvents": [], "mustHitSection": false, "changeBPM": true, "bpm": 150 } ] } }
```

## ROX support

Not read as Maru; the legacy codec (`song.notes[].sectionNotes`) would read the notes and ignore `sectionEvents`, `offsets` and `players` [inference].

## Parsers & tools

- Moonchart `FNFMaru` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/FNFMaru.hx

## Observed in real files

`songs/<song>/charts/<difficulty>.json` with a `songMeta.json` beside it; `offsets: [0,0]`, `players: [bf, dad, gf]` (e.g. `["GudBF","danny","gf"]`), `stage`; notes-free sections are `{}`; events like `[22500, "addZoom", ["0.075", "0.05"]]`; fractional sustains (`931.928571428571`) [observed: vs-danny/easy.json, returnal/hard.json].

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: GameBanana mods built on Maru Funkin' (search `Maru Funkin`, e.g. mods 466972, 508895). Charts live in `songs/<song>/charts/<difficulty>.json` (+ `songMeta.json`); see Observed in real files.

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/5d9fbc2cb2afed76dd325134c6f9edb757c090a1/src/moonchart/formats/fnf/FNFMaru.hx
