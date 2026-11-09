# Samples: Ragnarock map (`info.dat` + difficulty `.dat`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-info.dat` | hand-written from the field handling of `Classes/MapEditor/RagnarockMap.cs` (Edda, PKBeam/Edda commit a9e7fe2de798c177568a58f642135b3343b93d2e) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` `info.dat`: `_version` "1", `_beatsPerMinute`, `_songFilename`, `_environmentName` Midgard, `_difficultyBeatmapSets` with characteristic `Standard` and two difficulties (`Easy`, `Hard`) whose `_beatmapFilename` point to the two files below (renamed with a `synthetic-` prefix), per-map `_customData` |
| `synthetic-Easy.dat` | same | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` difficulty file: 8 notes (`_lineIndex` 0-3, `_lineLayer` 1, `_type` 0, `_cutDirection` 1), no BPM changes |
| `synthetic-Hard.dat` | same | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` difficulty file: 34 notes in half-beat steps including two simultaneous notes at beat 20, two `_BPMChanges` (120 -> 150 BPM at beat 16) and one bookmark in `_customData` |

Notes: the files follow what Edda (GPL-3.0) validates (`ValidateInfo`, `ValidateMap`) and writes (`InitInfo`, `AddMap`, `SetNotesForMap`): note `_type` must be 0 and `_cutDirection` 1, `_lineIndex` 0-3, `_lineLayer` 0-3. They were not opened in Edda or in the game. In a real map folder the files are called `info.dat`, `Easy.dat`, `Normal.dat`, `Hard.dat`; the `synthetic-` prefix is only a repository convention. No real community map could be committed (RagnaCustoms maps are third-party works with audio).
