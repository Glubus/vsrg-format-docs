# Samples: DTXMania older chart format (`.gda`)

No real `.gda` file could be obtained (see the `Getting samples` section of the fiche).

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `synthetic-drums-guitar-bass.gda` | hand-written for this repository from the channel table `STGDAPARAM` and `tInput_LineAnalysis_ChipLocation` in https://github.com/limyz/DTXmaniaNX (commit 9cdabe2778d405b3f313c34f5ee7096dcea1aabf, `DTXMania/Code/Score,Song/CDTX.cs`) | this repository's maintainers (agent-authored) | CC0 / public domain (declared) | `synthetic`, ASCII, LF. NOT a copy of a real GDA file: it is what DTXMania's loader accepts for the `.gda` extension. Data lines use the 2-letter channel names in place of the hex channel (`#001HH`, `#001SD`, `#001BD`, `#002HT`, `#002LT`, `#002CY`, tempo `#002TC: 5A` (hex 0x5A = 90), bar length `#002BL: 0.75`, guitar `G1`/`G7`/`GW`, bass `B0`/`B1`, fill-in `FI`), plus the numeric SE names (`#00101`). Header and `#WAVzz` lines are the DTX ones (the loader uses one line parser for GDA, G2D and DTX). Real GDA headers may differ: Unknown. |
