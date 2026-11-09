# Rock Band / Clone Hero MIDI chart (`notes.mid`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: binary

## Overview
Standard MIDI chart layout of Guitar Hero 1/2 and Rock Band, adopted by FoFiX / Frets on Fire and Phase Shift. Modern `.mid` charts follow the Rock Band layout plus Phase Shift extensions (SysEx modifiers, Real Drums, dance track) and Clone Hero extensions (note-based tap/open markers, 6-fret). Read by Clone Hero, YARG, Phase Shift, FoFiX, Rock Band 3; written by REAPER/Onyx/EoF/Moonscraper. This page covers the lane-mapped tracks (5-fret, 6-fret, drums, dance); the full per-track tables are in TheNathannator's docs (Sources). Pro Guitar/Pro Keys/vocals are summarized only.

## Packaged in
- `.sng` (Clone Hero / YARG single-file package: masked container with the song folder plus a metadata key/value table).
- `.yargsong` (YARG single-file package from the YARC Launcher; internal layout Unknown).

## Container & encoding
- Standard MIDI File format type 1, ticks-per-quarter resolution (480 common [inference]). Format 0/2 and SMPTE division are unsupported.
- Big-endian numbers; variable-length quantities up to 4 bytes; chunks `MThd` (length 6) and `MTrk`; running status. Charts in the wild violate the spec: running status is not reset after SysEx/meta events (breaks NAudio-like parsers) and SysEx contains data bytes above 0x7F (0xFF).
- Folder layout: `notes.mid` + `song.ini` (metadata) + audio files. The `.mid` names no metadata or audio.
- Tracks are identified by the track name meta event (first event, FF 03); unknown tracks are ignored. Instrument tracks are `PART <NAME>`.

## Structure / metadata
Tracks (names exact):
| Track name | Content |
| --- | --- |
| first track (tempo map) | tempo (meta FF 51) and time signature (meta FF 58) events; type 1 files use the first track for these |
| `EVENTS` | global text events: `[section <name>]` / `[prc_<name>]` (practice sections), `[end]`, `[coda]` (starts Big Rock Ending) |
| `BEAT` | note 14 weak beat, 13 strong beat, 12 measure beat |
| `PART GUITAR`, `PART GUITAR COOP`, `PART BASS`, `PART RHYTHM`, `PART KEYS`, `T1 GEMS` (GH1 lead) | 5-fret parts |
| `PART GUITAR GHL`, `PART BASS GHL`, `PART RHYTHM GHL`, `PART GUITAR COOP GHL`, `PART KEYS GHL` | 6-fret (GHL) |
| `PART DRUMS` (4-lane, 4-lane Pro and 5-lane), `PART DRUM` (FoFiX alias), `PART DRUMS_2X` (RBN 2x kick), `PART REAL_DRUMS_PS` (Phase Shift Real Drums) | drums |
| `PART DANCE` | Phase Shift / Editor on Fire dance track |
| `PART VOCALS`, `HARM1/2/3` (`PART HARM1..3`) | vocals / harmonies |
| `PART REAL_GUITAR`, `PART REAL_GUITAR_22`, `PART REAL_BASS`, `PART REAL_BASS_22`, `PART REAL_GUITAR_BONUS` | Pro Guitar/Bass (17 / 22 fret) |
| `PART REAL_KEYS_X/H/M/E` | Pro Keys per difficulty |
| `VENUE`, `ANIM` (GH1), others | venue/animation data, ignorable for gameplay |

`song.ini` carries title/artist and options that change parsing (`pro_drums`, `five_lane_drums`, `hopo_frequency`, `sustain_cutoff_threshold`, `multiplier_note`/`star_power_note`, `sysex_*` flags for Phase Shift): see [ini](../ini/README.md).

## Timing model
Delta ticks; tempo from FF 51 (microseconds per quarter note) in the first track, time signatures from FF 58. `seconds = sum(dTicks_i / TPQN * usPerQuarter_i / 1e6)`. Chart delay is `song.ini` `delay` (ms, not recommended).

## Notes
Difficulties are octaves in one track. Common ranges (MIDI note numbers): Expert 96-107, Hard 84-95, Medium 72-83, Easy 60-71; notes 108-127 (and some below the ranges) hold markers/animation.

### 5-fret (`PART GUITAR` etc.)
| MIDI note | Expert | Hard | Medium | Easy |
| --- | --- | --- | --- | --- |
| open (needs `[ENHANCED_OPENS]` event on the track; otherwise use the SysEx open modifier) | 95 | 83 | 71 | 59 |
| Green (1st) | 96 | 84 | 72 | 60 |
| Red (2nd) | 97 | 85 | 73 | 61 |
| Yellow (3rd) | 98 | 86 | 74 | 62 |
| Blue (4th) | 99 | 87 | 75 | 63 |
| Orange (5th) | 100 | 88 | 76 | 64 |
| Force HOPO | 101 | 89 | 77 | 65 |
| Force strum | 102 | 90 | 78 | 66 |

Markers (all difficulties unless noted): 103 solo (and GH1/2 star power if no note 116 exists), 104 tap-note marker (newer, not supported everywhere), 105 / 106 player 1 / 2 versus phrase, 116 star power, 120-124 Big Rock Ending markers 5..1, 126 tremolo lane, 127 trill lane (these apply to Expert, and to Hard when velocity is 41-50). Notes are Note On / Note Off pairs; the length is the gap. Notes are strums by default and become HOPOs when within `(resolution / 3) + 1` ticks (floored) of the previous different-lane, non-chord note (configurable with `hopo_frequency`, `hopofreq`, `eighthnote_hopo`). **Sustains shorter than a 1/12 step are cut to normal notes** (`sustain_cutoff_threshold`). Notes within 10 ticks are snapped into a chord in GH1/2/RB (use the earliest position and the shortest length).
SysEx (Phase Shift) modifiers: `F0 <len> 50 53 00 <type=00> <difficulty> <modifier> <value> F7`: payload `'P' 'S' 0 type difficulty modifier value`; difficulty 0 easy..3 expert, 0xFF all (tap only); modifier 0x01 open note (5/6-fret), 0x04 tap note; value 1 start, 0 end. Tap phrases include their end tick; open markers do not.
Rock Band additions: left-hand position notes 40-59 (animation), 2P/versus phrases, `[idle]`/`[play]` animation text events.

### 6-fret GHL
Expert: 94 open, 95 White 1 (4th lane), 96 White 2 (5th), 97 White 3 (6th), 98 Black 1 (1st), 99 Black 2 (2nd), 100 Black 3 (3rd), 101 force HOPO, 102 force strum; markers 103 solo, 104 tap, 116 star power. Other difficulties follow the same layout 12 notes lower (Hard: open 82, white 83-85, black 86-88, force 89/90).

### Drums (`PART DRUMS`)
Expert: 95 Expert+ kick (2x), 96 kick, 97 red, 98 yellow, 99 blue, 100 4-lane green / 5-lane orange, 101 5-lane green. Hard 84 kick, 85-89 lanes; Medium 72 kick, 73-77; Easy 60 kick, 61-65. Markers: 103 solo, 105/106 versus phrases, 109 flam, 110 / 111 / 112 yellow / blue / green **tom** markers (4-lane notes are cymbals by default in `.mid`, the reverse of `.chart`), 116 star power/overdrive, 120-124 fill / Big Rock Ending markers, 126 single-lane roll, 127 double-lane roll (Expert; Hard when velocity 41-50). Velocity 127 = accent, 1 = ghost, enabled by `[ENABLE_CHART_DYNAMICS]`. Text events `[mix <diff> drums<config><flag>]` set the stem layout (diff 0-3; config 0-5; flags `d`, `dnoflip`, `e`...). Track type detection: `pro_drums`/`five_lane_drums` tags, else tom markers => Pro, green 5-lane note or sustains => 5-lane.

### Dance (`PART DANCE`, Phase Shift)
Four lanes per difficulty: Beginner 48-51, Easy 60-63, Medium 72-75, Hard 84-87, Challenge 96-99 (left, down, up, right in order); 116 star power, 103 solo. MIDI channel: 0 normal, 1 mine, 2 lift, 3 roll. Implemented only in Phase Shift and Editor on Fire; underspecified.

### Others
Vocals (pitch notes 36-84, percussion 96/97, phrase markers 105/106, star power 116), Pro Guitar (strings per lane, fret in velocity, channel-based modifiers), Pro Keys (notes 48-72 + range shifts): see the source docs.

## Audio & images
Not referenced from the `.mid`: the game looks for reserved names (`song`, `guitar`, `rhythm`, `bass`, `keys`, `drums`, `drums_1..4`, `vocals`, `crowd`, `preview`) in the folder; artwork/video via `song.ini`.

## Versions & variants
- GH1/2 MIDI (`T1 GEMS`, `ANIM`, face-off phrases, star power on note 103) vs the Rock Band layout.
- Rock Band Network / C3 (RB3 authoring conventions); Phase Shift (SysEx, Real Drums, dance); Clone Hero (tap/open markers 104, GHL tracks); Editor on Fire.
- Real Rock Band files in CON/PKG archives are the same MIDI plus a `songs.dta` ([dta](../../rock-band/dta/README.md)).

## Quirks & pitfalls
Open note (95/83/...) is disabled without `[ENHANCED_OPENS]`; 4-lane cymbal/tom default is inverted vs `.chart`; tempo map must be track 0; velocity 41-50 affects Hard trills/rolls; HOPO threshold formula differs from `.chart`; zero-velocity Note On equals Note Off; SysEx modifier support is inconsistent; chord snapping within 10 ticks.

## Example
Binary; hand-built from the tables above: in a `PART GUITAR` track, Note On 96 (Expert Green) at tick 0 and Note Off at tick 240 = a 240-tick Expert green sustain; Note On 96 + 97 on one tick = Green+Red chord.

## ROX support
Read since Prism's addition of `rox::formats::clone_hero::MidDecoder` (decode only), only for a file named `notes.mid` (any case; other `.mid` files are not charts, `auto_decode*` refuse them). Own SMF reader (`smf.rs`): format 0 and 1; format 2 and SMPTE are errors; tolerates running status not reset by SysEx/meta; hard limits on size, chunks, events, notes. The first track is the tempo map and time signatures (a format 0 file's single track is both: an extension, `YARG.Core` skips instruments there).

- Variants: `PART GUITAR`, `PART GUITAR COOP`, `PART BASS`, `PART RHYTHM`, `PART KEYS` at Expert (96-100), Hard (84-88), Medium (72-76), Easy (60-64), ordered by instrument then difficulty (`variants`, `decode_variant`, `decode_with_ini`, `decode_with_audio_plan`, `auto_decode*` with the folder's `song.ini`; a `.sng` `notes.mid` is preferred to `notes.chart`).
- Not read, listed in `ChartReport::unsupported_tracks`: drums, vocals, harmonies, GHL, `PART REAL_*`, `PART DANCE`, `T1 GEMS`.
- Counted and ignored: forced HOPO/strum (101/102, 89/90, 77/78, 65/66), tap marker 104, tap SysEx. Open notes (keys 95/83/71/59 after `[ENHANCED_OPENS]`, notes inside an open SysEx phrase) have no column: dropped and counted. Not used: star power, solos, versus, BRE, tremolo/trill, HOPO threshold, chord snapping.
- A note longer than 0 ticks is a hold unless shorter than `resolution / 3` (integer division, as `YARG.Core`; `song.ini` `sustain_cutoff_threshold` replaces it, 0 read as 1); holds stop at the next note of their fret.
- `song.ini` `delay` shifts the times (a `.mid` has no `Offset`); title, artist, charter and `diff_*` come only from `song.ini`.
- No real `.mid` is used by the tests (community charts have no licence): every test file is built byte by byte. Decisions: `rhythm-open-exchange/src/formats/clone_hero/mod.rs`.

## Parsers & tools
YARG.Core (C#): https://github.com/YARC-Official/YARG.Core · Onyx (Haskell): https://github.com/mtolly/onyx · Moonscraper (C#, reads/writes MIDI): https://github.com/FireFox2000000/Moonscraper-Chart-Editor · REAPER + RBN tooling; Editor on Fire; FoFiX (Python): https://github.com/fofix/fofix · Phase Shift (closed).

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Not obtained: Pro Guitar/Pro Bass tracks. More: Chorus Encore (`https://api.enchor.us/search`, `https://files.enchor.us/<md5>.sng`), Onyx (https://github.com/mtolly/onyx; community transcriptions, mixed licences), RhythmVerse, extracted Rock Band CON/PKG folders (https://wiki.yarg.in/wiki/Songs).

## Sources
- https://thenathannator.github.io/GuitarGame_ChartFormats/ (mid-format: Format-Overview, Technical-Details, Tracks/*; Implementation-Specific/Rock-Band, Guitar-Hero-1-and-2, Phase-Shift)
- https://github.com/TheNathannator/GuitarGame_ChartFormats
- https://wiki.yarg.in/wiki/Help:Charting (references RBN/C3 docs)
