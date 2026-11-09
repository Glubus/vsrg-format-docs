# Samples: Bemuse sound pack (.bemuse + metadata.json)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `bemuse-test-a-metadata.json` | https://github.com/bemusic/bemuse at `4bf3e7d98a44841b323741cc403ecb7b41618ade`, `bemuse/src/resources/test-fixtures/a/metadata.json` (fixture `b` has a byte-identical metadata.json) | Bemuse contributors | AGPL-3.0 (repo `LICENSE`, read; README: "AGPLv3 ... only applies to the main Bemuse project") | `metadata.json` index: 3 files mapped to one chunk (`ref` = `[chunk index, start, end]`), `refs` with payload hash. |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)
| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `bemuse-test-a_mp3.0.ea6087c3.bemuse` | https://raw.githubusercontent.com/bemusic/bemuse/4bf3e7d98a44841b323741cc403ecb7b41618ade/bemuse/src/resources/test-fixtures/a/mp3.0.ea6087c3.bemuse | AGPL-3.0 (bemuse repo); test audio fixture, so not committed | Minimal .bemuse chunk with three mp3 files (do.mp3, mi.mp3, sol.mp3); pair with the committed bemuse-test-a-metadata.json (90293 bytes, sha256 `24b81020d31ea78e...`) |
| `bemuse-test-b_mp3.0.ea6087c3.bemuse` | https://raw.githubusercontent.com/bemusic/bemuse/4bf3e7d98a44841b323741cc403ecb7b41618ade/bemuse/src/resources/test-fixtures/b/mp3.0.ea6087c3.bemuse | AGPL-3.0 (bemuse repo); test audio fixture, so not committed | Variant chunk (99846 vs 90293 bytes) of the same three mp3 files, same metadata.json as test fixture a (see the committed bemuse-test-a-metadata.json) (99846 bytes, sha256 `8a4efe9e4d52f67f...`) |

Live, not hashable (removed from the manifest, URL not immutable): `bemuse-ninja_onlylove_remix_metadata.json`, `bemuse-ninja_onlylove_remix_m4a.5.18649bde.bemuse`. See the fiche's Getting samples section for the live URLs.
