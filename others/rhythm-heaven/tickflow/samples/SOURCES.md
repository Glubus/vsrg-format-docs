# Samples: Rhythm Heaven Megamix / DS tickflow (`.bin`, source `.tickflow`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-spaceball.tickflow` | hand-written from the Tickompiler docs `basic_syntax.rst`, `functions.rst`, `engines.rst` (rhmodding/Tickompiler commit c0c61fa43532fa509a615d732d9a1a6820c84cbc) | vsrg-format-docs (OthersC) | CC0 / public domain | `synthetic` tickflow source: `#index`/`#start` directives, a compile-time variable (`beat = 0x30`), expressions (`beat * 4`), `engine 0` (Spaceball), `rest`, Spaceball operations `0x100` (bat object) and `0x101` (batter costume) |

Notes: this file was NOT run through Tickompiler; it contains no `#assets` directive, which the docs say is needed to insert a game into the ROM. No real tickflow file could be obtained: decompiling needs the game's `.bin` files from a retail copy.
