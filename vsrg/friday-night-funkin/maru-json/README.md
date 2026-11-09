# FNF Maru Funkin' chart (legacy-like JSON with `sectionEvents`, `offsets`, `players`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: json

## Overview

The chart layout of "Maru Funkin'", an FNF engine that Moonchart marks `@:deprecated("Maru Funkin' engine is dead.")`; Moonchart describes it as "Like FNF Legacy but worse" and as "pretty similar to FNFLegacy although with enough changes to need a seperate implementation". Everything here comes from Moonchart's `FNFMaru.hx` (commit `5d9fbc2cb2afed76dd325134c6f9edb757c090a1`); the engine itself and any real Maru chart were NOT seen.

## Packaged in

Not packaged: loose JSON.

## Container & encoding

UTF-8 JSON `{ "song": { ... } }`. File-name candidates (`formatFile`): only the lower-cased difficulty name. A meta file is "possible" (`hasMetaFile: POSSIBLE`). Moonchart detects the format by the special values `"offsets":`, `"stage":`, and optionally `"players":` / `"player3":`.

## Structure / metadata

`FNFMaruJsonFormat`: `song` (string), `notes` (array of sections), `bpm` (float), `speed` (float), `offsets` (array of int: `[instrumental offset, vocals offset]`), `stage` (string), `players` (array of three strings: bf, dad, gf), plus optional backward-compatible `player1`, `player2`, `player3` (when `players` is missing Moonchart builds it from them, defaults `bf`, `dad`, `gf`).

`FNFMaruSection`: `sectionNotes` (legacy notes `[time, lane, sustain]`), `sectionEvents` (array of events), `mustHitSection`, `bpm`, `changeBPM`. No `lengthInSteps`, `typeOfSection` or `altAnim` in the typedef.

`sectionEvents[i]` = `[time, name, values]` (`values` an array). Event names are not listed in the source read: Unknown.

## Timing model

As legacy ([../legacy-json/README.md](../legacy-json/README.md)): absolute ms for notes and events; BPM changes through section `changeBPM`/`bpm`. `offsets[0]` is the chart offset (`getChartMeta` returns it as the offset).

## Notes

Legacy rule: `[strumTime, noteData, sustainLength]`, `noteData` 0-7, side decided with `mustHitSection`. Note-type strings used by Moonchart's resolver: `default`, `default-hey`, `default-alt`, `fire` (mapped to default, cheer, alt animation, mine), so a fourth slot carrying one of these strings is expected [inference from the resolver registration; no file seen].

## Audio & images

Not in the chart.

## Versions & variants

Unknown.

## Quirks & pitfalls

- The writer (`optimizedOutput`) removes section defaults: `mustHitSection: true`, `changeBPM: false`, `bpm: 0` are omitted, and the reader re-adds them (`fromJson`), so a missing `mustHitSection` means TRUE.
- `players` is an array, not the `player1/player2` fields.

## Example

Hand-written (synthetic) from the typedefs, in the optimised form:

```json
{ "song": { "song": "Demo", "bpm": 120, "speed": 2.0, "offsets": [0, 0], "stage": "stage",
  "players": ["bf", "dad", "gf"],
  "notes": [ { "sectionNotes": [[0, 0, 0], [1000, 2, 250]], "sectionEvents": [] },
             { "sectionNotes": [[2000, 0, 0]], "sectionEvents": [], "mustHitSection": false, "changeBPM": true, "bpm": 150 } ] } }
```

## ROX support

Not read as Maru; the legacy codec needs `song.notes[].sectionNotes` and would read the notes, ignoring `sectionEvents`, `offsets` and `players` [inference from the ROX description in the legacy fiche].

## Parsers & tools

- Moonchart `FNFMaru` (Haxe): https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/FNFMaru.hx

## Getting samples

- Committed: [samples/](samples/) holds one hand-written chart, see [samples/SOURCES.md](samples/SOURCES.md).
- Manifest: none. No real Maru Funkin' chart or engine repository was found; the engine is described as dead by Moonchart. To get one, find a mod built on Maru Funkin' (community sites such as GameBanana; search "Maru Funkin'") and copy its song JSON [inference].

## Sources

- https://raw.githubusercontent.com/MaybeMaru/moonchart/5d9fbc2cb2afed76dd325134c6f9edb757c090a1/src/moonchart/formats/fnf/FNFMaru.hx
