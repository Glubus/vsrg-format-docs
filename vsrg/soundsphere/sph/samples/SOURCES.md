# Samples: SPH chart
All files: https://github.com/semyon422/rizu at `cf4603379dcab949d3510b8c31d1d3e421df6ec0` (GPL-3.0). Test files are the Lua long-string literals of the repo tests, extracted byte for byte (Lua drops the newline after `[[`; the one before `]]` is kept).
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rizu-test-close_point_in.sph`, `rizu-test-close_point_out.sph` | same file, `test.close_point` (`s_in`, `s_out`) | semyon422 | GPL-3.0 | encoder input / normalised output (close visual points) |
| `rizu-test-close_point_2_layers_in.sph`, `rizu-test-close_point_2_layers_out.sph` | same file, `test.close_point_2_layers` | semyon422 | GPL-3.0 | two layers (`v2`, `v3`), negative expand (`e-2`) |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)
| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `rizu-sea-chart_1.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/sea/chart/samples/chart_1.sph | 2026-11-09 | `fcd79b59484d400e73ff0caf5e75ad95504c2680cd98fe1a243523821b947442` | semyon422 | GPL-3.0 | repo sample chart, 4key jumptrill with = anchors and + fractions |
| `rizu-test-basic.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.basic, extracted string) | 2026-11-09 | `5e3f11edc695f1e0a5d92e82bf9d9ae30424ab0ba7503a52d8c6c6b5a49e22b8` | semyon422 | GPL-3.0 | sounds, volumes, velocities, expand, measure marker, holds, comments |
| `rizu-test-visuals.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.visuals) | 2026-11-09 | `483c0d3f081049c614eb958f5269f7e214dad85ecf5b1f0fe05956439a9922a5` | semyon422 | GPL-3.0 | named visual layers |
| `rizu-test-close_point_in.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.close_point s_in) | 2026-11-09 | `27ff127584f133742346e68192818bbc198c46f9a211100804fff5d2d8ea937b` | semyon422 | GPL-3.0 | encoder input |
| `rizu-test-close_point_out.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.close_point s_out) | 2026-11-09 | `3b1d9379939abe88e54a97516a2b430f3420e148753de46ff41d2ff1dbd22817` | semyon422 | GPL-3.0 | normalised output |
| `rizu-test-close_point_2_layers_in.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.close_point_2_layers s_in) | 2026-11-09 | `240797290de340b74c6735732985b67518b63b9cd0efc75b30034cacd13b589c` | semyon422 | GPL-3.0 | two layers input |
| `rizu-test-close_point_2_layers_out.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/EncodeDecode_test.lua (test.close_point_2_layers s_out) | 2026-11-09 | `b4d37ad7586dd02515051a86111e0f8d25365b2e4d555f7716275902dfa22fc9` | semyon422 | GPL-3.0 | two layers output |
| `rizu-test-sph-sounds_z85.sph` | https://github.com/semyon422/rizu/blob/cf4603379dcab949d3510b8c31d1d3e421df6ec0/chart/format/sph/tests/Sph_test.lua (encdec_1) | 2026-11-09 | `3dd48c5ea4ac20ae2e3677157f9d32221649b3b17434228474bda726fe526908` | semyon422 | GPL-3.0 | Z85 sound keys incl. `##` |
