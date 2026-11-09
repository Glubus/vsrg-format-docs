# Samples: SNG song package (`.sng`)

## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| synthetic-chart-audioless.sng | Synthetic: written by script for this repository, built from the fiche and the mdsitton/SngFileFormat specification | GuitarGames (ROX sample corpus) | CC0 1.0 / public domain (declared by the author of this file) | SNG version 1 with a hand-computed mask, 11 metadata pairs and one file `notes.chart` (the bytes of `chart/samples/synthetic-feature-tour.chart`); built by script strictly from the specification in mdsitton/SngFileFormat (README + SngLib/SngSerializer.cs, repo licence MIT) and re-parsed with an independent reader (header, metadata, index, unmasking all consistent). **No audio**: the package is not playable in-game |
| synthetic-mid-audioless.sng | Synthetic: written by script for this repository, built from the fiche and the mdsitton/SngFileFormat specification | GuitarGames (ROX sample corpus) | CC0 1.0 / public domain (declared by the author of this file) | Same, with one file `notes.mid` (the bytes of `mid/samples/synthetic-notes.mid`) and `.mid`-related metadata (delay, multiplier_note, sysex_slider, sysex_open_bass); different xorMask; no audio |
