# EZ2AC keysound index (`.ezi`)
Kind: audio

Doc status: partial · ROX: no · Category: vsrg · Encoding: text (CP949), possibly encrypted like `.ez`

## Overview
Text sidecar of an [`.ez`](../ez/README.md) chart: maps each note key (keysound index) to a sample file. Documented from EZ2BMS `io/ez/ezi.ts`, which reproduces EZ2PORT's `ez2/ezi.c` (itself a transcription of the original `EziLoader::loadEZI`).

## Container & encoding
Text, CP949 (Korean). Plain or encrypted with the `.ezi` key table (same cipher as `.ez`; EZ2PORT treats it as plaintext if its first 512 bytes contain no control characters other than TAB/LF/CR and no DEL).

## Structure / metadata
scanf-style tokens: `<note> <mode> <file>`; a mode-2 line carries a second file (read and ignored by the game). Parse rules of the original: a `;` comment skips a PAIR of tokens, not a line; a later line for the same note wins; a trailing token without a mode ends the parse; a note outside the table rejects the whole file. Token buffers are 64 bytes, names 260 bytes. Table size: 0x800 slots in the original executable, 0x10000 in EZ2PORT (u16 keys of v8 notes). File name in the text is `.wav`, the game's is `.ssf`.

## Timing model / Notes
Not applicable.

## Audio & images
Keysound file names (`.ssf` in the game folder; `.wav` accepted).

## Versions & variants
Old charts name notes like MIDI keys: `C#0 1 mix-st.wav` (the original's `atol` reads all as note 0, EZ2BMS reads octave*12 + semitone); `ez2EziConverter` (EZ2Tools) converts such old EZI to the modern numeric ids.

## Quirks & pitfalls
Comment tokens skip pairs; duplicates overridden; legacy note names.

## Example
Not applicable beyond the legacy line quoted above (from the EZ2BMS source comment).

## ROX support
Not read by ROX.

## Parsers & tools
EZ2BMS (https://github.com/Roganis/EZ2BMS), EZ2Tools `ez2EziConverter` (https://github.com/ben-rnd/EZ2Tools).

## Getting samples
- **Committed: none (no real file found).** Same situation as [`.ez`](../ez/README.md#getting-samples): no `.ezi` file found at any public source reached; EZ2BMS's fixtures contain none (`packages/chart-core/test/fixtures/README.md`).
- **How to get one**: copy the `.ezi` keysound-name files from an EZ2DJ/EZ2AC installation you own, next to the `.ez` charts of the same song; they use their own 512-byte cipher table (fiche, EZ2BMS `ez2data/crypt.ts`). Tools: https://github.com/Roganis/EZ2BMS, https://github.com/ben-rnd/EZ2Tools.

## Sources
- https://raw.githubusercontent.com/Roganis/EZ2BMS/main/packages/chart-core/src/io/ez/ezi.ts
- https://raw.githubusercontent.com/ben-rnd/EZ2Tools/master/ez2EziConverter/README.md
