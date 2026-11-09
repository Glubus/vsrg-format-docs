# Music Master chart (`.xml`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: xml

## Overview
Chart format of 乐动达人 (Music Master, RedAtoms). Identified by the original README (`.xml`: **Music Master** chart) and by rmstZ's feature list ("xml (乐动达人谱面)", http://yd2012.redatoms.com/, read and write); a TapTap player review (search snippet) says the format is "simple and clear", so self-made charts existed from the start. No schema, sample or parser source was found: the element/attribute names are Unknown.

## Container & encoding
XML text (per rmstZ). Not verified.

## Structure / metadata
Unknown.

## Timing model / Notes / Audio & images
Unknown (lane-based vertical-scroll game; number of lanes not verified).

## Versions & variants
Successor Music Times uses an encrypted chart variant after an update (see [music-times](../../music-times/xml/README.md)).

## Quirks & pitfalls
Unknown.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
rmstZ (closed source): https://lrfasd.github.io/rmstZ/ ; no open-source parser found.

## Getting samples

- Committed / manifest: none. No public repository with a downloadable chart under a redistributable licence was found.
- Leads found: the 2013 iOS client of 乐动达人 keeps charts as `config.xml` / `config4.xml` (3-key / 4-key) in each song pack `1200XX.zip` of the IPA, with `type` cells of the form `N`, `N$N`, `N_N` (hold, N ms), `N_N$N`...; the browser port https://github.com/chuxue2777/yuedongdr2012web (README.dev.md, no licence) documents this and embeds the data in `js/songs.js` (not XML, ripped from the game). [inference] Relation to the `.xml` of rmstZ not verified.
- How to get one: obtain the iOS app package of 乐动达人 (RedAtoms), unzip the song pack and read `config.xml`; or open an existing chart with rmstZ (https://lrfasd.github.io/rmstZ/, closed-source converter) which reads/writes it.

## Sources
- https://lrfasd.github.io/rmstZ/
- http://www.redatoms.com/games/yddr/
- https://www.taptap.cn/app/7083/review?os=android (search snippet)
