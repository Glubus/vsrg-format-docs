# Samples: Interlude chart data (`.yav` / headless binary chart)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-4k-headless.bin | written for this repository with Python `struct` from Prelude `Chart.WriteToStreamHeadless` (YAVSRG/YAVSRG @ a7c78e77733595749e63da26b5300e8962a4e111, prelude/src/Charts/Chart.fs, NoteRow.fs, Shared/TimeArray.fs) | this repository | CC0 / public domain | 114 bytes: 4 keys, 7 note rows incl. 2 holds (HOLDHEAD, HOLDBODY, HOLDTAIL rows), 2 BPM entries (500 and 400 ms/beat, meter 4), 3 SV entries; no key count, header or hash stored in the blob (the key count is external). Decoded back with an independent Python reader that also reproduces the SHA-256 `Chart.Hash()` of 7 real CDN charts; the hash of this file is 3E146DAD7DF928E7E59C44634580E5E2BFB3B47362DC1CED0D1E32E75B8ED3F9 [computed with the same Python, not by Interlude] |

## Live, not hashable (no manifest entries)

Real charts are served by the Interlude CDN at `https://cdn.yavsrg.net/<CHART-HASH>` (hash = `Chart.Hash()`, listed in `backbeat/archive/charts.json` of YAVSRG/YAVSRG). On 2026-11-09 only a small part of the listed hashes still downloaded (4K, 6K, 7K and 9K ones; the others answered HTTP 404 `{"code":"not_found"...}`). Seven files were downloaded and decoded successfully (e.g. `10998A89...` 4K 1537 bytes, `63416743...` 9K 1869 bytes, `A46FD3D6...` 7K 2418 bytes, `C9838B18...` 6K 17773 bytes), but the CDN is a live site whose content may be removed, so they are not in the manifest and their redistribution rights are unknown.
