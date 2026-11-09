# Samples: Crypt of the NecroDancer custom music beat file (`<song>.mp3.txt`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-120bpm.ogg.txt` | hand-written from the official FAQ ("numbered list of numbers ... position of a beat, in seconds") and the output rule of Supinic/necrodancer-custom-music (`beats.join("\n")`) | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. 8 beats at a constant 120 BPM (0.5 s), one decimal number per line, LF; file name = audio file name + `.txt` |
| `synthetic-variable-tempo.ogg.txt` | hand-written from the same sources | OthersA | CC0 / public domain (hand-written for this repository) | synthetic. 8 beats with slightly drifting intervals (~0.51-0.52 s, i.e. a tempo-tracker-like output rather than a perfect grid), decimal seconds, LF |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `steam-forum_custom-music-test_beats.txt` | https://steamcommunity.com/app/247080/discussions/3/1471967615847881557/ | 2026-11-09 | 1cbc1b9385305b931046d535977302374a51073498b489c972d88b996e375a08 | Steam forum user (2017 thread "Custom Music Test") | forum post; no licence; accepted risk | real beat list pasted in the thread: comma-separated integers (milliseconds at ~173 BPM), single line, no trailing newline; extracted from the post text |
