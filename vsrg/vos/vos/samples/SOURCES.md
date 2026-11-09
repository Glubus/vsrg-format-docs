# Samples: Virtual Orchestra Studio song (`.vos`)

Tiny binary songs (MIDI arrangement + playable-note track), each embedding a Standard MIDI File. Bytes unchanged from the source.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `1.vos` (57 732 B) | https://github.com/rhythmus-emulator/rparser/tree/d2efba4c36e5f74fda3da4b90f7e9119f1f62861/test/chart_sample (`test/chart_sample/1.vos`) | Unknown (song authors of the VOS community; the parser repository is by @lazykuna) | MIT | **Header int32 = 2**: followed by the length-prefixed file name `Vosctemp.trk` (12 bytes), a 32-bit [observed; layout per `src/ChartLoaderVOS.cpp` `ParseMetaDataV2` of the same repository] |
| `103.vos` (57 509 B) | same | Unknown | MIT | Header int32 = 2, tag **`VOS008`** |
| `23.vos` (91 893 B) | same | Unknown | MIT | **Header int32 = 3**: segment table `inf` / `mid` / `EOF`, then the tag `VOS1` |
| `24.vos` (56 864 B) | same | Unknown | MIT | Header int32 = 3, same layout as `23.vos`; last note 1'23 (83 000 ms) per |
| `109.vos` (216 364 B) | same | Unknown | MIT | Header int32 = 3, but the 12 bytes after the segment table are **not** zero |

Doubt (also in `/tmp/fsc-parts/doubts/ArcadePcSims.md`): community arrangements with unstated authors/licences; committed because the carrying repository is MIT.

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

Downloaded with curl on 2026-11-09, byte for byte, charts only.

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `vosdroid_Canon_in_D.vos` | https://raw.githubusercontent.com/ReVanTis/VosDroid/692f3def3293aabcd2414b4a1ff0bad6550ad5a8/android/assets/Canon%20in%20D.vos | 2026-11-09 | ee4e23be676fcfe7f78fd8ae394069e263e9f66c56ae3f3d8510ae7307aec706 | ReVanTis/VosDroid (repository; chart author see file) | no licence file in the source repository | VOS v3 song shipped with the VosDroid player file |
