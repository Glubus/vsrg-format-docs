# osu! storyboard file (`.osb`)
Kind: effects

Doc status: partial · ROX: no · Category: vsrg (it accompanies mania maps; it carries no notes) · Encoding: text

## Overview

`.osb` is "a file format containing information about an osu! storyboard" (osu-wiki `.osb (file format)`, a one-line page). It holds the storyboard shared by all difficulties of a set; each `.osu` may also carry its own storyboard in `[Events]`. It has no notes and no timing. Some mania sets use `Sample` events as keysounds.

## Packaged in

- `.osz` (zip of a beatmap set: one `.osu` per difficulty, audio, background, optional video, `.osb` storyboard, hitsounds).

## Container & encoding

Text, same conventions as `.osu` (UTF-8, `//` comments, `[Section]` headers). It sits in the beatmap folder next to the `.osu` files (and inside the `.osz`), usually named `Artist - Title (Creator).osb`. The first line is normally `osu file format v14`. [inference from osu-file-parser, which can append an `.osb` to an `.osu` structure]

## Structure / metadata

- `[Events]`: same syntax as the storyboard part of `.osu` `[Events]`: object declarations (`Sprite`, `Animation`), `Sample`, and their commands. Command table: [../osu/README.md](../osu/README.md#storyboard-events-inside-events-or-the-osb-file) (F, M, MX, MY, S, V, R, C, P, L, T, easing 0-34).
- `[Variables]`: `$name=value` text substitutions applied to every later line (`Sprite,Pass,Centre,$sample_path,320,240` -> `"Sample.png"`). Only valid in `.osb`, not supported in `.osu` (osu-wiki, Storyboard/Scripting/Variables). The editor replaces all occurrences of a value by the variable name on save, so short values (e.g. `12`) are dangerous.

## Timing model

All times are absolute ms from the start of the audio (event `startTime`, command start/end, `Sample` time), independent of BPM. Triggers and loops are relative to their own start.

## Notes

No notes. `Sample,<time>,<layer>,"file",<volume>` plays an audio file at `time`.

## Audio & images

Paths are relative to the beatmap folder, with `\` or `/` separators, usually quoted. Animations refer to `name.ext` and use `name0.ext..nameN.ext`.

## Versions & variants

Follows the `.osu` version line. `Variables` exist only here.

## Quirks & pitfalls

File order of objects is the draw order within a layer; commands, not declaration order, set appearance time. An object disappears after its last command ends. `Fail`/`Pass` layer objects depend on the player's HP state, so a static decoder must pick one.

## Example

No `.osb` sample is copied here. The wiki's examples are in the command tables of the `.osu` page.

## ROX support

Not read by ROX.

## Parsers & tools

- osu-file-parser (Rust) parses `.osb` and can append it to an `.osu` structure: https://docs.rs/osu-file-parser
- osu!lazer storyboard decoder (C#): https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/Formats/LegacyStoryboardDecoder.cs (file exists, HTTP 200; not read in detail)

## Getting samples

- Committed in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): 14 tiny `.osb` decoder test files from ppy/osu @ bb37f05 (MIT): animation loops/types, `[Variables]` (self-reference, suffix), video events with upper/lower-case extensions, out-of-order start times.
- Also committed: 7 real storyboards of the osu-file-parser tests (`osu-file-parser_*.osb`; 0.3-76 KB), see `samples/SOURCES.md`; upstream has no LICENSE file.
- More: a mapset's `.osb` sits at the root of the `.osz` next to the `.osu` files. The osu! wiki storyboard section and any ranked set with storyboard (https://osu.ppy.sh/beatmaps, filter "Has storyboard") provide real ones. The editor writes the shared storyboard to `<set>/<Artist - Title (Creator)>.osb`.

## Sources

- https://github.com/ppy/osu-wiki/tree/master/wiki/Client/File_formats (osb page)
- https://github.com/ppy/osu-wiki/tree/master/wiki/Storyboard/Scripting (Objects, Commands, Compound_Commands, Audio, Variables)
- https://docs.rs/osu-file-parser/1.1.0/
