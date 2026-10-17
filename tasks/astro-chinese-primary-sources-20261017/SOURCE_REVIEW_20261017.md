# Chinese astrology source study — initial archival admission (not empirical validation)

2026-10-17, Africa/Dakar UTC+0.

## What was actually read and why the systems remain separate

**BaZi / Four Pillars** — the user supplied two complete Joey Yap works in-session. The observed PDF of Book 1 is 316 frames, identified internally as originally published in February 2005. The EPUB of Book 2 identifies an original 2006 edition; its EPUB metadata bears 2018. Both formats were opened and inspected, metadata and source-byte SHA256 recorded in `SOURCE_MANIFEST_V1.json`. Full copyrighted source files are NOT published in the repository. Book 1 offers birth year/month/day/hour stem-branch table, Li Chun (solar seasonal-year) and seasonal monthly boundaries, early/late Zi hour variants, Day Master, elemental factors, first Luck Pillar and decade timing, and historical gender-coded spouse assignments. Book 2 adds Hidden Stems and important adjustments to the beginner simplified formulas, and separately treats combinations, clashes, punishments, harms, destruction, and example life courses. These authored forecasts and cases remain unblinded and unconfirmed.

**Zi Wei Dou Shu / Purple Star** — the transmitted three-volume Chinese `紫微斗數全書` was located and inspected on Chinese Wikisource, with a different modern Chinese-English annotation at https://xingge.tw/en/quanshu. Chinese sources give concrete Life/Body palace setting, 12-palace ordering, first Yin palace stem, five-phase Bureau and extra classical rules for configurations and decade/annual luck. The original text, not an unverified late historical author legend, is preserved as the primary textual authority. Surviving printed edition, preface date and attributed authorship require further critical bibliography.

## First verified historical source notes and chart-engine subset

`bazi/BAZI_SOURCE_FIRST_RULES_V1.json`: **46 source-only qualified records** from the two author works with original book/page or EPUB HTML section anchors. No full excerpt text and no personal forecasts.

`ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json`: **26 source-only annotated records** from the transmitted Chinese volumes; the original Chinese quote/translation collation is NOT complete, and disputed conventions remain unchosen.

Two narrowly scoped and independent deterministic source-configuration modules:
- `bazi/bazi_source_mechanics.py` computes hour branch/stem from an already established sexagenary Day Master (including Book 1's late Zi rule), year-polarity luck direction, next/previous decade pillar from Month Pillar, approximate first-Luck-Pillar age from author-reported days/3, the source's five factor element roles, and complete San He/San Hui triplet detection.
- `ziwei/ziwei_source_mechanics.py` computes classical Life/Body palace offsets from an already established LUNAR month/double-hour and explicitly chosen leap-month rule, and traditional first Yin Palace stem from year-stem class and sequential palace stem placements.

**38 deterministic integrity tests** passed. The source's published hour-pillar examples are reproduced for 20 Feb 1967 16:30, 26 Mar 1956 09:30, and 18 May 1940 23:58 (the last tests Book 1's late Rat distinction). Original Zi Wei worked Life/Body palace mnemonics are reproduced for lunar first month Zi/Chou/Yin double-hours. Tests cover potential silent merging of distinct schools, missing source anchors, nonpromotion status and failed alternatives. They do **not** prove full Gregorian-to-lunar or solar-term calendar charts, nor human predictive accuracy. Unit tests were executed in the HumanDesign branch without publishing either owner ebook.

## Source inconsistencies and methodological cautions to preserve

- First book states `Li Chun around February 4` and a rough calendar table. Actual year/month transitions require **computed astronomical solar-term instants**, not permanently fixed dates.
- First book's 26 March 1956 illustrated example shows Ren day master and Yi Si hour, but adjacent passage calls the day master Yi; a source errata candidate to review from original page scan.
- First book's 2005 year statement includes a discrepant Chinese character combination in prose (Yi You versus Yi Chou); must inspect original illustration before repairing.
- The same source distinguishes early versus late Rat hour. Zi Wei original source, modern Zi Wei websites and other BaZi schools adopt different conventions. This is a **choice of calendar mechanics**, not a chart quality problem.
- Book 1 labels an example as week/age of luck using integer days/3 and mixes wording 'round up' with ordinary nearest integer. The reproducible partial implementation uses nearest integer as shown by examples; exact first luck-start date remains **unresolved**.
- Book 2 warns that combining two or three branches need NOT automatically produce a positive person relationship or transformed element; full combinations versus half, adjacency and favorable/unfavorable chart requirements must be separately encoded.
- Classical Zi Wei Quan Shu's intercalary month, Life/Body forward/backward calculation, Zi hour, and the timing conventions used on Xingge differ in specific places; all are versioned and unresolved until detailed line-by-line source study.
- Historical source gender, trustworthiness, crime, addiction, intimate behavior and spousal medical/mortality descriptions are **not** established characteristics of any actual person.

## Unfinished priorities

1. Verify calendrical year/month solar term and sexagenary day engine from a trusted dated historical Chinese calendar plus independent mathematical library, not only from the present hour/decade subset; include every boundary and uncertainty.
2. Verify Zi Wei complete 12-palace, major/minor star and Four Transformations placements and independently compare variants across San He and Flying Star before interpreting chart meanings.
3. Complete source-level coverage of both author books and every relevant volume of original classical BaZi and Zi Wei; trace copyright/provenance and catalogue genuine contradictions rather than choosing the convenient rendition.
4. Freeze predictive targets in the survey, preregister link rules and negative events, implement matched decoys and demographics/season/date controls, then test on **unseen human lives** against Lilly/other traditions without pooling retrospective successes.
5. Do not retune source predicates from the author's own chart or other biography data once results are seen. Do not promote any source rule to a current production person-life interpreter without separate owner-requested gate.

**Study metrics:** Source-only records **72** (46 BaZi + 26 Zi Wei). Focused provenance/mechanics tests **38 passing**. Birth date conversion **not implemented**. Zi Wei full stars/Four Transformations **not implemented**. Empirical human validations **0**. New runtime rules promoted **0**.
