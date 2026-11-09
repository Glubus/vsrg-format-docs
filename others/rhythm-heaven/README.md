# Rhythm Heaven (リズム天国 / Rhythm Paradise) and Rhythm Heaven Studio

Nintendo/tsunku♂ rhythm minigame series (GBA *Rhythm Tengoku*, DS, Wii *Fever/Minna no Rhythm Tengoku*, 3DS *Megamix*). Each stage is a short minigame played to a beat with single-button inputs; there are no scrolling notes: the "chart" is a **cue/script timeline** (when each game's cue happens). The official games' timelines are compiled "tickflow" scripts inside the ROM/archives; no chart format of the official games was researched in sources I could open (not documented here).

The one **documented, open** chart format in the series' ecosystem is the **RIQ** file of the fan game **Rhythm Heaven Studio** (RHeavenStudio, Unity), which lets players build "remixes" out of minigame events on a beat timeline.

**Category: others** — event/cue timeline per minigame (not note lanes).

## Formats

| Folder | Format | Notes |
|---|---|---|
| [riq/](riq/README.md) | `.riq` Rhythm Heaven Studio remix (zip of JSON charts + audio) | documented through the open-source Jukebox library |
| [tickflow/](tickflow/README.md) | `.bin` / `.tickflow` Rhythm Heaven Megamix (3DS) and DS game scripts | bytecode VM described by Tickompiler; cue scripts of the official games (partial) |

## Links

- Jukebox (RIQ parser/serializer): <https://github.com/RHeavenStudio/Jukebox>
- Rhythm Heaven Studio: developed by the RHeavenStudio organisation (<https://github.com/RHeavenStudio>), uses Jukebox for its file format
