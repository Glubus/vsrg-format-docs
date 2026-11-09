# Samples: Cytus 1 chart ("Rayark v2 modified") (`.txt`)

## Committed (synthetic, hand-written)

| File | Origin | Author | Licence | What it exercises |
|---|---|---|---|---|
| `synthetic-c1.txt` | hand-written from the fiche and the Cytoid parser (Cytoid `Chart.cs` FromLegacyChart reads PAGE_SIZE, PAGE_SHIFT, NOTE, LINK by whitespace split) | OthersA | CC0 / public domain | synthetic. VERSION 2 header (BPM 120, PAGE_SIZE 2.0 = 240/BPM, PAGE_SHIFT 0), tab-separated NOTE lines |

## Real charts downloaded from public sources (snapshots, fetched 2026-11-09)

| File | Source URL | Date fetched | sha256 (of the downloaded file) | Author | Licence / terms as known | What it exercises / remarks |
|---|---|---|---|---|---|---|
| `cyl_package_tool_test_c1.txt` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/test_c1.txt | 2026-11-09 | 48bbd45666519471d5f10c46e777400383fe3b0eaedf6ec0654c7fd4e0700429 | ky_reflection | MIT | C1 chart: VERSION 2, BPM 320, PAGE_SIZE 0.75, title-case `Note` keyword (not `NOTE`), 27 KB |
| `cyl_package_tool_test_cytus1_chart.txt` | https://github.com/ky-reflection/cyl_package_tool/blob/3ee9792908a12827e62971fd29b3ba6ba36363c5/tests/resources/test_cytus1_chart.txt | 2026-11-09 | 6abd5de713132e88dc2361c4954da44beb694cc644fa6cd3a2e1e8313c327359 | ky_reflection | MIT | C1 chart: VERSION 2, BPM 167.996643, PAGE_SHIFT 0.84, PAGE_SIZE 1.4286, upper-case `NOTE` lines tab-separated, simultaneous |
| `make_cytus2_trytoc2_chang_BPM.hard.txt` | https://github.com/we684123/Make_Cytus2/blob/f1423347b400f24103dcf214e0fc83e3d47d13d0/trytoc2%28chang_BPM%29.hard.txt | 2026-11-09 | ada1dc0ea430083e66834a5cbd5a9ad282221e0cfcbece23db6525795c50d092 | we684123 | MIT | C1-style text with tool-specific header (17896 bytes); variant with BPM changes |
| `make_cytus2_trytoc2_chang_BPM_and_have_CKLINK.hard.txt` | https://github.com/we684123/Make_Cytus2/blob/f1423347b400f24103dcf214e0fc83e3d47d13d0/trytoc2%28chang_BPM_and_have_CKLINK%29.hard.txt | 2026-11-09 | 49a81b1b3fb1201544dd9006273fd1ad39ad5a70bab8290a537f3e2f34c497db | we684123 | MIT | C1-style text with tool-specific header (17900 bytes); variant with BPM changes and CK links |
| `make_cytus2_trytoc2_not_chang_BPM.hard.txt` | https://github.com/we684123/Make_Cytus2/blob/f1423347b400f24103dcf214e0fc83e3d47d13d0/trytoc2%28not_chang_BPM%29.hard.txt | 2026-11-09 | dc5e3cca5fee843c7f60df17d58dcba184630cc446540bec1dac1c07c01487d1 | we684123 | MIT | C1-style text with `VERSION 3` and extra tool-specific header lines |
