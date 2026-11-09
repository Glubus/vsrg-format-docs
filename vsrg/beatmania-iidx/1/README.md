# beatmania IIDX arcade chart (`.1`)
Kind: chart

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary

Binary chart archive used by the beatmania IIDX arcade games ("first discovered in 9th Style AC", per SaxxonPike). Source: SaxxonPike/rhythm-game-formats `iidx/1.md` and the `iidx-ps2tools` chart plugins (`charttool/iidx_common.py`, `plugins/iidx25thac.py`).

## Overview

- Each song has one `.1` file in the game data (alongside a `.2dx` sound archive, see [`../2dx`](../2dx/README.md)). The `.1` holds all difficulties of the song: the file name is typically the numeric song id (e.g. `01000` in the plugin's metadata comment), but the extension `.1` and the id naming are from the tools, not an official doc.
- No official documentation; everything is reverse-engineered. Konami's data is not encrypted at this level (the chart bytes are plain, little-endian), but the files live in game HDD/IFS data, not in this repo.
- Older IIDX games (3rd-8th style arcade) and the PS2 home versions used other chart layouts; `iidx-ps2tools` has a plugin per style (`iidx3rdcs.py` ... `iidx16thcs.py`) whose code is the only description. Not documented here.

## Container & encoding

- Binary, **little-endian**. One file = *directory* (12 entries x 8 bytes = 0x60 bytes) followed by chart blobs.
- Directory entry (SaxxonPike): `+00 int32 offset of the chart from the start of the file`, `+04 int32 length in bytes`. The charts are "typically" stored right after the directory but this must not be assumed. An empty slot has offset 0 or size 0 (iidx-ps2tools skips them).
- The 12 slots map to difficulties (`IIDX_AC_DIFFICULTY_MAPPING` in iidx-ps2tools): 0 = SP NORMAL, 1 = SP HYPER, 2 = SP ANOTHER, 6 = DP NORMAL, 7 = DP HYPER, 8 = DP ANOTHER. The other slots (3-5, 9-11) are unnamed in the tools (SP/DP BEGINNER, LEGGENDARIA etc. are not covered by the sources read) [inference: unused or later difficulties].
- Each chart ends with the terminator event whose offset is `0x7FFFFFFF` (bytes `FF FF FF 7F 00 00 00 00`).

## Structure / metadata

The file has no text metadata (no title/artist); those live in the game's music database. Only the events below.

Event (8 bytes, little-endian):

| Offset | Type | Meaning |
| --- | --- | --- |
| +00 | int32 | event offset in ticks |
| +04 | byte | event type |
| +05 | byte | event parameter |
| +06 | int16 | event value |

Event types (SaxxonPike; `0B` appears as `unk` in iidx-ps2tools):

| Type | Meaning | Parameter | Value |
| --- | --- | --- | --- |
| `00` | Visible note, player 1 | column | `0` = normal note; non-zero = freeze (charge) note length in ticks |
| `01` | Visible note, player 2 | column | same |
| `02` | Sample change, player 1 | column | sample number the column now plays |
| `03` | Sample change, player 2 | column | sample number |
| `04` | Tempo change | denominator (0 invalid) | numerator; BPM = numerator/denominator (denominator 1 or 100 in practice) |
| `05` | Meter (time signature) information | denominator | numerator |
| `06` | End of song | - | - |
| `07` | BGM sound | stereo panning `01`-`0F` (left to right, `08` centre) | sound number |
| `08` | Timing window information | which part of the window (see below) | frame count, signed 8-bit |
| `0B` | unknown | - | - |
| `0C` | Measure bar | player the bar is visible for | - |
| `10` | Note count information | player | number of playable notes |

Columns: `00` key 1, `01` key 2, `02` key 3, `03` key 4, `04` key 5, `05` key 6, `06` key 7, `07` scratch.

Timing window parameters (type `08`, value = signed frame count, "frames ahead of the note a player presses"; negative = late, positive = early; JUST GREAT is implicitly 0 and 1): `00` latest end of the judgement window, `01` latest end of GOOD, `02` latest end of GREAT, `03` earliest end of GREAT, `04` earliest end of GOOD, `05` earliest end of the window. The default example values in the spec's figure are -16, -6, -1, 3, 8, 18; GAMBOL uses -15, -7, 0, 2, 9, 17. Some double charts repeat these events; effect unknown.

The iidx-ps2tools 25th-style plugin shows slightly different field naming for the same bytes (`<BBH` = type, param, value), e.g. type `05` as `numerator=param`, `denominator=value`, which disagrees with SaxxonPike's text (Parameter = denominator, Value = numerator). The PS2/old "create_event_ps2" path in the same tool packs numerator/denominator the other way round. Check with real data before relying on the order for meter events [uncertain].

## Timing model

- No tick rate is stored. SaxxonPike: ticks per second depend on the game version: **before 14 GOLD 59.94**, **GOLD 60.046**, **after GOLD 1000** ("precision greatly increases on TROOPERS and later"). Seconds = `offset / ticks_per_second`.
- Tempo events (`04`) are informational for display/BPM; positions are already absolute ticks. A converter to a beat grid must integrate the tempo events: [inference] derive beats from ticks and BPM since the file has no beat positions except measure-bar events (`0C`).
- Meter (`05`) tells the game how to count beats (e.g. 7/8 sections in some songs; "probably the flashing graphic in the background").
- No stops/scroll events: speed effects are done with tempo events.

## Notes

- Playable notes: types `00`/`01` with the column in the parameter. Freeze notes (charge notes) = non-zero value = length in ticks (the SaxxonPike spec; the iidx25thac plugin names it `value`).
- Keysounds: each column has a "current sample" set by type `02`/`03` events at the chart start and whenever the keysound changes; a note plays the sample currently assigned to its column ("does not actually make a sound by itself"). BGM sounds are `07` events with a sound number and a pan.
- Mines/BSS: no separate event types are known; the sources do not mention them.
- Note count (`10`) per player.
- SP charts use player-1 events; DP charts use both players' events.

## Audio & images

Sample numbers index the keysounds in the song's `.2dx` archive ([`../2dx`](../2dx/README.md)). No image data in the chart.

## Versions & variants

- `.1` since 9th style AC; "the latest format in use today". Tick resolution changed at GOLD/TROOPERS (see Timing).
- `iidx25thac.py` is the plugin that reads/writes 25th style AC charts; it writes the directory with `0x60` bytes header, chart offsets relative to file start.
- Earlier AC and console formats: not documented in the sources read.

## Quirks & pitfalls

- Chart end is the `0x7FFFFFFF` marker, not the chart length alone.
- Offset `0` note events are dropped by the writer plugin (`if event_name in [note_p1, note_p2] and offset == 0: continue`) - a hint that offset-0 notes are invalid.
- Tick rate must be provided by the caller (game version).
- Denominator 0 in tempo events is invalid.
- Several events at the same tick are normal; the plugin groups them by offset preserving order.

## Example

No real file is included. Hand-built from the table above (illustrative, not a real chart): a minimal chart with one BPM event of 120 (numerator 120, denominator 1) at tick 0 and a normal note on key 1 for player 1 at tick 1000, then the terminator, as hex (little-endian):

```
00 00 00 00  04 01 78 00      tick 0, type 04, param 01 (denominator), value 0x0078 = 120
E8 03 00 00  00 00 00 00      tick 1000, type 00 (P1 note), column 0, value 0 (tap)
FF FF FF 7F  00 00 00 00      end of chart
```

## ROX support

Not read by ROX. A decoder needs per-game tick rates and meter/BPM integration; 8 columns per side with freeze notes map to Tap/Hold.

## Parsers & tools

- SaxxonPike/iidx-ps2tools charttool (Python): https://github.com/SaxxonPike/iidx-ps2tools (`charttool/iidx_common.py`, `plugins/iidx25thac.py`; converts `.1` <-> JSON).
- SaxxonPike/rhythm-game-formats `iidx/1.md`.

## Getting samples

No sample is committed: no real file of this format could be obtained. Searches on 2026-11-09 (GitHub path search through Sourcegraph for `<id>.1`, `*_op.bin`/`*_hp.bin`/`*.ifs`; the repositories of every parser/converter named below; archive.org full-text/title search; web searches) found no public copy: the tools ship no fixtures and the only archive.org items are whole-game dumps or soundtracks (not individual chart files, and far above the 20 MB limit or audio). The data is Konami game data that exists only inside a game installation. A hand-written binary `.1` was not made either, because the layout is only partly verified (see Doc status).

How to obtain real files (you need your own copy of the game):

- From an IIDX installation, the song folder holds the chart next to its sound archive. The converter iidx2bms (Python GUI + `one2bme` C tool) looks, for a song id `<id>`, in `\contents\data\sound\<id>\` (or directly in `\contents\data\sound\`) for `<id>.1` + `<id>.s3p` + `<id>_pre.2dx`, or else for one `<id>.ifs` archive (read with `ifstools`, which unpacks `<id>.1`, `<id>.2dx`, `<id>_pre.2dx`). Source: `iidx2bms/conversion/conversion.py` (`_find_chart_source`, `_prepare_from_ifs`) at https://github.com/Glebsin/iidx2bms/blob/893a6a94b0bc442356be88852188cd5e05fe1b8e/iidx2bms/conversion/conversion.py and its README ("Choose your `\contents\data\sound\` and `\contents\data\movie\` paths").
- The `.ifs` wrapper is unpacked with mon/ifstools (https://github.com/mon/ifstools).
- drmext/iidx-datatools `parse_chart_notecounts.py` "supports .ifs files directly and loose .1 files in directories" (README of the LupinThidr mirror, commit a4c86e76c79f2d1f1dd9aa0c03fd97d377b314e4), a cheap way to check that a dumped `.1` parses.
- Slot layout seen in a converter: `one2bme.c` of iidx2bms maps directory slot 0 to `[Hyper7]`, 1 `[Normal7]`, 2 `[Another7]`, 3 `[Beginner7]`, 4 `[Leggendaria7]`, 6 `[Hyper14]`, 7 `[Normal14]`, 8 `[Another14]`, 10 `[Leggendaria14]` (`kDiffs` table, commit 893a6a94b0bc442356be88852188cd5e05fe1b8e). This differs from the "Container" section above, which, following iidx-ps2tools, lists slot 0 as SP NORMAL and slot 1 as SP HYPER, and does not name slots 3-5 and 9-11; which one is right for which game version is Unknown [uncertain: not verified on real data].
- Converters that write BMS/BME from `.1`: iidx2bms (https://github.com/Glebsin/iidx2bms), osu!mania: QingQiz/iidx2osu. Community BMS recreations of official charts exist (ZIv thread "beatmania, beatmania IIDX and pop'n music official BMS/PMS simfiles preservation project") but they are BMS files, not `.1`.

## Sources

- https://raw.githubusercontent.com/SaxxonPike/rhythm-game-formats/master/iidx/1.md
- https://raw.githubusercontent.com/SaxxonPike/iidx-ps2tools/master/charttool/iidx_common.py
- https://raw.githubusercontent.com/SaxxonPike/iidx-ps2tools/master/charttool/plugins/iidx25thac.py
- https://github.com/SaxxonPike/iidx-ps2tools (README)
- Zenius-I-Vanisher thread on IIDX timing (cited by the spec): https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=5233
- iidx2bms (Getting samples): https://github.com/Glebsin/iidx2bms/tree/893a6a94b0bc442356be88852188cd5e05fe1b8e (`iidx2bms/conversion/conversion.py`, `iidx2bms/one2bme/one2bme.c`, `README.md`)
- iidx-datatools mirror (Getting samples): https://github.com/LupinThidr/iidx-datatools/tree/a4c86e76c79f2d1f1dd9aa0c03fd97d377b314e4
