# NOSTALGIA (ノスタルジア)

Konami arcade "piano" rhythm game (2017-; *NOSTALGIA*, *FORTE*, *Op.2*, *Op.3*), played on a keyboard-like touch device: notes fall onto piano keys of a keyboard whose width/position varies; there are taps, long (hold) notes, "trill" notes, and the playfield shifts as the music moves between registers.

**Category: others** — continuous horizontal key positions on a keyboard with moving ranges (not a fixed-column game).

## Formats

**No chart format folder.** No public specification, reverse-engineered parser or sample of the arcade chart files was found. The only open-source project found, `sleepily/nostalgia`, is a cross-platform *clone* that **consumes osu! beatmaps** (it implements an osu! beatmap parser for song info and hit objects, with slider-tick based hold notes and long notes in progress) — it does not document NOSTALGIA's own format. A format folder would therefore have to be invented, which this reference does not do.

Possible future leads (not opened): Konami's chart data in the arcade data tree, BEMANI utility projects such as `bemaniutils` (services emulation only).

## Getting samples

No sample is committed and no format folder exists: no public specification, parser or chart file of the arcade game was found. The only code found, `sleepily/nostalgia` (tree checked at `84351aa1`), is a clone whose README says it parses osu! beatmaps; its tree holds no `.osu` or other chart file, so it gives no NOSTALGIA data. Obtaining real data would require arcade game data (commercial) and reverse-engineering; no source read says where the charts are stored [inference]. If a format is documented, add `nostalgia/<format>/` with a fiche and samples/manifest.

## Links

- RemyWiki: <https://remywiki.com/What_is_NOSTALGIA>
- sleepily/nostalgia clone: <https://github.com/sleepily/nostalgia>
