# Etterna

Category: **vsrg**: vertical-scrolling rhythm game built on the StepMania 5.0 code base; notes fall on fixed columns toward a receptor row.

Etterna (a fork of StepMania 5.0, https://github.com/etternagame/etterna, MIT licence) is a keyboard-oriented fork with an online score site (EtternaOnline) and its own difficulty calculator (MSD values). It does **not** use a chart format of its own for authoring: charts are plain StepMania [`.sm`](../stepmania/sm/README.md) and [`.ssc`](../stepmania/ssc/README.md) files (plus the imports below). What Etterna adds are *derived* files and extra tags:

| Artefact | What it is | Fiche |
|---|---|---|
| `#CHARTKEY:X<sha1>;` and `#MSDVALUES:` tags | Written into Etterna's cache copies of an `.ssc` chart; the chart key identifies a chart (`"X" + hex(SHA-1(note types + BPM per non-empty row))`, `Steps::GenerateChartKey`); MSD values are the per-skillset difficulty ratings. They are **not** present in hand-authored `.sm`/`.ssc` files [observed in `NotesWriterSSC.cpp`, `NotesLoaderSSC.cpp` (`steps_tag_handlers["CHARTKEY"]`)]. | [`ssc`](../stepmania/ssc/README.md) |
| `.ett` | A song file in an SSC-derived dialect with a compact 4-key note encoding; written by `NotesWriterETT`, but nothing in the source reads or calls it. | [`ett`](ett/README.md) |
| `songdata.cache`, `<chartkey>.cache` | Per-song SSC cache text and per-chart binary arrays of `{notes bitmask, row time}` that the pack builder and online pack installer produce. | [`cache`](cache/README.md) |
| `Save/ReplaysV2/` | Replay files of played scores (`FULL_REPLAY_DIR = "/Save/ReplaysV2/"` in `ReplayConstantsAndTypes.h`). **Not charts** and not documented here. | n/a |

Chart files read by the Etterna loaders (`src/Etterna/Models/NoteLoaders`, commit `2d706147cc4bcf95a8ceb24dc4f4129be207f803`): `.ssc`, `.sma`, `.sm`, `.dwi`, `.bms`/`.bme`/`.bml`, `.ksf`, `.osu` (`NotesLoader::LoadFromDir` tries them in that order). Writers: `.sm`, `.ssc`, `.dwi`, `.ett`. There is no `.crs` loader any more, and `.edit` files are not documented here.

Format folders: [`ett/`](ett/README.md), [`cache/`](cache/README.md). Related: [StepMania family](../stepmania/README.md).

Samples: Etterna's own repository ships only theme music `.sm`/`.ssc` files; they are committed under [`../stepmania/sm/samples`](../stepmania/sm/samples/SOURCES.md) and [`../stepmania/ssc/samples`](../stepmania/ssc/samples/SOURCES.md) (`etterna_*`).

Links: https://github.com/etternagame/etterna, https://etternaonline.com.
