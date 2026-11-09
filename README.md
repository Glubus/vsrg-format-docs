# Rhythm game chart formats

One page per chart format of rhythm games (encoding, timing, notes, sources) and real sample charts for each. Started from a link list
(upstream `README.md`, commit `503382a`), extended for Prism's map library [ROX](https://github.com/Glubus/rhythm-open-exchange).

182 chart formats over 102 games: 109 VSRG (39 complete, 45 partial, 25 stub), 73 others (17 complete, 40 partial, 16 stub).

- [`FORMATS.md`](FORMATS.md): status of every format (real charts, ROX read/write, samples ROX decodes, played by Prism).
- [`SAMPLES-STATUS.md`](SAMPLES-STATUS.md): sample counts per format and why some have fewer than 5 real charts.
- Format page: `<category>/<game>/<format>/README.md`. Game page: `<category>/<game>/README.md`.
- Samples: `<format>/samples/`, sources in `samples/SOURCES.md`. Do not edit them (line endings and encodings matter, see `.gitattributes`).

## Samples

Chart files only: no audio, video, images or archives (packages are unpacked and only their charts kept, one subfolder per set).
`synthetic-*` files were written here (CC0); the rest comes from public sources, redistributed at the owner's risk. Formats with no public
copy have no sample; their page says how to get one.

## Rules

- No invented facts: each comes from a source linked on the page or from the ROX source. Unknown is written `Unknown`, a deduction `[inference]`, a fact read in a sample `[observed in ...]`.
- Category by gameplay: `vsrg/` for notes on fixed lanes toward a judgement line (the model ROX reads), `others/` for the rest. The reason per game is in [the game table](#game-by-game-category-decisions).
- English. A new format gets its page, a row in the index below and a row in `SAMPLES-STATUS.md`.

Doc status: `complete` (a parser can be written from the page), `partial` (gaps stated), `stub` (identity and sources). ROX: `Yes` (read and write),
`Decode only`, `Partial` (one dialect), `No`.

## Packages

Archives that carry charts with their audio and images. No page or sample of their own; each chart page lists them under "Shipped in".

| Package (extension) | Game | What is inside | Charts in |
|---|---|---|---|
| `.sng` | Clone Hero / YARG | Clone Hero / YARG single-file package: a masked container with the song folder, i.e. chart, audio, images, video, plus a metadata key/value table | [`.chart`](vsrg/clone-hero/chart/), [`.mid`](vsrg/clone-hero/mid/) |
| `.fms` | fluXis | Zip of a fluXis mapset: `.fsc` difficulties, `.ffx` effects, audio, background, video, hitsounds | [`.fsc`](vsrg/fluxis/fsc/), [`.ffx`](vsrg/fluxis/ffx/) |
| `.fnfc` | Friday Night Funkin' (0.3+, V-Slice) | Zip saved by the V-Slice Chart Editor: `-metadata.json`, `-chart.json` and the audio | [`-chart.json`](vsrg/friday-night-funkin/vslice-chart-json/), [`-metadata.json`](vsrg/friday-night-funkin/vslice-metadata-json/) |
| `.fnfmod` | Friday Night Funkin' (official mod menu) | Zip of a whole FNF mod from the official Mod Menu: songs as V-Slice chart/metadata files, characters, stages | [`-chart.json`](vsrg/friday-night-funkin/vslice-chart-json/), [`-metadata.json`](vsrg/friday-night-funkin/vslice-metadata-json/) |
| `.snp` | KrazyRain | KrazyRain `VDISK1.0` archive: zlib-compressed `.xnt` charts, `.xne` XML files and OGG samples | [`.xnt`](vsrg/o2jam/xnt/) |
| `.mcz` | Malody / Malody V | Zip: one or more `.mc` charts plus audio, background, optional video and keysounds | [`.mc`](vsrg/malody/mc/) |
| `.osz` | osu! (all modes) | Zip of a beatmap set: one `.osu` per difficulty, audio, background, optional video, `.osb` storyboard, hitsounds | [`.osu`](vsrg/osu-mania/osu/), [`.osb`](vsrg/osu-mania/osb/); other modes: [osu!standard](others/osu-standard/osu/), [osu!taiko](others/osu-taiko/osu/), [osu!catch](others/osu-catch/osu/) |
| `.olz` | osu!mania (osu!lazer) | Zip exported by osu!lazer: the set's `.osu` difficulties plus audio, images, storyboard; lazer-only, not readable by stable | [`.osu`](vsrg/osu-mania/osu/) |
| `.qp` | Quaver | Zip of a Quaver mapset: one `.qua` per difficulty, audio, background, banner, hit samples | [`.qua`](vsrg/quaver/qua/) |
| `.smzip` | StepMania / ITG / Etterna / OutFox | Zip with install-relative paths `Songs/<Group>/<Song>/` holding `.sm`/`.ssc` and audio, optional `smzip.ctl`; plain `.zip` packs have the same layout | [`.sm`](vsrg/stepmania/sm/), [`.ssc`](vsrg/stepmania/ssc/), [`.crs`](vsrg/stepmania/crs/) |
| `.yargsong` | YARG | YARG single-file song package from the YARC Launcher; internal layout Unknown | [`.chart`](vsrg/clone-hero/chart/), [`.mid`](vsrg/clone-hero/mid/) [inference] |
| `.arcpkg` | Arcaea (ArcCreate) | ArcCreate zip: `index.yml`, `*.arcproj`, `.aff` charts, audio, jacket, background | [`.aff`](others/arcaea/aff/) |
| BeatSaver `.zip` | Beat Saber | Map folder: `Info.dat`, one difficulty `.dat` each, audio, cover | [`.dat`](others/beat-saber/dat/), [`Info.dat`](others/beat-saber/info-dat/) |
| `.cytoidlevel` | Cytoid / Cytus | Zip of a Cytoid level: `level.json`, chart text/JSON files, music, background | [`.txt`](others/cytus/c1-txt/), [`.json`](others/cytus/c2-json/) |
| `.mdm` | Muse Dash | Zip of a custom album: `info.json`, `map1.bms`..`map5.bms`, cover, demo, music; a `.mdp` pack is a zip of `.mdm` | [`.bms`](others/muse-dash/bms/) |
| `.pez` | Phigros (Phira / PhiZone) | Phira / PhiZone zip: a chart file, music, illustration, `info.yml` | [RPE](others/phigros/rpe/), [official JSON](others/phigros/official-json/), [PEC](others/phigros/pec/) |
| `.rdzip` | Rhythm Doctor | Zip of an `.rdlevel` plus its audio and sprites | [`.rdlevel`](others/rhythm-doctor/rdlevel/) |
| `.riq` | Rhythm Heaven Studio (fan game inspired by Rhythm Heaven) | Rhythm Heaven Studio zip: `.meta`, `Charts/chart<N>.json`, `Music/`, `Resources/` | none (RIQ chart JSON has no page of its own) |
| `.psarc` | Rocksmith 2014 (official DLC and CDLC) | PlayStation archive, encrypted table of contents: `.sng` arrangements, JSON manifests, Wwise audio, art | [`.sng`](others/rocksmith/sng/) |
| `.scp` | Sonolus | Sonolus Collection Package zip: levels with gzip LevelData, engines, skins, effects, particles | [`.json` (gzip LevelData)](others/sonolus/level-data/) |

## Formats: vsrg

| Format (extension) | Game(s) | Category | Doc status | Read by ROX | Folder |
|---|---|---|---|---|---|
| [`.bdon / .json`](vsrg/bang-dream/bdon/) BDON (BanG Dream! Our Notes) chart | BanG Dream! Our Notes | vsrg | partial | Decode only (12 lanes; `.json` by content) | [`vsrg/bang-dream/bdon`](vsrg/bang-dream/bdon/) |
| [`.json`](vsrg/bang-dream/bestdori-json/) Bestdori chart (v2 JSON) | BanG Dream! Girls Band Party (Bestdori) | vsrg | partial | Decode only (by content, any `.json` name) | [`vsrg/bang-dream/bestdori-json`](vsrg/bang-dream/bestdori-json/) |
| [`.txt`](vsrg/bang-dream/txt/) BanG! Simulator chart (txt) | BanG Dream! (BanG! Simulator) | vsrg | complete | Decode only (by content) | [`vsrg/bang-dream/txt`](vsrg/bang-dream/txt/) |
| [`.1`](vsrg/beatmania-iidx/1/) beatmania IIDX arcade chart archive (.1) | beatmania IIDX (arcade, 9th style onward) | vsrg | partial | No | [`vsrg/beatmania-iidx/1`](vsrg/beatmania-iidx/1/) |
| [`.2dx`](vsrg/beatmania-iidx/2dx/) beatmania IIDX keysound archive (2DX9 container) | beatmania IIDX (and other Konami games with the same engine) | vsrg | partial | No | [`vsrg/beatmania-iidx/2dx`](vsrg/beatmania-iidx/2dx/) |
| [`.bemuse`](vsrg/bemuse/bemuse/) Bemuse sound pack (+ metadata.json) | Bemuse (web BMS player) | vsrg | complete | No | [`vsrg/bemuse/bemuse`](vsrg/bemuse/bemuse/) |
| [`bemuse-song.json / index.json`](vsrg/bemuse/bemuse-song-json/) Bemuse song metadata and music server index | Bemuse (web BMS player) | vsrg | complete | No | [`vsrg/bemuse/bemuse-song-json`](vsrg/bemuse/bemuse-song-json/) |
| [`.bme`](vsrg/bms/bme/) Be-Music Extend (BME) chart, 7 keys + scratch | BMS ecosystem (beatmania IIDX layout): LR2, beatoraja, Bemuse | vsrg | complete | Decode only | [`vsrg/bms/bme`](vsrg/bms/bme/) |
| [`.bml`](vsrg/bms/bml/) Be-Music Longnote (BML) chart | BMS ecosystem (long-note charts via #LNOBJ) | vsrg | complete | Decode only | [`vsrg/bms/bml`](vsrg/bms/bml/) |
| [`.bms`](vsrg/bms/bms/) Be-Music Source (BMS) chart | BMS ecosystem: LR2, beatoraja, Bemuse, Raindrop, ruv-it!, uBMplay, OutFox (beatmania/IIDX simulators) | vsrg | complete | Decode only | [`vsrg/bms/bms`](vsrg/bms/bms/) |
| [`.bmson`](vsrg/bms/bmson/) bmson 1.0.0 (JSON BMS successor) | Bemuse, Raindrop, beatoraja (and BMS-ecosystem tools) | vsrg | complete | Decode only | [`vsrg/bms/bmson`](vsrg/bms/bmson/) |
| [`.ibmsc`](vsrg/bms/ibmsc/) iBMSC project file | iBMSC / uBMSC / pBMSC (BMS editor) | vsrg | complete | No | [`vsrg/bms/ibmsc`](vsrg/bms/ibmsc/) |
| [`.pms`](vsrg/bms/pms/) feeling-PoMu Script (PMS), 9-button BMS dialect | pop'n music style simulators: feeling pomu, LR2, beatoraja (PMS mode) | vsrg | complete | Decode only | [`vsrg/bms/pms`](vsrg/bms/pms/) |
| [`.chart`](vsrg/clone-hero/chart/) Clone Hero / Moonscraper chart | Clone Hero / Moonscraper / Feedback Editor / YARG / Phase Shift | vsrg | complete | Decode only | [`vsrg/clone-hero/chart`](vsrg/clone-hero/chart/) |
| [`.ini`](vsrg/clone-hero/ini/) Clone Hero song.ini metadata | Clone Hero / YARG / Phase Shift / FoFiX | vsrg | complete | Decode only | [`vsrg/clone-hero/ini`](vsrg/clone-hero/ini/) |
| [`.mid`](vsrg/clone-hero/mid/) Rock Band / Clone Hero MIDI chart (notes.mid) | Clone Hero / YARG / Rock Band / Guitar Hero 1-2 / Phase Shift / FoFiX | vsrg | partial | Decode only | [`vsrg/clone-hero/mid`](vsrg/clone-hero/mid/) |
| [`.gen`](vsrg/ddr/gen/) DDR S+ song container (iOS) | Dance Dance Revolution S+ (iOS) | vsrg | stub | No | [`vsrg/ddr/gen`](vsrg/ddr/gen/) |
| [`.ssq (chunk 9)`](vsrg/ddr/hudson-ssq/) Hudson SSQ type 9 step chunk | DDR Mario Mix / DDR Hottest Party 1 (Wii/GC) | vsrg | complete | No | [`vsrg/ddr/hudson-ssq`](vsrg/ddr/hudson-ssq/) |
| [`.ssq (chunk 16)`](vsrg/ddr/hudson-ssq-lane/) Hudson SSQ type 16 lane-format chunk | DDR Hottest Party 4/5 (Wii) | vsrg | complete | No | [`vsrg/ddr/hudson-ssq-lane`](vsrg/ddr/hudson-ssq-lane/) |
| [`.msd`](vsrg/ddr/msd/) MSD step script | DDR'99 (PC simulator) | vsrg | partial | Decode only (DWI grammar) | [`vsrg/ddr/msd`](vsrg/ddr/msd/) |
| [`.sdf`](vsrg/ddr/sdf/) Pocket DDR chart | Pocket DDR | vsrg | partial | No | [`vsrg/ddr/sdf`](vsrg/ddr/sdf/) |
| [`.ssq`](vsrg/ddr/ssq/) DDR SSQ step data | Dance Dance Revolution (Konami) | vsrg | complete | Decode only | [`vsrg/ddr/ssq`](vsrg/ddr/ssq/) |
| [`step`](vsrg/ddr/step/) DDR STEP (1st-3rd Mix, DDR Utility) | Dance Dance Revolution | vsrg | partial | Decode only (by content) | [`vsrg/ddr/step`](vsrg/ddr/step/) |
| [`step2`](vsrg/ddr/step2/) DDR STEP2 (1st Mix) | Dance Dance Revolution | vsrg | partial | No | [`vsrg/ddr/step2`](vsrg/ddr/step2/) |
| [`x_data_US.bin / .sng / .sif`](vsrg/ddr/ultramix-archive/) DDR Ultramix archives | DDR Ultramix (Xbox) | vsrg | complete | No | [`vsrg/ddr/ultramix-archive`](vsrg/ddr/ultramix-archive/) |
| [`.xmk`](vsrg/dj-hero/xmk/) DJ Hero chart (xmk) | DJ Hero / DJ Hero 2 | vsrg | partial | Decode only (5 columns; `.fsgmub` too) | [`vsrg/dj-hero/xmk`](vsrg/dj-hero/xmk/) |
| [`.pt`](vsrg/djmax/pt/) DJMAX pattern (PTFF) | DJMAX Online / DJMAX Technika (arcade, Technika Q) | vsrg | partial | No | [`vsrg/djmax/pt`](vsrg/djmax/pt/) |
| [`.dtx`](vsrg/dtxmania/dtx/) DTXMania chart | DTXMania (GuitarFreaks/DrumMania simulator) | vsrg | complete | Decode only | [`vsrg/dtxmania/dtx`](vsrg/dtxmania/dtx/) |
| [`.g2d`](vsrg/dtxmania/g2d/) DTXMania older chart (G2D) | GuitarFreaks/DrumMania via DTXMania | vsrg | partial | Decode only (as GDA) | [`vsrg/dtxmania/g2d`](vsrg/dtxmania/g2d/) |
| [`.gda`](vsrg/dtxmania/gda/) DTXMania older chart (GDA) | GuitarFreaks/DrumMania via DTXMania | vsrg | partial | Decode only (DTX with GDA channel names) | [`vsrg/dtxmania/gda`](vsrg/dtxmania/gda/) |
| [`set.def`](vsrg/dtxmania/set-def/) DTXMania song set descriptor | DTXMania | vsrg | complete | No | [`vsrg/dtxmania/set-def`](vsrg/dtxmania/set-def/) |
| [`.dwi`](vsrg/dwi/dwi/) Dance With Intensity step file | Dance With Intensity | vsrg | complete | Decode only | [`vsrg/dwi/dwi`](vsrg/dwi/dwi/) |
| [`.ett`](vsrg/etterna/ett/) Etterna song file (write-only) | Etterna | vsrg | partial | No | [`vsrg/etterna/ett`](vsrg/etterna/ett/) |
| [`.ez`](vsrg/ez2/ez/) EZ2DJ/EZ2AC chart (EZFF) | EZ2DJ / EZ2AC | vsrg | partial | No | [`vsrg/ez2/ez`](vsrg/ez2/ez/) |
| [`.ezi`](vsrg/ez2/ezi/) EZ2AC keysound index | EZ2DJ / EZ2AC | vsrg | partial | No | [`vsrg/ez2/ezi`](vsrg/ez2/ezi/) |
| [`.swf`](vsrg/flash-flash-revolution/swf/) FFR legacy level SWF (beatBox) | Flash Flash Revolution | vsrg | partial | Decode only (4 columns; embedded MP3 not read) | [`vsrg/flash-flash-revolution/swf`](vsrg/flash-flash-revolution/swf/) |
| [`.ffx`](vsrg/fluxis/ffx/) fluXis effects file | fluXis | vsrg | partial | No | [`vsrg/fluxis/ffx`](vsrg/fluxis/ffx/) |
| [`.fsc`](vsrg/fluxis/fsc/) fluXis map | fluXis | vsrg | partial | Decode only (ticks as taps; scroll groups, effects not read) | [`vsrg/fluxis/fsc`](vsrg/fluxis/fsc/) |
| [`.mid`](vsrg/fortnite-festival/mid/) Fortnite Festival chart MIDI | Fortnite Festival (Jam Tracks) | vsrg | stub | No | [`vsrg/fortnite-festival/mid`](vsrg/fortnite-festival/mid/) |
| [`.json`](vsrg/friday-night-funkin/codename-json/) FNF Codename Engine chart + meta.json | Friday Night Funkin' (Codename Engine) | vsrg | partial | Decode only (player strumlines; by content) | [`vsrg/friday-night-funkin/codename-json`](vsrg/friday-night-funkin/codename-json/) |
| [`.json`](vsrg/friday-night-funkin/fps-plus-json/) FNF FPS Plus chart + meta/events | Friday Night Funkin' (FPS Plus) | vsrg | stub | No | [`vsrg/friday-night-funkin/fps-plus-json`](vsrg/friday-night-funkin/fps-plus-json/) |
| [`.json`](vsrg/friday-night-funkin/kade-json/) FNF Kade Engine chart (KE1) | Friday Night Funkin' (Kade Engine) | vsrg | partial | Partial (legacy `.json` layout only) | [`vsrg/friday-night-funkin/kade-json`](vsrg/friday-night-funkin/kade-json/) |
| [`.json`](vsrg/friday-night-funkin/legacy-json/) FNF legacy week chart (song.notes[].sectionNotes) | Friday Night Funkin' (≤0.2.x, Kade/Psych-compatible) | vsrg | complete | Yes (read + write) | [`vsrg/friday-night-funkin/legacy-json`](vsrg/friday-night-funkin/legacy-json/) |
| [`.png`](vsrg/friday-night-funkin/ludum-dare-png/) FNF Ludum Dare chart (PNG per section) | Friday Night Funkin' (Ludum Dare jam build) | vsrg | partial | Decode only (the `.json` with its bitmaps; player side) | [`vsrg/friday-night-funkin/ludum-dare-png`](vsrg/friday-night-funkin/ludum-dare-png/) |
| [`.json`](vsrg/friday-night-funkin/maru-json/) FNF Maru Funkin' chart | Friday Night Funkin' (Maru Funkin', dead engine) | vsrg | stub | No | [`vsrg/friday-night-funkin/maru-json`](vsrg/friday-night-funkin/maru-json/) |
| [`.json`](vsrg/friday-night-funkin/nmv-json/) FNF Nightmare Vision chart (nmv2) | Friday Night Funkin' (NightmareVision) | vsrg | partial | No | [`vsrg/friday-night-funkin/nmv-json`](vsrg/friday-night-funkin/nmv-json/) |
| [`.json`](vsrg/friday-night-funkin/psych-json/) FNF Psych Engine chart (psych_v1) | Friday Night Funkin' (Psych Engine) | vsrg | complete | Partial (legacy `.json` layout; `psych_v1` lane rule read since 2026-10-28) | [`vsrg/friday-night-funkin/psych-json`](vsrg/friday-night-funkin/psych-json/) |
| [`.json`](vsrg/friday-night-funkin/troll-json/) FNF Troll Engine chart | Friday Night Funkin' (Troll Engine) | vsrg | stub | No | [`vsrg/friday-night-funkin/troll-json`](vsrg/friday-night-funkin/troll-json/) |
| [`.json`](vsrg/friday-night-funkin/vslice-chart-json/) FNF V-Slice chart data (-chart.json) | Friday Night Funkin' (0.3+, V-Slice) | vsrg | complete | Decode only | [`vsrg/friday-night-funkin/vslice-chart-json`](vsrg/friday-night-funkin/vslice-chart-json/) |
| [`.json`](vsrg/friday-night-funkin/vslice-metadata-json/) FNF V-Slice song metadata (-metadata.json) | Friday Night Funkin' (0.3+, V-Slice) | vsrg | complete | Decode only | [`vsrg/friday-night-funkin/vslice-metadata-json`](vsrg/friday-night-funkin/vslice-metadata-json/) |
| [`.dsq/.gsq`](vsrg/gitadora/dsq/) Older DrumMania/GuitarFreaks sequences | GuitarFreaks/DrumMania (early) | vsrg | stub | No | [`vsrg/gitadora/dsq`](vsrg/gitadora/dsq/) |
| [`.sq2`](vsrg/gitadora/sq2/) GuitarFreaks/DrumMania sequence | GF/DM V-series / XG | vsrg | stub | No | [`vsrg/gitadora/sq2`](vsrg/gitadora/sq2/) |
| [`.sq3`](vsrg/gitadora/sq3/) GITADORA sequence (SEQP/SQ3T) | GITADORA | vsrg | partial | No | [`vsrg/gitadora/sq3`](vsrg/gitadora/sq3/) |
| [`.mid`](vsrg/guitar-hero/gh12-mid/) Guitar Hero 1/2 MIDI chart | Guitar Hero / Guitar Hero II (Harmonix) | vsrg | complete | Decode only (by content; `T1 GEMS` as the guitar) | [`vsrg/guitar-hero/gh12-mid`](vsrg/guitar-hero/gh12-mid/) |
| [`.qb`](vsrg/guitar-hero/qb-chart/) Neversoft Guitar Hero chart (QB) | Guitar Hero III / World Tour (Neversoft) | vsrg | partial | No | [`vsrg/guitar-hero/qb-chart`](vsrg/guitar-hero/qb-chart/) |
| [`.yav`](vsrg/interlude/yav/) Interlude binary chart (legacy file, now database/CDN blob) | Interlude (YAVSRG) | vsrg | partial | Decode only (`.yav`; a headless blob with its key count given) | [`vsrg/interlude/yav`](vsrg/interlude/yav/) |
| [`.ksf`](vsrg/kick-it-up/ksf/) Kick It Up step file (+Direct Move) | Kick It Up / Direct Move (Pump) | vsrg | complete | Decode only (single, halfdouble, double) | [`vsrg/kick-it-up/ksf`](vsrg/kick-it-up/ksf/) |
| [`.d2r`](vsrg/legacy-dance-formats/d2r/) Dazzle Dazzle Realization chart | Dazzle Dazzle Realization | vsrg | partial | No | [`vsrg/legacy-dance-formats/d2r`](vsrg/legacy-dance-formats/d2r/) |
| [`directmove`](vsrg/legacy-dance-formats/directmove/) Direct Move (extended KSF) | Direct Move | vsrg | partial | Decode only | [`vsrg/legacy-dance-formats/directmove`](vsrg/legacy-dance-formats/directmove/) |
| [`.ftb`](vsrg/legacy-dance-formats/ftb/) Raindrop FTB chart | Raindrop (origin unknown) | vsrg | partial | No | [`vsrg/legacy-dance-formats/ftb`](vsrg/legacy-dance-formats/ftb/) |
| [`.slo`](vsrg/legacy-dance-formats/slo/) SLOEDIT chart | D2R / SLOEDIT editor | vsrg | stub | No | [`vsrg/legacy-dance-formats/slo`](vsrg/legacy-dance-formats/slo/) |
| [`.step`](vsrg/legacy-dance-formats/step/) pyDDR/pydance .step | pydance | vsrg | partial | Decode only (by content, as `.dance`) | [`vsrg/legacy-dance-formats/step`](vsrg/legacy-dance-formats/step/) |
| [`.sul`](vsrg/legacy-dance-formats/sul/) D2R legacy chart | Dazzle Dazzle Realization (older version) | vsrg | stub | No | [`vsrg/legacy-dance-formats/sul`](vsrg/legacy-dance-formats/sul/) |
| [`.mc`](vsrg/malody/mc/) Malody chart (JSON) | Malody / Malody V (Key, Catch, Pad, Taiko, Ring, Slide, Live, Cube) | vsrg | partial | Yes (read + write) | [`vsrg/malody/mc`](vsrg/malody/mc/) |
| [`.xml`](vsrg/music-master/xml/) Music Master chart | Music Master (乐动达人) | vsrg | stub | No | [`vsrg/music-master/xml`](vsrg/music-master/xml/) |
| [`.xml`](vsrg/music-times/xml/) Music Times chart | Music Times (乐动时代) | vsrg | stub | No | [`vsrg/music-times/xml`](vsrg/music-times/xml/) |
| [`.txt`](vsrg/musync/txt/) MUSYNX (Musync) chart (txt) | MUSYNX / Musync | vsrg | stub | No | [`vsrg/musync/txt`](vsrg/musync/txt/) |
| [`.ojm`](vsrg/o2jam/ojm/) O2Jam music/sample container (M30 / OMC / OJM) | O2Jam | vsrg | complete | Decode only | [`vsrg/o2jam/ojm`](vsrg/o2jam/ojm/) |
| [`.ojn`](vsrg/o2jam/ojn/) O2Jam note file | O2Jam (and Open2Jam, O2Mania, CXO2) | vsrg | complete | Decode only | [`vsrg/o2jam/ojn`](vsrg/o2jam/ojn/) |
| [`OJNList.dat`](vsrg/o2jam/ojnlist-dat/) O2Jam client music list | O2Jam | vsrg | partial | No | [`vsrg/o2jam/ojnlist-dat`](vsrg/o2jam/ojnlist-dat/) |
| [`.txt`](vsrg/o2jam/txt/) O2Jam - Music & Game chart | O2Jam - Music & Game (mobile) | vsrg | stub | No | [`vsrg/o2jam/txt`](vsrg/o2jam/txt/) |
| [`.xnt`](vsrg/o2jam/xnt/) KrazyRain chart (XNOT) | KrazyRain | vsrg | partial | No | [`vsrg/o2jam/xnt`](vsrg/o2jam/xnt/) |
| [`.osb`](vsrg/osu-mania/osb/) osu! storyboard file | osu! (storyboards of osu!mania mapsets) | vsrg | partial | No | [`vsrg/osu-mania/osb`](vsrg/osu-mania/osb/) |
| [`.osu`](vsrg/osu-mania/osu/) osu! beatmap (mode 3, osu!mania) | osu!mania (osu!) | vsrg | complete | Yes (read + write) | [`vsrg/osu-mania/osu`](vsrg/osu-mania/osu/) |
| [`(unknown)`](vsrg/pop-n-music/arcade-chart/) pop'n music arcade chart events | pop'n music (arcade) | vsrg | stub | No | [`vsrg/pop-n-music/arcade-chart`](vsrg/pop-n-music/arcade-chart/) |
| [`.mmws / .ccmmws / .unchmmws`](vsrg/project-sekai/ccmmws/) MikuMikuWorld binary layout (MMWS/CCMMWS/UCMMWS) | Project SEKAI (MikuMikuWorld editors and forks) | vsrg | partial | No | [`vsrg/project-sekai/ccmmws`](vsrg/project-sekai/ccmmws/) |
| [`.sus`](vsrg/project-sekai/holodori-sus/) hololive Dream SUS dialect | hololive Dream | vsrg | partial | No | [`vsrg/project-sekai/holodori-sus`](vsrg/project-sekai/holodori-sus/) |
| [`.mmws`](vsrg/project-sekai/mmws/) MikuMikuWorld score (MMWS) | Project SEKAI (MikuMikuWorld editor) | vsrg | stub | No | [`vsrg/project-sekai/mmws`](vsrg/project-sekai/mmws/) |
| [`.pjsk / .json / .json.gz`](vsrg/project-sekai/pjsk/) PJSK score maker chart | Project SEKAI: Colorful Stage! | vsrg | partial | No | [`vsrg/project-sekai/pjsk`](vsrg/project-sekai/pjsk/) |
| [`.sus`](vsrg/project-sekai/sus/) Sliding Universal Score (SUS) | Project SEKAI (Seaurchin / Chunithm lineage) | vsrg | partial | Decode only | [`vsrg/project-sekai/sus`](vsrg/project-sekai/sus/) |
| [`.usc`](vsrg/project-sekai/usc/) Universal Sekai Chart (USC) | Project SEKAI (Sonolus) | vsrg | partial | Decode only | [`vsrg/project-sekai/usc`](vsrg/project-sekai/usc/) |
| [`.not / .not5`](vsrg/pump-it-up/not/) Pump It Up NOT/NOT5 step file | Pump It Up (Andamiro) | vsrg | partial | Decode only (5 or 10 columns) | [`vsrg/pump-it-up/not`](vsrg/pump-it-up/not/) |
| [`.stx`](vsrg/pump-it-up/stx/) Pump It Up STX step file (STF4) | Pump It Up (Andamiro) | vsrg | partial | Decode only (one chart per mode) | [`vsrg/pump-it-up/stx`](vsrg/pump-it-up/stx/) |
| [`.ucs`](vsrg/pump-it-up/ucs/) Pump It Up User Custom Step | Pump It Up | vsrg | partial | Decode only | [`vsrg/pump-it-up/ucs`](vsrg/pump-it-up/ucs/) |
| [`.dance`](vsrg/pydance/dance/) pydance step file | pydance | vsrg | complete | Decode only | [`vsrg/pydance/dance`](vsrg/pydance/dance/) |
| [`.xml`](vsrg/qq-dance/xml/) QQ Dance mobile chart | QQ Dance mobile (QQ炫舞手游) | vsrg | partial | No | [`vsrg/qq-dance/xml`](vsrg/qq-dance/xml/) |
| [`.qua`](vsrg/quaver/qua/) Quaver map (YAML) | Quaver | vsrg | complete | Yes (read + write) | [`vsrg/quaver/qua`](vsrg/quaver/qua/) |
| [`.r2n`](vsrg/r2beat/r2n/) R2Beat chart package | R2Beat | vsrg | stub | No | [`vsrg/r2beat/r2n`](vsrg/r2beat/r2n/) |
| [`.xml`](vsrg/r2beat/xml/) R2Beat note chart | R2Beat | vsrg | partial | No | [`vsrg/r2beat/xml`](vsrg/r2beat/xml/) |
| [`.imd`](vsrg/rhythm-master/imd/) Rhythm Master classic chart | Rhythm Master (节奏大师) | vsrg | complete | Decode only | [`vsrg/rhythm-master/imd`](vsrg/rhythm-master/imd/) |
| [`.json`](vsrg/rhythm-master/json/) Rhythm Master imdjson (BNDQ) | Rhythm Master (节奏大师) / WeChat mini program | vsrg | partial | No | [`vsrg/rhythm-master/json`](vsrg/rhythm-master/json/) |
| [`.mde`](vsrg/rhythm-master/mde/) Rhythm Master star motion chart | Rhythm Master (节奏大师) | vsrg | stub | No | [`vsrg/rhythm-master/mde`](vsrg/rhythm-master/mde/) |
| [`.jrox`](vsrg/rhythm-open-exchange/jrox/) ROX JSON | Rhythm Open Exchange | vsrg | complete | Yes (read + write) | [`vsrg/rhythm-open-exchange/jrox`](vsrg/rhythm-open-exchange/jrox/) |
| [`.rox`](vsrg/rhythm-open-exchange/rox/) ROX native binary | Rhythm Open Exchange | vsrg | complete | Yes (read + write) | [`vsrg/rhythm-open-exchange/rox`](vsrg/rhythm-open-exchange/rox/) |
| [`.yrox`](vsrg/rhythm-open-exchange/yrox/) ROX YAML | Rhythm Open Exchange | vsrg | complete | Yes (read + write) | [`vsrg/rhythm-open-exchange/yrox`](vsrg/rhythm-open-exchange/yrox/) |
| [`.lua`](vsrg/robeats/lua-songmap/) RoBeats custom-server song map (Lua ModuleScript) | RoBeats (Roblox) | vsrg | partial | No | [`vsrg/robeats/lua-songmap`](vsrg/robeats/lua-songmap/) |
| [`.dta`](vsrg/rock-band/dta/) Rock Band songs.dta database | Rock Band / Guitar Hero (Harmonix engine) | vsrg | stub | No | [`vsrg/rock-band/dta`](vsrg/rock-band/dta/) |
| [`.ksh`](vsrg/sound-voltex/ksh/) K-Shoot MANIA chart (text) | K-Shoot MANIA / Unnamed SDVX Clone / SOUND VOLTEX fan charts | vsrg | complete | Decode only (6 columns; lasers not supported for now: dropped; by content) | [`vsrg/sound-voltex/ksh`](vsrg/sound-voltex/ksh/) |
| [`.kson`](vsrg/sound-voltex/kson/) K-Shoot MANIA JSON chart | K-Shoot MANIA / Unnamed SDVX Clone (Rust rewrite) | vsrg | partial | No | [`vsrg/sound-voltex/kson`](vsrg/sound-voltex/kson/) |
| [`.vox`](vsrg/sound-voltex/vox/) SOUND VOLTEX arcade chart | SOUND VOLTEX (arcade, Konami) | vsrg | partial | No | [`vsrg/sound-voltex/vox`](vsrg/sound-voltex/vox/) |
| [`.nanochart`](vsrg/soundsphere/nanochart/) NanoChart (rizu compact note stream) | rizu (soundsphere) | vsrg | complete | No | [`vsrg/soundsphere/nanochart`](vsrg/soundsphere/nanochart/) |
| [`.sph`](vsrg/soundsphere/sph/) SPH chart (rizu / soundsphere) | rizu (soundsphere) | vsrg | partial | No | [`vsrg/soundsphere/sph`](vsrg/soundsphere/sph/) |
| [`.crs`](vsrg/stepmania/crs/) StepMania course file | StepMania / ITG / OutFox / NotITG | vsrg | complete | No | [`vsrg/stepmania/crs`](vsrg/stepmania/crs/) |
| [`.edit`](vsrg/stepmania/edit/) StepMania edit file | StepMania (player edits) | vsrg | complete | Decode only | [`vsrg/stepmania/edit`](vsrg/stepmania/edit/) |
| [`.sm`](vsrg/stepmania/sm/) StepMania simfile | StepMania 3.x/4/5, Etterna, ITG, NotITG, OutFox | vsrg | complete | Yes (read + write) | [`vsrg/stepmania/sm`](vsrg/stepmania/sm/) |
| [`.ssc`](vsrg/stepmania/ssc/) StepMania 5 simfile | StepMania 5 / Etterna / ITGmania / OutFox | vsrg | complete | Yes (read + write) | [`vsrg/stepmania/ssc`](vsrg/stepmania/ssc/) |
| [`.sma`](vsrg/stepmania-amx/sma/) StepMania AMX simfile | StepMania AMX | vsrg | partial | No | [`vsrg/stepmania-amx/sma`](vsrg/stepmania-amx/sma/) |
| [`.json`](vsrg/stepmania-micro/json/) StepMania JSON (StepMania Micro) | StepMania Micro | vsrg | partial | No | [`vsrg/stepmania-micro/json`](vsrg/stepmania-micro/json/) |
| [`.vos`](vsrg/vos/vos/) Virtual Orchestra Studio song (.vos) | Virtual Orchestra Studio (HanseulSoft) / CanMusic / Mania simulator | vsrg | partial | No | [`vsrg/vos/vos`](vsrg/vos/vos/) |

## Formats: others

| Format (extension) | Game(s) | Category | Doc status | Read by ROX | Folder |
|---|---|---|---|---|---|
| [`.adofai`](others/a-dance-of-fire-and-ice/adofai/) A Dance of Fire and Ice level | A Dance of Fire and Ice | others | partial | No | [`others/a-dance-of-fire-and-ice/adofai`](others/a-dance-of-fire-and-ice/adofai/) |
| [`.aff`](others/arcaea/aff/) Arcaea chart (AFF) | Arcaea | others | complete | No | [`others/arcaea/aff`](others/arcaea/aff/) |
| [`songlist`](others/arcaea/songlist/) Arcaea songlist / packlist | Arcaea | others | stub | No | [`others/arcaea/songlist`](others/arcaea/songlist/) |
| [`.audica`](others/audica/audica/) Audica map package | Audica | others | partial | No | [`others/audica/audica`](others/audica/audica/) |
| [`*.dat`](others/beat-saber/dat/) Beat Saber beatmap (v2/v3/v4, Lightshow, BPMInfo) | Beat Saber | others | complete | No | [`others/beat-saber/dat`](others/beat-saber/dat/) |
| [`Info.dat`](others/beat-saber/info-dat/) Beat Saber Info (v1 info.json, v2, v4) | Beat Saber | others | complete | No | [`others/beat-saber/info-dat`](others/beat-saber/info-dat/) |
| [`level.json`](others/beatblock/level-json/) Beatblock level (JSON events) | Beatblock | others | stub | No | [`others/beatblock/level-json`](others/beatblock/level-json/) |
| [`.c2s`](others/chunithm/c2s/) C2S (CHUNITHM chart) | CHUNITHM (arcade) | others | partial | No | [`others/chunithm/c2s`](others/chunithm/c2s/) |
| [`.sus`](others/chunithm/sus/) SUS (Sliding Universal Score) | Seaurchin, UMIGURI, ched, Project Sekai tooling | others | partial | Decode only (as a Project SEKAI chart) | [`others/chunithm/sus`](others/chunithm/sus/) |
| [`.ugc`](others/chunithm/ugc/) UMIGURI Chart v8 | UMIGURI / Margrete (CHUNITHM simulator) | others | complete | No | [`others/chunithm/ugc`](others/chunithm/ugc/) |
| [`.txt (<song>.mp3.txt)`](others/crypt-of-the-necrodancer/beatmap-txt/) Crypt of the NecroDancer custom music beat file | Crypt of the NecroDancer | others | partial | No | [`others/crypt-of-the-necrodancer/beatmap-txt`](others/crypt-of-the-necrodancer/beatmap-txt/) |
| [`.txt`](others/cytus/c1-txt/) Cytus 1 chart ("Rayark v2 modified") | Cytus (Cytoid) | others | complete | No | [`others/cytus/c1-txt`](others/cytus/c1-txt/) |
| [`.json`](others/cytus/c2-json/) Cytus II / Cytoid chart (C2) | Cytus II (Cytoid) | others | partial | No | [`others/cytus/c2-json`](others/cytus/c2-json/) |
| [`.drb`](others/dancerail/drb/) DanceRail chart | DanceRail | others | partial | No | [`others/dancerail/drb`](others/dancerail/drb/) |
| [`.json`](others/deemo/json/) Deemo chart (JSON) | Deemo | others | partial | No | [`others/deemo/json`](others/deemo/json/) |
| [`.bytes`](others/djmax-technika-q/bytes/) DJMAX Technika Q song | DJMAX Technika Q | others | partial | No | [`others/djmax-technika-q/bytes`](others/djmax-technika-q/bytes/) |
| [`.mid`](others/donkey-konga/mid/) Donkey Konga score MIDI | Donkey Konga 2 (GameCube) | others | stub | No | [`others/donkey-konga/mid`](others/donkey-konga/mid/) |
| [`.csv`](others/drums-rock/notes-csv/) Drums Rock custom song (notes.csv + info.csv) | Drums Rock (VR drums) | others | complete | No | [`others/drums-rock/notes-csv`](others/drums-rock/notes-csv/) |
| [`.dy`](others/dynamix/dy/) Dynamaker bundle (.dy) | Dynamix | others | stub | No | [`others/dynamix/dy`](others/dynamix/dy/) |
| [`.xml`](others/dynamix/xml/) Dynamix chart XML | Dynamix | others | partial | No | [`others/dynamix/xml`](others/dynamix/xml/) |
| [`.json`](others/gadvia/chart-json/) Gadvia chart (JSON asset) | Gadvia | others | stub | No | [`others/gadvia/chart-json`](others/gadvia/chart-json/) |
| [`.chc`](others/gitaroo-man/chc/) Gitaroo Man stage chart (CHC) | Gitaroo Man / Gitaroo Man Lives! | others | partial | No | [`others/gitaroo-man/chc`](others/gitaroo-man/chc/) |
| [`.aar`](others/groove-coaster/aar/) AAR / ALAR archives (Groove Coaster) | Groove Coaster (Steam/arcade/Switch) | others | stub | No | [`others/groove-coaster/aar`](others/groove-coaster/aar/) |
| [`.eve`](others/jubeat/eve/) EVE (jubeat chart events) | jubeat (arcade) | others | complete | No | [`others/jubeat/eve`](others/jubeat/eve/) |
| [`.jbsq`](others/jubeat/jbsq/) JBSQ (jubeat binary sequence) | jubeat (Konami) | others | partial | No | [`others/jubeat/jbsq`](others/jubeat/jbsq/) |
| [`.txt (memo)`](others/jubeat/memo/) jubeat analyser memo formats (memo/memo1/memo2/boogie/mono-column/youbeat) | jubeat analyser (fan simulator) | others | partial | No | [`others/jubeat/memo`](others/jubeat/memo/) |
| [`.memon`](others/jubeat/memon/) memon (jubeat JSON chart set) | jubeat fan tools (F.E.I.S, jujube) | others | complete | No | [`others/jubeat/memon`](others/jubeat/memon/) |
| [`.dtape.ckd / .ktape.ckd`](others/just-dance/ubiart-tape/) Just Dance UbiArt tape (dance, karaoke) | Just Dance (UbiArt Framework versions, 2016-2022) | others | partial | No | [`others/just-dance/ubiart-tape`](others/just-dance/ubiart-tape/) |
| [`unknown`](others/lanota/lanotalium/) Lanotalium / Layesta fan chart | Lanota | others | stub | No | [`others/lanota/lanotalium`](others/lanota/lanotalium/) |
| [`.json`](others/love-live-sif/sift-json/) SIFTrain beatmap (Love Live! SIF live JSON) | Love Live! School Idol Festival | others | partial | No | [`others/love-live-sif/sift-json`](others/love-live-sif/sift-json/) |
| [`.ma2`](others/maimai/ma2/) MA2 (maimai DX chart) | maimai DX (arcade) | others | partial | No | [`others/maimai/ma2`](others/maimai/ma2/) |
| [`.sdt`](others/maimai/sdt/) SRT / SZT / SCT / SDT (maimai classic charts) | maimai (classic, pre-DX) | others | partial | No | [`others/maimai/sdt`](others/maimai/sdt/) |
| [`maidata.txt`](others/maimai/simai/) simai (maidata.txt, 'simai language') | maimai fan simulators (simai, MajdataEdit/MajdataPlay) | others | complete | No | [`others/maimai/simai`](others/maimai/simai/) |
| [`.bms`](others/muse-dash/bms/) Muse Dash BMS dialect | Muse Dash | others | partial | No | [`others/muse-dash/bms`](others/muse-dash/bms/) |
| [`.yml`](others/ohshape/yml/) OhShape level (YAML) | OhShape (VR fitness) | others | partial | No | [`others/ohshape/yml`](others/ohshape/yml/) |
| [`.ogkr`](others/ongeki/ogkr/) OGKR (ONGEKI chart) | ONGEKI (arcade) | others | partial | No | [`others/ongeki/ogkr`](others/ongeki/ogkr/) |
| [`.osu`](others/osu-catch/osu/) osu! beatmap (mode 2, osu!catch) | osu!catch (osu!) | others | partial | No | [`others/osu-catch/osu`](others/osu-catch/osu/) |
| [`.osu`](others/osu-standard/osu/) osu! beatmap (mode 0, osu!standard) | osu!standard (osu!) | others | partial | No | [`others/osu-standard/osu`](others/osu-standard/osu/) |
| [`.osu`](others/osu-taiko/osu/) osu! beatmap (mode 1, osu!taiko) | osu!taiko (osu!) | others | partial | Decode only | [`others/osu-taiko/osu`](others/osu-taiko/osu/) |
| [`.rlrr`](others/paradiddle/rlrr/) Paradiddle song / kit / recording (RLRR) | Paradiddle (VR drums) | others | complete | No | [`others/paradiddle/rlrr`](others/paradiddle/rlrr/) |
| [`unknown`](others/paradigm-reboot/chart/) Paradigm: Reboot chart | Paradigm: Reboot | others | stub | No | [`others/paradigm-reboot/chart`](others/paradigm-reboot/chart/) |
| [`.json`](others/phigros/official-json/) Phigros official chart | Phigros | others | complete | No | [`others/phigros/official-json`](others/phigros/official-json/) |
| [`.pec`](others/phigros/pec/) PhiEdit Chart (PEC) | Phigros (PhiEdit) | others | partial | No | [`others/phigros/pec`](others/phigros/pec/) |
| [`.json / protobuf`](others/phigros/phi-common-chart/) PhiCommonChart (PhiFanmade interchange model) | Phigros (PhiFanmade) | others | stub | No | [`others/phigros/phi-common-chart`](others/phigros/phi-common-chart/) |
| [`.json`](others/phigros/rpe/) Re:PhiEdit chart (RPEJSON) | Phigros (Re:PhiEdit) | others | partial | No | [`others/phigros/rpe`](others/phigros/rpe/) |
| [`.pw / .pw_beat`](others/pistol-whip/pwcl-level/) Pistol Whip Custom Levels folder (level.pw, .pw_beat, .pw_koreo, .pw_sec, .pw_geo) | Pistol Whip (PWCL community mod) | others | partial | No | [`others/pistol-whip/pwcl-level`](others/pistol-whip/pwcl-level/) |
| [`.dsc`](others/project-diva/dsc/) DSC (Project DIVA DivaScript) | Hatsune Miku: Project DIVA (PSP, arcade, f/F2nd/X, Future Tone, Mega Mix) and Project Mirai (3DS) | others | partial | No | [`others/project-diva/dsc`](others/project-diva/dsc/) |
| [`info.dat`](others/ragnarock/info-dat/) Ragnarock map (Beat Saber-derived) | Ragnarock | others | stub | No | [`others/ragnarock/info-dat`](others/ragnarock/info-dat/) |
| [`.rb`](others/reflec-beat/rb/) RB package (Reflec Beat plus iOS) | REFLEC BEAT plus | others | stub | No | [`others/reflec-beat/rb`](others/reflec-beat/rb/) |
| [`.rgc`](others/rgc/rgc/) RGC (Rhythm Game Chart) | Multi-game interchange (SDVX, DDR, osu!...) | others | complete | No | [`others/rgc/rgc`](others/rgc/rgc/) |
| [`.rdlevel`](others/rhythm-doctor/rdlevel/) Rhythm Doctor level | Rhythm Doctor | others | partial | No | [`others/rhythm-doctor/rdlevel`](others/rhythm-doctor/rdlevel/) |
| [`.bin / .tickflow`](others/rhythm-heaven/tickflow/) Rhythm Heaven Megamix / DS tickflow script | Rhythm Heaven Megamix (3DS) and Rhythm Heaven DS | others | partial | No | [`others/rhythm-heaven/tickflow`](others/rhythm-heaven/tickflow/) |
| [`.json`](others/rizline/chart-json/) Rizline chart (chart.json) | Rizline | others | complete | No | [`others/rizline/chart-json`](others/rizline/chart-json/) |
| [`.sng`](others/rocksmith/sng/) Rocksmith 2014 SNG (binary) | Rocksmith 2014 | others | stub | No | [`others/rocksmith/sng`](others/rocksmith/sng/) |
| [`.xml`](others/rocksmith/xml/) Rocksmith 2014 arrangement XML | Rocksmith 2014 | others | stub | No | [`others/rocksmith/xml`](others/rocksmith/xml/) |
| [`.txt`](others/rotaeno/chart-text/) Rotaeno chart text (as read by RotaenoChartTool) | Rotaeno | others | partial | No | [`others/rotaeno/chart-text`](others/rotaeno/chart-text/) |
| [`.indies`](others/smash-drums/indies/) Smash Drums Indies package | Smash Drums (VR drums) | others | partial | No | [`others/smash-drums/indies`](others/smash-drums/indies/) |
| [`.json (gzip)`](others/sonolus/level-data/) Sonolus Level Data | Sonolus (platform; Project SEKAI, Deemo and other fan engines) | others | complete | No | [`others/sonolus/level-data`](others/sonolus/level-data/) |
| [`.sspm`](others/sound-space/sspm/) Sound Space Plus / Rhythia map (v1, v2) | Sound Space Plus / Rhythia | others | complete | No | [`others/sound-space/sspm`](others/sound-space/sspm/) |
| [`.txt`](others/sound-space/txt/) Sound Space (Roblox) text map | Sound Space (Roblox) / SS+ | others | partial | No | [`others/sound-space/txt`](others/sound-space/txt/) |
| [`.bin (DGSH)`](others/space-channel-5/dgsh/) Space Channel 5 Part 2 DGSH sequence files | Space Channel 5: Part 2 (PC) | others | stub | No | [`others/space-channel-5/dgsh`](others/space-channel-5/dgsh/) |
| [`.srtb`](others/spin-rhythm-xd/srtb/) Spin Rhythm XD track bundle | Spin Rhythm XD (custom tracks, SpinShare) | others | partial | No | [`others/spin-rhythm-xd/srtb`](others/spin-rhythm-xd/srtb/) |
| [`.csv`](others/starlight-stage/csv/) CGSS beatmap CSV | THE iDOLM@STER Cinderella Girls Starlight Stage | others | partial | No | [`others/starlight-stage/csv`](others/starlight-stage/csv/) |
| [`.synth`](others/synth-riders/synth/) Synth Riders map | Synth Riders | others | partial | No | [`others/synth-riders/synth`](others/synth-riders/synth/) |
| [`.bin`](others/taiko-no-tatsujin/fumen/) Fumen (official Taiko no Tatsujin binary chart) | Taiko no Tatsujin (arcade, consoles, PC Drum Master) | others | partial | No | [`others/taiko-no-tatsujin/fumen`](others/taiko-no-tatsujin/fumen/) |
| [`.tcc`](others/taiko-no-tatsujin/tcc/) Open Taiko Chart (.tci/.tcc/.tcm JSON) | Koioto, TJAPlayer3-f, OpenTaiko | others | partial | No | [`others/taiko-no-tatsujin/tcc`](others/taiko-no-tatsujin/tcc/) |
| [`.tja`](others/taiko-no-tatsujin/tja/) TJA (Taiko Jiro chart) | Taiko no Tatsujin simulators (TaikoJiro, TJAPlayer2/3, OpenTaiko, taiko-web, OutFox); modes taiko, konga, jube | others | complete | No | [`others/taiko-no-tatsujin/tja`](others/taiko-no-tatsujin/tja/) |
| [`.tjf`](others/taiko-no-tatsujin/tjf/) TJF (Taikosan / TJF EDIT chart) | Taikosan, TaikoJiro 1 | others | stub | No | [`others/taiko-no-tatsujin/tjf`](others/taiko-no-tatsujin/tjf/) |
| [`.pc / .objlib`](others/thumper/objlib/) Thumper object library (leaf, level, gate, master) | Thumper | others | partial | No | [`others/thumper/objlib`](others/thumper/objlib/) |
| [`.tmb`](others/trombone-champ/tmb/) Trombone Champ custom track (song.tmb) | Trombone Champ (TrombLoader custom tracks) | others | complete | No | [`others/trombone-champ/tmb`](others/trombone-champ/tmb/) |
| [`.json`](others/voez/json/) VOEZ chart set (info / note / track JSON) | VOEZ | others | partial | No | [`others/voez/json`](others/voez/json/) |
| [`.json`](others/vulnus/json/) Vulnus map (meta.json + difficulty json) | Vulnus | others | stub | No | [`others/vulnus/json`](others/vulnus/json/) |
| [`.mer`](others/wacca/mer/) MER (WACCA / Mercury chart) | WACCA (arcade) | others | partial | No | [`others/wacca/mer`](others/wacca/mer/) |

## Game-by-game category decisions

| Game | Category | Why | Formats |
|---|---|---|---|
| [BanG Dream!](vsrg/bang-dream/) | vsrg | Seven fixed lanes with perspective approach to a bottom line (flick/slide are extras). | [`.bdon / .json`](vsrg/bang-dream/bdon/), [`.json`](vsrg/bang-dream/bestdori-json/), [`.txt`](vsrg/bang-dream/txt/) |
| [beatmania IIDX](vsrg/beatmania-iidx/) | vsrg | Seven keys plus scratch, vertical notes. | [`.1`](vsrg/beatmania-iidx/1/), [`.2dx`](vsrg/beatmania-iidx/2dx/) |
| [Bemuse](vsrg/bemuse/) | vsrg | Web player of BMS/bmson charts; vertical key lanes. | [`.bemuse`](vsrg/bemuse/bemuse/), [`bemuse-song.json / index.json`](vsrg/bemuse/bemuse-song-json/) |
| [BMS (Be-Music Script family)](vsrg/bms/) | vsrg | Keyboard lanes (5K/7K/9K/14K/PMS 9-button) with vertical notes. | [`.bms`](vsrg/bms/bms/), [`.bme`](vsrg/bms/bme/), [`.bml`](vsrg/bms/bml/), [`.pms`](vsrg/bms/pms/), [`.bmson`](vsrg/bms/bmson/), [`.ibmsc`](vsrg/bms/ibmsc/) |
| [Clone Hero](vsrg/clone-hero/) | vsrg | Five-lane fret highway; notes travel along fixed lanes to a strike line. | [`.chart`](vsrg/clone-hero/chart/), [`.mid`](vsrg/clone-hero/mid/), [`.ini`](vsrg/clone-hero/ini/) |
| [Dance Dance Revolution](vsrg/ddr/) | vsrg | Panel steps scroll vertically along fixed arrow columns. | [`.gen`](vsrg/ddr/gen/), [`.ssq (chunk 9)`](vsrg/ddr/hudson-ssq/), [`.ssq (chunk 16)`](vsrg/ddr/hudson-ssq-lane/), [`x_data_US.bin / .sng / .sif`](vsrg/ddr/ultramix-archive/), [`.msd`](vsrg/ddr/msd/), [`.ssq`](vsrg/ddr/ssq/), [`.sdf`](vsrg/ddr/sdf/), [`step`](vsrg/ddr/step/), [`step2`](vsrg/ddr/step2/) |
| [DJ Hero](vsrg/dj-hero/) | vsrg | Three tap lanes plus scratch zones and crossfader; lane-based with non-column extras. | [`.xmk`](vsrg/dj-hero/xmk/) |
| [DJMAX](vsrg/djmax/) | vsrg | DJMAX Online charts have 4-8 fixed lanes with vertical notes. | [`.pt`](vsrg/djmax/pt/) |
| [DTXMania](vsrg/dtxmania/) | vsrg | Drum/guitar/bass lanes with vertical notes. | [`.dtx`](vsrg/dtxmania/dtx/), [`.gda`](vsrg/dtxmania/gda/), [`.g2d`](vsrg/dtxmania/g2d/), [`set.def`](vsrg/dtxmania/set-def/) |
| [Dance With Intensity](vsrg/dwi/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.dwi`](vsrg/dwi/dwi/) |
| [EZ2DJ / EZ2AC](vsrg/ez2/) | vsrg | 5K/7K/14K lanes with turntable and pedal; vertical notes. | [`.ez`](vsrg/ez2/ez/), [`.ezi`](vsrg/ez2/ezi/) |
| [Etterna](vsrg/etterna/) | vsrg | StepMania 5.0 fork; vertical columns scrolling to a receptor row (charts are plain `.sm`/`.ssc`; own derived files below). | [`.ett`](vsrg/etterna/ett/) |
| [Flash Flash Revolution](vsrg/flash-flash-revolution/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.swf`](vsrg/flash-flash-revolution/swf/) |
| [fluXis](vsrg/fluxis/) | vsrg | Lane-based vertical game with key columns and scroll velocities. | [`.fsc`](vsrg/fluxis/fsc/), [`.ffx`](vsrg/fluxis/ffx/) |
| [Fortnite Festival](vsrg/fortnite-festival/) | vsrg | Five fixed lanes toward a strike line, Rock Band style. | [`.mid`](vsrg/fortnite-festival/mid/) |
| [Friday Night Funkin'](vsrg/friday-night-funkin/) | vsrg | Four arrow lanes per side scrolling vertically. | [`.json`](vsrg/friday-night-funkin/legacy-json/), [`.json`](vsrg/friday-night-funkin/psych-json/), [`.json`](vsrg/friday-night-funkin/kade-json/), [`.json`](vsrg/friday-night-funkin/codename-json/), [`.json`](vsrg/friday-night-funkin/fps-plus-json/), [`.json`](vsrg/friday-night-funkin/troll-json/), [`.json`](vsrg/friday-night-funkin/vslice-chart-json/), [`.json`](vsrg/friday-night-funkin/vslice-metadata-json/), [`.png`](vsrg/friday-night-funkin/ludum-dare-png/), [`.json`](vsrg/friday-night-funkin/nmv-json/), [`.json`](vsrg/friday-night-funkin/maru-json/) |
| [GITADORA](vsrg/gitadora/) | vsrg | Fixed drum and guitar/bass lanes. | [`.sq3`](vsrg/gitadora/sq3/), [`.sq2`](vsrg/gitadora/sq2/), [`.dsq/.gsq`](vsrg/gitadora/dsq/) |
| [Guitar Hero](vsrg/guitar-hero/) | vsrg | Five-lane note highway. | [`.mid`](vsrg/guitar-hero/gh12-mid/), [`.qb`](vsrg/guitar-hero/qb-chart/) |
| [Interlude](vsrg/interlude/) | vsrg | Fixed 3-10 lanes, vertical scrolling (`Chart.CheckForErrors` accepts 3..10 keys). | [`.yav`](vsrg/interlude/yav/) |
| [Kick It Up](vsrg/kick-it-up/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.ksf`](vsrg/kick-it-up/ksf/) |
| [Legacy dance formats](vsrg/legacy-dance-formats/) | vsrg | Old Japanese/PC dance simulators: panel steps along fixed columns. | [`.d2r`](vsrg/legacy-dance-formats/d2r/), [`.slo`](vsrg/legacy-dance-formats/slo/), [`.sul`](vsrg/legacy-dance-formats/sul/), [`.step`](vsrg/legacy-dance-formats/step/), [`.ftb`](vsrg/legacy-dance-formats/ftb/), [`directmove`](vsrg/legacy-dance-formats/directmove/) |
| [Malody](vsrg/malody/) | vsrg | Key mode (the bulk of charts) is a fixed-column vertical scroller; other modes share the container but are not column-based. | [`.mc`](vsrg/malody/mc/) |
| [Music Master](vsrg/music-master/) | vsrg | Lane-based vertical-scroll mobile game. | [`.xml`](vsrg/music-master/xml/) |
| [Music Times](vsrg/music-times/) | vsrg | Lane-based vertical-scroll mobile game. | [`.xml`](vsrg/music-times/xml/) |
| [Musync / MUSYNX](vsrg/musync/) | vsrg | Fixed key lanes (4K/6K) with falling notes. | [`.txt`](vsrg/musync/txt/) |
| [O2Jam](vsrg/o2jam/) | vsrg | Seven fixed lanes with vertical-falling notes. | [`.ojn`](vsrg/o2jam/ojn/), [`.ojm`](vsrg/o2jam/ojm/), [`OJNList.dat`](vsrg/o2jam/ojnlist-dat/), [`.xnt`](vsrg/o2jam/xnt/), [`.txt`](vsrg/o2jam/txt/) |
| [osu!mania](vsrg/osu-mania/) | vsrg | Fixed-column vertical charts (4K..10K+). | [`.osu`](vsrg/osu-mania/osu/), [`.osb`](vsrg/osu-mania/osb/) |
| [pop'n music](vsrg/pop-n-music/) | vsrg | Nine fixed button columns toward a judgement line. | [`(unknown)`](vsrg/pop-n-music/arcade-chart/) |
| [Project SEKAI](vsrg/project-sekai/) | vsrg | 12 fixed lanes on an integer lane/width grid, notes falling to a fixed line (borderline, like BanG Dream). | [`.pjsk / .json / .json.gz`](vsrg/project-sekai/pjsk/), [`.mmws / .ccmmws / .unchmmws`](vsrg/project-sekai/ccmmws/), [`.sus`](vsrg/project-sekai/holodori-sus/), [`.sus`](vsrg/project-sekai/sus/), [`.usc`](vsrg/project-sekai/usc/), [`.mmws`](vsrg/project-sekai/mmws/) |
| [Pump It Up](vsrg/pump-it-up/) | vsrg | Panel steps scroll vertically along 5 or 10 fixed columns. | [`.stx`](vsrg/pump-it-up/stx/), [`.not / .not5`](vsrg/pump-it-up/not/), [`.ucs`](vsrg/pump-it-up/ucs/) |
| [pydance](vsrg/pydance/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.dance`](vsrg/pydance/dance/) |
| [QQ Dance (mobile)](vsrg/qq-dance/) | vsrg | Star motion and traditional modes are lane-based; other modes are free-position but share the schema. | [`.xml`](vsrg/qq-dance/xml/) |
| [Quaver](vsrg/quaver/) | vsrg | Fixed 1-10 lanes (4K/7K mainly) scrolling vertically. | [`.qua`](vsrg/quaver/qua/) |
| [R2Beat](vsrg/r2beat/) | vsrg | Racing/rhythm hybrid (obstacle kinds up/down/left/right/diagonal/long); not lane-based, kept in vsrg as the closest category [inference]. Corrects the earlier "vertical-lane" guess (Newton wiki). | [`.xml`](vsrg/r2beat/xml/), [`.r2n`](vsrg/r2beat/r2n/) |
| [Rhythm Master](vsrg/rhythm-master/) | vsrg | 4/5/6 vertical lanes. | [`.imd`](vsrg/rhythm-master/imd/), [`.mde`](vsrg/rhythm-master/mde/), [`.json`](vsrg/rhythm-master/json/) |
| [Rhythm Open Exchange (ROX)](vsrg/rhythm-open-exchange/) | vsrg | Interchange format for column-based VSRG charts; fixed key count. | [`.rox`](vsrg/rhythm-open-exchange/rox/), [`.jrox`](vsrg/rhythm-open-exchange/jrox/), [`.yrox`](vsrg/rhythm-open-exchange/yrox/) |
| [RoBeats](vsrg/robeats/) | vsrg | Four fixed tracks scrolling vertically. | [`.lua`](vsrg/robeats/lua-songmap/) |
| [Rock Band](vsrg/rock-band/) | vsrg | Metadata for lane-based guitar/drum charts. | [`.dta`](vsrg/rock-band/dta/) |
| [SOUND VOLTEX](vsrg/sound-voltex/) | vsrg | Six button lanes plus two laser lanes (borderline: lasers are analog). | [`.ksh`](vsrg/sound-voltex/ksh/), [`.kson`](vsrg/sound-voltex/kson/), [`.vox`](vsrg/sound-voltex/vox/) |
| [soundsphere / rizu](vsrg/soundsphere/) | vsrg | Keyboard column VSRG engine. | [`.sph`](vsrg/soundsphere/sph/), [`.nanochart`](vsrg/soundsphere/nanochart/) |
| [StepMania / Etterna / ITG / NotITG / OutFox](vsrg/stepmania/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.crs`](vsrg/stepmania/crs/), [`.sm`](vsrg/stepmania/sm/), [`.ssc`](vsrg/stepmania/ssc/), [`.edit`](vsrg/stepmania/edit/) |
| [StepMania AMX](vsrg/stepmania-amx/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.sma`](vsrg/stepmania-amx/sma/) |
| [StepMania Micro](vsrg/stepmania-micro/) | vsrg | Panel steps scroll vertically along fixed columns. | [`.json`](vsrg/stepmania-micro/json/) |
| [Virtual Orchestra Studio](vsrg/vos/) | vsrg | Seven piano-style keys with falling note blocks. | [`.vos`](vsrg/vos/vos/) |
| [YARG](vsrg/yarg/) | vsrg | Lane-based guitar/drum charts. | (none, see the Clone Hero formats) |
| [A Dance of Fire and Ice](others/a-dance-of-fire-and-ice/) | others | Geometric tile path defined by angles, two orbiting planets; no lanes. | [`.adofai`](others/a-dance-of-fire-and-ice/adofai/) |
| [Arcaea](others/arcaea/) | others | Arcs in a 3D sky plane plus two ground lanes with a free-position model; not a pure column game. | [`.aff`](others/arcaea/aff/), [`songlist`](others/arcaea/songlist/) |
| [Audica](others/audica/) | others | VR aim targets at free positions on a grid; no lanes. | [`.audica`](others/audica/audica/) |
| [Beat Saber](others/beat-saber/) | others | Free 3D notes on a 4x3 grid with cut directions, arcs, chains and walls. | [`Info.dat`](others/beat-saber/info-dat/), [`*.dat`](others/beat-saber/dat/) |
| [Beatblock](others/beatblock/) | others | Notes arrive radially around a central paddle; no lanes. | [`level.json`](others/beatblock/level-json/) |
| [CHUNITHM](others/chunithm/) | others | 16 cells with variable-width notes and an air plane; vertical, but not a column model (borderline). | [`.c2s`](others/chunithm/c2s/), [`.ugc`](others/chunithm/ugc/), [`.sus`](others/chunithm/sus/) |
| [Crypt of the NecroDancer](others/crypt-of-the-necrodancer/) | others | Rhythm roguelike on a tile map; the file holds only a beat grid. | [`.txt (<song>.mp3.txt)`](others/crypt-of-the-necrodancer/beatmap-txt/) |
| [Cytus / Cytoid](others/cytus/) | others | Scanline game; notes at arbitrary x on pages. | [`.json`](others/cytus/c2-json/), [`.txt`](others/cytus/c1-txt/) |
| [DanceRail](others/dancerail/) | others | Free x-position and width, camera changes; not fixed columns. | [`.drb`](others/dancerail/drb/) |
| [Deemo](others/deemo/) | others | Continuous x/width notes and piano keysounds; not fixed columns. | [`.json`](others/deemo/json/) |
| [DJMAX Technika Q](others/djmax-technika-q/) | others | Touch game with drag/chain/repeat notes on three lines; not a column model. | [`.bytes`](others/djmax-technika-q/bytes/) |
| [Donkey Konga](others/donkey-konga/) | others | Horizontal bongo track like Taiko. | [`.mid`](others/donkey-konga/mid/) |
| [Drums Rock](others/drums-rock/) | others | VR drum game; six drums behave like lanes but the play space is 3D (judgement call, could be vsrg). | [`.csv`](others/drums-rock/notes-csv/) |
| [Dynamix](others/dynamix/) | others | Three-sided free-position notes and sides; not columns. | [`.xml`](others/dynamix/xml/), [`.dy`](others/dynamix/dy/) |
| [Osu! Tatakae! Ouendan / Elite Beat Agents](others/elite-beat-agents/) | others | Free-position touch notes on the DS screen; no public format found. | none (see game page) |
| [Gadvia](others/gadvia/) | others | Notes carry 3D positions and lyric words; no documented column layout. | [`.json`](others/gadvia/chart-json/) |
| [Gitaroo Man](others/gitaroo-man/) | others | Stick-steered trace lines with continuous angles; not column-based. | [`.chc`](others/gitaroo-man/chc/) |
| [Groove Coaster](others/groove-coaster/) | others | Notes follow a free 3D rail. | [`.aar`](others/groove-coaster/aar/) |
| [jubeat](others/jubeat/) | others | 4x4 panel grid, not lanes. | [`.eve`](others/jubeat/eve/), [`.jbsq`](others/jubeat/jbsq/), [`.txt (memo)`](others/jubeat/memo/), [`.memon`](others/jubeat/memon/) |
| [Just Dance](others/just-dance/) | others | Motion-scored dance game; the chart is a clip timeline. | [`.dtape.ckd / .ktape.ckd`](others/just-dance/ubiart-tape/) |
| [Lanota](others/lanota/) | others | Rotating disc with concentric rings; angular, not columnar. | [`unknown`](others/lanota/lanotalium/) |
| [Love Live! School Idol Festival](others/love-live-sif/) | others | Radial travel to 9 circles on a semicircle. | [`.json`](others/love-live-sif/sift-json/) |
| [maimai](others/maimai/) | others | Radial layout with 8 buttons and slides. | [`.ma2`](others/maimai/ma2/), [`maidata.txt`](others/maimai/simai/), [`.sdt`](others/maimai/sdt/) |
| [Muse Dash](others/muse-dash/) | others | Horizontal two-lane (air/ground) runner. | [`.bms`](others/muse-dash/bms/) |
| [NOSTALGIA](others/nostalgia/) | others | Piano keys at continuous positions with moving ranges; no public format found. | none (see game page) |
| [OhShape](others/ohshape/) | others | Full-body pose walls; no lanes. | [`.yml`](others/ohshape/yml/) |
| [ONGEKI](others/ongeki/) | others | Free horizontal positions, bending lanes, bullets and beams. | [`.ogkr`](others/ongeki/ogkr/) |
| [osu!catch](others/osu-catch/) | others | Free horizontal position (x 0-512) of falling fruits. | [`.osu`](others/osu-catch/osu/) |
| [osu!standard](others/osu-standard/) | others | Free 2D positions and curved slider paths. | [`.osu`](others/osu-standard/osu/) |
| [osu!taiko](others/osu-taiko/) | others | Horizontal scroll with don/kat inputs only. | [`.osu`](others/osu-taiko/osu/) |
| [Paradiddle](others/paradiddle/) | others | VR drum kit; notes target named instruments, no lane index. | [`.rlrr`](others/paradiddle/rlrr/) |
| [Paradigm: Reboot](others/paradigm-reboot/) | others | Placement model unknown; tentative `others` pending a spec. | [`unknown`](others/paradigm-reboot/chart/) |
| [Phigros](others/phigros/) | others | Free judgement lines that move, rotate and scale. | [`.json`](others/phigros/official-json/), [`.json`](others/phigros/rpe/), [`.pec`](others/phigros/pec/), [`.json / protobuf`](others/phigros/phi-common-chart/) |
| [Pistol Whip](others/pistol-whip/) | others | Targets as enemies on a 3D path; no lanes. | [`.pw / .pw_beat`](others/pistol-whip/pwcl-level/) |
| [Hatsune Miku: Project DIVA](others/project-diva/) | others | Targets at free screen positions with trajectories inside a PV script. | [`.dsc`](others/project-diva/dsc/) |
| [Ragnarock](others/ragnarock/) | others | VR drumming hit targets, format derived from Beat Saber. | [`info.dat`](others/ragnarock/info-dat/) |
| [REFLEC BEAT](others/reflec-beat/) | others | Free 2D positions with reflecting trajectories. | [`.rb`](others/reflec-beat/rb/) |
| [RGC (Rhythm Game Chart)](others/rgc/) | others | Game-agnostic JSON model with n-dimensional positions; not column-bound. | [`.rgc`](others/rgc/rgc/) |
| [Rhythia](others/rhythia/) | others | Free-position notes on a 3x3 grid hit with a cursor (formats shared with Sound Space). | none (see game page) |
| [Rhythm Doctor](others/rhythm-doctor/) | others | One-button game, event timeline by bar/beat; no key lanes. | [`.rdlevel`](others/rhythm-doctor/rdlevel/) |
| [Rhythm Heaven](others/rhythm-heaven/) | others | Minigame cue/event timeline, not notes on lanes. | [`.bin / .tickflow`](others/rhythm-heaven/tickflow/) |
| [Rizline](others/rizline/) | others | Notes ride freely shaped lines on moving canvases. | [`.json`](others/rizline/chart-json/) |
| [Rocksmith](others/rocksmith/) | others | (string, fret) pairs with techniques on a guitar highway. | [`.xml`](others/rocksmith/xml/), [`.sng`](others/rocksmith/sng/) |
| [Rotaeno](others/rotaeno/) | others | Angular dial driven by device rotation. | [`.txt`](others/rotaeno/chart-text/) |
| [Smash Drums](others/smash-drums/) | others | VR drum game; six instruments act as lanes but the play space is 3D (judgement call). | [`.indies`](others/smash-drums/indies/) |
| [Sonolus](others/sonolus/) | others | Game-agnostic platform: engines define their own charts. | [`.json (gzip)`](others/sonolus/level-data/) |
| [Sound Space / Sound Space Plus](others/sound-space/) | others | 3x3 grid notes hit with a cursor. | [`.sspm`](others/sound-space/sspm/), [`.txt`](others/sound-space/txt/) |
| [Space Channel 5](others/space-channel-5/) | others | Call-and-response scripted sequences. | [`.bin (DGSH)`](others/space-channel-5/dgsh/) |
| [Spin Rhythm XD](others/spin-rhythm-xd/) | others | Turntable wheel with spins and scratches along a 3D track. | [`.srtb`](others/spin-rhythm-xd/srtb/) |
| [THE iDOLM@STER Cinderella Girls Starlight Stage](others/starlight-stage/) | others | Fan-shaped travel from a vanishing point to 5 positions. | [`.csv`](others/starlight-stage/csv/) |
| [Synth Riders](others/synth-riders/) | others | Free 2D positions and rails on a z-axis track. | [`.synth`](others/synth-riders/synth/) |
| [Taiko no Tatsujin](others/taiko-no-tatsujin/) | others | Horizontal drum track with don/kat; per-measure scroll speed and branches. | [`.tja`](others/taiko-no-tatsujin/tja/), [`.bin`](others/taiko-no-tatsujin/fumen/), [`.tjf`](others/taiko-no-tatsujin/tjf/), [`.tcc`](others/taiko-no-tatsujin/tcc/) |
| [Thumper](others/thumper/) | others | Beat-timed sequencer tracks on a 3D rail; no columns. | [`.pc / .objlib`](others/thumper/objlib/) |
| [Trombone Champ](others/trombone-champ/) | others | Notes are pitch ribbons on a continuous pitch axis. | [`.tmb`](others/trombone-champ/tmb/) |
| [VOEZ](others/voez/) | others | Notes ride free-moving, resizable tracks. | [`.json`](others/voez/json/) |
| [Vulnus](others/vulnus/) | others | Cursor-aimed notes on a small grid. | [`.json`](others/vulnus/json/) |
| [WACCA](others/wacca/) | others | Circular ring of 60 positions with variable-width arcs. | [`.mer`](others/wacca/mer/) |

## Known without a format page

Games with a page but no chart-format folder: [NOSTALGIA](others/nostalgia/), [Osu! Tatakae! Ouendan / Elite Beat Agents](others/elite-beat-agents/) (no public chart format found), [Rhythia](others/rhythia/) (shares Sound Space's [`.sspm`](others/sound-space/sspm/)).
Investigated, no public format found, so no folder: osu!stream (`.osc`/`.osz2`), Unplugged (`.usm` is a third-party manager archive), Audition Online (only the undocumented `.arp` replay), KeyboardMania, Pump It Up arcade `.pak`/`.nxa`, DDR Freestyle, Dance Dance Immolation, `.pump`/`.nx`/`.ddr`, Funky Friday, Taptap Heroes, Dancing Line, Rhythm Cat, Tone Sphere, Beat Fever, Ensemble Stars, Uta no Prince, D4DJ, Girls Band Cry, Geometry Dash, Soundboxing, BoxVR/FitXR. Historic BMS dialects (MGQ, MBM, EMS, KMS) are listed in [`vsrg/bms/README.md`](vsrg/bms/) without a spec. `.fnfm` was requested but no such format was found (nearest: `.fnfc`, `.fnfmod`). Not investigated: Tap Tap Revolution, Rhythm Hive, Rhythm Game Maker, Raindrop `.dcf`, the FNF engines Forever / Leather / Andromeda.

## History

- Upstream list at commit `503382a` (2020-12-09); its `*-samples/` and `ojn-docs/` moved, unchanged, into `<format>/samples/` and `vsrg/o2jam/ojn/docs/`.
- Added since: one page per format and game, the sample corpus (about 2 000 real charts), the package table, `FORMATS.md` and `tools/gen_formats.py`.
