# Clone Hero `song.ini`
Kind: metadata

Doc status: complete · ROX: decode only · Category: vsrg · Encoding: text

## Overview
`song.ini` is the metadata companion of `notes.mid` and `notes.chart`, used by Clone Hero, YARG, Phase Shift, FoFiX / Frets on Fire and Rock Band-style custom song tools. It holds no notes, but some tags change chart parsing. Its metadata overrides the `.chart` `[Song]` section.

## Container & encoding
INI text: one `[song]` (or `[Song]`) header, then `key = value` lines in any order with inconsistent key case. Pad `=` with spaces (some programs fail without). Comments `;` or `#` (usually whole lines; support varies). Values may hold formatting tags such as `<color=#00FF00>`; strip them if unused. Encoding unspecified. `.sng` converts the tags into its metadata pairs.

## Structure / metadata
Value types: number (-1 can mean unset), float, string (no quotes unless stated), boolean (`True/False`, `true/false`, `0/1`), file name, MIDI note, MIDI velocity.

Standard tags (from GuitarGame_ChartFormats):
| Tag | Meaning |
| --- | --- |
| `name`, `artist`, `album`, `genre`, `year` | song info |
| `rating` | 1 family friendly, 2 supervision recommended, 3 mature, 4 or 0 unrated |
| `charter` (`frets` is a duplicate: ignore), `version` | chart info |
| `preview_start_time`, `preview_end_time` | ms |
| `playlist`, `sub_playlist`, `album_track` (`track`), `playlist_track` | sorting |
| `song_length` | ms (metadata only), `modchart` bool, `loading_phrase` |
| `diff_band`, `diff_guitar`, `diff_guitarghl`, `diff_guitar_coop`, `diff_guitar_coop_ghl`, `diff_guitar_real`, `diff_guitar_real_22`, `diff_rhythm`, `diff_rhythm_ghl`, `diff_bass`, `diff_bassghl`, ... (drums, keys, vocals) | per-track difficulty numbers |
| `pro_drums`, `five_lane_drums` | force drum track type |
| `vocal_gender`, `vocal_scroll_speed` (percent, default 100), `tuning_offset_cents` | vocals |
| `real_guitar_tuning`, `real_guitar_22_tuning`, `real_bass_tuning`, `real_bass_22_tuning` | 4-6 semitone offsets + optional quoted name, e.g. `0 0 0 0 0 0 "Standard tuning"` |
| `icon`, `background`, `video`, `video_loop`, `video_start_time`, `video_end_time`, `cover` | resources |
| `delay` (ms, not recommended), `hopo_frequency` (ticks, recommended), `hopofreq`, `eighthnote_hopo`, `sustain_cutoff_threshold` (ticks), `multiplier_note` / `star_power_note` (103 or 116), `lyrics` | chart behaviour tweaks |

Game/tool specific:
- Clone Hero: `end_events` (bool: honour end events in the chart).
- Phase Shift: `preview` (two ms values, e.g. `55000 85000`), `drum_fallback_blue`, `sysex_slider`, `sysex_high_hat_ctrl`, `sysex_rimshot`, `sysex_open_bass`, `sysex_pro_slide` (enable the `.mid` SysEx events), `guitar_type`/`bass_type`/`kit_type`/`keys_type` (sample sets), `link_name_a/b`, `banner_link_a/b`.
- FoFiX: `cassettecolor`, `tags` (only `cover`), `hopofreq` (0-5; 0 = 1/24 ... 5+ = 1/4 [reader's interpretation]), `early_hit_window_size` (`none|half|full`), `pro_drum`, `tutorial`, `boss_battle`, `scores`, `scores_ext`, `count`, career tags `unlock_id`, `unlock_require`, `unlock_text`, `unlock_completed`.

## Timing model
Only `delay`, `preview_*` and `video_start_time` (ms).

## Notes
Unknown.

## Audio & images
Audio uses reserved file names beside the chart (see chart/mid docs). `background`, `cover`, `icon`, `video` name files in the folder.

## Versions & variants
Phase Shift, FoFiX and Clone Hero each added tags. YARG: https://wiki.yarg.in/wiki/Song.ini

## Quirks & pitfalls
Inconsistent key case; `year` often `", 2002"`; `frets` duplicates `charter`; `delay` changes timing without changing the chart hash; `[Song]` header may be lower case.

## Example
```
[song]
name = Example Song
artist = Example Artist
charter = Someone
diff_guitar = 4
pro_drums = True
preview_start_time = 45000
```
(Hand-built from the tag tables above.)

## ROX support
Read (`SongIni::parse`, `rox::formats::clone_hero`; decode only): `name`, `artist`, `album`, `genre`, `year`, `charter`, `delay`, `song_length`, `preview_start_time`, `preview_end_time`, `sustain_cutoff_threshold`, `background`, `diff_*`. UTF-8 or Latin-1, `[song]` case-insensitive, whole-line `;`/`#` comments, formatting tags removed. Metadata beats `[Song]`, `delay` beats `Offset`. Other tags are ignored.

## Parsers & tools
YARG.Core (C#): https://github.com/YARC-Official/YARG.Core · FoFiX (Python) · Moonscraper.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: every Clone Hero/YARG song folder has a `song.ini`; Chorus Encore stores the same keys as `.sng` metadata (see sng). Tag lists: https://github.com/TheNathannator/GuitarGame_ChartFormats (`docs/Chart-File-Formats/song-ini/Standard-Tags.md`, Clone Hero and Phase Shift tag pages, CC0).

## Sources
https://thenathannator.github.io/GuitarGame_ChartFormats/ (song-ini/Format-Overview, Standard-Tags; Implementation-Specific/Clone-Hero, Phase-Shift, Frets-on-Fire-X song-ini tags) · https://wiki.yarg.in/wiki/Song.ini
