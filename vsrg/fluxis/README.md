# fluXis

Category: **vsrg**: keyboard vertical-scrolling rhythm game (notes fall along 1..N key lanes toward a receptor line, with scroll velocities).

fluXis (https://github.com/InventiveRhythm/fluXis, C#, osu!framework) is a community-driven open-source VSRG. Maps are JSON, one file per difficulty, with a separate effects file and a ZIP package for distribution. The game imports osu!mania, Quaver and StepMania maps by converting them.

Format folders:
- [`fsc/`](fsc/README.md): `.fsc` map (JSON): timing points, SVs, hit objects.
- [`ffx/`](ffx/README.md): `.ffx` effects/events (JSON, legacy text variant).
- [`fms/`](fms/README.md): `.fms` mapset package (ZIP).

Not documented: `.fsb` storyboard (JSON `Storyboard` class) and `.fsk` skin package.

Related: [Quaver](../quaver/README.md), [osu!mania](../osu-mania/README.md), [StepMania](../stepmania/README.md).

Links: https://github.com/InventiveRhythm/fluXis
