# Kick It Up (KIU) and Direct Move

Category: **vsrg**: Pump It Up style 5-panel (diagonal + centre) dance game; arrows scroll vertically along fixed panel columns.

Kick It Up is a PC simulator of Andamiro's Pump It Up whose step files carry the `.ksf` extension ("Kick It Up Step File"; the format "was originally used in the Kick It Up simulator, but can also be parsed by other programs", per the format notes of Joe Wreschnig written for pydance and kept in StepMania's `Docs/SimfileFormats/KSF/ksf-format.txt`). Korean communities then moved to **Direct Move**, a simulator by "Kiho" (a programmer and chart producer) that removed the 3-shift limit and added rapid shifting; Direct Move extended `.ksf` with a "new grammar" (`|T`, `|B`, `|E`, `|D`, ... control rows and `#BPM2/#BPM3/#BUNKI/#STARTTIME2/#STARTTIME3` headers, see the format page). Later communities converted to StepMania `.sm/.ssc/.sma` instead (the Spanish "Team StepMasters" distribute Pump It Up packs in `KSF / SM / SMA / SSC` and a converter `STX2DM`, from Pump It Up's `STX` data to Direct Move `.ksf`, exists in the StepMania-AMX GitHub organization).

Format folder: [`ksf/`](ksf/README.md) (`.ksf`, including the Direct Move dialect; Direct Move is also indexed in [legacy-dance-formats/directmove](../legacy-dance-formats/directmove/README.md)).

Related: [Pump It Up](../pump-it-up/README.md) (`.ucs`), [StepMania AMX `.sma`](../stepmania-amx/sma/README.md), [StepMania family](../stepmania/README.md).

Links: https://github.com/stepmania/stepmania/blob/master/Docs/SimfileFormats/KSF/ksf-format.txt, https://github.com/syspro86/directmove (Direct Move / KSF Creator downloads), https://github.com/StepMania-AMX/STX2DM, https://team-stepmasters.com/ (KSF/SM/SMA/SSC conversions of Pump It Up releases).
