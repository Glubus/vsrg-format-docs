# Music Times chart (`.xml`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: xml (reportedly encrypted in newer versions)

## Overview
Chart format of 乐动时代 (Music Times). Identified by the original README (`.xml`: **Music Times** chart) and rmstZ ("xml (乐动时代谱面)", http://www.ydsd.com/, read/write). A TapTap review snippet says that after the game upgrade "the official side encrypted the charts to guarantee chart quality" (search snippet, not verified). No schema or parser source was found: the structure is Unknown.

## Container & encoding
XML for plain charts (per rmstZ); encrypted variant: algorithm Unknown.

## Structure / metadata
Unknown.

## Timing model / Notes / Audio & images
Unknown.

## Versions & variants
Plain vs encrypted.

## Quirks & pitfalls
Unknown.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (closed source): https://lrfasd.github.io/rmstZ/

## Getting samples

- Committed: none. No public sample or parser source exists (rmstZ is closed source).
- How to get one: install 乐动时代 (Music Times, http://www.ydsd.com/) from an older client (later clients reportedly encrypt charts, see Overview), locate its downloaded `.xml` chart and open it in rmstZ (https://lrfasd.github.io/rmstZ/) which lists it as readable and writable. [inference] on exact paths.

## Sources
- https://lrfasd.github.io/rmstZ/
- http://www.redatoms.com/games/ydsd/
- https://www.taptap.cn/app/7083/review?os=android (search snippet)
