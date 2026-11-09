# Ragnarock map (`info.dat` + difficulty `.dat`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
Ragnarock custom songs use a folder/zip of JSON files modelled on the Beat Saber v2 map format (`info.dat`, difficulty `.dat`, audio, cover). Primary statement: "Ragnarock's beatmap format is derived from Beat Saber's ... there are major differences between Beat Saber and Ragnarock's song formats. Some aspects of Beat Saber's song format don't translate well to Ragnarock's, and others are unused or missing entirely" (Edda site). The field set below was read from the source of the editor Edda (PKBeam/Edda, GPL-3.0: `Classes/MapEditor/RagnarockMap.cs`, `Classes/EddaConstants.cs`); it is what Edda writes and validates, not a published specification of the game's own reader.

## Container & encoding
JSON text; distributed as a ZIP of the map folder via RagnaCustoms (inferred from the site's "download maps" flow). See [Beat Saber info-dat](../../beat-saber/info-dat/README.md) and [dat](../../beat-saber/dat/README.md) for the base schema.

## Structure / metadata / Timing model / Notes
`info.dat` (Edda `InitInfo` / `ValidateInfo`): `_version` (string `"1"`), `_songName`, `_songSubName`, `_songAuthorName`, `_levelAuthorName`, `_explicit` (string `"false"`), `_beatsPerMinute` (number > 0), `_shuffle`, `_shufflePeriod`, `_previewStartTime`, `_previewDuration` (Edda's source comments the shuffle/preview fields as "unused?"), `_songApproximativeDuration`, `_songFilename` (Edda default `song.ogg`), `_coverImageFilename`, `_environmentName` (Edda offers Midgard, Alfheim, Nidavellir, Asgard, Muspelheim, Helheim, Hellfest, Sabaton, Empty, DarkEmpty), optional `_songTimeOffset`, `_customData` (`_contributors`, `_editors`), and `_difficultyBeatmapSets[0]` = `{_beatmapCharacteristicName: "Standard", _difficultyBeatmaps: [...]}` with at most three maps named `Easy`, `Normal`, `Hard` (files `Easy.dat`, ...); each map entry has `_difficulty`, `_difficultyRank` (1-99 accepted), `_beatmapFilename`, `_noteJumpMovementSpeed`, `_noteJumpStartBeatOffset` and `_customData` (`_editorOldOffset`, `_editorGridSpacing`, `_editorGridDivision`, `_warnings`, `_information`, `_suggestions`, `_requirements`; `_information` strings `medal_<n>=<distance>` store medal distances). Difficulty `.dat`: `_version`, `_customData` {`_time`, `_BPMChanges` [{`_BPM`, `_time`, `_beatsPerBar`, `_metronomeOffset`}], `_bookmarks` [{`_time`, `_name`}]}, `_events`, `_notes` [{`_time`, `_lineIndex`, `_lineLayer`, `_type`, `_cutDirection`}], `_obstacles`. Edda accepts only `_time` >= 0, `_lineIndex` 0-3 (the four drums), `_lineLayer` 0-3 (it writes 1), `_type` 0 and `_cutDirection` 1; a source comment says the game does not check the map `_version`. `_time` is presumably in beats, as in Beat Saber v2 [inference].

## Audio & images
Unknown (presumably referenced by filename from `info.dat` as in Beat Saber [inference]).

## Versions & variants
Unknown.

## Quirks & pitfalls
Do not assume Beat Saber field semantics (hand colors, cut directions) apply.

## Example
Hand-written, built from the Edda source: [samples/synthetic-info.dat](samples/synthetic-info.dat), [samples/synthetic-Easy.dat](samples/synthetic-Easy.dat), [samples/synthetic-Hard.dat](samples/synthetic-Hard.dat). No real community map was read.

## ROX support
Not read by ROX.

## Parsers & tools
- Edda (C#, WPF): https://github.com/PKBeam/Edda
- MediocreMapAssistant2: https://git.bsmg.dev/Top_Cat/MediocreMapAssistant2
- taiko midi to json for Ragnarock: https://github.com/jjcosmos/taiko (seen in search only)

## Getting samples

- Committed ([samples/](samples/), see [samples/SOURCES.md](samples/SOURCES.md)): 8 real maps from RagnaCustoms (`info.dat` + every difficulty `.dat`, prefixed `ragnacustoms<id>_`) and 3 hand-written `synthetic-*` files built from the Edda source. Audio and covers were not kept.
- More: `https://ragnacustoms.com/songs/ddl/<id>` returns the map zip (observed 2026-11-09, ids up to about 6600; some ids answer 403); the site FAQ (https://ragnacustoms.com/getting-started) describes the app and the `CustomSongs` folder (`Documents\Ragnarock\CustomSongs` or the Steam folder; Quest `Android/data/com.wanadev.ragnarockquest/files/UE4Game/Ragnarock/Ragnarock/Saved/CustomSongs`). Create maps with Edda (https://pkbeam.github.io/Edda/). [observed in samples/ragnacustoms6608_info.dat: `_version` is `"1.0.0"`, not `"1"` as Edda writes]

## Sources
- https://pkbeam.github.io/Edda/
- https://ragnacustoms.com/getting-started (search snippet)
