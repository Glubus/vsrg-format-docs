# Beat Saber

VR rhythm game by Beat Games (Meta), released 2018. The player holds two sabers and slices colored blocks flying along a 4 x 3 grid, avoids bombs and walls, and follows arcs and chains. Custom maps are distributed mainly through BeatSaver (`.zip` packages) and edited with the Official Editor, ChroMapper, MediocreMapAssistant and others.

Category: others. Notes are free 3D objects on a 4-column x 3-row grid in front of the player (plus rotation lanes in 360/90 degree modes), cut with a direction. Obstacles are volumes, and much of the file is lighting. It does not fit the vsrg column model.

## Formats

| Folder | File | What |
|---|---|---|
| [info-dat/](info-dat/README.md) | `Info.dat` (v2, v4) and legacy `info.json` (v1) | Map entry point: metadata, audio/cover references, list of difficulties |
| [dat/](dat/README.md) | `<Difficulty>.dat` (v2, v3, v4), `Lightshow.dat` (v4), `BPMInfo.dat` / `AudioData.dat` | Beatmap objects (notes, bombs, walls, arcs, chains), events and lightshow, audio BPM regions |

Related: Ragnarock uses a format derived from Beat Saber v2 ([../ragnarock/](../ragnarock/README.md)).

## Links

- BSMG Wiki, map format: https://bsmg.wiki/mapping/map-format.html
- BeatSaber-Deno (`bsmap`): https://github.com/KivalEvan/BeatSaber-Deno
- BeatSaver: https://beatsaver.com/
