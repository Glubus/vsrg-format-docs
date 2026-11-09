# NOSTALGIA (ノスタルジア)

Konami arcade "piano" rhythm game (2017-; *NOSTALGIA*, *FORTE*, *Op.2*, *Op.3*) played on a keyboard-like touch device. Notes fall onto piano keys whose width and position vary; there are taps, long (hold) notes and "trill" notes, and the playfield shifts as the music moves between registers.

Category: others. Continuous horizontal key positions on a keyboard with moving ranges, not a fixed-column game.

## Formats

No chart format folder. No public specification, reverse-engineered parser or sample of the arcade chart files was found. The only open-source project found, `sleepily/nostalgia`, is a cross-platform clone that consumes osu! beatmaps (osu! parser for song info and hit objects, slider-tick based hold notes); it does not document NOSTALGIA's own format.

Untested leads: Konami's chart data in the arcade data tree; BEMANI utility projects such as `bemaniutils` (services emulation only).

## Getting samples

No sample and no format folder exist. `sleepily/nostalgia` (tree checked at `84351aa1`) holds no `.osu` or other chart file. Real data would need commercial arcade game data and reverse-engineering; no source read says where the charts are stored [inference]. If a format gets documented, add `nostalgia/<format>/` with a fiche and samples/manifest.

## Links

- RemyWiki: <https://remywiki.com/What_is_NOSTALGIA>
- sleepily/nostalgia clone: <https://github.com/sleepily/nostalgia>
