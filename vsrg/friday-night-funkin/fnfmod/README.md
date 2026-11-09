# FNF mod package (`.fnfmod`)
Kind: package

Doc status: stub · ROX: no · Category: vsrg (it contains FNF song/chart data; it is a mod container, not a chart format) · Encoding: archive (ZIP)

## Overview

`.fnfmod` is the mod archive extension introduced with the Funkin' Mod Menu of the official game (Funkin' Crew blog, "WEEK OF 2026/08/03 - Introducing: The Mod Menu"). It is a ZIP file: the blog says the game "accepts zip files with the new .fnfmod extension" dropped over the game window, next to plain mod folders. No `.fnfm` extension was found; `.fnfmod` is the only match. Not a chart format: it carries whole mods (songs, characters, stages...), and therefore the `-chart.json`/`-metadata.json`/`.ogg` song files of [vslice-chart-json](../vslice-chart-json/README.md) and [vslice-metadata-json](../vslice-metadata-json/README.md).

## Contents

- Whole mods (songs, characters, stages), not only charts.
- Song files inside: [V-Slice chart JSON](../vslice-chart-json/README.md) and [V-Slice metadata JSON](../vslice-metadata-json/README.md).

## Container & encoding

ZIP (per the blog post). The inner layout is a mod folder as documented by the modding docs: `data/songs/<songid>/<songid>-metadata.json`, `<songid>-chart.json`, `songs/<songid>/Inst.ogg`, `Voices-*.ogg`, and `_polymod_meta.json` (the Polymod mod descriptor) at the mod root ("Adding the Custom Song"). Mods may declare dependencies and optional dependencies (blog: dependencies ordered under the mod that needs them). The exact manifest schema of `.fnfmod` is Unknown here.

## Structure / metadata

Unknown beyond the above (`_polymod_meta.json` is the descriptor of Polymod mods; the `.fnfmod`-specific schema was not found).

## Timing model

Not applicable.

## Notes

Not applicable (see the V-Slice chart doc).

## Audio & images

OGG files inside the mod folder (see the `.fnfc` doc).

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown. Dependencies between mods affect load order (blog).

## Example

The mod layout shown by the modding docs (not specific to `.fnfmod`):

```
mods/myMod/
  data/songs/mychart/mychart-metadata.json
  data/songs/mychart/mychart-chart.json
  songs/mychart/Inst.ogg
  songs/mychart/Voices-bf.ogg
  _polymod_meta.json
```

## ROX support

Not read.

## Parsers & tools

The official game (Mod Menu); Polymod: https://github.com/larsiusprime/polymod [Polymod's role is stated in the modding docs path name `_polymod_meta.json`; the link itself was not opened].

## Sources

- https://funkin.me/blog/2026-08-03/ (Mod Menu post)
- https://funkincrew.github.io/funkin-modding-docs/02-custom-songs-and-custom-levels/02-02-adding-the-custom-song.html
