# Samples: Dynamix chart XML (`.xml`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `dynode-old-xml-import-test.xml` | https://github.com/NagaseIori/DyNode/blob/310df44db9cdfec2ba29cce6a5fb6aa64fcc3f4f/DyCore/tests/old_xml_import_ctest.cpp (raw string literal `oldXmlContent`, extracted verbatim; no trailing newline) | NordLandeW (DyNode) | MIT (repository LICENSE, (c) 2022-2026 NordLandeW) | Dialect B (`DynamixMap` with `Center`/`Left`/`Right`), 130 bars/min, `TimeOffset` 0.15, NORMAL / HOLD+SUB (SubIndex link) / CHAIN notes, left PAD + right MIXER; hand-written test fixture of DyNode, not a real song chart (680 bytes) |
| `synthetic-cmap.xml` | hand-written for this repository, built from the dialect A field list of `../README.md` (checked against the importer `parse_standard_format_xml` in NagaseIori/DyNode `DyCore/src/project/format/xml.cpp`) | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | Dialect A (`CMap`, `m_` elements): NORMAL / HOLD+SUB pair (`m_subId`) / CHAIN notes in a MIXER right side, PAD left side, centre + both side lists, left-edge `m_position`, fractional `m_time` (bars), two `CBpmchange` entries (30 -> 60 bars/min at bar 3), LF endings, UTF-8 declaration (2268 bytes) |

