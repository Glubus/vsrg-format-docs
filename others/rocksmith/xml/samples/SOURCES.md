# Samples: Rocksmith 2014 arrangement XML (`.xml`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `rocksmith2014net_instrumental.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/instrumental.xml | iminashi | MIT | version 8 Lead, `Test Instrumental`, artist `Test`, 12 levels, 127 notes, 136 chords, 294 ebeats, 2 sections |
| `rocksmith2014net_instrumental_capo.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.DLCProject.Tests/instrumental_capo.xml | iminashi | MIT | same song, `capo` 5, `centOffset` 50.0, `tuning` string0=-1 ... string5=-6 |
| `rocksmith2014net_chordnotes.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/chordnotes.xml | iminashi | MIT | `version="7"`, one level, 3 chords and chord notes |
| `rocksmith2014net_instrumental_1level_chordsonly.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/instrumental_1level_chordsonly.xml | iminashi | MIT | version 7, arrangement `Chords_Only`, one level |
| `rocksmith2014net_instrumental_1level_notesonly.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/instrumental_1level_notesonly.xml | iminashi | MIT | version 7, arrangement `PART REAL_GUITAR`, one level, notes only |
| `rocksmith2014net_arr_bass_RS2.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.IntegrationTests/project/arr_bass_RS2.xml | iminashi | MIT | version 7 Bass arrangement, artist `Integration`, 10 notes |
| `rocksmith2014net_arr_lead_RS2.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.IntegrationTests/project/arr_lead_RS2.xml | iminashi | MIT | version 7 Lead arrangement of the same project |
| `rocksmith2014net_vocals.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.Conversion.Tests/vocals.xml | iminashi | MIT | `<vocals count="67">`; note 254 = unpitched [inference] |
| `rocksmith2014net_jvocals.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.DLCProject.Tests/jvocals.xml | iminashi | MIT | Japanese vocals fixture (UTF-8 BOM, small) |
| `rocksmith2014net_showlights.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.XML.Tests/Showlights.xml | iminashi | MIT | `<showlights>` file, 9 KB, UTF-8 BOM |
| `rocksmith2014net_showlights_small.xml` | https://github.com/iminashi/Rocksmith2014.NET/blob/4cf3325174e13f1dc5ce997e7663b2851c6afcce/tests/Rocksmith2014.DLCProject.Tests/showlights.xml | iminashi | MIT | minimal `<showlights>` file (UTF-8 BOM) |

Copied byte for byte from Rocksmith2014.NET test projects. Origin of the note content is not stated. Identical copies in `XML.Tests/instrumental.xml` and `DLCProject.Tests/instrumental.xml` are not duplicated.
