# Outcome-blind Jyotish forecast: frozen-package inspection and first questionnaire scoring

**Review date:** 2026-10-21, Africa/Dakar. **Status:** completed one-person historical/development evaluation; chart-specific predictive lift NOT ESTABLISHED. The original author is reported by the owner to have been blinded to survey and biography; preserve that as the working premise. Do not misdescribe this as an outcome-informed original reading. The subsequent evaluator necessarily read responses.

## Parent owner outcome

The owner submitted the original interpretation catalog, the newly frozen testable JSON, and an answered version of the blinded questionnaire, and asked to check whether the new forecast is technically sound and whether its recorded predictions outperform guessing. Preserve all wrong, ambiguous and future cases. Continue natal astrology research separately with newly untouched participants; do not rewrite this frozen forecast after scores are known.

## Files examined (public artifact integrity only)

- Original-passage workbook: 138 rows, 13 consolidated themes. Reported SHA-256 matched: `725f92ea840af45b5db306d23612da4246b280b9d3d5d957a2c16f8903c5767b`.
- New frozen prediction JSON: 36 scored records (31 primary Lahiri, five secondary Kala probabilities on identical question outcomes), ten explicit abstentions, 31 unique questions. Reported SHA-256 matched: `1492241599d344094e87d17d36c21659e4e8632f5bea6d9f90ad1c9cd90f7e1b`.
- Answered seven-page `.odg` drawing: different file format and modified content compared with the original frozen PDF. **The original PDF file hash was not independently verified.** All 31 rendered text-layer questionnaire question stems matched their frozen JSON questions; 26 had exactly one answer checkbox marked, five future questions none. Of the 26 marked, five explicitly say missing/unclear.
- The original narrative catalog contains three abbreviated excerpts mislabeled as strict contiguous VERBATIM (`A005`, `A038`, `A106`). They are text annotations rather than audited exact quotations. Preserve the original frozen files; correct in a separately versioned erratum if needed.

## Purely aggregate evidence (NO private response records or individual labels)

For the fixed `lahiri` primary arm, **21 of 26 historical/personality questionnaire items** were actually answered with one of the frozen two outcomes; five were explicitly missing. Preferred forecasted outcomes matched in **11/21 (52.4%)**. Its mean **two-category summed Brier loss = 0.5072**; a fixed uniform `p(yes)=0.5` comparator has 0.5000. Its mean log loss = 0.7012; uniform comparator 0.6931. Lower losses are better. This small negative performance difference is an outcome of this case only, not a population significance estimate.

Within the primary set: personality/lifetime portion = 10/18 preferred-outcome matches, Brier 0.4820; dated historical portion = 1/3 matches, Brier 0.6584. All six gradeable primary forecasts whose preferred outcome was **No** were answered **Yes**. Respondent Yes was the majority among the measured lifetime outcomes; a post-hoc constant-Yes hit-count baseline looks substantially better than model hit count, but is NOT a calibrated prospective control.

For the four answered questions with separate Kala probabilities, **Kala = 3/4 preferred-outcome matches and Brier 0.3718, vs Lahiri = 2/4 and Brier 0.4839 on those same four observations**. It is neither an independent second cohort nor sufficient basis to promote a different zodiac. The predeclared primary arm stays Lahiri.

Five distinct future questions (six model-specific records) are **PENDING**, not wrong or absent, until declared windows and duration-verification periods close.

A dependency sensitivity analysis over 13 author-declared construct groups gives mean Brier skill vs uniform `-0.0199`. Aggressively collapsing all declared inter-claim links gives six connected groups and mean skill `-0.0354`; these are sensitivity definitions, not proof that connected claims are independent.

## Scientific and scoring limitations

- No externally measured no-chart endorsement frequencies for the exact binary questionnaire options. Uniform 0.5 is an illustrative uninformative benchmark, **not** the expected chance rate for these broad lifetime events.
- No unrelated-chart forecast probability vectors covering the same questions exist in the submitted JSON. Thus neither source-chart discrimination nor gain beyond population guessing can be concluded. This is the central unfinished scientific gate.
- One respondent's self-reports are not independently corroborated external events and several lifetime/career conditions are genuinely ambiguous. Five missing are correctly not forced into No.
- Relocation questions of different temporal specificity can be supported by the same actual event. They are different bets but not independent behavioral outcomes; group them in uncertainty analysis.
- Many probabilities cluster around 50–60%; several high-confidence forecasts predict nonoccurrence of relatively rare future events. Those need real base-rate controls rather than inflated success counts.
- Hash agreement confirms the current A/B files match the stated original hashes, **not** independent third-party proof of source author context or that generation preceded access to all life information. The owner's explicit account of chart-only generation is respected.

## Next executable work frontier

1. Keep the submitted prediction JSON byte-identical and archive this aggregate review. The prepared private review includes a question-level marked-answer extraction, likelihood/Brier ledger, scoring workbook, and missingness adjudication notes; it is not published.
2. Resolve genuinely ambiguous respondent-defined categories only under the frozen original meanings. Do not recode categories to benefit the astrologer, and never score future nonoccurrence early.
3. For a genuinely chart-specific test, separately generate source-blinded readings for **unrelated birth charts** using the same question bank. Freeze all distributions before disclosing any responses, compare against actual cohort survey responses and a held-out nonchart baseline, and analyze respondent-wise dependence.
4. The current result is **not positive evidence above even the uniform benchmark**. That does not falsify all Jyotish rules, but does provide honest negative evidence for this particular declared probability package.

## Data boundary

This is a **public repository**. No answers, question-by-question score labels, private respondent comments, past survey text, or private answer file checksum appear here. They remain in separately delivered owner-private artifacts. This report does not alter the historical original chart reading, frozen prediction records, or the project's accepted source-research branch.
