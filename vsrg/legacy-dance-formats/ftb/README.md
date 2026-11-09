# Raindrop FTB text chart (`.ftb`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg (7 fixed lanes) · Encoding: text

## Overview

`.ftb` is read by Raindrop's `NoteLoaderFTB.cpp`, described in its own comment as "pretty much the simplest possible loader: all notes should contain a start time, possibly an end time (both in seconds [sic: ms in the file]) and you require at least a single BPM". The origin game/tool is Unknown; the Flash Flash Revolution forum thread on "raindrop ARCADE" lists "ftb txt charts" among supported formats. Everything below is read from the loader ([zardoru/raindrop @662dd11](https://github.com/zardoru/raindrop/blob/662dd11f4/src/NoteLoaderFTB.cpp)).

## Container & encoding

Text, one record per line; lines starting with `#` or empty are skipped. Fields are space separated. Metadata comes from a separate file read by `LoadMetadata`: line 1 = music file name, line 2 = title, line 3 = author.

## Structure / metadata

- `BPM <time_ms> <bpm>`: a BPM/timing segment at a time in **milliseconds** (the loader divides by 1000).
- Note line: `<start_ms>[-<end_ms>] <unused> <track>`: field 0 is the start time (ms), optionally `start-end` for a hold; field 1 is ignored ("index 1 is unused"); field 2 is the 1-based track.

## Timing model

Times are absolute milliseconds ("BT_MS"). The first BPM segment time becomes the chart offset; at least one `BPM` line is required, otherwise loading fails. Raindrop uses a single measure holding all notes.

## Notes

Fixed **7 channels** (`Channels = 7`); `Track` 1..7 (stored as `Track-1`). Tap = single time, hold = `start-end`. No mines, no keysounds.

## Audio & images

Only the music file name from the metadata file.

## Versions & variants

None known.

## Quirks & pitfalls

Time unit is ms despite the code comment; a note line without `-` has no end; the unused middle field must exist (loader indexes `LineContents[2]`).

## Example

Illustrative, built from the loader rules:

```
BPM 0 150
1000 0 1
1500-2000 0 4
```

## ROX support

Not read by ROX. Trivial to decode: 7 columns, ms times, Tap/Hold, BPM points.

## Parsers & tools

Raindrop (C++).

## Getting samples

Committed in [`samples/`](samples/SOURCES.md): one **synthetic** (hand-written, CC0) `.ftb` written from Raindrop's `NoteLoaderFTB.cpp`: two `BPM` lines, taps on all 7 tracks, a chord, and holds (`start-end`). The loader reads titles from a separate metadata file (3 lines: music file, title, author), not included.

No real `.ftb` exists in the open: Raindrop's test folder has `esb.osu`, `esb.osb`, `jnight.ssc` only; the origin game/tool of the format is Unknown. How: run [Raindrop](https://github.com/zardoru/raindrop) (GPL-3.0) and load a folder whose charts are `.ftb`; a chart can also be produced by hand from the page's rules.

## Sources

- https://github.com/zardoru/raindrop/blob/662dd11f/src/NoteLoaderFTB.cpp
- https://www.flashflashrevolution.com/vbz/home/forum/gaming/other-music-games/121823-raindrop-arcade-freeware-music-game-now-recruiting?t=146390
