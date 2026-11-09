# Samples: osu!lazer beatmap archive (`.olz`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| decimal-timing-beatmap.olz | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/decimal-timing-beatmap.olz | ppy/osu contributors | MIT (ppy/osu LICENCE, Copyright (c) 2025 ppy Pty Ltd) | 1 entry only: `underscores - Count of three (You can eat ____) (fmthesis) [Normal].osu`, osu file format v128, Mode 0, decimal (non-integer) timing point and hit object times, UTF-8 BOM, 990 bytes; no audio |
| fractional-coordinates.olz | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/fractional-coordinates.olz | ppy/osu contributors | MIT (ppy/osu LICENCE, Copyright (c) 2025 ppy Pty Ltd) | 2 entries: a v128 `.osu` with fractional object coordinates and a `__MACOSX/._...osu` resource-fork entry (zip flag bit 3 set, i.e. made by macOS Archive Utility), 1359 bytes; no audio |
| legacy-export-stability-test.olz | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/legacy-export-stability-test.olz | ppy/osu contributors | MIT (ppy/osu LICENCE, Copyright (c) 2025 ppy Pty Ltd) | 1 entry `legacy export - stability test (spaceman_atlas) [].osu`, v128, sliders with mixed curve types (P, B, L) and an empty Version; the test file for the stable-compatible export path (`LegacyBeatmapExporter`), 946 bytes; no audio |

## Notes

- Verified by reading the archives with Python `zipfile`: all three are ordinary ZIP files holding `.osu` entries (no audio or images, so they are committed unchanged). The `.osu` inside begin with `osu file format v128` (lazer's own version number), unlike the `v14` written for stable.
