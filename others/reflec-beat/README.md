# REFLEC BEAT

Konami arcade game (2010-2018: Reflec Beat, Limelight, Colette, groovin'!!, VOLZZA, VOLZZA 2; also Reflec Beat plus for iOS/Android): a two-player touch table where balls cross the field and are reflected by touching the matching spot.

Category: others. Notes have free 2D positions and reflecting trajectories, no lanes.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [rb/](rb/README.md) | `.rb` zip package of Reflec Beat plus (iOS), containing encrypted `note_*` charts | stub; shares the container with jubeat plus `.jbt` and pop'n rhythmin `.orb` |

The arcade chart format is not publicly documented. `bemaniutils` (DragonMinded) supports Reflec Beat versions 1-6 (Limelight/Colette/groovin'!!/VOLZZA/VOLZZA 2) for services and music import from the game DLL, not chart parsing. A fan Unity simulator (`neoncircuit/reflec-beat-simulator`) uses its own JSON `*.rbchart.json`, not an official format.

## Links

- SaxxonPike rhythm-game-formats (iOS packages): <https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/jbt-rb-orb.md>
- bemaniutils: <https://github.com/DragonMinded/bemaniutils>
- Reflec Beat Simulator (`.rbchart.json`): <https://github.com/neoncircuit/reflec-beat-simulator>
- Expert Xylophone (reconstructed source of REFLEC BEAT plus 4.5.8): <https://github.com/Tatsh/expert-xylophone>
