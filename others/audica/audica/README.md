# Audica map package (`.audica`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive

## Overview

A ZIP bundling one song: metadata (`song.desc`), up to four difficulty cue lists (`beginner.cues`, `moderate.cues`, `advanced.cues`, `expert.cues`), a MIDI tempo map, the audio (`.mogg`, described by a `.moggsong` text file) and optional album art `song.png`. No official spec exists; knowledge comes from the community C# library `Audica-.NET-Tools` (octoberU) and the osu! converter built on it. Harmonix's in-game map creator lets mappers choose MIDI or cues as the map file type (blog), matching `useMidiForCues` in `song.desc`.

## Contents

`song.desc` (JSON metadata), a MIDI file (tempo map), `*.cues` per difficulty (the chart), `*.moggsong` (text: `mogg_path`, `vol`, `pans`), `*.mogg` (multitrack audio).

## Container & encoding
- ZIP. The library lists entries by `Entry.Name`, so subfolders are tolerated.
- `song.desc` and `*.cues` are JSON (UTF-8 with BOM in the library sources).
- `.moggsong`: text, parsed line by line (`(mogg_path "x.mogg")`, `(vol ...)`, `(pans ...)`). `.mogg` is a Harmonix/Rock Band multitrack Ogg container.
- MIDI (`midiFile` in desc): standard MIDI with tempo events.

## Structure / metadata
### `song.desc` (class `Description`)
`songID`, `moggSong`, `title`, `artist`, `author` (mapper), `midiFile`, `targetDrums`, `sustainSongLeft`, `sustainSongRight`, `fxSong`, `songEndEvent`, `highScoreEvent`, `songEndPitchAdjust` (float), `prerollSeconds` (float), `previewStartSeconds` (double), `useMidiForCues` (bool), `hidden` (bool). Modded extras: `customExpert`, `customAdvanced`, `customModerate`, `customBeginner` (strings, null omitted on write).

### `<difficulty>.cues` (class `Difficulty`)
`{ "cues": [ ... ], "repeaters": [ ... ], "targetSpeed": 1.0 }`

Each cue (class `Cue`):
| Field | Meaning |
|---|---|
| `tick` | start in MIDI ticks |
| `tickLength` | length in ticks (sustain/chain length; old maps may contain floats, cast to int) |
| `pitch` | integer, MIDI pitch, selects the target slot/sound [role inferred; the converter encodes position through `gridOffset`] |
| `velocity` | integer velocity |
| `gridOffset` | `{ "x": float, "y": float }` target position offset on the grid |
| `zOffset` | float depth offset (0 omitted in the descriptor) |
| `handType` | 0 Either, 1 Right, 2 Left, 3 None |
| `behavior` | 0 Standard, 1 Vertical, 2 Horizontal, 3 Hold, 4 ChainStart, 5 Chain, 6 Melee, 7 Dodge |

The library also writes a textual descriptor `tick;tickLength;pitch;velocity;x;y;handType;behavior[;zOffset]`, used in-game for the cue-list text form [inference from `GetDescriptor`].

## Timing model
Ticks are MIDI ticks at 480 per quarter note (`new MidiEventCollection(0, 480)`); the converter treats 480 ticks as one beat, so 1/3, 1/4, 1/6 ... subdivisions are exact. Tempo changes are MIDI `TempoEvent`s (microseconds per quarter note) in the file named by `midiFile`; the library reads them into `TempoData(tick, µs/quarter)`. Millisecond time of a cue = `TempoData.TickToMilliseconds(tick, tempoData)`. `prerollSeconds` is the audio preroll.

## Notes

- `behavior` 0 Standard (hand color by `handType`); Vertical/Horizontal are directional targets; Hold = sustain (`tickLength` > 0, sustain audio `sustainSongLeft/Right`); ChainStart + Chain = chained targets; Melee and Dodge are prompts.
- Position: `gridOffset` (float x, y) relative to a pitch-defined grid cell [inference]; `zOffset` depth.
- Simultaneous cues share a tick. `repeaters`: Unknown semantics. `targetSpeed`: travel speed multiplier.

## Audio & images
`moggSong` -> `.moggsong` text -> `(mogg_path "...mogg")`; optional separate sustain mogg for left/right hand; `fxSong`; `song.png` album art. Preview start via `previewStartSeconds`.

## Versions & variants

Official OST packages and custom maps share the layout; official ones are encrypted/packed inside the game (Unknown, not covered). The in-game creator can save MIDI or cues files (blog). Mod extras: `custom*` in desc.

## Quirks & pitfalls

- Float `tickLength` in old maps.
- Ticks are MIDI ticks, not ms.
- Missing difficulties are absent (null).
- Waveform needs mogg decoding.

## Example
Illustrative, hand-built from the field list above (not a real chart):
```json
{ "cues": [ { "tick": 960, "tickLength": 480, "pitch": 64, "velocity": 20,
              "gridOffset": { "x": 0.0, "y": 0.0 }, "zOffset": 0.0,
              "handType": 1, "behavior": 3 } ],
  "repeaters": [], "targetSpeed": 1.0 }
```

## ROX support
Not read by ROX.

## Parsers & tools
- Audica .NET Tools (C#): https://github.com/octoberU/Audica-.NET-Tools
- AudicaConverter (C#): https://github.com/octoberU/AudicaConverter
- `audica` npm package: https://www.npmjs.com/package/audica (listed in search; not opened)

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (container-only format: no `.audica` committed; `maudica_<id>/` folders hold extracted members). More: https://maudica.com (API `https://maudica.com/api/maps?per_page=30&page=N`, download `https://maudica.com/maps/<id>/download`, ~2150 maps); the old list http://www.audica.wiki:5000/api/customsongs (Zingabopp/AudicaDownloader) no longer answered. Format wiki: https://wiki.maudica.com/files/. Unzip a `.audica` to get `song.desc`, `*.cues`, `song.mid`.

## Sources
- https://raw.githubusercontent.com/octoberU/Audica-.NET-Tools/main/AudicaTools/Audica.cs
- https://raw.githubusercontent.com/octoberU/Audica-.NET-Tools/main/AudicaTools/Cue.cs
- https://raw.githubusercontent.com/octoberU/Audica-.NET-Tools/main/AudicaTools/Description.cs
- https://raw.githubusercontent.com/octoberU/Audica-.NET-Tools/main/AudicaTools/Difficulty.cs
- https://raw.githubusercontent.com/octoberU/Audica-.NET-Tools/main/AudicaTools/MoggSong.cs
- https://github.com/octoberU/AudicaConverter
- https://www.harmonixmusic.com/blog/introducing-audicas-in-game-map-creator
