# DTXMania `set.def`
Kind: metadata

Doc status: complete · ROX: no (Prism lists every `.dtx` and does not read `set.def`) · Category: vsrg · Encoding: text (Shift_JIS or UTF-8)

## Overview
Text file named `set.def` placed next to chart files; DTXMania then ignores the individual chart files in that folder and lists only the charts in `set.def`, grouped as one song with several difficulties. Per the official documentation https://dtxmania.net/documents/create-setdef.

## Container & encoding
Text, Shift_JIS or UTF-8; BMS-like `#KEY: value` lines. One folder = one `set.def`; may describe several songs.

## Structure / metadata
`#TITLE` starts a song block (a new `#TITLE` begins the next song in the same file). Keys:

| Key | Content |
|---|---|
| `#TITLE:` | song title |
| `#FONTCOLOR:` | text colour, e.g. `#FFFFFF` (listed as unsupported by current DTXMania in the doc) |
| `#L1LABEL:` .. `#L5LABEL:` | difficulty label; defaults BASIC, ADVANCED, EXTREME, MASTER, ULTIMATE (the doc table spells L4's key `#L4LABLE`/ `#L4LABEL`) |
| `#L1FILE:` .. `#L5FILE:` | chart file, relative to the set.def folder (backslash paths seen, e.g. `ps2\initD_PS2_bas.dtx`) |

n = 1..5 map to the difficulty list bottom to top (n=1 lowest, by convention). Not all five are required.

## Timing model / Notes / Audio & images
Not applicable (indexing only).

## Versions & variants
[observed in samples/*_set.def, *_SET.DEF] Real files from community packs: CRLF; ASCII or Shift_JIS (Japanese titles: `SGURU.J_Drum9th-helicopter_set.def`, `wes_Spitz---haru_no_uta_set.def`); the file name may be upper case (`SET.DEF`); the colon after the key is optional and spaces around it vary (`#TITLE Blue Water Blue Sky` in `XtrRyce_blue_SET.DEF`, `#TITLE : LIBERTY` / `#L1FILE : LIBERTY.dtx` in `takky_liberty_set.def`, `#L1LABEL:BASIC` without a space in `goro-j_Drum8th-Dreams_in_the_night_set.def`); the last line may lack a final newline; `#LnFILE` may name `.gda` charts (`TEKKI_Momentary-Life_SET.DEF`: `bas.gda`, `adv.gda`, `ext.gda`; `SGURU.J_...`: `heriBSC.GDA`) as well as `.dtx`; a pack may hold only one level (`XtrRyce_blue_SET.DEF`).

## Quirks & pitfalls
When a `set.def` exists, loose `.dtx` files in the folder are ignored.

## Example
From the official doc (verbatim):
```
#TITLE: OMENS OF LOVE

#L1LABEL: Basic
#L1FILE: omensoflove_bas.dtx

#L2LABEL: Advanced
#L2FILE: omensoflove_adv.dtx

#L3LABEL: Extreme
#L3FILE: omensoflove_ext.dtx
```

## ROX support
Not read by ROX. Prism does not read it either: `set.def` is never listed as a chart, every `.dtx` of a folder is listed (DTXMania lists only the ones the `set.def` names), and the titles and difficulty labels of a `set.def` are not used.

## Parsers & tools
DTXMania (C#): https://github.com/limyz/DTXmaniaNX

## Getting samples
- **Committed** ([`samples/`](samples/SOURCES.md)): 15 real `set.def` files from community DTX/GDA packs of the archive.org item "Rare DTX&GDA Simfile Collection" (`raredtxgda`, `raredtxgda2`: TEKKI, XtrRyce, ウェス, さわね, リバドラ, goro-j, Ｍ田, SGURU.J, takky, Deathfox), each extracted from its pack's RAR (only the `set.def` kept), plus three hand-written `synthetic-*.def` files (single song, two songs, Shift_JIS).
- **More**: the same two archive.org items hold hundreds of packs (`https://archive.org/details/raredtxgda`, `https://archive.org/details/raredtxgda2`; RAR archives per charter, so download one and extract with `bsdtar`/`7z`); 64 `set.def` were counted in the ~95 smaller packs that were listed. The official documentation (https://dtxmania.net/documents/create-setdef) describes the keys; `woopsdez/dtx-syrup` generates `set.def` files.

## Sources
- https://dtxmania.net/documents/create-setdef
