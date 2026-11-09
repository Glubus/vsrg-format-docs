# GITADORA / GuitarFreaks & DrumMania (Konami arcade)

Konami's GuitarFreaks (guitar/bass controller: 3 then 5 fret buttons + pick + wail) and DrumMania (drum kit pads) series, merged under the name GuitarFreaks & DrumMania XG then GITADORA. Notes fall vertically on fixed lanes (drum: hi-hat, snare, bass, high tom, low tom, right cymbal, left cymbal, floor tom, left pedal; guitar/bass: R G B Y P + open): **vsrg**. Arcade charts are binary "sequence" files extracted from game data (Konami IFS archives); no official documentation. The public knowledge below comes from the open-source conversion project `fisyher/gitadora-customs` (plugin sources) which converts them to DTX ([DTXMania](../dtxmania/README.md)) and back.

| Folder | File | Role |
|---|---|---|
| [sq3/](sq3/README.md) | `.sq3` | GITADORA-era sequence archive (`SEQP` / `SQ3T`), 64-byte events |
| [sq2/](sq2/README.md) | `.sq2` | GuitarFreaks/DrumMania V-series/XG-era sequence, 16-byte events |
| [dsq/](dsq/README.md) | `.dsq`, `.gsq` (+ `.dsq0`..`.dsq2`, `.gsq1`..`.gsq3` variants of earlier games) | older drum/guitar sequence formats (stub) |

Other tools: RAintN22/gitadora-tools (creates/converts `.dsq`, `.sq2`, `.sq3` and `.dtx`; releases only seen), DTXMania (reads converted DTX), GDAmania blog (GDA/DTX conversions: http://gdamania.blogspot.com/). No source confirms a `.xg` extension (Unknown).
