# Current state — exact V1.4d century audit; answer-conditioned decoder open

Updated 2026-09-25. Branch: `chat/v14-answer-link-century-20260925`.

Read `tasks/ACTIVE-TASK.json`, then:
- `tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-EXACT-CENTURY-RESULT-20260925.md`
- `tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-SURVEY-DECODER-GAP-20260925.md`

## Owner outcome

Continue developing survey-based birth-date/time recovery from one combination of established astrology rules, allowing explicit target-aware owner development without arbitrary fitted numerical astrology weights. Do not replace a pooled model with a requirement that every tradition succeeds alone. A fitted signature is not automatically a finished survey decoder.

## Current request completed

The owner asked whether survey-answer edits currently change the saved six-rule score, what remains unfinished, and then requested the full century scan. The missing answer dependency was inspected and documented. The unchanged-model exact century audit is complete; no rule combinations, behavioral meanings, weights or answers were changed.

Every minute from 1926-08-24 10:42 UTC through 2026-08-24 10:42 UTC was checked directly: **52,596,001 instants**, across **211 contiguous chunks**, with zero gaps and overlaps. No interpolation-based screening was used. All maxima were replayed through the original full scorer.

Only **1985-01-29** contains a maximum. Its nine tied minute samples are **10:18 through 10:26 UTC**. The recorded **10:25 scores 6 and is tied for first**; zero candidates score higher. The 2013 comparator's **score is 1**, not rank 1. The six rules remain five Lilly clauses and one Phaladeepika clause, each with one equal vote.

Canonical result: `experiments/astrohd/v14_exact_century_20260925/result.json`, SHA-256 `4cba5a3107f7b7afb0fd289774e67ac8e2410aa04465b431c98992f5b3f87b84`. Published bytes were read back and matched the execution result. Original-scorer parity: 1,211 cases, zero disagreements. Focused/affected tests: 18 passed.

## Unfinished functionality — do not omit

The saved V1.4d scorer **does not read current survey answers**. Answers were used for development-time rule eligibility before target-aware subset selection. The saved artifact subsequently scores candidate charts against the six fixed conditions.

Therefore editing a survey answer does not automatically rerank this model. A fixed model can have changing inputs, but this artifact froze a personalized rule list rather than implementing `score(answers, chart)`. The missing path is changed answer -> neutral recoding -> updated behavioral profile -> explicit fixed answer-to-rule comparison -> candidate scores -> reranking. Survey UI/update integration is also not completed for this path.

Do not conceal this gap by quietly rerunning target-aware selection against the known birth date after each answer edit. Separately versioned target-aware training remains authorized. Unknown is not an automatic contradiction. Semantically unchanged or irrelevant answer edits need not move scores, and score changes need not always move ranks. Identical feature vectors remain tied.

## Preserved limits and history

The new calculation removes the old interpolation-screening uncertainty for the specified minute grid. It does not enumerate every second or prove continuous-time uniqueness. The earlier local plateau estimate, approximately 10:17:52–10:26:12 UTC, remains separate evidence. The old full-library identity finding explains why the neighboring minute tie cannot be broken by reselecting the unchanged 390-feature library.

This is a fitted owner-development result, not independent human validation. The parent questionnaire-decoder outcome remains **OPEN**. The requested explanation and exact-century audit are **COMPLETED**. No research worker is left running or background delivery promised.

UDA goal-protection repair remains merged via PR #253 at `91e4be060ca99151264f1f90ad4f9c19aaf05bcb`. Historical staged results and fixed-combination diagnostics remain in the task directory and Git history. Private answer transcripts and coding remain outside Git and were not sent to the century runtime.
