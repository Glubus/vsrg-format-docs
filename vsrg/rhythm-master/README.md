# Rhythm Master (节奏大师)

Rhythm Master (Light Speed Studio, Tencent; Chinese mobile game, 2012, old version closed 5 Feb 2021, relaunched later; "da.qq.com") has a **classic mode** of 4/5/6 vertical lanes with tap, slide and hold notes (vsrg) and a **star motion mode** (星动模式) similar to QQ Dance/Audition (lane-based too, with dance animation). Chart files:

| Folder | File | Role |
|---|---|---|
| [imd/](imd/README.md) | `.imd` | classic mode chart, binary, one per key count (4k/5k/6k) and difficulty (ez/nm/hd) |
| [mde/](mde/README.md) | `.mde` | star motion mode chart (stub: no public spec found) |
| [json/](json/README.md) | `.json` | "imdjson" (signature `BNDQ`), JSON equivalent of IMD used by newer clients; related to the WeChat mini-program JSON |

Tools around them: RMEssentials (C++/Qt, Fsu0413), RM2Malody (Python), rmstZ (Windows converter, closed), Malody's `imd_2_mc` plugin, imd2mc web tool, dreamimd.com community site. The old client's resource archive: https://github.com/GirlKiller512/RhythmMasterResource (classic-mode `.imd`, `.mp3`, covers, `mrock_song_client_android.xml` song list, `MD5List.xml`).
