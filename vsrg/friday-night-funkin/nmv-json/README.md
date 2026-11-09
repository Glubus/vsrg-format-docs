# FNF Nightmare Vision chart (`format: "nmv2"`, Psych-derived JSON with `keys`/`lanes`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview

NightmareVision (NMVTeam; the FNF wiki: "a modified version of Psych Engine developed by DuskieWhy and Data") is a Psych-derived engine with a modchart system and "4+ key support" / "2+ strumline support". Its chart is the Psych `{ "song": { ... } }` JSON ([../psych-json/README.md](../psych-json/README.md)) plus `keys`, `lanes`, `arrowSkins` and the format tag `nmv2`. Sources: `source/funkin/data/Chart.hx` and `Song.hx` (commit `e7837e2fe1e80fc314d1c69f30ac22e065305588`), Moonchart's `FNFNmv`.

## Packaged in

Loose JSON, one file per difficulty.

## Container & encoding

- UTF-8 JSON (`FunkinAssets.parseJson`). `Chart.fromSong(songName, difficulty)` loads `Paths.json('$songName/charts/${Difficulty.getDifficultyFilePath(difficulty)}')`; the repository's embedded test chart is `assets/embeds/songs/test/charts/normal.json`, so the layout is `songs/<song>/charts/<difficulty>.json` [observed in the repository tree].
- The file needs a top-level `song` object (`fromData` throws `data provided is invalid` otherwise). The loader recognises Psych (`format` containing `psych_v1`), V-Slice (`version` + `scrollSpeed`) and Codename (`codenameChart`) charts and refuses them (commit read) with "this is using a incompatible format" (the source comment says "this isnt gonna stay btw").

## Structure / metadata

`Song` typedef (`Song.hx`): `song` (string), `notes` (sections), `events` (array), `bpm` (float), `needsVoices` (bool), optional `trackSwap` (bool), `speed` (float), `keys` (int), `lanes` (int), `player1`, `player2`, `gfVersion`, `stage` (strings), `arrowSkins` (array of strings), optional `format` (string). The old `arrowSkin`/`splashSkin` fields are commented out in the typedef.

`SongSection`: `sectionNotes` (array), `mustHitSection` (bool), optional `sectionBeats` (int), `gfSection` (bool), `bpm` (float), `changeBPM` (bool), `altAnim` (bool).

`Chart.correctFormat` on load: `player3` becomes `gfVersion`; `keys` defaults to 4 and `lanes` to 2; an empty `arrowSkins` is filled with `"default"` once per lane; a missing `events` array is built from negative-lane pseudo-notes (`[time, <0, name, value1, value2]`, same as old Psych); a missing or NaN `sectionBeats` becomes 4 and `lengthInSteps` is deleted.

## Timing model

As Psych: absolute ms, `bpm` and section `changeBPM`/`bpm`, sections of `sectionBeats` beats (default 4) [inference; `Conductor` not read].

## Notes

`sectionNotes[i] = [strumTime, noteData, sustainLength, ...]`. `noteData` is an index over all strumlines: `keys` columns per strumline and `lanes` strumlines, so ids run `0 .. keys*lanes - 1` (the conversion code uses `keys * 2`, i.e. two strumlines, when it re-maps a legacy chart). Charts whose `format` is neither `psych_v1` nor `nmv2` are treated as legacy: in every section with `mustHitSection == false` each note with `0 <= noteData < keys*2` is rewritten to `(noteData + keys) % (keys*2)` and `format` is set to `nmv2`. After that the first `keys` ids are the player's side and the next `keys` ids the opponent's, as in `psych_v1` [inference from the rewrite]. The fourth slot (note type) is not described in `Song.hx`.

## Audio & images

Not in the chart. `arrowSkins` names note skins (e.g. `default`; the repository has `assets/game/data/noteskins/default.json` and `pixel.json`).

## Versions & variants

`format`: `psych_v1`, `nmv2` (written after conversion); anything else is converted. Moonchart (`FNFNmv extends FNFPsychBasic`) writes `format = "nmv2"`, recognises files by `arrowSkins`, `keys`, `lanes`, and lists translation of events, note types, metadata and lyrics as TODO. Moonchart also has an `NmvMetadata` typedef (`composer`, `fontSize`, `description`) and a lyrics JSON (`{ stuff: [ { lyric, timestamp, color } ] }`); their file names are unknown.

## Quirks & pitfalls

- The conversion test is an exact string comparison (`format != 'psych_v1' && format != 'nmv2'`), so a Psych chart carrying `psych_v1_convert` (as the Psych repository's base-game charts do, [observed in samples/psych_bopeebo.json]) is converted again by NMV [inference from the two string tests].
- `keys`/`lanes` default to 4/2; a reader that ignores them mis-assigns every note of a 5K+ chart.
- The loader rejects V-Slice and Codename charts; convert them first.

## Example

Synthetic, from `Song.hx`:

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

Not read as NMV. `.json` goes to the legacy codec ([../legacy-json/README.md](../legacy-json/README.md)): 4K notes decode via `mustHitSection` or `format`; `keys` > 4 is not understood [inference].

## Parsers & tools

- NightmareVision (Haxe): https://github.com/NMVTeam/NightmareVision (`source/funkin/data/Chart.hx`, `Song.hx`, `source/funkin/states/editors/ChartEditorState.hx`, `ChartConverterState.hx`)
- Moonchart `FNFNmv`: https://github.com/MaybeMaru/moonchart/blob/main/src/moonchart/formats/fnf/legacy/FNFNmv.hx

## Observed in real files

Charts made with NightmareVision on GameBanana (e.g. `gb_childs-play.json`) have `keys: 4`, `lanes: 2` and the singular `arrowSkin` / `splashSkin` fields, tab-indented, and no `format` / `arrowSkins` field [observed in samples/gb_childs-play.json, gb_withstand-hard.json, gb_faker.json]. The plural `arrowSkins` of the current `Song.hx` is newer than those files (Chart.hx fills it at load).

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). No real `format: nmv2` file with `arrowSkins` was found. More: https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=NightmareVision&_idGameRow=8694 and https://fridaynightfunking.fandom.com/wiki/Category:Mods_that_run_on_NightmareVision.

## Sources

- https://raw.githubusercontent.com/NMVTeam/NightmareVision/e7837e2fe1e80fc314d1c69f30ac22e065305588/source/funkin/data/Chart.hx
- https://raw.githubusercontent.com/NMVTeam/NightmareVision/e7837e2fe1e80fc314d1c69f30ac22e065305588/source/funkin/data/Song.hx
- https://raw.githubusercontent.com/MaybeMaru/moonchart/5d9fbc2cb2afed76dd325134c6f9edb757c090a1/src/moonchart/formats/fnf/legacy/FNFNmv.hx
- https://fridaynightfunking.fandom.com/wiki/NightmareVision
