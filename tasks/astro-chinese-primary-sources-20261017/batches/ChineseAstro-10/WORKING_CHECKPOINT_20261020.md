# ChineseAstro-10 — isolated source-based Zi Wei NaYin bureau parity

Working branch based on accepted Chinese V9 commit 09111bb87399dc2e681854cb247db3af6ff2381d. **NOT yet admitted into the V9 Chinese historical source-count registry.**

Goal: convert the existing frozen oldid1963110 Volume-II NaYin thirty-couplet poem and independently source-anchored year->Yin palace stem rule into a reproducible, explicitly qualified lookup. Preserve the transmitted errors: first-character pair 甲戊 instead of 甲戌 and second-character pair 已亥 instead of 己亥. Uncorrected source permits 58/60 sexagenary pairs and 116/120 year-stem/palace pair paths. A separately documented collation (not silent cleanup) allows conditional lookup of the remaining 4 paths.

Original frozen source: tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt; sha256 1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72.

Cross-witness (later editions/transcriptions, **not authenticated early manuscript**):
- Qing-period 卜筮正宗全書, 六十花甲納音歌, https://www.shidianguji.com/zh/book/HY1439/chapter/1m70sj2411nvn — online text supports 甲戌乙亥 and 戊戌己亥.
- Wiki-linked modern Zi Wei text https://m.gushiwen.cn/guwen/bookv_46fc9880f58c.aspx supports 甲戌乙亥 but reproduces 已亥 for the other couplet.
- Other transmitted corroboration 甲戌乙亥: https://ctext.org/wiki.pl?chapter=466438&if=gb; this text retains its own 巳/己 ambiguity in another couplet.
- Prior chat noted a modern printed-page-66 photo with both corrected readings, but its exact scan identifier and binary hash have not yet been recovered independently; do NOT claim the image independently verified here.

No civil-to-lunar conversion, actual 14-main-star placement parity, authentic Ming-era witness, behavioral prediction, blind participants, or production/clinical forecast is established. Zero human validations and runtime promotions.

Next: focused source/structural tests, independent verification, then source/engine-only branch commit and remote readback. Separate Lilly R13045 and BaZi BZI-R0211 remain open, unmodified.

## New reproducible mechanical result

Source-locked parser/lookup implemented in ziwei/quan_shu_vol2_nayin_bureau.py, with test suite tests/test_ziwei_nayin_bureau_source.py. Source hash and original 30 seven-character couplets are enforced. Both source defects appear explicitly in the uncorrected mode; the emendation mode repairs only exact known bad stem/branch characters, preserving provenance separately from their valid neighbors. Each of 60 sexagenary pairs occurs in exactly two of the 120 year-stem/palace paths. First original classical worked example (甲 year, 寅 life palace -> 丙寅 Fire-six) is reproduced. Source-only mechanical coverage is **116/120 without**, **120/120 with** carefully labeled later-witness readings. This is NOT independently calculated natal-chart parity.

Focused regression 12/12 green after correcting an initially discovered provenance error (the valid half of each affected couplet had been mislabeled emended; now it is direct). Initial 10/12 then corrected 12/12; failures preserved in test observer telemetry. All code/data new in isolated worktree; canonical V9 historic indexes unchanged.

## Five original bureau/day-to-Zi Wei diagrams and two-star chain

Follow-on after the first accepted research-only local/published commit. The same pinned oldid1963110 full source contains five vertically printed palace grids, one per elemental bureau (2,3,4,5,6). A parser preserves each Chinese numeral and branch position, including multi-palace ambiguity, instead of inferring the intended corrected diagram. New `ziwei/quan_shu_vol2_purple_star.py` offers original-only raw output, and opt-in documented variant comparison. A separate ordinary arithmetic rule (quotient and odd/even complement) is written independently of the source-grid parser for mechanical comparison, but both derive from the same astrological tradition: **this is internal mechanical agreement, not independence from that tradition**.

All **147/150 unique unambiguous original** palace locations agree with comparator. Original discrepancies: Wood3 lunar day **5** absent; Wood3 day **9** appears twice (Chen and Yin); Metal4 day **30** absent. Three *different* qualified statuses preserve the provenance of any conditional resolution: `modern_collation` day5/Yin; `ambiguity_resolved` day9/Chen; `rule_inference` day30/Hai. Conditional 150/150 algebraic agreement is NOT independent original-edition parity.

Across all 10 year stems × 12 Life-palace branches × 30 lunar days, source-uncorrected results are **3,412 unambiguous direct + 120 unresolved bureau + 46 missing star + 22 ambiguous star = 3,600**. Opt-in source variants make all 3,600 mechanically resolvable; not real birth-derived charts. New `ziwei/quan_shu_two_star_skeleton.py` combines Life/Body, palace stem, NaYin element bureau, original Purple-star day grid and Tian Fu palace reflection to yield only **two out of fourteen** major stars. Reproduces source demonstration for Jia-year, month1, Zi-hour, lunar day1: Life Yin, Body Yin, Bing-Yin Fire-six, Purple-star You, Tian Fu Wei. Source month, leap-month and birth-hour conventions are explicit, not calendar-verified. Neither branch has calculated Gregorian/local-civil-time -> true Chinese lunar date; neither supports predictions.

Tests: prior NaYin **12/12** and previously existing Chinese mechanics **38/38** passed. New independent-source-diagram comparator **11/11** green. Bounded two-star chain **9/9** green. Source/engine research only, **no added historical annotation records, no runtime promotion, no preregistered real-human prediction**.

## Next safe autonomous steps

- Do not count these engineering parity observations as historical notes or evidence astrology works.
- Independent independently published traditional Zi Wei chart examples with authenticated birth calendar/time-zone treatment; implement all 14 principal stars and Four Transformations, date-hour conversions with tests across leap months.
- Independently check exact source and date boundaries for BaZi day/solar terms, and Lilly historical 1647/1659 original printed page754 Chapter CLXXXI R13045, in separate worktrees; preserve source original and errors.
- Freeze model, target mapping and participant blind/test protocol before any human outcomes or decoy scoring. Publish each tested checkpoint to an isolated Git branch with SHA readback and keep negatives.
