# Pump It Up (Andamiro)

Category: vsrg: five-panel (down-left, up-left, centre, up-right, down-right; double = 10) dance game with notes scrolling vertically to a receptor row.

Pump It Up (Andamiro, Korea, 1999-; series: 1st..Premiere, Prex, Exceed, Zero, NX/NX2/NXA, Fiesta/Fiesta EX/2, Prime/Prime 2, XX, Phoenix, ...) is the main DDR competitor. Its arcade step data is proprietary and undocumented here. The community knows an `STX` step format ("Pump It Up's STX format"), converted to Direct Move `.ksf` by [StepMania-AMX/STX2DM](https://github.com/StepMania-AMX/STX2DM); no specification was found.

| Format | Role | Folder |
|---|---|---|
| `.ucs` | Andamiro's official User Custom Step: text chart format of the UCS system (player-made charts on the arcade, uploaded to piugame.com "UCS Share"); edited with StepEdit Lite or third-party editors (VainUCS, PIUUCSMaker) | [ucs](ucs/README.md) |
| `.ksf` | Kick It Up / Direct Move step files, the community lingua franca for Pump charts (PIU rips) | [../kick-it-up](../kick-it-up/ksf/README.md) |
| `.sma` | StepMania AMX | [../stepmania-amx](../stepmania-amx/sma/README.md) |
| `.sm`/`.ssc` | StepMania `pump-single/halfdouble/double/couple/routine`; StepF2/StepP1 forks and OutFox's PIU loader; Pump It Up Pro/Infinity (official titles on StepMania) | [../stepmania](../stepmania/README.md) |

Searched without finding public documentation: `.pump` or `.nx` Andamiro files, "Pump It Up Pro" chart files (they are StepMania `.sm`/`.ssc`), "PIU Phoenix" data. UCS tooling and community: https://www.piugame.com/ (UCS Share), https://piuforge.com/tools/vain-ucs, https://www.pumpproplus.com/ (UCS base list).

Related: [Kick It Up](../kick-it-up/README.md), [StepMania AMX](../stepmania-amx/README.md).

Parser-derived pages (from UCSConverterTool and STX2DM): [`stx/`](stx/README.md) (`.stx`, magic `STF4`), [`not/`](not/README.md) (`.not` NOT4 and `.not5`).
