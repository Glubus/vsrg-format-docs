# K-Shoot MANIA chart (`.ksh`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text

## Overview
`.ksh` is the text chart format of **K-Shoot MANIA** (KSM), the SOUND VOLTEX simulator by m4saka, and the format that Unnamed SDVX Clone (USC), voltedit and the SDVX fan-chart community (Nautica, sdvx.org) use. One `.ksh` file is one difficulty (Light / Challenge / Extended / Infinite) of one song; the folder normally also holds the audio (`.ogg`, optionally prerendered FX variants), jacket and background images. There is an official, CC0-licensed specification (kshootmania/ksm-chart-format, `ksh_format.md`); the newer JSON successor is [`kson`](../kson/README.md).

## Container & encoding
- Plain text, recommended **UTF-8 with BOM** (KSM detects the encoding from the BOM; without BOM it assumes ANSI). Charts made before editor v1.32 are ANSI (locale code page, e.g. Shift-JIS/CP932 or CP936). rmstZ tries CP932 then CP936 when reading.
- Line-oriented, CRLF usual. Empty lines are ignored.
- Five line types: option line `name=value`, chart line, bar line `--`, definition line `#define_<type> <name> <value>`, comment `//...`.
- File name: any `.ksh`; per-difficulty names such as `exh.ksh`, `inf.ksh`, `mxm.ksh`, `nov.ksh` by convention [inference; the spec does not define names].

## Structure / metadata
Layout: **header** (option lines before the first `--`), **body** (measures separated by `--`, with option lines allowed inside), **footer** (only `#define_*` lines after the last `--`).

- Option line: `<param-name>=<value>`; whitespace around `=` is significant; the value is everything after the first `=`. Many values are `;`-separated lists. `title` must be the first line (no comments before it).

### Header options (defaults in brackets)
| Option | Meaning |
| --- | --- |
| `title` [""], `title_translit` (v2), `title_img` | song title, transliteration, image |
| `artist`, `artist_translit` (v2), `artist_img` | artist |
| `effect` | **chart author** (yes, the author field is named `effect`) |
| `jacket` , `illustrator` | jacket image file (or presets `nowprinting1/2/3`) and its author |
| `difficulty` [`light`] | `light`, `challenge`, `extended`, `infinite` (unknown = infinite) |
| `level` [1] | 1-20 |
| `t` [120] | BPM; a range string like `180-220` when the chart has tempo changes (first tempo placed just after the first bar line); float otherwise (0.001-65535) |
| `to` [0] | standard BPM for hi-speed (0 = auto) |
| `beat` [`4/4`] | time signature `num/den` (also valid after a bar line) |
| `m` | song file(s), `;`-separated: 1 file (effects applied by the software), 2 files (`song.ogg;song_f.ogg`: second used while long FX notes are active), 4 files (`song;song_f;song_p;song_fp`: default, FX, laser, FX+laser) |
| `mvol` [100] | song volume %, (x0.6 if `ver` is missing) |
| `o` [0] | song offset in ms; larger = note judgment later; may be negative |
| `bg` [`desert`] | background: 13 presets (desert, grass, night, deepsea, sky, sunset, ocean, flame, cyber, space, mars, cloudy, fantasy) or 1-2 files (2nd used when gauge >= 70%) |
| `layer` [`arrow`] | animation layer (arrow, smoke, wave, techno, snow, sakura, hidden or file); extra values `;speed_ms;rotation_flags` (`/` separator before ver 166) |
| `po`, `plength` [0] | preview offset / length in ms |
| `total` [0] | gauge total (0 = auto; >=100) |
| `chokkakuvol` [50], `chokkakuautovol` [1] | laser slam volume %, auto-scale with slam width |
| `filtertype` [`peak`] | laser audio effect: `peak`, `hpf1`, `lpf1`, `bitc`, `fx`, `fx;bitc`, or user-defined (`#define_filter`) |
| `pfiltergain` [50], `pfilterdelay` [40] | peaking filter gain, delay ms |
| `v`, `vo` | video file, video offset |
| `ver`, `ver_compat` | format version (see Versions) |
| `information` | text shown in song select |

### Body options (in measures; take effect at the next chart line)
`t` (tempo), `beat` (time signature, applies to the next measure if not right after the bar line), `chokkakuvol`, `chokkakuse` (`up|down|swing|mute` or audio file), `pfiltergain`, `scroll_speed` (v2, linear graph; two successive lines make an immediate change), `rotation_deg` (v2), `stop` (pause length, 192 per measure), `tilt` (`normal|bigger|biggest|keep_normal|keep_bigger|keep_biggest|zero`, deprecated `big`/`keep`, or a float), `zoom_top`, `zoom_bottom`, `zoom_side`, `center_split`, `*_curve` variants of all graph options (`"a;b"` floats 0..1; v2), `laserrange_l`, `laserrange_r` (`2x` = wide laser; put just before the laser starts), `laser_l_curve`, `laser_r_curve`, `fx-l`, `fx-r` (audio effect of the next long FX: `Retrigger;n`, `Gate;n`, `Flanger`, `PitchShift;pitch`, `BitCrusher;n`, `Phaser`, `Wobble;n`, `TapeStop;speed`, `Echo;n;feedback`, `SideChain`, or a user-defined name), `fx-l_se`, `fx-r_se` (`name;volume` chip-FX keysound; presets `clap`, `clap_punchy`, `clap_impact`, `snare`, `snare_lo`), `filtertype`, legacy `fx-l_param1`, deprecated `chiprate`/`longrate`/`laserrate`.

### Footer
`#define_fx <name> <params>` and `#define_filter <name> <params>`, e.g. `#define_fx LoFl type=Flanger;delay=80samples;depth=60samples`, `#define_filter TSTP type=TapeStop;trigger=off>on;speed=20%` (examples from the spec).

## Timing model
- Measures are separated by a bar line `--`; a chart needs at least one, and a bar line after the last chart line.
- A measure contains any number N of chart lines; the lines divide the measure **evenly** (line i is at i/N of the measure). The number of lines is chosen per measure by the editor (the sdvx.org guide: determined by the finest note division used in that measure: 4 lines = quarter notes, 8 = eighths, 32 = 32nds...).
- Measure length from `beat=num/den` (4/4 default); the measure spans num beats of 1/den notes [inference from the field name; the spec only states "time signature"].
- `t=` sets the BPM; in the body it applies from its chart line (the first tempo is placed right after the first `--`). Negative BPMs are read as stops by rmstZ (a community convention); the official stop is `stop=<ticks>` with 192 ticks per measure and has priority over `scroll_speed`.
- Time of a position: t = sum of the durations of earlier measures (each 4*(num/den) quarter beats at the active BPM) + fraction within the measure; the audio is shifted by `o` ms.
- Lane spin / swing lengths use the same 192-per-measure unit.
- `scroll_speed` is a hi-speed multiplier graph; `stop` is equivalent to scroll_speed 0 for a duration.

## Notes
Chart line: `<bt x4>|<fx x2>|<laser x2>[<spin>]`

Examples from the spec: `0000|00|--` (empty), `0110|22|--` (2 chip BT + 2 chip FX), `0220|11|--` (2 long BT + 2 long FX), `0000|00|0o` (2 lasers at default positions), `0000|00|::` (laser continuation), `0000|00|o0` (opposite positions).

- BT (4 chars, left to right A, B, C, D): `0` empty, `1` chip, `2` long. A `2` after a `2` in the same lane continues the long note (the note lasts while consecutive lines keep the `2`).
- FX (2 chars): `0` empty, `2` chip, `1` (or any other character) long, continuing while the next lines keep a non-`0`/`2` char. **BT and FX use opposite digits** (historical).
  - Legacy (< v1.60) long FX characters encode the audio effect: `S` Retrigger;8, `V` Retrigger;12, `T` Retrigger;16, `W` Retrigger;24, `U` Retrigger;32, `G` Gate;4, `H` Gate;8, `K` Gate;12, `I` Gate;16, `L` Gate;24, `J` Gate;32, `F` Flanger, `P` PitchShift, `B` BitCrusher, `Q` Phaser, `X` Wobble;12, `A` TapeStop, `D` SideChain.
- Lasers (2 chars: left blue, right red): `-` none, `:` linear connection (continuation between two laser positions), otherwise a position among 51 steps from left to right: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno` (index 0 = far left, 50 = far right, so x = index/50).
  - A laser segment lasts as long as consecutive lines carry laser characters; `-` ends it.
  - Segments of **1/32 or shorter are slams** (instant moves); ordinary 1/32 lasers cannot be written.
  - `laserrange_l/r=2x` makes the segment wide (2x range).
- Lane spin (optional suffix after the laser chars): `@(` spin left, `@)` spin right, `@<` half spin left, `@>` half spin right, `S<` / `S>` swing left/right, then the length in ticks (192 per measure), e.g. `@(192`; swing: `S<192;250;3;2` = length; scale [250]; repetitions [3]; decay 0 none/1 linear/2 squared [2].
- Simultaneity: any combination per line; BT/FX/laser per line independent.
- Keysounds: only chip-FX `fx-l_se`/`fx-r_se` samples; no per-BT keysounds.

## Audio & images
`m` (audio, up to 4 variants), `jacket`, `bg`, `layer`, `v` (video) + `vo`, `title_img`, `artist_img`; preview via `po`/`plength`. Files resolved relative to the chart folder; presets are names without extension.

## Versions & variants
`ver` history from the spec: missing (legacy: mvol x0.6, alphabet FX effects, layer separator `/`, BPM may exceed 65535), `120`, `120b`, `121`, `130` (t <= 65535), `160` (FX effects via `fx-l`/`fx-r`), `166` (layer separator `;`), `167` (top-lane zoom as 3D rotation; zoom no longer clamped to +-300), `171` (max laser-slam and keysound polyphony 1), `200` (charts converted from kson). `ver_compat` overrides behaviour selection. **KSH v2** features (marked "Not supported in KSM v1.xx" in the spec): `title_translit`, `artist_translit`, `chokkakuse` with file name, `scroll_speed`, `rotation_deg` and all `*_curve` options. USC / Nautica charts follow the same text format with USC-specific tolerance (`;` comments tolerated).

## Quirks & pitfalls
- The author is `effect=`, not a field named author.
- `title=` must be the very first line; the `t=` header may be a range string.
- BT/FX digit semantics are inverted; legacy FX letters.
- Laser slam threshold (1/32) depends on the *measure's* line count: a 192-line measure makes tiny lines; compute duration in note values, not lines.
- Measures have different line counts; `beat` changes apply from the next measure when not right after `--`.
- `ver` missing changes volume and tilt behaviour.
- Not-recommended `;` comments exist in the wild.
- A bar line after the last chart line is required.
- `chokkakuse`/`laserrange_*` must precede the object they affect.
- BOM vs ANSI encoding detection.

## Example
Illustrative, hand-built from the rules above (not a real chart); the line forms come from the spec examples:

```
title=Example
artist=Nobody
effect=me
difficulty=infinite
level=15
t=140
beat=4/4
m=song.ogg
o=0
--
0000|00|--
1000|00|0-
0100|00|:-
0010|00|o-
0001|00|--
--
0200|20|--
0200|20|--
0000|00|--
0000|00|--
--
```

## ROX support
**Lasers are not supported for now**: ROX has no laser model and Prism plays the buttons only; the lasers are read, dropped and counted (`KshReport`).

Read by ROX since Prism's addition of `rox::formats::ksh` (decode only): `KshDecoder` (`decode`, `decode_with_title`, `decode_with_report` giving a `KshReport`, `decode_file`; `DetectedFormat::Ksh` by the extension `.ksh`, which is also the Korn shell's, so `looks_like_ksh` / `is_ksh_chart_file` tell a chart from a script: first line `title=`, option or `//` lines up to the first `--`). ONE chart per file on **6 columns**: BT A-D (columns 0-3, chip `1` = tap, run of `2` = hold) then FX-L and FX-R (columns 4-5, chip `2` = tap, run of any other character = hold; the legacy effect letters and `fx-l`/`fx-r` are dropped and counted). **Lasers are dropped and counted** (laser notes, slams, lane spins, half spins, swings, `laserrange_*`): they are analog, not a column. Times: lines divide a measure evenly (no grid rounding), `beat=n/d` is `4n/d` quarter notes and applies from the next measure when it is not right after a bar line, a body `t=` applies from the next chart line (a range or a negative BPM is ignored and counted), `o` is added to every time (as `.sm` bakes `#OFFSET`), and `stop` moves NO time (it is `scroll_speed` 0: a scroll effect, counted). `m=` gives the audio (the first of the `;` list, the others counted). UTF-8 (BOM or not), else Shift_JIS, else GBK. Hand-written tests only; checked locally against four real charts and a `.kson` conversion of one of them (deleted afterwards). Not read: `.kson`, `.vox`, camera, scroll and audio-effect events.

## Parsers & tools
- libkson (C++20, KSH/KSON): https://github.com/kshootmania/libkson
- kson (Rust crate, KSH import/export): https://lib.rs/crates/kson ; kson-rs https://github.com/Drewol/kson-rs
- kshoot (JS/TS KSH/KSON): https://www.npmjs.com/package/kshoot
- Unnamed SDVX Clone (C++/Lua game): https://github.com/Drewol/unnamed-sdvx-clone
- sdvx-emulator (Lua/LOeVE): https://github.com/nucular/sdvx-emulator
- voltedit (editor): https://github.com/123jimin/voltedit
- vox2ksh (Python): https://github.com/whiteou7/vox2ksh
- rmstZ (web converter; reads/writes ksh, vox): https://lrfasd.github.io/rmstZ/

## Sources
- https://github.com/kshootmania/ksm-chart-format (`ksh_format.md`, CC0)
- https://kson.dev/docs/format-spec/ksh_format/
- https://www.sdvx.org/en/charting/kshfile
- https://github.com/kshootmania/libkson
- https://lrfasd.github.io/rmstZ/WHATSNEW.html (rmstZ ksh notes)
- https://github.com/whiteou7/vox2ksh
