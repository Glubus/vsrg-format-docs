# Legacy and obscure dance-game formats

Category: vsrg (DDR-style fixed panel/lane charts, scrolling vertically), except where noted.

Formats listed in the original README without a proper reference. Each has its own folder (sources in each page).

| Folder | Original README line | What it is | Doc status |
|---|---|---|---|
| [`d2r/`](d2r/README.md) | `.d2r`: Obscure old Japanese format | Dazzle Dazzle Realization 2ndMIX (1999 Windows DDR practice program) chart file; format page reverse-engineered by the editor's author | partial (format described from a Wayback copy) |
| [`slo/`](slo/README.md) | `.slo`: Obscure old Japanese format | one-hand-editing variant written by "SLOEDIT" of the same site | stub |
| [`sul/`](sul/README.md) | `.sul`: `paramax.hypermart.net` link | the older D2R chart format ("symbols used by the previous version's charts (`*.sul`)") | stub |
| [`step/`](step/README.md) | `.step` (empty) | most likely pyDDR/pydance `.step`, superseded by `.dance` (also: DDR "STEP" in [ddr/step](../ddr/step/README.md)) | stub |
| [`ftb/`](ftb/README.md) | `.ftb`: Raindrop reader | Raindrop's "simplest possible" 7-key text chart (`NoteLoaderFTB.cpp`) | partial (loader read) |
| [`directmove/`](directmove/README.md) | `???`: DirectMove | Korean Pump simulator; its charts are `.ksf` with an extended grammar | partial (see [kick-it-up/ksf](../kick-it-up/ksf/README.md)) |

The D2R family comes from the site "D2R譜面サーチ" (paramax.hypermart.net): a chart database and editors "D2REDIT" (reads `*.d2r`, `*.sul`, `*.msd`, `*.ddr`; writes `*.d2r`, `*.ddr`, `*.slo`) and "SLOEDIT" (reads/writes `*.slo`). `*.ddr` is a further format of that scene with no documentation found.

Searched for, nothing documented: DDR-like clones ("Dance Dance Immolation", Freestyle), Pump `.nx`/`.pump`, GroovyStats (a score site, not a format; see [stepmania](../stepmania/README.md#grooveStats-chart-hash) for the "GrooveStats" chart hash).

Related: [StepMania family](../stepmania/README.md), [DDR](../ddr/README.md), [pydance](../pydance/README.md), [Kick It Up](../kick-it-up/README.md).
