# BMS (Be-Music Source) family

BMS is the community rhythm-game ecosystem built around the plain-text chart format created by Urao Yane in 1998 for BM98 (a PC simulator of Konami's beatmania). Charts are *keysound based*: a timeline of references to many small audio files (`#WAVxx`), played by simulators on 5/7/9/10/14 keys + scratch.

Category: **vsrg** - notes fall in fixed lanes (keys + scratch turntable, or 9 buttons for PMS) toward a judgement line.

## Formats

| Folder | Extension | What it is | Status |
| --- | --- | --- | --- |
| [`bms/`](bms/README.md) | `.bms` | The format itself: full syntax, headers, channels, timing, long notes, encodings (complete reference) | complete |
| [`bme/`](bme/README.md) | `.bme` | "Be-Music Extend": 7 keys + scratch layout (channels 18/19, 28/29) | complete |
| [`bml/`](bml/README.md) | `.bml` | "Be-Music Longnote": charts using `#LNOBJ` long notes | complete |
| [`pms/`](pms/README.md) | `.pms` | feeling-PoMu Script: 9-button pop'n music style layout | complete |
| [`bmson/`](bmson/README.md) | `.bmson` | JSON successor: pulse timing, sound-channel slicing (spec v1.0.0) | complete |

The four text extensions share one syntax; the extension is historically a filter for which channels a chart uses, and modern players read all of them identically (except `.pms`, which selects the 9-button layout). Related formats documented elsewhere: DTX/GDA/G2D (BMS descendants for drum/guitar games, other folders of this repo); the arcade formats of the games BMS imitates ([`../beatmania-iidx`](../beatmania-iidx/README.md), [`../pop-n-music`](../pop-n-music/README.md)); [`../vos`](../vos/README.md).

Historic BMS-derived extensions named by the hitkey memo (no spec found, no folder): MGQ (24-key + long notes), MBM (MacBeat MOD), EMS, KMS, BAS (BMS-2), PHX, MGF, BMB, PMB, D2B, DEE; plus `.mdm` (Muse Dash Melon Loader fan charts, per Wikipedia, no spec).

## Ecosystem

- **Players**: Lunatic Rave 2 (LR2; closed source, de facto standard in Japan), beatoraja (Java/libGDX, reads `.bms/.bme/.bml/.pms/.bmson` and adds extensions), Bemuse (web; bms-js, bmson, `#SCROLL`/`#SPEED`), Raindrop (C++ VSRG engine with a BMS loader), ruv-it! (Korean de facto standard), uBMplay, Angolmois/Sonorous, Project OutFox / StepMania (parsers for `be-mu` and `po-mu`), feeling pomu second (9 keys).
- **Editors**: BMSE, iBMSC, BMS Creator (BMSC), GDA Creator; converters bmx2wav / bme2wav.
- **Database / community**: BMS Search (https://bmssearch.net/ - songs, charts, artists, events, playlists), BMS events such as BMS of Fighters (BOF, since 2004), difficulty tables, LR2IR / beatoraja IR.
- **Specifications**: hitkey "BMS command memo" (https://hitkey.nekokan.dyndns.info/cmds.htm), original BM98 spec (http://bm98.yaneu.com/bm98/bmsformat.html), Bemuse extensions (https://bemuse.ninja/project/docs/bms-extensions/), beatoraja wiki extensions, bmson-spec (https://github.com/bemusic/bmson-spec).
- **Libraries**: bms-js / bemuse-notechart (JS), bms-rs (Rust), StepMania `NotesLoaderBMS` (C++).

ROX status: none of these formats is read by ROX 0.8.1 (BMS is "planned" in the ROX README).

Added format pages: [`ibmsc/`](ibmsc/README.md) (iBMSC project file), [`bms-table/`](bms-table/README.md) (BMS difficulty table `header.json`/`data.json`); Bemuse's web layer is in [`../bemuse`](../bemuse/README.md).
