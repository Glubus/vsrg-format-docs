# Samples: osu! storyboard (`.osb`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| ppy-osu_animation-loop-no-explicit-end-time.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/animation-loop-no-explicit-end-time.osb | ppy/osu contributors | MIT | (`animation-loop-no-explicit-end-time`): 151 bytes, first line `[Events]`, 3 command lines |
| ppy-osu_animation-starts-before-alpha.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/animation-starts-before-alpha.osb | ppy/osu contributors | MIT | (`animation-starts-before-alpha`): 236 bytes, first line `[Events]`, 2 command lines |
| ppy-osu_animation-types.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/animation-types.osb | ppy/osu contributors | MIT | (`animation-types`): 431 bytes, first line `osu file format v14`, 0 command lines |
| ppy-osu_image-specified-as-video.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/image-specified-as-video.osb | ppy/osu contributors | MIT | (`image-specified-as-video`): 51 bytes, first line `osu file format v14`, 0 command lines |
| ppy-osu_loop-containing-earlier-non-zero-fade.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/loop-containing-earlier-non-zero-fade.osb | ppy/osu contributors | MIT | (`loop-containing-earlier-non-zero-fade`): 554 bytes, first line `osu file format v14`, 7 command lines |
| ppy-osu_loop-count.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/loop-count.osb | ppy/osu contributors | MIT | (`loop-count`): 329 bytes, first line `osu file format v14`, 9 command lines |
| ppy-osu_noop-fade-transform-is-ignored-for-lifetime.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/noop-fade-transform-is-ignored-for-lifetime.osb | ppy/osu contributors | MIT | (`noop-fade-transform-is-ignored-for-lifetime`): 253 bytes, first line `[Events]`, 4 command lines |
| ppy-osu_out-of-order-starttimes.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/out-of-order-starttimes.osb | ppy/osu contributors | MIT | (`out-of-order-starttimes`): 173 bytes, first line `[Events]`, 2 command lines |
| ppy-osu_variable-with-self-reference.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/variable-with-self-reference.osb | ppy/osu contributors | MIT | (`variable-with-self-reference`): 136 bytes, first line `[Variables]`, 0 command lines |
| ppy-osu_variable-with-suffix.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/variable-with-suffix.osb | ppy/osu contributors | MIT | (`variable-with-suffix`): 79 bytes, first line `[Variables]`, 0 command lines |
| ppy-osu_video-background-events-ignored.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/video-background-events-ignored.osb | ppy/osu contributors | MIT | (`video-background-events-ignored`): 78 bytes, first line `osu file format v14`, 0 command lines |
| ppy-osu_video-custom-alpha-transform.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/video-custom-alpha-transform.osb | ppy/osu contributors | MIT | (`video-custom-alpha-transform`): 77 bytes, first line `osu file format v14`, 1 command lines |
| ppy-osu_video-with-lowercase-extension.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/video-with-lowercase-extension.osb | ppy/osu contributors | MIT | (`video-with-lowercase-extension`): 71 bytes, first line `osu file format v14`, 0 command lines |
| ppy-osu_video-with-uppercase-extension.osb | https://github.com/ppy/osu/blob/bb37f0541894e46460fe8cdb5ec495d0fb0ac7f2/osu.Game.Tests/Resources/video-with-uppercase-extension.osb | ppy/osu contributors | MIT | (`video-with-uppercase-extension`): 71 bytes, first line `osu file format v14`, 0 command lines |

## Notes

- The `ppy-osu_*` files are tiny hand-made lazer storyboard-decoder test cases; each isolates one behaviour named by its file name (animation loops, `Variables` substitution, video events, out-of-order start times).
- The real storyboards (tens of KB, ranked sets) come from the osu-file-parser fixtures; upstream declares `MIT OR Apache-2.0` in Cargo.toml but has no LICENSE file. They are in the second table.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

Committed as downloaded (charts only; archives stripped of audio and images).

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `osu-file-parser_aspire_osb1.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/aspire_osb1.osb | 2026-11-09 | b3927659721c314cdf195aafdc3b84131d2032f3480b620ccbbe5c1f3cc39a11 | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_legacy_event.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/legacy_event.osb | 2026-11-09 | d47d151a5f691c100f3cdea5e4a844bb1093df6b9886e7c628582baaade70f93 | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_match_test.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/match_test.osb | 2026-11-09 | 7d0f71a88b33bc67d566ffc02f5b01846b981cc7192b3078483ff748676ad0d1 | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_osb.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/osb.osb | 2026-11-09 | 0d69637e62f2a1734dcc81f9940662a985083dce2f91a20a6f9baeab55ee2141 | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_osb_2.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/osb_2.osb | 2026-11-09 | 164c127d1a4286f5b6f18e19f51510ecec468f56cf5f40009e3c9074ba8f761b | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_variable.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/variable.osb | 2026-11-09 | 7d1b1840833b306264f2f3bab5fd5dfa463aca41e5686390654cb75ac50ad7d6 | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
| `osu-file-parser_variable2.osb` | https://raw.githubusercontent.com/Eddio0141/osu-file-parser/f3de899c4ee2d1ecb4313bd62d4ab332bf51adf9/src/tests/osu_files/files/variable2.osb | 2026-11-09 | 2305c40240c6f0ef86a2f2243306fb139f79d0175af27e1a9ccff8e12763e0dd | Eddio0141/osu-file-parser | Community map used as a parser test fixture | real storyboard |
