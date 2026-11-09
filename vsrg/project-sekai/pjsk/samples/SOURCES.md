# Samples: PJSK score-maker JSON

## Committed
| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-12lane.pjsk.json` | hand-written for this repository | vsrg-format-docs | CC0 / public domain | `synthetic`, plain JSON (not gzip/base64): BPM change, time-scale, SE volume and `4/4` events; normal and critical taps (lane ranges 0-3 / 4-7), flick, trace (`category 4`), a critical slide chain (`1` start, `2` visible relay, `13` hidden relay, `1` end; ids linked by `previousConnectionId`/`nextConnectionId`), a guide chain (`9` start, `9` end). Field names and `category`/`noteBaseType` pairs copied from the real fixture `empurple_append.pjsk.json` (manifest) and the fiche; not run through any parser. |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `empurple_append.pjsk.json` | https://raw.githubusercontent.com/UntitledCharts/rg_converters/57610afe5cee8e913664ca5f384c82fbd7c8d473/test_files/empurple_append.pjsk.json | Repo GPL-3.0; official chart data, not committed | Real plain-JSON dump, 1004 notes, 6 events, `VersionCode 10000`, `MusicId 0`, 2-space indented, alphabetical-ish key order |

Upstream also has `88s_append.pjsk.json` (932 KB) and `intense_voice_full_append.pjsk.json` (1.2 MB), skipped for size.
