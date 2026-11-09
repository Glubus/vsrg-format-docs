# osu!mania

Vertical-scrolling, key-count based mode of osu! (mode 3). Notes fall along 1 to 18 columns toward a judgement line (key count = `CircleSize`, lazer clamps it to 1..18; 4K and 7K dominate the samples here). Long notes are holds. Charts live in the same `.osu` text file as the other three modes, with `Mode: 3`. Quaver imports `.osz`; ROX and Moonchart have `.osu` mania codecs.

Category: vsrg (fixed lanes, vertical scrolling). The other modes (standard, taiko, catch) are not column based, share the file format and live in `others/`: [osu!standard](../../others/osu-standard/README.md), [osu!taiko](../../others/osu-taiko/README.md), [osu!catch](../../others/osu-catch/README.md).

| Format | Folder | Status |
|---|---|---|
| `.osu` beatmap (canonical doc for all 4 modes) | [osu/](osu/README.md) | complete |
| `.osb` storyboard file | [osb/](osb/README.md) | partial |
| `.osz` mapset archive, `.osk` skin archive | documented as a section of [osu/](osu/README.md#the-osz--osk-archive-wrapper) | - |

Samples: [osu/samples/](osu/samples/) (10 original community maps, 4K and 7K, v14, plus 48 fixtures: 1K-18K, special style, old format versions v4-v10, CRLF/BOM edge cases), [osb/samples/](osb/samples/).

lazer's `client.realm` is a Realm metadata database, not a chart format (`OsuGameBase.CLIENT_DATABASE_FILENAME`, ppy/osu @ bb37f05). lazer stores the `.osu`/audio files content-addressed under `files/` and exports sets as `.olz` (lazer-native) or `.osz` (stable-compatible).

Links: https://osu.ppy.sh/, https://github.com/ppy/osu, https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29, https://github.com/ppy/osu-wiki
