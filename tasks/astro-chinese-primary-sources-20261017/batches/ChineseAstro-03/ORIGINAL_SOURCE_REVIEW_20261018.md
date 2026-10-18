# Zi Wei Dou Shu Quan Shu, transmitted Volume II — original auxiliary and timing mechanics

**2026-10-18, Africa/Dakar (UTC+0).** Historical Chinese text research, **not empirical natal astrology validation**. Authority is a pinned transcription of `紫微斗數全書/卷二` on Chinese Wikisource **revision oldid=1963110**; raw wikitext **106,736 bytes**, SHA256 `1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72`. This verifies exact Chinese wording at that online revision, **not** the provenance of a particular ancient manuscript, a historically correct Ming woodblock edition, an expert translation or the efficacy of any chart predictions.

## Documented source scope and direct Chinese evidence

**45 new non-overlapping source-only annotations, ZWD-R0052–ZWD-R0096**, continue the preceding accepted ZWD-R0051 (Long Chi). Each new short Chinese phrase and its named original Chinese section heading was found in the pinned raw Simplified Chinese wikitext. `SOURCE_REVISION_ANCHOR_WITNESS_V1.json` records **45/45 exact source anchor matches, source-section offsets, Unicode character offsets and exact UTF-8 byte offsets/phrase hashes**. `ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json` stores readable original phrases and separate English historical paraphrases, source preconditions and unsolved exceptions. The full Wikisource chapter is not reprinted in GitHub.

The new source content falls into these distinct original sections:
- **Star placement**: Feng Ge birth-year counting opposite to the previously documented Long Chi, hour-based Tai Fu and Feng Gao, five bureau-specific Chang Sheng start palaces and the text's historically sex-coded stage counting.
- **Relationship-star mechanics**: Hong Luan from Zi-year Mao backwards and Tian Xi exactly opposite Hong Luan. Source verse makes claims about marriage and age, including adverse later-life stereotypes; these are *period rhetoric*, not actual marriage or widowhood predictions.
- **Yearly auxiliary stars and Dou Jun**: Sang Men two forward, Diao Ke two behind annual Tai Sui, Bai Hu/Guan Fu opposite; Dou Jun two-step annual Tai Sui → reverse lunar birth month → forward birth hour. Three deity stars Tian De, Yue De, Jie Shen distinguish current annual Tai Sui from natal-year branch.
- **Historical year-branch and stem rules**: Four flying-three-sha year-branch triad maps, five paired Jie Lu Kong Wang year-stem mappings, and six original sixty-day *xun* emptiness pairs. A problematic source-year glyph **戍** occurs in the Yin/Wu/Xu flying-star verse and is preserved rather than silently replacing it with **戌**.
- **Life-period methods**: Da Xian original year-polarity/sex-coded starts and directions, Xiao Xian original male/female counting rules and four birth-year trine starting palaces, and the first children's-period age-one-through-six palace mnemonic.

The compact module `ziwei/quan_shu_vol2_aux_placements.py` executes only a **bounded list of source-backed twelve-palace placement operations** for already resolved year branch/stem, lunar month, birth hour and historically classified bureau; invalid or unspecified inputs fail closed. It is **not** a Chinese calendar, full Zi Wei fourteen-main-star chart, personalized or gender-identity judgment, birth-time determination or natal forecast. The historical source's gender rules are quotation contexts, not modern claims about people.

## Cumulative source-only Chinese index

Previous `CHINESE_SOURCE_AUDIT_INDEX_V2.json` contains **46 BaZi +51 Zi Wei=97** annotations. The proposed version **V3 adds 45 Zi Wei notes**, for **46 BaZi +96 Zi Wei=142 Chinese historical annotations**. The original Chinese V1 and V2, earlier 46 BaZi, earlier 51 Zi Wei and Western Lilly/Ptolemy registries remain byte-for-byte preserved; Chinese next record becomes **ZWD-R0097**. BaZi next remains **BZI-R0047**. Historical record totals do not represent the number of independent predictive cases, persons or unique rule hypotheses.

## Source limitations and next audited frontier

The pinned online Volume II uses raw Simplified Chinese. Earlier rendered Traditional forms are derived display conversions, not byte-for-byte original text. A manuscript/edition provenance comparison with an independently scanned original is still needed for a historical critical edition. Lunar intercalary month treatments, the precise year boundary, late-Zi double-hour rule, source sex/gender categories, correct Five Element bureau calculation, complete 14-star and Four Transformations chart parity all remain unverified.

Next Zi Wei **ZWD-R0097** continues from the children's-period passage through `安命主`, `安身主`, star-palace idle-strength tables and `论星辰生克制化`, with original Chinese source phrases and conditions. For BaZi **BZI-R0047**, acquire and audit actual traditional Chinese texts such as *Di Tian Sui*, *Zi Ping Zhen Quan* and *Yuan Hai Zi Ping* against source edition/pagination, not just modern textbook paraphrases. **No current human predictive accuracy and no model inference rules promoted.**

The source integrity, photo/wording proof, internal mechanics tests and archive SHA-256 checks are **documentary engineering evidence**, not independent Chinese historical-expert or real-world astrology validation.
