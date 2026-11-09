# Rock Band `songs.dta`
Kind: metadata

Doc status: stub · ROX: no · Category: vsrg · Encoding: text

## Overview
`songs.dta` (compiled `songs.dtb` on disc) is the song database of Rock Band / Guitar Hero (Harmonix engine) DLC and custom packages: one DataArray per song with names, audio track layout and the path of the `.mid` chart. It holds metadata and audio mixing only; notes are in the referenced MIDI ([mid](../../clone-hero/mid/README.md)). YARG, Clone Hero and Phase Shift support `songs.dta` for custom Rock Band songs (YARG wiki "Songs" page).

## Container & encoding
Text S-expression (Lisp-like, parentheses; `;` starts a comment). Compiled form `.dtb` is binary (format not documented here). Normally shipped inside a CON/PKG package together with the `.mid`, `.mogg` (audio) and `gen/*.milo_*` files.

## Structure / metadata
Each entry: `(<shortname> (name "Title") (artist "Artist") (master TRUE) (song_id 1061) (song_length 208746) (preview 44369 74369) (game_origin rb3) (year_released ...) (genre poprock) (vocal_gender male) (album_art TRUE) (song (name songs/<s>/<s>) (tracks ((drum (0 1 2 3)) (bass 4) (guitar (5 6)) (vocals (7 8)))) (pans (...)) (vols (...)) (cores (...)) (midi_file songs/<s>/<s>.mid)) ...)`.
- `master`: FALSE displays "as made famous by".
- `song_id`: integer used for scores/leaderboards.
- `preview`: start/stop ms.
- `song.tracks`: maps instruments to channels of the `.mogg`; `pans` -1.0 left .. 1.0 right; `vols` -10..10 dB-like; `cores` integer array.
- Other keys (rank, bank, drum_bank, etc., difficulty "rank" values) exist: Unknown here; see sources.
Example origin: shortened from the Rock Band debug song "Dead on Arrival" as printed by The Cutting Room Floor and the Milo Modding Wiki.

## Timing model
Not applicable.

## Notes
Not applicable.

## Audio & images
`.mogg` multitrack audio (path in `song.name`), album art `.png_xbox`/`.png_ps3` in `gen/`, `.milo` files (animation).

## Versions & variants
`songs.dta` for RB1/2/3, GH and custom songs; extra keys differ per game (Unknown).

## Quirks & pitfalls
Compiled `.dtb` must be decompiled; keys vary per game version.

## Example
```
(deadonarrival
   (name "Dead on Arrival")
   (artist "Fall Out Boy")
   (master TRUE)
   (song
     (name songs/deadonarrival/deadonarrival)
     (tracks ((drum (0 1 2 3)) (bass 4) (guitar (5 6)) (vocals (7 8))))
     (midi_file songs/deadonarrival/deadonarrival.mid)))
```
(Excerpt of the Rock Band debug entry as published by The Cutting Room Floor; pans/vols/cores lines omitted.)

## ROX support
Not read by ROX.

## Parsers & tools
dtab (Haskell, Data.DTA.Serialize.RB3): https://hackage.haskell.org/package/dtab-1.0/docs/Data-DTA-Serialize-RB3.html · Onyx: https://github.com/mtolly/onyx · YARG.Core · Rock Band Customs Project guides.

## Getting samples
- Committed in [`samples/`](samples/SOURCES.md): `synthetic-songs.dta`, two fictional entries written strictly from the layout in this fiche (CC0).
- Manifest: `missing_song_data.dta` from the Onyx repository (186,793 bytes, GPL-3.0 repo). Observed there: a lighter DTA dialect with quoted symbols (`('21guns' ('song' ('vocal_parts' 3)) ('song_length' 327727) ('format' 10) ('game_origin' 'rb1_dlc') ...)`) and only a few keys per entry (no `tracks`/`midi_file`).
- More: any Rock Band 3 DLC/custom package extracted as a folder contains `songs/songs.dta` (structure: https://wiki.yarg.in/wiki/Songs, "ex-CON"/"ex-PKG"); the Rock Band Customs Project explains how to author one (https://rock-band-customs.gitlab.io/authoring-dtas.html); Onyx (https://github.com/mtolly/onyx) writes `songs.dta` when building RB3 packages. Commercial `songs.dta` files are not redistributable; compiled `.dtb` files need decompiling.

## Sources
https://milo.ipg.pw/index.php/Songs.dta (via search excerpts; page not reachable directly) · https://new.tcrf.net/Rock_Band_(PlayStation_2)/Debug_Songs · https://hackage.haskell.org/package/dtab-1.0/docs/Data-DTA-Serialize-RB3.html · https://rock-band-customs.gitlab.io/authoring-dtas.html · https://wiki.yarg.in/wiki/Songs
