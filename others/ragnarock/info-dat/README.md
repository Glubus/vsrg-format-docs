# Ragnarock map (`info.dat` + difficulty `.dat`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: json

## Overview
Ragnarock custom songs use a folder/zip of JSON files modelled on the Beat Saber v2 map format (`info.dat`, difficulty `.dat`, audio, cover). The only primary statement found: "Ragnarock's beatmap format is derived from Beat Saber's ... there are major differences between Beat Saber and Ragnarock's song formats. Some aspects of Beat Saber's song format don't translate well to Ragnarock's, and others are unused or missing entirely" (Edda site). The exact field set, the drum-lane mapping and which Beat Saber fields are used are **Unknown** here: the Edda source was not opened.

## Container & encoding
JSON text; distributed as a ZIP of the map folder via RagnaCustoms (inferred from the site's "download maps" flow). See [Beat Saber info-dat](../../beat-saber/info-dat/README.md) and [dat](../../beat-saber/dat/README.md) for the base schema.

## Structure / metadata / Timing model / Notes
Unknown beyond "derived from Beat Saber"; timing is presumably in beats like Beat Saber v2 [inference].

## Audio & images
Unknown (presumably referenced by filename from `info.dat` as in Beat Saber [inference]).

## Versions & variants
Unknown.

## Quirks & pitfalls
Do not assume Beat Saber field semantics (hand colors, cut directions) apply.

## Example
Not available (no real sample was read).

## ROX support
Not read by ROX.

## Parsers & tools
- Edda (C#, WPF): https://github.com/PKBeam/Edda
- MediocreMapAssistant2: https://git.bsmg.dev/Top_Cat/MediocreMapAssistant2
- taiko midi to json for Ragnarock: https://github.com/jjcosmos/taiko (seen in search only)

## Sources
- https://pkbeam.github.io/Edda/
- https://ragnacustoms.com/getting-started (search snippet)
