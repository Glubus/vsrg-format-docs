# FNF Nightmare Vision chart (`format: "nmv2"`, Psych-derived JSON with `keys`/`lanes`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview

NightmareVision (NMVTeam; the FNF wiki calls it "a modified version of Psych Engine developed by DuskieWhy and Data") is a Psych-derived FNF engine with a modchart system and "4+ key support" / "2+ strumline support". Its chart file is the Psych `{ "song": { ... } }` JSON ([../psych-json/README.md](../psych-json/README.md)) plus three fields that give it a variable key count and strumline count: `keys`, `lanes`, `arrowSkins`, and a format tag `nmv2`. Everything below is read from the engine's `source/funkin/data/Chart.hx` and `Song.hx` (commit `e7837e2fe1e80fc314d1c69f30ac22e065305588`) and from Moonchart's `FNFNmv`. The chart editor of the engine and real mod charts were not inspected.

## Packaged in

Not packaged: loose JSON files (one per difficulty).

## Container & encoding

- UTF-8 JSON (`FunkinAssets.parseJson`). `Chart.fromSong(songName, difficulty)` loads `Paths.json('$songName/charts/${Difficulty.getDifficultyFilePath(difficulty)}')`; the repository's embedded test chart is `assets/embeds/songs/test/charts/normal.json`, so the layout is `songs/<song>/charts/<difficulty>.json` [observed in the repository tree].
- The file MUST contain a top-level `song` object (`fromData` throws `data provided is invalid` otherwise). The loader recognises Psych (`format` containing `psych_v1`), V-Slice (`version` + `scrollSpeed`) and Codename (`codenameChart`) charts and, in the commit read, REFUSES them with "this is using a incompatible format" (the source comment says "this isnt gonna stay btw").

## Structure / metadata

`Song` typedef (`Song.hx`): `song` (string), `notes` (sections), `events` (array), `bpm` (float), `needsVoices` (bool), optional `trackSwap` (bool), `speed` (float), `keys` (int), `lanes` (int), `player1`, `player2`, `gfVersion`, `stage` (strings), `arrowSkins` (array of strings), optional `format` (string). The old `arrowSkin`/`splashSkin` fields are commented out in the typedef.

`SongSection`: `sectionNotes` (array), `mustHitSection` (bool), optional `sectionBeats` (int), `gfSection` (bool), `bpm` (float), `changeBPM` (bool), `altAnim` (bool).

`Chart.correctFormat` normalises every loaded chart: `player3` becomes `gfVersion`; `keys` defaults to 4 and `lanes` to 2; an empty `arrowSkins` is filled with `"default"` once per lane; a missing `events` array is built from negative-lane pseudo-notes (`[time, <0, name, value1, value2]`, same as old Psych); a missing or NaN `sectionBeats` becomes 4 and `lengthInSteps` is deleted.

## Timing model

As Psych: absolute milliseconds for notes and events, BPM from `bpm` and section `changeBPM`/`bpm`, a section is `sectionBeats` beats (default 4) [inference: the section fields are those of the Psych layout; the engine's `Conductor` was not read].

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, ...]`. `noteData` is an index over all strumlines: `keys` columns per strumline and `lanes` strumlines, so ids run `0 .. keys*lanes - 1` (the conversion code uses `keys * 2`, i.e. two strumlines, when it re-maps a legacy chart). Charts whose `format` is neither `psych_v1` nor `nmv2` are treated as legacy: in every section with `mustHitSection == false` each note with `0 <= noteData < keys*2` is rewritten to `(noteData + keys) % (keys*2)` and `format` is set to `nmv2`. After that the first `keys` ids are the player's side and the next `keys` ids the opponent's, as in `psych_v1` [inference from the rewrite]. The fourth note slot (note type) is not described in `Song.hx`; Unknown for this engine.

## Audio & images

Not in the chart. `arrowSkins` names note skins (e.g. `default`; the repository has `assets/game/data/noteskins/default.json` and `pixel.json`).

## Versions & variants

`format`: `psych_v1`, `nmv2` (written by the engine after conversion); anything else is converted. Moonchart (`FNFNmv extends FNFPsychBasic`) writes `format = "nmv2"` and recognises the files by the keys `arrowSkins`, `keys`, `lanes`; its own comments list translation of events and note types, metadata and lyrics as TODO. An `NmvMetadata` typedef (`composer`, `fontSize`, `description`) and a lyrics JSON (`{ stuff: [ { lyric, timestamp, color } ] }`) exist in Moonchart; their file names were not established.

## Quirks & pitfalls

- The conversion test is an exact string comparison (`format != 'psych_v1' && format != 'nmv2'`), so a Psych chart carrying `psych_v1_convert` (as the Psych repository's base-game charts do, [observed in the manifest file psych_bopeebo.json]) is converted again by NMV [inference from the two string tests].
- `keys`/`lanes` default to 4/2: a reader that ignores them mis-assigns every note of a 5K+ chart.
- The chart loader rejects V-Slice and Codename charts, so those need conversion first.

## Example

Hand-written (synthetic) from `Song.hx`:

```json
{ "song": { "song": "Demo", "bpm": 150, "speed": 2.0, "needsVoices": true,
  "keys": 4, "lanes": 2, "player1": "bf", "player2": "dad", "gfVersion": "gf", "stage": "stage",
  "arrowSkins": ["default", "default"], "format": "nmv2",
  "notes": [ { "sectionBeats": 4, "mustHitSection": true, "gfSection": false, "altAnim": false,
               "changeBPM": false, "bpm": 150, "sectionNotes": [[0, 0, 0], [400, 4, 0], [800, 2, 400]] } ],
  "events": [] } }
```

The player's left arrow at 0 ms, the opponent's left arrow at 400 ms (id 4), the player's up arrow held 400 ms at 800 ms.

## ROX support

Not read as NMV. `.json` goes to the legacy FNF codec ([../legacy-json/README.md](../legacy-json/README.md)); notes of a 4K chart decode through `mustHitSection` or `format`, but `keys` greater than 4 is not understood [inference from the ROX description in the legacy fiche].

## Parsers & tools

- NightmareVision (Haxe): https://github.com/NMVTeam/NightmareVision (`source/funkin/data/Chart.hx`, `Song.hx`, `source/funkin/states/editors/ChartEditorState.hx`, `ChartConverterState.hx`)
- Moonchart `FNFNmv`: https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFNmv.hx

## Getting samples

- Committed: [samples/](samples/) holds two hand-written `nmv2` charts (4K and 5K, `synthetic-*`), see [samples/SOURCES.md](samples/SOURCES.md).
- Manifest: the engine's embedded `test` chart (format-less, converted at load), not committed (FNF test content inside an Apache-2.0 repository).
- More: no real `nmv2` chart was found in a public repository. Mods "that run on NightmareVision" are listed on the FNF wiki category page https://fridaynightfunking.fandom.com/wiki/Category:Mods_that_run_on_NightmareVision (listed by search, not opened); the engine's chart editor (`ChartEditorState.hx`) writes the format [inference from the file name].

## Sources

- https://raw.githubusercontent.com/NMVTeam/NightmareVision/e7837e2fe1e80fc314d1c69f30ac22e065305588/source/funkin/data/Chart.hx
- https://raw.githubusercontent.com/NMVTeam/NightmareVision/e7837e2fe1e80fc314d1c69f30ac22e065305588/source/funkin/data/Song.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/5d9fbc2cb2afed76dd325134c6f9edb757c090a1/src/moonchart/formats/fnf/legacy/FNFNmv.hx
- https://fridaynightfunking.fandom.com/wiki/NightmareVision
