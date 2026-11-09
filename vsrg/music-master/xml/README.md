# Music Master chart (`.xml`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: xml

## Overview

Chart format of 乐动达人 (Music Master, RedAtoms): rmstZ's feature list names "xml (乐动达人谱面)" (http://yd2012.redatoms.com/, read and write), and a TapTap review (search snippet) calls the format "simple and clear". No schema, sample or parser source was found; element/attribute names are Unknown.

## Container & encoding
XML text (per rmstZ). Not verified.

## Structure / metadata
Unknown.

## Timing model / Notes / Audio & images
Unknown (lane-based vertical-scroll game; number of lanes not verified).

## Versions & variants

The successor Music Times uses an encrypted chart variant after an update (see [music-times](../../music-times/xml/README.md)).

## Quirks & pitfalls
Unknown.

## Example

None.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (closed source): https://lrfasd.github.io/rmstZ/ ; no open-source parser found.

## Getting samples

- Committed: none; no redistributable chart found.
- Leads: the 2013 iOS client keeps charts as `config.xml` / `config4.xml` (3-key / 4-key) in each song pack `1200XX.zip` of the IPA, with `type` cells like `N`, `N$N`, `N_N` (hold, N ms), `N_N$N`...; the browser port https://github.com/chuxue2777/yuedongdr2012web (README.dev.md, no licence) documents this and embeds data in `js/songs.js` (not XML, ripped from the game). [inference] Relation to rmstZ's `.xml` not verified.
- To get one: unzip a song pack from the iOS package and read `config.xml`, or open a chart with rmstZ (https://lrfasd.github.io/rmstZ/, closed-source converter).

## Sources
- https://lrfasd.github.io/rmstZ/
- http://www.redatoms.com/games/yddr/
- https://www.taptap.cn/app/7083/review?os=android (search snippet)
