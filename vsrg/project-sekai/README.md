# Project SEKAI: COLORFUL STAGE! feat. Hatsune Miku (and SUS / USC charts)

Project SEKAI (Sega / Colorful Palette, 2020) is a touch rhythm game with 12 fixed lanes. Notes fall vertically toward a bottom judgement line: taps, flicks, critical notes, "trace" notes and long slides that move across lanes on Bezier/eased paths. Its chart language descends from SUS (Sliding Universal Score), a text format created for Seaurchin (a Chunithm-like simulator) and also used for Chunithm fan charts. The Sonolus community converts SUS to USC (Universal Sekai Chart), a JSON score model consumed by the Sonolus PJSekai engines.

Category: vsrg. Lanes use an integer lane/width grid and notes fall toward a fixed line (slides move across lanes, which a column model only approximates). This is a judgement call: the layout is closer to BanG Dream / Chunithm than to free-position games. Sonolus' generic LevelData container is documented under `others/sonolus/`.

Formats documented:

- [`sus/`](sus/README.md): Sliding Universal Score text charts (PJSK dialect).
- [`usc/`](usc/README.md): Universal Sekai Chart JSON (Sonolus PJSekai engine input).
- [`pjsk/`](pjsk/README.md): score maker JSON.
- [`ccmmws/`](ccmmws/README.md): MMWS binary layout and the CCMMWS/UCMMWS fork variants.
- [`holodori-sus/`](holodori-sus/README.md): hololive Dream SUS dialect.

Links: <https://www.npmjs.com/package/sus-io>, <https://github.com/NonSpicyBurrito/sonolus-pjsekai-engine>, <https://github.com/UntitledCharts/rg_converters>.
