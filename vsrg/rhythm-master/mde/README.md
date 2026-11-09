# Rhythm Master star motion chart (`.mde`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown

## Overview

Chart of the star motion mode (星动模式) of Rhythm Master. rmstZ lists `mde` ("节奏大师谱面，星动模式") as readable and writable, next to `xml` (same description) and `imd` (classic). RMEssentials edits the star-mode song list ("客户端星动模式bin格式歌曲单编辑", removed later because "the new Rhythm Master removed the star motion mode"). No parser, layout description or sample was found: Unknown. The QQ Dance mobile XML ([qq-dance](../../qq-dance/xml/README.md)) is likely the same engine family (Tencent; star mode, lane-based) [inference].

## Container & encoding

Unknown (rmstZ reads and writes it as a chart file).

## Structure / metadata
Unknown.

## Timing model / Notes / Audio & images
Unknown.

## Versions & variants
Unknown. Rhythm Master star mode also exists as `xml` (rmstZ), no spec found.

## Quirks & pitfalls
Unknown.

## Example

Unknown.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (closed source, https://lrfasd.github.io/rmstZ/) lists it; RMEssentials only handles the song list.

## Getting samples

Committed: none. The only `.mde` found is RMEssentials' `src/librmessentials/test/tst_rmeutils/existnotes/existnotes_Papa_Normal.mde`, a 0-byte placeholder (commit `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca`). RMEssentials treats `.mde` as a chart name pattern (`existnotes_<song>_<Difficulty>.mde`); rmstZ reads and writes it; fan charts may circulate on https://www.dreamimd.com [inference].

## Sources
- https://lrfasd.github.io/rmstZ/
- https://www.dreamimd.com/c/tools (RMEssentials description)
- https://raw.githubusercontent.com/Fsu0413/RMEssentials/master/WHATSNEW
