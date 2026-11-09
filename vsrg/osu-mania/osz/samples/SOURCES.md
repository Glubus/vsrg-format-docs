# Samples: osu! mapset archive (`.osz`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| ppy-osu_japanese-filename.osz | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/japanese-filename.osz | ppy/osu contributors | MIT (ppy/osu LICENCE, Copyright (c) 2025 ppy Pty Ltd) | 816-byte archive with one `artist - title (peppy) [difficulty].osu` plus two **0-byte** audio entries (`track.ogg` and a second one whose name bytes are CP932-encoded Japanese, stored without the zip UTF-8 flag): tests the Shift-JIS entry-name decoding [inference from the file name and ZipArchiveReader.DEFAULT_ENCODING]. No real audio inside, so it is committed unchanged. |
| yavsrg-prelude_2089086 The Living Tombstone - My Ordinary Life (Speed up Ver.).osz | https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/tests/test_data/Osz/2089086%20The%20Living%20Tombstone%20-%20My%20Ordinary%20Life%20%28Speed%20up%20Ver.%29.osz | mapper Overlord68_ (Creator field) | MIT (prelude/LICENSE, Copyright (c) 2024 percyqaz) for the repository; the map is a community map, its own licence is unknown | 52 KB, audio-less real mapset: 5 mania 4K difficulties (1.0x-1.4x rate variants, v14), no audio/image files |
| yavsrg-prelude_989392 DJ Sharpnel - World Sound.osz | https://github.com/YAVSRG/YAVSRG/blob/a7c78e77733595749e63da26b5300e8962a4e111/prelude/tests/test_data/Osz/989392%20DJ%20Sharpnel%20-%20World%20Sound.osz | mapper Night Bunny 7 (Creator field) | MIT (prelude/LICENSE, Copyright (c) 2024 percyqaz) for the repository; the map is a community map, its own licence is unknown | 252 KB, audio-less real mapset: 10 mania 4K difficulties (LN Challenge and Lv.25 sets, base + 1.1x-1.4x rates, v14); names contain `[`, `]` and `'` |
| built-mania-key-counts-audioless.osz | built here with Python `zipfile` (deflate, fixed 2020-01-01 timestamps, ASCII entry names) from MIT ppy/osu files at bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2: Mania.Tests `4K.osu`, `7K.osu`, `10K.osu`, `mania-slider.osu` and Tests `loop-count.osb` | ppy/osu contributors (container assembled by this repository) | MIT (ppy/osu LICENCE, Copyright (c) 2025 ppy Pty Ltd); the zip itself is released as CC0 | 2.4 KB audio-less package: three mania difficulties (4K/7K/10K), the v5 slider file and a `.osb` storyboard in the standard layout `Artist - Title (Creator) [Version].osu` / `.osb`. The `.osu` bytes are unchanged; only the entry names were chosen here (the source files have no [Metadata]). |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| ppy-osu_conflicting-filenames-beatmap.osz | https://raw.githubusercontent.com/ppy/osu/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/conflicting-filenames-beatmap.osz | MIT (ppy/osu repository LICENCE; test resource of the lazer test suite) | lazer importer test archive (conflicting file names): 1 .osu, track.ogg, spinner-osu.ogg, spinner-osu.png (small); contains audio/image so not committed |
| ppy-osu_ogg-beatmap.osz | https://raw.githubusercontent.com/ppy/osu/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/ogg-beatmap.osz | MIT (ppy/osu repository LICENCE; test resource of the lazer test suite) | lazer importer test archive: oggbeatmap.osu + sample.ogg + track.ogg + __MACOSX entry (zip flag bit 3 set); contains audio so not committed |
| ppy-osu_Soleily-Renatus_virtual_quick.osz | https://raw.githubusercontent.com/ppy/osu/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/Archives/241526%20Soleily%20-%20Renatus_virtual_quick.osz | MIT (ppy/osu repository LICENCE; test resource of the lazer test suite) | lazer test copy of the bundled mapset 241526 Soleily - Renatus, audio removed: 12 .osu in all four modes (ExPew diffs are mania) + 87 KB background jpg + __MACOSX entries; image so not committed |

## Notes

- `.osz` is a ZIP; every committed archive is audio-less. lazer's own archives with audio/images are in the manifest (they contain tiny test `.ogg`/`.png`, or an 87 KB jpg).
- `.osk` skins are not charts and are not collected.
