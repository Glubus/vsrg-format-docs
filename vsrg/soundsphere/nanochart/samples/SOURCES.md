# Samples: NanoChart
## Committed
| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rizu-test-v1-positive-delay.nanochart` | Bytes built exactly as in `chart/transform/NanoChart_test.lua` (`decode_version_one_positive_delays`) of https://github.com/semyon422/rizu at `cf4603379dcab949d3510b8c31d1d3e421df6ec0` (header `01` + 16 zero bytes + `04`, then `e9 10 00`) | semyon422 (rizu) | GPL-3.0 (repo `LICENSE`, read) | Version 1 header, positive delay object (9 s), a single release of input 1 at t=9 s; 21 bytes. |
| `synthetic-v2-roundtrip.nanochart` | Hand-built by BmsAux: encoder `NanoChart:encode` of rizu ported line by line to Python and checked against the four exact-byte `encodeNote` vectors of `NanoChart_test.lua`; note list = the one of `encode_decode_roundtrip` (hash ASCII `0123456789abcdef`, 4 inputs); decoded back with a port of `NanoChart:decode` and compared. | BmsAux (synthetic) | CC0 / public domain | Version 2, same-time objects, delay objects (+2, then +7x4+6 = 34 s), extended objects (input 255, with the 0-input time marker); 37 bytes. |
| `synthetic-v2-negative-delay.nanochart` | Same method as above (encoder port + decoder round trip verified), own note list (13 inputs, 9 events). | BmsAux (synthetic) | CC0 / public domain | Version 2 signed delay nibble (a note at 5.125 s after a note at 10.75 s, so a -8..7 negative delta), chords at one time, extended input 13 (`inputCount` 13); 40 bytes. |

These are the only files: no real `.nanochart` export was found in public repositories (the format is only produced by the rizu editor's `NanoChartExporter` and embedded in replays).
