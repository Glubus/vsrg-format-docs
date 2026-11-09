# maimai / maimai DX

SEGA arcade rhythm game (2012-). The cabinet has a circular screen with a ring of **8 buttons** (numbered clockwise from the 1 o'clock position, 1–8) and, since maimai DX (2019), a touch screen divided into **34 sensor zones** (groups A–E, 8 zones each for A/B/D/E, 2 for C). Notes start at the centre and travel outward to a button on the judgement ring (taps, holds, breaks, EX notes); "star" notes spawn **slides** that must be traced across the sensors along a shape (straight, arc along the ring, V, p/q, zigzag, fan…); DX adds touch notes and touch holds on sensors.

**Category: others** — radial (centre-to-ring) movement, 8 ring positions + 34 touch zones, slide shapes; there are no vertical lanes. A ROX column model could only represent the 8 buttons as 8 columns and would lose slides and touch.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [ma2/](ma2/README.md) | `.ma2` official text chart (maimai DX, tab-separated, tick based; versions 1.03/1.04+) | reverse-engineered |
| [simai/](simai/README.md) | `maidata.txt` / "simai language" (`&inote_N=` blocks) | community format of Celeca's simai (2013) and MajdataEdit/MajdataPlay and others |
| [sdt/](sdt/README.md) | `.srt` / `.szt` / `.sct` / `.sdt` (maimai classic, 4 successive text formats; encrypted `.srb/.szb/.scb/.sdb` variants) | blog reverse-engineering by donmai |

Tools: MaiConverter (Python, ma2/sdt/simai), MaiLib + MaichartConverter (C#, ma2/simai), maidata-parser and ma2-parser (lcebot), `maidata-rs` (Rust, simai), MajdataEdit/MajdataPlay (simai editor/player), MaiChartManager.

## Links

- simai wiki: <https://w.atwiki.jp/simai/>
- ma2Research: <https://github.com/Littlebluemoon/ma2Research>
