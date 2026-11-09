# Samples: Rocksmith 2014 SNG (`.sng`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rocksmith2014net_unpacked.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/unpacked.sng | iminashi | MIT | unpacked SNG data, 47 948 bytes; begins `26 01 00 00 00 00 20 41 ...`, no `4A 00 00 00 <flags>` header |
| `rocksmith2014net_packed_pc.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/packed_pc.sng | iminashi | MIT | packed PC, 4160 bytes, begins `4A 00 00 00 03 00 00 00` (magic 0x4A + flags 3) |
| `rocksmith2014net_packed_mac.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.SNG.Tests/packed_mac.sng | iminashi | MIT | packed macOS, 4160 bytes, differs from the PC file from byte 25 on [inference: platform key] |
| `rocksmith2014net_instrumental.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/instrumental.sng | iminashi | MIT | packed PC, `Test Instrumental` Lead, 16 448 bytes |
| `rocksmith2014net_vocals.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/vocals.sng | iminashi | MIT | packed PC vocals, 4160 bytes |
| `rocksmith2014net_Tech_Test.sng` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.DLCProject.Tests/Tech_Test.sng | iminashi | MIT | packed PC, DLCProject tests, 4393 bytes, techniques test [name only] |

Only the first bytes were inspected (no decoder run). Packed files are encrypted with the PC/macOS key.
