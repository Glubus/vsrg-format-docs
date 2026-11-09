# Samples: Dynamix chart XML (`.xml`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `dynode-old-xml-import-test.xml` | https://github.com/NagaseIori/DyNode/blob/310df44db9cdfec2ba29cce6a5fb6aa64fcc3f4f/DyCore/tests/old_xml_import_ctest.cpp (raw string literal `oldXmlContent`, extracted verbatim; no trailing newline) | NordLandeW | MIT | Dialect B (`DynamixMap` with `Center`/`Left`/`Right`), 130 bars/min, `TimeOffset` 0.15, NORMAL / HOLD+SUB (SubIndex link) / |
| `synthetic-cmap.xml` | hand-written for this repository, built from the dialect A field list of `../README.md` (checked against the importer `parse_standard_format_xml` in NagaseIori/DyNode `DyCore/src/project/format/xml.cpp`) | vsrg-format-docs contributors | CC0-1.0 / public domain | Dialect A (`CMap`, `m_` elements): NORMAL / HOLD+SUB pair (`m_subId`) / CHAIN notes in a |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `camberloid__map_Sound_Souler_-_Paradise.xml` | https://raw.githubusercontent.com/CamberLoid/DynamixFanmade/6846626593638e59f363870fcf82e263901e8fe3/_map_Sound%20Souler%20-%20Paradise.xml | 2026-11-09 | `31025ed072ce81168e89b33cb3fefacd40793bdd696af75a1270d7b0f103eddd` | Community charters | WTFPL | Real fanmade chart, dialect A `CMap` with `xmlns:xsi`/`xmlns:xsd` attributes, `m_mapID` `_map_Sound Souler - Paradise_H`, 160 |
| `camberloid__map_ノマ_-_Brain_Power.xml` | https://raw.githubusercontent.com/CamberLoid/DynamixFanmade/6846626593638e59f363870fcf82e263901e8fe3/_map_%E3%83%8E%E3%83%9E%20-%20Brain%20Power.xml | 2026-11-09 | `c33d0f8edc0d46b78e3426cd138c390e1372183a379c7f922a52de72cc84d8a0` | Community charters | WTFPL | Real fanmade chart, dialect A (`CMap`), non-ASCII (Japanese) song name in `m_path`/`m_mapID`, file name starting |
