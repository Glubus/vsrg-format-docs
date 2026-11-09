# Samples: Pocket DDR `.sdf`

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| test.sdf | https://github.com/stepmania/stepmania/blob/7cbaff8ce2dcbede32dd3d6f3f2d8fafeafd674e/Docs/SimfileFormats/SDF/test.sdf | StepMania docs | MIT (StepMania repository) | Real converter output of SM2SDF for `../../stepmania/sm/samples/stepmania-docs_test.sm` (the source `.sm`): 812 bytes, starts with an embedded PNG (the 97-byte `ssc-banner.png` of the docs), a second PNG (background), then the chart data; two BPMs (93.81 -> 187.62) |
| test-1bpm.sdf | https://github.com/stepmania/stepmania/blob/7cbaff8ce2dcbede32dd3d6f3f2d8fafeafd674e/Docs/SimfileFormats/SDF/test-1bpm.sdf | StepMania docs | MIT (StepMania repository) | Same song converted with a single BPM (804 bytes); useful to diff against `test.sdf` for the tempo-change encoding |

The two embedded images are the tiny placeholder PNGs (`ssc-banner.png`, `ssc-bg.png`) from `Docs/SimfileFormats/SDF/` of the StepMania repository; they are part of the files and are not copyrighted artwork.
