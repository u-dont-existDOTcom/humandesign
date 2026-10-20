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
