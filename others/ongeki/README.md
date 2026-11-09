# ONGEKI (オンゲキ)

SEGA arcade rhythm game (2018-): a vertical-scrolling lane game combined with a **bullet-hell** layer. The player's avatar moves horizontally (lever) among three lanes (red / green / blue) while hitting Tap/Hold/Flick notes with side buttons, collecting Bells and dodging bullets; side walls ("wall taps/holds") are hit with the wall buttons. A chart also contains enemy spawns, beams, lane/wall shapes and per-note speed groups.

**Category: others** — notes are placed at free horizontal positions ("xUnit" in a −/+ coordinate space, 4096 units wide), lanes bend and move over time, bullets aim at the player position, walls and beams are separate objects. It is not a fixed N-column game.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [ogkr/](ogkr/README.md) | `.ogkr` text chart | reverse-engineered by MikiraSora (OngekiFumianDescription) and implemented by `fairywreath/ogkr` (Rust) and OngekiFumenEditor (C#) |

## Links

- OngekiFumianDescription: <https://github.com/MikiraSora/OngekiFumianDescription>
- OngekiFumenEditor: <https://github.com/MikiraSora/OngekiFumenEditor>
- fairywreath/ogkr (Rust parser): <https://github.com/fairywreath/ogkr>
