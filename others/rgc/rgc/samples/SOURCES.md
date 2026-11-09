# Samples: RGC (Rhythm Game Chart) (`.rgc`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `calibration.rgc` | https://github.com/rhythm-gaming/rgc/blob/724560c47a12fd2d13170370f1e2b8074d482951/test/chart/sdvx/calibration.rgc | HEXAGON (original k-shoot mania "Calibration" chart, per the file's `meta`); converted by the rgc authors | MIT (rhythm-gaming/rgc `LICENSE`, (c) 2025 r-g.kr) | real small SDVX chart: `header.version` 0.2.0, `game` sdvx, `timing.res` 1, one BPM (120), one 4/4 signature, lane group `bt` with `dim` 0 and four lanes of compact notes (bare integer ticks) |
| `synthetic-all-features.rgc` | hand-written from `docs/spec.md` of rhythm-gaming/rgc (same commit) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic`: `res` 24, negative `offset`, two BPM entries (the second at tick 384, 150.5 BPM), a 4/4 -> 3/4 signature change at tick 192, lane groups of `dim` 0, 1 and 2 (empty-string group id, `laser`, `osu`), compact notes (`t`, `[k,t,l,p]`, `[k,t,[v],l,p]`) and full object notes (`id`, `k`, `l`, `v`, `w`, `p`), a tick given as the string `"60"`, a custom `meta.level` and a custom top-level field |

Notes: `synthetic-all-features.rgc` was checked by eye against the spec (note ordering, `Pos` shapes, signature/resolution constraints) but not run through the TypeScript library.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `vsrg-chart-view_test.rgc` | https://raw.githubusercontent.com/rhythm-gaming/vsrg-chart-view/cb9a762daaca23c2d3ba562b7554907a7aa480a5/serve/test.rgc | 2026-11-09 | 27a70b63f19cc606142f989471e17618793bdc8b46f5e23e681b0849c95b3c69 | rhythm-gaming | MIT (repository LICENSE) | tiny test chart: `header.version` 0.1.0, `game` popn, `res` 4, lane group `note` with `dim` 0 |
