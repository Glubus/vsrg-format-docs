# StepMania Micro (SM Micro)

Category: **vsrg**: 4-lane DDR-style arrow game (HTML/CSS/JavaScript); notes scroll vertically along 4 fixed columns.

StepMania Micro was an experiment "to see how StepMania implemented in HTML/CSS/JavaScript would work", hosted by Chris Danford's StepMania site (`old.stepmania.com/wiki/StepMania_Micro`; browsers Chrome/Safari/Firefox 4/IE9/Opera 11; Wayback Machine, 2014-2015) with its own song list (`browse.php?micro=1`). The game is plain JS (`smjs-0.3`: `js/song.js`, `js/steps.js`, `js/stepmania.js`, jQuery 1.5.1). A song folder holds `background.png`, `<name>.mp3/.ogg`, `song.js` (`{bpm, addToMusicPosition}`) and `steps.js` (`noteData`). The note data uses the same serialization as StepMania's `NotesWriterJson`/`NotesLoaderJson` (note tuples `[beat, track, {tapnote}]`). See [`json/`](json/README.md).

Links: https://web.archive.org/web/20150110063934/http://old.stepmania.com/wiki/StepMania_Micro (page), https://web.archive.org/web/20150110120332if_/https://dl.dropboxusercontent.com/u/2963913/smjs-0.3/index.html (page source: view source), StepMania's [NotesLoaderJson.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderJson.cpp) / [NotesWriterJson.cpp](https://github.com/stepmania/stepmania/blob/master/src/NotesWriterJson.cpp).

Related: [StepMania family](../stepmania/README.md).
