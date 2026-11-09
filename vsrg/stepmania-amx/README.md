# StepMania AMX

Category: vsrg: Pump-It-Up-oriented dance game (5/6/10 panel columns scrolling vertically); same note-column model as StepMania.

StepMania AMX (SMA) is a fork of StepMania 3.9 "focused in improving the gameplay experience" (GitHub organization [StepMania-AMX](https://github.com/StepMania-AMX)); the original README calls it a "pump-oriented fork of StepMania 3.95" and the StepMania wiki "a fork based on a fork of 3.9, with a particular focus on Pump it Up-related enhancements". The loader source credits Aldo Fregoso and Jason Felds (2009-2011). Its `.sma` format extends `.sm` with times in rows and per-chart timing, and was never widely adopted ("not widely supported"; upstream dispute: [stepmania/stepmania#1125 ".sma file support"](https://github.com/stepmania/stepmania/issues/1125)). StepMania 5 (master) and Etterna contain an `SMALoader`; the StepMania repository has no `.sma` writer (the `NotesWriterSMA.cpp` link of the original README returns 404). Pump Pack conversions in `KSF / SM / SMA / SSC` flavours are published by Team StepMasters (team-stepmasters.com).

Format folder: [`sma/`](sma/README.md).

The upstream list (`README.md` at commit `503382a`) also mentions DirectMove ("Found on the StepMania Wikia page for StepMania AMX"), a Pump simulator with KSF files, documented in [kick-it-up](../kick-it-up/README.md) and [legacy-dance-formats/directmove](../legacy-dance-formats/directmove/README.md). The fandom page returned HTTP 403.

Related: [StepMania family](../stepmania/README.md), [Kick It Up `.ksf`](../kick-it-up/ksf/README.md).

Links: https://github.com/StepMania-AMX, https://stepmania.fandom.com/wiki/Step_formats (sma vs sm), https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp, https://zenius-i-vanisher.com/v5.2/thread?threadid=3965.
