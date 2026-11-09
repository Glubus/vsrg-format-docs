# jubeat

Konami arcade rhythm game (2008-): a **4×4 grid of 16 backlit touch panels**; notes ("markers") appear on a panel, animate for a fixed time, and must be tapped when the animation completes; long notes show a bar from one panel to a neighbour and require holding until released at the bar tip. The same series spawned `jubeat plus` (iOS/Android), `jukebeat`, and a large simulator/community scene (jubeat analyser, F.E.I.S, jujube, youbeat).

**Category: others** — a 4×4 grid (position = panel 0–15, not a column), no scrolling lanes, a note's "approach" is an in-place animation. ROX could map the 16 panels to 16 columns but it is not a scrolling-lane game.

## Formats

| Folder | Format | Notes |
|---|---|---|
| [eve/](eve/README.md) | `.eve` official text events (300 Hz ticks) | arcade charts, `time,command,value` |
| [jbsq/](jbsq/README.md) | `.jbsq` binary sequence (also `.ijbq`/`.ijsq` magics) | game-side compiled form of the same events (iOS/Android/`jubeat` Android port and later arcade versions) |
| [memo/](memo/README.md) | jubeat analyser text charts (`#memo`, `#memo1`, `#memo2`, `#boogie`, mono-column 1列形式, youbeat/yubiosi) | Japanese fan "memo" format read by Jubeat Analyser |
| [memon/](memon/README.md) | `.memon` JSON (Stepland) | modern fan format with JSON schema |

Also: iOS/Android package files `.jbt` / `.orb` / `.rb` (zip with Blowfish-encrypted entries, seq files = the same eve-like data per difficulty; see the Reflec Beat page), Malody Pad mode, and jubeatools (converter hub).

## Links

- jubeatools (eve, jbsq, malody, memon, memo, youbeat, boogie converters): <https://github.com/Stepland/jubeatools> (moved to <https://gitlab.com/Buggyroom/jubeatools>), docs <https://jubeatools.readthedocs.io>
- memon spec: <https://github.com/Stepland/memon>, docs <https://memon-spec.readthedocs.io>
- jubeat analyser (original tool): usage notes at <https://yuisin.com/jubeat/analyser/jubeatmemo_use.html>
