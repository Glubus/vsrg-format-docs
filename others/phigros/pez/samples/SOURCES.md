# Samples: Phira / PhiZone chart package (`.pez`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rpechart_demo.pez` | https://github.com/kamilhzn/rpechart/blob/58e6f624df967a37d839206c6d1c5fed5e30b5d3/tests/fixtures/demo.pez | kamilhzn / rpechart contributors | MIT (rpechart `LICENSE`) | zip package built by the library's `export_pez`: 2 members only, `chart.json` (RPE JSON, `RPEVersion` 160, name `Fixture Song`) and `info.txt` (CRLF, PhiEdit-style `Name:`/`Path:`/`Song:`/`Picture:`/`Chart:`/`Level:`/`Composer:`/`Charter:` keys, first line `#`). No audio or image is inside (`song.mp3`, `background.png` are only named); zip timestamps frozen to 2024-01-01 |

Notes: the package has no audio or picture, so it is not playable on its own; it shows the container layout only.
