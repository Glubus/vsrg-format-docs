# Lanotalium / Layesta fan chart (`unknown`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: unknown

## Overview

Lanotalium is a Lanota "Visual Fanmade Chart Maker" (Unity 2017.4 / Visual Studio 2017, "no license"), and Layesta is a companion fan player. Releases note "Support converting from Arcaea levels (*.aff)" (v2.1.2 delta) and the "splitter of Angleline" changes, which implies angle lines and a Copy format. The chart serialisation (extension, structure) could not be retrieved: the repository tree listing was blocked (HTTP 403 from the CDN used) and no external format document was found. Official Lanota charts are inside the game's Unity bundles in an undocumented layout.

## Container & encoding

Unknown.

## Structure / metadata

[observed in the source of Lanotalium, `Assets/Scripts/Schwarzer/Chart/Lanota/LanotaChartHandler.cs`, class `LnmReadJson`; no sample file seen] The chart text is JSON with the root keys `events` (array), `eos` (float, song length), `bpm` (array) and `scroll` (array of `{speed, timing}`). An `events` entry has `Id`, `Type`, `Timing`, `Duration`, `ctp`, `ctp1`, `ctp2`, `cfmi`, `cflg`, `Degree`, `Size`, `Critical`, `Combination`, `Bpm` and `joints` (`{j_count, j: [{idx, d_deg, d_time, d_e}]}`). The reader dispatches on `Type`: 0, 2, 3, 4 tap-like notes; 5 hold note with joints; 8 and 11 camera XZ events; 10 camera Y events; 12 default camera values (`ctp`, `ctp1`, `ctp2`, `Degree`); 13 camera rotation events. If `bpm` is missing the tempo defaults to 100, and if `scroll` is missing the speed defaults to 1. The meaning of the individual `Type` numbers beyond this dispatch, the units of `Timing`/`Duration` and the file extension were not determined. The tool exposes Ring/Angleline concepts (per release notes), tap/hold/slide notes.

## Timing model

Unknown.

## Notes

Unknown (Lanota has tap, hold, slide and rotate notes in-game).

## Audio & images

Unknown.

## Versions & variants

Unknown.

## Quirks & pitfalls

Unknown.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

Lanotalium (C#): <https://github.com/cnSchwarzer/Lanotalium> (mirror <https://github.com/reitowo/Lanotalium>); Layesta (closed source).

## Getting samples

**Committed:** none. The Lanotalium repository has no chart files and says "No License - Commercial use, Distribution is not permitted"; its ChartZone web API (`lanotaliumapi.schwarzer.wang`) returned nothing when queried, and no other public chart collection was found. Source-derived structure (JSON keys `events`, `eos`, `bpm`, `scroll`) is in the fiche.

**How to get one yourself**: install Lanotalium (<https://github.com/cnSchwarzer/Lanotalium>) and create a chart, or obtain fan charts from the Lanotalium/Layesta Discord servers linked in its README; official charts are inside the game's Unity bundles.

## Sources

- <https://github.com/reitowo/Lanotalium> (README fetched via CDN)
- Release notes quoted in search results: <https://github.com/cnSchwarzer/Lanotalium/releases>
