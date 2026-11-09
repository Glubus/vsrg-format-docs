# Dynamaker bundle (.dy) (`.dy`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview

A single-file bundle written by Dynamaker (the web/Electron Dynamix editor) so a chart can be played on a phone: chart, music and background in one file. Per the Dynamaker guide: right-click -> "Save as .DY" (versus "Save as XML" for the chart only); DyNode's docs say the `.dy` format stores chart-related files (music, background...) in Base64.

## Contents

- A single-file bundle: chart, music and background, for playback on a phone.
- Chart format inside: [Dynamix XML](../xml/README.md) (the chart-only export).

## Container & encoding

JSON object (the loader evals it): `{ "CMap": {...}, "remix": { "music": <data URL>, "bg": <data URL, optional> } }`; music and background are base64 data URLs.

## Structure / metadata

`CMap` has the same fields as the Dynamaker CMap XML (see `../xml/`, dialect A); `remix.music` is required, `remix.bg` optional.

## Timing model

Same as `../xml/` (bars).

## Notes

Same as `../xml/`.

## Audio & images

Embedded as base64 data URLs (`remix.music`, `remix.bg`).

## Versions & variants

Unknown.

[observed in dynamaker-modified `app/src/Script/function.js`] Dynamaker writes the bundle with `JSON.stringify({CMap, remix})` (`saveAsDynaMaker`); `saveAsMinimal` writes the same shape with `remix.isMinimal: true`. The loader also accepts a plain JSON file whose name ends in `JSON` with only `{CMap}` (`loadingScene.js`).

## Quirks & pitfalls

Large files because of base64 audio; loaded with `eval` by Dynamaker (not strict JSON in practice) [inference].

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

Dynamaker-modified: <https://github.com/jmakxd/dynamaker-modified>; DyNode: <https://dyn.iorinn.moe/en/>.

## Getting samples

**Committed** ([`samples/`](samples/SOURCES.md)): `synthetic-minimal.dy`, a hand-written bundle whose `remix.music` is a generated 0.1 s silent WAV (no copyrighted audio). **Manifest:** none (a real `.dy` embeds the song as base64, so real ones are not redistributable).

**How to get more**: open or create a chart in Dynamaker / dynamaker-modified (<https://github.com/jmakxd/dynamaker-modified>) and use "Save as .DY" (`saveAsDynaMaker()`, and `saveAsMinimal()` which adds `remix.isMinimal: true`; both in `app/src/Script/function.js`) or DyNode's `.dy` import/export. The Dynamaker guide documents the export (<https://github.com/TLChicken/dynamaker-guide>). Real bundles circulate in the Dynamix fanmade community with their music inside.

## Sources

- <https://cdn.jsdelivr.net/gh/jmakxd/dynamaker-modified@master/app/src/Script/loadingScene.js>
- <https://dyn.iorinn.moe/en/guide/import.html>
- <https://github.com/TLChicken/dynamaker-guide/blob/master/Contents/Old%20Guide%20v1.0.txt>
