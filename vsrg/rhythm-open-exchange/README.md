# Rhythm Open Exchange (ROX)

ROX is "a universal, compact binary format for Vertical Scrolling Rhythm Games (VSRG)", a pivot between game formats ("a ffmpeg of vsrg", README). It is the chart model and library behind Prism's map library (crate `rhythm-open-exchange` 0.8.1, MIT, by Glubus; https://github.com/Glubus/rhythm-open-exchange). The in-memory type is `RoxChart` (fixed key count, Tap/Hold/Burst/Mine notes, BPM and scroll-velocity points, microsecond times, hitsounds), with three native serialisations of that one model, documented here from the ROX source:

| Format | Folder | Encoding | Status |
|---|---|---|---|
| `.rox` | [rox/](rox/README.md) | binary: magic `ROX\0` + zstd(rkyv archive) | complete |
| `.jrox` | [jrox/](jrox/README.md) | JSON (serde) | complete |
| `.yrox` | [yrox/](yrox/README.md) | YAML (serde) | complete |

The README index lists it under **interchange** (a pivot between games). The machine-readable JSON index uses `vsrg`, since the model is VSRG-only (fixed columns).

The data model (`src/model/*`) is shared by all three serialisations and described once in [rox/README.md](rox/README.md#model-types).

ROX 0.8.1 (the vendored copy) reads and writes `.osu` (mania; taiko decode only), `.sm`, `.ssc`, `.qua`, `.mc` (Malody key mode), FNF legacy `.json` and the three native formats. Other formats documented in this repository are not read (BMS, O2Jam and Clone Hero are "planned" in the ROX README).

Sources: `rhythm-open-exchange/{README.md,CHANGELOG.md,wiki.wiki/*,src/**}`.
