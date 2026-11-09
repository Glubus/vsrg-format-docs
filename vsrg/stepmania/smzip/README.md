# StepMania package (`.smzip`)
Kind: package

Doc status: complete · ROX: no · Category: vsrg · Encoding: archive (ZIP)

## Overview

`.smzip` is StepMania's **distribution package** for songs, courses, note skins, themes, announcers, etc. It is an ordinary **ZIP archive** whose entries already carry the install-relative paths (`Songs/<Group>/<Song>/song.ssc`, `Songs/<Group>/<Song>/song.ogg`, `Themes/<Theme>/...`), plus an optional INI control file `smzip.ctl`. It exists because song packs (a "pack" is `Songs/<Group>/` with many song folders) are shared as a single file in the StepMania/ITG/Etterna/OutFox communities (Zenius-I-Vanisher, StepMania Online, Team Stepmasters...). Many packs on the web are plain `.zip` with the same layout; StepMania treats `.zip` and `.smzip` identically when installing. The format is not a chart format: charts are the `.sm`/`.ssc`/`.dwi`/... files inside. It is documented only by the StepMania source (`smpackage` tool, `ScreenInstallOverlay`).

## Contents

- Songs (`Songs/<Group>/<Song>/`), themes and other install-relative files in a ZIP.
- Chart formats inside: [`.sm`](../sm/README.md), [`.ssc`](../ssc/README.md); courses: [`.crs`](../crs/README.md).

## Container & encoding

- ZIP (deflate or stored). Entries are stored with **Windows-style relative paths** when written by the `smpackage` tool ("Must use backslashes in the path, or else WinZip and WinRAR don't see the files", source comment); readers should accept both `\` and `/`.
- Compression: the exporter stores media that is already compressed without deflate (`ogv avi mpeg mpg mp3 oga ogg gif jpg jpeg png` -> `Z_NO_COMPRESSION`) and deflates everything else with `Z_BEST_COMPRESSION`.
- The ZIP **global comment** carries a free text comment entered by the packager ("DontAskForComment" preference suppresses the prompt).
- Exporter ignore list (`SMPackageUtil::StripIgnoredSmzipFiles`): paths ending with `smzip.ctl`, `.old`, `Thumbs.db`, `.DS_Store`, and any path containing `CVS`; package detection also skips `.svn`.
- The in-game exporter `ScreenOptionsExportPackage::ExportPackage` is dead code: its body is commented out ("totally doesn't work") and returns `false`. Real `.smzip` files come from the Windows `smpackage` tool (`SmpackageExportDlg.cpp`) or from hand-zipping.

## Structure / metadata

### Archive layout

```
smzip.ctl                      (optional control file, see below)
Songs/<Group>/<Song folder>/<files...>
Courses/<Group>/<name>.crs
NoteSkins/<game>/<noteskin>/...
Themes/<Theme>/...
...
```

Package directory rule (`SMPackageUtil::GetPackageDirectory`): for most top-level directories the package is the first **two** path components (`Themes/Default`), for `Songs` and `NoteSkins` the first **three** (`Songs/Group/Song`, `NoteSkins/dance/default`). Entries under CVS/.svn are ignored.

### `smzip.ctl` (INI)

Written by `smpackage`, read by the Windows installer's `CheckPackages`:

```
[SMZIP]
Version=1
[Packages]
NumPackages=<n>
0=<package dir 0>
1=<package dir 1>
...
```

- `Version` must equal `1`, otherwise the control file is ignored.
- `Packages` lists the package directories contained in the archive (backslash separated, as produced by `GetPackageDirectory`); the installer uses them to offer **uninstalling older copies** of the same package before extracting (it checks that each directory exists and passes `IsValidPackageDirectory`).
- The game itself (`InstallSmzip`) does not read `smzip.ctl`: it just skips files with extension `ctl`.

## Timing model

Not applicable (container).

## Notes

Not applicable. Charts are inside the contained simfiles ([`.sm`](../sm/README.md), [`.ssc`](../ssc/README.md), `.dwi`, `.ksf`, ...).

## Audio & images

Everything (audio, banners, backgrounds, videos) is carried as ordinary files inside the song folders; see the simfile docs for how they are referenced.

## Versions & variants

- **Control file version 1** is the only one in the source.
- Encrypted packages exist: StepMania AMX's download index serves `PNEXT2.smzip`, a theme package whose entries (including `smzip.ctl` and `smzip.sig`) are WinZip-AES encrypted (ZIP method 99, flag bits 0x801, zip comment `PNEXT2`) [observed 2026-11-09 on the live URL `https://download.stepmania.amx.io/PNEXT2.smzip`, not in samples]; the key is unknown, so such packs cannot be listed or installed by generic tools.
- `.smzip` vs `.zip`: same handling. `ScreenPackages::RefreshPackages` lists `Packages/*.zip` and `Packages/*.smzip` (the in-game package downloader stores downloads in `Packages/`).
- Virtual mount: at startup StepMania scans the packages directory (`SpecialFiles::PACKAGES_DIR`) recursively for `*.zip` and `*.smzip` and **mounts each one as a virtual file system at `/`** (`StepMania.cpp`, `MountTreeOfZips`), so songs inside an archive can be played without installing.
- Install through the OS (double-click / command line argument) goes through `ScreenInstallOverlay::DoInstalls`: every argument ending in `.smzip` or `.zip` is mounted (`/@temp-zip/`), every file except `*.ctl` is copied to its path relative to the StepMania data dir (directories created as needed), and the "play after launch" target is deduced from the directory (`Songs/<Group>/<Song>` -> that song; `Themes/<Theme>` -> that theme).

## Quirks & pitfalls

- A pack inside a ZIP must keep the `Songs/<Group>/<Song>/` prefix, otherwise the installer copies files to the wrong place; some community archives have an extra wrapper folder.
- Backslash paths in older packs; ZIP filename charsets (CP437/Shift-JIS) are often wrong for non-ASCII song names.
- `smzip.ctl` is purely optional and must not be copied into the install tree.

## Example

Illustrative, hand-built from the `smpackage` export code (`SmpackageExportDlg.cpp`), for an archive holding one song `Songs/My Pack/Song A/`:

```
smzip.ctl:
[SMZIP]
Version=1
[Packages]
NumPackages=1
0=Songs\My Pack\Song A
```

## ROX support

Not read by ROX (ROX opens individual `.sm`/`.ssc` files, not archives).

## Parsers & tools

- StepMania (C++): [`ScreenInstallOverlay.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/ScreenInstallOverlay.cpp) (installer), [`smpackage/`](https://github.com/stepmania/stepmania/tree/5_1-new/src/smpackage) (Windows export/install tool, `SmpackageExportDlg.cpp`, `SMPackageInstallDlg.cpp`, `SMPackageUtil.cpp`), [`StepMania.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/StepMania.cpp) (zip mounting), [`ScreenPackages.cpp`](https://github.com/stepmania/stepmania/blob/5_1-new/src/ScreenPackages.cpp) (downloader).
- Any ZIP library can read/write it.

## Getting samples

Committed in [`samples/`](samples/SOURCES.md): two **synthetic, audio-less** rebuilds (Python `zipfile`): a plain-ZIP pack with the Springtime chart only, and an `smpackage`-style archive with `smzip.ctl`, backslash entry names, the Springtime chart and `Courses/Default/Jupiter.crs`. They cannot be played (no music).

Not in the manifest: no small open real `.smzip` has an immutable URL. Candidates observed on 2026-11-09: `PNEXT2.smzip` (6 MB theme package, live at `https://download.stepmania.amx.io/PNEXT2.smzip`, no Wayback copy; its entries are **WinZip-AES encrypted** (ZIP method 99, flag bits 0x801), including `smzip.ctl` and `smzip.sig`, zip comment `PNEXT2`), `PiuSMNX2_RDX.smzip` (114 MB), and StepMix 1.0 (`stepmix-1.0.smzip`, 256 MB, hosted by [simfilearchive.dev](https://simfilearchive.dev/), mixed per-song licences). To get one: build it with the Windows `smpackage` tool shipped with StepMania 3.9-5.x (Export As Smzip: pick a song folder, answer the comment prompt), or zip a `Songs/<Group>/<Song>/` tree yourself (any `.zip` works); real song packs are listed at [simfilearchive.dev](https://simfilearchive.dev/).

## Sources

- https://github.com/stepmania/stepmania/blob/5_1-new/src/smpackage/SmpackageExportDlg.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/smpackage/SMPackageInstallDlg.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/smpackage/SMPackageUtil.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/ScreenInstallOverlay.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/ScreenOptionsExportPackage.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/ScreenPackages.cpp
- https://github.com/stepmania/stepmania/blob/5_1-new/src/StepMania.cpp
