# osu!mania

osu!mania is the vertical-scrolling, key-count based game mode of osu! (mode 3). Notes fall along 1 to 18 columns (the key count is `CircleSize`; lazer clamps it to 1..18; 4K and 7K dominate the samples here) toward a judgement line; long notes are holds. Charts are stored in the same `.osu` text file as the other three osu! modes, with `Mode: 3`. It is a major source of VSRG charts: Quaver imports `.osz`, ROX and Moonchart have `.osu` mania codecs.

Category: **vsrg** (fixed lanes, vertical scrolling). The other osu! modes (standard, taiko, catch) are not column based and live in `others/` ([osu!standard](../../others/osu-standard/README.md), [osu!taiko](../../others/osu-taiko/README.md), [osu!catch](../../others/osu-catch/README.md)); they share the very same file format.

Formats in this folder:

| Format | Folder | Status |
|---|---|---|
| `.osu` beatmap (canonical doc for all 4 modes) | [osu/](osu/README.md) | complete |
| `.osb` storyboard file | [osb/](osb/README.md) | partial |
| `.osz` mapset archive, `.osk` skin archive | documented as a section of [osu/](osu/README.md#the-osz--osk-archive-wrapper) | - |

Sample files: [osu/samples/](osu/samples/) (10 real mania maps: 4K and 7K, all `osu file format v14`).

Links: https://osu.ppy.sh/, https://github.com/ppy/osu, https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29, https://github.com/ppy/osu-wiki

Added format page: [`osz/`](osz/README.md) (full page for the `.osz` mapset archive).
