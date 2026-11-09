# Rhythm Heaven (リズム天国 / Rhythm Paradise) and Rhythm Heaven Studio

Nintendo/tsunku♂ rhythm minigame series (GBA *Rhythm Tengoku*, DS, Wii *Fever/Minna no Rhythm Tengoku*, 3DS *Megamix*). Each stage is a short minigame with single-button inputs and no scrolling notes: the "chart" is a cue/script timeline. Official timelines are compiled "tickflow" scripts inside the ROM/archives; no other official chart format was researched. The one documented open format is the RIQ file of the fan game Rhythm Heaven Studio (RHeavenStudio, Unity), which builds "remixes" from minigame events on a beat timeline.

Category: others, event/cue timeline per minigame (not note lanes).

## Formats

| Folder | Format | Notes |
|---|---|---|
| [tickflow/](tickflow/README.md) | `.bin` / `.tickflow` Rhythm Heaven Megamix (3DS) and DS game scripts | bytecode VM described by Tickompiler; cue scripts of the official games (partial) |

## Links

- Jukebox (RIQ parser/serializer): <https://github.com/RHeavenStudio/Jukebox>
- Rhythm Heaven Studio: developed by the RHeavenStudio organisation (<https://github.com/RHeavenStudio>), uses Jukebox for its file format
