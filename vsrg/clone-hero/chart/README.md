# Clone Hero / Moonscraper chart (`.chart`)
Kind: chart

Doc status: complete · ROX: decode only · Category: vsrg · Encoding: text

## Overview
`.chart` is a text format created for **Feedback Editor** (Turkeyman's GH1 tool), later used for Guitar Hero 3 customs via GHTCP, then adopted by **Moonscraper Chart Editor** (FireFox2000000) and **Clone Hero**, where it is the most common custom-chart format next to `.mid`. One `.chart` holds all instruments and difficulties of a song as separate sections; the song folder also has `song.ini` and audio. Sources: FireFox's `.chart` specification and TheNathannator's GuitarGame_ChartFormats (CC0).

## Packaged in

- Packaged in [`sng`](../sng/).
- Packaged in [`yargsong`](../../yarg/yargsong/).

## Container & encoding
- Text, INI-like: sections in square brackets with `{ }` bodies, line based. The character encoding is not specified in the docs consulted.
- File names: `notes.chart` or a custom name; some charts ship several files whose names end with `[Y]`/`[F]` (has forced notes) or `[N]` (no forced notes), also lowercase or in parentheses. Prefer `notes.chart`, then `[Y]`/`[F]`, then the rest.
- Sections can appear in any order (at least instrument tracks); unknown sections are ignored; a missing section equals an empty one.
- Real files have no comments (the docs use `//` only to annotate examples). Values with spaces are quoted; there is no escape syntax, and quotes do occur inside values in the wild: strip only the outermost pair.

## Structure / metadata
Sections: `[Song]`, `[SyncTrack]`, `[Events]`, then `[<Difficulty><Instrument>]`.
Syntax: named entries `<Key> = <Value[]>` or track events `<Tick> = <TypeCode> <Values...>`. Value types: number, decimal (period), string (quoted), bare string, boolean, file path (quoted; relative or absolute; `None` if absent).
Track event type codes: `A` tempo anchor, `B` tempo change, `E` text event, `H` (legacy) GH1 hand position, `N` note, `S` special phrase, `TS` time signature.

### `[Song]`
| Key | Meaning |
| --- | --- |
| `Name`, `Artist`, `Album`, `Genre`, `Year` (string, typically `", 2002"`), `Charter` | metadata |
| `Resolution` | **required**: ticks per quarter note |
| `Difficulty` | number |
| `Length` | seconds (metadata only) |
| `Offset` | audio start time in seconds; a higher value makes the audio start sooner |
| `PreviewStart`, `PreviewEnd` | seconds |
| `MusicStream`, `GuitarStream`, `RhythmStream`, `BassStream`, `KeysStream`, `DrumStream`, `Drum2Stream`, `Drum3Stream`, `Drum4Stream`, `VocalStream`, `CrowdStream` | audio files |
| Legacy GHTCP/Feedback ("dB") keys: `ArtistText`, `Singer`, `Bassist`, `Boss`, `Player2` (`Bass`/`Rhythm`), `CountOff`, `GuitarVolume`/`GuitarVol`, `BandVolume`/`BandVol`, `HoPo` (HOPO threshold = step-size denominator / 4: 1/4 step = 1.00, 1/8 = 2.00, 1/2 = 0.50), `Fretboard`, `MediaType`, `MusicURL`, `PreviewURL` | ignorable |

`song.ini` metadata has priority over `[Song]` (see [ini](../ini/README.md)); `.chart` metadata is often not filled in.

### `[SyncTrack]`
- `<tick> = TS <numerator> [<denominator exponent>]`: denominator = 2^exponent, default exponent 2 (x/4). E.g. `768 = TS 7 4` = 7/16, `1104 = TS 3 3` = 3/8. A TS at tick 0 sets the start (4/4 if absent).
- `<tick> = B <tempo>`: tempo in thousandths of a BPM (`150325` = 150.325 BPM). A `B` at tick 0 sets the start (120 BPM if absent).
- `<tick> = A <microseconds>`: tempo anchor tying the tempo marker to an audio time; editor-only, ignore when playing.

### `[Events]`
`<tick> = E "<text>"` global events: `section <name>` or `prc_<name>` (practice/summary sections; `_` may replace the space), `end` (end of song); may be bracketed. 5-fret only: `<tick> = H <HandPos 0-19> <length>` (legacy GH1/2 hand animation positions).

### Instrument sections `[<Difficulty><Instrument>]`
Difficulties: `Expert`, `Hard`, `Medium`, `Easy`. Events: `N <type> <length>` (notes and modifiers; a modifier applies to all notes on its tick), `S <type> <length>` (special phrases; they do not apply to the tick at `position + length` unless stated, except zero-length), `E <text>` (local event; treat everything after `E` as one parameter, spaces allowed). Keep events in increasing tick order. Type numbers are grouped in blocks of 32: 0-31 standard, 32-63 Guitar Hero, 64-95 Rock Band.

| Section name suffix | Instrument |
| --- | --- |
| `Single` | lead guitar (5-fret) |
| `DoubleGuitar` / `DoubleBass` / `DoubleRhythm` | co-op guitar / bass / rhythm |
| `Keyboard` | 5-lane keys |
| `SingleBass` | legacy bass track (GH3/GHTCP) |
| `Drums` | drums (4-lane, 4-lane Pro and 5-lane share the track) |
| `GHLGuitar`, `GHLBass`, `GHLRhythm`, `GHLCoop`, `GHLKeys` | Guitar Hero Live 6-fret |
| `EnhancedGuitar`, `CoopLead`, `CoopBass`, `10KeyGuitar`, `DoubleDrums`, `Vocals` | legacy Feedback tracks, edited like 5-fret, never implemented elsewhere |

Clone Hero also defines a lyrics track (see the lyrics page of the GuitarGame_ChartFormats docs; not reproduced here).

## Timing model
- Position in ticks; `Resolution` ticks per quarter note. `seconds = (60 / bpm) * (dTicks / Resolution) + seconds_at_that_tempo_start`, accumulated tempo by tempo from tick 0 (`bpm = B / 1000`).
- Time signatures do not change the tick-to-time conversion, only measure boundaries.
- `Offset` (seconds) shifts the audio relative to the chart; `song.ini` `delay` (ms) does the same (not recommended).
- No stops, warps or scroll-velocity changes.

## Notes
### 5-fret (`Single`, `DoubleGuitar`, `DoubleBass`, `DoubleRhythm`, `Keyboard`)
| `N` type | Meaning |
| --- | --- |
| 0, 1, 2, 3, 4 | Green, Red, Yellow, Blue, Orange (frets 1-5) |
| 7 | Open note |
| 5 | modifier: strum/HOPO flip ("force") |
| 6 | modifier: tap (overrides force) |

Length 0 = tap, > 0 = sustain. A chord is several `N` events on one tick (their lengths may differ: extended sustains / disjoint chords). Notes are strums by default and become HOPOs automatically when within `(65/192) * Resolution` ticks (rounded down: 192 -> 65, 480 -> 162) of the previous note, unless same lane or chord. Sustains are not cut off when short (unlike `.mid`).
Special phrases (`S`): 0 / 1 = GH1/2 face-off phrase player 1 / 2, 2 = star power, legacy GHTCP: 3 battle star power, 4 / 5 = battle player 1 / 2 phrases. The 5-fret doc's own example uses `S 64 768` (Rock Band block). Local events: `solo`, `soloend` (notes on the `soloend` tick are inside the solo).

### 6-fret GHL
Types: 0 White 1 (4th fret), 1 White 2 (5th), 2 White 3 (6th), 3 Black 1 (1st), 4 Black 2 (2nd), 8 Black 3 (3rd), 7 open, 5 force, 6 tap; `S 2` star power. Deprecated early local events: `ghl_6`, `ghl_6_forced`.

### Drums
`N` types: 0 kick, 1 red, 2 yellow, 3 blue, 4 (4-lane green / 5-lane orange), 5 (5-lane green), 32 Expert+ (2x) kick. Accent modifiers 34-38 (red, yellow, blue, 4th lane, 5-lane green); ghost modifiers 40-44 (same order); cymbal modifiers 66 yellow, 67 blue, 68 green (4-lane notes are toms by default in `.chart`). Special phrases: 2 star power, 64 activation/fill phrase (its end tick is included), 65 single-lane roll, 66 double-lane roll. The drum track type is not marked in the file: use `pro_drums` / `five_lane_drums` in `song.ini`, else heuristics (cymbal markers = 4-lane Pro; 5-lane green note or sustained notes = 5-lane; else 4-lane). Local events: `solo`, `soloend`, `mix_<difficulty>_drums<config><flags>` (difficulty 0 easy ... 3 expert).

## Audio & images
`[Song]` stream tags and/or reserved file names (`song`, `guitar`, `rhythm`, `bass`, `keys`, `drums`, `drums_1..4`, `vocals`, `vocals_1/2`, `crowd`, `preview`; `.opus`, `.ogg`, `.mp3`; `.wav`). Check reserved names first, then the tags. Images/video are declared in `song.ini`.

## Versions & variants
Feedback Editor `.chart` (GH1/2 era); an unadopted `.chart-v2`; GHTCP/GH3 additions (tap/open); Moonscraper extensions; Clone Hero additions (lyrics, GHL tracks, drum parity with `.mid`); DJ Hero custom proposal (turntable track in `.chart`). Miscellaneous pages in the docs describe BMS conversions and old Moonscraper MIDI conversions.

## Quirks & pitfalls
- Quoted values may contain quotes.
- `Offset` sign: positive = audio sooner.
- 5 and 6 are modifiers, not notes; the open note is 7.
- Modifiers at one tick affect all notes on it.
- Several `.chart` variants in one folder.
- Resolution varies; tempos are in thousandths of a BPM.
- Drum track type is ambiguous.

## Example
Hand-assembled from field rules and the doc's examples (illustrative; the `[Song]` values mirror the doc's example):

```
[Song]
{
  Name = "Example Song"
  Resolution = 192
  Offset = 0.56
  MusicStream = "Example Song.ogg"
}
[SyncTrack]
{
  0 = TS 4
  0 = B 120000
}
[ExpertSingle]
{
  768 = N 0 0
  864 = N 1 0
  864 = N 5 0
  960 = N 2 96
  1056 = E solo
  1152 = N 7 0
  1248 = E soloend
}
```

## ROX support
Read by ROX since Prism's addition of `rox::formats::clone_hero` (decode only). `ChartDecoder` gives one 5-column chart per 5-lane track that has a note on the five frets (`Single`, `DoubleGuitar`, `DoubleBass`, `DoubleRhythm`, `Keyboard` × Expert/Hard/Medium/Easy; `variants`, `decode_variant`, `decode_with_ini`, `decode_with_audio_plan`; `auto_decode*` read the `song.ini` of the folder): frets 0-4 are the columns, sustains are holds (no cutoff unless the `song.ini` gives `sustain_cutoff_threshold`), `B`/`TS` make the tempo map, `[Song]` `Offset` and `song.ini` `delay` (same sign, the `song.ini` wins) move every time so that times count from the start of the audio, and the stems (reserved names and the `[Song]` stream tags) are the audio plan. Forced (5) and tap (6) flags and open notes (7, dropped: five columns) are counted, not kept; star power, solos, events, lyrics, drums, GHL tracks and `SingleBass` are not read. Decisions: `src/formats/clone_hero/mod.rs` in the ROX copy.

## Parsers & tools
- Moonscraper Chart Editor (C#): https://github.com/FireFox2000000/Moonscraper-Chart-Editor
- YARG.Core chart parser (C#): https://github.com/YARC-Official/YARG.Core
- Onyx (Haskell converter): https://github.com/mtolly/onyx
- Clone Hero (closed source), Feedback Editor, Editor on Fire
- Docs: https://github.com/TheNathannator/GuitarGame_ChartFormats

## Sources
- https://thenathannator.github.io/GuitarGame_ChartFormats/ (chart-format Format-Overview, Brief-History, Tracks/5-Fret-Guitar, 6-Fret-Guitar, Drums, Legacy-Tracks; Implementation-Info/Time-Conversions)
- https://github.com/TheNathannator/GuitarGame_ChartFormats
- https://wiki.yarg.in/wiki/Help:Charting
