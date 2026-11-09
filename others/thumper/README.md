# Thumper

"Rhythm violence" game by Drool (Brian Gibson, Marc Flury), 2016 (PC, consoles, VR). A beetle runs along a 3D track at high speed; the player hits thump (tap), grindable (hold), jump, turn, sentry and boss cues on the beat while the track bends in space. Levels are sequencer "leaf" patterns (beat grids that spawn and animate track objects) assembled by level/gate/master objects. There is no official custom-level tooling. The community reverse-engineered the binary `.pc` cache files and built editors (Thumper Custom Level Editor by CocoaMix86; the text-based "Thumper Modding Tool" by RainbowUnicorn7297).

Category: others. A 3D track with turns, jumps, multi-lane objects and boss patterns; cues are objects on a curved path, not columns.

## Formats
| Folder | File | Status |
|---|---|---|
| [objlib/](objlib/README.md) | cache `*.pc` / `.objlib` object libraries (leaf, level, gate, master, spawner, sample, xfm) | binary layout as written by the community modding tool, plus its Python-literal text form (partial) |

## Links
- Thumper Modding Tool (text objects to game cache files): https://github.com/RainbowUnicorn7297/thumper-modding-tool
- Thumper Custom Level Editor (C# GUI): https://github.com/CocoaMix86/Thumper-Custom-Level-Editor
- Thumper-Modding-Tool-resharp (mod loader): https://github.com/CocoaMix86/Thumper-Modding-Tool-resharp
