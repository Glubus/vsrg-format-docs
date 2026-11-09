# Sound Space text map (`.txt`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview
The original Sound Space (Roblox) map format: a single line of text, `audioId,x|y|ms,x|y|ms,...`. Sound Space Plus imports it as `MAP_TXT` (together with the audio file) and Rhythia tools can export it (`NOTES2TEXT` in pysspm). Communities keep large lists of `.txt` maps (e.g. GitHub `auxsyo/soundspace-maps`, `Uncle0698/Maps`, seen in search only).

## Container & encoding
Plain text, one line, comma-separated items. The audio is not in the file: the first item is the audio id (a Roblox asset id in the original game; SS+ ignores it and pairs the txt with a local audio file).

## Structure / metadata
- Item 0: audio id (discarded by SS+: `split.remove(0)`).
- Items 1..n: `x|y|ms` with three `|`-separated numbers.
- pysspm `NOTES2TEXT` writes `,x|y|ms` per note (a leading comma; the audio id left empty), i.e. a string like `,1|1|1000,2|0|1500`.
- No title/artist/difficulty metadata.

## Timing model
`ms` = milliseconds from the start of the audio. No BPM.

## Notes
- Tap-only. `x`, `y` are floats allowed (quantum). SS+ converts on import: `x_internal = 2 - x`, `y_internal = 2 - y` (SS+ `Song.gd` `loadRawData`), i.e. the text coordinates are mirrored relative to the sspm grid (sspm: 0 = left/top).
- Empty items count as "blank notes", items without exactly 3 fields as "invalid notes"; SS+ warns but keeps the rest.
- Notes are not required to be sorted (SS+ sorts).

## Audio & images
None in the file.

## Versions & variants
- Roblox Sound Space `.txt` (this format) vs sspm v1/v2 ([sspm](../sspm/README.md)).
- Vulnus JSON is a separate game format ([vulnus](../../vulnus/json/README.md)).

## Quirks & pitfalls
Mirrored coordinates, trailing separators and empty items, absent audio, ms as float.

## Example
Illustrative, hand-built from the rules above: `123456789,0|0|1000,1|1|1500,2|2|2000`  (audio id, then three notes).

## ROX support
Not read by ROX.

## Parsers & tools
- Sound Space Plus loader (GDScript): https://github.com/Rhythia/sound-space-plus
- pysspm-rhythia `NOTES2TEXT`: https://github.com/David-Jed/pysspm-rhythia

## Getting samples

Committed in [`samples/`](samples/): 21 real single-line maps - three built-in maps of Sound Space Plus (MIT), 13 maps from `nruv/sound-space` and five from `CotixGD/SS-Archive` (community maps by Robineesti11, some without extension in the repo; `.txt` added). See [`samples/SOURCES.md`](samples/SOURCES.md) for every file's source URL, fetch date, sha256 and terms. [observed: first item is a numeric id, then `x|y|ms` triples].

## Sources
- https://raw.githubusercontent.com/Rhythia/sound-space-plus/HEAD/scripts/content/game/Song.gd
- https://raw.githubusercontent.com/David-Jed/pysspm-rhythia/main/pysspm_rhythia/pysspm.py
