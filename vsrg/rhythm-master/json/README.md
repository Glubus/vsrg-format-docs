# Rhythm Master "imdjson" (`.json`, signature `BNDQ`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: json

## Overview
JSON chart dialect used by newer Rhythm Master clients (technical-test clients of 2022 onward store data as JSON per the RMEssentials changelog); RMEssentials calls it "imdjson", versions 1.2.1, 1.2.2, 1.2.3, 1.3.0, and converts IMD <-> imdjson. The original README lists "`.json`: Rhythm Master WeChat Mini Program chart"; whether the mini program uses exactly this schema is **not verified** (rmstZ lists the mini-program, Project FX and "Bu Xiu De Yin Fu" JSON together as one family). Source: RMEssentials `rmechart.cpp`, `tst_rmechart` fixtures.

## Container & encoding
UTF-8 JSON. The official files keep keys in a fixed order (RMEssentials changelog); readers accept any order.

## Structure / metadata
Top-level: `signature` = `"BNDQ"`, `version` string (1.2.1 / 1.2.2 / 1.2.3 / 1.3.0), `tempo` (number, single BPM), 1.3.0 adds `duration` (ticks) and `durationtime` (ms), 1.2.3+ adds `samples` (array, ignored/empty), `tracks`: array of `{ "track": n (3..8), "note": [...] }`.
Note object: `tick` (48 per beat: `tick = round(ms*bpm/1250)`), `key` (0), `dur` (duration in ticks, 0 if none), `isEnd` (0/1), `toTrack` (target lane for slides, = track otherwise), `volume`, `pan` (127/64 in 1.2.1-1.2.2, 0/0 from 1.2.3), `attr` (0 tap, 3 and 4 as the IMD types), and from 1.2.3: `time` (ms), `time_dur` (ms duration, or lane delta when `dur` is 0 and attr != 0), `idx`.

## Timing model
Single constant tempo; ticks of 1/48 beat; 1.2.3+ also carries absolute ms. IMD BPM lists are not representable ("All versions of imdjson do not support dynamic BPM").

## Notes
Same semantics as [imd](../imd/README.md): attr 0 tap, attr 3/4 + `dur` hold or slide chain members with `isEnd`/`toTrack`. Lane = track-3 (tracks 3..8, up to 6 lanes).

## Audio & images
Not in the file.

## Versions & variants
1.2.1 = 1.2.2; 1.2.3 = 1.3.0 for notes; per-version fields above.

## Quirks & pitfalls
`time_dur` in files converted from IMD may be wrong when `dur` is 0 (RMEssentials: use `dur` as truth); `key` ignored; `samples` ignored.

## Example
First note of `tst_rmechart/tojson/friend01_4k_nm.imd.json` (RMEssentials test fixture, version 1.3.0, tempo 290):
```
{"tick": 384, "key": 0, "dur": 0, "isEnd": 0, "toTrack": 0, "volume": 0, "pan": 0, "attr": 0, "time": 1655, "time_dur": 0, "idx": 0}
```

## ROX support
Not read by ROX.

## Parsers & tools
RMEssentials (C++/Qt): https://github.com/Fsu0413/RMEssentials ; rmstZ.

## Getting samples

- Committed in [`samples/`](samples/): 5 real imdjson files converted from song charts (RMEssentials test tree, AGPL-3.0 repo), 4 valid one-note `existnotes_*` files and 19 deliberately invalid files from the same unit tests. Everything is listed with origin, date and sha256 in [`samples/SOURCES.md`](samples/SOURCES.md).
- More: convert any `.imd` with RMEssentials (https://github.com/Fsu0413/RMEssentials, `RmeChart::toJson`); whether the WeChat mini program uses this schema is unverified.

## Sources
- https://raw.githubusercontent.com/Fsu0413/RMEssentials/master/src/librmessentials/src/rmechart.cpp
- https://raw.githubusercontent.com/Fsu0413/RMEssentials/master/WHATSNEW
- https://lrfasd.github.io/rmstZ/
