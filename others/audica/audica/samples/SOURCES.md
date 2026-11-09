# Samples: Audica map package (`.audica`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `audicaconv-template_expert.cues` | https://github.com/octoberU/AudicaConverter/blob/77532a7f906354610f5d18cfb592c95f306039b7/template.audica (member `expert.cues`) | octoberU (desc `author: octo`) | MIT (repo LICENSE.md, "Copyright (c) 2020 ...") | real expert cue list extracted from the zip: 571 cues (hand types 0/1/2: 32/265/274; behaviors 0..6), tick/tickLength/pitch/velocity/gridOffset/zOffset/handType/behavior, plus a root `NRCueData` object (version 1, `pathBuilderNoteCues` with behavior 101) written by a mod; 4-space JSON indentation |
| `audicaconv-template_song.desc` | https://github.com/octoberU/AudicaConverter/blob/77532a7f906354610f5d18cfb592c95f306039b7/template.audica (member `song.desc`) | octoberU (desc `author: octo`) | MIT (repo LICENSE.md, "Copyright (c) 2020 ...") | single-line JSON `song.desc`: songID, mogg file names, title, artist, midiFile, fusion paths, `tempo` 150.0, `prerollSeconds`, `useMidiForCues` false, `author`, `offset`, `previewStartSeconds`, `bookmarks` |
| `audicaconv-template_song.mid` | https://github.com/octoberU/AudicaConverter/blob/77532a7f906354610f5d18cfb592c95f306039b7/template.audica (member `song.mid`) | octoberU (desc `author: octo`) | MIT (repo LICENSE.md, "Copyright (c) 2020 ...") | 57-byte Standard MIDI File (format 0, 1 track, 480 ticks/quarter): tempo meta event 384615 us/quarter (156 BPM) and 4/4 time signature at tick 0, repeated 994 ticks later; no notes (while song.desc says `tempo` 150.0) |
| `audicaconv-template_song.moggsong` | https://github.com/octoberU/AudicaConverter/blob/77532a7f906354610f5d18cfb592c95f306039b7/template.audica (member `song.moggsong`) | octoberU (desc `author: octo`) | MIT (repo LICENSE.md, "Copyright (c) 2020 ...") | S-expression text pointing at song.mogg / song.mid with mix/pan/vol (the audio itself is not committed) |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `audicaconv_template.audica` | https://raw.githubusercontent.com/octoberU/AudicaConverter/77532a7f906354610f5d18cfb592c95f306039b7/template.audica | MIT repo (octoberU/AudicaConverter) but the package embeds a 1.6 MB song.mogg of a commercial song, so not committed (chart members are committed extracted) | Complete `.audica` zip: song.desc, expert.cues, song.mid, 3 .moggsong, song.mogg, song_extras.mogg (1811162 bytes) |
