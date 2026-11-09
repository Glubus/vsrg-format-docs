# Samples: Malody chart package (`.mcz`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| built-quaver-api-malody-audioless.mcz | built here with Python `zipfile` (deflate, fixed 2020-01-01 timestamps) from the three `quaver-api_*.mc` files (Quaver.API @ a921d561b2ece7f6bf3682446696c06c17b81649) | chart authors as in the .mc; container assembled here | MPL-2.0 repository; chart licence unknown | 10 KB flat audio-less package with 3 Key-mode `.mc` (4 columns, `bar_begin` 0/2/6) named by their timestamp ids; the audio/background they reference are absent (layout is an [inference]: the real layout is Unknown in the fiche) |
| built-mc2tja-taiko-audioless.mcz | built here from `mc2tja_FranticWolf.mc` and `mc2tja_KappaSays.mc` (LuiCat/mc2tja @ 58ffc91b4220e53a7884ae021e24f7a0d15c388d) | LuiCat; container assembled here | MIT (mc2tja LICENSE) | audio-less package with the two Taiko-mode (mode 5) charts at the root; same layout caveat |

## Notes

- Entries are placed flat at the archive root. Whether real `.mcz` files use a flat layout or per-chart folders is Unknown in the fiche; these packages are valid ZIPs for tests of the container only.
