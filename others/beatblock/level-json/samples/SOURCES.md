# Samples: Beatblock level (`level.json` and chart JSON)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-level.json` | hand-written, key names and layout copied from the real packages listed in the manifest (Tetris C type.zip etc.) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Observed level.json shape: `properties` (speed, offset, formatversion 13, loadBeat) + `events` (a `play` event with file/angle/bpm/volume/time, a `showResults` event); no audio file shipped |
| `synthetic-chart-Synthetic.json` | hand-written, key names and layout copied from the real packages listed in the manifest (Tetris C type.zip etc.) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. Chart file = JSON array of note objects, file name `chart-<variant name>.json`; uses types block, inverse, side, hold (angle2 + duration), mine, extraTap with fractional beat time 9.5 |
| `synthetic-manifest.json` | hand-written, key names and layout copied from the real packages listed in the manifest (Tetris C type.zip etc.) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. manifest.json shape: `metadata`, `properties.formatversion`, `variants[]` (display, difficulty, charter, name), `defaultVariant` |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `Tetris_C_type.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/Tetris%20C%20type.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v13, 286 notes (block, inverse), manifest.json variants, backup/ folder; 575 KB (574838 bytes) |
| `Otonoke_ITA_from_DANDADAN_-_Fakkinenza.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/Otonoke%20ITA%20%28from%20DANDADAN%29%20-%20Fakkinenza.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v14, chart-Hard.json with hold/mineHold/mine/side/inverse/extraTap, `paddles` events; 784 KB (783817 bytes) |
| `gravityFallsTheme.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/gravityFallsTheme.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v13, heavy decorations (28 deco), 66 setColor, bookmark/hom/noise/outline events, portalAnim.json spritesheet descriptor; 1 MB (1071014 bytes) |
| `Levan_Polka.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/Levan%20Polka.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v13, 759 notes (block/inverse/extraTap), chart.json + level.json (metadata inside level.json); 2 MB (2018504 bytes) |
| `nyanyanyanyanyanyanya.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/nyanyanyanyanyanyanya.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v14, 385 `tag` events + tags/ folder JSON, 153 ease events, setBoolean; tag JSON files have trailing commas; 1.9 MB (1943209 bytes) |
| `world.executeme.zip` | https://raw.githubusercontent.com/ItsBritex/beatblock-levels/e29250abd56c3b83eff0e1e219ef25d90ac00662/levels/downloads/world.execute%28me%29%3B.zip | No licence in the repo; community Beatblock level zips incl. song audio + images, not committed | format v12, 873 notes, 165 deco events, tags/, lyrics.json; 3.2 MB (3218101 bytes) |
