# Crypt of the NecroDancer custom music beat file (`<song>.mp3.txt`)
Kind: metadata

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview

When the player assigns a custom MP3/OGG to a zone, the game stores its beat analysis in a text file "with the same name as your song file" (official FAQ). It holds only beat positions, which is all the timing the game needs. Sources disagree on the unit (seconds in the FAQ and in a CLI tool that writes the files; milliseconds with commas in a 2017 forum sample), so a parser must sniff the content.

## Container & encoding

- Plain text at `<game dir>/data/custom_music/<audio file name>.txt` (Supinic's tool). The name is the audio file name including its extension plus `.txt` (forum). The audio file is referenced from `save_game.xml` (the tool edits it to add symlinks; a custom lobby track that later goes missing can crash the game, FAQ).
- FAQ (2021 text): "The beat data text file is a numbered list of numbers ... Each number indicates the position of a beat, in seconds. So if you want to remove the final 10 beats, remove the final ten numbers in the list."
- Supinic's tool writes `beats.join("\n")`: one float per line, in seconds (`i + offset` stepping by `60/bpm`).
- A 2017 forum sample is one line of comma-separated integers (e.g. `352,699,1046,1393,...`), milliseconds at 173 BPM (346.8 ms per beat), with its author's notes `BPM: 173`, `Beats: 368` outside the file. [conflict: the format may have changed since 2017, or the sample came from the author's own tool; unresolved]

## Structure / metadata

No header or metadata, just numbers; count = number of beats. [Unknown whether the game accepts both separators.]

## Timing model

Beat times are absolute positions in the audio; intervals give the local tempo. The automatic tracker allows tempo changes but "needs a strong beat", and silence at the end keeps producing beats until the end of the audio (FAQ). Manual mode ("Manual Beats", tap the beat) writes the same file. The first-beat offset is the first number.

## Notes

Unknown: only beats exist; the player drives movement and attacks.

## Audio & images

MP3 or OGG only (FAQ), fully loaded into memory for beat detection. Custom music disables Steam achievements and uses separate leaderboards.

## Versions & variants

- Seconds (FAQ, Supinic tool) vs milliseconds (2017 forum sample).
- `necrodancer.xml` and dungeon files (items, enemies, level layout; parsed by toofz-necrodancer-core) are not charts.

## Quirks & pitfalls

- A renamed non-OGG/MP3 file makes the character fall through floors (FAQ).
- Silence at the end yields extra beats: delete the trailing numbers (FAQ).
- The file name keeps the original audio extension.

## Example
Hand-built from the FAQ and the tool's output rule (120 BPM, one beat every 0.5 s):
```
0.5
1
1.5
2
```
The forum sample line begins `352,699,1046,1393,1740,2087,2434` (origin: Steam discussion thread, 2017, millisecond interpretation inferred).

## ROX support

Not read by ROX (no notes to convert; at most a metronome grid).

## Parsers & tools
- necrodancer-custom-music (JavaScript; wrapper over the game's `beattracker.exe`, writes the `.txt`): https://github.com/Supinic/necrodancer-custom-music
- toofz-necrodancer-core (C#, game XML/replay/save): https://github.com/leonard-thieu/toofz-necrodancer-core
- Game's essentia-based `beattracker` (ships in `data/essentia/` on Windows).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Real beat files are generated locally by the game and not published; the one real sample is a beat list pasted in a 2017 Steam forum thread (comma-separated milliseconds).

More: assign an MP3/OGG as custom music in a zone (official FAQ https://braceyourselfgames.com/crypt-of-the-necrodancer/faq/) and the game writes the beat file next to the audio, or run Supinic/necrodancer-custom-music. Checked, no beat files: Supinic/necrodancer-custom-music, SamuelDev/Necrodancer-Custom-Music-Fix, Callum-Mitchell/Waltzifier.

## Sources
- https://braceyourselfgames.com/crypt-of-the-necrodancer/faq/ (Custom Music section)
- https://github.com/Supinic/necrodancer-custom-music (README, `lib/beatmap.js`, `lib/index.js`)
- https://steamcommunity.com/app/247080/discussions/3/1471967615847881557/ (2017 thread with a beatmap sample)
