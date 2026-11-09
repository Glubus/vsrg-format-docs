# Samples: Beat Saber custom level package (BeatSaver `.zip`)

## Committed

| File | Origin (URL, pinned commit if any) | Author | Licence | What it exercises |
|---|---|---|---|---|
| `goldcray_spine_noaudio.zip` | BUILT here from https://cdn.beatsaver.com/d29685cb1d27b770366273ba4d3193532c0e806b.zip (BeatSaver map 3171, "Spine", by goldcray) keeping only info.dat, Expert.dat, Hard.dat; song.egg (audio) and cover.jpg removed | goldcray (BeatSaver description: "mapping + lights cc0/public domain"); rebuild by OthersA | CC0 / public domain for the mapping per the author's BeatSaver description; song audio/cover not committed | legacy-era BeatSaver zip layout: flat (no wrapper folder), lowercase `info.dat`, v2.0.0 difficulties named `Expert.dat`/`Hard.dat`; info.dat references the audio and cover that are absent from this rebuild |

## Fetched by tools/fetch-samples.sh (not committed; listed in samples.manifest.json)

| Target file | URL | Licence note | What it exercises |
|---|---|---|---|
| `beatsaver_3171_d29685cb.zip` | https://cdn.beatsaver.com/d29685cb1d27b770366273ba4d3193532c0e806b.zip | mapping CC0/public domain per author description (song audio included in zip); URL is content-addressed by the map version hash | 35 s map, legacy flat layout, lowercase info.dat, Hard+Expert v2.0.0 (original zip incl. song.egg + cover.jpg) (771902 bytes) |
| `beatsaver_1337b_df0ded28.zip` | https://cdn.beatsaver.com/df0ded28f2c6b6a15ef73b24bbe97f3550ee0947.zip | mapping CC0/public domain per author description (song audio included in zip); URL is content-addressed by the map version hash | 142 s map, Info.dat capital I, Expert + ExpertPlus v2.0.0, 190 KB difficulty files (2912560 bytes) |
| `beatsaver_53af_1c68f916.zip` | https://cdn.beatsaver.com/1c68f916a734c5eaeeb2f99cd15a7d3aceb16e9a.zip | music by Kevin MacLeod CC BY 4.0 (stated in the BeatSaver description); map licence not stated; URL is content-addressed by the map version hash | 5 difficulties Easy..ExpertPlus (Standard), v2.0.0, custom lighting, 97 s (2030689 bytes) |

The `cdn.beatsaver.com/<hash>.zip` URLs are content-addressed (the map version hash is part of the URL), so they are treated as immutable; the sha256 values were checked by downloading each URL twice during collection.
