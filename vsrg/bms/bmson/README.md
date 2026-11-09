# bmson (`.bmson`)
Kind: chart

Doc status: complete · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: json

JSON successor to BMS. Specification v1.0.0-beta (2015-12-26), from the bmson-spec source (`doc/index.rst`) at https://github.com/bemusic/bmson-spec.

## Overview

- wosderge started bmson as a BMS alternative easy for developers, artists and chart authors (Wikipedia). Bemuse and Raindrop implemented 0.2x/0.26; their developers then wrote the 1.0.0 spec. Official site: https://bmson.nekokan.dyndns.info/. Players: Bemuse (since 2015-08), Raindrop, beatoraja ("BMSON 0.2.1 / 1.0.0 (.bmson)").
- Sound-channel based: a sound channel is one audio file and its notes are slice points the player cuts between consecutive note positions. No `#WAVxx` limit (1295). Timing is in pulses, with no measures.
- A community fork (DJKero, "bmson-spec-fork", Version 2.0.0, 2023-10-24; https://github.com/djkero/bmson-spec-fork) restructures the objects (`song_info`, `chart_info`, `chart_data`, `note_events`, `judge_multiplier`, `life_multiplier`, `ln_type_hint`, `ln_judge_hint`, `ln_life_hint`, DJ.NEXT fields `judge_deltas`, `life_deltas`, per-note `vol`/`pan`/`up`). Beatoraja and Bemuse do not use it; this page covers 1.0.0.

## Container & encoding

- Plain JSON (UTF-8), one chart per file. It sits in a song folder next to the audio and image files it references (relative paths; `\` or `/` both allowed, must be normalised; absolute paths, `..` and NUL must be rejected by the player).
- Recommended sound: WAV, OGG Vorbis, MP4 AAC (`.m4a`); MP3 discouraged (encoder delay up to ~20 ms). BGA: PNG, WebM, 1280x720 preferred (1920x1080 accepted).

## Structure / metadata

Types use Web IDL (`?` = nullable/optional). Spec 1.0.0:

```
dictionary Bmson {
  DOMString      version;         // "1.0.0" (SemVer). Missing = legacy (reject or treat as 0.21)
  BmsonInfo      info;
  BarLine[]?     lines;           // bar lines in pulses
  BpmEvent[]?    bpm_events;
  StopEvent[]?   stop_events;
  SoundChannel[] sound_channels;
  BGA            bga;
}
dictionary BmsonInfo {
  DOMString title; DOMString subtitle = ""; DOMString artist;
  DOMString[]? subartists = [];     // ["key:value"], key = music|vocal|chart|image|movie|other
  DOMString genre;
  DOMString mode_hint = "beat-7k";  // "beat-7k","popn-5k","generic-nkeys",...
  DOMString chart_name;             // e.g. "HYPER"
  unsigned long level;              // >= 0
  double init_bpm;                  // REQUIRED (fatal error if absent)
  double judge_rank = 100;          // relative judge width (percent-like)
  double total = 100;               // relative gauge gain
  DOMString? back_image; DOMString? eyecatch_image; DOMString? banner_image;
  DOMString? preview_music;
  unsigned long resolution = 240;   // pulses per quarter note
}
dictionary BarLine   { unsigned long y; }
dictionary SoundChannel { DOMString name; Note[] notes; }
dictionary Note      { any x; unsigned long y; unsigned long l; boolean c; }
dictionary BpmEvent  { unsigned long y; double bpm; }
dictionary StopEvent { unsigned long y; unsigned long duration; }   // pulses
dictionary BGA       { BGAHeader[] bga_header; BGAEvent[] bga_events; BGAEvent[] layer_events; BGAEvent[] poor_events; }
dictionary BGAHeader { unsigned long id; DOMString name; }
dictionary BGAEvent  { unsigned long y; unsigned long id; }
```

The prose of the spec also defines `info.title_image` (image shown before the song starts, equivalent to `#BACKBMP` in OADX+ skins).

| Field | Meaning / rules |
| --- | --- |
| `version` | `1.0.0`. Compare with SemVer. `null` -> show an error. |
| `info.title`, `subtitle`, `artist`, `genre` | Display text. Do not split title on delimiters. Subtitle may contain `\n`. |
| `info.subartists` | Array of `"key:value"`; keys `music`, `vocal`, `chart`, `image`, `movie`, `other` (default `other`); trim spaces. |
| `info.mode_hint` | Layout/game mode (see Notes). Default `beat-7k`. A new mode must use a new `mode_hint`, not a new `version`. |
| `info.chart_name` | e.g. `BEGINNER`, `NORMAL`, `HYPER`, `ANOTHER`, `7keys Beginner`. Default `""`. |
| `info.level` | Unsigned integer; for `beat` modes on a 1-12 scale recommended. |
| `info.init_bpm` | Starting tempo; required. |
| `info.judge_rank` | Default 100. > 100 wider window, < 100 narrower. Non-normative interpretation: percentage of the player's default window (20 ms PERFECT at 100). Windows: LR2 `#RANK 2` Perfect GREAT 18 ms, GREAT 40, GOOD 100, BAD 200; Bemuse 20/50/100/200. |
| `info.total` | Default 100, must be >= 0 (negative: absolute value); relative gauge gain. IIDX reference: `7.605*n/(0.01*n+6.5)` percent for n notes. |
| `info.back_image`, `eyecatch_image`, `title_image`, `banner_image`, `preview_music` | Paths. Banner ratio 15:4 (normally 600x160). If `preview_music` is absent, the player may build one from `sound_channels`. |
| `info.resolution` | Pulses per quarter note of 4/4. Default 240 (lowest common multiple of 48 and 5: covers 80th, 120th, 240th notes). `0`/null -> 240, negative -> absolute value. |

## Timing model

- Time units: `t` (seconds), `b` (beats, quarter note), `y` (pulses). Events are positioned by `y`.
- No measures, no time signature. `lines` (bar lines) are visual only: the list of `y` where a bar line is drawn. `lines` absent/null -> a bar line every 4 quarter notes (960 pulses at resolution 240). Empty array -> no bar line (the "100% minimoo-G" effect). The first line at `y = 0` may be omitted. Mapping from BMS measure lengths (spec example): `#00102:0.75` and `#00302:1.25` give lines at 960, 1680, 2640, 3840.
- `info.init_bpm` is the tempo at `y = 0`. `bpm_events`: at `y` the tempo becomes `bpm`; several at the same `y` -> the last wins.
- `stop_events`: at `y` the music pauses for `duration` pulses (converted with the BPM in effect); several at the same `y` add up.
- Processing order inside one pulse: notes and BGA events, then BPM events, then stop events. A BPM change and a stop at the same pulse: BPM first, then the pause uses the new BPM. A BGM note at a stop pulse plays before the pause; a playable note at a stop pulse must be hit at the start of the pause (`t = 1.0` in the spec's example, not when the music resumes).
- Position to time: `seconds += dy / resolution * 60 / bpm`, plus `duration / resolution * 60 / bpm` at stops. Spec example at 60 BPM, resolution 240: y = 120 -> 0.5 s, y = 240 with a 240-pulse stop -> 1.0 s start of pause (ambiguous up to 2.0 s), y = 241 -> 481/240 s.
- There is no scroll-speed event in 1.0.0; beatoraja adds `scroll_events` (see below).

## Notes

- Notes are grouped by `sound_channels[i]` (one audio file each). `Note`:
  - `x`: lane. `0` or `null` -> not playable (BGM note). `1`, `2`, ... -> playable lane according to `mode_hint`.
  - `y`: pulse where the note is activated.
  - `l`: `0` = tap, `> 0` = long note from `y` to `y + l` (pulses).
  - `c`: continuation flag. `true` = continue the audio (do not restart), `false` = restart the file from its beginning at this note.
- Slicing: gather the distinct pulses of a channel's notes, convert to seconds; the audio is restarted whenever a note without `c` is hit; slices go between consecutive pulses; each note plays the slice starting at its pulse. Example from the spec: `vox.wav` with notes at y = 240 (c false), 360, 360, 720 (c false), 720, 840, 840, 1200, 1680 at 120 BPM gives 6 slices (0-0.25 s, 0.25-1, 1-1.25, 1.25-2, 2-3, 3-end). Multiple notes may share a slice. If a slice is assigned to both a playable and a BGM note, the BGM note is discarded. If a pulse mixes `c: true` and `c: false` notes, treat it as `c: false`. Polyphony of a slice is 1 (same slice triggered twice does not get louder); different slices of one channel can overlap.
- Layered notes: notes of different channels at the same (x, y) fuse into one note that plays every slice. Length mismatch is an error (warning allowed).
- Mode hints (spec appendix), x values:

  | mode_hint | x = lane |
  | --- | --- |
  | `beat-5k` | P1: x = 1-5 keys, x = 8 turntable (SC) |
  | `beat-7k` | P1: x = 1-7 keys, x = 8 turntable (SC) |
  | `beat-10k` | P1: 1-5 keys + SC at x = 8; P2: 1-5 keys + SC at x = 16 (spec table columns 9-13 / 16) |
  | `beat-14k` | P1: 1-7 + SC at x = 8; P2: 1-7 at x = 9-15 + SC at x = 16 |
  | `popn-5k` | 1-5 |
  | `popn-9k` | 1-9 |
  | `generic-nkeys` | n keys, left to right |

  `SC` = scratch (turntable) column.
- No mine or invisible note in 1.0.0. beatoraja extensions (from its wiki): in `info`: `ln_type` (1 LN / 2 CN / 3 HCN); per `Note`: `t` (long-note type, overrides `ln_type`), `up` (true on the end position of a LN = the sound of the LN end); root: `scroll_events: [{y, rate}]` (scroll multiplier, negative = reverse, since beatoraja 0.7.6), `mine_channels: [{name, notes:[{x,y,damage}]}]` (landmine: gauge loses `damage` if the key is held at judgment time, plays the sound on explosion), `key_channels: [{name, notes:[{x,y}]}]` (invisible notes: not drawn or judged, play the sound on key press).

## Audio & images

- `sound_channels[].name`: file name; extension optional (player tries `.wav`, `.ogg`, `.m4a`...; if the given extension is not found/playable, drop it and retry). Subdirectories allowed; protect against absolute/parent/NUL paths.
- `bga.bga_header[]` = table (`id`, `name`) of pictures/videos; `bga_events`, `layer_events` (drawn over BGA; black is not transparent, unlike BMS channel 07, so use alpha formats), `poor_events` (on miss) place them by pulse. A BMS-to-bmson converter must turn black pixels of layer images into alpha. Duplicate `id`s: warn, the later one wins.

## Versions & variants

- 0.21 (legacy, camelCase: `soundChannel`, `judgeRank`, `initBPM`, `bgaHeader`, `bgaNotes`, `layerNotes`, `poorNotes`, `ID`, `bpmNotes`, `stopEvents`, `BarLine.k`, other time units, absolute `total`). Players supported 0.2.1 and 0.26 before 1.0.
- 1.0.0 from 0.21: snake_case; `bpmNotes -> bpm_events`, `stopEvents -> stop_events`, `BarLine.k` removed, `EventNote` split into `BpmEvent`/`StopEvent`, time unit = pulse, relative `total`; added `version`, `subtitle`, `subartists`, `mode_hint`, `chart_name`, `back_image`, `eyecatch_image`, `banner_image`, `preview_music`, `resolution`.
- Fork 2.0.0 (2023) and beatoraja extensions: see Overview and Notes.

## Quirks & pitfalls

- Files without `version` must be rejected or parsed as 0.21.
- `x` is typed `any`: numbers, `null` or missing; `null`/0 is BGM.
- `init_bpm` missing is fatal; `lines` missing differs from `lines: []`.
- With resolution 240, BMS data on a 1/192 grid needs 192 -> 240 rescaling (most games use 48 pulses per quarter; 240 = lcm(48, 5)).
- Slicing needs the audio length; the last slice runs to the end of the file.
- Stop and BPM order must follow the spec; "stop at note pulse" is unusual.
- A BGM (x = 0) and a playable note at one pulse of a channel: BGM dropped.

## Example

Hand-built from the spec rules (illustrative; field names from the spec, values invented):

```json
{
  "version": "1.0.0",
  "info": {
    "title": "Example", "artist": "Nobody", "genre": "Test",
    "mode_hint": "beat-7k", "chart_name": "NORMAL", "level": 3,
    "init_bpm": 120.0, "resolution": 240
  },
  "lines": [ {"y": 960}, {"y": 1920} ],
  "bpm_events": [ {"y": 1920, "bpm": 150.0} ],
  "stop_events": [ {"y": 960, "duration": 240} ],
  "sound_channels": [
    { "name": "kick.wav", "notes": [ {"x": 1, "y": 0, "l": 0, "c": false}, {"x": 8, "y": 480, "l": 240, "c": false} ] },
    { "name": "bgm.ogg",  "notes": [ {"x": 0, "y": 0, "l": 0, "c": false} ] }
  ],
  "bga": { "bga_header": [], "bga_events": [], "layer_events": [], "poor_events": [] }
}
```

Tap on key 1 at pulse 0, a 240-pulse long note on the turntable (x = 8) at pulse 480, BGM at pulse 0, bar lines every 960 pulses, a one-beat stop at pulse 960, BPM 150 at pulse 1920.

## ROX support

Decode only (`rox::formats::bms::bmson`, `BmsonDecoder`; `auto_encode` refuses it). Source `rhythm-open-exchange/src/formats/bms/bmson.rs`, tests `bmson_tests.rs`, chart `assets/bms/example.bmson` (also [`samples/synthetic-features.bmson`](samples/synthetic-features.bmson)).

- Accepts `version` 1.x (missing version or another major is refused); `info.init_bpm` required and positive. Resolution default 240, 0 is 240, negative is absolute.
- Time: `y / resolution` beats; `bpm_events` (last of a pulse wins, non-positive ignored); `stop_events` (summed per pulse, a playable note on a stop sits at the start of the pause). `lines` and `bga` ignored.
- `mode_hint` (default and unknown = `beat-7k`, like beatoraja): `beat-5k`/`beat-7k` keys `x` = 1..N, scratch 8; `beat-10k`/`beat-14k` P1 keys 1..N and scratch 8, P2 keys 9..8+N and scratch 16; `popn-5k`/`popn-9k` 5/9 columns; `generic-Nkeys` N columns; `keyboard-24k` (26 columns) and `keyboard-24k-double` (52) from beatoraja's `Mode`. Column order as BMS: `[scratch] keys`, double `[scratch1] P1 keys | P2 keys [scratch2]`, scratch only when used. Notes outside the layout are dropped.
- Notes: `x` 0, null or missing = background; `l` > 0 = hold; negative `y` dropped; layered notes (same `x`, `y`, other channel) keep the first channel; a note inside a hold or at the same time and column is dropped.
- Audio: each playable note's channel `name` goes to the hitsound table (`\` becomes `/`; absolute names, drive letters and `..` refused). With exactly ONE background note whose channel holds nothing else, that file is `metadata.audio_file` and the time origin. Otherwise `audio_file` is empty and Prism refuses the chart as "audio missing". A background note at a playable note's pulse in its channel is dropped.
- Metadata: `title`, `artist`, `genre`, `level`, difficulty name from `chart_name` else `subtitle` else `Normal`, creator from a `chart:` sub-artist, background from `back_image` else `eyecatch_image`.
- `decode_with_audio_plan` slices every channel as beatoraja does: a pulse restarts the file at 0 when any of its notes has `c` false; a slice lasts to the next pulse if that continues, else to the file end; stops ignored. The spec's example table keeps a growing offset at restart pulses; its text and beatoraja restart at 0. Prism mixes the plan into one Opus track when there is no single background sound.
- Not handled: beatoraja `mine_channels`, `key_channels`, `scroll_events`, `ln_type`, note `t`/`up`, `c`, BGA, `preview_music`, the 2.0.0 fork, legacy 0.2x.

## Parsers & tools

- Bemuse (TypeScript/JS): https://github.com/bemusic/bemuse ; spec repo https://github.com/bemusic/bmson-spec
- Raindrop (C++): https://github.com/zardoru/raindrop
- beatoraja (Java): https://github.com/exch-bms2/beatoraja
- bms-rs (Rust): https://github.com/MikuroXina/bms-rs (BMS; bmson conversion is out of this repo's research)
- Editors/converters: see the "how_to_bmson" and "bmson Creation Notes" links of the spec.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). The Bemuse music server lists charts in `https://bemuse.ninja/music/index.json`; a chart is at `https://bemuse.ninja/music/<song path>/<file>` (URL-encode `[` `]`). `[flicknote]onlylove_remix` is its only bmson song. `bms2bmson-python` (MIT, https://github.com/bemusicscript/bms2bmson-python) and `bms-rs` (`src/bmson/bms_to_bmson.rs`) convert `.bms` to bmson. The `bemusic/bmson-spec` repo has no sample file.

## Sources

- bmson spec 1.0.0-beta: https://bmson-spec.readthedocs.io/en/master/doc/index.html (raw: https://github.com/bemusic/bmson-spec/raw/master/doc/index.rst)
- Spec fork 2.0.0: https://raw.githubusercontent.com/djkero/bmson-spec-fork/master/doc/index.rst
- beatoraja wiki: https://github.com/exch-bms2/beatoraja/wiki/楽曲製作者向け資料
- Wikipedia "Be-Music Source" (bmson section): https://en.wikipedia.org/wiki/Be-Music_Source
- Bemuse bmson support article: https://qiita.com/dtinth/items/a2d644c608b3d1cf41ff (search snippet only)
