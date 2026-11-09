# Samples: Quaver mapset package (`.qp`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| built-princess-of-winter-audioless.qp | built here with Python `zipfile` (deflate, fixed 2020-01-01 timestamps) from the 8 `Maps/PrincessOfWinter/*.qua` files of Quaver/Quaver @ e9b54a66c5274b1651328c66e9ea3846f8614508 (committed in ../qua/samples/quaver-resources_PrincessOfWinter_*.qua) | Quaver / Quaver.Resources contributors; container assembled here | CC-BY-NC 4.0 (Quaver.Resources/LICENSE.md) | 32 KB flat, audio-less `.qp`: 8 difficulties named `<id>.qua` (2043..5507) at the archive root as real Quaver exports do (compare the manifest packages); the `AudioFile` it references is absent |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| quaver-default_Lollipop-vibing-outside-the-supermarket.qp | https://raw.githubusercontent.com/Quaver/Quaver/e9b54a66c5274b1651328c66e9ea3846f8614508/Quaver.Resources/Quaver.Resources/DefaultMaps/Lollipop%20-%20vibing%20oustide%20the%20supermarket%20at%201am.qp | Quaver.Resources is CC-BY-NC 4.0 (Quaver.Resources/LICENSE.md and README.md); song copyright is the artists | real Quaver default mapset (4 .qua + mp3 + jpg); audio so not committed |
| quaver-default_zetoban-Flowering-Night.qp | https://raw.githubusercontent.com/Quaver/Quaver/e9b54a66c5274b1651328c66e9ea3846f8614508/Quaver.Resources/Quaver.Resources/DefaultMaps/zetoban%20-%20Flowering%20Night.qp | Quaver.Resources is CC-BY-NC 4.0 (Quaver.Resources/LICENSE.md and README.md); song copyright is the artists | real Quaver default mapset with 6 difficulties (+ mp3 + jpg); audio so not committed |
| quaver-default_zetoban-Csikos-Post.qp | https://raw.githubusercontent.com/Quaver/Quaver/e9b54a66c5274b1651328c66e9ea3846f8614508/Quaver.Resources/Quaver.Resources/DefaultMaps/zetoban%20-%20Csikos%20Post.qp | Quaver.Resources is CC-BY-NC 4.0 (Quaver.Resources/LICENSE.md and README.md); song copyright is the artists | real Quaver default mapset with 6 difficulties (+ mp3 + png); audio so not committed |

## Notes

- Layout of the real packages (verified by listing the three manifest files with Python `zipfile`): flat root, `<mapid>.qua` files + one mp3 + one background jpg/png, no folders.
