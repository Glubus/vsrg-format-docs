# osu! beatmap (`.osu`)
Kind: chart

Doc status: complete · ROX: reads/writes (mode 3 only; mode 1 taiko decode only, modes 0 and 2 refused) · Category: vsrg (for mode 3; the other modes live in `others/`) · Encoding: text

This is the canonical `.osu` document of this repository. The mode-specific pages
([osu!standard](../../../others/osu-standard/osu/README.md),
[osu!taiko](../../../others/osu-taiko/osu/README.md),
[osu!catch](../../../others/osu-catch/osu/README.md)) describe only what differs per mode and link back here.

## Overview

`.osu` is the beatmap file of osu! (by ppy / Dean "peppy" Herbert; the format version history below runs from v3 to v14 stable and v128 lazer). One `.osu` file is one difficulty of one game mode (`Mode:` in `[General]`: 0 standard, 1 taiko, 2 catch, 3 mania). Several `.osu` files, the audio, images, videos, an optional storyboard (`.osb`) and hitsound samples are bundled in a mapset archive (`.osz`, see below). The format is human readable and line based, and it is the most commonly imported chart format in this documentation set (Quaver's importer accepts `.osz`; Moonchart and ROX have `.osu` mania codecs; the Quaver.API repository ships osu! converters). osu!mania charts (`Mode: 3`) are the ones relevant to a vertical scrolling rhythm game. Files are found in the osu! `Songs/` folder (stable), in lazer's file store, and on osu.ppy.sh as `.osz` downloads. Editors: the official in-game editor (the `[Editor]` section stores its state) and third-party tools.

## Packaged in

- Packaged in [`osz`](../osz/).

## Container & encoding

- Plain text, UTF-8 (older files may carry a UTF-8 BOM; the full ROX parser does not strip it: a BOM-prefixed first line is simply not recognised as the version line and ignored, and `OsuDecoder::peek_mode` has a test with a BOM-prefixed file). Line endings `\n` or `\r\n` are both accepted (ROX strips a trailing `\r`).
- One file per difficulty. File name by convention `Artist - Title (Creator) [Version].osu` (the repository samples follow it).
- The first non-empty line is the magic `osu file format v<N>`. osu!lazer's `Decoder` looks at the first non-empty line, and if it starts with `osu file format v` it builds a decoder for version `N`, otherwise it falls back to a decoder of the latest version (osu source `Beatmaps/Formats/Decoder.cs`, `LegacyBeatmapDecoder.Register`).
- Section headers are `[Name]` on their own line. Lines starting with `//` are comments and are skipped; lazer also strips a trailing `// ...` from any line except in `[Metadata]` (titles may legitimately contain `//`) (osu source `LegacyDecoder.cs`: `ShouldSkipLine`, `StripComments`).
- Key/value sections use `Key: Value`; the line is split at the FIRST `:` and both sides are trimmed (`SplitKeyVal`). Real files mix `Key: Value` (`[General]`, `[Editor]`, `[Difficulty]` in some versions) and `Key:Value` (`[Metadata]`, `[Difficulty]`), see the samples.
- Unknown sections and unknown keys are ignored. Lines that fail to parse are logged and skipped by lazer (one bad line does not kill the file); ROX also logs and skips bad timing-point and hit-object lines.
- Whole-file limit in ROX: 100 MiB.

## Structure / metadata

Sections, in the order osu! writes them:

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

osu!lazer's `LegacyDecoder.Section` enum additionally lists `Fonts`, `CatchTheBeat` and `Mania`; these legacy section names are known to the decoder, but no keys of them are handled in the sources consulted. [inference: historical sections, never documented].

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

lazer additionally reads `SampleVolume` (default hit sample volume, default 100) from `[General]` (osu source `LegacyBeatmapDecoder.handleGeneral`); it is not in the wiki table. A missing `Mode` means 0: a file without `Mode:` is osu!standard (ROX `peek_mode` follows the same rule, and treats a non-numeric value as 0).

### `[Editor]`

`Bookmarks` (comma list of ms), `DistanceSpacing` (decimal), `BeatDivisor` (int, lazer clamps it to the editor's allowed range), `GridSize` (int), `TimelineZoom` (decimal). lazer also reads `VelocityPresets` (comma list of decimals). Editor-only, no gameplay effect. In versions <= 5 `Bookmarks` and `DistanceSpacing` were stored in `[General]` as `EditorBookmarks` / `EditorDistanceSpacing` (osu-file-parser, general/mod.rs: those two fields are only written when version <= 5). [third-party parser evidence]

### `[Metadata]`

`Title` (romanised), `TitleUnicode`, `Artist` (romanised), `ArtistUnicode`, `Creator`, `Version` (= difficulty name), `Source`, `Tags` (space separated), `BeatmapID` (difficulty id), `BeatmapSetID` (set id). IDs are 0 or -1 for unsubmitted maps (ROX copies them to `chart_id`/`chartset_id`; casts negative ids to u64 as-is, see ROX source `build_metadata`).

### `[Difficulty]`

| Key | Meaning |
|---|---|
| `HPDrainRate` | 0-10 |
| `CircleSize` | 0-10 for std/taiko/catch; for mania **the key count** (lazer clamps mania to 1..18: `MAX_MANIA_KEY_COUNT = 18`) |
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
| Video | `Video,startTime,"file.avi",xOffset,yOffset` (or `1,...`) | start time may be negative (sample: `Video,-608,"op.avi"`). lazer: if the extension is not a known video extension the event is treated as a background (very old maps misused `1`) |
| Break | `2,startTime,endTime` (or `Break,...`) | |
| Storyboard objects / samples | see below | |

The 4 storyboard layer headers appear as comments in real files (`//Storyboard Layer 0 (Background)` ... `//Storyboard Sound Samples`), so that editors can place lines.

#### Storyboard events (inside `[Events]`, or the `.osb` file)

Source: ppy/osu-wiki `Storyboard/Scripting/*`. An object declaration is followed by indented commands (one leading space or `_` per level).

```
Sprite,<layer>,<origin>,"<filepath>",<x>,<y>
Animation,<layer>,<origin>,"<filepath>",<x>,<y>,<frameCount>,<frameDelay>,<loopType>
Sample,<time>,<layer>,"<filepath>",<volume>
```

- `layer`: `Background`/0, `Fail`/1, `Pass`/2, `Foreground`/3 (the numeric form is used by `Sample`).
- `origin`: TopLeft 0, Centre 1, CentreLeft 2, TopRight 3, BottomCentre 4, TopCentre 5, Custom 6, CentreRight 7, BottomLeft 8, BottomRight 9. Coordinates are in a 640x480 space (widescreen storyboards extend it).
- `Animation`: frames are `name0.png`, `name1.png`... referenced as `name.png`; `loopType` `LoopForever` (default) or `LoopOnce`; `frameDelay` in ms.
- `Sample`: audio played at `time` ms on a layer (so it only plays in Pass or Fail state if the layer says so), `volume` 1-100 (default 100). Many mania maps use storyboard `Sample` lines as keysounds (see the sample `STARTails - ne! ne! ne! (TV Size) ... [EZ].osu`, which has ~80 `Sample,<ms>,0,"LR_Clap Fast Low.wav",70` lines).
- Commands: `<event>,<easing>,<start>,<end>,<params...>`, event letters `F` fade, `M` move, `MX`, `MY`, `S` scale, `V` vector scale, `R` rotate (radians), `C` colour (r,g,b), `P` parameter (`H` flip h, `V` flip v, `A` additive blend); compound `L,<start>,<loopCount>` (children prefixed by two levels, times relative to each iteration) and `T,<trigger>,<start>,<end>[,<group>]` (trigger types `HitSound[SampleSet][AdditionsSet][Addition][CustomSet]`, `Passing`, `Failing`). Easing 0-34 (0 linear, 1 out, 2 in, 3-5 quad, 6-8 cubic, 9-11 quart, 12-14 quint, 15-17 sine, 18-20 expo, 21-23 circ, 24-28 elastic, 29-31 back, 32-34 bounce). Shorthand: when end time is omitted/equal and end values omitted the start values are reused (`_F,0,1000,3000,1`).
- `[Variables]` (`$name=value`) are textual substitutions allowed only in `.osb` files.
- `.osb` is a separate optional file in the beatmap folder shared by all difficulties of the set; see [../osb/README.md](../osb/README.md).

## Timing model

`[TimingPoints]` lines: `time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects`. Sorted chronologically (required by the format; lazer re-sorts hit objects only).

| Field | Meaning |
|---|---|
| `time` | ms (decimal allowed) from the beginning of the audio; the section lasts until the next point |
| `beatLength` | uninherited: ms per beat (`BPM = 60000 / beatLength`). Inherited: **negative** value = `-100 / SV multiplier` (`-50` = 2.0x, `-100` = 1.0x, `-133.33` = 0.75x). lazer: a NaN beatLength on an inherited point disables slider ticks (edge case) |
| `meter` | beats per measure (inherited points ignore it); lazer treats a first char `0` as 4 |
| `sampleSet` | 0 beatmap default, 1 normal, 2 soft, 3 drum |
| `sampleIndex` | custom sample index; `0` = osu! default |
| `volume` | 0-100 |
| `uninherited` | `1` = timing (red) point, `0` = inherited (green) point |
| `effects` | bit 0 kiai, bit 3 omit first barline (taiko, mania) |

- Position -> time: all objects carry absolute ms times; no beat/measure arithmetic is needed to play a chart. Beats are only needed for editor snapping and slider length.
- An uninherited point resets the SV multiplier to 1; an inherited point at the same `time` as an uninherited one refines it (lazer queues same-time points and lets non-timing points override). Several points may share a `time`.
- osu!mania scroll speed: lazer maps the inherited-point multiplier to `EffectControlPoint.ScrollSpeed` for rulesets 1 (taiko) and 3 (mania) (`LegacyBeatmapDecoder.handleTimingPoint`). In mania the multiplier scales scroll speed only; hit timing is unaffected. `SliderMultiplier` has no effect on mania notes.
- ROX: uninherited points with `beatLength > 0` become `TimingPoint::Bpm { bpm = 60000/beatLength, signature = meter }`; inherited ones become `TimingPoint::Sv { scroll_speed = -100/beatLength }` (ROX source `OsuTimingPoint::bpm/scroll_velocity`). Time -> microseconds as `(time * 1000) as i64` (truncation).
- Time offset of old files: for format versions < 5, osu! applies a +24 ms correction to every time value (timing points, hit objects, breaks, non-negative preview time) (osu source `EARLY_VERSION_TIMING_OFFSET = 24`). ROX does NOT apply it.

Truncated example (real, from the sample file `HoneyWorks - Kikoemasu ka ... [Normal].osu`):

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
| `type` | bit flags: bit 0 hit circle, bit 1 slider, bit 2 new combo, bit 3 spinner, bits 4-6 combo colour skip, **bit 7 mania hold** |
| `hitSound` | bit flags: bit 0 normal (1), bit 1 whistle (2), bit 2 finish (4), bit 3 clap (8). No bit set = normal |
| `objectParams` | per type, below |
| `hitSample` | `normalSet:additionSet:index:volume:filename`, default `0:0:0:0:` |

Type decoding order in lazer is: circle (bit 0), then slider (bit 1), spinner (bit 3), hold (bit 7); the new-combo bit and the 3-bit skip are masked out first. Unknown type -> the line is rejected.

### osu!mania objects

- Key count `K` = `[Difficulty] CircleSize` (rounded; at least 1; lazer clamps to <= 18; ROX parses it as f32, defaults to 4 if unparseable, and casts to `u8` with truncation).
- **Column**: `column = floor(x * K / 512)`, clamped to `0 .. K-1` (wiki). ROX computes `(x * K) / 512` in integer arithmetic and does not clamp (`OsuHitObject::column`): an `x` >= 512 or negative would produce an invalid column, caught later by ROX validation (`InvalidColumn`). Standard mania x for the centre of column `i`: `floor((i + 0.5) * 512 / K)` (e.g. K=4: 64, 192, 320, 448; K=7: 36, 109, 182, 256, 329, 402, 475, see the samples).
- `y` is ignored; editors write 192.
- **Tap note** = hit circle: `type` 1 (5 if it also carries the new-combo bit, as in the sample first line `182,192,429,5,2,...`; the new-combo bit has no meaning in mania). No `objectParams`; `hitSample` follows `hitSound`.
- **Hold note (LN)** = `type` 128 (bit 7): `x,y,time,128,hitSound,endTime:hitSample`. `endTime` and the sample are joined by `:` instead of `,`, i.e. the hold's end time is the FIRST element of the colon-separated 6-part field `endTime:normalSet:additionSet:index:volume:filename`. Real example (sample `HoneyWorks ... [Normal].osu`): `329,192,10536,128,0,11012:0:0:0:0:`. If the field is missing lazer sets `endTime = startTime` (zero-length hold; do not rely on it). Combinations with other bits (e.g. 128 + 4 new combo = 132) occur in the wild; decode by testing bit 7.
- Sliders and spinners are not used in mania. ROX's hit-object parser reads only `x,time,type,hitSound` and the raw tail; any object without bit 7 is decoded as a tap in the column derived from `x`, so a stray slider/spinner line would become a tap (see Quirks).
- Simultaneous notes: any number of objects can share a `time`; two objects in the same column must not overlap (ROX validation `OverlappingNotes`: a note starting before the previous note in that column ended is an error).
- Hold semantics: no release timing is stored beyond `endTime`; `endTime` > `time` required (ROX `InvalidHoldDuration` for duration <= 0).

### Hitsounds / keysounds

- `hitSound` bit flags select which of the 4 samples play: normal, whistle, finish, clap (wiki). The sample file names are `<set>-hit<sound><index>.wav` with `set` in `normal|soft|drum` (`normalSet` for the normal sound, `additionSet` for the additions) and `index` omitted for 0/1; looked up in the beatmap folder (only if `index != 0`), then the skin, then the default resources (wiki).
- `hitSample`: `normalSet` / `additionSet` (0 none, 1 normal, 2 soft, 3 drum), `index` (0 = take the timing point's), `volume` (1-100, 0 = take the timing point's), `filename` (if present, ONLY that file in the beatmap folder is played and no additions).
- mania "keysound" maps use that `filename` field per note. Real example (sample `HoneyWorks ... [Normal].osu`): tap `256,192,11488,1,0,0:0:0:40:bell2.wav` (volume 40, custom file); hold `182,192,14345,128,0,15298:0:0:0:40:bell2.wav`.
- Effective volume/set: hit-object value if non-zero, else the timing point active at the object's end time (+5 ms leniency in lazer: `CONTROL_POINT_LENIENCY`).
- In every mode except mania the `LayeredHitSounds` skin option forces the normal sound; mania does not layer (wiki).
- Storyboard `Sample` lines (see Events) are the other way maps carry background hitsounds.
- ROX: for each note whose `filename` is not empty ROX creates one `Hitsound { file, volume }` per distinct filename and sets `hitsound_index`; `volume` 0 means `None`. Sets and `hitSound` flags are not preserved (ROX source `assign_hitsound`).

### Other modes (summary; details in `others/`)

Circles / sliders / spinners are all parsed for modes 0-2 and the same line syntax applies; see the three mode pages. Slider line: `x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample`. Spinner: `x,y,time,type,hitSound,endTime,hitSample`.

## Audio & images

- `[General] AudioFilename` = main audio (mp3/ogg/wav), `AudioLeadIn` ms of silence prepended.
- `PreviewTime` = preview start in ms (ROX maps -1 to 0 with `max(0)`).
- Background: `[Events]` `0,0,"bg.jpg",0,0`; video: `Video,<offset>,"v.mp4"`. ROX reads only `0,0,"file"` lines and keeps the LAST one (`parse_event` overwrites); that path becomes `background_file`. Videos are ignored.
- Skin/storyboard images are referenced from `[Events]` / `.osb`. Hitsound samples live loose in the set folder.

### The `.osz` / `.osk` archive wrapper

- `.osz`: "an overall file archive, containing beatmaps and any additional resources such as skin or hitsounds" (osu-wiki `.osz (file format)`). It is a ZIP file with the extension renamed: all `.osu` files of the set, `.osb`, audio, images, videos, samples at its root or in sub-folders (storyboard paths are relative to the set folder). One `.osz` = one beatmap set (`BeatmapSetID`). Download endpoints: osu.ppy.sh/d/<setid>, mirrors. [ZIP nature of `.osz` is common knowledge and consistent with the wiki; the wiki page itself is a one-liner]
- `.osk`: "a file archive containing an osu! skin folder" (osu-wiki `.osk (file format)`); a ZIP of skin elements and `skin.ini`. It is not a chart format; mentioned because mania uses `skin.ini` `[Mania]` sections for key images and layout.
- Other importers accept `.osz` too: Quaver (`.osz`, `.sm`, `.mcz` per the Quaver FAQ), Malody, etc. A ROX consumer must unzip an `.osz` first; ROX itself does not read archives.

## Versions & variants

- The first line states the version: `osu file format v14` is the latest osu!stable version (wiki). The ten original samples of this repository are v14 [observed in samples/]; the committed fixtures also include v4, v5, v6, v7, v9 and v10 files (`samples/ppy-osu_beatmap-version-4.osu`, `ppy-osu_mania-slider.osu` (v5), `ppy-osu_beatmap-version-6.osu`, `ppy-osu_controlpoint-difficulty-multiplier.osu` (v7), `ppy-osu_100374.osu` (v9), `ppy-osu_4869637.osu` (v10)), lazer's `v128` only inside [`.olz`](../olz/README.md) archives, and the `osu-file-parser_v3.osu` to `osu-file-parser_v14.osu` samples add v3 to v14 real files. osu!lazer writes `osu file format v128` (`FIRST_LAZER_VERSION = 128`); from v128 on, object positions keep their decimals (below that lazer truncates to int).
- Versions that exist in the wild: v3 to v14 (the range supported by the `osu-file-parser` crate). The differences found in the sources consulted:

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

  Everything not listed (e.g. what exactly changed between v9 and v12) is "Unknown" in the sources consulted; the tolerant approach used by both lazer and ROX is to treat every field after `time,beatLength` as optional with the defaults above.
- Mode-specific dialects: see the three `others/osu-*` pages.
- osu!lazer's `client.realm` is **not** a chart format: it is lazer's Realm metadata database (`OsuGameBase.CLIENT_DATABASE_FILENAME = "client.realm"`, ppy/osu @ bb37f05); the actual `.osu` files are content-addressed under `files/` (`RealmFileStore`, `GetStoragePath`: `<hash[0]>/<hash[0..1]>/<hash>`). The lazer export of a set is an [`.olz`](../olz/README.md) (or a legacy `.osz`).
- osu!lazer extras: the lazer encoder can write mania maps as `.osu` v128 (conversion of its internal model).

## Quirks & pitfalls

- A file with no `Mode:` is osu!standard, not mania. ROX decides the mode from `[General]` only, the LAST `Mode:` wins, and a malformed value counts as 0.
- `x` for mania is the column centre computed by the editor, but any `x` in a column's range is valid; do not round-trip `x` byte-exact.
- Hold `endTime` is inside `hitSample`: split `objectParams` on `,` first, then on `:`. The trailing `:` of `0:0:0:0:` leaves an empty `filename`.
- Missing `hitSample`: defaults to `0:0:0:0:`; short forms with fewer fields appear in old files.
- A note counts as tap in ROX whenever bit 7 is not set, even when the type is a spinner or slider (ROX `OsuHitObject::is_hold`); mania maps do not contain those.
- Out-of-order hit objects exist in ranked maps (a hand-edited file at osu.ppy.sh/s/594828 is cited in lazer); lazer stably sorts by `time`. ROX sorts by time after decoding (`sort_by_key`), validation requires sorted notes.
- First BPM point after the first note: ROX refuses it (`BpmAfterFirstNote`) unless `OsuDecodeOptions::re_arrange_bpm` is set; it then moves the first BPM point to 1 us before the first note.
- Timing: mania lazer keeps non-timing (green) point at the same `time` as a red point; two red points at the same `time` are legal but ambiguous.
- BOM / CRLF / mixed `Key: Value` spacing must all be tolerated; metadata may contain `:` and `//`.
- Key count > 18 or < 1: stable/lazer clamp (1..18); the ROX u8 key count accepts up to 255 but `CircleSize` is cast with truncation.
- Slider/spinner/circle conversion into other modes (e.g. standard -> mania conversion with pseudo-random patterns, `ManiaBeatmapConverter`) is a client feature and not part of the file format; converted maps are not stored in the `.osu` (the file stays `Mode: 0`).

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

Interpretation: 7K, BPM = 60000/352.94 = 170.0; first note at 429 ms in column floor(182*7/512) = 2 (third column); second at 781 ms in column floor(475*7/512) = 6; hold at x=329 in a 4K or 7K map: column floor(329*K/512), from 10536 ms to 11012 ms (476 ms).

## ROX support

Per ROX source `src/formats/osu` and `auto/detect.rs`:
- `.osu` is auto-detected by extension; mode is peeked from `[General]` (`OsuDecoder::peek_mode`) before the whole file is parsed. Mode != 3 -> `InvalidFormat("Not a mania beatmap (mode=N, expected 3)")`. Taiko (mode 1) is decodable only by calling `TaikoDecoder` explicitly, see [../../../others/osu-taiko/osu/README.md](../../../others/osu-taiko/osu/README.md).
- Reads: `[General]` (`AudioFilename`, `AudioLeadIn` -> `audio_offset_us`, `PreviewTime`, `Mode`), `[Metadata]` (title/artist prefer the `*Unicode` variants; creator, version -> `difficulty_name`, source, tags, ids), `[Difficulty]` (`CircleSize` -> key count; `OverallDifficulty` -> `difficulty_value`), first background in `[Events]`, `[TimingPoints]`, `[HitObjects]`. Everything else (Editor, Colours, storyboard, breaks, kiai, effects, sample sets, `hitSound` flags, `SpecialStyle`) is dropped.
- Writes: `OsuEncoder` emits mania `.osu` (column -> x via `column_to_x`); Burst and Mine notes are not representable (`RoxChart::remove_unsupported_notes`).
- Limits: 100 MiB per file; UTF-8 only (non-UTF-8 files are rejected with "Invalid UTF-8", even though old maps may use other code pages).

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

(The four C/C++ parsers are the ones listed in the repository's original README, "found via GitHub search"; they were not audited.)

## Getting samples

- **Committed** in [`samples/`](samples/) (see [`samples/SOURCES.md`](samples/SOURCES.md)): the 10 community maps already present (origin unknown) plus 48 files with known origin and licence: lazer's mania test maps (1K-18K, `SpecialStyle:1`, v4/v5/v6/v7/v9/v10 old versions, SV 0.01x, spinner-as-hold, hitsound sample banks; MIT), Quaver.API's osu!->Quaver conversion inputs (7K keysound maps, CRLF, a 9245-timing-point map; MPL-2.0), Prelude's replay-parity maps (MIT) and three hand-written Beatmap Lens fixtures (MIT) including a deliberately malformed UTF-8-BOM file.
- **Also committed**: 16 real files of the osu-file-parser test suite (`osu-file-parser_*.osu`), covering every format version v3 to v14 (including the `v13`/`v14` mania maps and `v9_spaces`); upstream has no LICENSE file.
- **How to get more**: osu!stable writes one `.osu` per difficulty into `Songs/<set>/` after extracting an `.osz` (osu! wiki, see [osz](../osz/README.md)); every ranked/loved mania map on https://osu.ppy.sh/beatmaps (mode filter `mania`) downloads as an `.osz`, and unzipping it (ZIP) gives the `.osu`. osu!lazer keeps imported files content-addressed under `files/<first hash char>/<first two>/<sha256>` (`RealmFileStore`, `GetStoragePath`), indexed by `client.realm`: that Realm database is **not** a chart format, it only stores metadata and file names (`OsuGameBase.CLIENT_DATABASE_FILENAME = "client.realm"`, ppy/osu @ bb37f05). The osu!lazer test suite (`osu.Game.Rulesets.Mania.Tests/Resources/Testing/Beatmaps/`, `osu.Game.Tests/Resources/`) and the rosu-map `resources/` folder (a copy of lazer's) are the best small fixture sets. Rate-changer tools write `.osz` variants (the Prelude mapsets here are such rates).

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
