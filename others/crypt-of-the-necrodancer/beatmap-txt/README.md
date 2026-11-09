# Crypt of the NecroDancer custom music beat file (`<song>.mp3.txt`)
Kind: metadata

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview
When the player assigns a custom MP3/OGG to a zone, NecroDancer analyses it and stores the result in a text file next to the game data: the beat data text file "with the same name as your song file" (official FAQ). It contains only beat positions, no notes. Because the game is a rhythm roguelike, this is the entire timing description the game needs for custom music. Sources disagree on the unit (seconds in the FAQ and in a CLI tool that writes the files, milliseconds with commas in a 2017 forum sample), so a parser must sniff the content.

## Container & encoding
- Plain text. Location (Supinic's tool): `<game dir>/data/custom_music/<audio file name>.txt`; the audio file is referenced from the game's `save_game.xml` (the tool edits it to add symlinks; a custom lobby track that is later missing can crash the game, FAQ).
- Name: exactly the audio file name including its extension plus `.txt` (forum: "the name is the same as the song name including extension + .txt").
- Official FAQ (2021 text): "The beat data text file is a numbered list of numbers ... Each number indicates the position of a beat, in seconds. So if you want to remove the final 10 beats, remove the final ten numbers in the list."
- Supinic's tool writes `beats.join("\n")`, i.e. one floating point number per line, in seconds (`i + offset` stepping by `60/bpm`).
- A forum sample from 2017 shows a single line of comma-separated integers (e.g. `352,699,1046,1393,...`) which at 173 BPM (346.8 ms per beat) are milliseconds, followed (outside the file) by its author's notes `BPM: 173`, `Beats: 368`. [conflict: the format may have changed between 2017 and the FAQ, or the sample was the output of the author's own console tool; unresolved]

## Structure / metadata
No header, no metadata: just numbers. Count = number of beats. [Unknown whether the game accepts both separators.]

## Timing model
Beat times are absolute positions in the audio. Intervals between numbers define the tempo locally (tempo changes are allowed by the automatic tracker, which "needs a strong beat"; silence at the end keeps producing beats until the end of the audio, FAQ). Manual mode ("Manual Beats" option, tap the beat) produces the same file. First-beat offset is just the first number.

## Notes
Not applicable: gameplay events (movement, attacks) are driven by the player; only beats exist.

## Audio & images
MP3 or OGG only (FAQ), which must be fully loaded into memory for beat detection. Using custom music disables Steam achievements and uses separate leaderboards.

## Versions & variants
- Unit seconds (FAQ, Supinic tool) versus milliseconds (2017 forum sample).
- The game also has its own XML (`necrodancer.xml`, dungeon files) for items, enemies and level layout, parsed by toofz-necrodancer-core; these are not charts.

## Quirks & pitfalls
- Wrong or non-OGG/MP3 content with a renamed extension makes the character fall through floors (FAQ).
- Silence at the end yields extra beats: delete the trailing numbers (FAQ).
- The file name must keep the original audio extension.

## Example
Illustrative, hand-built from the FAQ and the tool's output rule (120 BPM, one beat every 0.5 s):
```
0.5
1
1.5
2
```
The forum sample line begins `352,699,1046,1393,1740,2087,2434` (origin: Steam discussion thread, 2017, millisecond interpretation inferred).

## ROX support
Not read by ROX. No notes to convert; at best a metronome grid.

## Parsers & tools
- necrodancer-custom-music (JavaScript; wrapper over the game's `beattracker.exe`, writes the `.txt`): https://github.com/Supinic/necrodancer-custom-music
- toofz-necrodancer-core (C#, game XML/replay/save): https://github.com/leonard-thieu/toofz-necrodancer-core
- Game's essentia-based `beattracker` (ships in `data/essentia/` on Windows).

## Getting samples

- **Committed**: 2 file(s) in [`samples/`](samples/) (see samples/SOURCES.md for origin, author and licence of each).
- **Manifest**: none.
- **More samples**: the game writes the file itself: assign an MP3/OGG as custom music in a zone (official FAQ, https://braceyourselfgames.com/crypt-of-the-necrodancer/faq/) and the beat text file appears with the audio name + `.txt`; or run Supinic/necrodancer-custom-music (writes `<game dir>/data/custom_music/<audio>.txt`, per the fiche). No real file was found under a licence; the two committed files are synthetic. The 2017 Steam forum thread cited in the fiche contains a (millisecond) sample line that was not copied.

## Sources
- https://braceyourselfgames.com/crypt-of-the-necrodancer/faq/ (Custom Music section)
- https://github.com/Supinic/necrodancer-custom-music (README, `lib/beatmap.js`, `lib/index.js`)
- https://steamcommunity.com/app/247080/discussions/3/1471967615847881557/ (2017 thread with a beatmap sample)
