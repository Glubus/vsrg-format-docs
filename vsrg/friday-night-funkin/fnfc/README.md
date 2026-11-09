# FNF chart package (`.fnfc`)
Kind: package

Doc status: complete · ROX: decode only · Category: vsrg · Encoding: archive (ZIP)

## Overview

`.fnfc` is the chart package saved by the Chart Editor of Friday Night Funkin' 0.3+ (V-Slice). It bundles the metadata ([../vslice-metadata-json/README.md](../vslice-metadata-json/README.md)), the chart data ([../vslice-chart-json/README.md](../vslice-chart-json/README.md)) and the audio of a song for easy sharing and collaboration. The official spec is `docs/FNFC-SPEC.md` of FunkinCrew/Funkin ("Updated 2024-04-29": manifest `1.0.0`, metadata `2.2.2`, chart data `2.0.0`). The game itself does not store songs as `.fnfc`: it stores the `-metadata.json`, `-chart.json` and `.ogg` files separately; `.fnfc` is for the editor and for distribution.

## Contents

- A V-Slice song: metadata, chart data and audio, as in the FNFC spec.
- Chart format inside: [V-Slice chart JSON](../vslice-chart-json/README.md); metadata: [V-Slice metadata JSON](../vslice-metadata-json/README.md).

## Container & encoding

"FNFC files are standard ZIP files" (spec); renaming `mychart.fnfc` to `mychart.zip` lets any archive tool open it (modding docs: "an FNFC file is actually secretly a ZIP file!"). Contents:

| File | Required | Meaning |
|---|---|---|
| `manifest.json` | yes | `{ "version": "1.0.0", "songId": "<songid>" }`: minimal info so the editor can find the other files by name |
| `Inst.ogg` | yes (a chart without instrumental is invalid) | default instrumental, OGG Vorbis |
| `Inst-<instid>.ogg` | optional | alternative instrumental (`playData.characters.instrumental`) |
| `Voices-<charid>.ogg` | optional | vocals of a character (player/opponent ids from the metadata) |
| `Voices-<charid>-<variation>.ogg` | optional | vocals for an alternate variation |
| `<songid>-metadata.json` | yes | default variation metadata |
| `<songid>-metadata-<variation>.json` | optional | alternate variation metadata |
| `<songid>-chart.json` | yes | default variation chart |
| `<songid>-chart-<variation>.json` | optional | alternate variation chart |

Each component JSON has its own semver `version`; changes with backwards compatibility bump `1.x.0`, breaking ones `x.0.0`.

## Structure / metadata

`manifest.json` keys: `version` (semver string for the manifest) and `songId`. Everything else is in the two JSON files. Concept of **variations**: groups of difficulties sharing gameplay data (events, characters, stage, music); difficulties start in the `default` variation; `Erect`/`Nightmare` live in the `erect` variation in the example of the spec; the editor learns the variations from `playData.songVariations` of the default metadata.

## Timing model

See the metadata (`timeChanges`) and chart (`t` times) docs.

## Notes

See the chart doc.

## Audio & images

OGG Vorbis only, in the ZIP root. Missing vocals files are ignored by the game; missing `Inst.ogg` is an error. Album art, icons, characters, stages are not in the package.

## Versions & variants

Manifest 1.0.0; metadata 2.2.x; chart 2.0.x. Also: `.fnfmod` mod packages ([../fnfmod/README.md](../fnfmod/README.md)) are a different, larger archive type.

## Quirks & pitfalls

- To use a chart in a mod, unzip it: `manifest.json` is dropped; metadata and chart go to `data/songs/<songid>/`, the `.ogg` files to `songs/<songid>/` (modding docs "Adding the Custom Song").
- File names follow the fixed patterns of the table above (`Inst.ogg`, `Voices-<charid>.ogg`, `<songid>-chart.json`), so keep the exact case; the `songId` of `manifest.json` is used to build the metadata/chart names.
- Variation files exist only if listed in `songVariations`.

## Example

Typical listing (from the official modding docs, "Creating a Chart"):

```
manifest.json
mychart-metadata.json
mychart-chart.json
Inst.ogg
Voices-bf.ogg
Voices-pico.ogg
```

## ROX support

Read, decode only: `rox::formats::fnf_vslice::FnfcPackage` (`open`, `song_id`, `entries`, `chart(variation)`, `metadata(variation)`, `read_entry`, `variations`) and `VSliceDecoder::{fnfc_variants, decode_fnfc_variant, decode_fnfc_with_report, decode_fnfc_with_audio_plan}`; `DetectedFormat::Fnfc` (`auto_decode*` take the default variation). The ZIP is read in memory (never extracted) with limits: 1024 entries, 2 GiB declared unpacked, 512 MiB per entry, 64 MiB per JSON entry (never trusting the declared size); an absolute entry name, one with `..`, a backslash or a repeated name refuses the package. Files are looked up in the root with the exact case from the manifest's `songId`. The audio plan's events are `SoundEvent::in_container` events on the package file name the caller gives, `index` = entry number in archive order; the vocals are searched as the game does (list, then the id shortened at `-`, then `Voices[-<variation>].ogg`); a missing `Inst.ogg` is an error for the plan.

## Parsers & tools

- FNF Chart Editor (in-game, Haxe): https://github.com/FunkinCrew/Funkin
- Moonchart `FNFVSlice` (Haxe) reads/writes the pair: https://github.com/MaybeMaru/moonchart
- Codename Engine's song editor imports V-Slice charts.

## Getting samples

- `.fnfc` is a ZIP container, so NO archive is committed here (owner rule: charts only). The chart members of real `.fnfc` exports are committed as `-chart.json` / `-metadata.json` in [../vslice-chart-json/samples/](../vslice-chart-json/samples/) and [../vslice-metadata-json/samples/](../vslice-metadata-json/samples/), one subfolder per set, with the download URL of each package in their SOURCES.md; see [samples/SOURCES.md](samples/SOURCES.md).
- Real packages come from GameBanana (e.g. mod 631833 `17bucksfull`, 619290 `Can't Hold Us`, 651119 Lit Up erect, 520484 four charts; search https://gamebanana.com/apiv11/Util/Search/Results?_sSearchString=fnfc&_idGameRow=8694) and from https://github.com/MeguminBOT/fnf-chart-info-tool (`test_charts/vslice/thorns-erect.fnfc`). Each real package contains `manifest.json` (`{"version": "1.0.0", "songId": ...}`), `<songid>-metadata.json`, `<songid>-chart.json`, `Inst.ogg` [observed].
- Make your own: in the in-game Chart Editor (V-Slice) save, or ZIP the files above yourself per [docs/FNFC-SPEC.md](https://github.com/FunkinCrew/Funkin/blob/main/docs/FNFC-SPEC.md) and rename to `.fnfc`.

## Sources

- https://github.com/FunkinCrew/Funkin/blob/main/docs/FNFC-SPEC.md
- https://funkincrew.github.io/funkin-modding-docs/02-custom-songs-and-custom-levels/02-01-creating-a-chart.html and `02-02-adding-the-custom-song.html`
