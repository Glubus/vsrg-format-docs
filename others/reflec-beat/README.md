# REFLEC BEAT

Konami arcade game (2010-2018, versions Reflec Beat, Limelight, Colette, groovin'!!, VOLZZA, VOLZZA 2; also *Reflec Beat plus* for iOS/Android): a two-player touch table; notes ("balls") travel across the field and are hit/reflected by touching the matching spot, with long notes and special-note mechanics.

**Category: others** — free two-dimensional note positions and reflecting ball trajectories; not a lane game.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [rb/](rb/README.md) | `.rb` zip package of Reflec Beat plus (iOS), containing encrypted `note_*` charts | stub; shares the container with jubeat plus `.jbt` and pop'n rhythmin `.orb` |

The **arcade chart format is not publicly documented** in sources I could open. `bemaniutils` (DragonMinded) supports Reflec Beat versions 1–6 (Limelight/Colette/groovin'!!/VOLZZA/VOLZZA 2) for services/music import from the game DLL, not chart parsing. A fan Unity simulator (`neoncircuit/reflec-beat-simulator`) uses its own JSON `*.rbchart.json` — a simulator-specific format, not official.

## Links

- SaxxonPike rhythm-game-formats (iOS packages): <https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/jbt-rb-orb.md>
- bemaniutils: <https://github.com/DragonMinded/bemaniutils>
- Reflec Beat Simulator (`.rbchart.json`): <https://github.com/neoncircuit/reflec-beat-simulator>
- Expert Xylophone (reconstructed source of REFLEC BEAT plus 4.5.8): <https://github.com/Tatsh/expert-xylophone>
