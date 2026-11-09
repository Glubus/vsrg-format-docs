# CGSS beatmap CSV (`.csv`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: text

## Overview
Beatmap tables of CGSS extracted from the game's `.bdb` databases (raw chart CSV blobs; audio is ACB/HCA). The schema is from the DereInfo README ("CSV scheme (2020.12.19 update - witch mode)").

## Container & encoding
CSV text, one row per object, one file per song/difficulty (debut, regular, pro, master, master+, light, trick, piano, forte per DereInfo). In the game they live in SQLite `.bdb` files; DereInfo extracts the SQLite DBs from the data bundle.

## Structure / metadata

Columns in order (as listed by DereInfo):

| # | Column | Meaning |
|---|---|---|
| 1 | `id` | primary key; not the note order |
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

Absolute seconds per row (`sec`). Tempo changes are `type = 93` rows (status = tempo, default 100) that rescale the speed seen by the engine; `distance` is derived after them.

## Notes

Holds pair start/end rows via `groupId`; slides link rows by `groupId` with changing positions; flicks use `status` = left/right; grand variants carry width in `status`. Positions count from the left.

## Audio & images

ACB/HCA audio, handled by libcgss.

## Versions & variants

2020.12.19 update added witch mode columns (`visible`, `size`, `distance`) and types 8, 9, 93; earlier files have fewer columns.

## Quirks & pitfalls

`id` is not an order; `status` is overloaded by type (width in grand mode); rebuild holds and slides from group ids.

## Example

First rows, 8-column variant without the witch columns [observed: mishiro-score-viewer_8039-1.csv]:

```
id,sec,type,startPos,finishPos,status,sync,groupId
1,0,100,0,0,116,0,0
2,0,91,,,,0,0
3,2.926829,1,1,2,0,0,0
4,4.390244,1,4,5,0,0,0
```

## ROX support

Not read by ROX.

## Parsers & tools

DereTore (C#, authoring toolkit): <https://github.com/OpenCGSS/DereTore>; libcgss (HCA/ACB): <https://github.com/hozuki/libcgss>; DereGuide (iOS): <https://github.com/superk589/DereGuide>; DereInfo (Kotlin/Android): <https://github.com/KYHSGeekCode/DereInfo>; motto-cgss: <https://github.com/logchan/motto-cgss>.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (`<musicId>-<difficulty>.csv` from the mishiro-score-viewer repository).

[observed: mishiro-score-viewer_*.csv] 8-column header `id,sec,type,startPos,finishPos,status,sync,groupId` (no `visible`/`size`/`distance`); `type` values found: 1, 2, 3, 91, 92 and 100 (the first rows are a `100` and a `91` at sec 0 with status e.g. 46). The meaning of 91/92/100 is not in the sources. More: extract `.bdb` databases from the game data (DereInfo, DereTore).

## Sources

- <https://raw.githubusercontent.com/yhs0602/DereInfo/master/README.md>
- <https://github.com/OpenCGSS/DereTore> (listed in search, not read)
