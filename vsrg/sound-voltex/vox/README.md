# SOUND VOLTEX arcade chart (`.vox`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: text

## Overview
`.vox` is the chart format of the Konami arcade game SOUND VOLTEX (SDVX), stored inside the game data (one `.vox` per song and difficulty, next to the `.2dx`/`.s3v` audio). It is **proprietary and undocumented by Konami**; the knowledge comes from community reverse engineering: zacharied's original notes, m0seng's rewrite covering v10/v12, and the whiteou7/vox2ksh writeup (v10/v12/v13; it says it was produced with Ghidra decompilation of `soundvoltex.dll` and that part of the analysis was LLM-assisted, so treat details as unverified). Charts are obtained from game data the user already owns; converters (vox2ksh, rmstZ) turn them into [`ksh`](../ksh/README.md). No chart files are included here.

## Container & encoding
Plain text. **UTF-8 or Shift-JIS** (which one is not predictable; Japanese comments break the wrong decoding); rmstZ tries CP932/CP936. Comments start with `//`, even mid-line. Every file starts with the 3-line banner `//====...`, `// SOUND VOLTEX OUTPUT TEXT FILE`, `//====...`. Sections are `#NAME` ... `#END` (extra stray closing tags occur and are ignorable). Fields are tab-separated ("tabsep") or comma(+tab)-separated ("commasep").

## Structure / metadata
| Section | Content |
| --- | --- |
| `#FORMAT VERSION` | one integer (observed 10, 12, 13) |
| `#BEAT RESOLUTION` (v12) | cells per quarter note, default 48 (so a 4/4 measure has 192 cells) |
| `#BEAT INFO` | time signatures: timing, top, bottom; always at a measure start; entries may overlap |
| `#BPM INFO` | timing, BPM (4 decimals), `4` or `4-` (`-` = pause) |
| `#BPM OPTION` (v13) | `ConstantScroll` 0/1, `RepresentativeBpm` |
| `#TILT MODE INFO` | timing, mode 0 normal / 1 bigger / 2 bigger+stay max |
| `#LYRIC INFO` | obsolete |
| `#END POSITION` | single timing of the official end (often past the last note) |
| `#TAB EFFECT INFO` | 5 lines of laser effects: 1 lowpass, 2 highpass (mix, cutoff lo/hi, resonance), 3 bitcrush (mix, rate factor) |
| `#FXBUTTON EFFECT INFO` | 12 pairs of lines of FX effects: ids 0 none, 1 Retrigger, 2 Gate, 3 Flange, 4 Tape Stop, 5 Side Chain, 6 Wobble, 7 Bit Crusher, 8 Echo/Retrigger Ex, 9 Pitch Shift, 10 Tape Stop Ex, 11 LPF, 12 HPF, 13 Pitch & Speed; per-id column formats (printf-style) in the vox2ksh `vox_format.md` |
| `#TAB PARAM ASSIGN INFO` | 24 rows tying lasers to effect parameters |
| `#REVERB EFFECT PARAM` | always empty |
| `#TRACK1` / `#TRACK8` | left / right laser |
| `#TRACK2` / `#TRACK7` | FX-L / FX-R |
| `#TRACK3`..`#TRACK6` | BT-A, BT-B, BT-C, BT-D |
| `#TRACK AUTO TAB` | applies FX hold effects to lasers |
| `#TRACK ORIGINAL L/R` (v12) | control nodes of curved lasers (safe to ignore) |
| `#SPCONTROLER` / `#LOCKED_SPCONTROLER` (v13) | camera/background/Live2D control (`CAM_RotX`, `CAM_Radi`, `Tilt`, `LaneY`, `BAROFF`, `BAR`, `Morphing2`, `ManualSpeed`, `SpecialN`...) |
| `#POSTEFFECT` | optional post-processing |
| `#SCRIPT_DEFINE`, `#SCRIPTED_TRACK1..8` | optional per-note scripts (`$targetStep`, `$offsetX`, `$offsetY`) |

## Timing model
Timing = `mmm,bb,cc`: measure (1-indexed), beat (1-indexed, counted in units of the **local time signature's denominator**, not quarter notes), cell (0-indexed). Cells per beat = (4 * BEAT RESOLUTION) / denominator (usually 192/den), e.g. 4/4: 48 per beat; 15/16: 12 per beat. No row has `bb` >= numerator or `cc` >= cells per beat (verified by the writeup over its corpus). Lengths (`C1` of tracks) are in cells. BPM changes may happen mid-measure.

## Notes
- BT tracks: C0 timing, C1 length in cells (0 = chip), C2 unknown (usually 2 for holds), C3 optional cells-per-chain.
- FX tracks: C1 length (0 = chip), C2: chip -> sample id (1-14: big snare (quiet), big clap, short clap, big snare, short snare, crash, kick+crash+downlifter, open hi-hat, kick+crash, snare+click, female "oh", male "hey", male "yeah", fireworks; 0 and 255 = none), hold -> index (2-based) into `#FXBUTTON EFFECT INFO`; C3 optional cells-per-chain.
- Laser tracks (C0..C9): timing; position (v10 integer 0-127, v12 decimal 0-1); node type (0 continue, 1 start, 2 end; two points on the same tick = slam); roll/swing type 0-7; laser effect (0 peak, 1-5 index into `#TAB EFFECT INFO`, 6 control source); range (1 normal, 2 wide); unused; curve type (v12: 0 linear, 2 cubic Hermite, 3 interpolated linear, 4 sine ease out, 5 sine ease in; 1 unknown); roll length (C8 up to v12, C9 in v13; unit 1/4 note, 1/10 for types 6/7); cells per chain.
- v13 shifts roll length to C9 and C8 becomes an unknown 0/1/2 flag.

## Audio & images
Not in the chart file; audio is in the game's `.2dx`/`.s3v` containers and referenced by folder (preview offsets are not stored; see vox2ksh notes). Backgrounds via `SpecialN EXBG`.

## Versions & variants
Observed format versions 10, 12, 13; the writeup's corpus is 8254 charts, ~148 of them format 13. Versions 9 and earlier: Unknown.

## Quirks & pitfalls
Mixed encodings; comments mid-line; beat column units; v13 column shift; lasers are pre-sampled curves (as fine as 1/64 measure), so converting to ksh needs thinning; `#END POSITION` is not the last note.

## Example
Illustrative, hand-built from the field tables above (not a real chart): `001,01,00<TAB>0<TAB>2` as a BT-A chip at measure 1 beat 1 cell 0 in `#TRACK3`.

## ROX support
Not read by ROX.

## Parsers & tools
vox2ksh (Python): https://github.com/whiteou7/vox2ksh · ksm2sdvx (writes VOX v13): https://github.com/Foahh/ksm2sdvx · VOXL4DD3R (KSH/KSON -> VOX v13): https://github.com/ooznon/VOXL4DD3R · rmstZ (reads/writes vox): https://lrfasd.github.io/rmstZ/ · sdvxeditor PR #3 (vox import): https://github.com/Kizuruki/sdvxeditor/pull/3

## Sources
https://github.com/whiteou7/vox2ksh (README, specs/vox_format.md, specs/notes.md) · https://lrfasd.github.io/rmstZ/WHATSNEW.html · https://github.com/Foahh/ksm2sdvx · https://github.com/ooznon/VOXL4DD3R
