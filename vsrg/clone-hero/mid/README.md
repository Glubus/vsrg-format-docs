# Rock Band / Clone Hero MIDI chart (`notes.mid`)
Kind: chart

Doc status: partial · ROX: decode only · Category: vsrg · Encoding: binary

## Overview
Harmonix designed Guitar Hero 1/2 and Rock Band to store charts as Standard MIDI Files; early fan games (FoFiX / Frets on Fire, Phase Shift) adopted that layout, and Rock Band Network (user-authored RB DLC) made it the most documented chart format. Modern `.mid` charts follow the Rock Band layout plus community extensions from Phase Shift (SysEx modifiers, Real Drums, dance track) and Clone Hero (note-based tap/open markers, 6-fret). Charts are read by Clone Hero, YARG, Phase Shift, FoFiX, Rock Band 3 (with its own tooling) and written by REAPER/Onyx/EoF/Moonscraper. This page documents the instrument tracks that map to lanes (5-fret, 6-fret, drums, dance), and lists the others; the full per-track tables are in TheNathannator's docs (see Sources). The Pro Guitar/Pro Keys/vocals tracks are summarized only.

## Packaged in

- Packaged in [`sng`](../sng/).
- Packaged in [`yargsong`](../../yarg/yargsong/).

## Container & encoding
- Standard MIDI File format type 1 (multi-track), **ticks per quarter note** resolution (480 is common [inference]; the docs only state "ticks-per-quarter"). Format 0/2 and SMPTE division are not supported.
- Big-endian numbers; variable-length quantities up to 4 bytes; chunks `MThd` (length 6) and `MTrk`; running status (resets after SysEx/meta events). Data bytes above 0x7F occur in the wild in SysEx (0xFF).
- Folder layout: `notes.mid` + `song.ini` (metadata) + audio files. No metadata or audio file names inside the `.mid`.
- Tracks are identified by the **track name meta event** (first event, FF 03). Unknown tracks are ignored. Instrument tracks are `PART <NAME>`.
- Notable violations: running status not reset after SysEx/meta events (breaks NAudio-like parsers); 0xFF bytes inside SysEx.

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
Delta times in ticks; tempo from FF 51 events (microseconds per quarter note) in the first track; time signatures from FF 58. `seconds = sum(dTicks_i / TPQN * usPerQuarter_i / 1e6)`. Chart delay is `song.ini` `delay` (ms, not recommended). Hand positions etc. use the same ticks.

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
Not referenced from the `.mid`; the game looks for reserved file names (`song`, `guitar`, `rhythm`, `bass`, `keys`, `drums`, `drums_1..4`, `vocals`, `crowd`, `preview`) in the folder and artwork/video via `song.ini`.

## Versions & variants
- Guitar Hero 1/2 MIDI (`T1 GEMS`, `ANIM`, face-off phrases, different notes/markers; GH1/2 star power on note 103) vs Rock Band layout (what modern charts use).
- Rock Band Network / C3 (RB3 authoring conventions).
- Phase Shift extensions (SysEx, Real Drums, dance), Clone Hero extensions (tap/open note markers 104, GHL tracks), Editor on Fire (EoF) additions.
- Real Rock Band files inside CON/PKG archives are the same MIDI plus a `songs.dta` database ([dta](../../rock-band/dta/README.md)).

## Quirks & pitfalls
Open note via note 95/83/... is disabled unless `[ENHANCED_OPENS]`; 4-lane cymbal/tom default is inverted vs `.chart`; tempo map must be track 0; velocity 41-50 affects Hard for trills/rolls; HOPO threshold formula differs from `.chart`; note-off/zero-velocity note-on equivalence; SysEx modifiers have inconsistent support; chord snapping within 10 ticks.

## Example
Not a real file (binary). Illustrative layout from the tables above, hand-built: a `PART GUITAR` track with Note On 96 (Expert Green) at tick 0, Note Off at tick 240 = an Expert green sustain of 240 ticks; Note On 96 + Note On 97 on the same tick = a Green+Red chord.

## ROX support
Read by ROX since Prism's addition of `rox::formats::clone_hero::MidDecoder` (decode only), ONLY for a file NAMED `notes.mid` (any case; `.mid` is the extension of every MIDI file, so any other `.mid` is not a chart, `auto_decode*` refuse it). Own Standard MIDI File reader (`smf.rs`: format 0 and 1, ticks per quarter note; format 2 and SMPTE are errors; running status not reset by SysEx/meta events, which charts in the wild commit; hard limits on size, chunks, events and notes). The FIRST track gives the tempo map and the time signatures (in a format 0 file the single track is both: an extension, `YARG.Core` skips instruments there); tracks `PART GUITAR`, `PART GUITAR COOP`, `PART BASS`, `PART RHYTHM`, `PART KEYS` are 5-column variants at Expert (96-100), Hard (84-88), Medium (72-76), Easy (60-64), ordered by instrument then difficulty (`variants`, `decode_variant`, `decode_with_ini`, `decode_with_audio_plan`, `auto_decode*` with the `song.ini` of the folder; the `.sng` may hold a `notes.mid`, preferred to `notes.chart`). Drums, vocals, harmonies, GHL, `PART REAL_*`, `PART DANCE` and `T1 GEMS` are listed in `ChartReport::unsupported_tracks`, not read. Forced HOPO/strum (101/102, 89/90, 77/78, 65/66), the tap marker 104 and the tap SysEx are counted and ignored; open notes (the keys 95/83/71/59 after `[ENHANCED_OPENS]`, and notes inside an open SysEx phrase) have no column and are dropped and counted; star power, solos, versus, BRE, tremolo/trill markers, HOPO threshold and chord snapping are not used. A note longer than 0 ticks is a hold unless shorter than a third of the resolution (`resolution / 3`, integer division, as `YARG.Core`; a `song.ini` `sustain_cutoff_threshold` replaces it, 0 read as 1); holds stop at the next note of their fret. `song.ini` `delay` shifts the times (no `Offset` in a `.mid`); title, artist, charter and `diff_*` come from the `song.ini` only. No real `.mid` is used by the tests (community charts have no licence): every file is built byte by byte. Decisions: `rhythm-open-exchange/src/formats/clone_hero/mod.rs`.

## Parsers & tools
YARG.Core (C#): https://github.com/YARC-Official/YARG.Core · Onyx (Haskell): https://github.com/mtolly/onyx · Moonscraper (C#, reads/writes MIDI): https://github.com/FireFox2000000/Moonscraper-Chart-Editor · REAPER + RBN tooling; Editor on Fire; FoFiX (Python): https://github.com/fofix/fofix · Phase Shift (closed).

## Getting samples
- Committed in [`samples/`](samples/SOURCES.md): 17 real files and 1 synthetic. Real: nine small Clone Hero charts by TheGreatNi (`thegreatni_*_notes.mid`, 6-12 KB up to 138 KB, CC BY 4.0, from https://archive.org/details/YoungDublinersAshleyFalls.7z), YARG.Core `yarg-core_test.mid` (11 tracks incl. GHL and vocals) and `drawntotheflame.mid` (18 tracks incl. Pro Keys E/M/H/X, HARM1-3, VENUE, BEAT), two Onyx DIY-folder transcriptions (`onyx_btbam-*`, Pro Keys/harmonies; the larger is ~1.3 MB, 960 tpqn), and three `notes.mid` extracted from Chorus Encore `.sng` downloads (a Harmonix RB chart, a 6-fret GHL layout, a FreeStyleGames GHL chart; containers and audio are not stored). The synthetic `synthetic-notes.mid` covers tap SysEx, `[ENHANCED_OPENS]`, tom markers.
- Not obtained: Pro Guitar/Pro Bass tracks.
- More: Chorus Encore (`https://api.enchor.us/search`, `https://files.enchor.us/<md5>.sng`), Onyx (https://github.com/mtolly/onyx; many community transcriptions with mixed licences), RhythmVerse, extracted Rock Band CON/PKG folders (https://wiki.yarg.in/wiki/Songs).

## Sources
- https://thenathannator.github.io/GuitarGame_ChartFormats/ (mid-format: Format-Overview, Technical-Details, Tracks/*; Implementation-Specific/Rock-Band, Guitar-Hero-1-and-2, Phase-Shift)
- https://github.com/TheNathannator/GuitarGame_ChartFormats
- https://wiki.yarg.in/wiki/Help:Charting (references RBN/C3 docs)
