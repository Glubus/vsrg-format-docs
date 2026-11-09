# Etterna

Category: vsrg: vertical-scrolling rhythm game on the StepMania 5.0 code base; notes fall on fixed columns toward a receptor row.

Etterna (https://github.com/etternagame/etterna, MIT) is a keyboard-oriented StepMania 5.0 fork with an online score site (EtternaOnline) and its own difficulty calculator (MSD values). Charts are plain StepMania [`.sm`](../stepmania/sm/README.md) and [`.ssc`](../stepmania/ssc/README.md) files (plus the imports below). Etterna adds derived files and extra tags:

| Artefact | What it is | Fiche |
|---|---|---|
| `#CHARTKEY:X<sha1>;` and `#MSDVALUES:` tags | Written into Etterna's cache copies of an `.ssc` chart. The chart key is `"X" + hex(SHA-1(note types + BPM per non-empty row))` (`Steps::GenerateChartKey`); MSD values are per-skillset difficulty ratings. Absent from hand-authored `.sm`/`.ssc` [observed in `NotesWriterSSC.cpp`, `NotesLoaderSSC.cpp` (`steps_tag_handlers["CHARTKEY"]`)]. | [`ssc`](../stepmania/ssc/README.md) |
| `.ett` | SSC-derived song file with a compact 4-key note encoding; written by `NotesWriterETT`, never read or called. | [`ett`](ett/README.md) |
| `Save/ReplaysV2/` | Replay files of played scores (`FULL_REPLAY_DIR = "/Save/ReplaysV2/"` in `ReplayConstantsAndTypes.h`). Not charts. | n/a |

Loaders (`src/Etterna/Models/NoteLoaders`, commit `2d706147cc4bcf95a8ceb24dc4f4129be207f803`) read `.ssc`, `.sma`, `.sm`, `.dwi`, `.bms`/`.bme`/`.bml`, `.ksf`, `.osu` (`NotesLoader::LoadFromDir` tries them in that order). Writers: `.sm`, `.ssc`, `.dwi`, `.ett`. No `.crs` loader remains; `.edit` files are not covered here.

Format folder: [`ett/`](ett/README.md). Related: [StepMania family](../stepmania/README.md).

Samples: Etterna's repository ships only theme music charts, committed under [`../stepmania/sm/samples`](../stepmania/sm/samples/SOURCES.md) and [`../stepmania/ssc/samples`](../stepmania/ssc/samples/SOURCES.md) (`etterna_*`).

Links: https://github.com/etternagame/etterna, https://etternaonline.com.
