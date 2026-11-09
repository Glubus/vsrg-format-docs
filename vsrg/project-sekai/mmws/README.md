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

- Committed / manifest: none. No `.mmws` file exists in any of the MikuMikuWorld repositories checked (Eyelove3rd, serseraph, vewaxio, Choccodrize, GuanYixuan forks: no `.mmws` in their trees; crash5band/MikuMikuWorld and sevenc-nanashi/MikuMikuWorld4CC were not retrievable anonymously from here). A binary file cannot be hand-written safely without a verified decoder.
- How to get one: install MikuMikuWorld (https://github.com/crash5band/MikuMikuWorld releases), create a chart (or open a `.sus`) and use File > Save: it writes `.mmws`. Community charts are shared as `.mmws` in the Untitled Sekai / Chart Cyanvas Discord communities and on their sites (check the author's licence). rg_converters lists `.mmws/.ccmmws/.unchmmws` as fully supported (read and write) in its README, so it can convert SUS/USC to `.mmws`.

## Sources

- <https://github.com/UntitledCharts/rg_converters>
- <https://sekai-guide.tootiejin.com/getting-started/usage-guide-mmw4cc> (listed in search)
