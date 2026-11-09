# ONGEKI (オンゲキ)

SEGA arcade rhythm game (2018-): a lane game with a bullet-hell layer. The avatar moves horizontally (lever) among three lanes (red / green / blue) while hitting Tap/Hold/Flick notes with side buttons, collecting Bells and dodging bullets; side walls ("wall taps/holds") use the wall buttons. Charts also hold enemy spawns, beams, lane/wall shapes and per-note speed groups.

Category: others. Notes sit at free horizontal positions ("xUnit", −/+ space, 4096 units wide), lanes bend and move over time, bullets aim at the player, walls and beams are separate objects. There is no fixed column count.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [ogkr/](ogkr/README.md) | `.ogkr` text chart | reverse-engineered by MikiraSora (OngekiFumianDescription) and implemented by `fairywreath/ogkr` (Rust) and OngekiFumenEditor (C#) |

## Links

- OngekiFumianDescription: <https://github.com/MikiraSora/OngekiFumianDescription>
- OngekiFumenEditor: <https://github.com/MikiraSora/OngekiFumenEditor>
- fairywreath/ogkr (Rust parser): <https://github.com/fairywreath/ogkr>
