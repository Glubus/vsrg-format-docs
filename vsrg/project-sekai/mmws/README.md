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

- Committed in [`samples/`](samples/): 5 `rgconv_*.mmws` files, produced by rg-converters (`mmw.mmws.export`) from real official/engine charts. **They are converted, not downloaded**: no `.mmws` file is published anywhere I could reach (checked the MikuMikuWorld fork repos, the Chart Cyanvas and Untitled Charts tooling). Everything is listed with origin, date and sha256 in [`samples/SOURCES.md`](samples/SOURCES.md).
- Observed [observed in samples/rgconv_sekaibest_0001_01_easy.mmws]: file starts with the magic `MMWS` followed by `00 04 00 00 00` ...
- How to get a native one: install MikuMikuWorld (crash5band) or a fork, open a `.sus` and File > Save.

## Sources

- <https://github.com/UntitledCharts/rg_converters>
- <https://sekai-guide.tootiejin.com/getting-started/usage-guide-mmw4cc> (listed in search)
