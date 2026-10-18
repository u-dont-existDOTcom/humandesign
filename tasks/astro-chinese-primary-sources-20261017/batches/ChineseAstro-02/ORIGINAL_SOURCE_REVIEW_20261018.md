# Zi Wei Dou Shu Quan Shu: Volume II pinned-original source audit, part A

**Scope:** transmitted `紫微斗數全書`, Volume II, Wikisource **revision 1963110** (September 2020), fixed Chinese wikitext via `oldid`. This edition is a transmitted transcript with uncertain classical manuscript lineage, NOT proof Chen Tuan authored the extant wording. Modern annotated versions may diverge.

## Direct source integrity

Pinned raw URL is in `SOURCE_REVISION_ANCHOR_WITNESS_V1.json`. Network read status 200. Raw page **106,736 bytes**, SHA256 **1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72**. All **25/25 short Chinese anchors and named sections occur in the raw pinned wikitext**, witnessed individually. The first verification failed 25/25 when using Traditional glyphs from the converted reading interface; raw source is written in Simplified. `restore_pinned_raw_glyph_anchors.py` retains both raw source witness and display-transformed traditional forms. No full Wikisource source body is copied into GitHub or the release ZIP.

The direct original text has specific mechanics absent from the preceding 26-note high-level inventory. The 25 new records **ZWD-R0027–ZWD-R0051** include:
- major star starting adjacency/skip directions (not complete fourteen-star calculation);
- Wen Chang and Wen Qu **opposite** hour counting;
- Zuo Fu / You Bi **opposite** lunar-month counting;
- Tian Kui / Tian Yue year-stem pairing; Tian Ma four year-branch trines;
- Lu Cun year-stem table, adjoining Qing Yang / Tuo Luo with **explicit Gui-year** example;
- Fire/Bell historical group verse without verified star ordering;
- Jia-year Four Transformations row and a separately preserved ten-year-stem verse (school differences unresolved);
- Di Jie / Tian Kong opposite birth-hour placement from Hai;
- Tian Shang and Tian Shi tied to explicitly named Associates/Illness palaces;
- twelve auxiliary-stage orientation conditional on historical gender/year-polarity;
- lunar-month Tian Xing / Tian Yao, birth-day San Tai / Ba Zuo, year Tian Ku / Tian Xu and Long Chi.

## Bounded mechanical experiment, not chart/prediction validation

`ziwei/quan_shu_vol2_placements.py` implements only source-checkable reversible palace arithmetic. Examples: Zi-hour Wen Chang at **Xu**, Wen Qu at **Chen**; Chou-hour at **You/Si**. Lunar first-month Zuo Fu **Chen**, You Bi **Xu**; second-month **Si/You**. Zi-hour Di Jie and Tian Kong both **Hai**, Chou-hour **Zi/Xu**, Wu-hour both **Si**. Gui Lu Cun **Zi**, Qing Yang **Chou**, Tuo Luo **Hai**. San Tai day one = Zuo Fu, Ba Zuo day one = You Bi. All 12 branches, 10 year stems and out-of-range inputs receive separate deterministic test coverage.

These *placement* results are historical arithmetic only. No lunar intercalary-month conversion, Gregorian-to-Chinese calendar engine, true-solar-time alternative, late-Zi day boundary, complete primary-stars, Na Yin bureaux, modern Si Hua parity or independent published golden-chart parity is established. The full ten-stem Four Transformations mapping is not executed as a modern chart engine. The historical source's first Tian Ma triad reads **寅午戍**, whereas the normalized Earthly Branch transliteration used in computation is **Xu/戌**; the transmitted glyph difference is a source-review issue, not silently overwritten.

Gender, class, danger, illness, reputation and other historically prejudicial interpretations are source-only. The mechanics cannot be used for medical, safety, relationship or real-person forecasting. No blind human validation, no runtime predictions or model promotion.

## Append-only accepted structure

Prior independent source registry `CHINESE_SOURCE_AUDIT_INDEX_V1.json` and original BaZi 46 and Zi Wei 26 note files remain exactly unchanged. New cumulative **V2** preserves 46 BaZi plus **51 Zi Wei = 97 Chinese documentary notes**, with separate source-group references and SHA bytes. The Western Lilly index stays at **11,325**, Ptolemy stays **1,066**. Do not add the Chinese count to Western totals or treat clause numbers as empirical samples.

## Open next frontier

Finish pinned Volume II `安龍池鳳閣訣` through `論星辰生克制化` as a second source batch from **ZWD-R0052** with raw glyph anchors and condition flags, especially Long Chi's Feng Ge counterpart, annual/monthly timing, twelve-palace strength gender stereotypes, star-bureau tables and source contradictions. Complete the missing classic BaZi manuscript studies and source-book page-by-page audits independently. Build exact calendar and independent double-parity chart engines before any person study; preregister held-out human outcome forecasts against null and decoy charts. No current person-specific predictions are permitted from this batch.

Mechanical tests and archive replay establish **internal evidence integrity**, not independent sinological expertise or scientific astrology validity.
