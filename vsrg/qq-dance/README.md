# QQ Dance mobile (QQ炫舞手游, "QQ Hyun Dance")

Tencent's mobile dance rhythm game (X5M, launched 2018; PC predecessor QQ Dance/QQ Audition). Modes: star motion (星动: notes fall in 4/5 lanes, tap/slide/hold, with a dancing avatar), traditional/classic (传统), quarter-moon/crescent (弦月: notes on a ring, angle-based), marble/pinball (弹珠: notes land on areas), bubble (泡泡: notes at free screen positions). Charts are XML (compressed as `xml.bytes` in the 2019 apk, later downloaded, no longer extractable per the QQX5Tools author). Star and traditional modes are column based (vsrg); crescent, pinball and bubble are not (others): they share one XML schema family, so one folder is kept here, category **vsrg** for the format, with the free-position modes flagged below.

| Folder | File | Role |
|---|---|---|
| [xml/](xml/README.md) | `.xml` (`.xml.bytes`) | chart of one mode (root `<Level>`) |
