# fluXis effects file (`.ffx`)
Kind: effects

Doc status: partial · ROX: no · Category: vsrg · Encoding: json (legacy text variant)

## Overview

`.ffx` is the **map effects/events file of fluXis**: a list of timed visual and gameplay events (flashes, pulses, shakes, shaders, playfield and camera transforms, lane switches, scroll multipliers, time offsets, note events...) that accompany a [`.fsc`](../fsc/README.md) difficulty. A `.fsc` references it by name in its `EffectFile` field; several difficulties of a set can share one `.ffx`. It is separate from the `.fsb` storyboard (sprites/shaders layered behind the playfield, not covered here). The Quaver importer emits `.ffx` files (`QuaverImport.cs` writes `<name>.ffx`).

## Packaged in

- Shipped in: `.fms` (zip of a fluXis mapset: `.fsc` difficulties, `.ffx` effects, audio, background, video, hitsounds).

## Container & encoding

- UTF-8 text, loaded by `MapEvents.Load<T>(content)`: if the trimmed content does **not** start with `{` it is parsed with the **legacy line format**; otherwise as JSON (Newtonsoft.Json) into the `MapEvents` class.
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

All event classes share `time` (double, ms), `lane` (int, editor lane) and `group` (string, omitted when null) from `ITimedObject`. Colours (`Color4`) and easings (osu!framework `Easing`) are serialised by Newtonsoft; their exact JSON form was not verified.

### Legacy text lines

Lines of the form `Type(arg,arg,...)`: `LaneSwitch(time,count[,duration])`, `Flash(time,duration,inBackground,easing,startColour,startOpacity,endColour,endOpacity)` (needs >= 8 args), `Pulse(time)`, `PlayfieldMove(time,offsetX,duration,easing)` (needs >= 4 args), and others handled in `MapEvents.loadLegacy`. Arguments split on `,` between the first `(` and the first `)`; numbers use the invariant culture. Unknown lines are ignored.

## Timing model

Every event has an absolute `time` in milliseconds and (for transitions) a `duration` in ms plus an easing; no beat/measure units.

## Notes

Not a note format: only `laneswitch` (changes how many lanes are visible), `scroll-multiply`, `time-offset` and `hitease` affect gameplay; the rest are visuals. `notes` are free-text markers.

## Audio & images

None (shaders and colours only).

## Versions & variants

- Legacy line-based `.ffx` (`LaneSwitch(...)`) and JSON `.ffx`.
- `hitfade`/`playfieldfade` -> `layerfade`; `PlayfieldRotateEvent` pitch/yaw are commented out.
- `playfield`/`subfield` indices address extra/dual playfields of the map (`extra-playfields`, `dual` in the `.fsc`).

## Quirks & pitfalls

- Content sniffing: any file not starting with `{` is parsed as legacy; a BOM or leading text breaks JSON detection. [inference]
- `lane` on events is an editor field, not gameplay lane.
- `scroll-multiply` targets scroll groups, not lanes (`groups`).

## Example

No sample in the repo; hand-built from the attributes above (illustrative):

```json
{
  "laneswitch": [ { "time": 20000, "lane": 0, "count": 5, "speed": 500, "easing": 0 } ],
  "shake": [ { "time": 30000, "lane": 0, "duration": 300, "magnitude": 10 } ]
}
```

## ROX support

Not read by ROX. Only `scroll-multiply`, `laneswitch` and `time-offset` have gameplay meaning; ROX would drop everything else.

## Parsers & tools

fluXis (C#): https://github.com/InventiveRhythm/fluXis (`fluXis/Map/MapEvents.cs`, `Map/Structures/Events/**`), built-in editor, converter `fluXis.Import.Quaver`.

## Getting samples

- **Committed** ([`samples/`](samples/), see [`SOURCES.md`](samples/SOURCES.md)): six real `.ffx` JSON effect files extracted from public fluXis mapsets (laneswitch, flash, shaders, playfield and camera events...), downloaded 2026-11-09.
- **How to get more**: unzip any mapset from `https://fluxis.flux.moe/api/mapsets/<id>/download`; the `.ffx` named by `EffectFile` in a `.fsc` is in the ZIP. The legacy line format was not seen in these sets.

## Sources

- https://github.com/InventiveRhythm/fluXis (commit `4187865461e9bf7d1b8201843b0a522229f87699`): `fluXis/Map/MapEvents.cs`, `fluXis/Map/Structures/Events/**`, `fluXis/Map/MapInfo.cs` (`GetMapEvents`), `fluXis/Map/MapStore.cs`, `fluXis.Import.Quaver/QuaverImport.cs`
