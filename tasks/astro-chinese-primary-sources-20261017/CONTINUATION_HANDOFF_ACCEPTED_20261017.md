# Chinese astrology HumanDesign research — BZI+ZWDS initial intake and continuation

2026-10-17 21:53 UTC Africa/Dakar.

## Owner goal

Continue Lilly first-edition Western source research AND add Chinese astrology: independent **BaZi / Four Pillars** and **Zi Wei Dou Shu** original-source study, then later empirical comparison and preregistered combination with Western/Hellenistic/Jyotish source lanes. Do not confuse historical printed source notes with validated person-level forecasts. All work in HumanDesign Git repository, keep separate source/validation/model-status indices.

## Completed Chinese independent source batch

Isolated branch `research/astro-chinese-bazi-ziwei-primary-20261017` based on Lilly last accepted B06k source commit `cda26884df02d92462166849c9fe865045c0a791`.

Project path `tasks/astro-chinese-primary-sources-20261017/`. Files:
- `SOURCE_MANIFEST_V1.json`: SHA256 source IDs/provenance of two USER-UPLOADED copyrighted Joey Yap complete works and original Zi Wei Chinese public historical three-volume web text. Book1 original copyright first edition 2005, observed PDF file SHA `8b40261a8fb4eeacadb19381c91e91208aa3a9de66685407868b2691afb1a6a2`; Book2 first edition 2006, EPUB metadata 2018-07-24, file SHA `9d29d83c94b67b1c887d6a2935ee8361e821bb6216487f9fe86b444a48489e81`. Do not copy copyrighted ebooks into Git.
- `RESEARCH_PLAN_20261017.md`: full source-first, chart computation, goldens, hidden stellar school conventions, blind empirical comparisons.
- `bazi/BAZI_SOURCE_FIRST_RULES_V1.json`: **46 qualified source-only notes**, book1/book2 printed page or EPUB HTML reference. Stems, branches, solar terms/approx Feb 4, months, 23:00 late Rat, hour from day stem, source example golden chart partial, day master, seasonal strength, decade luck direction and starting age, factors, first-year stereotypes, combinations/clashes/punishments/harm/destruction, no real human validations.
- `ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json`: **26 source-only Chinese historical notes**. Chinese Vol1/2/3 original from Wikisource. Exact original Life/Body palindrome and 5 Tiger year stem origins; twelve palaces; star, favorable vs malefic and ranking implications; school-convention register. All incomplete Chinese-English line collations clearly flagged.
- Partial source mechanics `bazi/bazi_source_mechanics.py` & `ziwei/ziwei_source_mechanics.py` deliberately lack full birth-calendar conversion, full Zi Wei fourteen-star and Four Transformations, source-valid scoring and any personal predictions. Tested example hour stems 1967 Yi→Jia-Shen, 1956 Ren→Yi-Si, 1940 late Rat Xin→Geng-Zi; first five-factor classification and San He/San Hui; classic Zi Wei month1 Zi/Chou/Yin Life/Body and five year-stem starting pairs.
- `tests/test_chinese_source_mechanics.py` **38/38 focused tests PASS**; Ruff clean. ZIP `~/Téléchargements/Astrology-Chinese-BaZi-ZiWei-Source-Research-20261017.zip`, hash `21c94ac3c3418bd3f9f2336d4b40b3b0cf28f43b5e39109bf9efb4a0440eba65`, complete member CRC+SHA and 38 extracted test replay PASS. Source ebooks NOT embedded.
- `SOURCE_REVIEW_20261017.md`: documented source study and source inconsistencies, source classification and next.
- `state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md`: Chinese track state independent of `state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md` Lilly.

After verified GitHub push/readback, **Chinese study initial total 72 source-only annotations, chart mechanics 38 focused tests, 0 entire chart engines, 0 independent human predictive validity and 0 runtime promotions.** Do not conflate with Lilly existing 9,207 source notes.

## Next Chinese source extraction

1. Complete Book 1 source audit p1–p259, locate all charts, original age/solar-term tables and material author's explicit caveats; Book2 EPUB 331 HTML fragments printed p1–294 with charts, decode its 10 Gods, hidden stems, full six combinations/clashes and punishments, harm/destruction, conditional transformation. Fix known source prose typo 1956 day stem 'Yi' vs chart Ren only after original image review, preserve source errata.
2. Critical historical BaZi texts `Di Tian Sui` 滴天髓, `Zi Ping Zhen Quan` 子平真詮, `Yuan Hai Zi Ping` 淵海子平 source manuscripts/editions; no original Chinese collated at current checkpoint.
3. Complete Zi Wei Quan Shu transmitted 3 volumes at `https://zh.wikisource.org/zh-hant/紫微斗數全書`. Source-first Chinese plus trusted English cross-check xingge.tw/en/quanshu, with explicit cases that annotator's chart differs from transmitted original in start of luck, palace-stage direction and late Rat time. Verify historical provenance separately, and classify San He vs Si Hua (Flying Stars) and alternate stem tables; no universal table claimed.
4. Build exact independent calendar/date converters with real solar term epochs (BaZi), lunisolar calendar leap months (Zi Wei), local historical clock time/timezone, alternative true solar time. Use independently checked published golden calendars and freeze all convention cases before person data.
5. Preregister causal/association hypothesis against the same held-out participant responses, owner-introduced wonder/synchronicity constructs only after hypothesis freeze. Matched decoy and baseline comparison; negative results mandatory. No moral/criminality/intimate characterization of actual person from these source claims.

## Western Lilly continuation NOT superseded

Existing last VERIFIED Lilly checkpoint B06k: **8,141 Lilly +1,066 Ptolemy = 9,207 historical documentary notes** at original 1647 PDF627/894 (70.1% scanned page position, not program progress), last R8141. Isolated **B06l** worktree `/home/joel/humandesign-worktrees/astro-original-b06l-20261017`, starting original printed CHAP CXXXIIII/editorial CXXXV on wife appearance (PDF627–631 before printed CXXXV marriage-concord heading). Original photos PDF627–634 are already downloaded in B06l/evidence and NONCOMMITTED, no B06l notes yet accepted. Need continue from those original photos; broad chapter includes appearance, alleged wife personality, postures, immoral/infertility claims, class-relative dowry/fortune, and spouse ill fortune, not merely physical beauty. These are historical socially stigmatizing stereotypes, NOT actual diagnosis or predictions. Lilly source work should be resumed separately with original-source photo SHA, records R8142 onwards, guarded index, focused tests, archive and GitHub remote readback. Last accepted B06k Git commit `cda26884df02d92462166849c9fe865045c0a791`. The Chinese branch is a parallel independent source branch and must not overwrite the Lilly index.

## Program instructions

Reload universal-dev-architecture/AGENTS.md, HumanDesign AGENTS.md (current active source rules), source state checkpoint. Keep summary of all unresolved issues. Source-only task branch push is accepted authorized project work; do not copy full source ebooks to GitHub. Do not assert full-scope project completion, quantitative human accuracy, calendar parity or automatic background processing. Strict append-only source numbering for each lane; versioned rule indexes. Use User's "continue" to resume without redundant successful calls.
