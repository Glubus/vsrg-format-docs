# Samples: ArcCreate package / project (`.arcpkg`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `etoile_sn.test.noaudio.arcpkg` | BUILT here from https://github.com/freeze-dolphin/EtoileResurrection/blob/6c20526e9782a60212fdc3f6be8b9ebb8636a341/core/src/test/resources/ArcCreate_project/sn.test.arcpkg by dropping `test/base.ogg` and `test/base.jpg` (entries and timestamps otherwise preserved) | freeze-dolphin (original); audio-less rebuild by OthersA | GPL-3.0 (repo LICENSE) | ArcCreate package (zip): root `index.yml` (`- directory: test`, `identifier: sn.test`, `settingsFile: project.arcproj`, `type: level`) plus `test/0.aff`..`4.aff` and `test/project.arcproj`; the project file still names `base.ogg`/`base.jpg`, which are absent here |
| `etoile_project.arcproj` | https://github.com/freeze-dolphin/EtoileResurrection/blob/6c20526e9782a60212fdc3f6be8b9ebb8636a341/core/src/test/resources/ArcCreate_project/project.arcproj | freeze-dolphin (EtoileResurrection test resources) | GPL-3.0 (repo LICENSE) | loose ArcCreate project file (YAML): `lastOpenedChartPath`, `charts[]` with `chartPath`, `audioPath`, `jacketPath`, `baseBpm`, `bpmText`, `syncBaseBpm`, `title`, `composer`, `difficulty`, `chartConstant`, `difficultyColor`, `skin{...}`, `previewEnd`, `lastWorkingTiming` |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `etoile_sn.test.arcpkg` | https://raw.githubusercontent.com/freeze-dolphin/EtoileResurrection/6c20526e9782a60212fdc3f6be8b9ebb8636a341/core/src/test/resources/ArcCreate_project/sn.test.arcpkg | GPL-3.0 repo; original package, includes a 44 KB base.ogg and base.jpg (test media of unknown origin), hence not committed (an audio-less rebuild is committed) | Original un-modified ArcCreate `.arcpkg` (9 entries incl. base.ogg/base.jpg) (8457 bytes) |
