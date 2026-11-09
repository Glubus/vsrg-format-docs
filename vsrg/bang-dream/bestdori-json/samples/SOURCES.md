# Samples: Bestdori chart JSON

## Committed
| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-bestdori-v2.json` | hand-written for this repository | vsrg-format-docs | CC0 / public domain | `synthetic`: `BPM` (2), `System` entry (seen in official chart JSON), `Single` with `skill`/`flick`/`charge`, two `Long`, a `Slide` with a `hidden` node and flick end, two `Directional` (Left width 2, Right width 1). Lanes 0..6. Built from `../README.md` plus the shapes observed in official `charts/1/expert.json`; not run through any parser. |

## Not fetched (live, not hashable)
Official charts are public and need no login (`https://bestdori.com/api/charts/<songId>/<easy|normal|hard|expert|special>.json`, checked 2026-11-09: 1/easy 2805 bytes, 1/expert 18550, 3/special 50591 with `Directional`, 200/expert with 3 BPM changes, 400/expert with 5) but the site is a live service (no immutable URL; Wayback snapshots were not reachable from here), so they cannot be hashed in the manifest. They are Bushiroad/Craft Egg charts anyway. Community charts: `https://bestdori.com/api/post/details?id=<postId>` (e.g. 1070, category `SELF_POST`/`chart`) returns a wrapper whose `post.chart` is the same array; the wrapper includes mutable counters (likes) and falls under Bestdori terms, so it is not listed.
