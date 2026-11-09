# Lanotalium / Layesta fan chart (`unknown`)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: unknown

## Overview

Lanotalium is a Lanota fan chart maker (Unity 2017.4 / Visual Studio 2017, "no license"); Layesta is a companion fan player. Release notes mention "Support converting from Arcaea levels (*.aff)" (v2.1.2 delta) and "splitter of Angleline" changes, which implies angle lines and a Copy format. The file extension is unknown: the repository tree listing returned HTTP 403 and no external format document exists. Official Lanota charts sit in the game's Unity bundles in an undocumented layout.

## Container & encoding

Unknown.

## Structure / metadata

[observed in the source of Lanotalium, `Assets/Scripts/Schwarzer/Chart/Lanota/LanotaChartHandler.cs`, class `LnmReadJson`; no sample file seen] The chart is JSON with root keys `events` (array), `eos` (float, song length), `bpm` (array) and `scroll` (array of `{speed, timing}`). An `events` entry has `Id`, `Type`, `Timing`, `Duration`, `ctp`, `ctp1`, `ctp2`, `cfmi`, `cflg`, `Degree`, `Size`, `Critical`, `Combination`, `Bpm` and `joints` (`{j_count, j: [{idx, d_deg, d_time, d_e}]}`). The reader dispatches on `Type`: 0, 2, 3, 4 tap-like notes; 5 hold note with joints; 8 and 11 camera XZ events; 10 camera Y events; 12 default camera values (`ctp`, `ctp1`, `ctp2`, `Degree`); 13 camera rotation events. A missing `bpm` defaults the tempo to 100; a missing `scroll` defaults the speed to 1. Other `Type` meanings and the units of `Timing`/`Duration` are unknown. Per the release notes the tool has Ring/Angleline concepts and tap/hold/slide notes.

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

Committed: none. The Lanotalium repository has no chart files and says "No License - Commercial use, Distribution is not permitted". Its ChartZone web API (`lanotaliumapi.schwarzer.wang`) returned nothing, and no other public chart collection exists.

To get one: install Lanotalium (<https://github.com/cnSchwarzer/Lanotalium>) and create a chart, or take fan charts from the Lanotalium/Layesta Discord servers linked in its README. Official charts are inside the game's Unity bundles.

## Sources

- <https://github.com/reitowo/Lanotalium> (README fetched via CDN)
- Release notes quoted in search results: <https://github.com/cnSchwarzer/Lanotalium/releases>
