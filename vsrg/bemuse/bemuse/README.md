# Bemuse sound pack (`.bemuse` + `metadata.json`)
Kind: audio

Doc status: complete · ROX: no · Category: vsrg · Encoding: binary chunks + json index

## Overview

Bemuse is a web-based BMS/bmson player (HTML5, React, Redux, Pixi.js; GitHub `bemusic/bemuse`). A BMS archive can contain hundreds or thousands of keysound files; serving them one by one over HTTP is slow and one big ZIP is too large to retry. The **`.bemuse` file format** is Bemuse's answer: keysounds converted to `.ogg` are concatenated into **chunks of about 1.4 MB** (`max = 1474560` bytes in the packer), each chunk written as a `*.bemuse` file, with a JSON index `metadata.json` that maps each sound name to a byte range inside a chunk. It is a sound-asset container only; the charts remain `.bms/.bme/.bml/.bmson` files next to it. Produced by `bemuse-tools` (CLI) and by the Bemuse Song Workshop web app; consumed by the Bemuse client.

## Container & encoding

Two kinds of file:

1. `metadata.json` (index): UTF-8 JSON.
2. `<name>.<n>.<hash8>.bemuse` (data chunk): binary.

### `*.bemuse` chunk

| Offset | Size | Value |
|---|---|---|
| 0 | 10 | ASCII signature `BEMUSEPACK` |
| 10 | 4 | `uint32` **little-endian** length `L` of an optional metadata block (always `0` in files written by the current packer; the doc says "All zeroes (legacy reasons)") |
| 14 | `L` | metadata block (empty) |
| 14 + `L` | rest | **payload**: the sound files concatenated back to back |

The reader (`getPayload`) checks the signature (`Invalid magic number` otherwise), reads the 4-byte length, and slices the blob from `14 + L`. Byte ranges in `metadata.json` are relative to the **payload start**, so `file bytes = chunk[14 + start .. 14 + end]` (for `L = 0`).

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
| `files[].name` | Sound file name, e.g. `snare.ogg`. Lookup in the client is **case-insensitive** (`name.toLowerCase()`). |
| `files[].ref[0]` | Index into `refs` (which chunk). |
| `files[].ref[1]` | Start offset in the chunk **payload**. |
| `files[].ref[2]` | End offset (exclusive, as in `Blob.slice`). |
| `refs[].path` | URL of the chunk relative to `metadata.json`. |
| `refs[].hash` | MD5 (hex) of the chunk **payload** as produced by the packer (`Payload.hash`; the Bemuse docs call it "MD5 hash of the chunk file content"). |
| `refs[].size` | Size in bytes (documented; the packer shown writes only `path`/`hash`, readers ignore `size`). |

## Timing model

Not applicable (no chart data).

## Notes

Not applicable.

## Audio & images

Audio only: OGG Vorbis files (converted from the BMS `.wav/.ogg` keysounds by SoX/ffmpeg during packing). Images and video are not packed (see the song workshop for `bemuse-data/eyecatch_image`, `back_image`, `bga`, [`bemuse-song.json`](../bemuse-song-json/README.md)).

Retrieval recipe from the docs: look up the entry by name, read `ref`, fetch `refs[ref[0]].path`, take `.slice(ref[1] + 14, ref[2] + 14)`.

## Versions & variants

- Legacy "music server" layout: `<server>/<song>/assets/metadata.json` + `assets/*.bemuse`; default `bemusepack_url` is `assets/metadata.json`.
- Song Workshop ("new method"): keysound pack in `bemuse-data/sound/` (the guide shows `bemuse-data/sound` with optimised files), `bemusepack_url` in `bemuse-song.json` may point elsewhere or be `null` to use real files.
- The 4-byte header length field is the only extensibility point; no known version number.

## Quirks & pitfalls

- Offsets in `metadata.json` do **not** include the 14-byte header; add 14 (or `14 + L`).
- The `hash` in `refs` is the payload MD5, so it cannot be verified by hashing the whole `.bemuse` file.
- Names are case-insensitive for lookup; two sounds differing only by case collide.
- Files are not individually compressed (they are already OGG).

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

Not read by ROX (it is a keysound container for BMS, which ROX 0.8.1 does not read yet).

## Parsers & tools

- Bemuse client (TypeScript): [`bemuse/src/resources/bemuse-package.ts`](https://github.com/bemusic/bemuse/blob/master/bemuse/src/resources/bemuse-package.ts).
- Packer (JavaScript): [`packages/bemuse-tools/src/bemuse-packer.js`](https://github.com/bemusic/bemuse/blob/master/packages/bemuse-tools/src/bemuse-packer.js), [`payload.js`](https://github.com/bemusic/bemuse/blob/master/packages/bemuse-tools/src/payload.js); Song Workshop https://github.com/bemusic/song-workshop.
- Format doc: [`website/docs/bemusepack.md`](https://github.com/bemusic/bemuse/blob/master/website/docs/bemusepack.md).

## Getting samples

- **Committed** ([`samples/`](samples/)): `bemuse-test-a-metadata.json`, the `metadata.json` index of the Bemuse test fixture (AGPL-3.0).
- **Fetched by `tools/fetch-samples.sh`** (not committed because the chunks contain audio): the two test `.bemuse` chunks (`bemuse/src/resources/test-fixtures/a|b/mp3.0.ea6087c3.bemuse`, pinned at commit `4bf3e7d98a44841b323741cc403ecb7b41618ade`). A real production pack (`metadata.json` and chunk `m4a.5.18649bde.bemuse` of `[flicknote]onlylove_remix`, CC-BY-NC) is on live URLs, not hashable, fetch manually.
- **More**: any song of the official server `https://bemuse.ninja/music/` has `<song>/assets/metadata.json` whose `refs[].path` lists the `.bemuse` chunks next to it (`ogg.N.<hash>.bemuse`, `m4a.N.<hash>.bemuse`); the song list is `https://bemuse.ninja/music/index.json`. To produce one from your own BMS, use the Bemuse Song Workshop or `bemuse-tools` packer (see Parsers & tools).

## Sources

- https://github.com/bemusic/bemuse (commit `4bf3e7d98a44841b323741cc403ecb7b41618ade`): `website/docs/bemusepack.md`, `website/docs/music-server.md`, `website/docs/song-workshop.md`, `bemuse/src/resources/bemuse-package.ts`, `packages/bemuse-tools/src/bemuse-packer.js`, `packages/bemuse-tools/src/payload.js`, `packages/bemuse-types/index.d.ts`
