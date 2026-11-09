# osu!taiko

osu!taiko is the taiko-drum mode of osu! (mode 1). Objects scroll horizontally from the right to a fixed target; the player hits centre (don) and rim (kat) keys, rolls drum rolls and mashes swells.

Category: **others**. Justification: the playfield scrolls horizontally with only two input classes (don/kat) and no fixed key-count lanes, so it does not fit a vertical column model (ROX can only approximate it by remapping to 4 columns).

Format: `.osu` with `Mode: 1`, see [osu/](osu/README.md) (mode-specific encoding) and the canonical doc [vsrg/osu-mania/osu/README.md](../../vsrg/osu-mania/osu/README.md).

ROX: decode only (`TaikoDecoder`, 4-column conversion, not auto-detected).

Related: the arcade game Taiko no Tatsujin and its `.tja` fan format are in [../taiko-no-tatsujin/](../taiko-no-tatsujin/).

Links: https://osu.ppy.sh/wiki/en/Game_mode/osu%21taiko, https://github.com/ppy/osu/tree/master/osu.Game.Rulesets.Taiko
