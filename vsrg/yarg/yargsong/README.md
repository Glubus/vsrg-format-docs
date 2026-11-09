# YARG song package (`.yargsong`)
Kind: package

Doc status: stub · ROX: no · Category: vsrg · Encoding: binary

## Overview
`.yargsong` is the single-file song package distributed by the YARC Launcher for YARG. The YARG wiki states it is "supported as a single-file song package for easier distribution of complete song bundles". Third-party tools (YASS, Nautilus) treat it like Clone Hero's `.sng` (Nautilus' changelog groups "Clone Hero SNG files or YARG YARGSONG files"), which suggests a shared container structure [inference]; no standalone specification was found, the authoritative source is the YARG.Core code.

## Contents

- A single-file song package for YARG. Its internal layout is Unknown.
- Chart inside: [`.chart`](../../clone-hero/chart/README.md) or [`.mid`](../../clone-hero/mid/README.md) [inference: same song-folder layout as Clone Hero].

## Container & encoding
Binary container; layout Unknown (probably the [SNG](../../clone-hero/sng/README.md) layout [inference, unverified]). The file starts with the 8-byte signature `YARGSONG`, one seed byte and a 15-byte set (24-byte header); the remainder is obfuscated by a cipher parametrised by those bytes [observed in YARG.Core `YARG.Core/IO/YARGSongFileStream.cs` @ 2f3900cf91aa141149d60cb122e88876e1709abb].

## Structure / metadata
Unknown. Contents are a normal chart folder (`notes.mid`/`notes.chart`, audio, images) with `song.ini`-style metadata.

## Timing model
See [chart](../../clone-hero/chart/README.md) / [mid](../../clone-hero/mid/README.md).

## Notes
See chart/mid.

## Audio & images
YASS reads album art and previews straight from `.yargsong`, `.sng` and CON files.

## Versions & variants
Unknown.

## Quirks & pitfalls
fretwork issue #14 notes it does not parse `.yargsong`; requirements unclear.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
YARG.Core (C#): https://github.com/YARC-Official/YARG.Core · Nautilus (C#): https://github.com/trojannemo/Nautilus · YASS: https://github.com/DevPrice/YASS

## Getting samples
- Committed: none. Manifest: none. No `.yargsong` file was found in YARG.Core, YARG, Nautilus, YASS or fretwork (trees/READMEs checked), and no public specification exists besides the code.
- What the code shows [observed in YARG.Core `YARG.Core/IO/YARGSongFileStream.cs` @ 2f3900cf91aa141149d60cb122e88876e1709abb]: a 24-byte header starting with the ASCII signature `YARGSONG` (8 bytes), one seed byte and a 15-byte set; the rest of the file is read through a cipher (the code's comment calls it a "Crawford multi-value cipher") whose parameters are derived from the header bytes. The decrypted content layout is not shown in that file (Unknown here).
- How to get one: install YARG with the YARC Launcher (https://github.com/YARC-Official/YARG) and look in the song folders it downloads [inference: the launcher's download format and folder were not verified]; the YARG wiki also states `.yargsong` is supported as a single-file package (https://wiki.yarg.in/wiki/Help:Charting). A file could only be produced with YARC tooling; building one by hand is not attempted because the layout after decryption is unverified.

## Sources
https://wiki.yarg.in/wiki/Help:Charting · https://docs.yarg.in/en/faq · https://github.com/DevPrice/YASS · https://github.com/Staycation44/fretwork/issues/14 · https://github.com/trojannemo/Nautilus/releases
