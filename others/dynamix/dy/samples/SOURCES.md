# Samples: Dynamaker bundle (`.dy`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-minimal.dy` | hand-written for this repository, built from `saveAsDynaMaker()` in jmakxd/dynamaker-modified `app/src/Script/function.js` (JSON `{CMap, remix:{bg, music}}`) and the loader in `loadingScene.js`; same notes as `../xml/samples/synthetic-cmap.xml` | vsrg-format-docs contributors | CC0-1.0 / public domain (synthetic) | Dynamaker `.dy` JSON bundle (single line, `JSON.stringify` style): `CMap` object with `m_notes.m_notes.CMapNoteAsset` arrays, side regions PAD/MIXER, `m_bpmchange`, and `remix.music` = base64 `data:` URL of a 0.1 s silent 8-bit 8 kHz mono WAV generated for this file (no copyrighted audio), `remix.bg` = null. Value types (JSON numbers vs strings) in real files are not verified [inference] (2134 bytes) |

