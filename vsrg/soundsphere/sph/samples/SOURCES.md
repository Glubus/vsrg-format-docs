# Samples: SPH chart
All files come from https://github.com/semyon422/rizu at commit `cf4603379dcab949d3510b8c31d1d3e421df6ec0` (licence: GNU GPL v3, `LICENSE` at the repo root, read). Author: semyon422 and rizu contributors. Test files are the Lua long-string literals of the repository tests, extracted byte for byte (Lua drops the newline right after `[[`; the trailing newline before `]]` is kept).
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rizu-sea-chart_1.sph` | `sea/chart/samples/chart_1.sph` | semyon422 | GPL-3.0 | Real sample file shipped in the repo (loaded by `sea/chart/samples/Samples.lua`): metadata block (title, artist, name, creator, audio, preview, input 4key), `=<s>` absolute-time anchors and `+n/d` beat fractions, 4-column jumptrill ("Jumptrill 180"). |
| `rizu-test-basic.sph` | `chart/format/sph/EncodeDecode_test.lua`, `test.basic` | semyon422 | GPL-3.0 | `# sounds` section, `:` keysound lists and `.` volumes, `x` velocity (1, 3 values), `e` expand, `#n/d` measure marker, `^` same-time line, hold notes (`2`/`3`), `-` empty lines, `//` comment, `=` anchors. Round-trip tested by the repo (encode(decode(s)) == s). |
| `rizu-test-visuals.sph` | same file, `test.visuals` | semyon422 | GPL-3.0 | Named visual layers `v1`/`v2`/`v3` attached to stacked (`^`) lines. |
| `rizu-test-close_point_in.sph`, `rizu-test-close_point_out.sph` | same file, `test.close_point` (`s_in`, `s_out`) | semyon422 | GPL-3.0 | Input and expected normalised output of the encoder (close visual points). |
| `rizu-test-close_point_2_layers_in.sph`, `rizu-test-close_point_2_layers_out.sph` | same file, `test.close_point_2_layers` | semyon422 | GPL-3.0 | Same with two visual layers (`v2`, `v3`), negative expand values (`e-2`). |
| `rizu-test-sph-sounds_z85.sph` | `chart/format/sph/tests/Sph_test.lua` | semyon422 | GPL-3.0 | Z85 sound keys including the maximal key `##` (`## sound##.ogg`, note line `:01##`). |
