# Samples: FFR legacy level SWF

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| synthetic-level.swf | Hand-written for this repository (synthetic), built from the fiche (FWS v6, uncompressed, 412 bytes: header, DoAction, ShowFrame, End; no audio) | the repository author (public domain / CC0 1.0) | CC0 1.0 | `_root.beatBox` array of 15 beats [frame, direction, colour(, ms)]: 4 directions, colours red, blue, purple, yellow, pink, orange, green, white, three entries with the 4th ms element. Checked by a Python port of rCubed `Beatbox.parseBeatbox`, not by Flash |
