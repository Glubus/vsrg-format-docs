# Samples: K-Shoot MANIA chart (`.ksh`)

Charts only (no audio, jackets or backgrounds). The real charts below are UTF-8 with BOM and CRLF, bytes unchanged from the source repositories.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `Gram_lt.ksh`, `Gram_ch.ksh`, `Gram_ex.ksh`, `Gram_in.ksh` | https://github.com/kshootmania/libkson/tree/41e6250f4f3e806430e686c3c49f83746fa1fc13/tests/assets (`tests/assets/`) | Blast Smith (song); `effect=` 龍馬 / 坂本龍馬 | MIT (libkson); same files in https://github.com/Drewol/kson-rs commit 9880e2444aa85c30ea0e849354782ec715dee11a (`kson/src/tests/assets/`); see doubt note | one song, 4 difficulties (6/13/16/19), `ver=160`, `t=191`, footer `#define_fx`/`#define_filter`, `filtertype`, `zoom_top`, `tilt`, spins, `S<` swing |
| `cantabile.ksh` | https://github.com/123jimin/voltedit/tree/bfa48b04b49b4c5b2dd98435c3ad1887d3179c87/test | puddi ("All charts have been permitted by charters to be put in this repo", `test/README.md`) | MIT (voltedit) + author permission | long chart (668 bar lines, 485 KB), `ver=167`, 10 `t=`, 4 `beat=`, 346 `laserrange_*`, 253 `zoom_top`, 32 spins |
| `hawk.ksh` | same | hexagon | MIT + permission | "Nodding Hawk" infinite 18, `ver=160`: 28 `laserrange`, 3 spins, 3 `chokkakuse`, 96 `zoom_top`, 18 `tilt`, `fx-l=Flanger`/`BitCrusher;10`/`PitchShift;12`, `.mp3`, `o=310` |
| `howling.ksh` | same | hexagon | MIT + permission | "H.O.W.ling" infinite 18, `ver=160`: 145 `zoom_top`, 20 `tilt`, two simultaneous FX effects, 33 `beat=`, 16 `filtertype` |
| `juicy.ksh` | same | hexagon ("One Juicy Step", Makou) | MIT + permission | `ver=167`, 17 spins/slam spins (`@(`, `@)` up to 1032), beat changes, no FX effects |
| `konga.ksh` | same | hexagon | MIT + permission | "Konga Conga Kappa" infinite 19, `ver=167`: 92 `t=`, 61 `beat=` in 62 bar lines, long slam spin |
| `tenkuu.ksh` | same | hexagon (天空の華) | MIT + permission | extended 18, `ver=160`, `stop=192`, Japanese title (UTF-8) |
| `xeroize.ksh` | same | hexagon ("Xeroize") | MIT + permission | infinite 19, `ver=167`, `t=20400`, `t=17.391-26800` ranges ("over 20,000" per `test/README.md`), 41 `beat=`, 11 `t=` |
| `synthetic-legacy-sjis.ksh` | hand-written from `ksh_format.md` of https://github.com/kshootmania/ksm-chart-format (commit b984509ad6b43c208f8a3b4aff51d6a8664b896d) | repository maintainers | CC0 | `synthetic`. Shift_JIS (CP932) no BOM, CRLF, no `ver` (pre-1.60), `layer=arrow/1100/1` (legacy `/`), FX letters `S` Retrigger;8, `G` Gate;4, `:`/`-` lasers, 1/32 slams, `@(96`, `@>96`, `S<192`, `t=150`, 3/4, 12/16/8/32-line bars, `song.ogg` |
| `synthetic-modern-features.ksh` | hand-written from `ksh_format.md` of https://github.com/kshootmania/ksm-chart-format (commit b984509ad6b43c208f8a3b4aff51d6a8664b896d) | repository maintainers | CC0 | `synthetic`. UTF-8 BOM, LF, `ver=171` + `ver_compat=167`, `t=120-180`, `to=`, 2 files in `m=`, `o=-120`, `layer=snow;1100;3`, `fx-l`/`fx-r` (`Retrigger;8`, `Gate;16`, `Wobble;12`, `custom1`), `fx-l_se`, `laserrange_l=2x`, `laser_l_curve`, `tilt`, `zoom_*`, `center_split`, `scroll_speed`, `rotation_deg`, `stop`, `chokkakuse`, `filtertype` (`hpf1`, `lpf1`, `fx;bitc`), `pfiltergain`, 6/8, footer defines; hand-checked, not run in KSM |

Doubt (also in `/tmp/fsc-parts/doubts/ArcadePcSims.md`): the `Gram_*` charts are the sample song bundled with K-Shoot MANIA. The KSM readme says bundled songs "are the property of the content creators" (https://github.com/kshootmania/ksm-v2 `dist_scripts/assets_win/readme_en.txt`), while libkson (same maintainer) ships them in an MIT repository. Charts only are kept here on the strength of the repository licence.

More real fan charts are on Nautica and sdvx.org (see `Getting samples` in the README).

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

Downloaded with curl on 2026-11-09, committed byte for byte (charts only).

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `voxl4dd3r_poly.ksh` | https://raw.githubusercontent.com/ooznon/VOXL4DD3R/ff221d86f780aabd19f2f560d441c3f271a9a1a6/testdata/poly.ksh | 2026-11-09 | be0931f27fdccf4bddd6b07bd89ae4e6af347942648eaf7a38c423bc80cd4a2e | ooznon | MIT (repo); third-party fan chart | fan chart, ver=167, UTF-8 BOM, LF-only |
