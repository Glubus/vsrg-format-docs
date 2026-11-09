# Malody chart (`.mc`)
Kind: chart

Doc status: partial · ROX: reads/writes (Key mode, `meta.mode == 0`, only) · Category: vsrg · Encoding: json

## Overview
`.mc` is the JSON chart format of Malody / Malody V (Mugzone). One file holds one difficulty of one game mode. All modes (Key, Catch, Pad, Taiko, Ring, Slide, Live, Cube) share the container; only `meta.mode`, `meta.mode_ext` and the per-note fields change. Files come from the in-game editor, the chart store (inside an `.mcz` package, see ../mcz/) or converters (osu2mc, rmstZ...).

Category: vsrg. Key mode (4K-9K, up to 10K by editing) is a fixed-column vertical scroller and nearly all charts (kangalioo scraped >10,000 4K and >1,000 5K-10K charts). The other modes (Catch = osu!catch-like, Pad = jubeat-like grid, Taiko, Ring = circular, Slide = free x-position slides, Live, Cube) are not column-based but share the container, so they are documented here. The Ring sample (mode 6, 8 columns, holds) is index based and plays on a circle.

Mode numbers (`meta.mode`; the "Mode definition" of the official Store API, same table in the editor plugin API):

| `meta.mode` | Mode | Evidence |
| --- | --- | --- |
| 0 | Key | Store API, Editor Plugin API, samples |
| 3 | Catch | Store API, Editor Plugin API |
| 4 | Pad | Store API, Editor Plugin API |
| 5 | Taiko | Store API, Editor Plugin API; `mc2tja` sample file has `"mode": 5` |
| 6 | Ring | Store API, Editor Plugin API; samples `1543393546.mc` / `1549455608.mc` have `"mode": 6`, `mode_ext.column = 8`, hold notes (`endbeat`) |
| 7 | Slide | Store API, Editor Plugin API |
| 8 | Live | Store API |
| 9 | Cube | Editor Plugin API only |
| 1, 2 | Step (`.sm`-like) and DJ (`.bms`-like) in older Malody (the FAQ lists "Key/Step" for `.sm` and "Key/DJ" for bms/pms) | ids 1 and 2 are an [inference] from the numbering gap; no source states them |

## Packaged in

- `.mcz` (zip: one or more `.mc` charts plus audio, background, optional video and keysounds).

## Container & encoding
- JSON, UTF-8. Some files begin with a UTF-8 BOM (`EF BB BF`): the MorePractice server strips 3 bytes before parsing; malody-convert uses default `json.load`. Skip a BOM. The repo samples have none. Pretty-printed (4 spaces) and single-line (e.g. `1557200618.mc`) files both exist.
- One file = one chart. Store packages name it `<chart id>.mc`; samples use Unix timestamps such as `1487327905.mc`.
- Top-level keys: `meta`, `time`, `note`, optionally `effect` and `extra` (editor state). Tolerate unknown keys (malody-convert rejects unknown meta keys as a safety check; its allow-list is below).

## Structure / metadata

```
{ "meta": {...}, "time": [...], "effect": [...], "note": [...], "extra": {...} }
```

### `meta`

| Field | Type | Meaning / notes |
| --- | --- | --- |
| `$ver` | int | Chart format version; only seen as `0` in the sample `1557200618.mc`, absent in older files. Other values: Unknown. |
| `creator` | string | Chart author (may be empty). |
| `background` | string | Background image file name, relative to the chart folder (e.g. `tmp.jpg`). May be empty. |
| `version` | string | Difficulty name (`"5K NORMALLY Lv.27"`, `"Crazy"`); free text. |
| `preview` | int | Preview start in ms (ROX maps it to `preview_time_us`). Optional. |
| `id` | int | Chart id on the Malody store; 0 for local. |
| `mode` | int | Game mode, see table above. |
| `time` | int | Last modification Unix time (seconds). |
| `song` | object | `title`, `artist`, optional `titleorg` / `artistorg` (original-script names; malody-convert and ROX prefer them), `id` (store song id), optionally `org` object (`title`, `artist`; malody-convert), `source`. |
| `mode_ext` | object | Mode specific. Key/Ring: `column` (key count; observed 4, 5 in Key samples; 8 in Ring samples). Taiko: `bar_begin` (first bar index; mc2tja uses it). osu2mc also writes `bar_begin` for Key (value 0). |
| `video` | string | Optional video file (malody-convert allow-list). |
| `cover` | string | Written by ROX's encoder; not seen in the samples. |

malody-convert's allow-lists (known fields): meta = `preview, $ver, creator, background, version, id, mode, time, song, mode_ext, video`; song = `title, titleorg, artist, artistorg, id` (+ `org`); mode_ext = `column, bar_begin`; time item = `beat, bpm`; note item = `beat, endbeat, column, sound, vol, type, offset`.

### `time` (tempo list)

`[{"beat":[0,0,1],"bpm":170.0}, {"beat":[34,0,4],"bpm":85.0}, ...]`. The first entry is at `[0,0,1]`; key order in the object varies between files. Optional `sign` (time signature numerator, ROX default 4; ROX writes it only when != 4). Negative BPM is not documented here.

### `effect`

Optional. Key mode: scroll-speed changes, `{"beat":[b,n,d],"scroll":1.5}` (as read by osu2mc and ROX). The samples have `"effect": []`. Taiko mode (from `mc2tja` sample `KappaSays.mc` and its reader): items `{"beat":..., "sign":5}` (bar length), `"showbar": bool`, `"hs": 1.2` (scroll speed), `"ggt": 0|1` (go-go time). The Editor Plugin API names the effect types `sv`, `hs`, `jump` (`AddEffect(beat, type, val)`); how `sv`/`jump` serialize in JSON is Unknown.

### `extra`

Editor state, e.g. `{"test":{"divide":4,"speed":100,"save":0,"lock":0,"edit_mode":0}}` (all 10 samples; osu2mc writes the same block). Ignorable. The Plugin API also has custom key-values (`ReadChartCustom`, 6.6.22+); their location in the JSON is Unknown.

## Timing model

- A position is a beat triple `[i, n, d]` meaning `i + n/d` beats. `i` is the integer beat count from the chart start (quarter-note beat, not the bar index), `n/d` the fraction within that beat (`d` may be 1, 2, 3, 4, 6, 8, 12, 16, 288...). malody-convert converts with `bar = beats // 4` and ROX's `beat_to_f64` is `b[0] + b[1]/b[2]`. Notes can sit on arbitrary fractions, so there is no grid limit. `n` can exceed `d` ("overflow", e.g. `[13,4,4]`) and negative `n`/`d` occur in the wild (malody-convert normalises them).
- Time of a beat `B`: find the last `time` entry with `beat <= B`; `t = t_entry + (B - beat_entry) * 60000 / bpm_entry` ms, with `t_entry` accumulated from the previous entries the same way. Time 0 of the tempo map is the audio-start reference (see offset below).
- Audio offset: the `type:1` entry of `note` carries `offset` (ms) for the audio file. ROX computes `t_beat0 = -offset` (starting the first section at `-offset` ms) and sets `audio_offset_us = -offset * 1000`. malody-convert computes `song.offset = seconds_at(beat of the sound entry) + offset/1000` for `.sm`. Sample values: `342`, `65`, `66`.
- Time signature: only `sign` (ROX) / Taiko `effect.sign`; Key-mode beat triples count quarter beats, so measures are implied (4 beats by default).
- Scroll velocity: `effect[].scroll` (Key).

## Notes

`note` is an array mixing real notes and special entries.

### Key mode (mode 0) and Ring mode (mode 6)

| Entry | Fields | Meaning |
| --- | --- | --- |
| Tap | `beat`, `column` | `column` is 0-based from the left (Key). |
| Hold | `beat`, `endbeat`, `column` | `endbeat` = release beat. |
| Audio entry | `beat` (usually `[0,0,1]`), `sound`, `vol`, `offset`, `type: 1` | Background music: file name, volume (100), offset in ms. `type` is absent (0) on playable notes. |
| Keysound | tap/hold with extra `sound` (file) and `vol`, maybe `type: 0` | per-note hit sound (osu2mc writes `sound`/`vol` on notes). A note with `sound` but no `column` is a background keysound event (malody-convert: "if 'sound' in event: audio event (may be keysounded)"). |

Samples: 4K: 1944 taps + 720 holds etc. The audio entry is stored last in the array (osu2mc appends it at the end; mc2tja splices out all `type == 1` entries). The game ignores notes whose `column >= mode_ext.column` (malody-convert). In every sample all notes have exactly `beat`+`column` (+`endbeat`), plus one audio entry per file.

Ring mode (6): same JSON shape as Key (`beat`, optional `endbeat`, `column`, with `mode_ext.column = 8`), verified on the two samples. The meaning/order of the column index on the ring is Unknown.

### Taiko mode (mode 5; from mc2tja)

`{"beat":[2,0,288],"style":1}`; `style` 0..3. mc2tja's `getNumFromNoteStyle` maps style 0 to TJA note `1`, style 1 to `3`, style 2 to `2`, style 3 to `4` (TJA: 1 = don, 2 = ka, 3 = big don, 4 = big ka), so Malody styles are probably don / big don / ka / big ka [inference from the TJA mapping]. `endbeat` makes a drum-roll (mc2tja ends it with TJA `8`); an optional `hits` field is the balloon hit count (pushed into TJA `BALLOON:`). Uses `meta.mode_ext.bar_begin` and `effect` items (`sign`, `showbar`, `hs`, `ggt`). Beat denominators up to 288 occur in the sample.

### Catch (3), Pad (4), Slide (7), Live (8), Cube (9)

No public chart-format document was found. The Editor Plugin API (Mugzone/Documents) lists the editor-side note model: note types (`Normal=1`, Catch rain `=8`, Hold `=128`, Wipe `=1024`, Slide `=2048`, Live flick `=16384`), per-note `X` (horizontal unit), `Width`, `Flag` (arrow direction: none 0, flick 1, right 2, up 4, left 8, down 16, own direction 32), `Group`, and Slide body segments (beat offset from head + x offset). The JSON key names for these (e.g. `x`, `w`, `seg`) are Unknown; no consulted source verifies them. Inspect real files to find them.

Mode summary from the official descriptions (Moegirlpedia, Apple Store): Catch = osu!catch-like catcher, normal + "rain" bonus notes; Pad = jubeat-like grid; Ring = 6 judgement points + 2 spawners (mobile; 8 spawn columns in the files); Slide = free-width slides; Live and Cube are newer (Malody V).

## Audio & images
Audio: `sound` of the `type:1` entry (same folder/package, often `.ogg`), volume `vol`. Background `meta.background`, video `meta.video`, preview `meta.preview` ms. Per-note `sound` references keysound files in the chart folder.

## Versions & variants
- `$ver` (0 seen) in recent files; absent in older ones (2017 samples).
- Malody 4.x has the older Step/DJ modes (`.sm`, BMS-style); Malody V (5.x/6.x) adds Live, Cube and editor plugins.
- Third-party writers differ in `meta`: ROX writes `id`, `cover`, `time` as empty/0 and `song.org` etc.

## Quirks & pitfalls
- The first beat component is a beat count, not a measure number.
- Notes can be out of order (the audio entry is often last); sort by beat.
- Key order inside objects varies (`bpm` before/after `beat`).
- Ignore notes with `column >= column count`.
- `n`/`d` can be negative or overflow.
- Hold end may equal or precede the start in broken charts (ROX clamps duration to at least 1 µs).
- Ring (mode 6): `column` is an index on the ring (6 judgement points + 2 spawners per Moegirlpedia), not a screen lane.
- `bpm` can be a long float (109.99346569090918). Strings are plain UTF-8, non-Latin titles are common.

## Example

From the repo sample `samples/1557200618.mc` (Key, 5 columns), shortened:

```json
{"meta":{"$ver":0,"creator":"kuma224","background":"tmp.jpg","version":"5k lv25 hard","preview":117,"id":40914,"mode":0,"time":1557513607,"song":{"title":"She is my wife","artist":"SUPER STAR 滿-MITSURU-","id":2455},"mode_ext":{"column":5}},
 "time":[{"beat":[0,0,1],"bpm":170.0},{"beat":[34,0,4],"bpm":85.0}],
 "effect":[],
 "note":[{"beat":[2,0,4],"column":0},{"beat":[2,0,4],"column":2},
         {"beat":[17,3,8],"endbeat":[21,0,8],"column":0},
         {"beat":[0,0,1],"sound":"1487346597.ogg","vol":100,"offset":342,"type":1}]}
```

## ROX support
ROX source `src/formats/mc/{types,decoder,encoder}.rs`.
- Decoder (`McDecoder`, extension `mc`): requires `meta.mode == 0` ("Malody mode N is not supported (only Key mode=0)"); errors if `time` is empty. `key_count = mode_ext.column`. Title/artist prefer `titleorg`/`artistorg`; `version` -> difficulty name; `preview` ms -> µs. Audio comes from the last note with `type != 0` (`sound`, `offset`; `audio_offset_us = -offset * 1000`). Beats -> ms via a tempo timeline starting at `-offset`; `BPM` points get `sign` (default 4). `effect[].scroll` -> SV points. `endbeat` -> Hold (duration >= 1 µs), else Tap.
- Ignored: note keysounds (`sound`, `vol`), `meta.video`, `mode_ext.bar_begin`; negative/overflow beats are not specially handled (`beat: [i32;3]`).
- Encoder: writes mode 0 as pretty JSON; first `note` entry is the audio entry (`type:1`, beat `[0,0,1]`); `sign` only when != 4; `effect` scroll. Rational beats use denominator 60,000,000,000.
- Not supported: Catch/Pad/Taiko/Ring/Slide/Live modes (Ring `mode_ext.column=8` files are refused because mode != 0), `video`, per-note keysounds.

## Parsers & tools

- malody-convert (Python; Key mode to `.sm`): https://github.com/kangalioo/malody-convert/blob/094f81168ef0b7bc4598db53931d3fe0b11031c4/chart.py
- osu2mc (Python; read + write Key mode): https://github.com/deraium/osu2mc/blob/master/mc.py
- mc2tja (JavaScript; Taiko mode to TJA): https://github.com/LuiCat/mc2tja
- malody2osu (Python; Key mode to osu!mania): https://github.com/Jakads/malody2osu
- MorePracticeMalodyServer (C#; reads `.mc` meta inside the zip): https://github.com/RhythmCodec/MorePracticeMalodyServer
- malody-scrape (scraper): https://github.com/kangalioo/malody-scrape
- rmstZ (JavaScript web converter, reads/writes mc incl. Slide mode): https://lrfasd.github.io/rmstZ/
- Malody Creative / mce (Cryville, .mc editor): https://www.cryville.world/Projects/A007
- Official: Malody Store API: https://github.com/Mugzone/Malody_Store_API, editor plugin docs: https://github.com/Mugzone/Documents

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: Malody downloads charts from its store as `.mcz` (see the Packages section of the root README). The store protocol is in https://github.com/Mugzone/Malody_Store_API (`/api/store/download` returns file URLs and MD5s; it needs a client `uid`/`key`, the plain website host answered with HTML). kangalioo's "Malody Converts" packs on the EtternaOnline forum (4K-10K, 280 MB-1 GB each) are Etterna conversions, `.sm` not `.mc` [inference]. No sample exists for Catch 3, Pad 4, Slide 7, Live 8, Cube 9: install Malody, switch the store to that mode and download a chart, or make one in the editor. Searching GitHub for `"mode_ext"` / `"column"` `.mc` files finds converters' test charts.

## Sources

- https://github.com/Mugzone/Malody_Store_API (mode definition table)
- https://github.com/Mugzone/Documents (Creator/Editor/Editor Plugin API.md: enums for mode, NoteType, NoteFlag)
- https://github.com/kangalioo/malody-convert (chart.py)
- https://github.com/deraium/osu2mc (mc.py)
- https://github.com/LuiCat/mc2tja (js/mc2tja.js, js/mcreader.js, chart/KappaSays.mc)
- https://github.com/Jakads/malody2osu (convert.py)
- https://github.com/RhythmCodec/MorePracticeMalodyServer (Model/FileModel/McFile.cs)
- https://forums.etternaonline.com/t/malody-converts-packs-releases-everything-from-4k-to-10k-over-ten-thousand-charts/893
- https://m.mugzone.net/page/175 (FAQ: supported formats)
- ROX source: src/formats/mc/
- Repo samples: vsrg/malody/mc/samples/
