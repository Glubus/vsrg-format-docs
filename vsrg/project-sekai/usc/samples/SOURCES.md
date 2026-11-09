# Samples: Universal Sekai Chart (USC)

## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-12lane.usc` | hand-written for this repository | vsrg-format-docs | CC0 | `synthetic`: bare `{offset, objects}` form |

## Real charts (fetched or converted 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `susc-converter_ccmmw.usc` | https://raw.githubusercontent.com/Kyonkrnk/susc-converter/8aebc413a6c17f18283e367f67b8f1424f5ee4da/tests/ccmmw.usc | 2026-11-09 | 7d26109efa5c3fbc5195934fc47589879a770001e6f7dcf43c642677aca82e15 | Kyonkrnk | MIT | Real MMW4CC-style USC |
| `susc-converter_ccmmw.json` | https://raw.githubusercontent.com/Kyonkrnk/susc-converter/8aebc413a6c17f18283e367f67b8f1424f5ee4da/tests/ccmmw.json | 2026-11-09 | a36ff2e4c6c58e1e2ab49cbf59125b13e5558dab7be37d744158a18e40949277 | Kyonkrnk | MIT | Same chart as the .usc, pretty-printed (4-space indent) wrapper form |
| `rgconv_sekaibest_0001_01_easy.usc` | converted locally with rg-converters (`usc.export`) from https://storage.sekai.best/sekai-jp-assets/music/music_score/0001_01/easy.txt | 2026-11-09 | 92a62adc6d3afc6c301dabce2e05a992594e81093a2335fcaaf6e770d4b3b9a5 | rg_converters output; chart by Sega / Colorful Palette | GPL-3.0 (converter); official data | Converted, not downloaded: compact wrapped USC with `timeScaleGroup`; sha256 is of the converted file |
| `rgconv_sekaibest_0001_01_expert.usc` | converted locally with rg-converters (`usc.export`) from https://storage.sekai.best/sekai-jp-assets/music/music_score/0001_01/expert.txt | 2026-11-09 | a0f084973589bd62aba8a1020ccb04be63f858abadabd71d22448b588e63ae7e | rg_converters output; chart by Sega / Colorful Palette | GPL-3.0 (converter); official data | Converted, not downloaded: compact wrapped USC with `timeScaleGroup`; sha256 is of the converted file |
| `rgconv_sekaibest_0003_01_master.usc` | converted locally with rg-converters (`usc.export`) from https://storage.sekai.best/sekai-jp-assets/music/music_score/0003_01/master.txt | 2026-11-09 | 67e6ee06674bdb9b6f14ea8a07b0d8ef641d7e498877293f86ceb60487151389 | rg_converters output; chart by Sega / Colorful Palette | GPL-3.0 (converter); official data | Converted, not downloaded: compact wrapped USC with `timeScaleGroup`; sha256 is of the converted file |
| `rgconv_sekaibest_0010_01_expert.usc` | converted locally with rg-converters (`usc.export`) from https://storage.sekai.best/sekai-jp-assets/music/music_score/0010_01/expert.txt | 2026-11-09 | 11f900e287c96131d2bb725f719a9e9933a2289e3b33844029c9734721b30be7 | rg_converters output; chart by Sega / Colorful Palette | GPL-3.0 (converter); official data | Converted, not downloaded: compact wrapped USC with `timeScaleGroup`; sha256 is of the converted file |
| `rgconv_pjsk-engine-extended_expert.usc` | converted locally with rg-converters (`usc.export`) from Tell Your World expert from PurplePalette/sonolus-pjsekai-engine-extended `src/level/data/expert.sus` | 2026-11-09 | 6885c6bc8c600a284aa54f17a9273b08a7d72a0f28f9ae0007ae2edc82063710 | rg_converters output; chart by Sega / Colorful Palette | GPL-3.0 (converter); official data | Converted, not downloaded: compact wrapped USC with `timeScaleGroup`; sha256 is of the converted file |

## Notes
sonolus-pjsekai-engine (MIT, commit `0f6f37fc9b512b9d156ec4c00d998fe3916b157d`) ships only Sonolus LevelData (`shared/src/level/data/append.json`, 1.2 MB), a different format (see others/sonolus), so it is not included. Sonolus servers (e.g. https://untitledcharts.com/sonolus/levels/list) serve LevelData, not USC.
