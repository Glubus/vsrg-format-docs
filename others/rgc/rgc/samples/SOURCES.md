# Samples: RGC (Rhythm Game Chart) (`.rgc`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `calibration.rgc` | https://github.com/rhythm-gaming/rgc/blob/724560c47a12fd2d13170370f1e2b8074d482951/test/chart/sdvx/calibration.rgc | HEXAGON (converted by the rgc authors) | MIT (`LICENSE`, (c) 2025 r-g.kr) | real SDVX chart: `header.version` 0.2.0, `game` sdvx, `timing.res` 1, one BPM (120), one 4/4 signature, lane group `bt` with `dim` 0 and four lanes of compact notes (bare integer ticks) |
| `synthetic-all-features.rgc` | hand-written from `docs/spec.md` of rhythm-gaming/rgc (same commit) | vsrg-format-docs | CC0 | `res` 24, negative `offset`, BPM 150.5 at tick 384, 4/4 -> 3/4 at tick 192, `dim` 0/1/2 lane groups (empty-string id, `laser`, `osu`), compact and full notes, tick as string `"60"`, custom `meta.level` and top-level field |

`synthetic-all-features.rgc` was checked by eye against the spec, not run through the TypeScript library.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `vsrg-chart-view_test.rgc` | https://raw.githubusercontent.com/rhythm-gaming/vsrg-chart-view/cb9a762daaca23c2d3ba562b7554907a7aa480a5/serve/test.rgc | 2026-11-09 | 27a70b63f19cc606142f989471e17618793bdc8b46f5e23e681b0849c95b3c69 | rhythm-gaming | MIT (repository LICENSE) | tiny test chart: `header.version` 0.1.0, `game` popn, `res` 4, lane group `note` with `dim` 0 |
