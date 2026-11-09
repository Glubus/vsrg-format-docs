# Samples: bmson
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-features.bmson` | Already in the repository before this corpus work (commit `a7c56f8`, "enriched format reference"); hand-written synthetic file, authorship not otherwise recorded | unknown (repository owner / earlier contributor) | unknown (labelled synthetic; presumed public domain, to be confirmed by the owner) | bmson 1.0.0 `mode_hint beat-7k`, `resolution 240`, `lines`, a `bpm_events` change, a `stop_events` entry, 3 sound channels (one BGM, two keysound channels) with long notes (`l` > 0), empty `bga`. |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `bms-rs_lostokens.bmson` | https://raw.githubusercontent.com/MikuroXina/bms-rs/1eb789caa32a3e0851d274723468576de26a2d08/tests/bmson/files/lostokens.bmson | Third-party chart (wosderge); repo bms-rs is Apache-2.0 but the chart licence is not stated | bmson 1.0.0 beat-7k, resolution 240, 39 sound channels, 67 long notes, bga block (224986 bytes, sha256 `ced64b2ababe3d50...`) |
| `bms-rs_bemusicstory_483_48K_ANOTHER.bmson` | https://raw.githubusercontent.com/MikuroXina/bms-rs/1eb789caa32a3e0851d274723468576de26a2d08/tests/bmson/files/bemusicstory_483_48K_ANOTHER.bmson | Third-party event chart (BE-MUSiC STORY); licence not stated; not committed | mode_hint keyboard-24k-double (48 keys), resolution 7920, bpm_events, bga_header/bga_events, 1295 sound channels; 790 KB (789615 bytes, sha256 `c6b9fa5eb66319d1...`) |
| `bemuse-ninja_onlylove_remix_beginner.bmson` | https://web.archive.org/web/20160222162836id_/http://bemuse.ninja/music/%5Bflicknote%5Donlylove_remix/onlylove_remix_beginner.bmson | CC-BY-NC (declared in the chart info.license field and in the song README); NC terms so not committed | bmson 1.0.0 as served by the Bemuse music server, beginner chart, 10 sound channels, 10 long notes; live URL (not pinned, may change) (43859 bytes, sha256 `3dfd830a4b1e724d...`) |

No licensed real bmson chart was found: the real files above are third-party charts or CC-BY-NC, so they are only fetched. The official `bemusic/bmson-spec` repository (commit `668c4338cd7c64da2d2ec0f848c4ad58a3a881d9`) has no LICENSE file and no sample file, only the RST specification, so nothing was taken from it.

Live, not hashable (removed from the manifest, URL not immutable): `bemuse-ninja_onlylove_remix_normal.bmson`, `bemuse-ninja_onlylove_remix_hyper.bmson`. See the fiche's Getting samples section for the live URLs.
