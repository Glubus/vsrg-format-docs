# Osu! Tatakae! Ouendan / Elite Beat Agents (iNiS, Nintendo DS)

iNiS touch-screen rhythm games (*Osu! Tatakae! Ouendan* 2005, *Elite Beat Agents* 2006, *Moero! Nekketsu Rhythm Damashii Osu! Tatakae! Ouendan 2* 2007). Numbered circles appear at free positions on the touch screen with a shrinking approach circle; sliders and spinners are traced/spun. The osu! game and its `.osu` format (standard mode) are modelled on this gameplay (see the osu!standard docs, `others/osu-standard/`).

**Category: others** — free-position touch notes, no lanes.

## Formats

**No chart format folder.** I found **no public documentation or parser** of the actual NDS chart data: web searches only returned documentation of the graphics/model formats of the game files (NCLR, NCGR, NCSR, NCER, NANR, nsbmd, nsbca; The VG Resource wiki) and of the PC `.osu` format, not of the beatmap data inside the ROM. Creating a folder with an invented extension or layout would violate the no-invention rule. If someone later documents the ROM chart format, it belongs in `elite-beat-agents/<format>/`.

## Getting samples

No sample is committed, none is in the manifest, and no format folder exists. Nothing public documents the DS chart data (see Formats above); the only chart-like files around are the PC `.osu` descendants of the gameplay. To obtain the real data one would have to own the NDS cartridge/ROM of *Osu! Tatakae! Ouendan*, *Elite Beat Agents* or *Ouendan 2* and locate the beatmap data inside its file system; no source read says where it is or how it is encoded [inference: it would have to be reverse-engineered, e.g. starting from the VG Resource wiki page linked below, which only lists graphics/model formats]. If a format is reverse-engineered, add `elite-beat-agents/<format>/` with a fiche and samples/manifest.

## Links

- Elite Beat Agents on the VG Resource wiki (file formats of graphics/models only): <https://wiki.vg-resource.com/Elite_Beat_Agents>
- osu! `.osu` format (the descendant): <https://osu.ppy.sh/wiki/en/Client/File_formats/osu_(file_format)>
- GDC 2007 talk by Keiichi Yano ("From Ouendan! to HELP!: Inside the Elite Beat Agents"): <https://archive.org/details/GDC2007Yano> (not opened)
