# DSC (`.dsc`, Project DIVA script / chart)
Kind: chart

Doc status: partial · ROX: no · Category: others · Encoding: binary (stream of 32-bit integers; little- or big-endian by platform)

## Overview

In SEGA's Project DIVA series (PSP, arcade, PS3/Vita *f*, *F*, *F 2nd*, *X*, PS4/Switch *Future Tone* / *Mega Mix*, 3DS *Project Mirai*) the chart is not a separate format. It is embedded in the DSC ("DivaScript") file of a PV: a compiled script of timed commands that also drives camera, character motions, expressions, lyrics, lighting, post-processing and the targets. The chart is the sequence of `TARGET(...)` commands (plus `BAR_TIME_SET`/`TARGET_FLYING_TIME`, branch and challenge-time commands). Each game generation has its own opcode numbering and parameter counts ("DSC formats"). Community tools dump DSC to a text script `OPCODE(arg, arg, ...);` and reassemble it: Open PD Script Editor (nastys, Qt/C++, based on samyuu's ScriptEditor opcodes), DSC Studio (formerly DSC Editor), samyuu's ScriptEditor / Comfy Studio, DSCTools (DivaModding), `DIVA_Tools/FDSC`, `dsc-merger` (Rust), MikuMikuLibrary. DivaDocs ("DivaScript" page) returned HTTP 404, so semantics below come from the Open PD Script Editor source and dsc-merger.

Category: others. Free-position targets (x, y, angle, distance, amplitude/frequency curve) fly along trajectories; the file is a general PV script.

## Container & encoding

- Binary, 32-bit signed integers only: `[opcode:i32] [param0:i32] ... [param(n-1):i32]`, `n` = parameter count of that opcode in that game format. No framing: the parser must know the counts (tables below).
- Endianness: Open PD Script Editor handles both (user selects LE/BE; for the PSP "Edit" layout a 16-byte shift applies to all offsets in big-endian mode). Which platform uses which order is not stated in the sources opened (the F2 writer carries a TODO "endianness flag 0x10 LE, 0x18 BE?").
- Headers (Open PD Script Editor `DSC.cpp`; reader skip / writer header):
  - f: 4-byte header (`0x12020220` = 302121504 written on save), commands to end of file.
  - FT (the editor's "FT" format): 4-byte header `0x14050921` (335874337), commands to end of file.
  - Mirai (3DS): 4-byte header (writer emits `0x12020220`), commands to end of file.
  - F 2nd and X: header starting with ASCII magic `PVSC` (dword `0x43535650`), zero dwords and size fields (the F2 writer stores `file size - 92` at offsets 4 and 20; writers emit 19 dwords, readers skip 72 bytes), then the commands, then a trailer: magic `EOFC` (`0x43464F45`) + 6 zero dwords. The X reader stops at `EOFC`.
  - A12 / PDA (arcade 1.01 / 2.00) and PSP1 / PSP2: no header; plain command stream to end of file.
  - PSP "Edit" data (editor format `PSP2Edit`, Project DIVA 2nd/Extend edit mode): fixed layout, not a stream. Script at `0xE108`, lyrics (600 × 0x29-byte strings) at `0x2C2AC`, BPM changes (600 dwords, -1 = none) at `0x337DC`, then 600 "change bar" and 600 time-signature dwords (stored -1), song end at `0x353FC`, two modules, 20 stages (from `0x35408`), 30 motions, a button-SFX id and 9 hand items (names 0x28 bytes).
- Related files (from search results about the community docs, not opened): `pv_db.txt` PV metadata (encrypted `DIVAFILE` in F 2nd/X), `.farc` archives holding the DSC files, audio files, `.mot` motions.

## Structure / metadata

A PV script is a time-ordered list: `TIME(t)` sets the current time and following commands run at it until the next `TIME`. Typical start: `TIME(0)`, `PV_BRANCH_MODE(0)` ...; end: `PV_END` then `END`. Branches are `PV_BRANCH_MODE(n)` blocks (editor `time_branch` slots: 0 = default, 1 = fail, 2 = success), used for "Challenge Time"/dual-route data in newer games.

Chart-relevant opcodes:

| Opcode | Meaning |
|---|---|
| `TIME(t)` | timestamp in **units of 10 µs** (1/100 000 s): the editor converts `h:m:s.ms` as `(ms + (min·60 + h·3600)·1000)·100`; `6 000 000` = 1 minute |
| `TARGET(...)` | spawn a target (button note) arriving at this time. Parameter count per game: PSP1/PSP2/A12/FT **7**, f **11**, F2/X **12**. Contains target type (circle, cross, square, triangle, star, holds, rush…), position (x, y), approach angle/curve parameters, hold length...**exact parameter meanings are not documented in the sources opened** |
| `TARGET_FLYING_TIME(ms)` | time (ms) a target takes to travel from spawn to its hit point; equals `240000/BPM` for the "normal" speed |
| `BAR_TIME_SET(bpm, timesig)` | sets tempo and the time signature index used for bar timing; relation to flying time in the editor: `flying_time = 1000 / (bpm / ((ts+1)·60))` ms and `bpm = round(240000 / flying_time)` with `ts = 3` (4/4) |
| `PV_BRANCH_MODE(m)` | begin a section for branch `m` (f/F2/X/FT) |
| `MUSIC_PLAY`, `PV_END`, `END` | start audio, end of PV, end of script |
| `TARGET_FLAG` (FT) | extra target flag (FT only) |
| `TARGET_EFFECT` (F2/X) | target effects (11 params) |
| `LYRIC`, `EDIT_LYRIC`, `LYRIC_2`, `LYRIC_READ(_2)` | lyrics lines (X has extra variants) |
| `SET_CAMERA`, `DATA_CAMERA`, `MOVE_CAMERA`, `EDIT_CAMERA` … | camera work |
| `MIKU_MOVE`, `MIKU_ROT`, `SET_MOTION`, `HAND_ANIM`, `MOUTH_ANIM`, `EXPRESSION`, `LOOK_ANIM`, `EYE_ANIM`, `EDIT_*` … | character animation |
| `EFFECT`, `FADEIN_FIELD`, `FADEOUT_FIELD`, `CHANGE_FIELD`, `FOG`, `BLOOM`, `DOF`, `TONE_MAP`, … | stage/post effects |

### Opcode table (id / parameter count per game format)

Extracted from the opcode database of Open PD Script Editor (`opcode_db/db.json`, 186 opcode names). `–` = opcode does not exist in that format. Column keys: **PSP1** Project DIVA (PSP), **PSP2** 2nd/Extend, **A12** arcade 1.01/2.00, **f** Project DIVA f, **F2** F 2nd, **X** Project DIVA X, **FT** arcade Future Tone (the editor's "FT" format). Mega Mix+ reuses the FT/F2-style layout (`DSC Studio` handles it) [not verified here].

| Opcode | PSP1 | PSP2 | A12 | f | F2 | X | FT |
|---|---|---|---|---|---|---|---|
| `END` | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| `TIME` | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| `MIKU_MOVE` | 2/3 | 2/4 | 2/3 | 2/4 | 2/4 | 2/4 | 2/4 |
| `MIKU_ROT` | 3/1 | 3/2 | 3/1 | 3/2 | 3/2 | 3/2 | 3/2 |
| `MIKU_DISP` | 4/1 | 4/2 | 4/1 | 4/2 | 4/2 | 4/2 | 4/2 |
| `MIKU_SHADOW` | 5/1 | 5/2 | 5/1 | 5/2 | 5/2 | 5/2 | 5/2 |
| `TARGET` | 6/7 | 6/7 | 6/7 | 6/11 | 6/12 | 6/12 | 6/7 |
| `SET_MOTION` | 7/3 | 7/4 | 7/3 | 7/4 | 7/4 | 7/4 | 7/4 |
| `SET_PLAYDATA` | 8/1 | 8/2 | 8/1 | 8/2 | 8/2 | 8/2 | 8/2 |
| `EFFECT` | 9/5 | 9/6 | 9/5 | 9/6 | 9/6 | 9/6 | 9/6 |
| `FADEIN_FIELD` | 10/2 | 10/2 | 10/2 | 10/2 | 10/2 | 10/2 | 10/2 |
| `EFFECT_OFF` | 11/1 | 11/1 | 11/1 | 11/1 | 11/1 | 11/1 | 11/1 |
| `SET_CAMERA` | 12/6 | 12/6 | 12/6 | 12/6 | 12/6 | 12/6 | 12/6 |
| `DATA_CAMERA` | 13/2 | 13/2 | 13/2 | 13/2 | 13/2 | 13/2 | 13/2 |
| `CHANGE_FIELD` | 14/1 | 14/1 | 14/1 | 14/1 | 14/2 | 14/2 | 14/1 |
| `HIDE_FIELD` | 15/1 | 15/1 | 15/1 | 15/1 | 15/1 | 15/1 | 15/1 |
| `MOVE_FIELD` | 16/3 | 16/3 | 16/3 | 16/3 | 16/3 | 16/3 | 16/3 |
| `FADEOUT_FIELD` | 17/2 | 17/2 | 17/2 | 17/2 | 17/2 | 17/2 | 17/2 |
| `EYE_ANIM` | 18/2 | 18/3 | 18/2 | 18/3 | 18/3 | 18/3 | 18/3 |
| `MOUTH_ANIM` | 19/3 | 19/5 | 19/3 | 19/5 | 19/5 | 19/5 | 19/5 |
| `HAND_ANIM` | 20/4 | 20/5 | 20/4 | 20/5 | 20/5 | 20/5 | 20/5 |
| `LOOK_ANIM` | 21/3 | 21/4 | 21/3 | 21/4 | 21/4 | 21/4 | 21/4 |
| `EXPRESSION` | 22/3 | 22/4 | 22/3 | 22/4 | 22/4 | 22/4 | 22/4 |
| `LOOK_CAMERA` | 23/4 | 23/5 | 23/4 | 23/5 | 23/5 | 23/5 | 23/5 |
| `LYRIC` | 24/1 | 24/2 | 24/1 | 24/2 | 24/2 | 24/2 | 24/2 |
| `MUSIC_PLAY` | 25/0 | 25/0 | 25/0 | 25/0 | 25/0 | 25/0 | 25/0 |
| `MODE_SELECT` | 26/1 | 26/2 | 26/1 | 26/2 | 26/2 | 26/2 | 26/2 |
| `EDIT_MOTION` | 27/2 | 27/4 | 27/2 | 27/4 | 27/4 | 27/4 | 27/4 |
| `BAR_TIME_SET` | 28/2 | 28/2 | 28/2 | 28/2 | 28/2 | 28/2 | 28/2 |
| `SHADOWHEIGHT` | 29/1 | 29/2 | 29/1 | 29/2 | 29/2 | 29/2 | 29/2 |
| `EDIT_FACE` | 30/2 | 30/1 | 30/2 | 30/1 | 30/1 | 30/1 | 30/1 |
| `DUMMY` | – | – | – | – | – | 31/21 | – |
| `MOVE_CAMERA` | 31/19 | 31/21 | 31/19 | 31/21 | 31/21 | – | 31/21 |
| `PV_END` | 32/0 | 32/0 | 32/0 | 32/0 | 32/0 | 32/0 | 32/0 |
| `SHADOWPOS` | 33/2 | 33/3 | 33/2 | 33/3 | 33/3 | 33/3 | 33/3 |
| `EDIT_LYRIC` | – | 34/2 | – | 34/2 | 34/2 | 34/2 | 34/2 |
| `NEAR_CLIP` | 34/2 | 49/2 | 34/2 | 49/2 | 49/2 | 49/2 | 49/2 |
| `CLOTH_WET` | 35/1 | 50/2 | 35/1 | 50/2 | 50/2 | 50/2 | 50/2 |
| `EDIT_TARGET` | – | 35/5 | – | 35/5 | 35/5 | 35/5 | 35/5 |
| `EDIT_MOUTH` | – | 36/1 | – | 36/1 | 36/1 | 36/1 | 36/1 |
| `SCENE_FADE` | – | 52/6 | 36/6 | 52/6 | 52/6 | 52/6 | 52/6 |
| `SET_CHARA` | – | 37/1 | – | 37/1 | 37/1 | 37/1 | 37/1 |
| `TONE_TRANS` | – | 53/6 | 37/6 | 53/6 | 53/6 | 53/6 | 53/6 |
| `EDIT_MOVE` | – | 38/7 | – | 38/7 | 38/7 | 38/7 | 38/7 |
| `SATURATE` | – | 54/1 | 38/1 | 54/1 | 54/1 | 54/1 | 54/1 |
| `EDIT_SHADOW` | – | 39/1 | – | 39/1 | 39/1 | 39/1 | 39/1 |
| `FADE_MODE` | – | 55/1 | 39/1 | 55/1 | 55/1 | 55/1 | 55/1 |
| `EDIT_EYELID` | – | 40/1 | – | 40/1 | 40/1 | 40/1 | 40/1 |
| `EDIT_EYE` | – | 41/2 | – | 41/2 | 41/2 | 41/2 | 41/2 |
| `EDIT_ITEM` | – | 42/1 | – | 42/1 | 42/1 | 42/1 | 42/1 |
| `EDIT_EFFECT` | – | 43/2 | – | 43/2 | 43/2 | 43/2 | 43/2 |
| `EDIT_DISP` | – | 44/1 | – | 44/1 | 44/1 | 44/1 | 44/1 |
| `EDIT_HAND_ANIM` | – | 45/2 | – | 45/2 | 45/2 | 45/2 | 45/2 |
| `AIM` | – | 46/3 | – | 46/3 | 46/3 | 46/3 | 46/3 |
| `HAND_ITEM` | – | 47/3 | – | 47/3 | 47/3 | 47/3 | 47/3 |
| `EDIT_BLUSH` | – | 48/1 | – | 48/1 | 48/1 | 48/1 | 48/1 |
| `LIGHT_ROT` | – | 51/3 | – | 51/3 | 51/3 | 51/3 | 51/3 |
| `AUTO_BLINK` | – | 56/2 | – | 56/2 | 56/2 | 56/2 | 56/2 |
| `PARTS_DISP` | – | 57/3 | – | 57/3 | 57/3 | 57/3 | 57/3 |
| `TARGET_FLYING_TIME` | – | 58/1 | – | 58/1 | 58/1 | 58/1 | 58/1 |
| `CHARA_SIZE` | – | 59/2 | – | 59/2 | 59/2 | 59/2 | 59/2 |
| `CHARA_HEIGHT_ADJUST` | – | 60/2 | – | 60/2 | 60/2 | 60/2 | 60/2 |
| `ITEM_ANIM` | – | 61/4 | – | 61/4 | 61/4 | 61/4 | 61/4 |
| `CHARA_POS_ADJUST` | – | 62/4 | – | 62/4 | 62/4 | 62/4 | 62/4 |
| `SCENE_ROT` | – | 63/1 | – | 63/1 | 63/1 | 63/1 | 63/1 |
| `EDIT_MOT_SMOOTH_LEN` | – | – | – | 64/2 | 64/2 | 64/2 | 64/2 |
| `PV_BRANCH_MODE` | – | – | – | 65/1 | 65/1 | 65/1 | 65/1 |
| `DATA_CAMERA_START` | – | – | – | 66/2 | 66/2 | 66/2 | 66/2 |
| `MOVIE_PLAY` | – | – | – | 67/1 | 67/1 | 67/1 | 67/1 |
| `MOVIE_DISP` | – | – | – | 68/1 | 68/1 | 68/1 | 68/1 |
| `WIND` | – | – | – | 69/3 | 69/3 | 69/3 | 69/3 |
| `OSAGE_STEP` | – | – | – | 70/3 | 70/3 | 70/3 | 70/3 |
| `OSAGE_MV_CCL` | – | – | – | 71/3 | 71/3 | 71/3 | 71/3 |
| `CHARA_COLOR` | – | – | – | 72/2 | 72/2 | 72/2 | 72/2 |
| `SE_EFFECT` | – | – | – | 73/1 | 73/1 | 73/1 | 73/1 |
| `CHARA_SHADOW_QUALITY` | – | – | – | – | – | 74/2 | – |
| `EDIT_MOVE_XYZ` | – | – | – | 74/9 | 74/9 | – | 74/9 |
| `EDIT_EYELID_ANIM` | – | – | – | 75/3 | 75/3 | – | 75/3 |
| `STAGE_SHADOW_QUALITY` | – | – | – | – | – | 75/2 | – |
| `COMMON_LIGHT` | – | – | – | – | – | 76/2 | – |
| `EDIT_INSTRUMENT_ITEM` | – | – | – | 76/2 | 76/2 | – | 76/2 |
| `EDIT_MOTION_LOOP` | – | – | – | 77/4 | 77/4 | – | 77/4 |
| `TONE_MAP` | – | – | – | – | – | 77/2 | – |
| `EDIT_EXPRESSION` | – | – | – | 78/2 | 78/2 | – | 78/2 |
| `IBL_COLOR` | – | – | – | – | – | 78/2 | – |
| `EDIT_EYE_ANIM` | – | – | – | 79/3 | 79/3 | – | 79/3 |
| `REFLECTION` | – | – | – | – | – | 79/2 | – |
| `CHROMATIC_ABERRATION` | – | – | – | – | – | 80/3 | – |
| `EDIT_MOUTH_ANIM` | – | – | – | 80/2 | 80/2 | – | 80/2 |
| `EDIT_CAMERA` | – | – | – | 81/24 | 81/22 | – | 81/24 |
| `STAGE_SHADOW` | – | – | – | – | – | 81/2 | – |
| `EDIT_MODE_SELECT` | – | – | – | 82/1 | 82/1 | – | 82/1 |
| `REFLECTION_QUALITY` | – | – | – | – | – | 82/2 | – |
| `PV_END_FADEOUT` | – | – | – | 83/2 | 83/2 | 83/2 | 83/2 |
| `CREDIT_TITLE` | – | – | – | – | – | 84/1 | – |
| `TARGET_FLAG` | – | – | – | – | – | – | 84/1 |
| `BAR_POINT` | – | – | – | – | – | 85/1 | – |
| `ITEM_ANIM_ATTACH` | – | – | – | – | – | – | 85/3 |
| `BEAT_POINT` | – | – | – | – | – | 86/1 | – |
| `SHADOW_RANGE` | – | – | – | – | – | – | 86/1 |
| `HAND_SCALE` | – | – | – | – | – | – | 87/3 |
| `RESERVE` | – | – | – | – | 87/9 | 117/2 | – |
| `LIGHT_POS` | – | – | – | – | – | – | 88/4 |
| `PV_AUTH_LIGHT_PRIORITY` | – | – | – | – | 88/2 | 88/2 | – |
| `FACE_TYPE` | – | – | – | – | – | – | 89/1 |
| `PV_CHARA_LIGHT` | – | – | – | – | 89/3 | 89/3 | – |
| `PV_STAGE_LIGHT` | – | – | – | – | 90/3 | 90/3 | – |
| `SHADOW_CAST` | – | – | – | – | – | – | 90/2 |
| `EDIT_MOTION_F` | – | – | – | – | – | – | 91/6 |
| `TARGET_EFFECT` | – | – | – | – | 91/11 | 91/11 | – |
| `FOG` | – | – | – | – | 92/3 | 92/3 | 92/3 |
| `BLOOM` | – | – | – | – | 93/2 | 93/2 | 93/2 |
| `COLOR_COLLE` | – | – | – | – | – | – | 94/3 |
| `COLOR_CORRECTION` | – | – | – | – | 94/3 | 94/3 | – |
| `DOF` | – | – | – | – | 95/3 | 95/3 | 95/3 |
| `CHARA_ALPHA` | – | – | – | – | 96/4 | 96/4 | 96/4 |
| `AOTO_CAP` | – | – | – | – | – | – | 97/1 |
| `AUTO_CAPTURE_BEGIN` | – | – | – | – | 97/1 | 97/1 | – |
| `MANUAL_CAPTURE` | – | – | – | – | 98/1 | 98/1 | – |
| `MAN_CAP` | – | – | – | – | – | – | 98/1 |
| `TOON` | – | – | – | – | – | – | 99/3 |
| `TOON_EDGE` | – | – | – | – | 99/3 | 99/3 | – |
| `SHIMMER` | – | – | – | – | 100/3 | 100/3 | 100/3 |
| `ITEM_ALPHA` | – | – | – | – | 101/4 | 101/4 | 101/4 |
| `MOVIE_CUT` | – | – | – | – | 102/1 | 102/1 | – |
| `MOVIE_CUT_CHG` | – | – | – | – | – | – | 102/1 |
| `CHARA_LIGHT` | – | – | – | – | – | – | 103/3 |
| `CROSSFADE` | – | – | – | – | 103/1 | – | – |
| `EDIT_CAMERA_BOX` | – | – | – | – | 108/112 | 103/112 | – |
| `EDIT_STAGE_PARAM` | – | – | – | – | 109/1 | 104/1 | – |
| `STAGE_LIGHT` | – | – | – | – | – | – | 104/3 |
| `SUBFRAMERENDER` | – | – | – | – | 104/1 | – | – |
| `AGEAGE_CTRL` | – | – | – | – | – | – | 105/8 |
| `EDIT_CHANGE_FIELD` | – | – | – | – | 110/1 | 105/1 | – |
| `EVENT_JUDGE` | – | – | – | – | 105/36 | – | – |
| `MIKUDAYO_ADJUST` | – | – | – | – | – | 106/7 | – |
| `PSE` | – | – | – | – | – | – | 106/2 |
| `TOON＿EDGE` | – | – | – | – | 106/2 | – | – |
| `FOG_ENABLE` | – | – | – | – | 107/2 | – | – |
| `LYRIC_2` | – | – | – | – | – | 107/2 | – |
| `LYRIC_READ` | – | – | – | – | – | 108/2 | – |
| `LYRIC_READ_2` | – | – | – | – | – | 109/2 | – |
| `ANNOTATION` | – | – | – | – | – | 110/5 | – |
| `STAGE_EFFECT` | – | – | – | – | – | 111/2 | – |
| `SONG_EFFECT` | – | – | – | – | – | 112/3 | – |
| `SONG_EFFECT_ATTACH` | – | – | – | – | – | 113/3 | – |
| `LIGHT_AUTH` | – | – | – | – | – | 114/2 | – |
| `FADE` | – | – | – | – | – | 115/2 | – |
| `SET_STAGE_EFFECT_ENV` | – | – | – | – | – | 116/2 | – |
| `COMMON_EFFECT_AET_FRONT` | – | – | – | – | – | 118/2 | – |
| `COMMON_EFFECT_AET_FRONT_LOW` | – | – | – | – | – | 119/2 | – |
| `COMMON_EFFECT_PARTICLE` | – | – | – | – | – | 120/2 | – |
| `SONG_EFFECT_ALPHA_SORT` | – | – | – | – | – | 121/3 | – |
| `LOOK_CAMERA_FACE_LIMIT` | – | – | – | – | – | 122/5 | – |
| `ITEM_LIGHT` | – | – | – | – | – | 123/3 | – |
| `CHARA_EFFECT` | – | – | – | – | – | 124/3 | – |
| `MARKER` | – | – | – | – | – | 125/2 | – |
| `CHARA_EFFECT_CHARA_LIGHT` | – | – | – | – | – | 126/3 | – |
| `ENABLE_COMMON_LIGHT_TO_CHARA` | – | – | – | – | – | 127/2 | – |
| `ENABLE_FXAA` | – | – | – | – | – | 128/2 | – |
| `ENABLE_TEMPORAL_AA` | – | – | – | – | – | 129/2 | – |
| `ENABLE_REFLECTION` | – | – | – | – | – | 130/2 | – |
| `BANK_BRANCH` | – | – | – | – | – | 131/2 | – |
| `BANK_END` | – | – | – | – | – | 132/2 | – |
| `VR_LIVE_MOVIE` | – | – | – | – | – | 141/2 | – |
| `VR_CHEER` | – | – | – | – | – | 142/2 | – |
| `VR_CHARA_PSMOVE` | – | – | – | – | – | 143/2 | – |
| `VR_MOVE_PATH` | – | – | – | – | – | 144/2 | – |
| `VR_SET_BASE` | – | – | – | – | – | 145/2 | – |
| `VR_TECH_DEMO_EFFECT` | – | – | – | – | – | 146/2 | – |
| `VR_TRANSFORM` | – | – | – | – | – | 147/2 | – |
| `GAZE` | – | – | – | – | – | 148/2 | – |
| `TECH_DEMO_GESUTRE` | – | – | – | – | – | 149/2 | – |
| `VR_CHEMICAL_LIGHT_COLOR` | – | – | – | – | – | 150/2 | – |
| `VR_LIVE_MOB` | – | – | – | – | – | 151/5 | – |
| `VR_LIVE_HAIR_OSAGE` | – | – | – | – | – | 152/9 | – |
| `VR_LIVE_LOOK_CAMERA` | – | – | – | – | – | 153/9 | – |
| `VR_LIVE_CHEER` | – | – | – | – | – | 154/5 | – |
| `VR_LIVE_GESTURE` | – | – | – | – | – | 155/3 | – |
| `VR_LIVE_CLONE` | – | – | – | – | – | 156/7 | – |
| `VR_LOOP_EFFECT` | – | – | – | – | – | 157/7 | – |
| `VR_LIVE_ONESHOT_EFFECT` | – | – | – | – | – | 158/6 | – |
| `VR_LIVE_PRESENT` | – | – | – | – | – | 159/9 | – |
| `VR_LIVE_TRANSFORM` | – | – | – | – | – | 160/5 | – |
| `VR_LIVE_FLY` | – | – | – | – | – | 161/5 | – |
| `VR_LIVE_CHARA_VOICE` | – | – | – | – | – | 162/2 | – |

Plain-text dump syntax (Open PD Script Editor / dsc-merger "plaintext"): one command per statement, `NAME(p0, p1, …);`, e.g. `TIME(6000000);` then `TARGET(...)`; blank lines allowed.

## Timing model

- `TIME(t)` is absolute time in 10 µs units (1/100 000 s) from the start of the script; all commands after it fire then (several can share one `TIME`). `seconds = t / 100000`.
- Notes are authored by hit time; the game spawns the target `TARGET_FLYING_TIME` ms earlier (derived from BPM via `BAR_TIME_SET(bpm, ts)`: `240000/bpm` ms for 4/4). Converters get BPM from `BAR_TIME_SET` or `pv_db`, not from a header.
- No audio-offset field: sync is a property of the PV (audio starts at the `MUSIC_PLAY` command time).
- `PV_BRANCH_MODE(n)` splits the stream into alternative command lists chosen by player state (default/fail/success).

## Notes

Each `TARGET` is one note. Parameter counts: 7 in PSP/A12/FT, 11 in f, 12 in F2/X. Their meaning (type, position, trajectory, hold length) is not verified in the sources opened and not listed here. `TARGET_FLAG` (FT) and `TARGET_EFFECT` (F2/X) carry extra per-target data. No keysounds.

## Audio & images

Audio is separate (`MUSIC_PLAY` starts it). PV metadata, lyrics timing and difficulty stars are in `pv_db`; lyric lines are DSC `LYRIC` commands (600 fixed strings in the PSP edit layout). dsc-merger can add Challenge Time sections and lyric markers.

## Versions & variants

PSP1/PSP2 to A12 (arcade) to f to F2 to X to FT. Ids 0-33 are almost identical across formats; later additions sit in 34-163 (see the table); some ids are reused with another meaning (e.g. `EDIT_LYRIC`/`NEAR_CLIP`, `EDIT_CAMERA_BOX` at 103 in X and 108 in F2). Mega Mix+/DSC Studio: FT-style. Project Mirai (3DS) has its own table (`DivaScriptOpcode_Mirai`, not in the db above).

## Quirks & pitfalls

- Parse with the table of the right game format, or the stream desynchronises (the editor aborts "DSC is corrupted. Unknown opcode").
- Same name, different id/length between games (`TARGET`: 7/11/12; `CHANGE_FIELD`: 1/2; `MODE_SELECT`, `SET_PLAYDATA`: 1/2).
- `TOON＿EDGE` (F2, id 106) has a full-width underscore in the editor's DB.
- Scripts end with `END`; X/F2 add the `EOFC` trailer.
- `TIME` values must be non-decreasing; commands before the first `TIME` are invalid [inference].
- Big-endian PS3/Vita-era and little-endian files coexist.

## Example

Hand-built, placeholder values (not a real chart), plaintext form:

```
TIME(0);
PV_BRANCH_MODE(0);
BAR_TIME_SET(120, 3);
TIME(100000);
TARGET_FLYING_TIME(2000);
TIME(300000);
PV_END();
END();
```

`TIME(100000)` = 1.000 s; `BAR_TIME_SET(120, 3)`: `flying_time = 1000/(120/((3+1)·60)) = 2000` ms.

## ROX support

Not read by ROX 0.8.1. A DSC to ROX conversion would be lossy (free-position targets) and needs reverse-engineered `TARGET` semantics.

## Parsers & tools

- [nastys/Open-PD-Script-Editor](https://github.com/nastys/Open-PD-Script-Editor) (C++/Qt; opcode DB `opcode_db/db.json`, `DSC.cpp`) (deprecated in favour of DSC Studio and ScriptEditor)
- [jozsefsallai/dsc-merger](https://github.com/jozsefsallai/dsc-merger) (Rust; FT, F, F2, X)
- DSC Studio (<https://docs.divamodarchive.com/DSC_Studio> via search, <https://gamebanana.com/tools/15894>), samyuu's ScriptEditor / [Comfy Studio](https://github.com/Samyuu/ComfyStudio)
- [Waelwindows/DIVA_Tools](https://github.com/Waelwindows/DIVA_Tools) (C#, FDSC: dsc ↔ xml), [blueskythlikesclouds/MikuMikuLibrary](https://github.com/blueskythlikesclouds/MikuMikuLibrary)
- [Brolijah/DSC_ConvertF2nd_Luvit](https://github.com/Brolijah/DSC_ConvertF2nd_Luvit) (Lua, F to F 2nd DSC), thatrandomlurker's fork for Mirai / Miracle Girls Festival

## Getting samples

Committed: see [samples/SOURCES.md](samples/SOURCES.md) (`pv_<id>_extreme.dsc` from DIVA Mod Archive posts 672, 728, 607, extracted by HTTP range requests from the multi-hundred-MB zips). More: the DIVA Mod Archive API (`https://divamodarchive.com/api/v1/posts?query=song+pack`, observed 2026-11-09) lists song packs with `files` download URLs; charts sit at `<pack>/rom/script/pv_<id>_<difficulty>.dsc` in the zip. Also Comfy Studio exports (dsc-merger README), DSC Studio / Open PD Script Editor, or your own retail copy.

## Sources

- <https://raw.githubusercontent.com/nastys/Open-PD-Script-Editor/touchbar/DSC.cpp>, `DSC.h`, `command.cpp`, `mainwindow.cpp`, `diag_time.cpp`, `opcode_db/db.json` (read)
- <https://github.com/jozsefsallai/dsc-merger> README (read)
- DivaDocs *DivaScript* / *DSC Studio* pages (<https://docs.divamodarchive.com/DivaScript>): returned by search, fetch failed (HTTP 404), not used
