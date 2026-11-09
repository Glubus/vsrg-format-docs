# Samples: K-Shoot MANIA JSON chart (`.kson`)

All files are UTF-8 without BOM, LF line endings (bytes unchanged from the source repositories). No audio or images are committed.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `Gram_ex.kson` | https://github.com/kshootmania/libkson/blob/41e6250f4f3e806430e686c3c49f83746fa1fc13/tests/assets/Gram_ex.kson | KSH-to-KSON conversion (by libkson) of "Gram" (Blast Smith), extended chart by 坂本龍馬; test asset `TestKsonIO.cpp` ("Gram[EX] detailed chart validation") | MIT (libkson `LICENSE`); see the doubt note in `../../ksh/samples/SOURCES.md` about the bundled song | A complete real chart in KSON: `meta` (`difficulty` 2, `level` 16, `disp_bpm` "191", Japanese `chart_author`), `beat.bpm` `[[0,191.0]]`, `scroll_speed`, `note.bt/fx/laser`, `audio.bgm`/`key_sound`, `audio.audio_effect.fx` (`def` with `retrigger`, `gate`, `sidechain`, `switch_audio`, `flanger`..., `long_event`, `param_change`), `camera.cam`/`camera.tilt`, `bg.legacy`, `editor` (`app_name`, `app_version`), `compat.ksh_version` "160". |
| `oracle.kson` | https://github.com/ooznon/VOXL4DD3R/blob/ff221d86f780aabd19f2f560d441c3f271a9a1a6/testdata/oracle.kson | ooznon (title "Oracle fixture", artist "Local test", chart_author "Converter test") | MIT (VOXL4DD3R `LICENSE`, Copyright (c) 2026 ooznon) | Small synthetic fixture: BPM change `[[0,120],[960,150.5]]`, time signature change `[[0,[4,4]],[2,[3,4]]]`, `stop`, `scroll_speed` with `[v, vf]` and curve points, chip and long BT/FX notes, laser sections on both knobs incl. slams (`[v, vf]`) and negative/over-range values (`[-0.6, 0.6]`), `camera.cam.body` (`zoom_top`, `zoom_bottom`, `center_split`, `rotation_deg`), `camera.cam.pattern.laser.slam_event` (`spin`, `half_spin`, `swing` with `scale`/`repeat`/`decay_order`), `camera.tilt`, `audio.audio_effect.fx.def` + `long_event`. Its `meta.difficulty` is the object `{"idx":2,"name":"exhaust"}` ... see "Deviations" below. Its VOX conversion is committed as `../../vox/samples/oracle.golden.vox`. |
| `curve-scroll.kson` | https://github.com/ooznon/VOXL4DD3R/blob/ff221d86f780aabd19f2f560d441c3f271a9a1a6/testdata/curve-scroll.kson | ooznon | MIT | Synthetic: `scroll_speed` with immediate-change pairs (`[960,[1.0,1.5]]`), laser points with curve control points (`[0,0.0,[0.2,0.8]]`), one long BT. VOX output: `../../vox/samples/curve-scroll.golden.vox`. |
| `speed-curve.kson` | https://github.com/ooznon/VOXL4DD3R/blob/ff221d86f780aabd19f2f560d441c3f271a9a1a6/testdata/speed-curve.kson | ooznon | MIT | Synthetic: `scroll_speed` with a curve (`[960,1.5,[0.2,0.8]]`) and no notes. |
| `effects.kson` | https://github.com/ooznon/VOXL4DD3R/blob/ff221d86f780aabd19f2f560d441c3f271a9a1a6/testdata/effects.kson | ooznon | MIT | Synthetic: audio-effect definitions (`retrigger`, `wobble` for FX; `high_pass_filter` for laser), a long FX note carrying an effect name as third array element and a laser section carrying `{"effect":"hp"}` as fourth element (see "Deviations"). |

### Deviations from the spec as read (kson_format.md 1.0.2) [observed in the samples]
- `oracle.kson`, `curve-scroll.kson`, `speed-curve.kson`, `effects.kson` write `meta.difficulty` as an object `{"idx": 2, "name": "exhaust"}`; the spec text read says `uint|string`.
- `effects.kson` has a 3-element `ButtonNote` (`[0, 480, "r"]`) and a 4-element `LaserSection` (`[0, [...], 1, {"effect":"hp"}]`); the spec states "The array size of `ButtonNote` MUST be 2" and `LaserSection` size 2 or 3. These files come from a converter's dialect (VOXL4DD3R), not from the KSM reference tools.

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
| --- | --- | --- | --- |
| `ksm2sdvx_minimal.kson` | https://raw.githubusercontent.com/Foahh/ksm2sdvx/50bf1d358ba41aafd4c217b4da1571c2a3c40c95/tests/fixtures/kson/minimal.kson | No licence file found in the repository (only `LICENSES/` of third-party components) | Smallest document (256 B): `meta` (`difficulty` 2) + `beat.bpm` only, pretty-printed with one array element per line. |
| `ksm2sdvx_notes.kson` | https://raw.githubusercontent.com/Foahh/ksm2sdvx/50bf1d358ba41aafd4c217b4da1571c2a3c40c95/tests/fixtures/kson/notes.kson | same | 1.6 KB: bare-uint chip notes next to `[y,length]` notes in `bt`/`fx`, a 2x-wide laser section (`w`=2), a laser point with curve control points, BPM change `[960,180]`, 3/4 measure change, one `spin` slam event. |
| `ksm2sdvx_camera.kson` | https://raw.githubusercontent.com/Foahh/ksm2sdvx/50bf1d358ba41aafd4c217b4da1571c2a3c40c95/tests/fixtures/kson/camera.kson | same | 1.2 KB: `camera.cam.body.zoom_top`/`zoom_bottom` graphs with `[v, vf]` immediate pairs and a curve point, `camera.tilt` mixing numbers and the names `"normal"`/`"bigger"` (inside a `[v, vf]` pair as well). |

More KSON files: any `.ksh` converted with `ksh2kson` (libkson `tool/ksh2kson.cpp`) or the kson-rs `ksh2kson` example; see the `Getting samples` section of the fiche.
