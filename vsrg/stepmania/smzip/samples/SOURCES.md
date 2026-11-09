# Samples: StepMania `.smzip`

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-springtime-chart-only.smzip | Public domain (CC0); hand-written for this corpus (container); content from https://github.com/stepmania/stepmania/blob/7cbaff8ce2dcbede32dd3d6f3f2d8fafeafd674e/Songs/StepMania%205/Springtime/Springtime.ssc | Container: StepmaniaFamily corpus; chart: Kommisar / Vin.il | Container CC0; chart under the StepMania songs licence (CC-NC) | Audio-less rebuild: a plain ZIP (deflate, level 9, fixed 1980-01-01 timestamps, zip comment) holding only `Songs/StepMania 5/Springtime/Springtime.ssc` with forward-slash paths and no smzip.ctl: the layout many community packs use |
| synthetic-springtime-smpackage-layout.smzip | Public domain (CC0); hand-written for this corpus (container); content from the StepMania repository | Container: StepmaniaFamily corpus | Container CC0; Springtime chart CC-NC, Jupiter.crs MIT | Audio-less rebuild following the smpackage layout in this folder's README: `smzip.ctl` (`[SMZIP] Version=1`, `NumPackages=2`, backslash package paths; CRLF line endings are an inference) + `Songs\StepMania 5\Springtime\Springtime.ssc` + `Courses\Default\Jupiter.crs`, backslash entry names |

Both archives were built with Python `zipfile` from files of the repository; no audio, images or video are inside, so the song cannot be played (StepMania would load the chart and report missing music). No real, small, open-licence `.smzip` was found: see "Getting samples" in the fiche (real packs are 100 MB+).

Observed while probing `https://download.stepmania.amx.io/PNEXT2.smzip` (a 6 MB theme package, live URL, NOT in the manifest because it is not immutable and has no Wayback copy): its 286 entries use WinZip-AES encryption (ZIP method 99, flag bits 0x801), including `smzip.ctl` and `smzip.sig`, and its zip comment is `PNEXT2`; such packages cannot be listed without the key.
