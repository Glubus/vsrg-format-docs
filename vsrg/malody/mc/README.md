# Malody chart (`.mc`)
Kind: chart

Doc status: partial · ROX: reads/writes (Key mode, `meta.mode == 0`, only) · Category: vsrg · Encoding: json

## Overview

`.mc` is the chart format of **Malody** / **Malody V** (Mugzone, a Chinese volunteer team; Malody has existed since 2014, first with Key mode only). One JSON file holds exactly one difficulty of one game mode. The same container is used by every Malody mode (Key, Catch, Pad, Taiko, Ring, Slide, Live, Cube); only `meta.mode`, `meta.mode_ext`, and the per-note fields change. Files are produced by the in-game editor, downloaded from the Malody chart store (the game saves them inside an `.mcz` package, see [../mcz/](../mcz/README.md)), or written by converters (osu2mc, rmstZ...).

Category: **vsrg**. The Key mode (4K–9K, up to 10K by editing) is a classic fixed-column vertical-scroll game, and it is the overwhelming majority of the charts (kangalioo scraped >10,000 4K and >1,000 5K–10K charts). The other modes (Catch = osu!catch-like, Pad = jubeat-like grid, Taiko, Ring = circular, Slide = free x-position slides, Live, Cube) are not column-based; they share this file's container and are documented here, but would be "others" if they had their own folder. The Ring sample in this repo (mode 6, 8 columns, holds) is column/index based but plays on a circle.

Mode numbers (this is the `meta.mode` value; they also appear as "Mode definition" in the official Store API, and the editor plugin API lists the same table):

| `meta.mode` | Mode | Evidence |
| --- | --- | --- |
| 0 | Key | Store API, Editor Plugin API, samples |
| 3 | Catch | Store API, Editor Plugin API |
| 4 | Pad | Store API, Editor Plugin API |
| 5 | Taiko | Store API, Editor Plugin API; `mc2tja` sample file has `"mode": 5` |
| 6 | **Ring** | Store API, Editor Plugin API; the repo samples `1543393546.mc` / `1549455608.mc` have `"mode": 6`, `mode_ext.column = 8`, hold notes (`endbeat`) |
| 7 | Slide | Store API, Editor Plugin API |
| 8 | Live | Store API |
| 9 | Cube | Editor Plugin API only (not in the Store API table) |
| 1, 2 | Step (`.sm`-like) and DJ (`.bms`-like) in the older Malody (the Malody FAQ lists "Key/Step" for `.sm` and "Key/DJ" for bms/pms) | The ids 1 and 2 for them are an [inference] from the gap in the numbering; no source states the numbers. |

In the samples: `vsrg/malody/mc/samples/` contains 8 Key-mode files (mode 0; 4 or 5 columns) and 2 Ring-mode files (mode 6; 8 columns), i.e. **mode 6 = Ring**.

## Packaged in

- Packaged in [`mcz`](../mcz/).

## Container & encoding

- JSON, UTF-8. Some files begin with a UTF-8 BOM (`EF BB BF`): the MorePractice server strips 3 bytes before JSON-parsing the `.mc` it reads from a zip; malody-convert opens with default `json.load`. A robust parser should skip a BOM. The repo's samples have no BOM (they start with `{`). Both pretty-printed (4 spaces) and single-line (e.g. sample `1557200618.mc`) files exist.
- One file = one chart (one mode, one difficulty). File name in the store packages is typically `<chart id>.mc` (the samples are named by a Unix timestamp such as `1487327905.mc`).
- Top-level keys: `meta`, `time`, `note`, optionally `effect`, and `extra` (editor state). Unknown keys exist and must be tolerated (malody-convert refuses unknown meta keys by design as a safety check; its allow-list is below).

## Structure / metadata

```
{ "meta": {...}, "time": [...], "effect": [...], "note": [...], "extra": {...} }
```

### `meta`

| Field | Type | Meaning / notes |
| --- | --- | --- |
| `$ver` | int | Chart format version; only seen as `0` in the sample `1557200618.mc`, absent in older files. Meaning of values other than 0: Unknown. |
| `creator` | string | Chart author (may be empty). |
| `background` | string | Background image file name, relative to the chart folder (e.g. `tmp.jpg`). May be empty. |
| `version` | string | Difficulty name (`"5K NORMALLY Lv.27"`, `"Crazy"`); free text. |
| `preview` | int | Preview start in ms (ROX maps it to `preview_time_us`). Optional. |
| `id` | int | Chart id on the Malody store; 0 for local. |
| `mode` | int | Game mode, see table above. |
| `time` | int | Last modification Unix time (seconds). |
| `song` | object | `title`, `artist`, optional `titleorg` / `artistorg` (original-script names; malody-convert and ROX prefer them), `id` (store song id), optionally `org` object (`title`, `artist`; malody-convert), `source`. |
| `mode_ext` | object | Mode specific. Key/Ring: `column` (key count; observed 4, 5 in Key samples; 8 in Ring samples). Taiko: `bar_begin` (first bar index; mc2tja uses it). `bar_begin` is also written by osu2mc for Key (value 0). |
| `video` | string | Optional video file (malody-convert allow-list). |
| `cover` | string | Written by ROX's encoder; not seen in the samples. |

malody-convert's allow-lists (known fields): meta = `preview, $ver, creator, background, version, id, mode, time, song, mode_ext, video`; song = `title, titleorg, artist, artistorg, id` (+ `org`); mode_ext = `column, bar_begin`; time item = `beat, bpm`; note item = `beat, endbeat, column, sound, vol, type, offset`.

### `time` (tempo list)

`[{"beat":[0,0,1],"bpm":170.0}, {"beat":[34,0,4],"bpm":85.0}, ...]`. First entry is at `[0,0,1]` (key order in the object varies between files). Optional `sign` (time signature numerator, ROX default 4; ROX writes it only when != 4). Negative BPM is not documented here.

### `effect`

Optional. Key mode: scroll-speed changes, `{"beat":[b,n,d],"scroll":1.5}` (as read by osu2mc and ROX). The samples have `"effect": []`. Taiko mode (from `mc2tja` sample `KappaSays.mc` and its reader): items `{"beat":..., "sign":5}` (bar length), `"showbar": bool`, `"hs": 1.2` (scroll speed), `"ggt": 0|1` (go-go time). The Editor Plugin API names the effect types `sv`, `hs`, `jump` (`AddEffect(beat, type, val)`); how `sv`/`jump` serialize in JSON is Unknown.

### `extra`

Editor state, e.g. `{"test":{"divide":4,"speed":100,"save":0,"lock":0,"edit_mode":0}}` (all 10 samples; osu2mc writes this same block). Ignorable. Plugin API also has custom key-values (`ReadChartCustom`, 6.6.22+), location in the JSON Unknown.

## Timing model

- A position is a **beat triple** `[i, n, d]` meaning `i + n/d` beats where `i` is the integer **beat count from the chart start (quarter-note beat, not the bar index)**, `n/d` the fraction within that beat (`d` may be 1, 2, 3, 4, 6, 8, 12, 16, 288...). The task wording "bar" is wrong: malody-convert converts with `bar = beats // 4` and ROX's `beat_to_f64` is `b[0] + b[1]/b[2]`. Because notes can be on arbitrary fractions, there is no grid limit. `n` can exceed `d` ("overflow", e.g. `[13,4,4]`) and negative `n`/`d` occur in the wild (malody-convert normalises them).
- Time of a beat `B`: find the last `time` entry with `beat <= B`; `t = t_entry + (B - beat_entry) * 60000 / bpm_entry` ms, with `t_entry` accumulated from the previous entries the same way. Time 0 of the tempo map is the **audio-start** reference (see offset below).
- Audio offset: the `type:1` entry of `note` carries `offset` (ms) for the audio file. ROX computes `t_beat0 = -offset` (starting the first section at `-offset` ms) and sets `audio_offset_us = -offset * 1000`. malody-convert instead computes `song.offset = seconds_at(beat of the sound entry) + offset/1000` for `.sm`. Sample values: `342`, `65`, `66`.
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
| Keysound | tap/hold with extra `sound` (file) and `vol`, maybe `type: 0` | per-note hit sound (osu2mc writes `sound`/`vol` on notes). A note that has `sound` but no `column` is a background keysound event (malody-convert: "if 'sound' in event: audio event (may be keysounded)"). |

Notes in the samples: 4K: 1944 taps + 720 holds etc; the audio entry is stored **last** in the array (osu2mc appends it at the end; the sample files show it last; mc2tja splices out all `type == 1` entries). Notes whose `column >= mode_ext.column` are ignored by the game (malody-convert). Hold-only/tap-only counts for each sample were verified: all notes have exactly `beat`+`column` (+`endbeat`), plus one audio entry per file.

Ring mode (6): same JSON shape as Key (`beat`, optional `endbeat`, `column`, with `mode_ext.column = 8`), verified on the two samples. The meaning/order of the column index on the ring is Unknown.

### Taiko mode (mode 5; from mc2tja)

`{"beat":[2,0,288],"style":1}`; `style` 0..3. mc2tja's `getNumFromNoteStyle` maps style 0 to TJA note `1`, style 1 to `3`, style 2 to `2`, style 3 to `4` (TJA: 1 = don, 2 = ka, 3 = big don, 4 = big ka), i.e. Malody styles are probably don / big don / ka / big ka [inference from the TJA mapping]. `endbeat` makes a drum-roll (mc2tja ends it with TJA `8`); an optional `hits` field is the balloon hit count (pushed into TJA `BALLOON:`). Uses `meta.mode_ext.bar_begin` and `effect` items (`sign`, `showbar`, `hs`, `ggt`). Beat denominators up to 288 occur in the sample.

### Catch (3), Pad (4), Slide (7), Live (8), Cube (9)

No public chart-format document was found. What is verifiable: the Editor Plugin API (Mugzone/Documents) lists the editor-side note model: note types (`Normal=1`, Catch rain `=8`, Hold `=128`, Wipe `=1024`, Slide `=2048`, Live flick `=16384`), per-note `X` (horizontal unit), `Width`, `Flag` (arrow direction: none 0, flick 1, right 2, up 4, left 8, down 16, own direction 32), `Group`, and Slide **body segments** (beat offset from head + x offset). The JSON key names for these (e.g. `x`, `w`, `seg`) are **Unknown** here: not verified in any source consulted. A parser needing them must inspect real files.

Mode summary from the official descriptions (Moegirlpedia, Apple Store): Catch = osu!catch-like catcher, normal + "rain" bonus notes; Pad = jubeat-like grid; Ring = 6 judgement points + 2 spawners (mobile; 8 spawn columns in the files); Slide = free-width slides; Live and Cube are newer (Malody V).

## Audio & images

- Audio: the `type:1` entry's `sound` (file name in the same folder/package, often `.ogg`). `vol` is its volume.
- Background: `meta.background` (image file). Video: `meta.video` (optional). Preview: `meta.preview` ms.
- Keysound files: `sound` on individual notes, referencing files in the chart folder.

## Versions & variants

- `$ver` (0 seen) in recent files; absent in older ones (samples from 2017 lack it).
- Malody (4.x) vs Malody V (5.x/6.x): V adds Live and Cube modes and editor plugins; older Step/DJ modes (`.sm` and BMS-style) exist in Malody 4.
- Third-party writers (osu2mc, ROX, rmstZ) emit slightly different `meta`: ROX writes `id`, `cover`, `time` as empty/0 and `song.org` etc.

## Quirks & pitfalls

- First beat component is a beat count, not a measure number.
- Notes can be out of order; the audio entry is often last; sort by beat.
- Key order inside objects is not stable (`bpm` before/after `beat`).
- Notes with `column >= column count` must be ignored.
- Negative or overflowing `n`/`d` triples.
- Hold end may equal or precede the start in broken charts (ROX clamps duration to at least 1 µs).
- Strings are plain UTF-8 (non-Latin titles are common); no legacy code pages.
- Ring (mode 6) samples use 8 columns; Moegirlpedia describes the mode as 6 judgement points and 2 spawners, so `column` is an index, not a screen lane.
- `bpm` can be float with long fraction (109.99346569090918).

## Example

Taken from the repo sample `samples/1557200618.mc` (Key, 5 columns), shortened:

```json
{"meta":{"$ver":0,"creator":"kuma224","background":"tmp.jpg","version":"5k lv25 hard","preview":117,"id":40914,"mode":0,"time":1557513607,"song":{"title":"She is my wife","artist":"SUPER STAR 滿-MITSURU-","id":2455},"mode_ext":{"column":5}},
 "time":[{"beat":[0,0,1],"bpm":170.0},{"beat":[34,0,4],"bpm":85.0}],
 "effect":[],
 "note":[{"beat":[2,0,4],"column":0},{"beat":[2,0,4],"column":2},
         {"beat":[17,3,8],"endbeat":[21,0,8],"column":0},
         {"beat":[0,0,1],"sound":"1487346597.ogg","vol":100,"offset":342,"type":1}]}
```

## ROX support

ROX source: `src/formats/mc/{types,decoder,encoder}.rs`.
- Decoder (`McDecoder`, extension `mc`): requires `meta.mode == 0`, errors otherwise ("Malody mode N is not supported (only Key mode=0)"); errors if `time` is empty. Builds RoxChart with `key_count = mode_ext.column`. Metadata: title/artist = `titleorg`/`artistorg` if present else `title`/`artist`; creator, `version` -> difficulty name, `background`, `preview` ms -> µs. Audio: scans notes with `type != 0`, uses the last `sound` and `offset` (`audio_offset_us = -offset * 1000`). Beats -> ms through a tempo timeline starting at `-offset`; `BPM` points get `sign` (default 4). `effect[].scroll` -> SV points. `endbeat` present -> Hold (duration >= 1 µs) else Tap. Keysounds on notes (`sound`, `vol`) and `meta.video`, `mode_ext.bar_begin`, negative/overflow beats are not specially handled (`beat: [i32;3]`).
- Encoder: writes mode 0 as pretty JSON; the first `note` entry is the audio entry (`type:1`, beat `[0,0,1]`), then notes; tempo list with `sign` (only when != 4), `effect` scroll, notes. Rational beats use denominator 60,000,000,000.
- Not supported: Catch/Pad/Taiko/Ring/Slide/Live modes (Ring 6-key `mode_ext.column=8` files are refused because mode != 0, even though the JSON shape would fit), `video`, per-note keysounds.

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
