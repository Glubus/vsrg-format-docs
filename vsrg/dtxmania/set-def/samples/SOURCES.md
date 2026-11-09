# Samples: DTXMania `set.def`

All three files are hand-written (`synthetic`). They are named `synthetic-*.def` here; DTXMania only reads a file called exactly `set.def`, so rename when testing.

## Committed

| File | Origin (URL, pinned commit) | Author | Licence | What it exercises |
| --- | --- | --- | --- | --- |
| `synthetic-auldlangsyne-set.def` | hand-written from the field table of https://dtxmania.net/documents/create-setdef (no text copied from that page) | this repository's maintainers (agent-authored) | CC0 / public domain (declared) | ASCII, LF. One song with three levels (`#TITLE`, `#FONTCOLOR`, `#L1LABEL`/`#L1FILE` ... `#L3FILE`) whose targets are the real files `auldlangsynemetal-bas.dtx`, `-adv.dtx`, `-ext.dtx` in `../../dtx/samples/`. |
| `synthetic-multi-song-set.def` | same | same | CC0 (declared) | ASCII, LF. Two songs separated by `#TITLE` lines (documented feature); first song has level 1 only and no labels (default names); second song mixes an explicit `#L1LABEL`, a level without label (`#L4FILE`, default "MASTER"), and `#L5LABEL`/`#L5FILE` with a relative sub-folder path using a backslash (`subdir\...`, as in the page's `ps2\...` example). Targets: `whispermint-ext.dtx`, `confessionfull-bas.dtx` exist in `../../dtx/samples/`; the `subdir\` ones do not. |
| `synthetic-sjis-set.def` | same | same | CC0 (declared) | **Shift_JIS (CP932), CRLF**, Japanese title and labels (`#L1LABEL: やさしい` ...), three levels with files that are not shipped. The page states the encoding may be Shift_JIS or UTF-8. |

No real `set.def` was found under an open licence (see the fiche).
