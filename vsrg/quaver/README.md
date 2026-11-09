# Quaver

Quaver is a free, open-source (C#, MonoGame) competitive vertical-scrolling rhythm game on Steam and Mac/Windows, developed by Swan and the Quaver team since 2017. It plays 4K and 7K (the format also allows 1-10 keys and an optional scratch lane), has online ranking, a built-in editor and importers for osu!, StepMania and Malody maps.

Category: vsrg (fixed lanes, vertical scrolling).

Formats:

| Format | Folder | Status |
|---|---|---|
| `.qua` map (YAML), one per difficulty | [qua/](qua/README.md) | complete |

Reference implementation: https://github.com/Quaver/Quaver.API (the `Qua` class); game: https://github.com/Quaver/Quaver; site and downloads: https://quavergame.com/; wiki: https://wiki.quavergame.com/.

ROX: `.qua` read + write (Keys4/Keys7 only), `.qp` not read.
