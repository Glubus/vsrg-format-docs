# StepMania AMX

Category: **vsrg**: Pump-It-Up-oriented dance game (5/6/10 panel columns scrolling vertically); same note-column model as StepMania.

StepMania AMX (SMA) is a fork of StepMania 3.9 "focused in improving the gameplay experience" (its GitHub organization [StepMania-AMX](https://github.com/StepMania-AMX)); the original README of this repository calls it a "pump-oriented fork of StepMania 3.95" and the StepMania wiki "a fork based on a fork of 3.9, with a particular focus on Pump it Up-related enhancements". The loader source credits Aldo Fregoso and Jason Felds (2009-2011). Its `.sma` file format is an extension of `.sm` in which times can be given in **rows** and charts can carry their own timing; it was never adopted widely ("not widely supported"; an upstream dispute is cited in [stepmania/stepmania#1125 ".sma file support"](https://github.com/stepmania/stepmania/issues/1125)). StepMania 5 (master) and Etterna contain an `SMALoader`; there is **no `.sma` writer** in the StepMania repository (the `NotesWriterSMA.cpp` link of the original README returns 404). Pump Pack conversions in `KSF / SM / SMA / SSC` flavours are published by Team StepMasters (team-stepmasters.com).

Format folder: [`sma/`](sma/README.md).

The ORIGINAL_README also mentions **DirectMove** with a link to the StepMania Wikia page for StepMania AMX ("Found on the StepMania Wikia page for StepMania AMX"); DirectMove is a Pump simulator with KSF files and is documented in [kick-it-up](../kick-it-up/README.md) and [legacy-dance-formats/directmove](../legacy-dance-formats/directmove/README.md). The fandom page itself could not be fetched (HTTP 403).

Related: [StepMania family](../stepmania/README.md), [Kick It Up `.ksf`](../kick-it-up/ksf/README.md).

Links: https://github.com/StepMania-AMX, https://stepmania.fandom.com/wiki/Step_formats (sma vs sm), https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSMA.cpp, https://zenius-i-vanisher.com/v5.2/thread?threadid=3965.
