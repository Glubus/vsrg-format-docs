# Cytus II / Cytoid chart (C2) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview
JSON chart format of Cytus II (Rayark) as used by the fan game Cytoid (the "C2 chart format") and by editors such as PCtyx, Cytoid Chart Editor and Cy2Unity. The Cytoid wiki warns it is written "at Cytoid compatibility; some tools might not be fully supported". Official Cytus II charts are encrypted: a gist describes dumping libil2cpp, extracting the ASSET key and running a decryption script that yields BSON (readable with Json.NET's BsonReader). Fan charts are plain JSON.

## Packaged in
`.cytoidlevel` (zip of a Cytoid level: `level.json`, chart text/JSON files, music, background).

## Container & encoding
UTF-8 JSON, one file per difficulty (`chart.json`, `chart-extreme.json`, ...) referenced by `level.json` inside a `.cytoidlevel` zip (the wiki page for `.cytoidlevel` is a stub). Official game assets: encrypted, BSON-decoded.

## Structure / metadata

Root parameters (Cytoid wiki; the Fizzest guide uses slightly different names such as `start_offset_time`):

| Field | Type | Meaning |
|---|---|---|
| `format_version` | int | not required by Cytoid; the guide says set 0 (needed on Cytus 2 proper) |
| `time_base` | int | ticks per time unit (see Timing) |
| `music_offset` | float (s) | music playing offset (guide: `start_offset_time`, put 0) |
| `size` | float | note size, default 1.0 |
| `ring_color` | hex RGB | ring colour of all notes |
| `fill_colors` | array of hex RGB | `[click 1, click 2, drag 1, drag 2, hold 1, hold 2, long hold 1, long hold 2, flick 1, flick 2]` |
| `opacity` | float | max opacity, default 1.0 |
| `skip_music_on_completion` | bool | |
| `display_boundaries` | bool | draw the scan line boundaries |
| `horizontal_margin`, `vertical_margin` | int 1..5 | |
| `tempo_list` | array | `{tick, value}`: `value` = duration of a beat (time_base) in microseconds, i.e. `60000000 / BPM` for time_base = beat |
| `page_list` | array | `{start_tick, end_tick, scan_line_direction}`; direction `1` up, `-1` down (guide); one entry per page, all must be listed |
| `note_list` | array | notes (below) |
| `event_order_list` | array | `{tick, event_list: [{type, args}]}` : scan-line speed change markers; `type` 0 = faster than before, 1 = slower (guide); `args` `W` back to base speed, `R` faster than base, `G` slower than base |

Note object: `page_index`, `type` (0 Click, 1 Hold, 2 Long Hold, 3 Drag head, 4 Drag child, 5 Flick, 6 C-Drag head, 7 C-Drag child; the guide lists 0..5 only), `id` (unique int), `tick`, `x` (0..1, 0 left), `has_sibling` (bool: another note on the same tick), `hold_tick` (Hold and Long Hold only), `next_id` (Drag/C-Drag chain; `-1` ends the chain; 0 when unused), `is_forward` (bool, meaning not documented).

## Timing model

- Time is in ticks; a note at tick 120 stays there when the BPM changes.
- Pages: a note's tick is `page_index * time_base + alpha`, `start_tick = page*time_base`, `end_tick = (page+1)*time_base` (guide, with `time_base` 480 recommended for 4/4 and 2/4 songs). The Cytoid wiki describes `time_base` as "the length of a beat (in tick)"; the two descriptions differ on the page/beat relation and the sources were not reconciled.
- Tempo: `tempo_list[i].value` microseconds per `time_base` ticks from `tick` onwards, so seconds between two ticks = `dticks * value / time_base / 1e6` summed piecewise. The first entry must be at tick 0. Guide: "time_base = value in microseconds".

## Notes
Click (0), Hold (1) / Long Hold (2, spans pages) with `hold_tick`, Drag chains via `next_id` (head 3, child 4; C-Drag 6/7 use the same links), Flick (5). No keysounds.

## Audio & images
Unknown.

## Versions & variants
C2 replaces the C1 text format (`../c1-txt/`) in Cytoid. Cytus II's own format has more events (not documented in the pages consulted).

## Quirks & pitfalls
- Note ids must be unique; a `page_index` that does not match the tick's page hides the note but it still counts as a miss.
- `next_id` must be `-1` for the last note of a drag, `0` when unused.
- Names differ between guides (`music_offset` vs `start_offset_time`).

## Example

Illustrative, hand-built from the field list above (not from a real level):

```json
{"format_version":0,"time_base":480,"music_offset":0.0,
 "tempo_list":[{"tick":0,"value":500000}],
 "page_list":[{"start_tick":0,"end_tick":480,"scan_line_direction":1},
              {"start_tick":480,"end_tick":960,"scan_line_direction":-1}],
 "note_list":[{"page_index":0,"type":0,"id":0,"tick":240,"x":0.5,"has_sibling":false,"hold_tick":0,"next_id":0,"is_forward":false}],
 "event_order_list":[]}
```
`value` 500000 us per 480 ticks is 120 BPM for a 480-tick beat.

## ROX support

Not read by ROX.

## Parsers & tools

- Cytoid (C#, Unity): <https://github.com/Cytoid/Cytoid>
- Cytoid Chart Editor (C#): <https://github.com/CatalinTermure/Cytoid-Chart-Editor>
- Cy2Unity / PCtyx editors (see Cytoid wiki)
- Cy2Gen (practice chart generator): <https://github.com/davis0178/Cy2Gen>
- Chart decryption notes: <https://gist.github.com/HoLLy-HaCKeR/84bda48aa565c6214d1803a49fd6f5b7>

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: Cytoid levels at https://cytoid.io (`services.cytoid.io/levels` lists them; the package download needs a login or an unknown path, not scraped). The bundled level `8bit_adventurer/` (`ez.txt`, `hd.txt`, `ex.txt`) comes from `io.cytoid.8bit_adventurer.cytoidlevel`. Cytoid Chart Editor and PCtyx write the format.

## Sources

- <https://cytoid.wiki/en/reference/chart/c2-format>
- <https://sites.google.com/site/cytoidcommunity/charting/chart-format/c2-chart-format>
- <https://gist.github.com/HoLLy-HaCKeR/84bda48aa565c6214d1803a49fd6f5b7>
- <https://cytoid.wiki/en/reference/chart/cytoidlevel> (stub page)
