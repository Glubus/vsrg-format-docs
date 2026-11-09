# Dynamaker bundle (.dy) (`.dy`)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
Single-file bundle written by Dynamaker (the web/Electron Dynamix editor): chart, music and background, for playback on a phone. In Dynamaker: right-click -> "Save as .DY" ("Save as XML" saves the chart only). DyNode's docs say `.dy` stores chart-related files (music, background...) in Base64.

## Contents
Chart ([Dynamix XML](../xml/README.md)), music, background.

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
[observed: dynamaker-modified `app/src/Script/function.js`] Dynamaker writes the bundle with `JSON.stringify({CMap, remix})` (`saveAsDynaMaker`); `saveAsMinimal` writes the same shape with `remix.isMinimal: true`. The loader also accepts a plain JSON file whose name ends in `JSON` with only `{CMap}` (`loadingScene.js`).

## Quirks & pitfalls
Large because of base64 audio; Dynamaker loads it with `eval` (not strict JSON in practice) [inference].

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

Dynamaker-modified: <https://github.com/jmakxd/dynamaker-modified>; DyNode: <https://dyn.iorinn.moe/en/>.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). No real `.dy` was found (bundles embed the song as base64 and circulate only in the fanmade community). Make one with "Save as .DY" in Dynamaker / dynamaker-modified (`saveAsDynaMaker()`, `saveAsMinimal()` in `app/src/Script/function.js`) or DyNode.

## Sources

- <https://cdn.jsdelivr.net/gh/jmakxd/dynamaker-modified@master/app/src/Script/loadingScene.js>
- <https://dyn.iorinn.moe/en/guide/import.html>
- <https://github.com/TLChicken/dynamaker-guide/blob/master/Contents/Old%20Guide%20v1.0.txt>
