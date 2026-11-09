# Samples: Rocksmith 2014 SNG (`.sng`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rocksmith2014net_unpacked.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/unpacked.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | UNPACKED (decrypted, decompressed) SNG data, 47 948 bytes; begins `26 01 00 00 00 00 20 41 ...`, i.e. without the `4A 00 00 00 <flags>` header of the packed files |
| `rocksmith2014net_packed_pc.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/packed_pc.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | packed PC SNG (4160 bytes), begins `4A 00 00 00 03 00 00 00` (header magic 0x4A + flags 3); 'mac' key variant below differs from byte 25 on |
| `rocksmith2014net_packed_mac.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/packed_mac.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | packed macOS SNG (4160 bytes), same name/size as the PC file, differs from it from byte 25 on (platform-specific encryption [inference]) |
| `rocksmith2014net_instrumental.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/instrumental.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | packed PC SNG of the `Test Instrumental` Lead arrangement (16 448 bytes) |
| `rocksmith2014net_vocals.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/vocals.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | packed PC SNG of the vocals arrangement (4160 bytes) |
| `rocksmith2014net_Tech_Test.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.DLCProject.Tests/Tech_Test.sng | iminashi (test data) | MIT (iminashi/Rocksmith2014.NET `LICENSE`, (c) 2020 Tapio Malmberg) | packed PC SNG used by the DLCProject tests (4393 bytes), a techniques test arrangement [name only] |

Notes: only the first bytes were inspected here (no decoder was run); descriptions of the plaintext are limited to what the file names and sizes show. The packed files are encrypted with the PC/macOS key (see the fiche); the format has no audio, so the files are chart-only.
