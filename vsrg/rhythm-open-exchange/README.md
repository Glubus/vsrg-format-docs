# Rhythm Open Exchange (ROX)

ROX is "a universal, compact binary format for Vertical Scrolling Rhythm Games (VSRG)" used as a pivot between game formats ("a ffmpeg of vsrg", README). It is the chart model and library behind Prism's map library (`rhythm-open-exchange`, crate `rhythm-open-exchange` 0.8.1, MIT, by Glubus; repository https://github.com/Glubus/rhythm-open-exchange). The in-memory type is `RoxChart` (fixed key count, Tap/Hold/Burst/Mine notes, BPM and scroll-velocity points, microsecond times, hitsounds), and it has three native serialisations of that one model, all documented here from the ROX source:

| Format | Folder | Encoding | Status |
|---|---|---|---|
| `.rox` | [rox/](rox/README.md) | binary: magic `ROX\0` + zstd(rkyv archive) | complete |
| `.jrox` | [jrox/](jrox/README.md) | JSON (serde) | complete |
| `.yrox` | [yrox/](yrox/README.md) | YAML (serde) | complete |

Category stated for the README index: **interchange** (it is a pivot format between games, not a game's own format). In the machine-readable JSON index of this documentation set the category field is `vsrg`, because the model is VSRG-only (fixed columns).

Also here: the ROX data model (`src/model/*`), shared by the three serialisations, is described once in [rox/README.md](rox/README.md#model-types); jrox and yrox refer to it.

ROX 0.8.1 (the vendored copy) reads and writes `.osu` (mania; taiko decode only), `.sm`, `.ssc`, `.qua`, `.mc` (Malody key mode), FNF legacy `.json` and the three native formats; the other formats documented in this repository are not read (BMS, O2Jam and Clone Hero are "planned" in the ROX README).

Sources: `rhythm-open-exchange/{README.md,CHANGELOG.md,wiki.wiki/*,src/**}`.
