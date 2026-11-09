# Pistol Whip

VR rhythm shooter by Cloudhead Games (PC VR, Quest, PS VR/PS VR2). The player moves forward along a track on a fixed path, shooting enemies, dodging walls and ducking obstacles in time with the music. Two ecosystems of custom levels exist: the community "Pistol Whip Custom Levels" (PWCL) mod and editor (Givo, MelonLoader/Unity) whose JSON formats can be read from the mod source, and the official "Pistol Mix" modding tool (mod.io) whose `.pw`, `.pw_event`, `.pw_art` JSON files are only described in mod.io guides (not fetched here).

Category: **others**: targets are enemies with 3D placement (near/middle/far distance, x/y placement grid), obstacles and scripted enemy action sequences along a moving path; no lanes.

## Formats
| Folder | File | Status |
|---|---|---|
| [pwcl-level/](pwcl-level/README.md) | `level.pw`, `<Diff>.pw_beat`, `.pw_koreo`, `.pw_sec`, `.pw_geo` | PWCL community level folder, JSON files, reconstructed from the mod's C# classes and real sample levels (partial) |

## Links
- PWCL docs (Docsify site, mostly stubs for the structure page): https://pwcl.givo.xyz/
- PWCL mod, editor and level repository (GitLab): https://gitlab.com/pwcl
- Official Pistol Mix guide: https://mod.io/g/pistol-whip/r/official-pistol-mix-how-to-guide
- Geomancer guide (level.pw, .pw_event, .pw_art notes): https://mod.io/g/pistol-whip/r/geomancer
