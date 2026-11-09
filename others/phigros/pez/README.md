# Phira / PhiZone chart package (`.pez`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive

## Overview

`.pez` is the chart package consumed by **prpr / Phira** (and distributed through PhiZone): a zip archive holding a chart file (RPE JSON, official JSON or PEC), the music, the illustration and a metadata file. prpr's README states a `.pez` file is recognised and an unzipped folder is accepted too. Format details beyond the README were not found.

## Contents

- A ZIP with a chart file, the music, the illustration and a metadata file.
- Chart format inside: [RPE JSON](../rpe/README.md), [official JSON](../official-json/README.md) or [PEC](../pec/README.md).

## Container & encoding

Zip archive (or the same files in a folder). Metadata file: `info.yml` (preferred) or legacy `info.txt` / `info.csv`; if `info.yml` exists the other two are ignored.

## Structure / metadata

`info.yml` keys (from the prpr README; defaults in parentheses): `id`, `name` ('UK'), `difficulty` (float, 10), `level` ('UK Lv.?'), `charter`, `composer`, `illustrator`, `chart` (path, 'chart.json'), `format` ('rpe'; available `rpe`, `pgr`, `pec`), `music` ('music.mp3'), `illustration` ('background.png'), `previewTime` (float, 0), `aspectRatio` (16/9), `lineLength` (half judgement-line length, 6), `tip`, `intro`, `tags`. Phira's chart-standard index also lists a "PBC" format with documentation pending.

## Timing model

Determined by the contained chart (`../rpe/`, `../official-json/`, `../pec/`).

## Notes

Not applicable (the package holds charts).

## Audio & images

Referenced by `music` and `illustration` keys, relative to the package root.

## Versions & variants

`format: pgr` denotes the official Phigros JSON (`../official-json/`).

## Quirks & pitfalls

The chart file's extension is ignored by Phira; format detection uses `info.yml` `format` or the file contents.

## Example

Not applicable (no example read).

## ROX support

Not read by ROX.

## Parsers & tools

prpr / Phira (Rust): <https://github.com/Mivik/prpr>, <https://github.com/TeamFlos/phira>. Third-party converter osz -> pez: <https://github.com/AkiraNyx/osz2pez> (appeared in search results, not inspected).

## Getting samples

- Container only: this folder holds no archive. A `.pez` is a zip with the chart (RPE `chart.json`, or official/PEC format), `info.yml`/`info.txt`, music and illustration. Layout observed in real packages downloaded from the Phira API: chart file named in `info.yml` (`chart:`), `info.yml`, `info.txt`, music (`.mp3`/`.ogg`), illustration, sometimes extra files (`extra.json`, `.glsl`).
- The real charts extracted from Phira packages are committed in [../rpe/samples/](../rpe/samples/) (`phira_<id>.json`; see its SOURCES.md for the source URLs).
- More: Phira's public API (`https://api.phira.cn/chart?page=1&pageNum=N&order=-updated`, observed 2026-11-09) lists charts with a `file` URL pointing to the `.pez`; packages are exported from Re:PhiEdit or built by tools such as rpechart (`export_pez`).

## Sources

- <https://github.com/Mivik/prpr> (README)
- <https://github.com/TeamFlos/phira-docs/blob/main/src/chart-standard/chart-format/index.md>
