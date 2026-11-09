# O2Jam music list (`OJNList.dat`, `X2OJNList.dat`)
Kind: metadata

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview
Client-side song index of the O2Jam game: the entire list of songs the client knows (not necessarily playable: playability depends on local `.ojn`/`.ojm`). Each entry is the 300-byte OJN header of a song. In e-Games and NOWCOM distributions extra sections (new flag, premium price, release date) follow. It is not a chart; documented because the original README lists OJN-related files and the SirusDoma/CXO2 project documents it. Files: `Image/OJNList.dat` (`X2OJNList.dat` for O2Jam X2); in client v3.10 it is stored inside `Playing(1).opi`.

## Container & encoding
Little-endian; strings as in OJN (ASCII or EUC-KR by distribution). No compression.

## Structure / metadata
| Section | Entry size | Content |
|---|---|---|
| File header | 4 | `int32` number of music entries |
| Music header array | 300 each | first 300 bytes of an OJN file each ([ojn header table](../ojn/README.md#structure--metadata)) |
| 1 New (optional) | 16 | `int32` count, then `{int32 music_id; int32 unknown (always 0); int32 unknown (sometimes 1); int32 unknown (sometimes 0 else 1)}`; presence of the id applies the "new" label |
| 2 Premium (optional) | 16 | count, then `{music_id, price in ePoint, unknown (0, presumably O2Cash/MusicCash), unknown (0, presumably GEM)}` : music to buy in the shop |
| 3 Release date (optional) | 28 | count, then `{int32 music_id; char[11] date "yyyy-MM-dd" NUL-terminated; byte unk 0; int32 unk 0; int32 unk always 1243692 (0x12FA2C); int32 unk always 4540192 (0x454720)}` |

Extra sections are optional but ordered; a file may end after any one; a section with no data is a count of 0. The layout is the NX layout (v3.15..v3.82 and the legacy v3.10); X2 (v2.33), O2JamO2 beta (v5.89), O2JamO2 (v6.65) and Classic (v8.02) have their own documents (`X2OJNList.md`, ... in the CXO2 repo, not read here: Unknown).

## Timing model
Not applicable.

## Notes
Not applicable.

## Audio & images
Not applicable (only metadata, cover bytes are not stored).

## Versions & variants
Per-client layouts: v3.10 (embedded in OPI), v3.82 NX (above), v2.33 X2, v5.89 / v6.65 O2Jam O2, v8.02 Classic. See CXO2 docs.

## Quirks & pitfalls
Entries describe all songs, not only installed ones. The song id in the header may not be unique across regional lists.

## Example
Not applicable.

## ROX support
Not read by ROX.

## Parsers & tools
- SirusDoma/O2MusicList (music list generator, archived): https://github.com/SirusDoma/O2MusicList ; CXO2 : https://github.com/SirusDoma/CXO2 ; Fadreus/Open2Jam `tools/ojn_header.pl`.

## Getting samples
- **Committed: none (no real file found).** No OJNList file was found in the public repositories scanned (CXO2, O2MusicList, open2jam, render-ojn). A binary file was not invented.
- **How to get one**: copy `Image/OJNList.dat` (or `X2OJNList.dat`) from an O2Jam client you own; in client v3.10 it is inside `Playing(1).opi` (fiche; CXO2 file-format dev log https://dev.cxo2.me/o2jam-file-format lists `Image/OJNList.dat (or X2OJNList.dat for X2 client)`). Or **generate one**: https://github.com/SirusDoma/O2MusicList (MIT, archived; successor https://github.com/SirusDoma/o2jam-workshop-center) "creates or modifies OJNList files", adding OJN files to a new list in the Korean or Chinese layout (its README: File -> New, then Add). [inference] Feeding it the synthetic OJNs of [ojn samples](../ojn/samples/SOURCES.md) would give an OJNList of public-domain-like data; it was not run here (.NET Windows tool).

## Sources
- https://github.com/SirusDoma/CXO2/blob/develop/docs/file-format/FileFormat.md
- https://raw.githubusercontent.com/SirusDoma/CXO2/develop/docs/file-format/3.82/OJNList.md
