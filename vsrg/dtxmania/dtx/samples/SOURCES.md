# Samples: DTXMania chart (`.dtx`)

Charts only; no audio, video or images.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `JetpacksWasYes-Extreme.dtx`, `JetpacksWasYes-Master.dtx`, `OceanAvenueMST.dtx`, `WayAwayMST.dtx`, `auldlangsynemetal-adv.dtx`, `auldlangsynemetal-bas.dtx`, `auldlangsynemetal-ext.dtx`, `bedtimestory-mst.dtx`, `confessionfull-bas.dtx`, `whispermint-ext.dtx` | from upstream repository, origin and licence unknown | Unknown | Unknown | Real community DTX charts: drums, 4 of 10 pure ASCII/UTF-8, 6 Shift_JIS-like, `#BPMzz` + channel |
| `README.md` | from upstream repository, origin and licence unknown | Unknown | Unknown | Lists the files of the original archive of `OceanAvenueMST.dtx` (not a chart). |
| `dtx2gp_test3.dtx` (253 B), `dtx2gp_test4.dtx` (806 B), `dtx2gp_test5.dtx` (157 B), `dtx2gp_test6.dtx` (198 B) | https://github.com/lathspell/dtx2gp/tree/c5d8a8b3847d7862e427237caf0ef50e5c1313ea/data (`data/test3.dtx` ... `test6.dtx`) | Christian Brunotte | LGPL-3.0 | Hand-written unit-test charts of a DTX-to-GuitarPro converter (drums only, measure 0-1): `test3` basic 11/12/13 patterns |
| `synthetic-drums-bpm-barlength.dtx` | hand-written for this repository from the DTXmaniaNX loader rules (`CDTX.cs`, `EChannel.cs`; see the fiche) | this repository's maintainers | CC0 / public domain | `synthetic`, ASCII, LF. All twelve drum channels (11-1C), BGM chip (01), extended BPM table |
| `synthetic-guitar-bass-hold.dtx` | same | same | CC0 | `synthetic`, ASCII, LF. `#GLEVEL`/`#BLEVEL`, `#BASEBPM: 100` with raw BPM chip `3C` on channel 03 |
| `synthetic-sjis-crlf.dtx` | same | same | CC0 | `synthetic`, **Shift_JIS (CP932) with CRLF**, Japanese `#TITLE`/`#ARTIST`, commands glued with a space instead of `:` |

Synthetic files follow the fiche text and are not verified in DTXMania.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)


| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `dtxmaniacx_01-pop-8-beat.dtx` | https://raw.githubusercontent.com/cwchanap/DTXManiaCX/bbc0254e5882431bc7a31a5275659298d4973cf6/DTXMania.Game/BundledSongs/Practice/01-pop-8-beat/01-pop-8-beat.dtx | 2026-11-09 | 0fb355f289287b29b134f9c3379d84d8a71523c44ec0a1ac1384358dd1a85b4a | cwchanap/DTXManiaCX | no licence file in the source | Generated metronome-only practice chart (pop 8-beat), UTF-8 LF |
| `dtxmaniacx_02-jazz-swing.dtx` | https://raw.githubusercontent.com/cwchanap/DTXManiaCX/bbc0254e5882431bc7a31a5275659298d4973cf6/DTXMania.Game/BundledSongs/Practice/02-jazz-swing/02-jazz-swing.dtx | 2026-11-09 | e4f33fe292f14b4074bcf2f099ef649be7bb750ab91ef374a18a40ee8469ea2b | cwchanap/DTXManiaCX | no licence file in the source | Generated metronome-only practice chart (jazz swing), UTF-8 LF |
| `dtxmaniacx_03-punk-beat.dtx` | https://raw.githubusercontent.com/cwchanap/DTXManiaCX/bbc0254e5882431bc7a31a5275659298d4973cf6/DTXMania.Game/BundledSongs/Practice/03-punk-beat/03-punk-beat.dtx | 2026-11-09 | 2fa459bd0ddd078689715ca5eeff7ba60ee480189947964f1af7d71ceae9923b | cwchanap/DTXManiaCX | no licence file in the source | Generated metronome-only practice chart (punk beat), UTF-8 LF |
| `dtxmaniacx_04-metal-double-bass.dtx` | https://raw.githubusercontent.com/cwchanap/DTXManiaCX/bbc0254e5882431bc7a31a5275659298d4973cf6/DTXMania.Game/BundledSongs/Practice/04-metal-double-bass/04-metal-double-bass.dtx | 2026-11-09 | 646ca7a2518f0f0cec77d861ad74bcdb2d0b040879f688ee656b5bcaf4bc105a | cwchanap/DTXManiaCX | no licence file in the source | Generated metronome-only practice chart (metal double bass), UTF-8 LF |
| `dtxmaniacx_sample.dtx` | https://raw.githubusercontent.com/cwchanap/DTXManiaCX/bbc0254e5882431bc7a31a5275659298d4973cf6/DTXMania.Test/TestData/sample.dtx | 2026-11-09 | 872c9dd54bd89b0cd2e5d7689c60761dacb2609ed5d878c426df7db6350ab953 | cwchanap/DTXManiaCX | no licence file in the source | Small generated test chart (966 B), 32-slot lines with ; trailing comments |
| `dtxtopng_example_input_file_1.dtx` | https://raw.githubusercontent.com/shian0346/DTXtoPNG/d8fe399b6e14ef41a391c98f9301a13edd7dbfa4/input/example_input_file_1.dtx | 2026-11-09 | 10180780b15bc591ddf3766edf0b571723c1d6d3485b9719f13b0f2831adb3de | shian0346/DTXtoPNG | no licence file in the source | Real community DTX: UTF-8 CRLF, DTXCreator 024, 7 BPM table entries |
| `dtxtopng_example_input_file_2.dtx` | https://raw.githubusercontent.com/shian0346/DTXtoPNG/d8fe399b6e14ef41a391c98f9301a13edd7dbfa4/input/example_input_file_2.dtx | 2026-11-09 | 7f06bf19aa1d241032f5e0bf82839c7d4d1996144fd8d3a8170d0fec4ecfcf59 | shian0346/DTXtoPNG | no licence file in the source | Real community DTX: Shift_JIS-like CRLF, DTXCreator 025 verK, XG left pedal/left bass lanes |
| `dtxtopng_example_input_file_3.dtx` | https://raw.githubusercontent.com/shian0346/DTXtoPNG/d8fe399b6e14ef41a391c98f9301a13edd7dbfa4/input/example_input_file_3.dtx | 2026-11-09 | 212471bd1b3bf278d4c38a25be5645b341323eb137c34849bd0ea77890d85748 | shian0346/DTXtoPNG | no licence file in the source | Real community DTX: Shift_JIS-like CRLF, 50 BPM table entries |
| `dtxtopng_example_input_file_4.dtx` | https://raw.githubusercontent.com/shian0346/DTXtoPNG/d8fe399b6e14ef41a391c98f9301a13edd7dbfa4/input/example_input_file_4.dtx | 2026-11-09 | 5c68ec6875da8732c9176cf08ffe4b4b15d5af485f0dd21fef64096ce45c1a04 | shian0346/DTXtoPNG | no licence file in the source | Real community DTX: UTF-16LE with BOM, DTXCreatorAL 010 |
| `dtxtopng_example_input_file_5.dtx` | https://raw.githubusercontent.com/shian0346/DTXtoPNG/d8fe399b6e14ef41a391c98f9301a13edd7dbfa4/input/example_input_file_5.dtx | 2026-11-09 | 0c72c37a430720c842cec97117e7a92ab32b255d723096c9ddf135bb22c99ba9 | shian0346/DTXtoPNG | no licence file in the source | Real community DTX: UTF-8 CRLF, NoChip B1-B9 channels and SE 66-72 |
