# Bemuse song metadata and music server index (`bemuse-song.json`, `index.json`)
Kind: metadata

Doc status: complete · ROX: no · Category: vsrg · Encoding: json

## Overview
Two JSON files give Bemuse ready-made song metadata:

- `bemuse-song.json` (`song.json` in the type docs): one song and its charts, written by the Bemuse Song Workshop ("Scan charts" + "Metadata" tabs) or the older `bemuse-tools` indexer.
- `index.json` (music server index): a `songs` array of song objects plus `id` and a relative `path` to the song folder. A server URL (`https://bemuse.ninja/?server=<url>`) is the folder holding `index.json`.

The legacy workflow also writes an `index.cache` (indexer cache, not read by clients). Charts stay `.bms/.bme/.bml/.bmson`; keysounds are [`.bemuse`](../bemuse/README.md).

## Container & encoding

JSON, UTF-8. Names are snake_case (the indexer source says "Our indexed JSON file is snake-cased") except the per-chart `noteCount`. Served over HTTP with CORS enabled.

## Structure / metadata

### `index.json`

```ts
interface MusicServerIndex { songs: SongMetadataInCollection[] }
interface SongMetadataInCollection extends SongMetadata { id: string  /* unique id */; path: string /* relative URL from index.json to the song folder */ }
```

### Song object (`SongMetadata`, from `bemuse-types/index.d.ts`)

| Field | Type | Meaning |
|---|---|---|
| `title`, `artist`, `genre` | string | Song metadata. |
| `bpm` | number | Representative BPM, used for sorting. |
| `alias_of` | string? | Artist's canonical name. |
| `artist_url` | string | Artist website. |
| `bms_url`, `song_url`, `youtube_url`, `long_url` | string? | Event page, song page, BGA on YouTube, link to a long version. |
| `added` | string? | ISO date. |
| `replaygain` | string | Loudness, format `"-X.YY dB"` (volume normalisation). |
| `video_file` | string? | Video file name from a bmson. |
| `video_url` | string? | Relative/absolute URL of a webm video; overrides `video_file`. |
| `video_offset` | number or string? | When to start the video. |
| `eyecatch_image_url`, `back_image_url` | string? | Loading-screen image and in-game background overrides. |
| `bmssearch_id` | number or string? | ID on https://bmssearch.net/. |
| `readme` | string | Relative/absolute URL of the README markdown. |
| `charts` | Chart[] | List of charts (below). |
| `warnings` | any[]? | Warnings from the indexer. |
| `chart_names` | map filename -> name? | Chart names when the BMS has no subtitle. |
| `initial` | bool? | Initially released song. |
| `preview_start` | number? | Start of the preview (seconds; previews are 30 s). |
| `preview_url` | string? | MP3 preview, default `_bemuse_preview.mp3`. |
| `tutorial` | number? | Marks a tutorial song. |
| `exclusive` | bool? | Only published on Bemuse. |
| `bemusepack_url` | string / null? | URL of the sound pack `metadata.json`; default `assets/metadata.json`; `null` = use the real files. |

### Chart object

| Field | Type | Meaning |
|---|---|---|
| `md5` | string | MD5 of the chart file (also the id for score ranking). |
| `info` | object | `title`, `artist`, `genre`, `subtitles[]`, `subartists[]`, `difficulty` (number), `level` (number). |
| `noteCount` | number | Playable notes. |
| `bpm` | object | `init`, `min`, `median`, `max`. |
| `duration` | number | Seconds [inference: units not stated in the type file]. |
| `scratch` | boolean | Has scratch notes. |
| `keys` | `'5K' | '7K' | '10K' | '14K' | 'empty'` | Key layout detected by `bemuse-indexer` (`getKeys`). |
| `file` | string | Chart file name. |
| `bga` | `{ file, offset }`? | BGA info embedded in the chart; "Not used by Bemuse - one song can contain one dedicated video file". |

## Timing model

Metadata only. The indexer computes `bpm` and `duration` from the BMS timing (`bpm-info.ts`, `duration.ts` in `bemuse-indexer`); see [`../../bms/bms`](../../bms/bms/README.md).

## Notes

Unknown. Each chart carries only `noteCount`, `keys`, `scratch`.

## Audio & images
`bemuse-data/song.ogg`, `preview.mp3` (30 s), `eyecatch_image.{jpg,png}`, `back_image.{jpg,png}`, `bga.{mp4,webm}` and the sound pack `bemuse-data/sound/` ([`.bemuse`](../bemuse/README.md)). After "clean up" a song folder holds only the chart files, `bemuse-song.json` and `bemuse-data/`.

## Versions & variants
- Legacy music server (`bemuse-tools server`): song folders with `assets/metadata.json` + `*.bemuse`, plus `index.json` and `index.cache`.
- Song Workshop: per-song `bemuse-song.json` ("Scan charts", "Save song metadata"); Server Manager assembles `index.json` from a list of `bemuse-song.json` URLs.

## Quirks & pitfalls

- Hosts need CORS and HTTPS.
- `video_offset` may be a number or a string.
- `bemusepack_url` defaults to `assets/metadata.json`; `null` means real files.
- `md5` identifies a chart; renaming the file does not change it.

## Example

Hand-built from the `bemuse-types` interfaces (values invented):

```json
{
  "songs": [
    {
      "id": "example-song",
      "path": "Example Song - Artist",
      "title": "Example Song", "artist": "Artist", "genre": "Genre",
      "bpm": 150, "artist_url": "https://example.com", "replaygain": "-6.50 dB", "readme": "README.md",
      "charts": [
        { "md5": "00000000000000000000000000000000",
          "info": { "title": "Example Song", "artist": "Artist", "genre": "Genre", "subtitles": [], "subartists": [], "difficulty": 3, "level": 7 },
          "noteCount": 800, "bpm": { "init": 150, "min": 150, "median": 150, "max": 150 },
          "duration": 120, "scratch": true, "keys": "7K", "file": "example_7a.bme" }
      ]
    }
  ]
}
```

## ROX support

Not read (a catalogue of BMS songs; ROX has no BMS reader in 0.8.1).

## Parsers & tools

- `bemuse-types` (TypeScript types): https://github.com/bemusic/bemuse/blob/master/packages/bemuse-types/index.d.ts
- `bemuse-indexer` (JavaScript/TypeScript): https://github.com/bemusic/bemuse/tree/master/packages/bemuse-indexer (reads `.bms`/`.bmson`, produces chart info).
- `bemuse-tools` (server indexer) and Bemuse Song Workshop https://github.com/bemusic/song-workshop; client loaders `bemuse/src/music-collection`, `bemuse/src/custom-song-loader`.

## Getting samples
Committed: see [`samples/SOURCES.md`](samples/SOURCES.md). `https://music4.bemuse.ninja/songs/<id>/bemuse-song.json` works for every id of the index (e.g. `[snack]dddd`); other servers publish their own `index.json` (`https://bemuse.ninja/?server=<url>`).

## Sources

- https://github.com/bemusic/bemuse (commit `4bf3e7d98a44841b323741cc403ecb7b41618ade`): `packages/bemuse-types/index.d.ts`, `packages/bemuse-indexer/src/index.ts` + `types.ts`, `website/docs/song-workshop.md`, `website/docs/music-server.md`
