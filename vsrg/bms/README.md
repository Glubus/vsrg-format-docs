# BMS (Be-Music Source) family

BMS is the plain-text chart format Urao Yane created in 1998 for BM98 (a PC simulator of Konami's beatmania), and the ecosystem around it. Charts are keysound based: a timeline of references to small audio files (`#WAVxx`), played on 5/7/9/10/14 keys + scratch (9 buttons for PMS).

Category: vsrg.

## Formats

| Folder | Extension | What it is | Status |
| --- | --- | --- | --- |
| [`bms/`](bms/README.md) | `.bms` | The format itself: syntax, headers, channels, timing, long notes, encodings | complete |
| [`bme/`](bme/README.md) | `.bme` | "Be-Music Extend": 7 keys + scratch layout (channels 18/19, 28/29) | complete |
| [`bml/`](bml/README.md) | `.bml` | "Be-Music Longnote": charts using `#LNOBJ` long notes | complete |
| [`pms/`](pms/README.md) | `.pms` | feeling-PoMu Script: 9-button pop'n music style layout | complete |
| [`bmson/`](bmson/README.md) | `.bmson` | JSON successor: pulse timing, sound-channel slicing (spec v1.0.0) | complete |

The four text extensions share one syntax. The extension was historically a filter for the channels a chart uses; modern players read all of them identically, except `.pms`, which selects the 9-button layout. Related formats: DTX/GDA/G2D (BMS descendants for drum/guitar games, other folders of this repo); the arcade formats BMS imitates ([`../beatmania-iidx`](../beatmania-iidx/README.md), [`../pop-n-music`](../pop-n-music/README.md)); [`../vos`](../vos/README.md).

Historic BMS-derived extensions in the hitkey memo (no spec, no folder): MGQ (24-key + long notes), MBM (MacBeat MOD), EMS, KMS, BAS (BMS-2), PHX, MGF, BMB, PMB, D2B, DEE; plus `.mdm` (Muse Dash Melon Loader fan charts, per Wikipedia, no spec).

## Ecosystem

- Players: Lunatic Rave 2 (LR2; closed source, de facto standard in Japan), beatoraja (Java/libGDX, reads `.bms/.bme/.bml/.pms/.bmson` and adds extensions), Bemuse (web; bms-js, bmson, `#SCROLL`/`#SPEED`), Raindrop (C++ VSRG engine with a BMS loader), ruv-it! (Korean de facto standard), uBMplay, Angolmois/Sonorous, Project OutFox / StepMania (parsers for `be-mu` and `po-mu`), feeling pomu second (9 keys).
- Editors: BMSE, iBMSC, BMS Creator (BMSC), GDA Creator; converters bmx2wav / bme2wav.
- Database / community: BMS Search (https://bmssearch.net/ - songs, charts, artists, events, playlists), BMS events such as BMS of Fighters (BOF, since 2004), difficulty tables, LR2IR / beatoraja IR.
- Specifications: hitkey "BMS command memo" (https://hitkey.nekokan.dyndns.info/cmds.htm), original BM98 spec (http://bm98.yaneu.com/bm98/bmsformat.html), Bemuse extensions (https://bemuse.ninja/project/docs/bms-extensions/), beatoraja wiki extensions, bmson-spec (https://github.com/bemusic/bmson-spec).
- Libraries: bms-js / bemuse-notechart (JS), bms-rs (Rust), StepMania `NotesLoaderBMS` (C++).

ROX status: ROX 0.8.1 reads none of these formats (BMS is "planned" in the ROX README).

Added format pages: [`ibmsc/`](ibmsc/README.md) (iBMSC project file); Bemuse's web layer is in [`../bemuse`](../bemuse/README.md).
