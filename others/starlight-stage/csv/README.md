# CGSS beatmap CSV (`.csv`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview

Beatmap tables of CGSS as extracted from the game's resources (the game stores them in `.bdb` databases containing raw chart CSV blobs, with ACB/HCA audio). The schema below is from the DereInfo README ("CSV scheme (2020.12.19 update - witch mode)"). Authoring/extraction tools exist (DereTore toolkit, libcgss, DereGuide).

## Container & encoding

CSV text, one row per object, one file per song/difficulty (debut, regular, pro, master, master+, light, trick, piano, forte are the difficulty names listed by DereInfo). In the game they live in SQLite `.bdb` files; DereInfo extracts SQLite DBs from the data bundle.

## Structure / metadata

Columns in order (as listed by DereInfo):

| # | Column | Meaning |
|---|---|---|
| 1 | `id` | primary key; does **not** indicate note order |
| 2 | `sec` | time (seconds) at which the note reaches the judgement line |
| 3 | `type` | object kind (see below) |
| 4 | `startPos`, 5 `finishPos` | start and end position counted from the left (note path endpoints) |
| 6 | `status` | 0 normal; normal left/right flick; in grand mode the raw note width; tempo if type is 93; colour if type is 9 |
| 7 | `sync` | whether notes at similar times are treated as simultaneous (flag) |
| 8 | `groupId` | links hold, slide and decorator notes |
| 9 | `visible` | when the note appears (>0) or disappears (<0); judge = 100 in witch mode |
| 10 | `size` | note size in witch mode |
| 11 | `distance` | helper for the engine after tempo changes |

`type` values listed by DereInfo: normal, hold (long), slide, grand normal, grand slide, grand left flick, grand right flick, witch accident, witch decorator, and `93` = change tempo (default 100). The ordered list in the README suggests 1..9 as the numeric values [inference]; `93` is explicit.

## Timing model

Absolute seconds per row (`sec`), with tempo changes encoded as `type = 93` rows (status = tempo, default 100) that rescale the speed seen by the engine; `distance` is derived after tempo changes.

## Notes

Normal tap, hold (paired via `groupId` start/end rows), flick (status = left/right), slide (connected by `groupId`, positions change across rows), grand-mode variants (width in `status`), witch-mode accident/decorator objects. Positions count from the left.

## Audio & images

Not in the CSV (ACB/HCA audio, handled by libcgss).

## Versions & variants

2020.12.19 update added witch mode columns (`visible`, `size`, `distance`) and types 8, 9, 93; earlier files have fewer columns.

## Quirks & pitfalls

`id` is not an order; `status` is overloaded by type; grand mode reinterprets `status` as width; group ids must be used to rebuild holds and slides.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

DereTore (C#, authoring toolkit): <https://github.com/OpenCGSS/DereTore>; libcgss (HCA/ACB): <https://github.com/hozuki/libcgss>; DereGuide (iOS): <https://github.com/superk589/DereGuide>; DereInfo (Kotlin/Android): <https://github.com/KYHSGeekCode/DereInfo>; motto-cgss: <https://github.com/logchan/motto-cgss>.

## Sources

- <https://raw.githubusercontent.com/yhs0602/DereInfo/master/README.md>
- <https://github.com/OpenCGSS/DereTore> (listed in search, not read)
