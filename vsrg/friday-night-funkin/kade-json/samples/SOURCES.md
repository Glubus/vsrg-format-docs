# Samples: FNF Kade Engine chart

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-kade-ke1.json | Hand-written for this repository (synthetic), built from the fiche and Kade `Song.hx` | the repository author (public domain / CC0 1.0) | CC0 1.0 | chartVersion KE1: eventObjects (Init BPM, BPM Change at beat 8, Scroll Speed Change), sections with startTime/endTime, 5-element notes [time, lane, sustain, isAlt, beat], isAlt true, changeBPM, playerAltAnim |
| synthetic-kade-ke1-meta.json | Hand-written for this repository (synthetic), built from the fiche | the repository author (public domain / CC0 1.0) | CC0 1.0 | the `_meta.json` companion (`name`, `offset`); named `synthetic-kade-ke1-meta.json` here |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| kade_bopeebo.json | https://raw.githubusercontent.com/Kade-github/Kade-Engine/b1fe905d9cfdcd10705f48ff47d62d1165d6c63a/assets/preload/data/songs/bopeebo/bopeebo.json | Kade Engine repo is Apache-2.0; the charts are FNF base-game data (not cleared for redistribution here); fetched only (master @ b1fe905) | Kade repo chart, unconverted (no chartVersion/eventObjects); the engine converts it to KE1 at load; 32 sections, 118 notes, 46 holds, lanes 0..6, note array lengths [3], bpm 100.0, 0 changeBPM sections |
| kade_offsettest.json | https://raw.githubusercontent.com/Kade-github/Kade-Engine/b1fe905d9cfdcd10705f48ff47d62d1165d6c63a/assets/preload/data/songs/offsettest/offsettest.json | Kade Engine repo is Apache-2.0; the charts are FNF base-game data (not cleared for redistribution here); fetched only (master @ b1fe905) | Kade offset-test chart; 27 sections, 55 notes, 1 holds, lanes 0..3, note array lengths [3], bpm 100, 0 changeBPM sections |
| kade_ridge.json | https://raw.githubusercontent.com/Kade-github/Kade-Engine/b1fe905d9cfdcd10705f48ff47d62d1165d6c63a/assets/preload/data/songs/ridge/ridge.json | Kade Engine repo is Apache-2.0; the charts are FNF base-game data (not cleared for redistribution here); fetched only (master @ b1fe905) | minified single-line JSON; 66 sections, 258 notes, 68 holds, lanes 0..7, note array lengths [3], bpm 145, 0 changeBPM sections, 11492 trailing NUL bytes after the closing brace |
| kade_milf.json | https://raw.githubusercontent.com/Kade-github/Kade-Engine/b1fe905d9cfdcd10705f48ff47d62d1165d6c63a/assets/preload/data/songs/milf/milf.json | Kade Engine repo is Apache-2.0; the charts are FNF base-game data (not cleared for redistribution here); fetched only (master @ b1fe905) | extra song fields (gfVersion); 95 sections, 513 notes, 102 holds, lanes 0..7, note array lengths [3], bpm 180, 0 changeBPM sections |
