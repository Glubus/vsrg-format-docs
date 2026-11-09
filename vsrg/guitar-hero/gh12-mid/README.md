# Guitar Hero 1 / Guitar Hero 2 MIDI chart (`.mid`, Harmonix)
Kind: chart

Doc status: complete (gameplay tracks); venue/trigger tracks partial · ROX: no · Category: vsrg (5-lane note highway: notes travel down fixed lanes toward a strum line) · Encoding: binary (Standard MIDI File, format 1)

## Overview

Guitar Hero and Guitar Hero II (Harmonix) store each chart as a Standard MIDI File. Chart tracks use MIDI notes as the 5 lanes (Green, Red, Yellow, Blue, Orange), with one note range per difficulty in the same track. The format is the ancestor of the Rock Band layout (see [`../../clone-hero/mid`](../../clone-hero/mid/README.md)) and of the community `.mid` charts of Frets on Fire, Phase Shift and Clone Hero. Differences: star power and face-off phrases are per difficulty, text events use a GH-specific vocabulary, and each song carries band-animation and venue tracks. Reference: TheNathannator's `GuitarGame_ChartFormats` ("Guitar Hero 1 and 2" notes), compiled from fan reverse engineering; its practice-section list also covers Rock the 80s.

## Container & encoding

- Standard MIDI File: header chunk `MThd`, track chunks `MTrk`, big-endian numbers, variable-length delta times (see the MIDI specification and TheNathannator's `Technical-Details.md`).
- Resolution 480 ticks per quarter note ("all Harmonix GH games use a resolution of 480"). Fan-made GH2 customs may differ: 2 of the 6 committed customs use 480 and 4 use 960 ticks per quarter note [observed in samples/gh2-customs_allalone.mid, samples/gh2-customs_allday.mid].
- Track names use the Track Name meta event (`FF 03`).
- Text events are meta events (`FF 01`) with bracketed text like `[verse]`.

## Structure / metadata

### Tracks

| Game | Track name | Purpose |
|---|---|---|
| GH1 | `T1 GEMS` | Lead guitar chart (plus vocalist mouth-control notes) |
| GH1 | `ANIM` | Guitarist left-hand position |
| GH1 | `Triggers` | Unknown purpose (notes 60, 61 unknown) |
| GH2 | `PART GUITAR` | Lead guitar |
| GH2 | `PART GUITAR COOP` | Co-op guitar |
| GH2 | `PART RHYTHM` or `PART BASS` | Rhythm or bass guitar (mutually exclusive in one chart) |
| GH2 | `BAND_BASS`, `BAND_DRUM`, `BAND_SINGER`, `Triggers` | Venue/animation tracks |
| both | global events track | `[section ...]`, venue/crowd text events |

### Instrument notes (GH1 `T1 GEMS` and all GH2 instrument tracks)

Lanes (5): 1 Green, 2 Red, 3 Yellow, 4 Blue, 5 Orange.

| Difficulty | Green | Red | Yellow | Blue | Orange | Star Power | P1 Face-Off | P2 Face-Off |
|---|---|---|---|---|---|---|---|---|
| Easy | 60 | 61 | 62 | 63 | 64 | 67 | 69 | 70 |
| Medium | 72 | 73 | 74 | 75 | 76 | 79 | 81 | 82 |
| Hard | 84 | 85 | 86 | 87 | 88 | 91 | 93 | 94 |
| Expert | 96 | 97 | 98 | 99 | 100 | 103 | 105 | 106 |

Other notes: 110 = "Big note" marker (GH2: the crowd reacts negatively when these notes are missed; marked per note, not as a phrase). 108 = vocalist mouth open/close in GH1's `T1 GEMS` (note on = open, note off = closed; "there may be some other mechanism that controls this, but this is what the current sources say"). 40-59 = left-hand fretting position 1 (near the headstock) to 20 (GH2 instrument tracks; on GH1 in the `ANIM` track; note 59 / position 20 "might not actually be valid").

Note on/off pairs: length = off - on. Face-Off markers (`105/106` etc.) mark the sections played by one or both players in versus; Star Power phrases mark where star power can be earned. Both are marked per difficulty in GH1/2, "something which has not made it over to the standard .mid format" (the later Rock Band layout has a single marker, note 116 for star power).

### Text events

GH1 global events: `[verse]`, `[chorus]`, `[solo]`, `[end]` (song end), and per-band-member animation controls (`[gtr_on]`/`[gtr_off]`, `[solo_on]`/`[solo_off]`, `[wail_on]`/`[wail_off]`, `[bass_on]`/`[bass_off]`, `[drum_on]`/`[drum_off]`/`[drum_half]`/`[drum_double]`/`[drum_normal]`/`[drum_allbeat]`, `[sing_on]`/`[sing_off]`, `[keys_on]`/`[keys_off]`).

GH2 global events: `[music_start]`, `[verse]`, `[chorus]`, `[solo]`, `[end]`, crowd (`[crowd_lighters_fast|slow|off]`, `[crowd_half_tempo|normal_tempo|double_tempo]`), band (`[band_jump]`, `[sync_head_bang]`, `[sync_wag]`), practice sections `[section <name>]`, and `[lighting (<type>)]` (types: none `()`, `flare`, `blackout`, `chase`, `strobe`, `color1`, `color2`, `color3`, `sweep`; requires `[music_start]` plus `[verse]`/`[chorus]`/`[solo]` beforehand).

GH2 instrument-track text events: `[idle]`, `[play]`, `[solo_on]`, `[solo_off]`, `[wail_on]`, `[wail_off]`, `[half_tempo]`, `[normal_tempo]`, `[map <name>]` with hand maps `HandMap_Default`, `HandMap_NoChords`, `HandMap_DropD2`.

Venue tracks (GH2): `BAND_BASS` (note 36 strum animation trigger; absent when the co-op track is bass; events `[idle]`, `[play]`), `BAND_DRUM` (notes 36 kick, 37 crash; events `[idle]`, `[play]`, `[normal_tempo]`, `[half_time]`, `[double_time]`, `[allbeat]`), `BAND_SINGER` (note 108 mouth; events `[idle]`, `[play]`), `Triggers` (incomplete list: 52 venue-specific effect, 50/49/48 lighting keyframes, 26/25/24 hi-hat/snare/kick practice-mode assist samples).

Practice sections: names such as `chorus_1`, `bridge_a` map to display names ("Chorus 1"). The compiled list (GH2, GH2 demo, Rock the 80s; GH1 has no practice mode) is in the source's `Practice-Sections.md`; match both `[section <name>]` and `[prc_<name>]` forms.

## Timing model

SMF tempo map (set-tempo meta events, microseconds per quarter note) and time signature events in the first (conductor) track. Integrate tempo segments to convert ticks (480/quarter) to seconds. Note on/off and text events sit on those ticks. GH1/2 have no offset fields; the audio aligns with tick 0 [inference].

## Notes

- Default note type is a strum. A note becomes a HOPO (hammer-on/pull-off) automatically if it is close enough to the previous note, unless it is on the same lane as the previous note or is a chord. The threshold is 170 ticks in GH1.
- Sustains shorter than 160 ticks are cut to a normal note.
- Chord lengths are forced equal (the game ignores differing lengths in the file).
- Notes within 10 ticks of each other snap into one chord, at the start position of the earliest note.
- No open notes, no tap flag, no explicit HOPO flags (later formats add them, see the Clone Hero page).

## Audio & images

None in the SMF.

## Versions & variants

GH1: `T1 GEMS` + `ANIM` + `Triggers`; GH2 and Rock the 80s: `PART *` and `BAND_*` tracks. Rock Band uses a different track set and a single star power note (116), see [`../../clone-hero/mid`](../../clone-hero/mid/README.md) and [`../../rock-band/README.md`](../../rock-band/README.md). Community tools read the per-difficulty star power/face-off notes only partially.

## Quirks & pitfalls

- Star power/face-off markers differ per difficulty; a Rock Band-style reader takes only note 103/116.
- The 170-tick HOPO threshold is GH1-specific; other games use `resolution / 3 + 1`-style thresholds.
- Text events are bracketed and game-specific; ignore unknown ones.
- GH1 note 108 (vocalist mouth) on the guitar track is not a lane.

## Example

Illustrative, hand-built from the note table: an Expert chord of Green + Yellow at tick 480 lasting a quarter note, in `PART GUITAR` (MIDI note numbers 96 and 98):

```
delta 480  Note On  ch0 note 96 vel 100
delta 0    Note On  ch0 note 98 vel 100
delta 480  Note Off ch0 note 96
delta 0    Note Off ch0 note 98
```

## ROX support

Not read by ROX (Clone Hero is planned, not implemented).

## Parsers & tools

- Any SMF library; chart-aware readers: Clone Hero, YARG (https://github.com/YARC-Official/YARG), Phase Shift, FoFiX, Editor on Fire, Moonscraper (convert through `.chart`/`.mid`).
- Documentation: https://github.com/TheNathannator/GuitarGame_ChartFormats (CC0), site https://thenathannator.github.io/GuitarGame_ChartFormats/.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (`gh2-customs_*.mid` from the Milohax-archive "GH2 customs" collection; tracks `PART GUITAR`, `PART BASS`, `BAND BASS/DRUMS/SINGER`, `EVENTS`, `TRIGGERS`; synthetic CC0 `synthetic-gh1.mid` with `T1 GEMS`/`ANIM` and `synthetic-gh2.mid`, built from the https://github.com/TheNathannator/GuitarGame_ChartFormats GH1/2 docs). No real GH1 `T1 GEMS` file is public; the originals sit inside the commercial discs.

More: https://github.com/Milohax-archive/gh2-customs has ~190 more songs (`GH2CUSTOMSREPO/songs/<name>/<name>.mid`); its `config/songs.dta` is committed under [rock-band/dta](../../rock-band/dta/samples/SOURCES.md). Onyx can export GH2 customs (https://github.com/mtolly/onyx).

## Sources

- https://github.com/TheNathannator/GuitarGame_ChartFormats (commit `3d3640574821e1f7f0ec4be70627893aa88fdff6`): `docs/Implementation-Specific/Guitar-Hero-1-and-2/MIDI-Tracks/{Guitar,Global-Events,Venue,Practice-Sections}.md`, `docs/Chart-File-Formats/mid-format/Technical-Details.md`
