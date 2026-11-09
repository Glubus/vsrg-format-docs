# AAR / ALAR archives (`.aar`, Groove Coaster)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive (container; chart payload format unknown)

## Overview
Groove Coaster for Steam (and the arcade/Switch builds, with differences) stores most files, including the charts, in `.aar` archives. Per the Steam discussion thread (via search result) and the Mod The Coaster README they are ALAR archives, sometimes compressed with ALLZ ("Aqualead LZSS") or both layers. New songs mostly add "Stage" files (music and chart scripts) and update the song list (`TableTune`). No chart-script layout was found in any source opened.

## Container & encoding
- `.aar` = ALAR archive; an uncompressed one starts with `ALAR`, a compressed one with `ALLZ` (decompress with Brolijah's Aqualead LZSS Decoder). README example: uncompressed `TableTune.aar` 392 KB, compressed 112 KB.
- Audio is `.asn`: an `.ogg` file with a 32-byte header ("ST will accept standard `.ogg` the same as `.asn`"); the Mod The Coaster "ASN Snip" tool trims the header.
- The ALAR layout ("documented for years, quickbms script exists") is not reproduced in the sources opened.
- The old mobile game's server data used encrypted request fields (Groove_Coaster_2_Server repo); irrelevant to chart files.

## Structure / metadata
Unknown. The song list/difficulty assignment lives in `TableTune.aar` (re-assigned by "Table Tune" in Mod The Coaster; works only on uncompressed files).

## Timing model

Unknown.

## Notes
Unknown (the game has beat, hold, slide and ad-lib types; encoding undocumented).

## Audio & images
`.asn` (OGG + 32-byte header). Jackets are converted for Switch builds ("Jacket Convert" tool: SW uses a different jacket layout).

## Versions & variants
Platforms: AC (arcade), APP (mobile), ST (Steam), SW (Switch). README tool matrix: ST fully supported, AC partial ("no 4MAX songs"), SW partial ("charts already in AC, no MAS charts").

## Quirks & pitfalls
Check the `ALAR`/`ALLZ` magic before treating a file as an archive; a compressed `TableTune` cannot be edited by Table Tune.

## Example
Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

[nemonaii/Mod-The-Coaster](https://github.com/nemonaii/Mod-The-Coaster) (JS, web), [Brolijah/Aqualead_LZSS](https://github.com/Brolijah/Aqualead_LZSS), [oocyberkevinoo/Groove-Coaster-Converter](https://github.com/oocyberkevinoo/Groove-Coaster-Converter), [Brolijah/groove-coaster-modding](https://github.com/Brolijah/groove-coaster-modding).

## Getting samples
None committed: no `.aar` or chart script is published in any open repository found (Mod-The-Coaster, Brolijah/groove-coaster-modding, Groove-Coaster-Converter and qwerfd2/Groove_Coaster_2_Server hold tools, docs and `.pak` server files only).

To get one: install Groove Coaster for Steam (app 744060) or use arcade/Switch data, decompress ALLZ files with Aqualead_LZSS and unpack the `.aar` with Mod The Coaster (<https://github.com/nemonaii/Mod-The-Coaster>). Brolijah's `ALAR_decode_encode/song .aar file layout.txt` (<https://github.com/Brolijah/groove-coaster-modding>) shows a song archive with, per difficulty, three `.dat` files (`ac_shiva_easy.dat`, `_clip.dat`, `_ext.dat`) plus `.asn` audio; the `.dat` files are presumably the chart scripts [inference]. The mobile game's stage files come as `.pak`/zip from servers such as <https://github.com/qwerfd2/Groove_Coaster_2_Server> (its `various-tools/pak file/` has a packer/unpacker).

## Sources

- <https://raw.githubusercontent.com/nemonaii/Mod-The-Coaster/main/README.md> (read)
- <https://steamcommunity.com/app/744060/discussions/0/2686880925148544980/> (search-result excerpts only)
- <https://github.com/oocyberkevinoo/Groove-Coaster-Converter> (repository page; no format details)
