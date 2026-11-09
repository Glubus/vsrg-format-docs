# Sonolus

Sonolus is a rhythm-game platform/app whose games are **engines** (user-written scripts compiled to engine data) driven by **levels** (cover, BGM, optional preview and a LevelData file). It is the common target of many fan recreations of mobile rhythm games (Project SEKAI, Deemo, Phigros, Cytus, Arcaea-likes...). Sonolus itself defines no gameplay: the same LevelData container can hold lane charts, free-position charts, rotating lines, etc.

Category: **others**: game-agnostic entity container (entities of engine-defined archetypes with named numeric data); only a profile of a given engine may be column-like.

Formats documented:

- [`level-data/`](level-data/README.md) - LevelData (gzip JSON), the chart payload of a Sonolus level.
- [`scp/`](scp/README.md) - Sonolus Collection Package (`.scp`) (stub).

Links: <https://wiki.sonolus.com/>, <https://github.com/Sonolus/sonolus-wiki>, <https://github.com/NonSpicyBurrito/sonolus-wiki>.
