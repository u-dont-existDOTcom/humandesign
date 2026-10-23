# Hellenistic source continuation — C09 durable checkpoint

**Date:** 2026-10-23. **Status:** OPEN source research. **Human predictive validations:** **0**. **Historical-source arithmetic tests:** **58/58 PASSED** after this batch. No release/merge gate or independent manuscript authentication was performed.

## Resume precisely here (do not repeat)

1. Live bootstrap: `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md`; `u-dont-existDOTcom/humandesign/AGENTS.md`, then this checkpoint. Follow the source/target/blinding constraints. This C09 handoff **supersedes only the next-step pointer** from C08, not the actual C08 Greek transcription correction.
2. **Parent/integration checkpoint:** `research/astro-missing-book-audit-20261022`, exact inspected base commit `5829f8ba7171872f1b7c4f33617a69ba3bfd40b7`.
3. **Isolated C09 worker branch:** `research/astro-hellenistic-c09-epitome-20261023`. All new work is limited to `docs/astrology-research-map/` source evidence, tests and C09 pointer. **Do not blindly commit to the parent research branch or merge into production.**
4. **Main new finding:** Pingree's Epitome IV §44 365-day parent periods have seven literal Greek finer allocations; **only Jupiter and Mars close**, while **Saturn +1, Sun +1, Venus +1, Mercury +1, Moon −3**. Seven parent totals sum **365**, seven child totals **366**. These are source-integrity facts, not chart predictions.
5. **§37 advanced but NOT complete:** Jupiter's 12-month child row sums 365, consistent with the five-day annual supplement rather than necessarily a scribal error. Venus's eight-month row tentatively sums **213 vs 240**; independent glyph confirmation still needed. Mars's Jupiter child glyph may mean 42 or 52, corresponding to candidate totals **450/460**; DO NOT use closure to decide what was printed. Sun/Mercury/Moon remaining rows still uncollated. The C08 correction remains: Saturn→Mercury printed **40**, algorithm-derived **140**, main Hephaistio II.29 **150**.
6. **Next source comparisons:** Obtain/inspect Æ. Boer's **1958** Greek Paulus edition and **1962** attributed Heliodorus commentary with Neugebauer/Pingree to resolve **34/120** monomoiria table disagreements (currently no Greek diagram inspected). Obtain/verify the original documentary image of **P.Oxy. 4277** from a legitimate holding collection/portal before upgrading the earlier scholarly-transcription **1/3** match. Do not bypass access controls.
7. Purchased Gansten Amazon *Primary Directions* ebook remains outside local study corpus. **Do not use Work to extract it.** Do not select historical readings based on known biographies, adjust production scoring, merge into other systems or claim human validation.

## Recover exact C09 artifacts

- `HELLENISTIC_SOURCE_C09_COMPLETE_FINE_ROWS_AND_OPEN_GLYPHS_20261023.md` — direct inspection notes, novel residuals, uncertainty, bibliographic next witnesses.
- `HEPHAISTIO_C09_FULL_FINE_PERIOD_AND_OPEN_GLYPHS_V1.json` — source evidence with seven §44 rows, additional §37 cases, editorial separation, negative cases and missing-authentication labels.
- `test_hellenistic_c09_greek_subperiods.py` — **9** C09 source-only regression assertions; original 49 retained.
- `README.md` — canonical map's latest Hellenistic checkpoint pointer (earlier lanes preserved verbatim).

## Verification and boundaries

Exact narrow source test:
```bash
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
Receipt on isolated C09 worktree: **Ran 58 tests ... OK**, command exit **0**; nine new C09 tests and 49 existing. No general test release boundary or human chart evaluation was attempted. Printed numbers were manually read from authorized Pingree Vol. II study PDF, verified SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`; original Greek PDF and images **not committed**. This is one modern edited textual witness, not multiple independent ancient testimonies.

**One-line resumption:** Begin with C09 §44 full printed child register and uncertain §37 Mars numeral; inspect independent Greek apparatus next, then 34 disputed Paulus cells and P.Oxy 4277 image; preserve negatives, keep model unscored, no Kindle extraction.
