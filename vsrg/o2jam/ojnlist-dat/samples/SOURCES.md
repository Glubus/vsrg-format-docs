# Samples: O2Jam music list (`OJNList.dat`)

Real file downloaded from a public source (fetched 2026-11-09).

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `o2jam-rar_OJNList.dat` | https://archive.org/download/o-2-jam_202506/O2Jam.rar (member `O2Jam/Image/OJNList.dat`) | 2026-11-09 | a93cb5c96b162d55fb2db3b6e35129dfe6a1643e5bd9b2696384fcf6e52004a0 (of the first 45 MB range of the 1.7 GB RAR) | O2Media / O2Jam client data | no licence stated; client folder preserved on archive.org item `o-2-jam_202506` | Extracted with libarchive `bsdtar`; 103192 bytes (file date Sep 19 2007 in the archive): `int32` 307 entries, then 307 x 300-byte OJN headers (first ids 100, 102, 103, 104, 105; last 703; titles such as "Bach Alive"), then **new** (3 entries of 16 bytes: music ids 659, 637, 622), **premium** (152 entries of 16 bytes, e.g. id 265 price 20) and a third section of 307 x 28 bytes that ends exactly at end of file. Its entries contain no `yyyy-MM-dd` string in this client (`09 01 00 00 a3 01 00 00 00 5f 45 00 ...`: id 265, then small ints and pointer-like constants, last int -1) [observed]. |
