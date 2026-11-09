# Interlude binary chart (`.yav`, "headless" chart blob)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian, .NET `BinaryWriter`)

## Overview

Interlude (YAVSRG) stores every imported chart in its own compact binary form: the key count, the note rows, the BPM list and the scroll-velocity list. Historically it was a file, `.yav`; since the "Chart database" change of the changelog ("Your charts are now stored in an SQLite database file instead of as folders of .yav files", `docs/changelog.md`) it is a `BLOB` column of a SQLite table and the payload the Interlude CDN serves. The source states that the file reader is dead code: "this unused code used to be for reading .yav files, which no longer exist" (`prelude/src/Charts/ImportChart.fs`), and that a "future .yav file format that allows charts to be imported and exported as files" is only planned. The wiki (`docs/wiki/adding_songs.md`) and Prelude's README still say charts are "converted to the .yav file format" [outdated: contradicts the code comment]. There is therefore **no current `.yav` file**, but the binary layout documented below is real, current, and is what a chart looks like when downloaded from `https://cdn.yavsrg.net/<chart hash>`.

Everything here is read from YAVSRG/YAVSRG @ a7c78e77733595749e63da26b5300e8962a4e111 (`prelude/src/Charts/Chart.fs`, `NoteRow.fs`, `Shared/TimeArray.fs`, `Shared/Bitmask.fs`, `Data/ChartDatabase/DbCharts.fs`, `Data/Imports/OnlineImports.fs`) and verified by decoding 7 real CDN files and recomputing their hash (see Getting samples).

## Packaged in

Not packaged in an archive. It lives in the `charts.Chart` BLOB column (`DbCharts`: `CREATE TABLE charts (Id TEXT PRIMARY KEY, Title, TitleNative, Artist, ArtistNative, DifficultyName, Subtitle, Source, Creator, Tags, Background, Audio, PreviewTime, Packs, Origin, Keys INTEGER, Length, BPM, DateAdded, CalcVersion, Rating, Patterns, Chart BLOB)`) and as the body of CDN downloads. Audio and background are separate assets (hash-named, `chart_db.AssetStorage`; the CDN serves them under `/assets/<hash>`).

## Container & encoding

- Little-endian binary written with .NET `BinaryWriter`; no magic, no version, no length or key count inside the blob: **the key count is stored outside** (the `Keys` column / `ChartMeta`) and must be passed to the reader (`Chart.ReadFromStreamHeadless(keys, br)`, "headless" = without the header).
- Legacy `.yav` file (reader kept in `ImportChart.legacy_from_yav_file`): `byte keys`, a .NET `BinaryWriter` string (7-bit-length-prefixed UTF-8) holding the JSON `ChartImportHeader`, then the headless chart. The exact JSON encoding of the union fields (`BackgroundFile`/`AudioFile: ImportAsset = Copy | Link | Download | Missing`) is Unknown; no `.yav` file was found to check.
- Identification: `Chart.Hash()` = uppercase hex SHA-256 over keys, rows, SV changes and length (below); it is the CDN file name and the chart id.

## Structure / metadata

Three consecutive `TimeArray`s (`TimeArray.write`: `int32 count`, then per item `float32 time (ms)` + the item payload):

| Block | Item payload |
|---|---|
| Notes | `uint16 mask` (bit *c* = column *c* non-empty, LSB = column 0; `Bitmask`), then one `byte` per set bit in ascending column order: 1 normal, 2 hold head, 3 hold body, 4 hold tail (`NoteType`) |
| BPM | `int32 meter` (beats per measure), `float32 ms-per-beat` |
| SV | `float32 multiplier` |

Metadata (title, artist, creator, difficulty name, tags, preview time, background/audio hashes, origins) is **not** in the blob; it is in the table row (`ChartMeta`) or the legacy JSON header (`ChartImportHeader`: Title, TitleNative, Artist, ArtistNative, Creator, DiffName, Subtitle, Source, Tags, PreviewTime, BackgroundFile, AudioFile, Origins).

## Timing model

Times are `float32` milliseconds from the audio start. Notes are grouped in rows (one row per distinct time; times strictly increasing, `CheckForErrors`). BPM entries give meter and ms per beat (`mspb >= 0`, not NaN); SV entries are a scroll multiplier from their time on (`NaN` forbidden, `+Infinity` allowed to mean "infinite" per the error text). There must be at least one BPM entry.

## Notes

Row `NoteType` per column: `0` nothing (not stored), `1` tap, `2/3/4` hold head/body/tail. A hold is stored as a head row, a body entry in **every intermediate row** of that column, then a tail row; the validator rejects a head inside a hold, a body or tail without a head, a missing body, an unterminated hold, an empty row (a row with only bodies/nothing) and 0 notes. Key count 3..10.

## Audio & images

Not stored (referenced by hash in the database, downloaded separately).

## Versions & variants

No version field. `CALC_VERSION` in `DbCharts.fs` versions the cached pattern/rating data, not the chart blob.

## Quirks & pitfalls

- A reader needs the key count from outside; with a wrong count a set bit beyond the key count makes decoding fail (observed with my reader: index error on the 94-byte JSON 404 body of the CDN, which is not a chart).
- Hash input (`Chart.Hash`): `int32 keys`; then for every row, one byte per column **including empty ones** (0..4); then for each SV entry whose multiplier differs from the running one (start 1.0) `int32 round((t - firstNoteTime) * 0.2)` + `float32 multiplier`; finally `int32 round((lastNoteTime - firstNoteTime) * 0.01)` ( .NET `Convert.ToInt32`, round-half-even; BPM is not hashed). A Python re-implementation reproduced the CDN hash for all 7 downloaded files [observed].
- Hold bodies are explicit rows entries, so there is no `endTime`.
- A chart missing from the CDN answers HTTP 404 with a JSON body, not a chart: most hashes listed in `backbeat/archive/charts.json` were 404 on 2026-11-09.

## Example

`samples/synthetic-4k-headless.bin` (114 bytes): `07 00 00 00` (7 rows) then `00 00 00 00 | 01 00 | 01` (time 0.0 ms, mask 0b0001, a tap on column 0), `00 00 FA 43 | 0A 00 | 01 02` (500.0 ms, mask 0b1010 = columns 1 and 3: tap, hold head) ... followed by the BPM block `02 00 00 00` (2 entries: 0 ms, meter 4, 500.0 ms/beat; 1000 ms, meter 4, 400.0) and the SV block `03 00 00 00` (1.0, 1.5, 1.0).

## ROX support

None. ROX has no Interlude codec; a converter would need the key count, BPM and SV lists above (hold bodies are redundant with head/tail).

## Parsers & tools

- Prelude (F#, MIT): `Chart.ReadFromStreamHeadless` / `WriteToStreamHeadless`; the `ImportChart` module for `.sm`/`.osu`/Quaver conversion into this model.
- Interlude's CDN client: `OnlineImports.cdn_install` downloads `https://cdn.yavsrg.net/<hash>`, parses it and refuses it when `Chart.Hash()` differs from the requested hash.

## Getting samples

- **Committed** in [`samples/`](samples/) (see [`SOURCES.md`](samples/SOURCES.md)): one 114-byte hand-built CC0 blob (4 keys, holds, 2 BPM, 3 SV) written from the source and read back with an independent decoder.
- **Manifest**: none. The 7 real charts decoded for this page (4K, 6K, 7K, 9K; 1.5-17.8 KB) come from the live CDN, which is not immutable (most listed hashes already 404), so they are not hashed; reproduce with `curl -L https://cdn.yavsrg.net/<HASH>` for the hashes of `backbeat/archive/charts.json` whose `Keys` you want (e.g. `10998A892E0891DDF16AD36EFE15340F08A45D3827BF03A89383D0A64F9ED912`, 4K, 1537 bytes, at the time of writing); check the response is not the 94-byte JSON error.
- **How to get more**: install Interlude (https://www.yavsrg.net), import any osu!mania/StepMania/Quaver library (Options > Library); the charts land in the SQLite `charts` table as `Chart` BLOBs (location of the database file: Unknown here), which you can extract with any SQLite tool; legacy folders of `.yav` files exist only in Interlude builds before the "Chart database" change [inference, changelog gives no version here].

## Sources

- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Charts/Chart.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Charts/NoteRow.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Shared/TimeArray.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Charts/ImportChart.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Data/ChartDatabase/DbCharts.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/src/Data/Imports/OnlineImports.fs
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/docs/changelog.md ("Chart database")
- https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/docs/wiki/adding_songs.md
- Repo samples: vsrg/interlude/yav/samples/
