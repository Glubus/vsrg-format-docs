# Fortnite Festival chart MIDI (`.mid`)
Kind: chart

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary (MIDI; encrypted in the game data)

## Overview

Jam Tracks ship their charts as MIDI files, encrypted in the game's download data; community tools (Festival-MIDI-Extractor, the "Fortnite Festival from the Outside" launcher project) decrypt them. Harmonix authored the game and the layout resembles Rock Band/Clone Hero MIDI ([clone-hero/mid](../../clone-hero/mid/README.md)). Encryption scheme and exact track names: Unknown.

## Container & encoding

Standard MIDI File after decryption; encryption Unknown.

## Structure / metadata
Per the dromzeh.dev write-up: instrument tracks with four difficulty tiers by MIDI note range: Easy 60-63 (4 frets), Medium 72-75 (4 frets), Hard 84-87 (4 frets), Expert 96-100 (5 frets). Fret index 0-4 = green to orange. Note 116 marks overdrive phrases (note on/off = phrase). Base+6..base+10 within a difficulty octave are lift notes. Notes sharing a tick form a chord. A `SECTION` track holds named song sections. Flags derived by the parser: tap, overdrive, lift, chord.

## Timing model
MIDI ticks with tempo map; sustain = note length, kept in ticks, ms and beats by the parser.

## Notes
5 lanes (Expert) / 4 lanes (lower), sustains, lifts, chords, taps, overdrive. Plastic-guitar charts (Pro Lead / Pro Bass, with HOPOs) exist as separate tracks [per the engadget/X reports: "Rock Band 5 in every way but name"].

## Audio & images

Unknown (stems are separate game assets).

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

Committed: none. No public real `notes.mid` exists: charts are encrypted and no public repository holds decrypted files (checked yotolo2354/Festival-MIDI-Extractor, Mynrax/Fest2CH, FEStoRB/FNFestivaltoRB, hmxmilohax/festivalinfobot: tools only; Chorus Encore entries mentioning Fortnite are fan charts). To get one: Festival-MIDI-Extractor (MIT, https://github.com/yotolo2354/Festival-MIDI-Extractor) downloads a Jam Track by track ID and, per its README, "decrypts the raw multi-track MIDI file (`notes.mid`)" and writes `song.ini` and `album.png` next to it ("Quick MIDI Export" fetches only those three). Mynrax/Fest2CH (https://github.com/Mynrax/Fest2CH) exports to Clone Hero/YARG folders per its description.

## Sources
https://dromzeh.dev/posts/reverse-engineering-fortnite-festival · https://github.com/yotolo2354/Festival-MIDI-Extractor · https://www.engadget.com/your-old-rock-band-guitars-now-work-in-fortnite-festival-164054839.html
