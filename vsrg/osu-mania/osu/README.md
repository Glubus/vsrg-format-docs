# osu! beatmap (`.osu`)
Kind: chart

Doc status: complete · ROX: reads/writes (mode 3 only; mode 1 taiko decode only, modes 0 and 2 refused) · Category: vsrg (for mode 3; the other modes live in `others/`) · Encoding: text

Canonical `.osu` page. The mode pages ([osu!standard](../../../others/osu-standard/osu/README.md), [osu!taiko](../../../others/osu-taiko/osu/README.md), [osu!catch](../../../others/osu-catch/osu/README.md)) cover only per-mode differences and link back here.

## Overview
`.osu` is the beatmap file of osu! (ppy / peppy; versions v3 to v14 stable, v128 lazer). One file is one difficulty of one game mode (`Mode:` in `[General]`: 0 standard, 1 taiko, 2 catch, 3 mania). A mapset archive (`.osz`) bundles the `.osu` files, audio, images, videos, an optional storyboard (`.osb`) and hitsound samples. It is the most commonly imported chart format here (Quaver imports `.osz`; Moonchart and ROX have `.osu` mania codecs; Quaver.API ships converters). Only `Mode: 3` suits a vertical scrolling game. Files live in `Songs/` (stable), lazer's file store and osu.ppy.sh `.osz` downloads.

## Packaged in

- `.osz`: zip of a beatmap set (one `.osu` per difficulty, audio, background, optional video, `.osb` storyboard, hitsounds).
- `.olz`: zip exported by osu!lazer (the set's `.osu` difficulties plus audio, images, storyboard); lazer-only, not readable by stable.

## Container & encoding

- UTF-8 text. Older files may carry a BOM; the full ROX parser does not strip it, so a BOM-prefixed first line is not recognised as the version line and is ignored (`OsuDecoder::peek_mode` has a test with a BOM-prefixed file). `\n` and `\r\n` are both accepted (ROX strips a trailing `\r`).
- One file per difficulty, named `Artist - Title (Creator) [Version].osu` by convention (the samples follow it).
- The first non-empty line is the magic `osu file format v<N>`. lazer's `Decoder` builds a decoder for version `N` if the line starts with `osu file format v`, otherwise a decoder of the latest version (osu source `Beatmaps/Formats/Decoder.cs`, `LegacyBeatmapDecoder.Register`).
- Section headers are `[Name]` on their own line. Lines starting with `//` are comments. lazer also strips a trailing `// ...` from any line except in `[Metadata]`, since titles may contain `//` (osu source `LegacyDecoder.cs`: `ShouldSkipLine`, `StripComments`).
- Key/value sections use `Key: Value`, split at the FIRST `:` with both sides trimmed (`SplitKeyVal`). Real files mix `Key: Value` (`[General]`, `[Editor]`, `[Difficulty]` in some versions) and `Key:Value` (`[Metadata]`, `[Difficulty]`), see the samples.
- Unknown sections and keys are ignored. lazer logs and skips lines that fail to parse; ROX also logs and skips bad timing-point and hit-object lines.
- Whole-file limit in ROX: 100 MiB.

## Structure / metadata

Sections in the order osu! writes them:

| Section | Content | Notes |
|---|---|---|
| `osu file format vN` | version line | not a section; first line |
| `[General]` | `Key: Value` | |
| `[Editor]` | `Key: Value` | editor state only |
| `[Metadata]` | `Key:Value` | |
| `[Difficulty]` | `Key:Value` | |
| `[Events]` | comma lists | background, video, breaks, storyboard |
| `[TimingPoints]` | comma lists | |
| `[Colours]` | `Key : Value` | combo/skin colours, `r,g,b` |
| `[HitObjects]` | comma lists | |
| `[Variables]` | `$name=value` | storyboard variables, `.osb` only, not supported in `.osu` per the wiki |

lazer's `LegacyDecoder.Section` enum also lists `Fonts`, `CatchTheBeat` and `Mania`. No keys of them are handled in the sources consulted. [inference: historical sections, never documented].

### `[General]`

(ppy/osu-wiki `.osu` page; defaults from the wiki.)

| Key | Type | Meaning | Default |
|---|---|---|---|
| `AudioFilename` | string | audio file relative to the folder | |
| `AudioLeadIn` | int ms | silence before audio starts | 0 |
| `AudioHash` | string | deprecated (only written in versions <= 13 by osu-file-parser) | |
| `PreviewTime` | int ms | preview start; `-1` = none | -1 |
| `Countdown` | int | 0 none, 1 normal, 2 half, 3 double | 1 |
| `SampleSet` | string | `Normal`, `Soft`, `Drum` default sample set | Normal |
| `StackLeniency` | decimal 0-1 | standard-mode stacking | 0.7 |
| `Mode` | int | 0 osu!, 1 taiko, 2 catch, 3 mania | 0 |
| `LetterboxInBreaks` | 0/1 | | 0 |
| `StoryFireInFront` | 0/1 | deprecated | 1 |
| `UseSkinSprites` | 0/1 | storyboard may use skin images | 0 |
| `AlwaysShowPlayfield` | 0/1 | deprecated | 0 |
| `OverlayPosition` | string | `NoChange`, `Below`, `Above` | NoChange |
| `SkinPreference` | string | preferred skin | |
| `EpilepsyWarning` | 0/1 | | 0 |
| `CountdownOffset` | int beats | | 0 |
| `SpecialStyle` | 0/1 | mania "N+1" key layout (extra special column, normally the first) | 0 |
| `WidescreenStoryboard` | 0/1 | | 0 |
| `SamplesMatchPlaybackRate` | 0/1 | | 0 |

lazer also reads `SampleVolume` (default hit sample volume, default 100), which the wiki table lacks (osu source `LegacyBeatmapDecoder.handleGeneral`). A missing `Mode` means 0, so a file without `Mode:` is osu!standard. ROX `peek_mode` follows the same rule and treats a non-numeric value as 0.

### `[Editor]`

`Bookmarks` (comma list of ms), `DistanceSpacing` (decimal), `BeatDivisor` (int, lazer clamps it to the editor's allowed range), `GridSize` (int), `TimelineZoom` (decimal). lazer also reads `VelocityPresets` (comma list of decimals). No gameplay effect. In versions <= 5 `Bookmarks` and `DistanceSpacing` were stored in `[General]` as `EditorBookmarks` / `EditorDistanceSpacing` (osu-file-parser, general/mod.rs: written only when version <= 5). [third-party parser evidence]

### `[Metadata]`

`Title` (romanised), `TitleUnicode`, `Artist` (romanised), `ArtistUnicode`, `Creator`, `Version` (= difficulty name), `Source`, `Tags` (space separated), `BeatmapID` (difficulty id), `BeatmapSetID` (set id). IDs are 0 or -1 for unsubmitted maps. ROX copies them to `chart_id`/`chartset_id` and casts negative ids to u64 as-is (ROX source `build_metadata`).

### `[Difficulty]`

| Key | Meaning |
|---|---|
| `HPDrainRate` | 0-10 |
| `CircleSize` | 0-10 for std/taiko/catch; for mania the key count (lazer clamps mania to 1..18: `MAX_MANIA_KEY_COUNT = 18`) |
| `OverallDifficulty` | 0-10; for mania the judgement window difficulty |
| `ApproachRate` | 0-10; if absent lazer copies `OverallDifficulty` into it (very old files) |
| `SliderMultiplier` | base slider velocity: hundreds of osu!pixels per beat (lazer clamps to 0.4-3.6) |
| `SliderTickRate` | ticks per beat (lazer clamps to 0.5-8) |

### `[Colours]`

`Combo1`, `Combo2`, ... (additive combo colours), `SliderTrackOverride`, `SliderBorder`; value is `R,G,B` (0-255 each; lazer also accepts `R,G,B,A` for skin colours). Irrelevant for mania.

### `[Events]`

`eventType,startTime,eventParams`; `eventType` is a name or a number.

| Event | Syntax | Notes |
|---|---|---|
| Background | `0,0,"file.jpg",xOffset,yOffset` | offsets optional; quotes usual, not required |
| Video | `Video,startTime,"file.avi",xOffset,yOffset` (or `1,...`) | start time may be negative (sample: `Video,-608,"op.avi"`). lazer treats the event as a background if the extension is not a known video extension (very old maps misused `1`) |
| Break | `2,startTime,endTime` (or `Break,...`) | |
| Storyboard objects / samples | see below | |

Real files carry the 4 storyboard layer headers as comments (`//Storyboard Layer 0 (Background)` ... `//Storyboard Sound Samples`) so editors can place lines.

#### Storyboard events (inside `[Events]`, or the `.osb` file)

Source: ppy/osu-wiki `Storyboard/Scripting/*`. An object declaration is followed by indented commands (one leading space or `_` per level).

```
Sprite,<layer>,<origin>,"<filepath>",<x>,<y>
Animation,<layer>,<origin>,"<filepath>",<x>,<y>,<frameCount>,<frameDelay>,<loopType>
Sample,<time>,<layer>,"<filepath>",<volume>
```

- `layer`: `Background`/0, `Fail`/1, `Pass`/2, `Foreground`/3 (`Sample` uses the numeric form).
- `origin`: TopLeft 0, Centre 1, CentreLeft 2, TopRight 3, BottomCentre 4, TopCentre 5, Custom 6, CentreRight 7, BottomLeft 8, BottomRight 9. Coordinates are in a 640x480 space (widescreen storyboards extend it).
- `Animation`: frames are `name0.png`, `name1.png`... referenced as `name.png`; `loopType` `LoopForever` (default) or `LoopOnce`; `frameDelay` in ms.
- `Sample`: audio played at `time` ms on a layer (so it plays in Pass or Fail state only if the layer says so), `volume` 1-100 (default 100). Many mania maps use storyboard `Sample` lines as keysounds (see the sample `STARTails - ne! ne! ne! (TV Size) ... [EZ].osu`, which has ~80 `Sample,<ms>,0,"LR_Clap Fast Low.wav",70` lines).
- Commands: `<event>,<easing>,<start>,<end>,<params...>`, event letters `F` fade, `M` move, `MX`, `MY`, `S` scale, `V` vector scale, `R` rotate (radians), `C` colour (r,g,b), `P` parameter (`H` flip h, `V` flip v, `A` additive blend); compound `L,<start>,<loopCount>` (children prefixed by two levels, times relative to each iteration) and `T,<trigger>,<start>,<end>[,<group>]` (trigger types `HitSound[SampleSet][AdditionsSet][Addition][CustomSet]`, `Passing`, `Failing`). Easing 0-34 (0 linear, 1 out, 2 in, 3-5 quad, 6-8 cubic, 9-11 quart, 12-14 quint, 15-17 sine, 18-20 expo, 21-23 circ, 24-28 elastic, 29-31 back, 32-34 bounce). When the end time is omitted/equal and the end values are omitted, the start values are reused (`_F,0,1000,3000,1`).
- `[Variables]` (`$name=value`) are textual substitutions allowed only in `.osb` files.
- `.osb` is a separate optional file in the beatmap folder, shared by all difficulties of the set; see [../osb/README.md](../osb/README.md).

## Timing model

`[TimingPoints]` lines: `time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects`. Sorted chronologically (required by the format; lazer re-sorts hit objects only).

| Field | Meaning |
|---|---|
| `time` | ms (decimal allowed) from the beginning of the audio; the section lasts until the next point |
| `beatLength` | uninherited: ms per beat (`BPM = 60000 / beatLength`). Inherited: negative value = `-100 / SV multiplier` (`-50` = 2.0x, `-100` = 1.0x, `-133.33` = 0.75x). lazer: a NaN beatLength on an inherited point disables slider ticks (edge case) |
| `meter` | beats per measure (inherited points ignore it); lazer treats a first char `0` as 4 |
| `sampleSet` | 0 beatmap default, 1 normal, 2 soft, 3 drum |
| `sampleIndex` | custom sample index; `0` = osu! default |
| `volume` | 0-100 |
| `uninherited` | `1` = timing (red) point, `0` = inherited (green) point |
| `effects` | bit 0 kiai, bit 3 omit first barline (taiko, mania) |

- All objects carry absolute ms times, so playing a chart needs no beat/measure arithmetic. Beats matter only for editor snapping and slider length.
- An uninherited point resets the SV multiplier to 1. An inherited point at the same `time` as an uninherited one refines it (lazer queues same-time points and lets non-timing points override). Several points may share a `time`.
- Mania scroll speed: lazer maps the inherited-point multiplier to `EffectControlPoint.ScrollSpeed` for rulesets 1 (taiko) and 3 (mania) (`LegacyBeatmapDecoder.handleTimingPoint`). In mania the multiplier scales scroll speed only; hit timing is unaffected. `SliderMultiplier` has no effect on mania notes.
- ROX: uninherited points with `beatLength > 0` become `TimingPoint::Bpm { bpm = 60000/beatLength, signature = meter }`; inherited ones become `TimingPoint::Sv { scroll_speed = -100/beatLength }` (ROX source `OsuTimingPoint::bpm/scroll_velocity`). Time becomes microseconds as `(time * 1000) as i64` (truncation).
- Format versions < 5: osu! applies a +24 ms correction to every time value (timing points, hit objects, breaks, non-negative preview time) (osu source `EARLY_VERSION_TIMING_OFFSET = 24`). ROX does NOT apply it.

Truncated real example (sample `HoneyWorks - Kikoemasu ka ... [Normal].osu`):

```
60,476.190476190476,3,1,1,15,1,0      <- BPM 126, 3/4, soft, volume 15
11488,-100,3,1,1,20,0,0               <- inherited, SV x1.0, volume 20
45774,-100,3,1,1,30,0,1               <- kiai on
```

## Notes

`[HitObjects]` line: `x,y,time,type,hitSound,objectParams,hitSample`.

| Field | Meaning |
|---|---|
| `x`,`y` | osu!pixel position in a 512x384 playfield (lazer clamps both to 0..512 and, below version 128, truncates to integers) |
| `time` | ms |
| `type` | bit flags: bit 0 hit circle, bit 1 slider, bit 2 new combo, bit 3 spinner, bits 4-6 combo colour skip, bit 7 mania hold |
| `hitSound` | bit flags: bit 0 normal (1), bit 1 whistle (2), bit 2 finish (4), bit 3 clap (8). No bit set = normal |
| `objectParams` | per type, below |
| `hitSample` | `normalSet:additionSet:index:volume:filename`, default `0:0:0:0:` |

lazer masks out the new-combo bit and the 3-bit skip first, then decodes the type in this order: circle (bit 0), slider (bit 1), spinner (bit 3), hold (bit 7). Unknown type: the line is rejected.

### osu!mania objects

- Key count `K` = `[Difficulty] CircleSize` (rounded; at least 1; lazer clamps to <= 18; ROX parses it as f32, defaults to 4 if unparseable, and casts to `u8` with truncation).
- Column: `column = floor(x * K / 512)`, clamped to `0 .. K-1` (wiki). ROX computes `(x * K) / 512` in integer arithmetic without clamping (`OsuHitObject::column`): an `x` >= 512 or negative gives an invalid column, caught later by ROX validation (`InvalidColumn`). Standard mania x for the centre of column `i`: `floor((i + 0.5) * 512 / K)` (e.g. K=4: 64, 192, 320, 448; K=7: 36, 109, 182, 256, 329, 402, 475, see the samples).
- `y` is ignored; editors write 192.
- Tap note = hit circle: `type` 1 (5 with the new-combo bit, as in the sample first line `182,192,429,5,2,...`; the bit means nothing in mania). No `objectParams`; `hitSample` follows `hitSound`.
- Hold note (LN) = `type` 128 (bit 7): `x,y,time,128,hitSound,endTime:hitSample`. `endTime` and the sample are joined by `:` instead of `,`: the end time is the FIRST element of the colon-separated 6-part field `endTime:normalSet:additionSet:index:volume:filename`. Real example (sample `HoneyWorks ... [Normal].osu`): `329,192,10536,128,0,11012:0:0:0:0:`. If the field is missing lazer sets `endTime = startTime` (zero-length hold; do not rely on it). Combinations with other bits (e.g. 128 + 4 new combo = 132) occur in the wild; decode by testing bit 7.
- Sliders and spinners are not used in mania. ROX's hit-object parser reads only `x,time,type,hitSound` and the raw tail; any object without bit 7 is decoded as a tap in the column derived from `x`, so a stray slider/spinner line becomes a tap (see Quirks).
- Any number of objects can share a `time`. Two objects in the same column must not overlap (ROX validation `OverlappingNotes`: a note starting before the previous note in that column ended is an error).
- No release timing is stored beyond `endTime`; `endTime` > `time` is required (ROX `InvalidHoldDuration` for duration <= 0).

### Hitsounds / keysounds

- `hitSound` bit flags select which of the 4 samples play: normal, whistle, finish, clap (wiki). Sample files are named `<set>-hit<sound><index>.wav` with `set` in `normal|soft|drum` (`normalSet` for the normal sound, `additionSet` for the additions) and `index` omitted for 0/1. Lookup order: beatmap folder (only if `index != 0`), then the skin, then the default resources (wiki).
- `hitSample`: `normalSet` / `additionSet` (0 none, 1 normal, 2 soft, 3 drum), `index` (0 = take the timing point's), `volume` (1-100, 0 = take the timing point's), `filename` (if present, ONLY that file in the beatmap folder is played and no additions).
- Mania keysound maps use that `filename` field per note. Real example (sample `HoneyWorks ... [Normal].osu`): tap `256,192,11488,1,0,0:0:0:40:bell2.wav` (volume 40, custom file); hold `182,192,14345,128,0,15298:0:0:0:40:bell2.wav`.
- Effective volume/set: the hit-object value if non-zero, else the timing point active at the object's end time (+5 ms leniency in lazer: `CONTROL_POINT_LENIENCY`).
- In every mode except mania the `LayeredHitSounds` skin option forces the normal sound; mania does not layer (wiki).
- Storyboard `Sample` lines (see Events) are the other way maps carry background hitsounds.
- ROX: for each note whose `filename` is not empty it creates one `Hitsound { file, volume }` per distinct filename and sets `hitsound_index`; `volume` 0 means `None`. Sets and `hitSound` flags are not preserved (ROX source `assign_hitsound`).

### Other modes (summary; details in `others/`)

Modes 0-2 parse circles, sliders and spinners with the same line syntax; see the three mode pages. Slider line: `x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample`. Spinner: `x,y,time,type,hitSound,endTime,hitSample`.

## Audio & images

- `[General] AudioFilename` = main audio (mp3/ogg/wav), `AudioLeadIn` ms of silence prepended.
- `PreviewTime` = preview start in ms (ROX maps -1 to 0 with `max(0)`).
- Background: `[Events]` `0,0,"bg.jpg",0,0`; video: `Video,<offset>,"v.mp4"`. ROX reads only `0,0,"file"` lines and keeps the LAST one (`parse_event` overwrites) as `background_file`. It ignores videos.
- Skin/storyboard images are referenced from `[Events]` / `.osb`. Hitsound samples live loose in the set folder.

### The `.osz` / `.osk` archive wrapper

- `.osz`: "an overall file archive, containing beatmaps and any additional resources such as skin or hitsounds" (osu-wiki `.osz (file format)`). It is a renamed ZIP holding all `.osu` files of the set, `.osb`, audio, images, videos and samples at its root or in sub-folders (storyboard paths are relative to the set folder). One `.osz` = one beatmap set (`BeatmapSetID`). Download endpoints: osu.ppy.sh/d/<setid>, mirrors. [ZIP nature of `.osz` is common knowledge and consistent with the wiki; the wiki page itself is a one-liner]
- `.osk`: "a file archive containing an osu! skin folder" (osu-wiki `.osk (file format)`); a ZIP of skin elements and `skin.ini`. Not a chart format; mania uses `skin.ini` `[Mania]` sections for key images and layout.
- Quaver (`.osz`, `.sm`, `.mcz` per the Quaver FAQ) and Malody also import `.osz`. ROX does not read archives; unzip first.

## Versions & variants

- `osu file format v14` is the latest osu!stable version (wiki). The ten original samples of this repository are v14 [observed in samples/]; the committed fixtures also include v4, v5, v6, v7, v9 and v10 files (`samples/ppy-osu_beatmap-version-4.osu`, `ppy-osu_mania-slider.osu` (v5), `ppy-osu_beatmap-version-6.osu`, `ppy-osu_controlpoint-difficulty-multiplier.osu` (v7), `ppy-osu_100374.osu` (v9), `ppy-osu_4869637.osu` (v10)), lazer's `v128` only inside `.olz` archives, and the `osu-file-parser_v3.osu` to `osu-file-parser_v14.osu` samples add v3 to v14 real files. lazer writes `osu file format v128` (`FIRST_LAZER_VERSION = 128`); from v128 on, object positions keep their decimals (below that lazer truncates to int).
- Versions v3 to v14 exist in the wild (the range supported by the `osu-file-parser` crate). Differences found in the sources consulted:

| Version | Difference | Source |
|---|---|---|
| <= 4 (3, 4) | +24 ms must be added to every time (timing points, hit objects, breaks, preview) | lazer `LegacyBeatmapDecoder` (`FormatVersion < 5`), osu-file-parser (`3..=4`) |
| 3 | `[TimingPoints]` lines may be just `time,beatLength` (meter 4, set normal, index 1, volume 100 assumed); slider `curvePoints` include the head point as first element, which is dropped; hit circle lines were written with a trailing comma | osu-file-parser (`timingpoints`, `hitobjects` modules) |
| 4 | timing points up to `time,beatLength,meter,sampleSet,sampleIndex` (no volume) | osu-file-parser |
| 5 | timing points up to `...,volume,uninherited` (no `effects`); first version without the 24 ms correction | osu-file-parser, lazer |
| <= 5 | `EditorBookmarks` / `EditorDistanceSpacing` stored in `[General]` | osu-file-parser |
| 6 | new stacking algorithm for osu!standard (`BeatmapVersion >= 6`); 8-field timing points | lazer `OsuBeatmapProcessor.ApplyStacking` |
| 8 | taiko slider->hit conversion and catch juice-stream tick distance stopped using the speed-adjusted beat length (details in the mode pages) | lazer `TaikoBeatmapConverter`, `CatchBeatmapConverter` |
| 10 | `[Editor] CurrentTime` exists only in this version | osu-file-parser |
| <= 13 | `AudioHash` still written | osu-file-parser |
| 14 | latest stable; no further structural change documented | wiki |
| 128 | lazer files, float positions | lazer encoder/decoder |

  Everything else (e.g. what changed between v9 and v12) is Unknown in the sources consulted. lazer and ROX both treat every field after `time,beatLength` as optional with the defaults above.
- Mode-specific dialects: see the three `others/osu-*` pages.
- The lazer encoder can write mania maps as `.osu` v128 (conversion of its internal model).
- lazer's `client.realm` is no chart format: it is lazer's Realm metadata database (`OsuGameBase.CLIENT_DATABASE_FILENAME = "client.realm"`, ppy/osu @ bb37f05). The `.osu` files are content-addressed under `files/` (`RealmFileStore`, `GetStoragePath`: `<hash[0]>/<hash[0..1]>/<hash>`). The lazer export of a set is an `.olz` (or a legacy `.osz`).

## Quirks & pitfalls

- No `Mode:` means osu!standard. ROX takes the mode from `[General]` only, the LAST `Mode:` wins, a malformed value counts as 0.
- `x` for mania is the column centre computed by the editor, but any `x` in a column's range is valid; do not round-trip `x` byte-exact.
- Hold `endTime` is inside `hitSample`: split `objectParams` on `,` first, then on `:`. The trailing `:` of `0:0:0:0:` leaves an empty `filename`.
- A missing `hitSample` defaults to `0:0:0:0:`; old files use shorter forms.
- ROX counts a note as tap whenever bit 7 is not set, even for a spinner or slider (ROX `OsuHitObject::is_hold`); mania maps contain none.
- Ranked maps contain out-of-order hit objects (a hand-edited file at osu.ppy.sh/s/594828 is cited in lazer); lazer stably sorts by `time`. ROX sorts by time after decoding (`sort_by_key`); validation requires sorted notes.
- First BPM point after the first note: ROX refuses it (`BpmAfterFirstNote`) unless `OsuDecodeOptions::re_arrange_bpm` is set, which moves the first BPM point to 1 us before the first note.
- Key count > 18 or < 1: stable/lazer clamp (1..18); the ROX u8 key count accepts up to 255 but `CircleSize` is cast with truncation.
- Cross-mode conversion (e.g. standard -> mania, `ManiaBeatmapConverter`) is a client feature; the file stays `Mode: 0`.

## Example

Truncated real excerpt (origin: sample `STARTails - ne! ne! ne! (TV Size) (dudehacker) [EZ].osu`, 7K, v14; the `[General]`/`[Difficulty]` keys shown are the ones the format needs):

```
osu file format v14

[General]
AudioFilename: audio.mp3
Mode: 3
[Difficulty]
CircleSize:7
OverallDifficulty:7
[TimingPoints]
429,352.941176470588,4,2,1,60,1,0
5899,-100,4,2,1,70,0,0
[HitObjects]
182,192,429,5,2,0:0:0:0:
475,192,781,1,12,0:0:0:0:
```

and a hold (origin: sample `HoneyWorks ... [Normal].osu`):

```
329,192,10536,128,0,11012:0:0:0:0:
```

7K, BPM = 60000/352.94 = 170.0. The first note is at 429 ms in column floor(182*7/512) = 2 (third column); the second at 781 ms in column floor(475*7/512) = 6. The hold at x=329 in a 4K or 7K map sits in column floor(329*K/512) and runs from 10536 ms to 11012 ms (476 ms).

## ROX support
Source: `src/formats/osu`, `auto/detect.rs`.
- `.osu` is auto-detected by extension; the mode is peeked from `[General]` (`OsuDecoder::peek_mode`). Mode != 3 gives `InvalidFormat("Not a mania beatmap (mode=N, expected 3)")`. Taiko (mode 1) decodes only through an explicit `TaikoDecoder`, see [../../../others/osu-taiko/osu/README.md](../../../others/osu-taiko/osu/README.md).
- Reads: `[General]` (`AudioFilename`, `AudioLeadIn` -> `audio_offset_us`, `PreviewTime`, `Mode`), `[Metadata]` (title/artist prefer the `*Unicode` variants; creator, version -> `difficulty_name`, source, tags, ids), `[Difficulty]` (`CircleSize` -> key count; `OverallDifficulty` -> `difficulty_value`), first background in `[Events]`, `[TimingPoints]`, `[HitObjects]`. Drops Editor, Colours, storyboard, breaks, kiai, effects, sample sets, `hitSound` flags and `SpecialStyle`.
- Writes mania `.osu` (`OsuEncoder`, column -> x via `column_to_x`); Burst and Mine notes are not representable (`RoxChart::remove_unsupported_notes`).
- Limits: 100 MiB per file; UTF-8 only (other code pages fail with "Invalid UTF-8").

## Parsers & tools

| Name | Language | URL |
|---|---|---|
| osu!lazer `LegacyBeatmapDecoder` (reference behaviour) | C# | https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/Formats/LegacyBeatmapDecoder.cs |
| osu-file-parser (versions 3-14, `.osb` support) | Rust | https://docs.rs/osu-file-parser |
| libosu | Rust | https://docs.rs/libosu |
| ROX `formats/osu` | Rust | vendored in this repo (`rhythm-open-exchange/src/formats/osu`) |
| osumap-parser | C | https://github.com/Gegel85/osumap-parser |
| osu-parser | C++ | https://github.com/HaselLoyance/osu-parser |
| osu_reader | C++ | https://github.com/ShaddyDC/osu_reader |
| osu-parser | C++ | https://github.com/ergrelet/osu-parser |
| Quaver.API converters (`.osu` -> `.qua`) | C# | https://github.com/Quaver/Quaver.API |
| Moonchart (`OsuMania`) | Haxe | https://github.com/MaybeMaru/moonchart |

(The four C/C++ parsers come from the repository's original README, "found via GitHub search"; they were not audited.)

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). osu!stable writes one `.osu` per difficulty into `Songs/<set>/` after extracting an `.osz` (osu! wiki). Every ranked/loved mania map on https://osu.ppy.sh/beatmaps (mode filter `mania`) downloads as an `.osz`; unzip it. osu!lazer keeps imported files content-addressed under `files/<first hash char>/<first two>/<sha256>` (`RealmFileStore`, `GetStoragePath`), indexed by `client.realm` (metadata and file names only). Best small fixture sets: the lazer test suite (`osu.Game.Rulesets.Mania.Tests/Resources/Testing/Beatmaps/`, `osu.Game.Tests/Resources/`) and rosu-map `resources/` (a copy of lazer's). Rate-changer tools write `.osz` variants.

## Sources

- https://github.com/ppy/osu-wiki/blob/master/wiki/Client/File_formats/osu_(file_format)/en.md (original README link; fetched raw)
- https://github.com/ppy/osu-wiki/tree/master/wiki/Client/File_formats (osz, osk, osb pages)
- https://github.com/ppy/osu-wiki/tree/master/wiki/Storyboard/Scripting (Objects, Commands, Compound_Commands, Audio, Variables)
- https://github.com/ppy/osu/blob/master/osu.Game/Beatmaps/Formats/LegacyBeatmapDecoder.cs, `LegacyDecoder.cs`, `Decoder.cs`
- https://github.com/ppy/osu/blob/master/osu.Game/Rulesets/Objects/Legacy/ConvertHitObjectParser.cs
- https://github.com/ppy/osu/blob/master/osu.Game.Rulesets.Mania/Beatmaps/ManiaBeatmapConverter.cs
- https://docs.rs/osu-file-parser/1.1.0/ (source pages of `osu_file::{general,editor,timingpoints,hitobjects,events}`)
- ROX source: `src/formats/osu/*`, `src/formats/auto/detect.rs`, `src/codec/validate.rs`
- Samples: [samples/](samples/) (10 files, all mode 3, v14)
