# MikuMikuWorld score (MMWS) (`.mmws`)
Kind: project

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview

MMWS (also `.ccmmws`, `.unchmmws` for popular MMW forks) is the native score file of the Project SEKAI chart editor MikuMikuWorld (MMW) and its forks (MMW4CC for Chart Cyanvas, Unchmmw). rg_converters lists these as fully supported formats (loaders/exporters credited to YarNix). The binary layout and the `.json` variant were not read.

## Container & encoding

Unknown (binary [inference: not verified]).

## Structure / metadata

Unknown.

## Timing model

Unknown.

## Notes

Unknown.

## Audio & images

Unknown.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

rg_converters (Python/C++): <https://github.com/UntitledCharts/rg_converters>; MMW4CC usage guide: <https://sekai-guide.tootiejin.com/getting-started/usage-guide-mmw4cc>.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). All are converted with rg-converters (`mmw.mmws.export`); no public `.mmws` exists (checked the MikuMikuWorld fork repos, Chart Cyanvas and Untitled Charts tooling).

[observed: rgconv_sekaibest_0001_01_easy.mmws] starts with magic `MMWS` then `00 04 00 00 00` ...

Native file: install MikuMikuWorld (crash5band) or a fork, open a `.sus`, File > Save.

## Sources

- <https://github.com/UntitledCharts/rg_converters>
- <https://sekai-guide.tootiejin.com/getting-started/usage-guide-mmw4cc> (listed in search)
