# Friday Night Funkin' (FNF) and its engines

Friday Night Funkin' is a free rhythm game by ninjamuffin99, PhantomArcade and The Funkin' Crew Inc. (author line of its itch.io page). It started as a 2020 game-jam build (the first public data layout is documented as "FNF (Ludum Dare)" in Moonchart) and is now developed commercially; the V-Slice 0.3+ update introduced the `.fnfc` chart packages. Four arrow lanes (left, down, up, right) scroll vertically on each side of the screen: the opponent's strumline and the player's strumline. The player hits arrows (and holds) in a rap battle. There is no chart format specification from the original authors for the early builds; the game's data files are JSON and each mod engine forked and extended the schema. This folder documents each variant that has its own schema, one folder per variant.

Category: **vsrg**. Justification: fixed arrow lanes (4 per side), vertical scrolling toward a strumline, time-ordered taps and holds; the format is a note list per lane.

ROX: `.json` files are read and written as FNF by ROX (experimental), using the legacy `song.notes[].sectionNotes` layout (see below). Players of V-Slice charts (`.fnfc`, `-chart.json`) are not read.

## Variants

| Folder | File(s) | Origin | Doc status | ROX |
|---|---|---|---|---|
| [legacy-json](legacy-json/README.md) | `<song>[-easy\|-hard].json`, `{"song": {...}}` | vanilla FNF up to 0.2.8 (week charts), most Kade/Psych-era mods | complete | read + write |
| [psych-json](psych-json/README.md) | same JSON, `psych_v1` format | Psych Engine (ShadowMario) | complete | read + write only as legacy layout; see doc for the lane-semantics difference |
| [kade-json](kade-json/README.md) | same JSON + `_meta.json` | Kade Engine (KadeDev), chart version `KE1` | partial | legacy-compatible subset |
| [codename-json](codename-json/README.md) | `charts/<diff>.json` + `meta.json` | Codename Engine (FNF-CNE-Devs) | partial | no |
| [fps-plus-json](fps-plus-json/README.md) | legacy JSON + `meta.json` + `events.json` | FPS Plus (ThatRozebudDude) | stub | no |
| [troll-json](troll-json/README.md) | Psych-derived JSON | Troll Engine (riconuts) | stub | no |
| [fnfc](fnfc/README.md) | `.fnfc` ZIP | V-Slice (official, 0.3+) | complete | no |
| [vslice-chart-json](vslice-chart-json/README.md) | `<song>-chart[-<variation>].json` | V-Slice | complete | no |
| [vslice-metadata-json](vslice-metadata-json/README.md) | `<song>-metadata[-<variation>].json` | V-Slice | complete | no |
| [ludum-dare-png](ludum-dare-png/README.md) | one PNG per section + `.json` | the Ludum Dare 47 jam build | stub | no |
| [nmv-json](nmv-json/README.md) | Psych-derived JSON, `format: "nmv2"`, `keys`/`lanes` | NightmareVision (NMVTeam) | partial | no |
| [maru-json](maru-json/README.md) | legacy-like JSON with `sectionEvents`, `offsets`, `players` | Maru Funkin' (dead engine, via Moonchart) | stub | no |
| [fnfmod](fnfmod/README.md) | `.fnfmod` ZIP | V-Slice mod package | stub | no |

`.fnfm`: no file format of this name was found in any source consulted; the closest real extensions are `.fnfc` (chart package) and `.fnfmod` (mod package, announced in the Funkin' Crew blog of 2026-08-03).

Other engines exist (Forever Engine, Leather Engine, Andromeda, ...). They were NOT inspected: their schema is unknown here (Moonchart lists no distinct format for them). NightmareVision and Maru Funkin' have their own folders above (Maru only from Moonchart's description).

## Samples

Each variant folder has a `samples/` folder with a `SOURCES.md` (hand-written synthetic charts, committed; real FNF charts are only fetched through the manifest because the game data is not freely redistributable) and a `Getting samples` section in its README.

## Cross-variant facts

- Time unit: milliseconds everywhere (note `strumTime`, sustain length), except Kade event positions (beats) and V-Slice's optional future `timeFormat`.
- Lane meaning: 0 = left, 1 = down, 2 = up, 3 = right, per strumline. Which strumline a note belongs to is encoded differently per variant (`mustHitSection` + lane 0-7 in legacy; `d` 0-7 in V-Slice; a per-strumline list in Codename).
- Hold notes: a start time plus a length in ms (`sustain length`); the game spawns sustain pieces every step (`stepCrochet = 60000 / bpm / 4`).
- Sections: legacy/Psych/Kade group notes in sections of 16 steps (4 beats); V-Slice and Codename have no sections.
- Moonchart (Haxe) converts between all of these, plus osu!mania, Quaver, StepMania, Clone Hero and MIDI: https://github.com/MaybeMaru/moonchart .

## Sources

- https://github.com/FunkinCrew/Funkin (tags v0.2.7.1 and main), https://github.com/FunkinCrew/Funkin/blob/main/docs/FNFC-SPEC.md
- https://github.com/ShadowMario/FNF-PsychEngine, https://github.com/Kade-github/Kade-Engine, https://github.com/FNF-CNE-Devs/CodenameEngine
- https://github.com/MaybeMaru/moonchart
- https://funkincrew.github.io/funkin-modding-docs/
- ROX source: `src/formats/fnf/*`, `src/formats/auto/detect.rs`
