# Samples: Cytus II / Cytoid chart (C2) (`.json`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-c2.json` | hand-written from the fiche field list (Cytoid wiki C2 format) | OthersA | CC0 / public domain | synthetic. 120 BPM (500000 us per 480 ticks), 4 pages, notes of type 0 |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `8bit_adventurer/ex.txt` | https://raw.githubusercontent.com/Cytoid/Cytoid/bd4eb6eea8accf7c832e4c9a957eafe27f1ef4cf/engines/unity/Assets/StreamingAssets/Levels/io.cytoid.8bit_adventurer.cytoidlevel | 2026-11-09 | c06992e95bf99ae946e8a9c87864265e4e686021eac7d7ff1daf5e934071b01e | TAR1412 vs HUNTER | GPL-3.0 repo | extracted from io.cytoid.8bit_adventurer.cytoidlevel (bundled in the Cytoid repo); C2-style JSON (174020 bytes), difficulty file named |
| `8bit_adventurer/ez.txt` | https://raw.githubusercontent.com/Cytoid/Cytoid/bd4eb6eea8accf7c832e4c9a957eafe27f1ef4cf/engines/unity/Assets/StreamingAssets/Levels/io.cytoid.8bit_adventurer.cytoidlevel | 2026-11-09 | c06992e95bf99ae946e8a9c87864265e4e686021eac7d7ff1daf5e934071b01e | TAR1412 vs HUNTER | GPL-3.0 repo | extracted from io.cytoid.8bit_adventurer.cytoidlevel (bundled in the Cytoid repo); C2-style JSON (71391 bytes), difficulty file named |
| `8bit_adventurer/hd.txt` | https://raw.githubusercontent.com/Cytoid/Cytoid/bd4eb6eea8accf7c832e4c9a957eafe27f1ef4cf/engines/unity/Assets/StreamingAssets/Levels/io.cytoid.8bit_adventurer.cytoidlevel | 2026-11-09 | c06992e95bf99ae946e8a9c87864265e4e686021eac7d7ff1daf5e934071b01e | TAR1412 vs HUNTER | GPL-3.0 repo | extracted from io.cytoid.8bit_adventurer.cytoidlevel (bundled in the Cytoid repo); C2-style JSON (107677 bytes), difficulty file named |
| `cyl_package_tool_test_cyl_chart.json` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/test_cyl_chart.json | 2026-11-09 | ed553038b55b7b3393c1b17d05dccd2f2a5f054cc46c1c14d360bcf960828dfd | ky_reflection | MIT | Cytus II style JSON: 62 KB chart with `format_version` 1, `start_offset_time`, `end_offset_time`, `is_start_without_ui`, per-page `PositionFunction` |
| `cyl_package_tool_viewer_drag_chain.json` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/viewer_drag_chain.json | 2026-11-09 | 7ac7ce667c1d31cc3c6ca039ac254128e14f89f48b1cbd5cd8cb3d9b890b8b5d | ky_reflection | MIT | Cytus II style JSON: 998-byte chart with a drag head (type 3, id 99) and |
| `cyl_package_tool_viewer_single_click.json` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/viewer_single_click.json | 2026-11-09 | bfa792c1c6830946ca2174f27241290fabc38193deaf6528b484b49b0990f0f4 | ky_reflection | MIT | Cytus II style JSON: 595-byte chart: one page with a `PositionFunction` object |
| `cyl_package_tool_viewer_two_page.json` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/viewer_two_page.json | 2026-11-09 | eb5867b2aa1bc338a712f3c18f2b969ecae0c68400e96e47e688da1e7a38b428 | ky_reflection | MIT | Cytus II style JSON: 978-byte chart with two pages |
| `cytoid-chart-editor_chovvy.test_chart-extreme.json` | https://github.com/CatalinTermure/Cytoid-Chart-Editor/blob/fc36b7a0acce5062ab50cc4f1742d91c4f72446d/Assets/Editor/Resources/chovvy.test/chart-extreme.json | 2026-11-09 | 6a402dcc2bec705ff1c4067be6d73ed1a1527abdf0ce2a02ab29b18be9fe9b89 | chovvy | GPL-3.0 | real Cytoid C2 chart from an editor test level: `format_version` 0, `time_base` 480, 116 pages |
