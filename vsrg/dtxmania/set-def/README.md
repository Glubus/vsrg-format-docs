# DTXMania `set.def`
Kind: metadata

Doc status: complete · ROX: no (Prism lists every `.dtx` and does not read `set.def`) · Category: vsrg · Encoding: text (Shift_JIS or UTF-8)

## Overview
Text file named `set.def` placed next to chart files. DTXMania then ignores the individual chart files in that folder and lists only the charts in `set.def`, grouped as one song with several difficulties (https://dtxmania.net/documents/create-setdef).

## Container & encoding
Text, Shift_JIS or UTF-8; BMS-like `#KEY: value` lines. One folder has one `set.def`, which may describe several songs.

## Structure / metadata
`#TITLE` starts a song block; the next `#TITLE` begins the next song in the same file. Keys:

| Key | Content |
|---|---|
| `#TITLE:` | song title |
| `#FONTCOLOR:` | text colour, e.g. `#FFFFFF` (listed as unsupported by current DTXMania in the doc) |
| `#L1LABEL:` .. `#L5LABEL:` | difficulty label; defaults BASIC, ADVANCED, EXTREME, MASTER, ULTIMATE (the doc table spells L4's key `#L4LABLE`/ `#L4LABEL`) |
| `#L1FILE:` .. `#L5FILE:` | chart file, relative to the set.def folder (backslash paths seen, e.g. `ps2\initD_PS2_bas.dtx`) |

n = 1..5 map to the difficulty list bottom to top (n=1 lowest, by convention). Not all five are required.

## Timing model / Notes / Audio & images
Unknown.

## Versions & variants
[observed: *_set.def, *_SET.DEF] Community-pack files: CRLF; ASCII or Shift_JIS (Japanese titles: `SGURU.J_Drum9th-helicopter_set.def`, `wes_Spitz---haru_no_uta_set.def`); the file name may be upper case (`SET.DEF`). The colon after the key is optional and spacing varies (`#TITLE Blue Water Blue Sky` in `XtrRyce_blue_SET.DEF`, `#TITLE : LIBERTY` / `#L1FILE : LIBERTY.dtx` in `takky_liberty_set.def`, `#L1LABEL:BASIC` in `goro-j_Drum8th-Dreams_in_the_night_set.def`). The last line may lack a final newline. `#LnFILE` may name `.gda` charts (`TEKKI_Momentary-Life_SET.DEF`: `bas.gda`, `adv.gda`, `ext.gda`; `SGURU.J_...`: `heriBSC.GDA`) as well as `.dtx`. A pack may hold only one level (`XtrRyce_blue_SET.DEF`).

## Quirks & pitfalls
Loose `.dtx` files in a folder with a `set.def` are ignored.

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
Not read by ROX. `set.def` is never listed as a chart, every `.dtx` of a folder is listed (DTXMania lists only the ones the `set.def` names), and `set.def` titles and difficulty labels are unused.

## Parsers & tools
DTXMania (C#): https://github.com/limyz/DTXmaniaNX

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md).

More: the archive.org items `https://archive.org/details/raredtxgda` and `https://archive.org/details/raredtxgda2` hold hundreds of packs (one RAR per charter, extract with `bsdtar`/`7z`); 64 `set.def` were counted in the ~95 smaller packs listed. `woopsdez/dtx-syrup` generates `set.def` files.

## Sources
- https://dtxmania.net/documents/create-setdef
