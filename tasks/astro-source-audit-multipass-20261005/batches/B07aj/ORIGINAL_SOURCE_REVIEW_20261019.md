# Lilly original Naibod tables: first and second historical printings

2026-10-19 — Africa/Dakar UTC+0. Historical-source collation only, not a birth-chart direction-time engine or prospective human prediction.

**Authority.** William Lilly, *Christian Astrology* (1647), original Wellcome b30338724 scanned PDF SHA-256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Printed folio713/PDF747 contains Naibod's table converting equatorial **degrees** to years/days/hours; printed folio714/PDF748 contains the **minute**-to-days/hours table and starts a worked Mars-terms example. Original 1659, separately typeset, printed713/714 (DjVu742/743), supplies auxiliary original evidence. Exact original image SHA/byte witnesses and 12 separately checked edition comparisons are in `ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json`.

**Physical source rows:** 90 explicitly labeled equatorial degree positions, 1–90; 59 visibly labeled minute positions, 1–26 and 28–60. The original printer skips the minute-27 label: do not invent a source row for it. Existing original first-edition B07x source observations were reused **byte-exact** rather than read anew; their photographically uncertain minute-1 *days* digit (5 or 6) is retained as **null** and alternatives, even though the separately typeset 1659 copy says 6. No member of these tables is promoted to a verified birth-time engine.

**Preserved first-edition printing issues:**
- Degree 69 prints **70 years, 4 days, 3 hours**, with subsequent degree-to-year offsets extending to degree 90 printing year91, whereas flattened secondary transcription writes year equal to input degree.
- Degree 80 prints **81 years, 62 days, 24 hours**, left as *24*, not silently normalized.
- Minute 8 prints **44 days, 10 hours**, in both typeset editions, despite a contrary arithmetic trend.
- **Minute 27 is not visibly printed**; the next row is labeled 28 and reads 166 days, 18 hours. This is a labeled-source gap, not license to fill 27 from interpolation.
- Minute 44 appears as **271 days, 8 hours** in 1647, but **271 days, 18 hours** in 1659. An apparent later-edition correction is documented separately rather than backfilled into the first.
- Minute 55 prints **339 days, 17 hours**, cited in the worked Mars-terms example.
- Minute 60 prints **374 days, 14 hours** in both copies. It disagrees with the single degree row under a simplistic 365-day carry; do not repair the historical glyph to a presumed correct rate.

**Scoped history entry:** `RULES.json` contains 21 historical documentary observations R12547–R12567, with the actual 149 independently reversible table rows in a separate crosswalk, not counted as 149 new chart rules or human observations. Lilly accepted index before this packet is 12,546 (plus 1,066 Ptolemy); after guarded admission it becomes **12,567 Lilly and 13,633 Western historical annotations**. Parallel Chinese V5 remains **262** (101 BaZi,161 Zi Wei). Chapter **CLXVI remains partial**, next R12568 PDF749/printed715 for exact Naibod worked carry and chapter boundary. The later distinct annual-profections chapter also bears printed CLXVI.

Regression tests confirm source hashes, all 90+59 historic records and 21 source rule slots, anomalies/nulls, old ledger immutability, and **no empirically verified real-person predictions or model promotion**. Stronger expert source critical collation, old-epoch astronomy/time engine, and out-of-sample human tests are still required for those separate claims.
