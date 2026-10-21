# HumanDesign Chinese BaZi V25 Di Tian Sui section19 Source/Flow — accepted continuation handoff

21 October 2026. **Root owner astrology research OPEN:** independently read Western Lilly/Ptolemy and Chinese BaZi/Zi Wei primary texts, build verified birth-derived natal/calendar chart engines, freeze precise chart-to-measured-outcome hypotheses before collecting untouched consenting human responses, and evaluate real forward/reverse blinded results against matched-chart decoys, demographic and nonastrology baselines. Historic source annotation counts and anecdotes do not test predictive success.

## Source identity and accepted fork

Isolated Chinese BaZi source branch `research/astro-chinese-v25-bazi-dts19-original-source-20261021`, based exactly accepted V24 Chinese commit `9f6d803a016a9f95f2ed8b36c86d752aed23487c` and previous source index SHA256 `ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1`. The local computer's HDD `/mnt/hdd` was at 100% with only about 922MB available; a full new Git checkout failed. Do not delete existing unrelated worktrees/files. We created an isolated **sparse checkout on the system SSD** `/home/joel/development-worktrees/humandesign/astro-chinese-v25-bazi19-20261021`, with only needed original BaZi, prior index and inherited Western snapshot files (~800KB). The worktree contains exactly this source batch plus versioned new Chinese index and state. No Western, independent Zi Wei original source, integration/runtime edits.

Pinned original online Wikitext `滴天髓/19` (源流論, Source/Flow), revision **oldid844368**, URL `https://zh.wikisource.org/w/index.php?title=滴天髓/19&oldid=844368&action=raw`, **909 bytes** SHA256 `032a772c550dedb35aa130b835bb12d09dd3f3e89652aea382d7b00587ccf28d`. Exact original raw source in `evidence/DiTianSui_19_oldid844368.wikitext`, manifest `PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json`.

**Six fully frozen historical text components BZI-R0211–BZI-R0216**: 1 complete verse, 3 complete transmitted Chinese commentary paragraphs, and **two original Wikitext four-pillar examples, each retaining original column order 時 hour, 日 day, 月 month, 年 year**, not reconstructed civil birth datetimes:
- Example 1: hour 丁巳, day 戊申, month 癸巳, year 辛酉. Text *claims* Fire-source flow to Metal/Water brings wealth/status `所以富貴`; no independent actual identified person or financial record.
- Example 2: hour 壬子, day 癸丑, month 壬戌, year 癸丑. Text *claims* support cannot be drawn and therefore `所以為僧也`, monkhood. No identity or life-event authentication.

Critically, expanded later online `滴天髓闡微` transmits **`流到何方住`** instead of short source **`流向可方住`**, and in example 2 **`得從引助`** instead of **`無從引助`**, and **`憎`** instead of **`僧`**. These alter the literal proposition or outcome label and cannot be fused or silently corrected. Multiple reproductions may share a textual ancestor; authenticated early print pages remain missing. Neither example is verified predictive success.

## Source index, evidence, tests, owner package

Chinese V25 cumulative original-text source index `tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V25.json` SHA256 **f5d2c95d6225bddc4b8a99fc5ddd923d61424a2002d5bb146c8693f72644c0df** (guarded/accepted locally): **216 BaZi +1059 Zi Wei =1275 historical annotations**, increment from prior 1269. Previous BaZi BZI-R0001–R0210 and all 1059 Zi Wei original text annotations preserved unchanged, old source indexes preserved in `recovery/`. Next original **BZI-R0217** section20 `通隔論`, separately pin a new raw original revision/SHA first. Completed twelve-palace online Zi Wei Volume II content remains accepted; possible future new Zi Wei note **ZWD-R1060** requires new independently pinned Volume III source.

Evidence files under `tasks/astro-chinese-primary-sources-20261017/batches/ChineseAstro-25SRC-BaZi-SourceFlow/`:
- `BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json`, `SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json`: per-component original CP, UTF8 byte, SHA256, role, original pillar order and unverified outcome flags.
- `freeze_bazi19_source.py`: pinned original extractor; **11/11 source-focused regression tests** `test_bazi25_original_source.py`.
- `build_bazi25_portable_archive.py` and owner cold-extractable evidence ZIP `/home/joel/Téléchargements/Astrology-BaZi-DiTianSui-SourceFlow-6-Original-Notes-V25-20261021.zip` (112274 bytes, SHA256 **83d9ba9c4e3153f21a431c7def138d7b86459777d14494ae5e6c6ec101c2ad03**), **17 archive members**, CRC and every member SHA/bytes verified, **11/11 cold-extracted source tests green**.
- Guarded `prepare_chinese25_index_v25.py` plus `test_bazi25_post_index.py`: **9/9 post-index tests green**, **20/20 combined targeted tests**. Broad unrelated project CI not run; none of these tests verifies astrological prediction in humans.
- `ORIGINAL_SOURCE_REVIEW_20261021.md`, `UNRESOLVED_SOURCE_LIMITS.json`, `ACCEPTANCE.json`, `CANONICAL_PREPARE_RECEIPT_20261021.json`, `SOURCE_RELEASE_RECEIPT_20261021.json` preserve critical source and evidence status. `state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md` and latest V25 state point to this chapter while retaining V24.

## Next safe autonomous research

1. Verify V25 local/remote exact Git SHA and index digest before any source changes. Next original BaZi `滴天髓/20` 通隔論 (Connection/Obstruction), first **BZI-R0217**, pin *actual* oldid and SHA. Preserve own exact Chinese verse, each commentary and all illustrative chart rows, and avoid over-scoring historical source claims; new isolated branch/worktree on SSD, no full HDD checkout.
2. Separately, review historical Zi Wei `紫微斗數全書 卷三` source (different volume, pin independent full SHA) and compare earliest woodblock Four Transformations rule cells before promoting any natal-engine rules.
3. Western accepted parent B07bh Lilly13271+Ptolemy1066 source annotations; separate B07bi imprisoned-source writer was unaccepted last checked. Reconcile actual remote status and writer before repeating any Western source work.
4. Prioritize deterministic natal chart calculations (solar terms, lunar/leap months, true local birth instant, Zi Wei star placement and BaZi strong/weak/flow mechanics), independent engine/source parity and clear falsifiable source-derived predictions. Freeze question selection, demographic nulls and decoys before new human answers. Retrospective user/Hale/merchant examples and the two historic Di Tian Sui tables are development/source context only.

**Zero independently blinded real-human predictive validations; zero runtime astrological rule promotions.** V25 source-only chapter is locally accepted; claim remotely accepted only after exact GitHub readback and clean worktree. Parent research mission remains OPEN.
