# V1.4d full-century exact minute-grid result

Completed: 2026-09-25 02:09:32 UTC. Classification: unchanged-model, target-aware owner-development audit; not a completed questionnaire decoder or independent human validation.

## Direct result

Every UTC minute from **1926-08-24 10:42** through **2026-08-24 10:42**, inclusive, was checked: **52,596,001 candidate instants** at the same fixed Philadelphia location used in the earlier experiment.

There are **nine** maximum-scoring minute instants. All are on **1985-01-29**, from **10:18 through 10:26 UTC**, inclusive. The recorded **10:25 UTC** scores **6**, is tied for first, and has **zero higher-scoring candidates**. The date is the only date with a maximum on this complete minute grid. The separate 2013-01-28 08:30 UTC comparator scores **1**, not rank 1.

The six rules, source mapping and one-vote-per-rule weights were unchanged. No new combinations were tried; no answers were changed. Raw and the declared lineage-deduplicated versions coincide for these six nonduplicate clauses.

## What makes this a stronger century check

The previous scan used interpolated planetary coordinates with numerical guards to screen possible maxima. This run did **not** use interpolated coordinates or numerical screening allowances to exclude any minute.

Instead, it directly evaluated exact Swiss Ephemeris inputs for necessary clauses at every grid position. Because the fixed model consists of six Boolean votes and the target reaches six, a candidate can be safely excluded from the maximum set as soon as one actual clause is false. This establishes all co-winners without computing every lower-scoring candidate's complete six-condition score. It is not a claimed histogram or full ranking of the losing candidates.

The exact scan therefore removes the old interpolation-screening uncertainty **for this one-minute grid**. It does not enumerate every possible second or prove continuous-time uniqueness. The earlier local transition calculation, approximately 10:17:52–10:26:12 UTC, remains separate evidence; the present global result is explicitly minute-resolution.

## Verification and execution evidence

- The same two production ephemeris files were used, with their original SHA-256 hashes checked. The engine was Swiss Ephemeris 2.10.03; Moshier fallback was rejected on every evaluated planetary call.
- The optimized predicate path matched the original full-snapshot six-rule scorer on **1,211** verification cases, including broad seeded century samples and local transition cases; **zero disagreements**.
- The focused/affected test run passed **18 tests**, including six new exact-scan tests for fallback rejection, endpoint coverage, neighboring-time ties, original-model parity and Julian-minute arithmetic.
- Post-run readback verified **211 nonoverlapping contiguous chunks**, **zero missing minutes**, **zero overlapping minutes**, and consistent rejection/match counts totaling 52,596,001.
- All nine maxima were rescored through the original full model in a separate replay. All scored six; the 2013 comparator scored one.
- A connector session/output failure interrupted progress collection. The existing process had ended before recovery action was taken. The same frozen run resumed from its **130 saved chunks**, without rerunning those completed chunks or changing rules. The final artifact covers all 211 chunks. Its `elapsed_this_invocation_seconds` is the resumed invocation only, not the complete task elapsed time.
- The published result was downloaded and its SHA-256 matched the original execution file exactly.

## Artifacts

Canonical result: `experiments/astrohd/v14_exact_century_20260925/result.json`.

Coverage and replay readback: `experiments/astrohd/v14_exact_century_20260925/coverage-audit.json`.

Result SHA-256: `4cba5a3107f7b7afb0fd289774e67ac8e2410aa04465b431c98992f5b3f87b84`.

Full per-chunk coverage manifest SHA-256: `b57c55dac932eb0f2ee525ce22e4b5bb20830733ff3fa23510df43d367c4e2d4`. The complete coverage manifest and original run artifacts are also preserved inside the authorized runtime's humandesign checkout. No private survey transcripts or profile codes were sent to that runtime or published.

Reproduction uses `scripts/scan_astrohd_v14_exact_century.py`, the unchanged six-rule manifest, and verified production ephemeris files. Redirect long-run stdout/stderr to a durable local log; an explicit `--resume` checks the same freeze and reuses completed chunks.

## Answer-dependent decoder remains unfinished

See `ASTROHD-V14-SURVEY-DECODER-GAP-20260925.md`. The saved six-rule scorer does not take the current survey answers as runtime input. Answers influenced development-time eligibility; the known target informed selection. A frozen general model could accept changing answers, but this artifact is a frozen personalized rule list.

A completed decoder needs an explicit tested path from updated answers through neutral recoding and behavioral interpretation to fixed rule-based candidate scoring and reranking. It must not secretly refit to the recorded target on every edit. This path was not invented or implemented as part of the fixed-model century audit.

The current request's explanation and century audit are complete. The parent survey-based recovery project remains OPEN, with the missing answer-conditioned comparison and survey-update connection explicitly owned. A successful fitted signature must not be laundered into completed survey-decoder functionality.
