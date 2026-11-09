# SIFTrain beatmap (Love Live! SIF live JSON) (`.json`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

Beatmap JSON used by the SIFTrain simulator (kbz) and compatible with the live-data layout of Love Live! School Idol Festival (note objects with `timing_sec`, `effect`, `effect_value`, `position`; the SIFTrain wiki page was last modified 2015). Converters such as LLPractice -> SIFTrain exist (Piranhaplant/LLP2ST). Source: the SIFTrain wiki page "Beatmap Format" (read through the github-wiki-see mirror).

## Container & encoding

JSON, UTF-8 (`song_name` supports latin/Japanese). The music file is looked up in `/beatmaps/soundfiles` by `music_file` name (extension optional: `.mp3`, `.wav`, `.ogg`).

## Structure / metadata

Root fields: `song_name`, `difficulty` (int 1-4, 1 = easy), `difficulty_name` (optional), `music_file` (optional), `lead_in` (seconds, optional, default 0; delays the audio start without changing note timing), `rank_info` (obsolete as of 2.0: list of `{rank_max}` with 4-5 entries), `song_info` (list; only item 0 is used) with `notes_speed` (obsolete) and `notes` (array).

Note: `timing_sec` (float, seconds since song start), `effect` (bit mask), `effect_value` (number; hold duration in seconds for holds, else 2), `position` (1-9, 1 = rightmost circle).

Effect mask: `1` normal (`0b00000001`), `2` filled/star (obsolete in 2.0), `4` hold (`effect_value` = duration seconds), `8` exclamation (obsolete), `16` simultaneous start, `32` simultaneous end (only used by the randomizer); combinations add up (e.g. `17` = simultaneous normal, `20` = simultaneous hold).

## Timing model

Absolute seconds (`timing_sec`); no BPM map; `lead_in` offsets the audio only.

## Notes

Normal, star (filled, obsolete flag), hold (with duration), exclamation (obsolete), simultaneous flags. Position 1..9 is the target circle (right to left).

## Audio & images

`music_file` only (name looked up in the app's soundfiles folder).

## Versions & variants

SIFTrain 2.0 made `rank_info`, `notes_speed`, `Filled` and `Exclamation` obsolete. The game's own live JSON and livesim2's native beatmap formats were not read.

## Quirks & pitfalls

Position 1 is the **rightmost** circle; simultaneous flags are redundant data that parsers should recompute; hold `effect_value` is seconds.

## Example

From the SIFTrain wiki (sample beatmap, first two notes):

```json
{"song_name":"SAMPLE NAME","difficulty":2,"lead_in":1.0,"difficulty_name":"kb_z's easy","music_file":"rick_roll.mp3",
 "song_info":[{"notes":[
  {"timing_sec":3.043,"effect":1,"effect_value":2,"position":9},
  {"timing_sec":4.889,"effect":1,"effect_value":2,"position":1}]}]}
```

## ROX support

Not read by ROX.

## Parsers & tools

SIFTrain (kbz): <https://github.com/kbz/SIFTrain>; livesim2 (Lua/LOVE): <https://github.com/DarkEnergyProcessor/livesim2_async>; LLBeatmapConvert (Lua): <https://github.com/DarkEnergyProcessor/LLBeatmapConvert>; LLP2ST: <https://github.com/Piranhaplant/LLP2ST>.

## Sources

- <https://github-wiki-see.page/m/kbz/SIFTrain/wiki/Beatmap-Format>
- <https://github.com/kbz/SIFTrain/wiki/Beatmap-Format>
