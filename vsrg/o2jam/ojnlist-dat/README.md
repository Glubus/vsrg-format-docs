# O2Jam music list (`OJNList.dat`, `X2OJNList.dat`)
Kind: metadata

Doc status: partial · ROX: no · Category: vsrg · Encoding: binary (little-endian)

## Overview

Client song index: every song the client knows (playability depends on local `.ojn`/`.ojm`). Each entry is a 300-byte OJN header; e-Games and NOWCOM builds append extra sections (new flag, premium price, release date). Files: `Image/OJNList.dat` (`X2OJNList.dat` for O2Jam X2); in client v3.10 it sits inside `Playing(1).opi`. Documented by SirusDoma/CXO2.

## Container & encoding
Little-endian; strings as in OJN (ASCII or EUC-KR by distribution). No compression.

## Structure / metadata
| Section | Entry size | Content |
|---|---|---|
| File header | 4 | `int32` number of music entries |
| Music header array | 300 each | first 300 bytes of an OJN file each ([ojn header table](../ojn/README.md#structure--metadata)) |
| 1 New (optional) | 16 | `int32` count, then `{int32 music_id; int32 unknown (always 0); int32 unknown (sometimes 1); int32 unknown (sometimes 0 else 1)}`; presence of the id applies the "new" label |
| 2 Premium (optional) | 16 | count, then `{music_id, price in ePoint, unknown (0, presumably O2Cash/MusicCash), unknown (0, presumably GEM)}`: music to buy in the shop |
| 3 Release date (optional) | 28 | count, then `{int32 music_id; char[11] date "yyyy-MM-dd" NUL-terminated; byte unk 0; int32 unk 0; int32 unk always 1243692 (0x12FA2C); int32 unk always 4540192 (0x454720)}` |

Extra sections are ordered; a file may end after any one; an empty section is a count of 0. This is the NX layout (v3.15..v3.82 and legacy v3.10). X2 (v2.33), O2JamO2 beta (v5.89), O2JamO2 (v6.65) and Classic (v8.02) have their own documents (`X2OJNList.md`, ... in the CXO2 repo, not read here: Unknown).

## Timing model
Unknown.

## Notes
Unknown.

## Audio & images
Metadata only; cover bytes are not stored.

## Versions & variants
[observed in samples/o2jam-rar_OJNList.dat] `int32` 307, 307 x 300-byte headers, then **new** (3 x 16 bytes: ids 659, 637, 622, flags `0 1 0`), **premium** (152 x 16 bytes, e.g. `265, 20, 0, 0`) and a third section of 307 x 28 bytes ending exactly at end of file. Its entries hold `music_id, int, 0x00455F00-like constant, 0, 0x0012FA24, 0x00452F54, -1` and no `yyyy-MM-dd` string at offset 4: this older release-date layout is Unknown. The ids are unique (100, 102, 103, ... 703).
Per-client layouts: v3.10 (in OPI), v3.82 NX (above), v2.33 X2, v5.89 / v6.65 O2Jam O2, v8.02 Classic (CXO2 docs).

## Quirks & pitfalls

Entries cover all songs, not only installed ones. The header song id may not be unique across regional lists.

## Example
Unknown.

## ROX support
Not read by ROX.

## Parsers & tools
- SirusDoma/O2MusicList (music list generator, archived): https://github.com/SirusDoma/O2MusicList ; CXO2 : https://github.com/SirusDoma/CXO2 ; Fadreus/Open2Jam `tools/ojn_header.pl`.

## Getting samples

Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). Other client folders: archive.org item `o-2-mania` (`O2Mania.rar`, 1.1 GB, "all songs" pack) and `o2jam_setup.exe` of item `o2jam-setup-client` (setup v20050120, 153 MB); neither was reached (the `Image/` folder lies beyond the first 45 MB read of the former, the latter is an installer). `X2OJNList.dat` belongs to the X2 client. Writers: https://github.com/SirusDoma/O2MusicList and https://github.com/YaKiZu/O2Jam-Music-Manager.

## Sources
- https://github.com/SirusDoma/CXO2/blob/develop/docs/file-format/FileFormat.md
- https://raw.githubusercontent.com/SirusDoma/CXO2/develop/docs/file-format/3.82/OJNList.md
