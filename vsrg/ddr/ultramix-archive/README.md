# DDR Ultramix archives (`x_data_US.bin`, `music_US.sng`, `.sif`)
Kind: package

Doc status: complete for the US release (EU/other mixes partly unknown) · ROX: no · Category: vsrg · Encoding: binary (little-endian, sector-aligned archives)

## Overview

DDR Ultramix (Xbox, 2003; Europe: *Dancing Stage Unleashed*) packs assets in two flat archives next to `default.xbe`: `x_data_US.bin` (charts, textures, song info, animation data) and `music_US.sng` (audio). The charts are legacy [SSQ](../ssq/README.md) files (`<id>_all.ssq`, TPS 75 or 150). skogaby reverse engineered the US layouts (`ddr-chart-tools/docs/ultramix_archive_formats.md`, extractor `scripts/extract_ultramix_data.py`). The EU release has different offsets; Ultramix 2/3/4 were not investigated.

```
default.xbe       game executable (contains the x_data table of contents as static data)
x_data_US.bin     textures, charts, song info, animation data, ...
music_US.sng      audio streams (XBOX-IMA ADPCM, 44.1 kHz stereo, headerless)
```

Both archives are sector-aligned to 0x800 (2048 bytes).

## Container & encoding

### `x_data_US.bin`

A concatenation of sector-aligned payloads with no header. The table of contents is a static array of 16-byte little-endian entries in the XBE.

| Parameter | US | EU |
|---|---|---|
| TOC file offset in `default.xbe` | `0x1AD890` | `0x1B06B0` |
| entry count (upper bound; loop bound `CMP ESI, 0x2E10`, `0x2E10 / 0x10`) | 737 | 737 |
| string VA -> file delta | `0xE780` | `0xE780` |

```c
struct x_data_entry {
    uint32_t name_va;       // +0x00 VA of NUL-terminated filename in the XBE .rdata
    uint32_t size;          // +0x04 actual file size
    uint32_t size_aligned;  // +0x08 size rounded up to the next 0x800
    uint32_t offset;        // +0x0C byte offset in the bin (0x800-aligned)
};
```

`name_file_offset = name_va - 0xE780`; names are ASCII. The game rejects names containing `\` (flat archive), compares case-insensitively (`_stricmp`) and scans linearly. A few entries are fully zero (e.g. the `all.ssq` sentinel); skip them. For all 737 entries `size_aligned == roundup(size, 0x800)`.

Contents (US, 737 entries, ~126 MB): `.tga` 249 (uncompressed 32-bit BGRA textures), `.dds` 231, `.ssq` 60 (legacy DDR charts, TPS 75 or 150), `.csv` 54 (per-song background animation / stage direction), `.sif` 51 (song info), `.act` 33 (animation curves), `.ani` 27 (character animations), `.bmp` 22, `.txt` 3, `.pd` 3 (particle scripts), `.ddm` 2 (unknown), `.xpu` 2 (pixel shader blobs).

Per-song group (4-character song id, e.g. `abs2`): `{id}.sif`, `{id}.csv`, `{id}_all.ssq`, `{id}_bk.dds/.tga` (background), `{id}_tb.dds/.tga` (banner), `{id}_th.dds/.tga` (thumbnail). Some songs have extra SSQs (`_org_all.ssq`, `_all_chris.ssq`).

### `music_US.sng`

The TOC is inline at the start of the file:

```
+0x0000  u32  entry_count N
+0x0004  N x 20-byte entries
+0x0800  payload data (sector-aligned); entry 0 payload starts at 0x800
```

```c
struct sng_entry {
    char     tag[4];       // +0x00 4 ASCII chars (compared as a u32)
    uint32_t offset;       // +0x04 file offset of the main stream (0x800-aligned)
    uint32_t size;         // +0x08 main stream size
    uint32_t loop_offset;  // +0x0C file offset of the preview-loop stream (0 if none)
    uint32_t loop_size;    // +0x10 preview-loop stream size (0 if none)
};
```

Entries with `loop_* == 0` are UI/non-song audio (tags `uime`, `uire`, `uigo`, `uisp`, `uirc`, `intr`, `inus`, `inuk`, `cred`, `live`). Entries with `loop_* != 0` are songs: `main` = full track, `loop` = ~8-second preview that loops on the song wheel. The tag equals the song id used by the `.sif`/`.ssq`/texture file names. The game reads the first sector once, keeps it resident and scans linearly, comparing the tag as a u32.

Audio: headerless XBOX-IMA ADPCM, stereo, 44.1 kHz, block size 0x48 bytes (64 samples per channel); stream sizes are exact multiples of 0x48.

### `.sif` (song info)

NUL-terminated ASCII strings at fixed indices, zero-padded to a fixed size (typically 512-1024 bytes). The file begins with a single empty leader field (one NUL byte); content starts at index 1:

| Index | Content (example) |
|---|---|
| 0 | empty leader (single NUL) |
| 1 | short id, e.g. `abs2` (matches the `.sif` file prefix and the `.sng` tag) |
| 2 | title, e.g. `ABSOLUTE` |
| 3 | subtitle, e.g. `Cuff -N- Stuff it Mix` (may be empty) |
| 4 | artist, e.g. `Thuggie D.` |
| 5+ | NUL padding |

## Structure / metadata

Chart data is SSQ ([`../ssq`](../ssq/README.md)): legacy TPS (75/150), non-zero `time_offset[0]`, chunk types 1/2/3 plus auxiliary. Conversions pair `abs2_all.ssq` with `abs2.wavm` (same XBOX-IMA stream).

## Timing model

As SSQ, with per-file TPS and the legacy origin shift (`time_offset[0]`): [`../ssq`](../ssq/README.md).

## Notes

As SSQ: 4-panel steps, freezes, shocks, no mines.

## Audio & images

`.sng` streams as above; textures `.tga`/`.dds`/`.bmp`.

## Versions & variants

US vs EU: same structure, different TOC offsets in `default.xbe`. Ultramix 2/3/4: unknown.

## Quirks & pitfalls

- The TOC is in the executable, not the bin: an extractor needs the XBE-specific offset and the VA -> file delta.
- Sizes are padded to 0x800 sectors; use `size`, not `size_aligned`.
- `.sng` tags are 4-char keys compared as an integer, so case matters for tags but not for `x_data` names.
- Some TOC entries are zeroed sentinels.

## Example

None; layouts above come from the spec.

## ROX support

Not read by ROX.

## Parsers & tools

[`skogaby/ddr-chart-tools`](https://github.com/skogaby/ddr-chart-tools) (Rust, with `scripts/extract_ultramix_data.py` and `src/wavm`, `src/ssq_legacy`): extraction + legacy SSQ -> SSC/DDR conversion. TCRF documents offsets of known content using the same "relative to `x_data_US.bin`" phrasing (per the spec).

## Getting samples

No sample: the archive is a 100+ MB Xbox asset pack and the tool repository has no fixture. Rip the Ultramix (Xbox, US) disc, take `default.xbe`, `x_data_US.bin` and `music_US.sng`, and run `scripts/extract_ultramix_data.py` of [skogaby/ddr-chart-tools](https://github.com/skogaby/ddr-chart-tools) (commit `a733404f43427bfc7b9dea3cae67710149767993`) to get the `<id>_all.ssq` charts.

## Sources

- https://github.com/skogaby/ddr-chart-tools/blob/main/docs/ultramix_archive_formats.md
- https://github.com/skogaby/ddr-chart-tools (README, `src/`, `docs/`)
