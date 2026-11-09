# Samples: BMS difficulty table (header.json / data.json)
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-header.json` | Hand-written by BmsAux from the fields documented in the fiche (header fields `name`, `symbol`, `tag`, `data_url`, `mode`, `level_order`, extra key `last_update`; `course` as array of groups with `constraint`, `trophy`, `md5` / `sha256` shorthand lists and a full `charts` list) | BmsAux (synthetic) | CC0 / public domain | Header with every documented key, three course styles, trophy conditions. |
| `synthetic-data.json` | Same | BmsAux (synthetic) | CC0 / public domain | Data array with md5-only, sha256-only, both, `url_diff`/`name_diff`, `url_pack`/`name_pack`/`org_md5`, per-chart `mode`, non-numeric levels (`!`, `?`), Japanese text, extra keys. Hashes are MD5/SHA-256 of arbitrary ASCII strings (`synthetic chart N`), except entry 6 which is the real hash of `../../bmson/samples/synthetic-features.bmson` as it was when written (it goes stale if that file changes). `example.invalid` URLs are placeholders. |

Live, not hashable (removed from the manifest, URL not immutable): `stella-header.json`, `stella-score.json`, `satellite-header.json`, `satellite-score.json`, `insane-header.json`, `insane-data.json`, `normal1-header.json`, `normal1-data.json`. See the fiche's Getting samples section for the live URLs.
