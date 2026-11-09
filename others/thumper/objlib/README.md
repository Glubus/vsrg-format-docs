# Thumper object library (`.pc` cache files, `.objlib`) and text objects
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (community text form: Python literals)

## Overview
Thumper's levels live in the game's `cache` folder as binary `.pc` files named by hashes (e.g. `25d1009d.pc`, config `c19c877c.pc`). A level file is an **object library** (`objlib`): a header, a list of `(type hash, name)` pairs, a definition block, then the serialized objects. Seven object types make up a playable level: `SequinLeaf` (`.leaf`: beat-grid pattern, where the cues are), `SequinLevel` (`.lvl`: chain of leaves with loops and approach distance), `SequinGate` (`.gate`: boss section), `SequinMaster` (`.master`: ordering of levels and gates), `EntitySpawner` (`.spn`), `Sample` (`.samp`: audio sample with mode, volume, pitch, pan) and `Xfmer` (`.xfm`: transform). The reverse-engineered writer in RainbowUnicorn7297's modding tool documents the binary layout of these objects and a readable text form (a Python literal list of dictionaries, parsed with `ast.literal_eval`). The game's own reading code is not public; the known layout is only what the tool needs to write. Official levels' full semantics (e.g. every `param_path` name) are only partially known.

## Container & encoding
- Binary, **little-endian**. Primitives (tool `common.py`): `int` = i32; `bool` = 1 byte; `float` = f32; `string` = i32 length + ASCII bytes (no terminator); `color` = 4 f32 (RGBA); `vec3` = 3 f32; `hash` = u32 of the name: FNV-1a 32-bit state (offset basis `0x811c9dc5`, per byte `h = ((h ^ c) * 0x1000193) & 0xffffffff`) followed by the one-at-a-time style final mix `h*=0x2001; h^=h>>7; h*=9; h^=h>>17; h*=0x21` (all mod 2^32).
- Level cache file layout written by `make_custom_levels`: `header.objlib` (raw bytes copied from a template) + `string(objlib_path)` + `obj_list_1.objlib` + `i32(63 + object_count)` + `obj_list_2.objlib` + for each object `hash(obj_type)`, `string(obj_name)` + `obj_def_<level>.objlib` (raw definition block) + serialized objects + `footer_1.objlib` + `float(bpm)` + `footer_2.objlib`. The template blocks are opaque in the tool (copied from original files): their inner structure is unknown.
- Config cache file (second `.pc`): `i32 9`, `i32 section_count`, `string` per `level_sections` (e.g. `SECTION_LINEAR`), then 4 colors `rails_color`, `rails_glow_color`, `path_color`, `joy_color`.
- Levels are installed by copying files into `<Thumper>/cache`; the tool also replaces three original `.pc` files (`2e7b0500`, `e0c51024`, `f78b7d78`). Level save data (scores) lives in the save folder.

## Structure / metadata
Text form per level (`LevelLib` object): `level_name`, `objlib_path` (e.g. `levels/custom/test.objlib`), `cache_filename`, `config_cache_filename`, `bpm` (float, written in the footer), `level_sections`, `rails_color`, `rails_glow_color`, `path_color`, `joy_color`.

Per-object serialization:

| Type | Header ints | Body |
|---|---|---|
| SequinLeaf | `34, 33, 4, 2` | `hash('AnimComp')`, `i32 1`, `f32 0`, `string 'kTimeBeats'`; `hash('EditStateComp')` + sequencer objects; footer `i32 0, i32 beat_cnt, beat_cnt*3 zero i32, 3 zero i32` |
| SequinLevel | `51, 33, 4, 2` | `hash('ApproachAnimComp')`, `1`, `0f`, `'kTimeBeats'`, `0`, `approach_beats`; `EditStateComp` + sequencer objects + leaf sequence (each: `bool true, i32 0, i32 beat_cnt, bool false, string leaf_name, string main_path, i32 sub_path_count, sub paths, string 'kStepGameplay', i32 start_beat, vec3 pos, 3 rotation vec3, scale vec3, 2 zero bytes`) + loops (`string samp_name, i32 beats_per_loop, i32 0`); footer `volume`, `input_allowed`, `tutorial_type`, `start_angle_fracs` |
| SequinGate | `26, 4, 1` | `string spn_name`, param path, boss patterns (node hash, `lvl_name`, sentry type, bucket), footer with `pre_lvl_name`, `post_lvl_name`, `restart_lvl_name`, `section_type`, `random_type` |
| SequinMaster | `33, 33, 4, 2` | skybox, intro level, groupings (`lvl_name`, `gate_name`, `checkpoint`, `checkpoint_leader_lvl_name`, `rest_lvl_name`, `play_plus`), footer with checkpoint level and `'path.gameplay'` |
| EntitySpawner | `1, 4, 2` | `Xfm` component + `objlib_path`, `bucket` |
| Sample | `12, 4, 1` | `mode` (`kSampleOneOff` etc.), `path` (wav), `volume`, `pitch`, `pan`, `offset`, `channel_group` |
| Xfmer | `4, 4, 1` | `xfm_name`, `constraint` (`kConstraintParent`), `pos`, `rot_x/y/z`, `scale` |

**Sequencer objects** (the core of a leaf and a level): `i32 count`, then per object: `string obj_name`, param path (`i32 depth`, then per element `hash(name)` + `i32 index (-1 none)`; text form joins elements with `:` and an index after `,`, e.g. `layer_volume,0`), `i32 trait_type` index into `kTraitInt, kTraitBool, kTraitFloat, kTraitColor, kTraitObj, kTraitVec3, kTraitPath, kTraitEnum, kTraitAction, kTraitObjVec, kTraitString, kTraitCue, kTraitEvent, kTraitSym, kTraitList, kTraitTraitPath, kTraitQuat, kTraitChildLib, kTraitComponent`, then `i32 point_count` and per data point `f32 beat`, value (by trait type: int/bool/float/color/vec3/string), `string interp` (default `kTraitInterpLinear`), `string ease` (default `kEaseInOut`), then `i32 0` and an 18-field footer (`ints`, two strings usually `kIntensityScale`, bools, floats...) whose meaning is unknown.

## Timing model
Beats. Every data point is at a float **beat** position inside its leaf (or level); a leaf has `beat_cnt` beats. The level BPM is a single float in the level footer. `kTimeBeats` is the time unit of the animation component. Levels follow `approach_beats` (default 16) so cues are visible before they hit; leaf placement uses `start_beat` accumulated in the leaf sequence. Tempo is constant per level; the sample files carry tempo in their names (`samp_level1_320bpm`, ... `480bpm`).

## Notes
Cues are not a note array: they are **sequencer tracks** keyed by `param_path`. Examples in the tool's `examples/playable_objects/`:
- `pitch` (`kTraitFloat`, stepped per beat) and `roll`/`turn`/`scale_x`/`scale_z` shape the track geometry; `turn` values like 15, 0, -30 per beat make turns.
- `<name>.ent` paths with `kTraitBool`/`kTraitAction` activate entities at a beat: e.g. in `leaf_2a_thump_types`, `thump.spn` / `thump_rails.ent` at beat 0, `thump_rails_fast_activat.ent` at 16, `thump_checkpoint.ent` at 32, `thump_boss_bonus.ent` at 48 (thump variants); `swerve_off.*`, `center_multi.ent`, `right_multi.*`, `millipede_quarter*`, `speed_streaks_RGB.ent`, `trees_4.ent` are other entity paths; `visible*`, `sequin_speed`, `win`, `win_checkpoint` control visibility, speed and win events. Suffixes `.a01 .a02 .z01 .z02` appear on multi-lane objects.
- `step: True` writes one data point for every beat in `0..beat_cnt-1` (defaults filled in); `step: False` writes only the listed points with interpolation.
- Cue types in the examples (file names): turns, scale, multilane, speed, thump types, multilane thumps, grindables, jumps, millipedes (half/quarter), sentries.
The full list of param paths and their gameplay meaning is not documented here (not found in sources).

## Audio & images
Audio is referenced by `Sample` objects: `path` of a `.wav` inside the game's data (e.g. `samples/drums/level1/massive_rhythms/thumper_absolute2.wav`), `channel_group` (e.g. `thumps_accents.ch`), plus level `loops` (`samp_name`, `beats_per_loop`). The `Sample` object only stores a path, not audio data. Images are not part of the files.

## Versions & variants
- Text-object format of the modding tool (Python literal) versus the CocoaMix86 editor's own project files (not examined). The binary layout above is what the tool (last commit October 2020) writes; compatibility with later game patches is not verified.
- The tool's `templates/` folder contains objects copied from the original levels (README), usable in custom levels as long as `obj_name` values are unique.

## Quirks & pitfalls
- Hash names must match the game's hash; non-ASCII strings cannot be written.
- Object names must be unique (`obj_name`), including across templates.
- Template blocks (`header`, `obj_list_*`, `obj_def_*`, `footer_*`) are copied bytes tied to a specific game version.
- Replacing the three original `.pc` files is how levels are swapped in; restoring needs the originals.

## Example
From the tool's `examples/playable_objects/leaf_2a_thump_types.txt` (trimmed):
```python
{
'obj_type': 'SequinLeaf',
'obj_name': '2a_thump_types.leaf',
'seq_objs': [
    { 'obj_name': 'thump.spn', 'param_path': 'thump_rails.ent', 'trait_type': 'kTraitBool',
      'data_points': { 0:1 }, 'step': True, 'default': 0,
      'footer': (2,1,2,1,2,'kIntensityScale','kIntensityScale',1,0,1,1,1,1,1,1,0,0,0) },
    { 'obj_name': 'thump.spn', 'param_path': 'thump_checkpoint.ent', 'trait_type': 'kTraitBool',
      'data_points': { 32:1 }, 'step': True, 'default': 0,
      'footer': (2,1,2,1,2,'kIntensityScale','kIntensityScale',1,0,1,1,1,1,1,1,0,0,0) }
    ],
'beat_cnt': 64
}
```

## ROX support
Not read by ROX. Beat-timed 3D track script; not a chart in the column sense.

## Parsers & tools
- thumper-modding-tool (Python; text objects to binary `.pc`): https://github.com/RainbowUnicorn7297/thumper-modding-tool
- Thumper Custom Level Editor (C#, WinForms): https://github.com/CocoaMix86/Thumper-Custom-Level-Editor
- Thumper-Modding-Tool-resharp (mod loader): https://github.com/CocoaMix86/Thumper-Modding-Tool-resharp

## Getting samples

Committed in [`samples/`](samples/): six real community text-form objects (leaf, level, config, master) from `RainbowUnicorn7297/thumper-modding-tool`. See [`samples/SOURCES.md`](samples/SOURCES.md) for every file's source URL, fetch date, sha256 and terms. Real binary `.pc` libraries are the game's data: copy them from `<Thumper>/cache` after installing the game.

## Sources
- https://github.com/RainbowUnicorn7297/thumper-modding-tool (`README.md`, `src/levels.py`, `src/common.py`, `examples/playable_objects/*.txt`, `levels/testlevel/*.txt`, `templates/*.txt`)
- https://github.com/CocoaMix86/Thumper-Custom-Level-Editor (README only; project not examined)
