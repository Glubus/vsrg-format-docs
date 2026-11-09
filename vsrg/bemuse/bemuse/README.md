# Bemuse sound pack (`.bemuse` + `metadata.json`)
Kind: audio

Doc status: complete · ROX: no · Category: vsrg · Encoding: binary chunks + json index

## Overview
Bemuse's `.bemuse` format packs keysounds (converted to `.ogg`) into chunks of about 1.4 MB (`max = 1474560` bytes in the packer), so a BMS song streams in a few HTTP requests. A JSON index `metadata.json` maps each sound name to a byte range in a chunk. Charts stay `.bms/.bme/.bml/.bmson` next to it. `bemuse-tools` and the Bemuse Song Workshop produce it; the Bemuse client (HTML5, React, Redux, Pixi.js; GitHub `bemusic/bemuse`) reads it.

## Container & encoding

Two kinds of file:

1. `metadata.json` (index): UTF-8 JSON.
2. `<name>.<n>.<hash8>.bemuse` (data chunk): binary.

### `*.bemuse` chunk

| Offset | Size | Value |
|---|---|---|
| 0 | 10 | ASCII signature `BEMUSEPACK` |
| 10 | 4 | `uint32` little-endian length `L` of an optional metadata block (always `0` in files written by the current packer; the doc says "All zeroes (legacy reasons)") |
| 14 | `L` | metadata block (empty) |
| 14 + `L` | rest | payload: the sound files concatenated back to back |

The reader (`getPayload`) checks the signature (`Invalid magic number` otherwise), reads the 4-byte length, and slices the blob from `14 + L`. Byte ranges in `metadata.json` are relative to the payload start, so `file bytes = chunk[14 + start .. 14 + end]` (for `L = 0`).

### Chunk names

`<name>.<index>.<first 8 hex chars of payload md5>.bemuse`, where `<name>` is the pack name given to the packer (e.g. `oggs`) and `<index>` counts chunks per name starting from 1 (e.g. `oggs.0.f7f0e987.bemuse` in the documentation example). [The docs example starts at `.0`, the packer code counts from 1: both are shown in the sources; the index in the name is cosmetic since `metadata.json` holds the real paths.]

## Structure / metadata

`metadata.json`:

```ts
{
  files: Array<{ name: string; ref: [chunkIndex: number, start: number, end: number] }>
  refs:  Array<{ path: string; hash: string; size: number }>
}
```

| Field | Meaning |
|---|---|
| `files[].name` | Sound file name, e.g. `snare.ogg`. Client lookup is case-insensitive (`name.toLowerCase()`). |
| `files[].ref[0]` | Index into `refs` (which chunk). |
| `files[].ref[1]` | Start offset in the chunk payload. |
| `files[].ref[2]` | End offset (exclusive, as in `Blob.slice`). |
| `refs[].path` | URL of the chunk relative to `metadata.json`. |
| `refs[].hash` | MD5 (hex) of the chunk payload as produced by the packer (`Payload.hash`; the Bemuse docs call it "MD5 hash of the chunk file content"). |
| `refs[].size` | Size in bytes (documented; the packer shown writes only `path`/`hash`, readers ignore `size`). |

## Timing model
Unknown (no chart data).

## Notes
Unknown.

## Audio & images
OGG Vorbis only (converted from BMS `.wav/.ogg` by SoX/ffmpeg). Images and video are not packed (see `bemuse-data/eyecatch_image`, `back_image`, `bga`, [`bemuse-song.json`](../bemuse-song-json/README.md)). Retrieval: look up the entry by name, read `ref`, fetch `refs[ref[0]].path`, take `.slice(ref[1] + 14, ref[2] + 14)`.

## Versions & variants
- Legacy music server: `<server>/<song>/assets/metadata.json` + `assets/*.bemuse`; default `bemusepack_url` is `assets/metadata.json`.
- Song Workshop: pack in `bemuse-data/sound/`; `bemusepack_url` in `bemuse-song.json` may point elsewhere or be `null` (use real files).
- The 4-byte header length is the only extension point; no version number.

## Quirks & pitfalls

- Offsets in `metadata.json` exclude the 14-byte header; add 14 (or `14 + L`).
- `refs[].hash` is the payload MD5, so hashing the whole `.bemuse` file cannot verify it.
- Lookup is case-insensitive; two sounds differing only by case collide.
- Files are not individually compressed (already OGG).

## Example

From the Bemuse docs (`website/docs/bemusepack.md`):

```json
{
  "files": [
    { "name": "beat.ogg", "ref": [0, 0, 1596631] },
    { "name": "bgm.ogg", "ref": [1, 0, 1574274] },
    { "name": "synth.ogg", "ref": [2, 0, 1350505] },
    { "name": "cymbal.ogg", "ref": [2, 1350505, 1415370] },
    { "name": "snare.ogg", "ref": [2, 1415370, 1430427] }
  ],
  "refs": [
    { "path": "oggs.0.f7f0e987.bemuse", "hash": "f7f0e987c5b9070b29d66b74c4b77609", "size": 1596645 },
    { "path": "oggs.1.03981ebc.bemuse", "hash": "03981ebc7f52705fb44063de5a79930b", "size": 1574288 },
    { "path": "oggs.2.8ed2dece.bemuse", "hash": "8ed2dece0eef7cd65195d7ef6a72708d", "size": 1430441 }
  ]
}
```

(`size` = payload length + 14: `1596631 + 14 = 1596645`.)

## ROX support
Not read (ROX 0.8.1 does not read BMS).

## Parsers & tools

- Bemuse client (TypeScript): [`bemuse/src/resources/bemuse-package.ts`](https://github.com/bemusic/bemuse/blob/master/bemuse/src/resources/bemuse-package.ts).
- Packer (JavaScript): [`packages/bemuse-tools/src/bemuse-packer.js`](https://github.com/bemusic/bemuse/blob/master/packages/bemuse-tools/src/bemuse-packer.js), [`payload.js`](https://github.com/bemusic/bemuse/blob/master/packages/bemuse-tools/src/payload.js); Song Workshop https://github.com/bemusic/song-workshop.
- Format doc: [`website/docs/bemusepack.md`](https://github.com/bemusic/bemuse/blob/master/website/docs/bemusepack.md).

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md) (indexes only, no `.bemuse` chunks). Every song of `https://bemuse.ninja/music/index.json` has `<song>/assets/metadata.json`, whose `refs[].path` names the chunks (`ogg.N.<hash>.bemuse`, `m4a.N.<hash>.bemuse`) beside it. To pack your own BMS use the Song Workshop or `bemuse-tools`.

## Sources

- https://github.com/bemusic/bemuse (commit `4bf3e7d98a44841b323741cc403ecb7b41618ade`): `website/docs/bemusepack.md`, `website/docs/music-server.md`, `website/docs/song-workshop.md`, `bemuse/src/resources/bemuse-package.ts`, `packages/bemuse-tools/src/bemuse-packer.js`, `packages/bemuse-tools/src/payload.js`, `packages/bemuse-types/index.d.ts`
