# Arcaea

Arcaea (lowiro, 2017) is a 3D touch rhythm game: a bottom plane with four lanes (floor taps and holds) and a vertical sky plane where **arcs** (free 3D Bezier-like ribbons with x/y position) and **arc taps** travel toward the judgement line. Charts are plain-text `.aff` files; the community editor ecosystem (Arcade/ArcadeZero, ArcCreate) adds project formats and scripted scene control.

Category: **others**. The four floor lanes alone would fit a column model, but arcs are continuous 2D curves in the sky plane (x, y) with easing, plus camera and scene-control events, so the chart as a whole is not column-based.

Formats documented:

- [`aff/`](aff/README.md) - the `.aff` chart file (complete from parser sources).
- [`arcpkg/`](arcpkg/README.md) - ArcCreate `.arcpkg` / project packages (stub).
- [`songlist/`](songlist/README.md) - the `songlist` / `packlist` JSON metadata that lists songs of the game (stub).

Links: <https://github.com/yojohanshinwataikei/vscode-arcaea-file-format>, <https://github.com/Arcthesia/ArcCreate>, <https://github.com/Tempestissiman/ArcadeScenecontrol>, <https://github.com/freeze-dolphin/EtoileResurrection>.
