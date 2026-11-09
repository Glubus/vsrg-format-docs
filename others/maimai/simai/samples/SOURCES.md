# Samples: simai / `maidata.txt`

`synthetic-maidata.txt` parses with MaiConverter's `parse_file_str` (MIT). `synthetic-maidata-3simai-extras.txt` is checked against the wiki text only: MaiConverter rejects connected slides, `[#s]`, `[a##b]` durations and `{#s}` commas.

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-maidata.txt` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | `maidata.txt` with header fields (`&title`, `&artist`, `&smsg`, `&des`, `&first`, `&wholebpm`, `&lv_N`, `&des_N`) and two charts |
| `synthetic-maidata-3simai-extras.txt` | hand-written, synthetic | vsrg-format-docs contributors | CC0-1.0 | 3simai-only forms: `\|\|` comment line, per-difficulty `&first_5`, connected slides (`1-4q7-2[1:2]`, per-segment durations), absolute durations `[#1.5]` |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)


| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `maidata-bpmChanges.txt` | https://raw.githubusercontent.com/Neskol/MaichartConverterUnitTest/fe07fd0a4a133b831121953a01c9528bdb4ffc68/MaichartConverterUnitTest/data/maidata-bpmChanges.txt | 2026-11-09 | 41854650c11eec60023feec8befe078610ef6beb78aa64ad0b6493e407bf93b9 | Neskol/MaichartConverterUnitTest (repository; chart author see file) | CC0-1.0 | simai `maidata.txt` (33 KB) by MaichartConverter: `[SD]` title, `&inote_2`..`&inote_5`, very many inline BPM changes `(..)` |
| `maidata_internet_overdose.txt` | https://raw.githubusercontent.com/Neskol/MaichartConverterUnitTest/fe07fd0a4a133b831121953a01c9528bdb4ffc68/MaichartConverterUnitTest/data/maidata_internet_overdose.txt | 2026-11-09 | ebad0fcca052438f2a5dd2bc0928c6dc7e9f500fd29f4eae164f7a565d0f1b93 | Neskol/MaichartConverterUnitTest (repository; chart author see file) | CC0-1.0 | simai `maidata.txt` by MaichartConverter: `[DX]` title, `&wholebpm`, `&shortid`, `&cabinet=DX`, `&version`, `&inote_2`..`&inote_5`, touch notes, 7 distinct |
| `maidata_pandora.txt` | https://raw.githubusercontent.com/Neskol/MaichartConverterUnitTest/fe07fd0a4a133b831121953a01c9528bdb4ffc68/MaichartConverterUnitTest/data/maidata_pandora.txt | 2026-11-09 | 358905d16edf34f73c7a3e3fe3c894ba75ff99c43e24aedd16a9e13b935f5384 | Neskol/MaichartConverterUnitTest (repository; chart author see file) | CC0-1.0 | simai `maidata.txt` written by MaichartConverter: UTF-8 without BOM, LF, `[SD]` title, `&inote_2`..`&inote_6`, no touch notes |
| `maidata_uma.txt` | https://raw.githubusercontent.com/Neskol/MaichartConverterUnitTest/fe07fd0a4a133b831121953a01c9528bdb4ffc68/MaichartConverterUnitTest/data/maidata_uma.txt | 2026-11-09 | 0c6a2dcbda7fafcc581adc7bf089ac68435ffc3a4d0e68ecfd139159aa8d80c0 | Neskol/MaichartConverterUnitTest (repository; chart author see file) | CC0-1.0 | simai `maidata.txt` by MaichartConverter: `[DX]` title, `&inote_2`..`&inote_6`, touch notes (`B1`, `C1h[..]` forms), 8 distinct inline |
| `maidata_uma_hold.txt` | https://raw.githubusercontent.com/Neskol/MaichartConverterUnitTest/fe07fd0a4a133b831121953a01c9528bdb4ffc68/MaichartConverterUnitTest/data/maidata_uma_hold.txt | 2026-11-09 | d01eabdcda9c677467d09dfb5d525df0d4e610b643e8b32b08bbc13c2cc1827d | Neskol/MaichartConverterUnitTest (repository; chart author see file) | repo says CC0 but looks like an excerpt | Short (716 B) `[DX]`-title excerpt with UTF-8 BOM, a single `&inote_6=`: tempo changes `(114.5)`..`(94.5)`, divisor [inference] |

