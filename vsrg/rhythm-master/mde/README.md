# Rhythm Master star motion chart (`.mde`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: Unknown

## Overview
Chart of the star motion mode (星动模式) of Rhythm Master (players hit/slide notes that fall in lanes, with a dancing avatar). Evidence: the original README lists `.mde` and rmstZ's feature list names `mde` ("节奏大师谱面，星动模式") as a readable and writable format, next to `xml` ("节奏大师谱面，星动模式") and `imd` (classic). The client also has a star-mode song list editable in RMEssentials ("客户端星动模式bin格式歌曲单编辑", removed from later versions since "the new Rhythm Master removed the star motion mode"). No parser source, layout description or sample file was found: the structure is Unknown. The QQ Dance mobile XML (see [qq-dance](../../qq-dance/xml/README.md)) is the likely same engine family (Tencent; star mode, lane-based) [inference].

## Container & encoding
Unknown (rmstZ lists it as a chart file read and write). Not text-verified.

## Structure / metadata
Unknown.

## Timing model / Notes / Audio & images
Unknown.

## Versions & variants
Unknown. Rhythm Master star mode also exists as `xml` (rmstZ), no spec found.

## Quirks & pitfalls
Unknown.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (closed source, https://lrfasd.github.io/rmstZ/) lists it; RMEssentials only handles the song list.

## Getting samples

- Committed / manifest: none. The only `.mde` found is RMEssentials' `src/librmessentials/test/tst_rmeutils/existnotes/existnotes_Papa_Normal.mde`, which is a 0-byte placeholder (checked at commit `8945cab60ec58aec2f3bf08966e7c75f2f0d1bca`).
- How to get one: the star motion mode (星动模式) of Rhythm Master; RMEssentials treats `.mde` as a chart file name pattern (`existnotes_<song>_<Difficulty>.mde`, `existnotes` test); fan charts of that mode circulate on https://www.dreamimd.com ([inference]); rmstZ reads and writes it.

## Sources
- https://lrfasd.github.io/rmstZ/
- https://www.dreamimd.com/c/tools (RMEssentials description)
- https://raw.githubusercontent.com/Fsu0413/RMEssentials/master/WHATSNEW
