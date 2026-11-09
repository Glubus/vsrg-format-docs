# Osu! Tatakae! Ouendan / Elite Beat Agents (iNiS, Nintendo DS)

iNiS touch-screen rhythm games (*Osu! Tatakae! Ouendan* 2005, *Elite Beat Agents* 2006, *Moero! Nekketsu Rhythm Damashii Osu! Tatakae! Ouendan 2* 2007). Numbered circles appear at free positions on the touch screen with a shrinking approach circle; sliders and spinners are traced/spun. The osu! game and its `.osu` format (standard mode) are modelled on this gameplay (see `others/osu-standard/`).

Category: others. Free-position touch notes, no lanes.

## Formats

No chart format folder. No public documentation or parser of the NDS chart data was found: web searches returned only the graphics/model formats of the game files (NCLR, NCGR, NCSR, NCER, NANR, nsbmd, nsbca; The VG Resource wiki) and the PC `.osu` format. A folder with an invented extension or layout would violate the no-invention rule. A documented ROM chart format belongs in `elite-beat-agents/<format>/`.

## Getting samples

None committed. Nothing public documents the DS chart data; the only chart-like files are PC `.osu` descendants. Real data requires an NDS cartridge/ROM of *Osu! Tatakae! Ouendan*, *Elite Beat Agents* or *Ouendan 2* and locating the beatmap data in its file system; no source says where or how it is encoded [inference: it would need reverse-engineering, e.g. starting from the VG Resource wiki below, which lists only graphics/model formats]. A reverse-engineered format gets `elite-beat-agents/<format>/` with a fiche and samples/manifest.

## Links

- Elite Beat Agents on the VG Resource wiki (file formats of graphics/models only): <https://wiki.vg-resource.com/Elite_Beat_Agents>
- osu! `.osu` format (the descendant): <https://osu.ppy.sh/wiki/en/Client/File_formats/osu_(file_format)>
- GDC 2007 talk by Keiichi Yano ("From Ouendan! to HELP!: Inside the Elite Beat Agents"): <https://archive.org/details/GDC2007Yano> (not opened)
