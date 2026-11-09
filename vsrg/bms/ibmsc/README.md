# iBMSC project file (`.ibmsc`)
Kind: project

Doc status: complete (as implemented by pBMSC; older iBMSC versions differ) · ROX: no · Category: vsrg · Encoding: binary (little-endian, .NET `BinaryWriter`)

## Overview

`.ibmsc` is the **native project/save format of iBMSC** (a BMS/BME/BML/PMS chart editor written in VB.NET for Windows; descendants are **uBMSC** and **pBMSC**). Where [`.bms`](../bms/README.md) is a lossy text export, `.ibmsc` is a binary dump of the editor's in-memory state: header fields, the WAV/BMP definition lists, measure lengths, the note array with editor-only flags, the editor preferences *and the whole undo/redo history*. It is documented here from the pBMSC source (`ChartIO.vb` `OpeniBMSC`/`SaveiBMSC`, `Note.vb`); no spec exists. The iBMSC site states that all `.ibmsc` files from iBMSC 2.x are **not compatible** with iBMSC 3.0, so only the 3.x layout below is covered. The editor also writes autosaves as `AutoSave_<timestamp>.IBMSC` next to the executable, and (pBMSC) a temporary text file with extension `.bmsc` used to launch a player for preview ("Changed the temporary bms file extension from .bms to .bmsc", pBMSC README; that file is ordinary BMS text).

## Container & encoding

- Binary, **little-endian**. Opened with `BinaryReader(stream, Encoding.Unicode)`, so every `string` is the .NET `BinaryWriter.Write(String)` encoding: a **7-bit encoded length prefix giving the number of bytes**, followed by that many bytes of **UTF-16LE**.
- `bool` = 1 byte (0/1). `short`/`int`/`long` = 2/4/8 bytes LE. `double` = IEEE-754 8 bytes, `single` = 4 bytes.
- One file = one chart (the active tab only; the source has `TODO: Save unsaved BMSes instead of just the active one`).
- Not compressed, not encrypted.

## Structure / metadata

### File header (9 bytes)

| Offset | Type | Value |
|---|---|---|
| 0 | int32 | `0x534D4269`, bytes `69 42 4D 53` = ASCII `iBMS` |
| 4 | byte | `0x43` (`C`) |
| 5 | byte | application version major (`My.Application.Info.Version.Major`) |
| 6 | byte | minor |
| 7 | byte | build |

(The reader checks the int32 and the `C`, then reads three version bytes and ignores them.)

### Blocks

After the header the file is a sequence of blocks read until EOF. Each block starts with an **int32 block ID** (a 4-character tag stored as a little-endian integer); the reader dispatches with a `Select Case` that has **no default and no length field**, so an unknown ID cannot be skipped and desynchronises parsing. The writer emits them in this order:

| ID (int32) | Bytes in file | Name | Body |
|---|---|---|---|
| `0x66657250` | `P r e f` | Preferences | `int32 flags`; `int32 gDivide`; `int32 gSub`; `int32 gSlash`; `single gxHeight`; `single gxWidth`; `int32 gColumns` (grid division 16, subdivision 4, 192 ticks per measure, zoom, number of columns, defaults 16/4/192/1.0/1.0/46) |
| `0x64616548` | `H e a d` | Header | see below |
| `0x00564157` | `W A V 00` | WAV list | `byte options` (bit0 multi-select, bit1 change-label); `int32 count`; `count x { int16 index; string filename }` |
| `0x00504D42` | `B M P 00` | BMP list | same layout as WAV list |
| `0x74616542` | `B e a t` | Measures | `int16 beatN; int16 beatD; byte changeMode; int32 count; count x { int16 measureIndex; double length }` |
| `0x6E707845` | `E x p n` | Expansion | `string` free-form text (the editor's "expansion code" box: raw extra BMS lines) |
| `0x65746F4E` | `N o t e` | Notes | `int32 ubound; ubound x note` (see below) |
| `0x6F646E55` | `U n d o` | Undo/redo | `int32 100`; `int32 currentIndex`; then for slot 0..200 (inclusive, `UndoRedoCount = 200`): `int32 undoCount; undoCount x { int32 len; byte[len] cmd }`, `int32 redoCount; redoCount x { int32 len; byte[len] cmd }` |

`flags` bits of the Preferences block (all booleans of the UI state): `0x1` NT input mode, `0x2` error check, `0x4` preview on click, `0x8` show file name, `0x100..0x2000` menu/toolbar/panel visibility, `0x4000` show grid, `0x8000` sub-grid, `0x10000` BG, `0x20000` measure numbers, `0x40000` measure bars, `0x80000` vertical lines, `0x100000` show C (comment/column), `0x200000` BGA column, `0x400000` STOP, `0x800000` BPM, `0x20000000` SCROLL, `0x1000000` snap, `0x2000000` disable vertical move, `0x4000000/0x8000000/0x10000000` split-panel locks. Not needed to reconstruct the chart.

### Header block (`Head`)

In order:

| Field | Type | BMS equivalent |
|---|---|---|
| title | string | `#TITLE` |
| artist | string | `#ARTIST` |
| genre | string | `#GENRE` |
| bpm | int64 | `#BPM` x 10000 (this is also stored as the special note 0) |
| player/rank | byte | low nibble = `#PLAYER` combo-box index, high nibble = `#RANK` index (`value >> 4`) |
| playLevel | string | `#PLAYLEVEL` |
| subTitle | string | `#SUBTITLE` |
| subArtist | string | `#SUBARTIST` |
| stageFile | string | `#STAGEFILE` |
| banner | string | `#BANNER` |
| backBMP | string | `#BACKBMP` |
| difficulty | byte | `#DIFFICULTY` combo index |
| exRank | string | `#EXRANK` |
| total | string | `#TOTAL` |
| comment | string | `#COMMENT` |
| lnObj | int16 | `#LNOBJ` combo index (index into the WAV list; 0 = none) |

(Fields `#MAKER`, `#MIDIFILE`, `#VOLWAV`, `#LNTYPE` are present as commented-out lines in the source and are **not** stored.)

### Measures block (`Beat`)

`beatN/beatD` is the editor's current beat-resolution selector; `changeMode` is the "beat change" option (index into {Preserve, Measure, Cut, Scale}). Then `count` records for measures whose length differs from the default: `measureIndex` (0..999) and `length` as a `double` in **ticks, where 192.0 = one 4/4 measure** (`length / 192` is the BMS `#xxx02` ratio).

### Note record (33 bytes, `Note.WriteBinWriter`)

| Offset | Type | Field | Meaning |
|---|---|---|---|
| 0 | double | VPosition | vertical position in ticks from the start of measure 0 (a measure is 192 ticks at default length; a note in measure `m` at fraction `f` has `VPosition = measureBottom(m) + f * length(m)`) |
| 8 | int32 | ColumnIndex | editor column (table below) |
| 12 | int64 | Value | object value x 10000: for a keysound/BGM/BMP note the base-36 object ID (`01`..`ZZ`) is `Value / 10000`; for a BPM column note it is the BPM x 10000; for STOP/SCROLL columns the stop/scroll value x 10000 |
| 20 | bool | LongNote | BMSE-style long-note flag (paired with the following note in the same column) |
| 21 | double | Length | NT-style long-note length in ticks (0 = short note); used when the NT input mode is on |
| 29 | bool | Hidden | invisible object (channels `3x/4x`) |
| 30 | bool | Landmine | landmine object (channels `Dx/Ex`) |
| 31 | bool | Ghost | editor "ghost" note (reference layer, not exported) |
| 32 | bool | Comment | editor comment note (not exported) |

Note index 0 is **not stored**; it is a synthetic BPM note (`ColumnIndex = BPM column`, `VPosition = -1`, `Value` = header BPM x 10000) created from the header. The file stores notes 1..ubound, so `ubound` equals the stored note count.

### Column indices (`EditorColumns.vb`)

`0` measure, `1` SCROLL, `2` BPM, `3` STOP, `4` spacer, `5..12` A1..A8 (player 1; base channel ids from the column table: A1 = 16 (scratch), A2..A6 = 11..15 (keys 1-5), A7 = 18 (key 6), A8 = 19 (key 7)), `13` spacer, `14..21` D1..D8 (player 2: D1..D5 = 21..25, D6 = 28, D7 = 29, D8 = 26 (scratch)), `22` spacer, `23` BGA, `24` LAYER, `25` POOR, `26` spacer, `27+` B columns (BGM/background tracks; `27 + k` = k-th BGM column, unlimited). The BMS channel is derived from the column's base channel id (`Column.Identifier`, the `xIdentifier` constructor argument, e.g. `16`, `11`; BGM `B` columns use `1`) plus offsets for long notes (`+0x40` for `5x`/`6x`), hidden (`3x`/`4x`) and landmine (`Dx`/`Ex`) objects (`GetBMSChannelBy`).

### Undo/redo commands

Each command is an opaque byte array starting with an opcode byte: `0` void, `1` add note, `2` remove note, `3` change note, `4` move note, `5` long-note modify, `6` hidden-note modify, `7` relabel, `15` remove all, `16` change measure length, `17` change time selection, `18` NT toggle, `20` WAV auto-increment flag, `21` change measure, `255` no-operation (`UndoRedo.fromBytes`). Payloads embed `Note` records. They are only useful to restore the editor's history.

## Timing model

BMS-style: tick positions inside variable-length measures (192 ticks = 4/4 measure at length 1.0), initial BPM in the header, BPM changes as notes in the BPM column (value = BPM x 10000), STOPs in the STOP column and SCROLL changes in the SCROLL column. There are **no separate `#BPMxx` tables**: the BPM/STOP/SCROLL objects carry the values; the exporter creates `#BPMxx`/`#STOPxx`/`#SCROLLxx` definitions and picks the extended-BPM channel (`+5`) when the BPM is non-integer, >= 256 or negative (`GetBMSChannelBy`). Seconds are computed like BMS: for each segment `duration = ticks / 192 * 4 * 60 / BPM`, plus STOP time (a `#STOP` value of `v` lasts `v / 192` of a 4/4 measure at the current BPM, standard BMS semantics). [inference: the timing math is standard BMS, not specific to `.ibmsc`.]

## Notes

Keys: 5K/7K (+scratch) singles, doubles (A and D columns), PMS 9-button, plus BGM/BGA/LAYER/POOR channels. Tap = `LongNote=false, Length=0`; hold = a `LongNote` pair (BMSE mode) or a note with `Length > 0` (NT mode); hidden, landmine, ghost and comment flags as above. Keysounds are the object IDs in `Value`; their filenames come from the WAV list (index 1..1295 = base-36 `01`..`ZZ`).

## Audio & images

WAV list (`index -> filename`) and BMP list (`index -> filename`, also used for BGA/LAYER/POOR image objects); header `stageFile`/`banner`/`backBMP` strings. Paths are stored as typed (relative to the chart).

## Versions & variants

- iBMSC 1.x/2.x (`.cff`, `.th`, `.lol`, `.ibmsc` of that era) are not compatible with 3.0 (iBMSC update history).
- iBMSC 3.0 introduced the layout above; uBMSC and pBMSC (version string `3.5.5.16` in pBMSC's `AssemblyInfo.vb`) keep the same block structure. The SCROLL column and preference bit `0x20000000` exist in the pBMSC source.
- Autosave files use the same layout (`AutoSave_*.IBMSC`).

## Quirks & pitfalls

- No block length: unknown block ID = parse failure (the reader has no `Case Else`).
- Strings are UTF-16LE with a byte-length prefix, not UTF-8.
- `Value` is x10000: object IDs are `Value / 10000`, BPM `Value / 10000`.
- `VPosition` uses the **editor's** measure lengths (192 per measure); measures are addressed by cumulative length, so measure-length records must be applied before placing notes in time.
- Undo/redo history makes files large; a reader that only wants the chart should stop after the `Note` block (the writer always emits `Undo` last).
- Format is VB.NET-internal; nothing guarantees backward compatibility between builds.

## Example

No sample in the repo; the format is binary and the source has no embedded example. Illustrative, hand-built from the rules above - the first 9 bytes of a file saved by version 3.5.5:

```
69 42 4D 53 43 03 05 05 | 50 72 65 66 ...
 i  B  M  S  C  maj min bld   'P' 'r' 'e' 'f'  (Preferences block starts)
```

## ROX support

Not read by ROX. ROX has no BMS support in 0.8.1 (planned); an `.ibmsc` reader would first need a BMS-like model (tick/measure timing, BPM/STOP objects, keysound objects).

## Parsers & tools

- iBMSC / uBMSC / pBMSC (VB.NET): [`Shimi9999/pBMSC`](https://github.com/Shimi9999/pBMSC) (`iBMSC/ChartIO.vb` `OpeniBMSC`/`SaveiBMSC`, `iBMSC/Option Windows/Note.vb`, `iBMSC/UndoRedo.vb`, `iBMSC/EditorColumns.vb`), original: [`aqtq314/iBMSC`](https://github.com/aqtq314/iBMSC).
- Other editors listed on [hitkey.nekokan.dyndns.info/editors.html](https://hitkey.nekokan.dyndns.info/editors.html): GDAC2, BMSE, uBMSC, pBMSC, iBMSCPP (native macOS/C++/Swift).
- No third-party standalone `.ibmsc` parser found.

## Sources

- https://github.com/Shimi9999/pBMSC (commit `06aaf7438dbca3c8a0611bd13d134f6d1ce04a28`): `iBMSC/ChartIO.vb` lines ~1072-1505, `iBMSC/Option Windows/Note.vb`, `iBMSC/EditorColumns.vb`, `iBMSC/UndoRedo.vb`, `iBMSC/MainWindow.vb` (defaults), `iBMSC/Strings.vb` ("iBMSC Binary Format (*.ibmsc)"), `README.md`
- https://www.cs.mcgill.ca/~ryang6/iBMSC/ and https://www.cs.mcgill.ca/~ryang6/iBMSC/UpdateHistory.html (compatibility note)
- https://github.com/aqtq314/iBMSC
