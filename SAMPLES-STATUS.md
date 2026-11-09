# Samples status

Real chart files per format of the [README index](README.md), all committed under `<format>/samples/` (charts only: no audio, video, images, and no archive or package of any kind; archives were opened and only their chart files kept). Origin URL, fetch date, author and licence/terms of every file are in the `samples/SOURCES.md` of each format; the "Getting samples" section of each format page says how to get more.

- Formats: **182** (chart formats only; packages such as `.osz`, `.qp`, `.fnfc` are listed in the README, section Packages). With at least 5 real charts: **115**. With 1 to 4 real charts: **18**. With no real chart: **49** (no public copy).
- Committed files: **2426** (including `SOURCES.md`-listed synthetic and converted files; the "Real" column below counts only real charts).
- "Real" = a chart written by a game, a tool or a person for actual play or for a real test, downloaded from a public source. "Synthetic" = hand-written or script-written here (CC0). Converted files (made by running a converter on a real chart) are not counted as real unless the SOURCES.md says the converter output was published by someone else.
- The 33 `.png` files of `vsrg/friday-night-funkin/ludum-dare-png` are the chart data itself (one tiny PNG per section, 12 rows high, no artwork); they are the only images in the repo.

## vsrg

| Format | Real | Synthetic / other | Why fewer than 5 real files, and how to get more |
|---|---:|---:|---|
| [`vsrg/bang-dream/bdon`](vsrg/bang-dream/bdon/) `.bdon / .json` BDON (BanG Dream! Our Notes) chart | 6 | 0 | git sparse-checkout of jp/original or intl/original in haneoka-gakuen/ournotes-charts |
| [`vsrg/bang-dream/bestdori-json`](vsrg/bang-dream/bestdori-json/) `.json` Bestdori chart (v2 JSON) | 13 | 1 | bestdori.com/api/charts/<songId>/<difficulty>.json and /api/post/details?id=<id> |
| [`vsrg/bang-dream/txt`](vsrg/bang-dream/txt/) `.txt` BanG! Simulator chart (txt) | 9 | 7 | BanGConverter in a browser on any Bestdori/official chart |
| [`vsrg/beatmania-iidx/1`](vsrg/beatmania-iidx/1/) `.1` beatmania IIDX arcade chart archive (.1) | 0 | 0 | Konami arcade data exists only inside a game install (contents/data/sound/<id>/<id>.1 or <id>.ifs); no public copy found in GitHub path search (Sourcegraph), parser/converter repos, archive.org or web search; Own an IIDX install: unpack <id>.ifs with ifstools, run iidx2bms or iidx-datatools parse_chart_notecounts.py on the .1 |
| [`vsrg/beatmania-iidx/2dx`](vsrg/beatmania-iidx/2dx/) `.2dx` beatmania IIDX keysound archive (2DX9 container) | 0 | 0 | Copyrighted keysound audio container exists only inside a game install and is audio, which the repo does not accept; no public copy found; Own an IIDX or pop'n install: <id>.2dx / <id>_pre.2dx (loose or inside .ifs), split with 2dx_extract or 2dxTools |
| [`vsrg/bemuse/bemuse`](vsrg/bemuse/bemuse/) `.bemuse` Bemuse sound pack (+ metadata.json) | 9 | 0 | other songs of bemuse.ninja/music/<song>/assets/metadata.json (chunks are audio, not stored) |
| [`vsrg/bemuse/bemuse-song-json`](vsrg/bemuse/bemuse-song-json/) `bemuse-song.json / index.json` Bemuse song metadata and music server index | 8 | 1 | music4.bemuse.ninja/songs/<id>/bemuse-song.json for the 42 ids in index.json |
| [`vsrg/bms/bme`](vsrg/bms/bme/) `.bme` Be-Music Extend (BME) chart, 7 keys + scratch | 55 | 0 | Same sources; 7K IIDX-style packs, iidx2bms output; bemusic/music has 87 .bme (41 committed) |
| [`vsrg/bms/bml`](vsrg/bms/bml/) `.bml` Be-Music Longnote (BML) chart | 13 | 1 | Same sources; any pack, search for *.bml or #LNOBJ (all 10 bemusic/music .bml are committed) |
| [`vsrg/bms/bms`](vsrg/bms/bms/) `.bms` Be-Music Source (BMS) chart | 99 | 6 | BMS Search, BMS of Fighters/manbow event pages, GENOSIDE starter packs, github.com/bemusic/music (221 charts, 62 more not yet committed), GenerationMania repo holds BOF packs |
| [`vsrg/bms/bmson`](vsrg/bms/bmson/) `.bmson` bmson 1.0.0 (JSON BMS successor) | 5 | 1 | more bmson only via Bemuse server (only onlylove_remix) or converters bms2bmson-python/bms-rs |
| [`vsrg/bms/ibmsc`](vsrg/bms/ibmsc/) `.ibmsc` iBMSC project file | 0 | 7 | no genuine editor-saved .ibmsc is public; the 5 committed files are real BMS charts converted to .ibmsc by a script (never opened in iBMSC); save any .bms as .ibmsc from iBMSC/uBMSC/pBMSC (rechecked: zardoru/iBMSC, RM-801/iBMSC-electron, asdfghjkoiuy/iBMSCPP, c0linw/BMSdori, Pulsus contain no .ibmsc) |
| [`vsrg/bms/pms`](vsrg/bms/pms/) `.pms` feeling-PoMu Script (PMS), 9-button BMS dialect | 23 | 59 | PMS Database releases (github.com/pmsdatabase/pmsdatabase.github.io/releases: bofu2016pms 21.7 MB, bofxv19pms, bofxvipms, bofxviipms, bofetpms, bofntpms, bofttpms, bof21pms not yet committed) |
| [`vsrg/clone-hero/chart`](vsrg/clone-hero/chart/) `.chart` Clone Hero / Moonscraper chart | 9 | 4 | Chorus Encore API (api.enchor.us) + files.enchor.us .sng downloads; Stickheadz32 and other GitHub chart repos; archive.org items with Clone Hero charts |
| [`vsrg/clone-hero/ini`](vsrg/clone-hero/ini/) `.ini` Clone Hero song.ini metadata | 15 | 3 | song.ini ships beside every chart folder; archive.org TheGreatNi charts, GitHub chart repos |
| [`vsrg/clone-hero/mid`](vsrg/clone-hero/mid/) `.mid` Rock Band / Clone Hero MIDI chart (notes.mid) | 17 | 0 | Chorus Encore .sng notes.mid, Onyx repo songs-*/ folders, archive.org TheGreatNi's Guitar Hero Charts, YARG.Core test fixtures |
| [`vsrg/ddr/gen`](vsrg/ddr/gen/) `.gen` DDR S+ song container (iOS) | 0 | 0 | every .gen embeds Blowfish-encrypted full-song and preview MP3 (audio) and the only public copies are 3 in the DDR S+ Lite IPA on archive.org; none in tool repos; download DanceDanceRevolution S Lite (US) IPA from archive.org item ios-ipa-com.konami.ddrslite and unzip Payload/DDRSPlusUS.app/*.gen; or buy songs in the DDR S+ app |
| [`vsrg/ddr/hudson-ssq`](vsrg/ddr/hudson-ssq/) `.ssq (chunk 9)` Hudson SSQ type 9 step chunk | 0 | 0 | only multi-GB Wii/GameCube disc images exist publicly (archive.org) and no chart extract or fixture is published; dump an owned Hottest Party 1 / Mario Mix disc and read type-9 SSQ chunks with skogaby/ddr-chart-tools |
| [`vsrg/ddr/hudson-ssq-lane`](vsrg/ddr/hudson-ssq-lane/) `.ssq (chunk 16)` Hudson SSQ type 16 lane-format chunk | 0 | 0 | only multi-GB Wii disc images exist publicly (archive.org) and no chart extract or fixture is published; dump an owned Hottest Party 4/5 disc and read type-16 SSQ chunks with skogaby/ddr-chart-tools |
| [`vsrg/ddr/msd`](vsrg/ddr/msd/) `.msd` MSD step script | 7 | 1 | other Wayback captures of doremi.kalin.to/ddr/ (only these 7 .msd were captured) |
| [`vsrg/ddr/sdf`](vsrg/ddr/sdf/) `.sdf` Pocket DDR chart | 2 | 0 | only the 2 sample files of the StepMania docs exist publicly (Pocket DDR itself is not hosted anywhere found); convert any .sm with SM2SDF (Pocket DDR converter) if the tool can be found |
| [`vsrg/ddr/ssq`](vsrg/ddr/ssq/) `.ssq` DDR SSQ step data | 31 | 0 | archive.org items DDR_S_1.0.1/1.0.3 IPAs (more .ssq in other versions), any owned DDR arcade/console data, ddr-chart-tools extractors |
| [`vsrg/ddr/step`](vsrg/ddr/step/) `step` DDR STEP (1st-3rd Mix, DDR Utility) | 3 | 0 | only 3 public fixtures exist (RhythmCodex test data); no other source found on GitHub or archive.org; DDR Utility export from owned DDR 2nd-3rd Mix/Solo data (see rhythm-game-formats ddr/step.md) |
| [`vsrg/ddr/step2`](vsrg/ddr/step2/) `step2` DDR STEP2 (1st Mix) | 3 | 0 | only 3 public fixtures exist (RhythmCodex test data); format exists only in DDR 1st Mix; DDR Utility export from owned DDR 1st Mix data |
| [`vsrg/ddr/ultramix-archive`](vsrg/ddr/ultramix-archive/) `x_data_US.bin / .sng / .sif` DDR Ultramix archives | 0 | 0 | container-sized (100+ MB) Xbox asset archive of a commercial game with no public copy found; it is also an archive, not a chart; rip an owned DDR Ultramix (Xbox) disc and run ddr-chart-tools scripts/extract_ultramix_data.py (charts are legacy SSQ) |
| [`vsrg/dj-hero/xmk`](vsrg/dj-hero/xmk/) `.xmk` DJ Hero chart (xmk) | 13 | 0 | archive.org DJ-HERO-CUSTOMS-ARCHIVE has ~400 more customs (zip central directories readable by HTTP range) |
| [`vsrg/djmax/pt`](vsrg/djmax/pt/) `.pt` DJMAX pattern (PTFF) | 0 | 7 | the 7 committed files are DJMAX Technika Q server pattern payloads of unknown relation to PTFF .pt; no real PTFF .pt is public; more Patterns/<id> files in UrsulaProject/DMTQResearch (4266 there) or extract .pt from an own DJMAX install |
| [`vsrg/dtxmania/dtx`](vsrg/dtxmania/dtx/) `.dtx` DTXMania chart | 24 | 4 | DTXMania chart libraries and YouTube/blog links (APPROVED DTX, Furukon), dtxmania.net, seqtool.py SQ3->DTX; Internet Archive was offline during this pass |
| [`vsrg/dtxmania/g2d`](vsrg/dtxmania/g2d/) `.g2d` DTXMania older chart (G2D) | 5 | 1 | larger packs of archive.org raredtxgda/raredtxgda2 |
| [`vsrg/dtxmania/gda`](vsrg/dtxmania/gda/) `.gda` DTXMania older chart (GDA) | 18 | 1 | ~358 .gda in the smaller packs of archive.org raredtxgda/raredtxgda2 (RAR, extract with bsdtar) |
| [`vsrg/dtxmania/set-def`](vsrg/dtxmania/set-def/) `set.def` DTXMania song set descriptor | 15 | 3 | more packs in archive.org items raredtxgda/raredtxgda2 (RAR per charter, 64 set.def counted in the smaller ones) |
| [`vsrg/dwi/dwi`](vsrg/dwi/dwi/) `.dwi` Dance With Intensity step file | 48 | 1 | archive.org DWIExtreme* items (dwi-extreme-all 4.9 GB), simfile-parser packs, the other pack folders of dwi.ddruk.com |
| [`vsrg/etterna/ett`](vsrg/etterna/ett/) `.ett` Etterna song file (write-only) | 0 | 0 | write-only format with no caller in the Etterna source; no file exists anywhere reachable; build Etterna from source and call Song::SaveToETTFile from code |
| [`vsrg/ez2/ez`](vsrg/ez2/ez/) `.ez` EZ2DJ/EZ2AC chart (EZFF) | 11 | 0 | archive.org items 19990420_, 20000807_, 20020728_ (RARs of PC EZ2DJ editions: only the first 40-45 MB were read, i.e. 3 songs; later songs need the whole 1-2 GB RAR) and the 7-13 GB HDD images |
| [`vsrg/ez2/ezi`](vsrg/ez2/ezi/) `.ezi` EZ2AC keysound index | 11 | 0 | same RARs as .ez |
| [`vsrg/flash-flash-revolution/swf`](vsrg/flash-flash-revolution/swf/) `.swf` FFR legacy level SWF (beatBox) | 7 | 1 | any playhash of https://www.flashflashrevolution.com/game/r3/r3-playlist.php via r3-songLoad.php (audio stripped) |
| [`vsrg/fluxis/ffx`](vsrg/fluxis/ffx/) `.ffx` fluXis effects file | 6 | 0 | unzip any mapset from fluxis.flux.moe/api/mapsets/<id>/download |
| [`vsrg/fluxis/fsc`](vsrg/fluxis/fsc/) `.fsc` fluXis map | 9 | 0 | https://fluxis.flux.moe/api/mapsets/<id>/download then unzip (ids from /maps) |
| [`vsrg/fortnite-festival/mid`](vsrg/fortnite-festival/mid/) `.mid` Fortnite Festival chart MIDI | 0 | 0 | charts are encrypted in the game data; no public decrypted .mid found (extractor tools and stems-only archive.org items); Festival-MIDI-Extractor or Fest2CH on your own account |
| [`vsrg/friday-night-funkin/codename-json`](vsrg/friday-night-funkin/codename-json/) `.json` FNF Codename Engine chart + meta.json | 8 | 3 | Codename mods on GameBanana, engine assets/songs |
| [`vsrg/friday-night-funkin/fps-plus-json`](vsrg/friday-night-funkin/fps-plus-json/) `.json` FNF FPS Plus chart + meta/events | 6 | 4 | FPS-Plus-Public assets/data/songs (all songs) |
| [`vsrg/friday-night-funkin/kade-json`](vsrg/friday-night-funkin/kade-json/) `.json` FNF Kade Engine chart (KE1) | 10 | 2 | Perkedel/Kaded-fnf-mods has about 200 more Kade charts |
| [`vsrg/friday-night-funkin/legacy-json`](vsrg/friday-night-funkin/legacy-json/) `.json` FNF legacy week chart (song.notes[].sectionNotes) | 6 | 2 | Funkin tag v0.2.7.1 assets/data, Kade/Psych repos, GameBanana mods |
| [`vsrg/friday-night-funkin/ludum-dare-png`](vsrg/friday-night-funkin/ludum-dare-png/) `.png` FNF Ludum Dare chart (PNG per section) | 33 | 5 | only bopeebo and fresh exist in tag 1.0.0 |
| [`vsrg/friday-night-funkin/maru-json`](vsrg/friday-night-funkin/maru-json/) `.json` FNF Maru Funkin' chart | 6 | 1 | GameBanana Maru Funkin mods (range-read zips) |
| [`vsrg/friday-night-funkin/nmv-json`](vsrg/friday-night-funkin/nmv-json/) `.json` FNF Nightmare Vision chart (nmv2) | 5 | 2 | GameBanana NightmareVision mods |
| [`vsrg/friday-night-funkin/psych-json`](vsrg/friday-night-funkin/psych-json/) `.json` FNF Psych Engine chart (psych_v1) | 15 | 4 | GameBanana Psych mods, Psych repo tags |
| [`vsrg/friday-night-funkin/troll-json`](vsrg/friday-night-funkin/troll-json/) `.json` FNF Troll Engine chart | 6 | 1 | Troll Engine default_content/example_content |
| [`vsrg/friday-night-funkin/vslice-chart-json`](vsrg/friday-night-funkin/vslice-chart-json/) `.json` FNF V-Slice chart data (-chart.json) | 22 | 2 | GameBanana .fnfc mods (API search fnfc), funkin.assets |
| [`vsrg/friday-night-funkin/vslice-metadata-json`](vsrg/friday-night-funkin/vslice-metadata-json/) `.json` FNF V-Slice song metadata (-metadata.json) | 18 | 2 | GameBanana .fnfc mods, funkin.assets |
| [`vsrg/gitadora/dsq`](vsrg/gitadora/dsq/) `.dsq/.gsq` Older DrumMania/GuitarFreaks sequences | 0 | 0 | No .dsq/.gsq is public (gitadora-customs/gitadora-tools ship plugins only, data comes from Konami IFS archives); extract from own GF/DM data, convert with gitadora-customs seqtool.py |
| [`vsrg/gitadora/sq2`](vsrg/gitadora/sq2/) `.sq2` GuitarFreaks/DrumMania sequence | 0 | 0 | No .sq2 is public (same reason); extract from own GF/DM data, gitadora-customs plugins/sq2.py |
| [`vsrg/gitadora/sq3`](vsrg/gitadora/sq3/) `.sq3` GITADORA sequence (SEQP/SQ3T) | 0 | 0 | No .sq3 is public (same reason); extract m<id>_seq.ifs from an own GITADORA install, or write SQ3 from DTX with gitadora-customs seqtool.py |
| [`vsrg/guitar-hero/gh12-mid`](vsrg/guitar-hero/gh12-mid/) `.mid` Guitar Hero 1/2 MIDI chart | 6 | 2 | Milohax-archive/gh2-customs has ~190 more GH2 customs; GH1/GH2 originals only from the commercial discs |
| [`vsrg/guitar-hero/qb-chart`](vsrg/guitar-hero/qb-chart/) `.qb` Neversoft Guitar Hero chart (QB) | 0 | 0 | GH3 charts exist only inside PAK/WAD containers (PS2 ISOs and PC qb.pak.xen on archive.org); no loose .mid.qb in any repo/item searched, Sourcegraph/GitHub code search unavailable (rate-limited/login); compile a .mid with Addys-Guitar-Hero-Toolkit/Honeycomb or extract from your own GH3 PAK |
| [`vsrg/interlude/yav`](vsrg/interlude/yav/) `.yav` Interlude binary chart (legacy file, now database/CDN blob) | 7 | 1 | cdn.yavsrg.net/<hash> from YAVSRG backbeat/archive/charts.json (most 404 now), or SQLite charts.Chart of an Interlude install |
| [`vsrg/kick-it-up/ksf`](vsrg/kick-it-up/ksf/) `.ksf` Kick It Up step file (+Direct Move) | 7 | 0 | Kick It Up / DirectMove song folders, StepMania-AMX/KickItUp repository |
| [`vsrg/legacy-dance-formats/d2r`](vsrg/legacy-dance-formats/d2r/) `.d2r` Dazzle Dazzle Realization chart | 0 | 1 | no real .d2r survives in reachable archives (D2R chart-search site pages are on Wayback but link to dead personal sites; editor zips contain no sample); only a synthetic file is committed; run D2REDIT (Wayback copy of paramax.hypermart.net/d2redit.zip) or find old D2R 2ndMIX charts on personal sites |
| [`vsrg/legacy-dance-formats/directmove`](vsrg/legacy-dance-formats/directmove/) `directmove` Direct Move (extended KSF) | 0 | 0 | no DirectMove-variant .ksf (with \|T/\|B control rows) found on GitHub or archive.org; install Direct Move (Korean simulator) and copy its song-folder .ksf files, or build KSFCreator from StepMania-AMX/directmove |
| [`vsrg/legacy-dance-formats/ftb`](vsrg/legacy-dance-formats/ftb/) `.ftb` Raindrop FTB chart | 0 | 1 | no real .ftb exists in any reachable repository (Raindrop tests have .osu/.ssc only); only a synthetic file is committed; load an .ftb-based song folder in zardoru/raindrop if one can be found |
| [`vsrg/legacy-dance-formats/slo`](vsrg/legacy-dance-formats/slo/) `.slo` SLOEDIT chart | 0 | 0 | no .slo file or grammar found anywhere reachable (only the SloEdit tool and its slohead.txt template on Wayback); run SloEdit.exe from the Wayback sloedit.zip and save a chart |
| [`vsrg/legacy-dance-formats/step`](vsrg/legacy-dance-formats/step/) `.step` pyDDR/pydance .step | 2 | 0 | only 2 .step URLs were captured by Wayback (0forkbomb, 6jan); pydance 0.7/0.8 tarballs are 404 in Wayback; older pyDDR releases, Text Text Revolution songs |
| [`vsrg/legacy-dance-formats/sul`](vsrg/legacy-dance-formats/sul/) `.sul` D2R legacy chart | 0 | 0 | no .sul file found anywhere reachable; run D2REDIT on charts of the earlier D2R, or convert .d2r with d2r2sul (tool not found online) |
| [`vsrg/malody/mc`](vsrg/malody/mc/) `.mc` Malody chart (JSON) | 32 | 3 | Malody store (login required) or editor; GitHub repos with .mc |
| [`vsrg/music-master/xml`](vsrg/music-master/xml/) `.xml` Music Master chart | 0 | 0 | No public copy found: charts only inside the 2013 iOS IPA (config.xml in song packs); no repo hosts XML (chuxue2777's web port embeds data in JS); Unzip the iOS IPA song packs; rmstZ reads the XML |
| [`vsrg/music-times/xml`](vsrg/music-times/xml/) `.xml` Music Times chart | 0 | 0 | No public copy found anywhere; later clients encrypt charts; rmstZ is closed source; Old client download folder + rmstZ |
| [`vsrg/musync/txt`](vsrg/musync/txt/) `.txt` MUSYNX (Musync) chart (txt) | 0 | 0 | No public copy found; game data is binary/encrypted and no repo hosts txt charts (KeyTap uses its own JSON); Extract from MUSYNX game data (Steam), rmstZ handles both plaintext and encrypted |
| [`vsrg/o2jam/ojm`](vsrg/o2jam/ojm/) `.ojm` O2Jam music/sample container (M30 / OMC / OJM) | 0 | 11 | OJM files are audio containers (they carry the game audio and cannot be stripped), so no real file is committed; only 11 synthetic M30/OJM seeds from render-ojn; Copy o2ma<id>.ojm next to an OJN from an own client Music/ folder or the Server Two music pack; extract with CXO2/Open2Jam/render-ojn |
| [`vsrg/o2jam/ojn`](vsrg/o2jam/ojn/) `.ojn` O2Jam note file | 21 | 11 | archive.org item o2jam_musicpack (3 700 per-song zips by server), o-2-mania, own client Music/o2ma*.ojn |
| [`vsrg/o2jam/ojnlist-dat`](vsrg/o2jam/ojnlist-dat/) `OJNList.dat` O2Jam client music list | 1 | 0 | only one OJNList.dat reachable: other client folders sit beyond the first 45 MB of 1-2 GB RARs (O2Mania.rar, o2jam_setup.exe is an installer); download the whole O2Mania.rar (1.1 GB) from archive.org item o-2-mania or o2jam_setup.exe and extract Image/OJNList.dat |
| [`vsrg/o2jam/txt`](vsrg/o2jam/txt/) `.txt` O2Jam - Music & Game chart | 0 | 0 | Format unknown and no file found: rmstZ test pack sits on a Jianguoyun share page that cannot be downloaded with curl; no repository holds an O2Jam Music & Game txt chart; export from the mobile app data or with rmstZ [unverified] |
| [`vsrg/o2jam/xnt`](vsrg/o2jam/xnt/) `.xnt` KrazyRain chart (XNOT) | 0 | 0 | No .xnt is public: they exist only inside KrazyRain .snp archives (no public copy found; KrazyRenderer and Arrowgene.KrazyRain ship none); extract an own KrazyRain .snp with Arrowgene.KrazyRain vdisk-extract |
| [`vsrg/osu-mania/osb`](vsrg/osu-mania/osb/) `.osb` osu! storyboard file | 21 | 0 | .osb at the root of any .osz whose set has a storyboard |
| [`vsrg/osu-mania/osu`](vsrg/osu-mania/osu/) `.osu` osu! beatmap (mode 3, osu!mania) | 107 | 0 | osu.ppy.sh/beatmaps mania maps (unzip .osz); lazer and rosu-map test resources; ROX assets/osu |
| [`vsrg/pop-n-music/arcade-chart`](vsrg/pop-n-music/arcade-chart/) `(unknown)` pop'n music arcade chart events | 0 | 0 | Konami arcade data exists only inside a game install (<ifs>_op.bin / _hp.bin inside the song .ifs); no public copy found in GitHub path search, popntowav/popn-tools/popngg repos, archive.org or web search; Own a pop'n install: unpack the song .ifs with ifstools; popntowav.js reads _op.bin or _hp.bin |
| [`vsrg/project-sekai/ccmmws`](vsrg/project-sekai/ccmmws/) `.mmws / .ccmmws / .unchmmws` MikuMikuWorld binary layout (MMWS/CCMMWS/UCMMWS) | 0 | 10 | no public .ccmmws/.unchmmws exists; the 10 committed files are real charts converted with rg-converters; Save from MMW4CC / MMW4UC; Chart Cyanvas and Untitled Charts communities |
| [`vsrg/project-sekai/holodori-sus`](vsrg/project-sekai/holodori-sus/) `.sus` hololive Dream SUS dialect | 6 | 0 | holodori-asset-tools download --filter '^chart_m.*\.sus$' fetches all songs from the public CDN |
| [`vsrg/project-sekai/mmws`](vsrg/project-sekai/mmws/) `.mmws` MikuMikuWorld score (MMWS) | 0 | 5 | no public .mmws exists; the 5 committed files are real charts converted with rg-converters; Save from MikuMikuWorld (crash5band) File > Save |
| [`vsrg/project-sekai/pjsk`](vsrg/project-sekai/pjsk/) `.pjsk / .json / .json.gz` PJSK score maker chart | 3 | 4 | 3 downloaded real files; 3 more are real charts converted with rg-converters; Extract score data from the game's asset bundles |
| [`vsrg/project-sekai/sus`](vsrg/project-sekai/sus/) `.sus` Sliding Universal Score (SUS) | 21 | 1 | storage.sekai.best music_score/<id>_01/<difficulty>.txt for every official song; Chart Cyanvas / Untitled Charts fan charts |
| [`vsrg/project-sekai/usc`](vsrg/project-sekai/usc/) `.usc` Universal Sekai Chart (USC) | 2 | 6 | 2 raw USC from the susc-converter tests; 5 more are converted; MMW4CC exports; convert SUS with rg-converters or susToUSC |
| [`vsrg/pump-it-up/not`](vsrg/pump-it-up/not/) `.not / .not5` Pump It Up NOT/NOT5 step file | 12 | 0 | archive.org piupc3rd (251 .NOT files); NOT5 files from later Andamiro data |
| [`vsrg/pump-it-up/stx`](vsrg/pump-it-up/stx/) `.stx` Pump It Up STX step file (STF4) | 12 | 0 | the other 61 STX in archive.org prex-pc PREX_PC.ISO; later Pump It Up PC/arcade data |
| [`vsrg/pump-it-up/ucs`](vsrg/pump-it-up/ucs/) `.ucs` Pump It Up User Custom Step | 8 | 0 | StepMania-AMX/micro step/ folder (3,124 .ucs); official UCS sites; PIUUCSMaker/StepEdit Lite exports |
| [`vsrg/pydance/dance`](vsrg/pydance/dance/) `.dance` pydance step file | 6 | 0 | no other .dance exists on icculus.org Wayback CDX; Debian songs package not found |
| [`vsrg/qq-dance/xml`](vsrg/qq-dance/xml/) `.xml` QQ Dance mobile chart | 0 | 0 | No public copy found: official xml.bytes only in old 2019 APKs; QQX5Tools has converters but no data; QQX5Tools BytesToXml on a 2019 APK; custom-chart tutorials on jianshu.com/p/cc6b74bf9520 |
| [`vsrg/quaver/qua`](vsrg/quaver/qua/) `.qua` Quaver map (YAML) | 121 | 2 | quavergame.com map pages (.qp = ZIP); Quaver import of osz/sm/mcz; Quaver.API tests |
| [`vsrg/r2beat/r2n`](vsrg/r2beat/r2n/) `.r2n` R2Beat chart package | 0 | 0 | No public copy found; no source documents the package; recorded only in rmstZ's feature list; Unknown; rmstZ lists r2n extraction |
| [`vsrg/r2beat/xml`](vsrg/r2beat/xml/) `.xml` R2Beat note chart | 10 | 1 | tablez/r2beat-viewer res/note_music* has 5680 charts; dzsfo/r2beat rnr_music |
| [`vsrg/rhythm-master/imd`](vsrg/rhythm-master/imd/) `.imd` Rhythm Master classic chart | 9 | 6 | GirlKiller512/RhythmMasterResource has 4134 .imd; nladuo/RM2Malody; dreamimd.com fan charts |
| [`vsrg/rhythm-master/json`](vsrg/rhythm-master/json/) `.json` Rhythm Master imdjson (BNDQ) | 9 | 19 | Convert any .imd with RMEssentials |
| [`vsrg/rhythm-master/mde`](vsrg/rhythm-master/mde/) `.mde` Rhythm Master star motion chart | 0 | 0 | No public copy found: the only .mde (RMEssentials test) is a 0-byte placeholder; Star-motion mode data of Rhythm Master; rmstZ reads/writes it |
| [`vsrg/rhythm-open-exchange/jrox`](vsrg/rhythm-open-exchange/jrox/) `.jrox` ROX JSON | 0 | 9 | no upstream .jrox exists; the 6 committed files are real .rox charts converted by a script; JroxEncoder / auto_encode from any chart |
| [`vsrg/rhythm-open-exchange/rox`](vsrg/rhythm-open-exchange/rox/) `.rox` ROX native binary | 9 | 0 | convert any chart with the rox crate (auto_encode); all available real files are 4K |
| [`vsrg/rhythm-open-exchange/yrox`](vsrg/rhythm-open-exchange/yrox/) `.yrox` ROX YAML | 0 | 9 | no upstream .yrox exists; the 6 committed files are real .rox charts converted by a script; YroxEncoder from any chart |
| [`vsrg/robeats/lua-songmap`](vsrg/robeats/lua-songmap/) `.lua` RoBeats custom-server song map (Lua ModuleScript) | 4 | 0 | robeats-cs-legacy/robeats-cs-maps repos private/removed, Wayback has no capture, Sourcegraph/grep.app blocked by bot checks, archive.org partly offline; osu-to-Lua converter per Robeats wiki; Roblox community places |
| [`vsrg/rock-band/dta`](vsrg/rock-band/dta/) `.dta` Rock Band songs.dta database | 5 | 1 | ex-CON/PKG songs/songs.dta, RB3 Deluxe _ark/songs/, Onyx builds, Rock Band Customs Project |
| [`vsrg/sound-voltex/ksh`](vsrg/sound-voltex/ksh/) `.ksh` K-Shoot MANIA chart (text) | 12 | 2 | K-Shoot MANIA default songs and Input Gate, Nautica, sdvx.org, IcarusFW/sdvx-practicecharts (kshootmania/*.ksh), voltedit |
| [`vsrg/sound-voltex/kson`](vsrg/sound-voltex/kson/) `.kson` K-Shoot MANIA JSON chart | 17 | 7 | Nautica API https://ksm.dev/app/songs?page=N lists ~7400 songs, ~1 in 4 has a .kson in its CDN zip (read by HTTP range) |
| [`vsrg/sound-voltex/vox`](vsrg/sound-voltex/vox/) `.vox` SOUND VOLTEX arcade chart | 12 | 6 | retail .vox only from own game data (data/music/<id>_<name>); IcarusFW/sdvx-practicecharts, JofoxTheCat/SDVX-Chart-Converter, VOXL4DD3R/ksm2sdvx/VoxCharger write v10/v13 |
| [`vsrg/soundsphere/nanochart`](vsrg/soundsphere/nanochart/) `.nanochart` NanoChart (rizu compact note stream) | 1 | 7 | only 1 genuine file (rizu test vector); the other 5 are real charts encoded by a script port of the rizu encoder; rizu editor export |
| [`vsrg/soundsphere/sph`](vsrg/soundsphere/sph/) `.sph` SPH chart (rizu / soundsphere) | 8 | 0 | run rizu and export converted charts |
| [`vsrg/stepmania/crs`](vsrg/stepmania/crs/) `.crs` StepMania course file | 25 | 0 | Courses/ of any StepMania/ITGmania install |
| [`vsrg/stepmania/edit`](vsrg/stepmania/edit/) `.edit` StepMania edit file | 40 | 3 | remaining 400 Drano edits in archive.org StepManiaDranoEdits; your own profile Edits/ folder |
| [`vsrg/stepmania/sm`](vsrg/stepmania/sm/) `.sm` StepMania simfile | 112 | 0 | archive.org simfile packs (ZeldaYEH, Tweety, stepmaniapack 9.7 GB), simfile-parser packs, simfilearchive.dev |
| [`vsrg/stepmania/ssc`](vsrg/stepmania/ssc/) `.ssc` StepMania 5 simfile | 42 | 0 | remaining OutFox Serenity ssc, PIU-Simfiles repos, archive.org piu-simfiles-stepp1 |
| [`vsrg/stepmania-amx/sma`](vsrg/stepmania-amx/sma/) `.sma` StepMania AMX simfile | 0 | 0 | no .sma file exists in any reachable repository, AMX build archive or archive.org item; the loader semantics are too loose to hand-write one; convert an .ssc with ssc2sma.amx.io or find .sma in AMX-targeted song packs |
| [`vsrg/stepmania-micro/json`](vsrg/stepmania-micro/json/) `.json` StepMania JSON (StepMania Micro) | 2 | 0 | only the 2 StepMania Micro 0.3 data files exist (Wayback); no NotesWriterJson output published anywhere found; build StepMania and call NotesWriterJson |
| [`vsrg/vos/vos`](vsrg/vos/vos/) `.vos` Virtual Orchestra Studio song (.vos) | 6 | 0 | VOS community song libraries, VOS Creator from MIDI |

## others

| Format | Real | Synthetic / other | Why fewer than 5 real files, and how to get more |
|---|---:|---:|---|
| [`others/a-dance-of-fire-and-ice/adofai`](others/a-dance-of-fire-and-ice/adofai/) `.adofai` A Dance of Fire and Ice level | 6 | 2 | levels are mostly shared on Steam Workshop/adofai.gg (not scraped); more from GitHub repos such as dashgd45-eng/adofai-levels |
| [`others/arcaea/aff`](others/arcaea/aff/) `.aff` Arcaea chart (AFF) | 19 | 0 | Suhri archive, ArcCreate projects, Arcaea fan community |
| [`others/arcaea/songlist`](others/arcaea/songlist/) `songlist` Arcaea songlist / packlist | 6 | 0 | fan song packs ship songlistadd.json |
| [`others/audica/audica`](others/audica/audica/) `.audica` Audica map package | 7 | 39 | maudica.com API (~2150 maps) |
| [`others/beat-saber/dat`](others/beat-saber/dat/) `*.dat` Beat Saber beatmap (v2/v3/v4, Lightshow, BPMInfo) | 51 | 0 | BeatSaver API/CDN, BeatSaber-Deno fixtures, BSMG wiki |
| [`others/beat-saber/info-dat`](others/beat-saber/info-dat/) `Info.dat` Beat Saber Info (v1 info.json, v2, v4) | 23 | 0 | BeatSaver API/CDN |
| [`others/beatblock/level-json`](others/beatblock/level-json/) `level.json` Beatblock level (JSON events) | 41 | 3 | Beatblock Browser (TLS unreachable), Steam Workshop, other level zips in ItsBritex/beatblock-levels |
| [`others/chunithm/c2s`](others/chunithm/c2s/) `.c2s` C2S (CHUNITHM chart) | 7 | 0 | more from UMIGURI_charts via MuConvert conversion |
| [`others/chunithm/sus`](others/chunithm/sus/) `.sus` SUS (Sliding Universal Score) | 6 | 0 | Ched fixtures, sonolus-level-converters |
| [`others/chunithm/ugc`](others/chunithm/ugc/) `.ugc` UMIGURI Chart v8 | 10 | 0 | mitsuhira/UMIGURI_charts has 23 ugc, only 6 taken |
| [`others/crypt-of-the-necrodancer/beatmap-txt`](others/crypt-of-the-necrodancer/beatmap-txt/) `.txt (<song>.mp3.txt)` Crypt of the NecroDancer custom music beat file | 1 | 2 | only one real beat list is published (2017 Steam forum post); 8 other Steam threads/guides, tool repos checked and hold none; files are generated locally by the game; assign custom music in the game or use Supinic/necrodancer-custom-music |
| [`others/cytus/c1-txt`](others/cytus/c1-txt/) `.txt` Cytus 1 chart ("Rayark v2 modified") | 5 | 1 | Cytoid wiki sample; game data |
| [`others/cytus/c2-json`](others/cytus/c2-json/) `.json` Cytus II / Cytoid chart (C2) | 8 | 1 | cytoid.io levels (package download needs login) |
| [`others/dancerail/drb`](others/dancerail/drb/) `.drb` DanceRail chart | 4 | 1 | only DanceRail3Viewer (4 distinct bluemelody charts) is publicly reachable; grep.app/Sourcegraph blocked, no .drb or other community pack found; DRMaker/DanceRail3 on Android |
| [`others/deemo/json`](others/deemo/json/) `.json` Deemo chart (JSON) | 8 | 1 | Deemo-I-Charts has ~1700 more |
| [`others/djmax-technika-q/bytes`](others/djmax-technika-q/bytes/) `.bytes` DJMAX Technika Q song | 6 | 0 | DMTQResearch Patterns folder has 2634 more |
| [`others/donkey-konga/mid`](others/donkey-konga/mid/) `.mid` Donkey Konga score MIDI | 3 | 8 | only one public custom Donkey Konga 2 track exists (3 charted MIDI files; the 6 other committed MIDI files are empty slots); dump a Donkey Konga 2 disc: files/Score/*.mid |
| [`others/drums-rock/notes-csv`](others/drums-rock/notes-csv/) `.csv` Drums Rock custom song (notes.csv + info.csv) | 12 | 2 | Steam guide 3284235843 links ~140 Drive folders |
| [`others/dynamix/dy`](others/dynamix/dy/) `.dy` Dynamaker bundle (.dy) | 0 | 1 | container-ish bundle with embedded audio: no real .dy is public (they embed copyrighted music, shared in private fanmade circles); 2nd pass: no real .dy found; Dynamaker/dynamaker-modified "Save as .DY" or DyNode export |
| [`others/dynamix/xml`](others/dynamix/xml/) `.xml` Dynamix chart XML | 3 | 1 | only 3 public real charts exist (CamberLoid/DynamixFanmade has 2, DyNode test fixture); dye.omegapigame.com is dead; 2nd pass: Sourcegraph/grep.app blocked by Cloudflare, Wayback offline, GitHub topic pages/DynaCharter/REnamix/DyNode repos hold no more charts; export from Dynamaker/DyNode; fan charts in Discord communities |
| [`others/gadvia/chart-json`](others/gadvia/chart-json/) `.json` Gadvia chart (JSON asset) | 0 | 0 | no public copy anywhere: Unity asset bundles inside the commercial Android game, extraction needs the installed game (see fiche); adb pull APKs + AssetRipper per Rhythm Game Wiki guide |
| [`others/gitaroo-man/chc`](others/gitaroo-man/chc/) `.chc` Gitaroo Man stage chart (CHC) | 0 | 0 | no public copy: game data of the PS2/PSP titles, no repo or site hosts CHC files; ISO is commercial and over 20 MB; own the game, unpack with gitarootools, read with Gitaroo-Man-File-Reader |
| [`others/groove-coaster/aar`](others/groove-coaster/aar/) `.aar` AAR / ALAR archives (Groove Coaster) | 0 | 0 | no public copy: archives of the commercial game (Steam/arcade/Switch) are not hosted anywhere reachable; install Groove Coaster for Steam, unpack with Mod The Coaster |
| [`others/jubeat/eve`](others/jubeat/eve/) `.eve` EVE (jubeat chart events) | 3 | 1 | only 3 public .eve files found (jubeatools test data); no other public collection; 2nd pass: GitLab+GitHub jubeatools, Jubeat-MemonEveConverter, asphyxia plugin checked, no further .eve; convert memo/memon with jubeatools; arcade data |
| [`others/jubeat/jbsq`](others/jubeat/jbsq/) `.jbsq` JBSQ (jubeat binary sequence) | 0 | 0 | no public copy: only the Kaitai spec exists; originals are arcade data; 2nd pass: web/GitHub searches find no .jbsq file anywhere; write one with jubeatools from memon/eve |
| [`others/jubeat/memo`](others/jubeat/memo/) `.txt (memo)` jubeat analyser memo formats (memo/memo1/memo2/boogie/mono-column/youbeat) | 8 | 0 | jubeatools tests; jubeat analyser community sites |
| [`others/jubeat/memon`](others/jubeat/memon/) `.memon` memon (jubeat JSON chart set) | 6 | 1 | F.E.I.S. and jubeatools; Stepland/memon tests |
| [`others/just-dance/ubiart-tape`](others/just-dance/ubiart-tape/) `.dtape.ckd / .ktape.ckd` Just Dance UbiArt tape (dance, karaoke) | 0 | 2 | no public real tape: test files are private (Ferris Dancing) or placeholders; only synthetic files committed; 2nd pass: checked JD fan repos (Lilypad-Next, JustDanceServer, WodsonKun, JiafeiTape, MAPDB-MAKER, 2014 tools): only code, JDN JSON or JD2014 binary tpl; extract .ipk of a game install with IpkTool/Ferris Dancing |
| [`others/lanota/lanotalium`](others/lanota/lanotalium/) `unknown` Lanotalium / Layesta fan chart | 0 | 0 | no public chart: Lanotalium repo has none and its chart-zone API is dead; charts shared in Discord only; 2nd pass: Lanotalium releases are tools only, chartzone API and lanotalium.cn empty; create in Lanotalium or ask the Lanotalium/Layesta community |
| [`others/love-live-sif/sift-json`](others/love-live-sif/sift-json/) `.json` SIFTrain beatmap (Love Live! SIF live JSON) | 8 | 1 | NPPS4 beatmaps/ (~1900 Live_*.json) and honoka-chan assets |
| [`others/maimai/ma2`](others/maimai/ma2/) `.ma2` MA2 (maimai DX chart) | 13 | 0 | MaichartConverterUnitTest data/ and official game data |
| [`others/maimai/sdt`](others/maimai/sdt/) `.sdt` SRT / SZT / SCT / SDT (maimai classic charts) | 0 | 4 | no public real classic chart: game data is encrypted (.sdb etc.) and not hosted; only 4 synthetic files committed; 2nd pass: no public classic chart in MaiConverter, Neskol repos or gists; convert ma2/simai with MaiConverter; maimai classic data dump |
| [`others/maimai/simai`](others/maimai/simai/) `maidata.txt` simai (maidata.txt, 'simai language') | 5 | 2 | MajdataEdit, Neskol/Maichart-Converts, converters |
| [`others/muse-dash/bms`](others/muse-dash/bms/) `.bms` Muse Dash BMS dialect | 16 | 8 | api.mdmc.moe/v3/charts (all community albums) |
| [`others/ohshape/yml`](others/ohshape/yml/) `.yml` OhShape level (YAML) | 8 | 0 | ohshapes.com /api/maps/latest/<page> (many more maps) |
| [`others/ongeki/ogkr`](others/ongeki/ogkr/) `.ogkr` OGKR (ONGEKI chart) | 5 | 0 | OngekiFumenEditor FumenSamples (about 138 files) |
| [`others/osu-catch/osu`](others/osu-catch/osu/) `.osu` osu! beatmap (mode 2, osu!catch) | 21 | 0 | same, catch difficulties |
| [`others/osu-standard/osu`](others/osu-standard/osu/) `.osu` osu! beatmap (mode 0, osu!standard) | 38 | 0 | any .osz from osu.ppy.sh (account) or fixture repos |
| [`others/osu-taiko/osu`](others/osu-taiko/osu/) `.osu` osu! beatmap (mode 1, osu!taiko) | 15 | 0 | same, taiko difficulties |
| [`others/paradiddle/rlrr`](others/paradiddle/rlrr/) `.rlrr` Paradiddle song / kit / recording (RLRR) | 16 | 2 | paradb.net API lists many more maps (maps.paradb.net/maps/<id>.zip) |
| [`others/paradigm-reboot/chart`](others/paradigm-reboot/chart/) `unknown` Paradigm: Reboot chart | 0 | 0 | commercial Unity game, format unknown, no public dump or parser found; wiki Data Mining page returns 403; see fiche Getting samples |
| [`others/phigros/official-json`](others/phigros/official-json/) `.json` Phigros official chart | 6 | 2 | phigros-chart-tracker / decrypted-data mirrors |
| [`others/phigros/pec`](others/phigros/pec/) `.pec` PhiEdit Chart (PEC) | 8 | 1 | more pec folders in yuameshi/phigros-charts-repo |
| [`others/phigros/phi-common-chart`](others/phigros/phi-common-chart/) `.json / protobuf` PhiCommonChart (PhiFanmade interchange model) | 0 | 0 | no file of this format exists publicly: only doc fragments at docs.nuanr-mxi.com; see fiche Getting samples |
| [`others/phigros/rpe`](others/phigros/rpe/) `.json` Re:PhiEdit chart (RPEJSON) | 11 | 0 | api.phira.cn/chart lists ~9700 charts (file = pez URL) |
| [`others/pistol-whip/pwcl-level`](others/pistol-whip/pwcl-level/) `.pw / .pw_beat` Pistol Whip Custom Levels folder (level.pw, .pw_beat, .pw_koreo, .pw_sec, .pw_geo) | 30 | 0 | mod.io official levels; pw_geo files over 20 MB were skipped |
| [`others/project-diva/dsc`](others/project-diva/dsc/) `.dsc` DSC (Project DIVA DivaScript) | 15 | 0 | divamodarchive.com API: many song packs, dsc extractable by HTTP range requests |
| [`others/ragnarock/info-dat`](others/ragnarock/info-dat/) `info.dat` Ragnarock map (Beat Saber-derived) | 21 | 3 | ragnacustoms.com/songs/ddl/<id> (ids up to ~6600) |
| [`others/reflec-beat/rb`](others/reflec-beat/rb/) `.rb` RB package (Reflec Beat plus iOS) | 0 | 0 | commercial Konami iOS package, entries Blowfish-encrypted, no public copy found; see fiche Getting samples |
| [`others/rgc/rgc`](others/rgc/rgc/) `.rgc` RGC (Rhythm Game Chart) | 2 | 1 | only two public .rgc found (rgc repo test, vsrg-chart-view test); rgc-bms/rgc-kshoot repos hold converters only |
| [`others/rhythm-doctor/rdlevel`](others/rhythm-doctor/rdlevel/) `.rdlevel` Rhythm Doctor level | 16 | 0 | datasette.rhythm.cafe JSON API (~7700 levels with rdzip_url) |
| [`others/rhythm-heaven/tickflow`](others/rhythm-heaven/tickflow/) `.bin / .tickflow` Rhythm Heaven Megamix / DS tickflow script | 17 | 1 | more in the same repo; decompile Megamix .bin with Tickompiler |
| [`others/rizline/chart-json`](others/rizline/chart-json/) `.json` Rizline chart (chart.json) | 1 | 1 | only the rizlib official test chart is public; Workshop charts need Steam, no GitHub collection found; see fiche Getting samples |
| [`others/rocksmith/sng`](others/rocksmith/sng/) `.sng` Rocksmith 2014 SNG (binary) | 6 | 0 | unpack any psarc with the toolkit |
| [`others/rocksmith/xml`](others/rocksmith/xml/) `.xml` Rocksmith 2014 arrangement XML | 11 | 0 | EOF/DDC authored CDLC |
| [`others/rotaeno/chart-text`](others/rotaeno/chart-text/) `.txt` Rotaeno chart text (as read by RotaenoChartTool) | 0 | 1 | no open source holds real Rotaeno charts (only metadata/tools); game data not publicly distributed; see fiche Getting samples |
| [`others/smash-drums/indies`](others/smash-drums/indies/) `.indies` Smash Drums Indies package | 6 | 1 | Indies-DB (public Supabase storage URLs) has hundreds more community charts; Smash Drums Editor export |
| [`others/sonolus/level-data`](others/sonolus/level-data/) `.json (gzip)` Sonolus Level Data | 7 | 2 | any Sonolus server (untitledcharts.com has ~77k levels); rg_converters from USC/SUS |
| [`others/sound-space/sspm`](others/sound-space/sspm/) `.sspm` Sound Space Plus / Rhythia map (v1, v2) | 8 | 2 | Rhythia API getBeatmaps lists 13k maps (legacy ones are .sspm); Rhythia-DB bulk downloader |
| [`others/sound-space/txt`](others/sound-space/txt/) `.txt` Sound Space (Roblox) text map | 21 | 0 | GitHub txt map lists (nruv/sound-space, CotixGD/SS-Archive); pysspm NOTES2TEXT |
| [`others/space-channel-5/dgsh`](others/space-channel-5/dgsh/) `.bin (DGSH)` Space Channel 5 Part 2 DGSH sequence files | 6 | 0 | extract R*_SH.BIN from Space Channel 5 Part 2 PC AFS archives |
| [`others/spin-rhythm-xd/srtb`](others/spin-rhythm-xd/srtb/) `.srtb` Spin Rhythm XD track bundle | 9 | 0 | SpinShare /api/song/<id>/download backup zips (tens of thousands of charts) |
| [`others/starlight-stage/csv`](others/starlight-stage/csv/) `.csv` CGSS beatmap CSV | 8 | 0 | mishiro-score-viewer docs/res has more ids; extract bdb databases from the game data (DereInfo/DereTore) |
| [`others/synth-riders/synth`](others/synth-riders/synth/) `.synth` Synth Riders map | 0 | 0 | synthriderz.com downloads are AES-encrypted zips (key not public), audio inside cannot be stripped; no unencrypted .synth found in any open repo; save a map from the Synth Riders Beatmap Editor or get an unencrypted file from a mapper |
| [`others/taiko-no-tatsujin/fumen`](others/taiko-no-tatsujin/fumen/) `.bin` Fumen (official Taiko no Tatsujin binary chart) | 30 | 0 | dump the official game data or run tja2fumen on any .tja |
| [`others/taiko-no-tatsujin/tcc`](others/taiko-no-tatsujin/tcc/) `.tcc` Open Taiko Chart (.tci/.tcc/.tcm JSON) | 5 | 0 | export from Koioto OpenTaikoChart plugin or TJAPlayer3-f / OpenTaiko |
| [`others/taiko-no-tatsujin/tja`](others/taiko-no-tatsujin/tja/) `.tja` TJA (Taiko Jiro chart) | 45 | 3 | TJADB tjadataba.se, taiko-web, TaikoJiro chart archives, OpenTaiko Songs folder |
| [`others/taiko-no-tatsujin/tjf`](others/taiko-no-tatsujin/tjf/) `.tjf` TJF (Taikosan / TJF EDIT chart) | 1 | 1 | only one real .tjf exists in the Taikosan package (getuploader archives 403, nothing else on Wayback/archive.org); Taikosan plusedit package (mediafire link on w.atwiki.jp/laser_bm/pages/72.html), TJF EDIT |
| [`others/thumper/objlib`](others/thumper/objlib/) `.pc / .objlib` Thumper object library (leaf, level, gate, master) | 6 | 0 | copy binary .pc files from <Thumper>/cache; CocoaMix86 Thumper Custom Level Editor |
| [`others/trombone-champ/tmb`](others/trombone-champ/tmb/) `.tmb` Trombone Champ custom track (song.tmb) | 10 | 1 | TromboneDB (tc-mods.github.io/TromboneDB, ~5800 charts via db.trombone.fyi/<id>.zip), TootTally |
| [`others/voez/json`](others/voez/json/) `.json` VOEZ chart set (info / note / track JSON) | 0 | 6 | no real VOEZ chart publicly reachable (official charts only in game AssetBundles; VoezEditor repo has no samples; fandom/GBAtemp links dead); VoezEditor export / dump Switch or mobile AssetBundles |
| [`others/vulnus/json`](others/vulnus/json/) `.json` Vulnus map (meta.json + difficulty json) | 0 | 3 | no real Vulnus map found (maps shared on Discord; converter repos ship no sample maps); copy a map folder from the Vulnus install maps directory |
| [`others/wacca/mer`](others/wacca/mer/) `.mer` MER (WACCA / Mercury chart) | 8 | 0 | frozenpandaman/MercuryPlayer MusicData has 1247 .mer files in total |

## Games without a format page

| Game | Real | Synthetic / other | Note |
|---|---:|---:|---|
| [`others/elite-beat-agents`](others/elite-beat-agents/) | 0 | 0 | No format folder: chart data of the DS games is undocumented; would need own NDS ROM and reverse-engineering (see game README Getting samples) |
| [`others/nostalgia`](others/nostalgia/) | 0 | 0 | No format folder: no public spec/parser/sample; arcade data is commercial (see game README Getting samples) |

## Licence notes

By decision of the repository owner, real charts (community maps, official game data that is publicly downloadable, test fixtures of other projects) are committed as downloaded and the licence risk is accepted; each `SOURCES.md` records the URL, fetch date and the terms as far as known. The list below flags the places where authorship or terms are especially unclear.

- vsrg/sound-voltex/ksh/samples/Gram_lt.ksh, Gram_ch.ksh, Gram_ex.ksh, Gram_in.ksh and kson/samples/Gram_ex.kson: sample song bundled with K-Shoot MANIA; ksm-v2 readme says bundled songs are the property of the content creators (outside use needs permission), but the files sit in MIT-licensed kshootmania/libkson (same maintainer); charts only, no audio
- vsrg/sound-voltex/ksh/samples/{cantabile,hawk,howling,juicy,konga,tenkuu,xeroize}.ksh: fan charts of third-party songs; voltedit test/README.md says all charts were permitted by charters to be put in the (MIT) repo; permission statement is by the repo author, not per chart
- vsrg/vos/vos/samples/{1,103,23,24,109}.vos: community song arrangements (MIDI of existing songs probably); only the MIT licence of rhythmus-emulator/rparser backs redistribution, authors unknown
- vsrg/sound-voltex/vox/samples/oracle.golden.vox, curve-scroll.golden.vox: exports from the sdvxindex.com editor of synthetic fixtures; repository MIT, tool output of a third-party editor
- vsrg/dtxmania/dtx/samples/dtx2gp_test3-6.dtx: LGPL-3.0 repo (COPYING); files are hand-written unit tests by the repo author (no per-file header)
- vsrg/o2jam/ojn/samples/*.seed and ojm/samples/*.seed\|.ojm\|.m30: GPL-3.0 fuzz corpus of djzmo/render-ojn (README says synthetic/redistributable only); extension .seed kept
- vsrg/dtxmania/{gda,g2d}/samples/synthetic-*: derived from loader code, not from a real GDA/G2D file; real header conventions unverified
- vsrg/project-sekai/usc: sonolus-pjsekai-engine shared/src/level/data/append.json (MIT repo, Sonolus LevelData, 1.2 MB) not taken: converted chart of unstated origin, probably an official chart; belongs to others/sonolus
- vsrg/rhythm-master/json/samples/rmessentials-fromjson_*.json: hand-written test files in AGPL-3.0 repo, contain joke strings; kept
- vsrg/rhythm-master/imd: RMEssentials tojson/toimd .imd fixtures (crunch, canonrock, legend, friend01, ...) look like official/fan song charts, manifest only
- vsrg/project-sekai/sus/samples/sus-analyzer_*: sample_data authored by repo owner (#DESIGNER mizucoffee), MIT repo; Touhou-song metadata only
- vsrg/bms/bmson/samples/synthetic-features.bmson: pre-existing file (commit a7c56f8), authorship/licence not recorded; documented as presumed public domain.
- vsrg/bms/bmson (manifest bms-rs_lostokens.bmson, bms-rs_bemusicstory_483_48K_ANOTHER.bmson): repo is Apache-2.0 but the charts are third-party; not committed.
- vsrg/bms/bmson (manifest bemuse-ninja_onlylove_remix_*.bmson): CC-BY-NC in the files; NC terms, not committed.
- vsrg/bms/bmson: bemusic/bmson-spec has no LICENSE file, nothing taken.
- vsrg/bms/ibmsc/samples/synthetic-*.ibmsc: hand-built from pBMSC source, never opened in iBMSC; verified only by a mirrored Python reader (undo block written empty).
- vsrg/bemuse/bemuse-song-json/samples/derived-aoi-olivia-bemuse-song.json: derived (id/path removed, reserialised) from the AGPL index.json fixture, not a real bemuse-song.json.
- vsrg/robeats/lua-songmap/samples/*.lua: spotco/RobeatsCustomServerTemplate has no LICENSE file; committed on the strength of the author's devforum statement ("100% Free and open source to do anything you want with"); Monday Night Monsters note data belongs to the template author's own song.
- vsrg/soundsphere/nanochart/samples/synthetic-*.nanochart: built with a Python port of the Lua encoder, checked only against 4 exact-byte vectors of NanoChart_test.lua.
- vsrg/rhythm-open-exchange/{jrox,yrox}/samples/synthetic-*: hand-written, never run through the Rust codec; yrox quoting style may differ from serde_yaml output.
- vsrg/fluxis: fluXis repo is MIT (LICENSE read) but contains no map files; fluXis map download without login not tested.
- vsrg/bms/bms/samples/0.ct_[MAX].bms (+ 0.ct_a/h/n.bms): extracted from rhythmus-emulator/rparser test/bms_sample_angelico.zip (MIT repo); the fan chart authors (anubasu-anubasu, obj 980円の人) gave no licence of their own
- vsrg/bms/bms/samples/allnightmokugyo.bms, l-for-nanasi.bms, vsrg/bms/bme/samples/L9^.bme: kusofumen from rhythmus-emulator/rparser (MIT repo); third-party joke charts (HIROHIO, paraoka), no licence from the authors
- vsrg/bms/bms/samples/J219_7key.bms, lilith_mx.bms, vsrg/bms/bme/samples/nc_mx.bme, dive_withblank.bme: bms-rs test fixtures (Apache-2.0 repo); the notes are credited to the bms-rs author ("obj: Mikuro Xina") but the songs belong to other artists (cranky, ikaruga_nex, Silentroom, xi)
- vsrg/bms/bms/samples/base62.bms: bemuse repo root is AGPL-3.0 but packages/bms is MIT (package.json); committed under MIT
- vsrg/bms/bms/samples/invisible.bms, vsrg/bms/bml/samples/longnote-*.bml: Angolmois test files, declared public domain in their headers although the repo is GPL-2.0+; the sound samples they reference (CC-BY OLPC) are not included
- vsrg/bms/bms/samples/{Another-capital,Hyper-capital}.bms duplicate another.bms / hyper.bms byte for byte (pre-existing upstream files, left in place)
- vsrg/bms/bms/samples/be-music_*.bms, be-music_9key-all-keys-quarter.pms: MIT repo Nekokan/be-music (LICENSE 'Copyright (c) 2026 nulltask'); example charts written by the project (artist 'Codex'), not third-party songs
- vsrg/bms/bms/samples/tapestry_*.bms: shuymn/tapestry bms-parser crate is MIT OR Apache-2.0 per README; tiny test stubs
- vsrg/bms/bme/samples/BMSParser_05.bon_voyage_7hyper.bme: real chart (song Bon Voyage by Mystinia) inside an MIT-licensed parser repo; no separate licence for the song/chart
- vsrg/friday-night-funkin/legacy-json/samples/rox-test-song.json: MIT via ROX (owner's crate), but whether the chart content is hand-made or derived from a real FNF chart is not stated
- vsrg/friday-night-funkin/*: all real FNF charts (Funkin tag v0.2.7.1 is plain Apache-2.0 repo-wide, engines Apache-2.0) kept manifest-only because funkin.assets licence is proprietary; the v0.2.7.1 and 1.0.0 trees may be redistributable under Apache-2.0 but the parent said manifest-only
- vsrg/flash-flash-revolution/swf/samples/synthetic-level.swf: verified only by a Python port of rCubed Beatbox.parseBeatbox, not by Flash/rCubed
- vsrg/clone-hero/chart/samples/yarg-core_test.chart: committed under the YARG.Core repo licence LGPL-3.0 (LICENSE read); the file is a synthetic feature-check chart ("Test" artist) but its individual author is not stated
- vsrg/clone-hero/mid/samples/yarg-core_test.mid: same, LGPL-3.0 repo fixture with synthetic-looking tracks, individual author not stated
- vsrg/clone-hero/mid (manifest drawntotheflame.mid): full RB-style chart, rights unclear, therefore manifest only
- vsrg/osu-mania/osu/samples/ppy-osu_*.osu: MIT repo (ppy/osu) but some fixtures (4869637, 100374, 20544) are real ranked-map derived; mapper licence unknown
- vsrg/osu-mania/osu/samples/quaver-api_*.osu and vsrg/quaver/qua/samples/quaver-api_*.qua: MPL-2.0 repo, but Camellia/megalovania/Blue Zenith/ReEnd of a Dream/Tsukahara maps are real community maps; map licence unknown
- vsrg/osu-mania/osu/samples/yavsrg-prelude_*.osu and osz/samples/yavsrg-prelude_*.osz: MIT repo, real community maps (DannyPX, Raveille, Overlord68_, Night Bunny 7); map licence unknown (osz are audio-less)
- vsrg/quaver/qua/samples/quaver-resources_*.qua and qp/samples/built-princess-of-winter-audioless.qp: Quaver.Resources is CC-BY-NC 4.0 (non-commercial, attribution) - acceptable per brief but flag
- vsrg/malody/mc/samples/quaver-api_*.mc and mcz/samples/built-quaver-api-malody-audioless.mcz: real Malody community charts in MPL-2.0 repo; chart licence unknown
- vsrg/malody/mc/samples/mc2tja_*.mc: MIT repo (LuiCat); charts of songs by third parties (Jerico, Mizutori), chart licence unknown
- Eddio0141/osu-file-parser test fixtures only in manifest (no LICENSE file, Cargo.toml says MIT OR Apache-2.0, real ranked maps)
- others/beat-saber/dat/samples/bsdeno_AngelVoices_*, bsdeno_PreservedValkyria_*, bsdeno_IBetYou_BPMInfo.dat, bsdeno_Necromantic_BPMInfo.dat: community maps shipped as test fixtures in the MIT BeatSaber-Deno repo; mapper licence not stated per map
- others/beat-saber/info-dat/samples/bsdeno_{AngelVoices,PreservedValkyria,IBetYou,Necromantic,BadApple,ECHO}_Info.dat: same doubt (community map metadata under the repo MIT licence)
- others/chunithm/ugc/samples/muconvert_{Mobius_mas,Terminal_terminal,sabi}.ugc and chunithm/c2s/samples/muconvert_{Mobius,Terminal,sabi}_*.c2s: community charts of copyrighted songs inside the LGPL-3.0 MuConvert test set; individual charter licences not stated
- others/chunithm/ugc/samples/muconvert_Example_basic.ugc: Margrete example chart by inonote (@DESIGN inonote), committed under the MuConvert repo licence only
- others/cytus/c1-txt/samples/cyl_package_tool_test_*.txt and make_cytus2_*.txt: charts inside MIT repos, origin of the charts themselves (possibly ripped from the game) not stated
- others/cytus/c2-json/samples/cyl_package_tool_*.json: same doubt (test fixtures, chart origin not stated)
- others/arcaea/aff/samples/suhri_*, testify*_4.aff etc.: fan charts of copyrighted songs, committed under the archive's WTFPL; audio not committed
- others/audica/audica/samples/audicaconv-template_*: chart of the song Dadadadadadadadadada by "octo" in the MIT AudicaConverter repo; song itself (mogg audio) not committed
- others/chunithm/sus/samples/sonolus-pjsekai-engine-extended_expert.sus: chart title "Tell your world" (artist exp); origin (fan chart vs game chart) not stated; MIT repo
- others/maimai/ma2 manifest 010070_03.ma2 and other converted official charts: CC0 repo licence but content derived from commercial game data, hence manifest only
- others/ongeki/ogkr manifest ongeki-editor-bench_*.ogkr: MIT repo, but the charts (creators NaNya, MikiraSora, ...) may be fan or game charts; rights unclear, manifest only
- others/jubeat/* manifest: Stepland/jubeatools, Stepland/memon have no LICENSE file; the GitHub jubeatools README says it moved to GitLab (not checked there)
- osu-standard/osu/samples/osu-resources_*.osu: extracted from CC-BY-NC-4.0 ppy/osu-resources .osz (non-commercial); kept per brief, flagged. ppy/osu fixtures: MIT repo but many are real ranked maps by third-party mappers (Soleily - Renatus, Within Temptation, 1124896-style ids) with no per-file licence; same for osu-catch/osu-taiko/osu-standard files from kionell/osu-taiko-stable, MaxOhn/rosu-pp, ekgame/beatmap-analyzer (GPL-3.0) tests.
- others/osu-standard/osu/samples/osu-resources_*.osu: extracted from the default-track .osz of ppy/osu-resources (CC-BY-NC-4.0, non-commercial + attribution); committed per brief, audio/images dropped
- others/osu-*/osu/samples (ppy/osu, kionell/osu-taiko-stable, MaxOhn/rosu-pp, ekgame/beatmap-analyzer GPL-3.0): code repos MIT/GPL, but most .osu are real ranked maps by third-party mappers (e.g. Soleily - Renatus, Within Temptation - The Unforgiving, Tomorrow Perfume) without a per-file licence
- others/rocksmith/xml/samples/rocksmith2014net_*.xml and rocksmith/sng/samples/rocksmith2014net_*.sng: MIT repo test data (title/artist 'Test'); not stated whether the note content was written from scratch or transcribed from a real song
- others/phigros/rpe/samples/rpechart_*.json, pez/samples/rpechart_demo.pez: MIT repo kamilhzn/rpechart, docstring states fixtures are synthetic and contain no third-party material
- others/paradiddle/rlrr/samples/defaultset.rlrr: GPL-3.0 ParadiddleUtilities drum kit file (kit layout, not a song)
- manifest others/phigros/*: yuameshi/phigros-charts-repo has no licence file; contains official Pigeon Games charts and fan charts
- manifest others/rizline/chart-json/Chart_EZ_64.json: MIT repo rizlib but the file is an extracted official Rizline chart
- others/sound-space/txt/samples/ssp_BigShot.txt: MIT repo bundle, but the map targets a third-party song (Big Shot); only chart text committed, song licence unknown
- others/sound-space/txt/samples/ssp_MeteoricImpact.txt, ssp_meganeko - Feral.txt: same, song licences not checked
- others/taiko-no-tatsujin/tja/samples/opentaiko_tower_*_optktower.tja: in MIT OpenTaiko repo; song/sound team credits in file, no separate chart licence stated
- others/taiko-no-tatsujin/tja/samples/pytaiko_TRIPLE HELIX.tja: GPL-3.0 repo; chart by repo author; headers credit Colin, Komi as charters
- others/trombone-champ/tmb/samples/test-awesome.tmb: MIT TromboneCharter test file; melody origin unknown
- vsrg/stepmania/sm/samples/nekonabe.sm and vsrg/stepmania/ssc/samples/simfile_L9.ssc: committed because the simfile repo is MIT, but the songs/charts (nekonabe by Saisei Hyper Beroove, L9 by paraoka) are third-party with no licence statement of their own
- vsrg/pydance/dance/samples/*.dance: pydance LICENSE is MIT and Debian's copyright file says it covers music/graphics, but the download page only calls the songs "free"; they are not inside the GitHub mirror
- vsrg/stepmania/ssc/samples/outfox-serenity_*.ssc: chart licence rests on the Serenity guidelines text (CC-BY 3.0/4.0 agreement by contributors), not on per-folder files; credits.txt/license.txt cover only music and graphics
- vsrg/stepmania/ssc/samples/outfox-serenity_Matduke*.ssc: music of those songs is "all rights reserved" (credits.txt); only the chart text is committed
- vsrg/stepmania/{sm,ssc}/samples/{Goin' Under,Mecha-Tribe Assault,Springtime}*: StepMania README says bundled songs are CC-NC (non-commercial); committed as chart text only
- vsrg/stepmania/{sm,ssc}/samples/existing community files: origin and licence unknown (from upstream list), left in place
