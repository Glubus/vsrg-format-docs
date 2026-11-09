# beatmania IIDX

Konami's arcade DJ game (7 keys + 1 turntable per side, first released 1999-02-26 as the 2-deck sequel to beatmania). Category: **vsrg** - notes fall in 8 fixed lanes (key 1-7 + scratch) per side toward a judgement line.

The BMS family originated as a simulator of beatmania and later IIDX; the community formats that *simulate* IIDX are documented in [`../bms`](../bms/README.md) (`.bme` = 7K layout, `.bmson` `beat-7k`). This folder documents the **arcade/console data formats** that have real public sources:

| Folder | Format | Status |
| --- | --- | --- |
| [`1/`](1/README.md) | `.1` chart archive (arcade, since 9th style) - 12-entry directory + 8-byte events | partial (SaxxonPike spec + iidx-ps2tools plugin) |
| [`2dx/`](2dx/README.md) | `.2dx` sound archive (keysounds in a `2DX9` container) | partial (reverse-engineered by extractor tools) |

Other things found while researching, with no format spec available (not given a folder): older PS2/console chart formats per style (SaxxonPike's `iidx-ps2tools` has one chart plugin per IIDX 3rd-16th style, the code is the only documentation), `.s3p` keysound archives (mentioned in SaxxonPike's `2dxfix` README), and the `ifs` Konami archive wrapper (see [`../pop-n-music`](../pop-n-music/README.md)).

Useful links: RemyWiki beatmania IIDX pages (https://remywiki.com/Beatmania_IIDX_Information), SaxxonPike rhythm-game-formats (https://github.com/SaxxonPike/rhythm-game-formats), iidx-ps2tools (https://github.com/SaxxonPike/iidx-ps2tools), mon/2dxTools (https://github.com/mon/2dxTools), iDestyKK/2dx_extract.
