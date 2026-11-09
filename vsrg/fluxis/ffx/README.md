# fluXis effects file (`.ffx`)
Kind: effects

Doc status: partial · ROX: no · Category: vsrg · Encoding: json (legacy text variant)

## Overview

Map effects/events file of fluXis: timed flashes, pulses, shakes, shaders, playfield and camera transforms, lane switches, scroll multipliers, time offsets and note events for a [`.fsc`](../fsc/README.md) difficulty. A `.fsc` names it in `EffectFile`; several difficulties can share one `.ffx`. The `.fsb` storyboard is separate and not covered. The Quaver importer writes `<name>.ffx` (`QuaverImport.cs`).

## Packaged in

- Shipped in: `.fms` (zip of a fluXis mapset: `.fsc` difficulties, `.ffx` effects, audio, background, video, hitsounds).

## Container & encoding

- UTF-8 text, loaded by `MapEvents.Load<T>(content)`: if the trimmed content does not start with `{` it is parsed with the legacy line format; otherwise as JSON (Newtonsoft.Json) into the `MapEvents` class.
- The game generates `<unix timestamp>.ffx` file names for new effect files (`MapStore.cs`).
- A hash of the text content (`MapUtils.GetHash`) is stored as `EffectHash`.

## Structure / metadata

### JSON layout

Top-level object, one array per event type; every array item is an event object. Keys (`MapEvents` `[JsonProperty]` names):

| Key | Event class | Notes |
|---|---|---|
| `laneswitch` | `LaneSwitchEvent` | `count` (int, new visible key count, default 1), `speed` (duration, ms), `easing` (default OutQuint). |
| `flash` | `FlashEvent` | `duration`, `background` (bool), `ease`, `start-color`, `start-alpha` (default 1), `end-color`, `end-alpha`. |
| `colorfade` | `ColorFadeEvent` | `fade-primary`/`primary`, `fade-secondary`/`secondary`, `fade-middle`/`middle` (colours), `duration`, `ease`, `playfield`, `subfield`. |
| `pulse` | `PulseEvent` | `width` (default 32), `duration`, `in-percent`, `easing` (default Out). |
| `playfieldmove` | `PlayfieldMoveEvent` | `x`, `y`, `z`, `duration`, `ease` (default OutQuint), `playfield`, `subfield`. |
| `playfieldscale` | `PlayfieldScaleEvent` | `x`, `y` (default 1), `duration`, `ease`, `playfield`, `subfield`. |
| `playfieldrotate` | `PlayfieldRotateEvent` | `roll`, `duration`, `ease`, `playfield`, `subfield` (pitch/yaw commented out in source). |
| `hitease` | `HitObjectEaseEvent` | `ease`. |
| `layerfade` | `LayerFadeEvent` | `duration`, `alpha` (default 1), `ease`, `layer` (enum `HitObjects`, `Stage`, `Receptors`, `Playfield`, `HUD`), `playfield`, `subfield`. Replaces the legacy `hitfade` and `playfieldfade` arrays (still read). |
| `shake` | `ShakeEvent` | `duration`, `magnitude` (default 10). |
| `shader` | `ShaderEvent` | `shader` (type: Bloom, Greyscale, Invert, Chromatic, Mosaic, Noise, Vignette, Retro, HueShift, Glitch, SplitScreen, ...), `duration`, `ease`, `use-start`, `start-params`, `end-params`, `params` with `strength`, `strength2`, `strength3`. |
| `beatpulse` | `BeatPulseEvent` | `strength` (default 1.05), `zoom` (default 0.25), `interval` (default 1). |
| `scroll-multiply` | `ScrollMultiplierEvent` | `duration`, `multiplier` (default 1), `ease`, `groups` (list of scroll-group ids). |
| `time-offset` | `TimeOffsetEvent` | `duration`, `use-start`, `start-offset`, `offset`, `ease` (shifts hit timing during the map). |
| `camera-move` | `CameraMoveEvent` | `x`, `y`, `duration`, `ease`. |
| `camera-scale` | `CameraScaleEvent` | `scale` (default 1), `duration`, `ease`. |
| `camera-rotate` | `CameraRotateEvent` | `roll`, `duration`, `ease`. |
| `loops` | `LoopEvent` | `target` (group), `distance`, `count`: repeats a group of events. |
| `notes` | `NoteEvent` | `content` (text note shown/used as a marker). |

All event classes share `time` (double, ms), `lane` (int, editor lane) and `group` (string, omitted when null) from `ITimedObject`. Colours (`Color4`) and easings (osu!framework `Easing`) are serialised by Newtonsoft; their JSON form was not verified.

### Legacy text lines

Lines of the form `Type(arg,arg,...)`: `LaneSwitch(time,count[,duration])`, `Flash(time,duration,inBackground,easing,startColour,startOpacity,endColour,endOpacity)` (needs >= 8 args), `Pulse(time)`, `PlayfieldMove(time,offsetX,duration,easing)` (needs >= 4 args), and others handled in `MapEvents.loadLegacy`. Arguments split on `,` between the first `(` and the first `)`; numbers use the invariant culture. Unknown lines are ignored.

## Timing model

Absolute `time` in ms; transitions add `duration` (ms) and an easing. No beats.

## Notes

Not a note format. Only `laneswitch` (visible lane count), `scroll-multiply`, `time-offset` and `hitease` affect gameplay; the rest is visual. `notes` are free-text markers.

## Audio & images

Unknown.

## Versions & variants

- Legacy line-based `.ffx` and JSON `.ffx`.
- `hitfade`/`playfieldfade` became `layerfade`.
- `playfield`/`subfield` indices address extra/dual playfields (`extra-playfields`, `dual` in the `.fsc`).

## Quirks & pitfalls

- Any file not starting with `{` is parsed as legacy; a BOM or leading text breaks JSON detection. [inference]
- `lane` on events is an editor field, not a gameplay lane.
- `scroll-multiply` targets scroll groups (`groups`), not lanes.

## Example

Hand-built from the attributes above (illustrative):

```json
{
  "laneswitch": [ { "time": 20000, "lane": 0, "count": 5, "speed": 500, "easing": 0 } ],
  "shake": [ { "time": 30000, "lane": 0, "duration": 300, "magnitude": 10 } ]
}
```

## ROX support

Not read by ROX. Only `scroll-multiply`, `laneswitch` and `time-offset` have gameplay meaning; ROX would drop the rest.

## Parsers & tools

fluXis (C#): https://github.com/InventiveRhythm/fluXis (`fluXis/Map/MapEvents.cs`, `Map/Structures/Events/**`), built-in editor, converter `fluXis.Import.Quaver`.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). More: unzip any mapset from `https://fluxis.flux.moe/api/mapsets/<id>/download`; the `.ffx` named by `EffectFile` in a `.fsc` is inside. The legacy line format was not seen in these sets.

## Sources

- https://github.com/InventiveRhythm/fluXis (commit `4187865461e9bf7d1b8201843b0a522229f87699`): `fluXis/Map/MapEvents.cs`, `fluXis/Map/Structures/Events/**`, `fluXis/Map/MapInfo.cs` (`GetMapEvents`), `fluXis/Map/MapStore.cs`, `fluXis.Import.Quaver/QuaverImport.cs`
