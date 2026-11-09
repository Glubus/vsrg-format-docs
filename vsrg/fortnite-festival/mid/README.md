# Fortnite Festival chart MIDI (`.mid`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (MIDI; encrypted in the game data)

## Overview
Jam Tracks ship their charts as MIDI files that are **encrypted** in the game's download data; community tools (Festival-MIDI-Extractor, the "Fortnite Festival from the Outside" launcher project) decrypt them. Harmonix (Rock Band) authored the game, and the layout resembles the Rock Band/Clone Hero MIDI layout ([clone-hero/mid](../../clone-hero/mid/README.md)). Encryption scheme and exact track names: Unknown here (not documented in the sources consulted).

## Container & encoding
Standard MIDI File after decryption; encryption: Unknown.

## Structure / metadata
Per the dromzeh.dev write-up: instrument tracks with four difficulty tiers by MIDI note range: Easy 60-63 (4 frets), Medium 72-75 (4 frets), Hard 84-87 (4 frets), Expert 96-100 (5 frets). Fret index 0-4 = green to orange. Note 116 marks overdrive phrases (note on/off = phrase). Base+6..base+10 within a difficulty octave are **lift** notes. Notes sharing a tick form a chord. A `SECTION` track holds named song sections. Flags derived by the parser: tap, overdrive, lift, chord.

## Timing model
MIDI ticks with tempo map; sustain = note length, kept in ticks, ms and beats by the parser.

## Notes
5 lanes (Expert) / 4 lanes (lower), sustains, lifts, chords, taps, overdrive. Plastic-guitar charts (Pro Lead / Pro Bass, with HOPOs) exist as separate tracks [per the engadget/X reports: "Rock Band 5 in every way but name"].

## Audio & images
Stems are separate game assets. Unknown here.

## Versions & variants
Unknown.

## Quirks & pitfalls
Charts are encrypted; legality of extraction is the user's responsibility.

## Example
None.

## ROX support
Not read by ROX.

## Parsers & tools
Festival-MIDI-Extractor: https://github.com/yotolo2354/Festival-MIDI-Extractor

## Getting samples
- Committed: none. Manifest: none. The charts are Epic/Harmonix assets encrypted in the game data, so no licence permits redistribution and no public sample exists.
- How to get one: the Festival-MIDI-Extractor GUI (MIT, https://github.com/yotolo2354/Festival-MIDI-Extractor) downloads a Jam Track by track ID and, per its README, "decrypts the raw multi-track MIDI file (`notes.mid`)" and writes `song.ini` and `album.png` into one song folder ("Quick MIDI Export" fetches only those three). It is a fork of ilayezra/Festival-Extractor and uses blurlconvert for BLURL parsing (README credits). Its `tests/test_chart_extraction.py` was seen in the file list but not read. Legality of extraction is the user's responsibility.
- Local check of the track layout described in this fiche (Easy 60-63 ... Expert 96-100, note 116 overdrive) needs such an extracted file; none was obtained here.

## Sources
https://dromzeh.dev/posts/reverse-engineering-fortnite-festival · https://github.com/yotolo2354/Festival-MIDI-Extractor · https://www.engadget.com/your-old-rock-band-guitars-now-work-in-fortnite-festival-164054839.html
