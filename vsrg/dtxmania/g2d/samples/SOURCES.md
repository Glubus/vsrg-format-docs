# Samples: DTXMania older chart format (`.g2d`)

No real `.g2d` file could be obtained (see the `Getting samples` section of the fiche).

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `synthetic-drums-guitar-bass.g2d` | hand-written for this repository from `CDTX.cs` of https://github.com/limyz/DTXmaniaNX (commit 9cdabe2778d405b3f313c34f5ee7096dcea1aabf): `tRead` maps `.g2d` to `EType.G2D`, which shares the GDA channel-name branch | this repository's maintainers (agent-authored) | CC0 / public domain (declared) | `synthetic`, ASCII, **CRLF** (the `.gda` twin is LF). Same content as `../../gda/samples/synthetic-drums-guitar-bass.gda` except the title: 2-letter channel names (`HH`, `SD`, `BD`, `HT`, `LT`, `CY`, `TC`, `BL`, `G1`, `G7`, `GW`, `B0`, `B1`, `FI`). What makes a real G2D differ from GDA is Unknown, so this file only demonstrates the loader-level equivalence. |
