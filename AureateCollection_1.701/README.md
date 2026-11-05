# Aureate Collection 1.701

Repair build of Aureate Collection 1.700. All 52 programs in TTF and WOFF2 under `fonts/`,
with the same family and style names as 1.700, so they install over the 1.700 set (or beside it
if 1.700 is removed first). `CHANGELOG.md` lists every finding and every change.

Rebuild from the 1.700 package:

    python3 source/repair_1701.py          # writes fonts/ and verification/repair_report.json
    python3 source/verify_1701.py          # shaping regression and metric checks against 1.700

Requires Python 3.10+, fontTools, brotli and uharfbuzz. Paths to the 1.700 package are at the
top of each script. OpenType timestamps are pinned to 2026-10-28 UTC.
