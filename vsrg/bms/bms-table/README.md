# BMS difficulty table (HTML + `header.json` + `data.json`)
Kind: metadata

Doc status: complete · ROX: no · Category: vsrg (metadata about BMS charts, no chart data) · Encoding: json (+ one HTML page)

## Overview

A **BMS difficulty table** (難易度表) is the community's way of rating BMS charts: a web page lists charts under a table-specific level scale (Satellite `sl0..`, Stella `st0..`, "Insane" `★`/`▼`, Overjoy, Normal, ...). The listing is machine-readable so that players such as **beatoraja** (whose author wrote the spec) and other tools can import a table, mark the charts the player owns, and offer them as folders/courses. The structure is defined by `exch-bms2` (author of beatoraja) in the `jbmstable-parser` wiki page "難易度表の仕様". A table is three resources: an **HTML page** (for humans, carries a `<meta name="bmstable">` pointer), a **header JSON** (table name, symbol, data URL, level order, courses) and a **data JSON** (the chart list). Charts are identified by the **MD5 and/or SHA-256 of the `.bms/.bme/.bml/.pms/.bmson` file**, not by path. There is also an aggregate "table list" JSON used by tools to enumerate known tables.

## Container & encoding

- JSON (UTF-8) for header and data; the HTML page is ordinary HTML.
- Header and data are separate HTTP resources; `data_url` in the header gives the data URL (relative URLs are resolved against the header URL by clients [inference]).
- The data JSON is a **top-level array** of chart objects. (The Rust parser explicitly does not support a `{ "charts": [...] }` wrapper.)
- File names are not part of the spec; commonly `header.json` and `data.json` (or `score.json`, `insane_data.json`, ...).

## Structure / metadata

### HTML page

In `<head>`:

```html
<meta name="bmstable" content="header.json">
```

(`property="bmstable"` is also accepted by `bms-table-rs`; the content is the header JSON URL.) A client given the HTML URL fetches the page, extracts this URL and then the header.

### Header JSON (single object)

| Field | Type | Required | Meaning |
|---|---|---|---|
| `name` | string | yes | Table name ("file-generatable name": usable as a file name). |
| `data_url` | string | yes | URL of the data JSON. |
| `symbol` | string | yes | Short symbol prefixed to levels, e.g. `sl`, `★`, `▼`. |
| `tag` | string | no | Text used when tagging a chart with this table; falls back to `symbol` when absent. |
| `level_order` | array of string/number | no | Display order of level labels. Omitted: order of first appearance in the data. Accepts numbers and strings (`[1,2,3]`, `["A","B"]`); `bms-table-rs` normalises entries to strings and rejects other types. |
| `course` | array of arrays of Course | no | Courses (段位 grade courses). Spec: `Array(Array(Course))` - outer array = groups, inner = courses; the Rust parser accepts arbitrarily nested arrays and flat arrays. |
| `mode` | string | no | Play mode of the charts, "same as bmson's `mode_hint`" (e.g. `beat-7k`). |
| *others* | any | no | Tables may add their own keys; parsers keep unknown keys as extras (`bms-table-rs` `extra`). |

#### Course object

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Course name. |
| `constraint` | array of string | Restrictions: `grade_random` (grade course; options RANDOM, R-RANDOM, S-RANDOM, MIRROR allowed), `grade_mirror` (grade; only MIRROR allowed), `no_speed` (no hi-speed changes), `no_good` (GOOD becomes BAD), `no_great` (GREAT/GOOD become BAD), `gauge_lr2` (LR2 grade gauge), `gauge_5k`, `gauge_7k`, `gauge_9k`, `gauge_24k` (grade gauges for the key counts), plus engine-specific extras such as `ln` seen in the Rust docs. |
| `trophy` | array of Trophy | Trophy conditions. |
| `charts` | array of data-JSON chart objects | The charts forming the course (full objects). |
| `md5` / `sha256` | array of string | Shorthand: hash lists in play order (parsers expand each to a chart item with `level = "0"`). |

Trophy: `{ "name": "goldmedal" | "silvermedal" | "bronzemedal", "missrate": float (upper bound, 0-100 %), "scorerate": float (lower bound, 0-100 %) }`.

### Data JSON (array of chart objects)

| Field | Type | Req. | Meaning |
|---|---|---|---|
| `md5` | string | one of md5/sha256 | MD5 of the BMS file. |
| `sha256` | string | one of md5/sha256 | SHA-256 of the BMS file. |
| `level` | string | yes | Level label (number or string accepted by parsers; `null`/missing -> `"0"`). |
| `title` | string | no | Chart title. |
| `artist` | string | no | Artist. |
| `url` | string | no | Download URL of the BMS. |
| `url_diff` | string | no | Download URL of the differential (patch) archive. |
| `name_diff` | string | no | Link text for the diff. |
| `url_pack` | string | no | URL of the package that contains it. |
| `name_pack` | string | no | Package name. |
| `comment` | string | no | Comment. |
| `org_md5` | string | no | MD5 of the bundled chart (used for automatic diff installation). |
| `mode` | string | no | Overrides the header's `mode`. |
| `ipfs` | string | no | IPFS path of the BMS (must be a directory). |
| `ipfs_diff` | string | no | IPFS path of the diff (file or directory). |
| `lr2_bmsid` | number | no | LR2IR BMS id (listed in `bms-table-rs` docs; not in the original wiki). |
| *others* | any | no | Table-specific, e.g. `eval`, `total`, `judge`, `note`, `tag` in the wiki example. |

### Table list JSON

Used by tools to enumerate tables: an array of `{ "name", "symbol", "url" }` (plus optional `tag1`, `tag2`, `comment`, `date`, `state`, `tag_order` as seen by `bms-table-rs`'s `BmsTableInfo`).

## Timing model

Not applicable (no chart data).

## Notes

Not applicable. Charts are referenced by hash; the BMS files themselves are obtained from `url`/`url_pack`/`ipfs` or from the player's local library.

## Audio & images

Not applicable.

## Versions & variants

- 2018 wiki revision (5 revisions) defines the core; later additions seen in tooling: `sha256` (as an alternative to `md5`), `mode`, `ipfs`/`ipfs_diff`, `lr2_bmsid`, `tag`, nested `course` arrays, `level` being a number.
- Courses: beatoraja also has its own course JSON (`CourseData`: `name`, `hash` (song array), `constraint`, `trophy`, `release`), see the beatoraja source; that is an application format, not the table spec.

## Quirks & pitfalls

- `level` is a **label**, not necessarily numeric ("sl3", "★12", "?"): order comes from `level_order`.
- md5 vs sha256: the spec requires at least one of the two; consumers should match on whichever is present.
- Course shorthand `md5`/`sha256` lists have no level (`"0"`), and the order is the play order.
- `course` nesting is inconsistent in the wild (flat array vs array of arrays vs deeper).
- Header and data are often served from different domains; many tables are hosted as GitHub Pages or Google Sheets exports.

## Example

From the spec page (`jbmstable-parser` wiki), header (abridged):

```json
{
"name":"第2発狂難易度",
"tag":"▼",
"data_url":"http://rattoto10.jounin.jp/js/insane_data.json",
"symbol":"▼",
"level_order":["0-","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","?"],
"course":[[{"name":"発狂初段","constraint":["grade_mirror"],
  "trophy":[{"name":"silvermedal","missrate":5.0,"scorerate":70.0},{"name":"goldmedal","missrate":2.5,"scorerate":85.0}],
  "md5":["c07125de4ed7fbe7cb066cc41e50e51e","fc7d46e7bbc9f6afd26d05e3bf2ef555","b3887714270e28988ce900e4b9300994","d1877ad5dc0134b27eb0238da5721eed"]}]]
}
```

and a data entry from the same page:

```json
[{"title":"Act Beloved [SP ★1]","level":"12","artist":"Nene Anegasaki feat. Salita / obj:slash Movie : Ryuka",
  "url":"http://manbow.nothing.sh/event/event.cgi?action=More_def&num=268&event=74","comment":"slash難易度表△1",
  "md5":"6a2cf3b81a38dc28f2a5b4e0d18d26ff"}]
```

(The page's data example also shows table-specific `eval`, `total`, `judge`, `tag`, `url_pack`, `name_pack`, `url_diff`, `name_diff`; omitted here.)

## ROX support

Not read by ROX. It carries no notes, only chart identifiers (MD5/SHA-256 of BMS files); it could serve as a rating/filter overlay for a future BMS reader.

## Parsers & tools

- `bms-table-rs` / `bms-table` crate (Rust, Apache-2.0): https://github.com/brightmeows/bms-table-rs, https://crates.io/crates/bms-table
- `bmstable` (Go): https://pkg.go.dev/github.com/Catizard/bmstable
- `jbmstable-parser` (Java, original): https://github.com/exch-bms2/jbmstable-parser
- beatoraja (Java; imports tables): https://github.com/exch-bms2/beatoraja (`TableData.java`, `TableDataAccessor.java`)

## Getting samples

- **Committed** ([`samples/`](samples/), see [`SOURCES.md`](samples/SOURCES.md)): real header + data JSON of four tables (Stella, Satellite, the NEW GENERATION Insane table, the 2017 Normal table archive), downloaded 2026-11-09, plus hand-written `synthetic-header.json` / `synthetic-data.json`.
- **More**: open any table page, read `<meta name="bmstable" content="header.json">` in its HTML, download that header and its `data_url`. Table lists are kept by the players that import them (beatoraja, LR2oraja); table authors' pages are the primary source.

## Sources

- https://github.com/exch-bms2/jbmstable-parser/wiki/%E9%9B%A3%E6%98%93%E5%BA%A6%E8%A1%A8%E3%81%AE%E4%BB%95%E6%A7%98 (specification, Japanese, 2018)
- https://github.com/brightmeows/bms-table-rs (`src/lib.rs`, `src/de.rs`, README) - commit `2caa25bd68a4e2f1f6feb0057700eed96c6a8705`
- https://pkg.go.dev/github.com/Catizard/bmstable
- https://github.com/exch-bms2/beatoraja (`CourseData.java`, commit `83574048ba489082eb46df7fe9806b464bf1f526`)
