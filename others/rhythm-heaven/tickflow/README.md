# Rhythm Heaven Megamix / DS tickflow (`.bin`, source `.tickflow`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (source form: text)

## Overview

"Tickflow" is the community name for the bytecode driving every minigame, remix and cutscene of Rhythm Heaven Megamix (3DS) and, with another opcode set, Rhythm Heaven DS. A program is a list of 32-bit instructions run by a small multi-threaded VM; timing comes from `rest` instructions in ticks (48 ticks = 1 beat), and engine-specific cue instructions (opcodes from 0x100) spawn the minigame prompts. The official "chart" is this script, not a note list. Tickompiler (rhmodding, Kotlin) compiles the text `.tickflow` language to little-endian `.bin` and back; the RHMPatch (Luma3DS patch) loads the results. The docs are marked "severely outdated" by their authors, with an archive at rhmodding.github.io/rhm-docs-archive.

## Container & encoding
- Binary `.bin`, little-endian (the CLI always passes `ByteOrder.LITTLE_ENDIAN`; the `Decompiler` class also supports big-endian internally). Source form: `.tickflow` text (extension required by the CLI).
- Files extracted from a decrypted `code.bin` with Tickompiler's `extract` command, one file per game/remix; `pack` / `put` re-insert them; `tfobj` is Tickompiler's "objectified" output folder.
- Megamix files start with a 12-byte metadata header (three 32-bit ints: `index`, `start`, `assets`); DS files (`--ds`) have no such header ("also disables Megamix-specific metadata").
- The body ends with the terminator word `0xFFFFFFFE`, followed by a string table (see below).

## Structure / metadata
Header (Megamix):

| Offset | Size | Field |
|---|---|---|
| 0 | u32 | `#index`: index of the rhythm game this file replaces when patched into the game |
| 4 | u32 | `#start`: byte offset where execution begins (usually 0) |
| 8 | u32 | `#assets`: byte offset of the asset-loading section (intro screen etc.), required for insertion |

Instruction encoding (Tickompiler `Decompiler.kt`):

| Bits of the first u32 | Meaning |
|---|---|
| 0-9 | opcode (0..0x3FF) |
| 10-13 | argument count (0..15) |
| 14-31 | "special" argument (a signed/unsigned value, also used to select variants of an opcode: `if`, `speed_relative`, asset-type operations, etc.) |

The instruction is followed by `argCount` u32 arguments. Then comes the next instruction. A first word `0xFFFFFFFF` prefix introduces Tickompiler-specific *annotations* (count + list of u32; type 0 = argument is a marker location, 1 = UTF-16 string, 2 = ASCII string, 3 = raw byte block) used for round-tripping; whether the game files themselves contain annotations is not established. [inference: annotations are a Tickompiler extension]

After the `0xFFFFFFFE` terminator come NUL-terminated strings, each padded to a 4-byte boundary; ASCII strings are stored as bytes, UTF-16 strings as 16-bit units (detected by the second byte being 0). Strings are referenced by their byte offset from the start of the instruction stream (counter used as the argument value).

Source language (`.tickflow`):
- Function calls `op<special> arg1, arg2, ...` (0 to 15 args), `op` is a name or a number; expressions with `* + - / >> << & | ^`.
- Compile-time variables `name = expr`; markers `name:`; directives `#index`, `#start`, `#assets`, `#alias name num`, `#include`.

## Timing model
- Unit: the tick; 48 (0x30) ticks per beat. There are no timestamps: events happen when the program reaches them, and `rest N` suspends the thread for N ticks (the rest counter decrements at 48 per beat, so tempo is independent). `unrest N` subtracts from the counter (buffering). `getrest/setrest` stores durations in slots.
- Tempo/BPM: the music tempo comes from the sound assets, not from the script; `speed val` sets playback speed to `val/256` of the original (0x100 = 100%), which also changes pitch; `speed_relative val, lb, ub` multiplies.
- Concurrency: threads are spawned by `async_call loc, delay` / `async_sub id, delay, cat`; `call` and `sub` are synchronous; `kill_*` operations stop threads by category, location or sub id. Each thread has its own rest counter and conditional variable context. [inference for per-thread rest]
- Cue timing inside a game engine is relative to the instruction (e.g. the Spaceball bat object `0x100 time, type`: `time` ticks before the batter has to hit).

## Notes
There are no notes. Gameplay cues are engine-specific instructions after `engine id` (0x28): e.g. Spaceball (engine 0): `0x100` bat object, `0x101` costume, `0x102` camera zoom, `0x103` alien animation; Clappy Trio (1): `0x100 time` clap cue (input after `2*time` ticks); Sneaky Spirits (2); Rhythm Tweezers (3): `0x100 type` spawn hair (plucked 4 beats later). Engines may bundle cue patterns into numbered subroutines (from 0x56 upward, `sub`/`async_sub`). Input is toggled by `0x6A` (`input flag`). Scoring ("skill star") is `0xAE`.

Core global operations (selection from the docs):
`0` async_sub, `1<0>` get_async / `1<1>` set_func, `2` async_call, `3` kill_*, `4` sub, `5` get_sync, `6` call, `7` return, `8` stop, `9` set_cat, `0xA` set condvar, `0xB` add condvar, `0xC` push condvar, `0xD` pop condvar, `0xE` rest, `0xF` getrest/setrest, `0x11` rest_reset, `0x12` unrest, `0x14` label, `0x15` goto, `0x16..0x18` if/else/endif (variants neq/lt/leq/gt/geq), `0x19..0x1D` switch/case/break/default/endswitch, `0x1E` countdown family, `0x24` speed, `0x25` speed_relative, `0x28` engine, `0x2A` game_model/cellanim/effect/layout slot assignment, `0x31/0x35/0x39/0x3E` model/cellanim/effect/layout asset management, `0x40` play_sfx, `0x5D` set_sfx, `0x5F` remove_sfx, `0x6A` input, `0x7E/0x7F/0x80` zoom/pan/rotate view, `0xAE` skill star, `0xB8` random.

## Audio & images

Not in the file: audio, cellanims, models, effects and layouts are referenced by slot/asset ID through asset-management operations. `set_sfx slot, str` loads a group name (string offset) into a slot; `play_sfx id` takes an ID whose encoding is "not yet clear" (docs).

## Versions & variants

- Megamix (3DS): metadata header, `MegamixFunctions` opcode table (Tickompiler default).
- Rhythm Heaven DS: `DSFunctions` opcode table, no header (`--ds`).
- Fever (Wii), Tengoku (GBA): not covered by Tickompiler per the sources opened.
- Tickompiler docs are for v1.9.0 and flagged outdated; rhmodding.github.io/rhm-docs-archive is the current reference (not opened).

## Quirks & pitfalls

- The "special" argument is part of the first word; `rest`, `label`, `goto`, `unrest` take their value only as special.
- Strings are addressed by offset into the stream plus string area, so inserting instructions moves them: use the compiler, not raw patching.
- Decompiler-generated marker names (`locNN:`): decompile/compile is not byte-identical unless metadata and annotations are kept.
- The 10-bit opcode space is shared between global operations and engine operations from 0x100. Do not mix `MegamixFunctions` and `DSFunctions` meanings.

## Example
Illustrative, hand-built from the documented syntax and signatures (not a real game file), Megamix style:

```
#index 0
#start 0
beat = 0x30        // 48 ticks = 1 beat
engine 0           // Spaceball
0x100 beat, 1      // bat object: a rice ball (type 1), `time` = 0x30 ticks before input
rest beat * 4      // wait 4 beats (rest counter += 192)
0x101 2            // batter costume: bunny
```

## ROX support

Not read by ROX. An executable script, not a chart; a decoder would need to emulate the VM and game engines.

## Parsers & tools
- Tickompiler (Kotlin; compile, decompile, extract, pack, put): https://github.com/rhmodding/Tickompiler
- Tickompiler docs: https://tickompiler.readthedocs.io/
- RHMPatch (3DS patch loading the compiled files): https://github.com/SneakySpook/RHMPatch (referenced in Tickompiler README)
- RHModding resources and guides: https://rhmodding.github.io/resources-and-guides/

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md) (`.tickflow` sources `1-1.tickflow` ... `4-4.tickflow` from the RHYTHM HEAVEN RE:MEGAMIX modpack repository by viviancherry9, plus `synthetic-spaceball.tickflow`; compiled `.bin`/`.tempo` not kept). More: that repository has more files and compiled output in `tickflow/Compiled/`; with a retail Megamix, decompile the game's `.bin` files with Tickompiler (`DecompileCommand`); "Doc's Remix Templates" are linked from https://rhmodding.github.io/resources-and-guides/ (Google Drive, not fetched).

## Sources
- https://github.com/rhmodding/Tickompiler (docs `basic_syntax.rst`, `concepts.rst`, `engines.rst`, `functions.rst`, sources `decompiler/Decompiler.kt`, `compiler/Compiler.kt`, `cli/CompileCommand.kt`, `cli/DecompileCommand.kt`)
- https://tickompiler.readthedocs.io/
- https://rhmodding.github.io/resources-and-guides/ (not opened, found by search)
