# Cytoid level package (`.cytoidlevel`)
Kind: package

Doc status: partial · ROX: no · Category: others · Encoding: archive

## Overview

A Cytoid level is custom gameplay content (music, background, info, charts) archived into a `.cytoidlevel` file; Cytoid imports these automatically. Per the Cytoid wiki it is "similar to `.osz`": it is simply a `.zip` with the extension changed. A level must contain a music file, a background image, at least one chart text file and a `level.json`. Levels are shared on CytoidDB (cytoid.io).

## Contents

- A ZIP with a music file, a background, `level.json` and at least one chart text file.
- Chart formats inside: [`c1` text](../c1-txt/README.md) or [`c2` JSON](../c2-json/README.md) (the version is not stated here).

## Container & encoding

Zip archive whose files are at the archive root (do not zip the enclosing folder). File names are free; relative paths in `level.json` locate them. Music: `.mp3` or `.ogg` (`.ogg` recommended; keep < 3 MB; a 30 s preview < 500 KB is strongly recommended). Background: `.jpg` / `.png` (jpg < 2 MB, > 1920x1080 preferred). Charts: `.txt` in the Cytus "Rayark v2 modified" format (`../c1-txt/`); newer Cytoid also reads JSON C2 charts (`../c2-json/`).

## Structure / metadata

`level.json` (from the Cytoid wiki sample):

| Field | Meaning |
|---|---|
| `version` | integer level version (starts at 1) |
| `id` | unique id; only `a-z`, `0-9`, `.`, `_`; required for uploading (e.g. `decnoe.hopes_and_dreams`) |
| `title`, `artist`, `illustrator`, `charter` | credits |
| `music.path`, `music_preview.path`, `background.path` | relative paths |
| `charts[]` | 1 to 3 charts: `type` (`easy`, `hard`, `extreme`), `difficulty` (integer, may exceed 9), `path` (chart file), optional `music_override.path` (alternate music for this difficulty) |

## Timing model

Defined by the chart files.

## Notes

Not applicable.

## Audio & images

As listed above; per-chart `music_override`.

## Versions & variants

`level.json` `version` int; newer Cytoid versions (the newer Cytoid wiki's cytoidlevel page is a WIP stub) may add fields not covered by this 2017-era wiki page.

## Quirks & pitfalls

Unknown.

## Example

From the Cytoid wiki (shortened):

```json
{"version":1,"id":"decnoe.hopes_and_dreams","title":"Hopes and Dreams","artist":"Toby Fox",
 "illustrator":"masyu_0331","charter":"Decnoe",
 "music":{"path":"Hopes and Dreams.mp3"},"music_preview":{"path":"preview.mp3"},"background":{"path":"background.jpg"},
 "charts":[{"type":"easy","difficulty":8,"path":"chart.easy.txt"}]}
```

## ROX support

Not read by ROX.

## Parsers & tools

Cytoid (C#, Unity): <https://github.com/Cytoid/Cytoid>; PCtyx can generate `level.json`; Cytoid Chart Editor: <https://github.com/CatalinTermure/Cytoid-Chart-Editor>; CytoidDB: <https://cytoid.io>.

## Sources

- <https://raw.githubusercontent.com/wiki/Cytoid/Cytoid/a.-Creating-a-level.md>
- <https://cytoid.wiki/en/reference/chart/cytoidlevel> (WIP stub)
