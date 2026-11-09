# RB package (`.rb`, Reflec Beat plus iOS song package)
Kind: package

Doc status: stub · ROX: no · Category: others · Encoding: archive (zip with Blowfish-encrypted entries)

## Overview

`.jbt`, `.orb` and `.rb` are the song packages of the Konami iOS BEMANI games: `.jbt` for jubeat plus / jukebeat (also Android jubeat plus), `.rb` for Reflec Beat plus / Rb+, `.orb` for pop'n rhythmin. All are zip files with a non-standard extension; every file inside is encrypted. The content below comes from SaxxonPike's `rhythm-game-formats` repository.

## Container & encoding

- Zip; every entry is encrypted with Blowfish (class `BFCodec` in all games, including the Android C++ build) using custom P and S boxes; the IV appears static.
- At least two keys exist, computed as `md5(unobfuscated_string)`, where the string is un-obfuscated from a table in the binary with `unobfuscated[i] = obfuscated[i] + i` (26 characters for one key, 22 + 7 added to each result for the alternate key). The repo does not disclose known keys/IVs.
- Each entry has 8 trailing verification bytes (apparently offsets; the last 4 bytes hold the start of the verification bytes); the decryptor strips them first.
- Images are Apple-optimised PNG (needs `pngdefry`).

## Structure / metadata

Entries in a Reflec Beat package:

| Entry | Content |
|---|---|
| `info` | XML property list: title, artist, etc. |
| `bgm` | M4A (AAC) song |
| `pre` | preview M4A |
| `artwork`, `artwork_2x` | cover (PNG, `_2x` retina) |
| `artist_b`, `artist_b2x`, `artist_w`, `artist_w2x` | artist images (assumed) |
| `title_b`, `title_b2x`, `title_w`, `title_w2x` | title card images |
| `note_bas`, `note_med`, `note_har` | charts for Basic, Medium, Hard |

"For note format files, it is generally assumed that the notes themselves are encoded the same way as their arcade counterparts, except in separate files." The decoded chart layout is **Unknown** here.

## Timing model

Unknown.

## Notes

Unknown.

## Audio & images

`bgm` and `pre` are AAC; images are PNG (see above).

## Versions & variants

Shared package scheme with jubeat plus (`seq_bas`, `seq_adv`, `seq_ext`, `index`, `name_b`, `name_w`, `artwork_s`) and pop'n rhythmin (`sheet_n`, `sheet_h`, `sheet_ex`, `title_2x`, `artist_2x`).

## Quirks & pitfalls

Encrypted payload, verification trailer, Apple PNG variant. For `.acv` (pop'n rhythmin) files see the source repo.

## Example

Unknown.

## ROX support

Not read by ROX.

## Parsers & tools

None found for the chart payload. Blowfish decryption routines exist in community BEMANI tools (not opened).

## Getting samples

Committed: nothing. Reflec Beat plus is a commercial Konami iOS game, every package entry is Blowfish-encrypted, and the documenting repository (SaxxonPike/rhythm-game-formats `ios/jbt-rb-orb.md`) does not disclose the keys; no public copy was found.

How to get one [inference]: take the package from a device or backup that still has the game, unzip a song `.rb` (entries `info`, `bgm`, `pre`, `note_bas`, `note_med`, `note_har`, ...) and decrypt the entries with keys recovered from the app binary as the repository describes. The decoded chart layout is Unknown.

## Sources

- <https://github.com/SaxxonPike/rhythm-game-formats/blob/master/ios/jbt-rb-orb.md> (read)
