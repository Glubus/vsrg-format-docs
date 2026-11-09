# Direct Move (simulator; charts are `.ksf`)
Kind: chart

Doc status: partial · ROX: decode only (reads, never writes) · Category: vsrg · Encoding: text (see KSF)

## Overview

"DirectMove" appears in the original README with an unknown extension, as "found on the StepMania Wikia page for StepMania AMX" (page not fetchable, HTTP 403). Direct Move is a Korean Pump-It-Up simulator by "Kiho"; it has **no format of its own**: it plays [`.ksf`](../../kick-it-up/ksf/README.md) files with an extended ("new") grammar. StepMania's KSF loader implements those extensions (`|T`, `|B`, `|E`, `|D`, `|M`/`|C`, `|S`, `|F`, `|X` control rows, `#BPM2/#BPM3/#BUNKI/#STARTTIME2/3` headers).

## Container & encoding

As KSF: CP949/EUC-KR text, CRLF.

## Structure / metadata

See the KSF page; the Direct Move additions are the pipe control rows inside `#STEP`.

## Timing model

See [KSF timing](../../kick-it-up/ksf/README.md#timing-model) (BUNKI centisecond BPM changes, per-row tick/BPM/delay/scroll controls).

## Notes

13-character rows; 5 panels per pad; `0 1 4` plus `M F L` in StepMania's loader.

## Audio & images

`song.mp3/ogg/wav`, intro clip, disc and back bitmaps (KSF layout).

## Versions & variants

Original KSF vs Direct Move "new grammar" ("the limit of 3 shifts disappeared"). Android port exists (net.zsoo.android.dmafree).

## Quirks & pitfalls

Negative BPM scrolls top-to-bottom in Direct Move (used for trick charts); KSF-compliance detection mixes badly with per-file grammars.

## Example

See the KSF sample.

## ROX support

Read by ROX as KSF: the `|T` `|B` `|E` `|D` rows of a `.ksf` are applied (see [`.ksf`](../../kick-it-up/ksf/README.md#rox-support)); the other `|` rows are ignored.

## Parsers & tools

StepMania `NotesLoaderKSF.cpp`; https://github.com/syspro86/directmove (downloads); STX2DM converter.

## Getting samples

No `.ksf` with DirectMove extensions was found in the open. [StepMania-AMX/directmove](https://github.com/StepMania-AMX/directmove) (fork of syspro86/directmove, commit `677c709a568a5e974721460f9e67758c0b9cb3ff`) holds the Visual Basic sources of KSFCreator/KSF Viewer and bitmaps, no chart. The plain KSF examples are in [`../../kick-it-up/ksf/samples`](../../kick-it-up/ksf/samples/SOURCES.md) (`sample.ksf`, plus the 7 real KIU charts). To get real DirectMove-variant files: install Direct Move (Korean simulator by "Kiho"; download links: see the AMX site https://dm.zsoo.net/pc/download referenced on http://stepmania.amx.io) and open its song folders (one `.ksf` per mode), or save a chart from KSFCreator (build from the repository). Look for `#BPM2`, `#BPM3`, `#BUNKI`, `#STARTTIME2` headers and `|T`, `|B` ... control rows per this page.

## Sources

- https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderKSF.cpp
- https://github.com/syspro86/directmove
- https://github.com/StepMania-AMX/STX2DM
- Upstream list, `README.md` at commit `503382a` (DirectMove line)
