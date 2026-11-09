# DGSH sequence (`.bin`, Space Channel 5 Part 2 PC)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (format not documented in the sources opened)

## Overview

The Space Channel 5: Part 2 (PC) "reports" (stages) store their call/response sequences in `.bin` files that the community editor Noizemaker (Hyonk-Tea, then Noizemaker V2 by wigwoo1) opens as "DGSH `.bin`" files. V2 edits entries on a timeline/inspector and patches them into a copy of the game files (`afs_english` layout). Edits save as `.sc5project` files (edit data plus source checksums) and export per report with a manifest. Game assets are read from the user's installation at runtime.

The binary layout, command set (voice calls "chu", "hey", directions…), timing units and "report" structure are Unknown here.

## Container & encoding

Binary `.bin` with magic `DGSH` followed by a u32 LE equal to the file size [observed: Noizemaker-V2_R22_SH2.BIN]; the PC files are stored in AFS archives (`afs_english`) per the editor's folder name.

## Structure / metadata

Unknown. Noizemaker V2 notes: "Report 1's recorded CPU route is supported; other routes and scene names remain provisional"; "Order: CPU run" is a list of 58 input phrases corroborated by captured engine queues for English Report 1.

## Timing model

Unknown (the editor shows a timeline).

## Notes

Unknown beyond commands/phrases.

## Audio & images

Read from the game installation by the editor.

## Versions & variants

Original Noizemaker versus Noizemaker V2 (in development).

## Quirks & pitfalls

The patcher needs matching game files and checksums; exports must go to a folder outside the game directory.

## Example

None.

## ROX support

Not read by ROX.

## Parsers & tools

[wigwoo1/Noizemaker-V2](https://github.com/wigwoo1/Noizemaker-V2) (Lua/LÖVE), [Hyonk-Tea/Noizemaker](https://github.com/Hyonk-Tea/Noizemaker).

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (`*_SH.BIN` from the Noizemaker-V2 repository). [observed: `Noizemaker-V2_*.BIN`] every file starts with `DGSH`, a little-endian u32 equal to the file size (e.g. 10200 for R22_SH2.BIN), then 16-bit values (`0000 0400 0800 0300`) [meaning not documented]. More: install Space Channel 5 Part 2 (PC); files are in the AFS archives per Noizemaker V2's README.

## Sources

- <https://github.com/wigwoo1/Noizemaker-V2> README (read)
