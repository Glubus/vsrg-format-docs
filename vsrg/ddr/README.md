# Dance Dance Revolution (Konami) and DDR-derived chart formats

Category: vsrg. DDR charts are panel/column based (4 arrows single, 8 double, 6 solo); notes scroll vertically to a receptor row.

Konami's DDR (1998-) has an arcade engine whose step data is a proprietary binary (`.ssq`, since 4th Mix) plus two older binary families (`STEP`, `STEP2`, 1st-3rd Mix era). Other "DDR charts" are simulator formats: `.msd` (the first PC simulator script, ancestor of `.dwi`/`.sm`), `.sdf` (Pocket DDR), `.sm/.ssc` (StepMania, the de-facto standard).

The original README lines, checked against sources:

| Original README line | What it really is | Folder |
|---|---|---|
| `.msd`: **Dance Dance Revolution** chart | MSD is the text script format of an early Windows DDR simulator (spec "MSDファイル書式 Ver2.0β1", "developed for DDR'99"), not Konami's. Grandfather of DWI/SM; StepMania still tokenizes its syntax (`#TAG:param:param;`). | [msd](msd/README.md) |
| `.ssq`: **DDR 4th Mix** chart | Konami's arcade/console step format: chunked little-endian binary. First used officially in 4th Mix (appears unreferenced in 3rd Mix Plus), still used in DDR A/World and in DDR Ultramix/Hottest Party ports (with variants). | [ssq](ssq/README.md) |
| `.sdf`: **Pocket DDR** chart, derived from .sm | A compact binary container written by the converter `SM2SDF` ("SM 2 SCF Converter v.1.0 by Robot2037") for Pocket DDR: two PNGs (banner, background) + a compact binary form of an `.sm` (metadata, BPM table, compressed charts). | [sdf](sdf/README.md) |
| (not in original README) DDR `STEP` / `STEP2` | Binary formats of DDR 1st-3rd Mix Plus (as exported by "DDR Utility"); only a stub exists upstream. | [step](step/README.md), [step2](step2/README.md) |

Other DDR-related pieces:

- StepMania `dance-single/double/solo/couple` charts: [../stepmania](../stepmania/README.md).
- DWI: [../dwi](../dwi/README.md). D2R / SLO / SUL: [../legacy-dance-formats](../legacy-dance-formats/README.md) (D2R = "Dazzle Dazzle Realization", a DDR practice program of 1999).
- Converters: [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (SSQ <-> SSC, also Ultramix legacy SSQs), [drmext/ddr-datatools](https://github.com/drmext/ddr-datatools) (`ddr-render.py`: xwb+ssq -> ogg/.sm), RhythmCodex ([SaxxonPike/RhythmCodex](https://github.com/SaxxonPike/RhythmCodex)), Scharfrichter, `ddrcharttool.py` (SM -> SSQ).
- Dance Dance Immolation and DDR Freestyle: no public chart-format documentation found (searches returned only Konami DDR data tooling). In The Groove / ITG and Pump It Up Pro/Infinity charts are StepMania `.sm/.ssc`. Flash Flash Revolution (browser DDR-style engine): [../flash-flash-revolution](../flash-flash-revolution/README.md).

Research hubs: [SaxxonPike/rhythm-game-formats `ddr/`](https://github.com/SaxxonPike/rhythm-game-formats/tree/master/ddr) (`ssq.md`, `step.md`, `step2.md`), ZIv's ["The DDR Research Master Thread"](https://zenius-i-vanisher.com/v5.2/thread?threadid=7564), skogaby's `docs/` (SSQ spec, mine chunk, Hudson/Wii variants, Ultramix archives, XSB).

Format pages added: [`gen/`](gen/README.md) (DDR S+ iOS `.gen`), [`hudson-ssq/`](hudson-ssq/README.md) (type 9 chunk, Mario Mix / Hottest Party 1), [`hudson-ssq-lane/`](hudson-ssq-lane/README.md) (type 16 chunk, Hottest Party 4/5), [`ultramix-archive/`](ultramix-archive/README.md) (Ultramix `x_data`/`.sng`/`.sif`).
