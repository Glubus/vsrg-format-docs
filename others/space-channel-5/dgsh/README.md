# DGSH sequence (`.bin`, Space Channel 5 Part 2 PC)
Kind: chart

Doc status: stub · ROX: no · Category: others · Encoding: binary (format not documented in the sources opened)

## Overview

The **Space Channel 5: Part 2 (PC)** "reports" (stages) store their call/response sequences in `.bin` files that the community editor **Noizemaker** (Hyonk-Tea, then **Noizemaker V2** by wigwoo1) opens as "DGSH `.bin`" files. In V2, entries are picked from a list, edited on a timeline/inspector (commands are labelled instead of identified by file name), applied to a pending patch set and **patched** into a copy of the game files (`afs_english` layout). Edits can be saved as `.sc5project` files containing edit data and source checksums, and exported per report with a manifest. Game assets are read from the user's own installation at runtime.

Only this much is documented in the READMEs opened. The binary layout of the DGSH files, the command set (voice calls "chu", "hey", directions…), timing units and the "report" structure are **Unknown** here.

## Container & encoding

Binary `.bin` ("DGSH" presumably a magic [inference from the editor wording]); the PC files are stored in AFS archives (`afs_english`) per the editor's folder name.

## Structure / metadata

Unknown. Noizemaker V2 notes: "Report 1's recorded CPU route is supported; other routes and scene names remain provisional"; "Order: CPU run" is a list of 58 input phrases corroborated by captured engine queues for English Report 1.

## Timing model

Unknown (the editor shows a timeline).

## Notes

Commands/phrases; no further detail.

## Audio & images

Audio and voice previews are read from the game installation by the editor.

## Versions & variants

Original Noizemaker vs Noizemaker V2 (in development).

## Quirks & pitfalls

The patching tool requires matching game files and checksums; exports must go to a folder outside the game directory.

## Example

Not applicable.

## ROX support

Not read by ROX.

## Parsers & tools

[wigwoo1/Noizemaker-V2](https://github.com/wigwoo1/Noizemaker-V2) (Lua/LÖVE), [Hyonk-Tea/Noizemaker](https://github.com/Hyonk-Tea/Noizemaker).

## Sources

- <https://github.com/wigwoo1/Noizemaker-V2> README (read)
