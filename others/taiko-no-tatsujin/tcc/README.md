# Open Taiko Chart (`.tci` + `.tcc`, also `.tcm`)
Kind: chart

Doc status: partial (Rev.1 documented; Rev.2.x additions not opened) · ROX: no · Category: others · Encoding: json (UTF-8 without BOM)

## Overview

**Open Taiko Chart** is a JSON-based chart format created by **AioiLight** (2019-08-17, rev. 1) to replace `.tja`/`.tjf`, whose weaknesses are complicated multi-difficulty/2-player text, hard parsing and the Shift-JIS encoding. A "work" is a set of files: one **`.tci` (Open Taiko Chart Information)** — metadata and the list of courses — plus one or more **`.tcc` (Open Taiko Chart Course)** files that hold the actual measures, plus audio/video in the same folder. Revisions: Rev.1, Rev.2 (Dan-i/rank certification support) with 2.1–2.4, Rev.3 (branching, still being specified at the time of writing). A **`.tcm` (Open Taiko Chart Medley)** JSON groups several charts (format rev. 2, 2019-11-15). Supported by Koioto (plugin "OpenTaikoChart"), TJAPlayer3-f ≥ 1.6.0.1 and OpenTaiko (0auBSQ) 0.6.1 (which adds `.optktci`/`.optktcm`). Details from the Rev.1 Japanese specification.

Category: **others** — same as [TJA](../tja/README.md).

## Container & encoding

JSON, **UTF-8 without BOM** (mandatory because of JSON), any newline convention. One `.tci` per work (never two); `.tcc` files are referenced from the `.tci`; audio/video must be in the same folder as the `.tci`.

## Structure / metadata

### `.tci` (Information)

| Key | Type | Meaning |
|---|---|---|
| `title`, `subtitle` | string | titles |
| `artist`, `creator` | array of strings | artists / chart authors |
| `audio` | string | audio file name (codec depends on the software) |
| `background` | string | background image or video |
| `bpm` | number | base BPM |
| `offset` | number | time (seconds) at which the first measure starts |
| `courses` | array of objects | one per difficulty: `difficulty` (`"oni"`, `"edit"`, …), `level` (number), `single` (path of the single-player `.tcc`), `multiple` (array of per-player `.tcc` paths, e.g. `["Edit_1P.tcc","Edit_2P.tcc"]`) |

### `.tcc` (Course)

| Key | Type | Meaning |
|---|---|---|
| `scoreinit`, `scorediff` | int | initial / increment of the score formula |
| `scoreshinuchi` | int | "shinuchi" (真打) score |
| `balloon` | int array | balloon hit counts, in order |
| `measures` | array of arrays of strings | one inner array per measure |

The Rev.1 sample uses the key `"measure"` while the field table and the C# class say `measures` — implementations should be tolerant [inconsistency in the source].

Measure strings: either note strings (`0` blank, `1` don, `2` ka, `3` DON, `4` KA, `5` roll, `6` ROLL, `7` balloon, `8` roll end) or commands. A mid-measure command splits the measure into several strings; each command is a string on its own: `#bpm n`, `#scroll n`, `#tsign n1/n2`, `#gogobegin`, `#gogoend`, `#delay s`. Rules: only `0` may occur inside a roll (e.g. `50001008`), never repeat the head symbol up to the end (`666668`).

## Timing model

Same as TJA: each note string is divided evenly into its symbols over the measure (4/4 unless `#tsign`), `bpm` / `#bpm` give the tempo, `offset` the start time of measure 1 (seconds), `#delay` shifts later notation.

## Notes

`1`–`8` as in TJA (no `9`, `A`–`I`, no branches in Rev.1).

## Audio & images

`audio`, `background` (same folder as the `.tci`).

## Versions & variants

Rev.1 (2019-08-17), Rev.2 (Dan-i), Rev.2.1–2.4, Rev.3 (branches; under specification). OpenTaiko adds `.optktci`/`.optktcm` with custom fields.

## Quirks & pitfalls

- Key `measure`/`measures` ambiguity (above). The `"name"` key appears in a table example for `title` (sample JSON uses `title`).
- Commands must be alone in their own array element.
- Rolls must be terminated by `8`.

## Example

From the Rev.1 specification (`.tcc` sample):

```json
{
    "scoreinit": 800,
    "scorediff": 200,
    "scoreshinuchi": 1200,
    "balloon": [ 6, 10, 24 ],
    "measure":
    [
        [ "1" ],
        [ "3030" ],
        [ "40", "#gogobegin", "40" ],
        [ "#gogoend", "70008010" ]
    ]
}
```

## ROX support

Not read by ROX 0.8.1.

## Parsers & tools

[AioiLight/Open-Taiko-Chart](https://github.com/AioiLight/Open-Taiko-Chart) (spec, C# classes for Json.NET), Koioto plugin, TJAPlayer3-f, OpenTaiko.

## Sources

- <https://github.com/AioiLight/Open-Taiko-Chart> (README, `Rev1_ja-JP.md` read)
- <https://iepiweidieng.github.io/TJAPlayer3/tja> (table of formats: `.tcc`, `.tci`, `.tcm`, `.optktci`)
