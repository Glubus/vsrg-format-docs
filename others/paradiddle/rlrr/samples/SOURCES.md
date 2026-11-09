# Samples: Paradiddle song / kit / recording (`.rlrr`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `defaultset.rlrr` | https://github.com/emretanirgan/ParadiddleUtilities/blob/39d05fc1bb11782de6b9d46d3f9721c9fab0d3c1/PDUtilities/drum_sets/defaultset.rlrr | Emre Tanirgan (ParadiddleUtilities) | GPL-3.0 (repository `LICENSE`) | Drum KIT layout: top-level `instruments` only (10 instruments `BP_HiHat_C_1`, `BP_Kick_C_1`, `BP_Crash15_C_1` ... with `location`/`rotation`/`scale`), no `version`, no `events`, no metadata |
| `synthetic-example_Easy.rlrr` | hand-written for this repository (generated from the schema `docs/rlrrschema.json` of ParadiddleUtilities, v0.7) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` song chart: `version` 0.7, `recordingMetadata`, `audioFileData` (no audio file is shipped; `song.ogg` is only a name), 8 instruments, `bpmEvents` (one tempo), 33 `events` (4 bars of 4/4 at 120 BPM: hi-hat, kick, snare, one crash, `time` as strings with 4 decimals) |
| `synthetic-example_Expert.rlrr` | same | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` song chart: tempo change 120 -> 150 BPM (two `bpmEvents`), 49 `events` with chords at equal `time`, ride, tom and floor-tom fill, velocities 80-127 |

The two `synthetic-*` files were checked by a script for the schema's required keys, `additionalProperties: false` key sets, integer `vel`/`loc`, string `time` and 3-element vectors; they were not loaded into Paradiddle. Instrument positions are placeholder values, not a playable kit layout. The converter's habit of writing tempo in a top-level `bpmEvents` array (not in `events`) is followed (source: `PDUtilities/midiconvert.py`).
