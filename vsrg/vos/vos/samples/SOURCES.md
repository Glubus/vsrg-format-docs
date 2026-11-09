# Samples: Virtual Orchestra Studio song (`.vos`)

Files are tiny binary songs (MIDI arrangement + playable-note track); each embeds a Standard MIDI File, there is no external audio. Bytes unchanged from the source repository.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `1.vos` (57 732 B) | https://github.com/rhythmus-emulator/rparser/tree/d2efba4c36e5f74fda3da4b90f7e9119f1f62861/test/chart_sample (`test/chart_sample/1.vos`) | Unknown (song authors of the VOS community; the parser repository is by @lazykuna) | MIT (rparser `LICENSE.md`, Copyright (c) 2017 @lazykuna). The licence covers the repository; the provenance of the song data is unknown, see doubt note. | **Header int32 = 2**: followed by the length-prefixed file name `Vosctemp.trk` (12 bytes), a 32-bit size, the tag **`VOS022`**, then length-prefixed text fields (16-bit lengths) and 0x3F7 reserved bytes [observed; layout per `src/ChartLoaderVOS.cpp` `ParseMetaDataV2` of the same repository]. Test case `RPARSER.VOSFILE_V2`. |
| `103.vos` (57 509 B) | same | Unknown | MIT (repository) | Header int32 = 2, tag **`VOS008`** (the loader only checks the prefix `VOS`; its comments mention `VOS009`/`VOS022`). Test case `VOSFILE_V2`. |
| `23.vos` (91 893 B) | same | Unknown | MIT (repository) | **Header int32 = 3**: segment table `inf` / `mid` / `EOF`, then the tag `VOS1` and length-prefixed (1-byte) text fields; the repository's test comment says last note at 2'05 (125 000 ms). Test case `VOSFILE_V3`. |
| `24.vos` (56 864 B) | same | Unknown | MIT (repository) | Header int32 = 3, same layout as `23.vos`; last note 1'23 (83 000 ms) per the test comment. |
| `109.vos` (216 364 B) | same | Unknown | MIT (repository) | Header int32 = 3, but the 12 bytes after the segment table are **not** zero, so `ParseMetaDataV3` takes its other branch (4 text fields, no `VOS1` tag); largest sample, last note 4'00 (240 000 ms) per the test comment. |

Doubt (also in `/tmp/fsc-parts/doubts/ArcadePcSims.md`): these are community song arrangements whose original authors/licences are not stated; they are committed only because the repository carrying them is MIT-licensed.

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
| --- | --- | --- | --- |
| `vosdroid_Canon_in_D.vos` | https://raw.githubusercontent.com/ReVanTis/VosDroid/692f3def3293aabcd2414b4a1ff0bad6550ad5a8/android/assets/Canon%20in%20D.vos | The repository has no licence file (checked at that commit); the composition (Pachelbel) is public domain but the arrangement's authorship is unknown | Header int32 = 3 (`inf`/`mid`/`EOF` table), 66 921 B; the sample song shipped with the VosDroid Android player, i.e. the file the open parser `VosParser.java` was developed against. |
