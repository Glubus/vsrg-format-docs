# Rhythm Doctor level (`.rdlevel`)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: json

## Overview

`.rdlevel` is the level file of Rhythm Doctor (7th Beat Games), JSON-like text written by the in-game editor (RDLE) with hundreds of event types (sound, rows/beats, VFX, camera, decorations, rooms, windows). This page covers the container, common event fields, timing and the rhythm-relevant events. The full per-event field list is in the community schema (`rd-schema`, `level.d.ts`, ~2400 lines) and on the wiki ("Surgery" section of each event page).

## Packaged in

- Shipped in: `.rdzip` (zip of an `.rdlevel` plus its audio and sprites).

## Container & encoding

- Tab-indented text, not strictly valid JSON: the real sample has trailing commas before `]` / `}` (`{ ... },\n\t],`). Parsers must tolerate them (RhythmBase, rd-schema users in VS Code use a JSON-with-comments mode). Field order is stable but not required.
- UTF-8 (the sample has Chinese strings) [BOM handling not confirmed for rdlevel; Unknown].
- One file = one level; it may reference audio, sprites, a second 2-player level (`separate2PLevelFilename`) or, via the "Go to Level" event (v1.2.0), other `.rdlevel` files.

## Structure / metadata
Top-level object (rd-schema `Level`): `$schema?`, `settings`, `rows[]`, `decorations[]`, `events[]`, `conditionals[]`, `bookmarks[]`, `colorPalette[]`. The sample has `"settings"`, `"rows"`, `"decorations"`, `"events"`, `"conditionals"`.

### `settings` (rd-schema `Settings`, sample `version` 51)
`version` (number, required), `artist`, `song`, `specialArtistType` (None|AuthorIsArtist|PublicLicense), `artistPermission`, `artistLinks`, `author`, `difficulty` (Easy|Medium|Tough|VeryTough), `seizureWarning`, `previewImage`, `syringeIcon`, `previewSong`, `previewSongStartTime`, `previewSongDuration`, `songNameHue`, `songLabelGrayscale`, `description`, `tags`, `separate2PLevelFilename`, `canBePlayedOn` (OnePlayerOnly|TwoPlayerOnly|BothModes), `firstBeatBehavior` (RunNormally|RunEventsOnPrebar), `customClass`, `inkFile`, `multiplayerAppearance` (HorizontalStrips|Nothing), `levelVolume`, `rankMaxMistakes[]` (4 numbers in the sample: 20, 15, 10, 5), `mods`, `rankDescription[]` (6 strings in the sample).

### `rows[]` (`Row`)
`row` (index, number), `character` (e.g. `HoodieBoy`, `Samurai`), `rowType` (`Classic` | `Oneshot`), `player` (P1|P2|CPU), `rooms[]`, `pulseSound` (`Kick`, ...), `pulseSoundVolume`, `pulseSoundPitch`, `pulseSoundPan`, `pulseSoundOffset`, plus `tag`, `runTag`, `active`, `if`, `cpuMarker`, `hideAtStart`, `rowToMimic`, `muteBeats`, `muteIn1P`, `length`.

### `events[]` common fields
`bar` (1-based integer), `beat` (1-based float within the bar; absent on a few events: Play Song, Set Crotchets Per Bar, Set Heart Explode Volume), `y` (editor timeline row; for row events it must equal `row`), `type` (event name), `if` (condition expression), `tag`, `runTag`, `active`, `rooms[]`.

### Rhythm-relevant events
| `type` | Fields | Meaning |
|---|---|---|
| `PlaySong` | `filename`, `volume`, `pitch`, `pan`, `offset` (ms), `bpm`, `loop` (rd-schema also has a nested `song` Sound object) | Starts the music and sets the initial BPM |
| `SetBeatsPerMinute` | `beatsPerMinute` | BPM change at a bar/beat |
| `SetCrotchetsPerBar` | `crotchetsPerBar`, `visualBeatMultiplier` | Beats per bar (time signature); example value 8 |
| `SetRowXs` (Set Beat Modifiers) | `row`, `pattern` (6 chars, `x` or `-`, e.g. `-xx-xx`, `-x-x-x`, `------`), `syncoBeat`, `syncoSwing`, `syncoVolume`, `syncoPitch`, `syncoStyle` (Chirp|Beep), `syncoPlayModifierSound`, `syncoPlayModifierOffSound` | Which of the 6 pulses carry the "x" |
| `AddClassicBeat` | `row`, `tick`, `swing`, `hold`, `setXs` (NoChange|ThreeBeat|FourBeat, wiki; rd-schema ThreeBeat|FourBeat), `length`, `sound`, `legacy` | A classic 7-pulse beat: `tick` is the spacing between pulses (default 1 = pulses on each beat, hit on the 7th); `swing` delays pulses 2/4/6, 0..2*tick; `hold` hold time |
| `AddFreeTimeBeat` | `row`, `pulse`, `hold` | Free-time beat (player-timed rows) |
| `PulseFreeTimeBeat` | `row`, `action` (Increment|Decrement|Custom|Remove), `customPulse`, `hold` | Free-time pulse control |
| `AddOneshotBeat` | `row`, `pulseType` (Wave|Square|Heart|Triangle), `freezeBurnMode` (Freezeshot|Burnshot), `interval`, `tick`, `delay`, `loops`, `subdivisions`, `subdivSound`, `skipshot`, `hold`, `holdCue` (Auto|Early|Late), `subdivTickOverride`, `sound`, `squareSound` | Oneshot rows (cue + shot) |
| `SetOneshotWave` | `row`, `waveType` (BoomAndRush|Ball|Spring|Spike|SpikeHuge|Single), `height`, `width`, `wobble` | Oneshot wave shape |
| `PlaySound`, `SetClapSounds`, `SetCountingSound`, `SayReadyGetSetGo`, ... | | Sound events |

Other tabs (theme, VFX preset, background, camera, rows, rooms, windows, decorations, dialogue) are visual events; see `rd-schema` and the wiki list.

Other top-level arrays: `decorations[]` (Sprite `{row, filename, ...}` or Text `{type:"Text", decoName, font, ...}`), `conditionals[]` (Language, PlayerMode, Accessibility, Narration, LastHit, Custom, TimesExecuted, each with `name`, `id`), `bookmarks[]` (`{bar, beat, color}`), `colorPalette[]` (color strings).

## Timing model

- Position = (bar, beat), both 1-based; the level starts at bar 1 beat 1. `beat` is a float (e.g. 3.5).
- Bar length = current `crotchetsPerBar` (`SetCrotchetsPerBar`, wiki example 8). Absolute beat index = sum of CPB of previous bars + (beat - 1). RhythmBase's `TickTime` models this as `Tick` counted from 1 plus bar/beat/time/BPM/CPB.
- BPM: `PlaySong.bpm` initial, `SetBeatsPerMinute.beatsPerMinute` changes it. Seconds = integral of 60/BPM over beats. `PlaySong.offset` (ms) shifts the audio vs. the beat grid; the song starts at the `PlaySong` event [semantics inferred from field names].
- A classic beat at (bar, beat) makes 7 pulses spaced by `tick` beats (default 1; 6 sub-pulses + the player-hit 7th), shaped by `swing` and the row's `SetRowXs` pattern. Bars shorter than 600 ms can break playback (wiki).
- No scroll speed; `SetSpeed` is a visual/playback event.

## Notes

Notes are rows: Classic (pulse trains hit on the 7th beat; optional `hold`), Free-time (player-timed) and Oneshot (cue/shot with intervals and subdivisions). Rows are indexed `row` 0..n, up to 2 players in co-op (`player` P1/P2/CPU). `hold` and `AddOneshotBeat.hold` are held beats; no mines. A column-model conversion maps each row beat to one hit at the 7th pulse (lossy).

## Audio & images

Audio via `PlaySong.filename`, `PlaySound`/`sound` objects `{filename, volume, pitch, pan, offset}`; sprites by `Sprite.filename`/`character`; preview image and syringe icon in settings. Files sit next to the `.rdlevel` (inside the `.rdzip` when packaged).

## Versions & variants

`settings.version` is the editor/format version (sample 51). Each wiki event page has an "Origin" (`r1`, `r<version>`) giving the version it appeared in. Updates add events (v1.2.0 "Go to Level", custom fonts). RhythmBase adapts versions. Older levels use legacy fields (`legacy` flags).

## Quirks & pitfalls

- Trailing commas; lenient parser required.
- Events that omit `beat` act on the bar start.
- Row events: `y` must equal `row`.
- `SetRowXs` patterns have 6 chars; the 7th pulse is the hit.
- Preserve inactive events (`active: false`) and unknown event types.
- Dialogue strings can contain markup.

## Example
From a real level (https://git.186526.xyz/7bg/rd-because-u-r-here, `main.rdlevel`, events cut to a few lines):
```
{ "bar": 1, "beat": 1, "y": 0, "type": "PlaySong", "filename": "urhere.ogg", "volume": 69, "pitch": 100, "pan": 0, "offset": 21, "bpm": 150, "loop": false },
{ "bar": 1, "beat": 1, "y": 1, "type": "SetRowXs", "row": 1, "pattern": "-xx-xx" },
{ "bar": 1, "beat": 1, "y": 1, "type": "AddClassicBeat", "row": 1, "tick": 0.3333333, "swing": 0, "hold": 0 },
{ "bar": 1, "beat": 5, "y": 1, "type": "AddClassicBeat", "row": 1, "tick": 0.5, "swing": 0, "hold": 0 },
```

## ROX support
Not read by ROX.

## Parsers & tools
- RhythmBase (C#, .NET): https://github.com/RDCN-Community-Developers/RhythmToolkit (reads `.rdlevel`, `.rdzip`, time parsing)
- rd-schema (JSON schemas / TS types): https://github.com/0f-0b/rd-schema
- RDLE standalone editor: https://giacomopc.itch.io/rdle
- Datasette of the Rhythm Cafe level DB (7,433 levels listed): https://datasette.rhythm.cafe/

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md). More: the Rhythm Cafe database (https://datasette.rhythm.cafe/) has a JSON API (`https://datasette.rhythm.cafe/rdlevels.json?sql=...`, observed 2026-11-09) with an `rdzip_url` per level; the in-game Level Editor (https://wiki.rhythm.cafe/page/Level_Editor) exports `.rdzip` (File -> Export).

## Sources
- https://wiki.rhythm.cafe/page/Level_Editor
- https://wiki.rhythm.cafe/page/Add_Classic_Beat
- https://wiki.rhythm.cafe/page/Set_Crotchets_Per_Bar
- https://wiki.rhythm.cafe/page/Set_Beats_Per_Minute
- https://github.com/0f-0b/rd-schema (level.d.ts)
- https://raw.githubusercontent.com/RDCN-Community-Developers/RhythmToolkit/master/docs/Tutorial.md
- https://github.com/RDCN-Community-Developers/RhythmToolkit
- https://git.186526.xyz/7bg/rd-because-u-r-here/raw/commit/c5a0a92fee8b3beedad3c57eb521e84a9a5d3d97/main.rdlevel
- https://store.steampowered.com/news/app/774181/view/692021394394843070
- https://en.wikipedia.org/wiki/Rhythm_Doctor
