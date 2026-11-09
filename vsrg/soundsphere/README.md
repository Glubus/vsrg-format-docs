# rizu (soundsphere)

Category: **vsrg**: keyboard vertical-scrolling rhythm game engine (osu!mania/BMS/O2Jam/Quaver/StepMania/IIDX-style columns, also osu!standard/catch experiments).

rizu (repository `semyon422/rizu`, Lua/LuaJIT; the chart format tag `sphere` and the name soundsphere refer to the same engine lineage [inference]) is a community engine that plays charts from many games by decoding them into one internal model (`chart/`): decoders exist for osu!, BMS, O2Jam, Quaver, StepMania, K-Shoot Mania, IIDX (`.1`, `.2dx`, `.s3p`, `.ifs`) and MIDI. It has its own text chart format, SPH.

Format folders:
- [`sph/`](sph/README.md): `.sph` text chart format.
- [`nanochart/`](nanochart/README.md): `.nanochart` compact binary note stream (replays/previews).

Related: [osu!mania](../osu-mania/README.md), [BMS](../bms/README.md), [Quaver](../quaver/README.md), [StepMania](../stepmania/README.md), [beatmania IIDX](../beatmania-iidx/README.md).

Links: https://github.com/semyon422/rizu
