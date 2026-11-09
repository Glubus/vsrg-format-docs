# Samples: StepMania `.edit`

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-springtime-ssc-style.edit | Public domain (CC0); hand-written for this corpus | StepmaniaFamily corpus (generated) | CC0 / public domain | synthetic. SM5-writer layout (`#SONG`, `#NOTEDATA`, `#STEPSTYPE:dance-single`, `#DIFFICULTY:Edit`) targeting the bundled song `StepMania 5/Springtime`; 4 measures with 4/8/16/12 rows: taps, a jump, a hold (2..3), a roll (4..3), a mine (M), a lift (L), a fake (F) |
| synthetic-springtime-sm-style.edit | Public domain (CC0); hand-written for this corpus | StepmaniaFamily corpus (generated) | CC0 / public domain | synthetic. SM 3.9/4-style layout: `#SONG` then one six-parameter `#NOTES:` tag (stepstype:description:difficulty:meter:radar:notes); same note content |
| synthetic-springtime-ssc-style-doubles.edit | Public domain (CC0); hand-written for this corpus | StepmaniaFamily corpus (generated) | CC0 / public domain | synthetic. 8-column `dance-double` edit in SSC layout (no radar values, no description tag order change); hold, mine and jumps across both pads |

Built strictly from the layout in this folder's README (`NotesWriterSSC::GetEditFileContents`) and the `.sm` note grammar; the only real `.edit` content in the repo is the inline `Edit` chart of `../ssc/samples/Tokimeki Experience.ssc`. No real `.edit` file with an open licence was found (edits live in players' profiles). The target song `StepMania 5/Springtime` is bundled with StepMania (chart in `../ssc/samples/Springtime.ssc`).
