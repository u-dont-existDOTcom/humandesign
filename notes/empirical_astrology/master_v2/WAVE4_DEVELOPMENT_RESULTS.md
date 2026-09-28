# Wave 4 development results

Date: 2026-09-28

## Outcome

Wave 4 completed the authorized mechanical evaluation of the frozen v1b model.
No eligible raw, non-owner same-hospital IPIP development dataset exists in the
tracked repository. Consequently, Wave 4 ran **zero human empirical tests** and
produced no empirical effect estimate, confidence interval, p-value, power
estimate, or evidence for or against the frozen association.

The machine-readable result file contains 36 rows:

| Status | Rows | Meaning |
|---|---:|---|
| `NOT_EVALUATED` | 20 | Required human-data comparison could not run because the frozen outcome/covariates and eligible cohort were unavailable. |
| `NOT_APPLICABLE_NO_INCLUDED_FEATURE` | 9 | CF-001 through CF-008 and the all-astrology ablation cannot be removed because no astrology feature is included. |
| `PASS` | 7 | Deterministic engineering fixture passed; this is software evidence only. |

Governing checkpoints:

- corrected evidence: `e7f82ab4a1b08705bf4429958a0d577b2758c407`;
- frozen Pro decision: `e1c61d441bf8516c88d866a59d871cd8ee72f009`;
- v1b implementation: `2d49b20b0721b2f567bfa5cdf1399b5f6cccab5f`;
- runner and typed implementation used for this result: `c4959b12c8bc27158c37ae14862d10d471b53619`.

## Input boundary and leakage control

`experiments/empirical_astrology/wave4/input_manifest.json` is the complete
allowlist. Its selected human-development file list and eligible dataset-ID list
are both empty. The run did not open owner-known outcomes or untouched
prospective outcomes.

The inventory excluded, without treating them as failed studies:

- 26 tracked literature registries/manifests/extraction files, because aggregate
  reports are not participant-level paired outcomes;
- 28 Astro-Databank relationship/event files, because they have the wrong
  outcome/design and lack the frozen sampling/covariate fields;
- 14 development-case files, because they are outside v1b and may contain
  inspected or owner-linked outcomes;
- one synthetic Human Design measurement fixture, because it is neither human
  IPIP evidence nor a same-hospital cohort;
- 13 owner- or person-named paths, which were denylisted and not opened.

No semantic biography pipeline, chart label, sign, aspect, orb, angularity,
Gauquelin sector, Vedic rule, clinical classification, or owner-specific result
entered the assembled model or evaluation.

## Required comparisons

The frozen full model and theory-neutral model are definitionally identical:
both contain TN-001 and no astrology column. The following empirical analyses
were `NOT_EVALUATED`:

- frozen full model and theory-neutral birth-time-distance model;
- intercept-only, date-only, time-only, site-only, season/cohort,
  full-conventional-null, time-distance-only, and full-plus-TN-001 baselines;
- twenty random-feature diagnostics and the maternal-age negative control;
- all twenty leave-one-network-out fits;
- lower and upper birth-gap-bound sensitivities;
- strict-precision, belief-level, and sign-knowledge summaries;
- development-residual null calibration at beta 0 and power simulation at beta
  0.01.

The last two remain launch-blocking because there is no declared, hash-bound
non-owner residual template with the same instrument and frozen 20-network by
100-pair design. Literature summary effects were not substituted.

## Robustness and ablations

No empirical robustness conclusion is possible. The required LOO, interval,
precision, and knowledge-stratum analyses lack eligible observations.

Every CF-001 through CF-008 ablation and the all-astrology ablation is
`NOT_APPLICABLE_NO_INCLUDED_FEATURE`. This means the relevant model column does
not exist; it is not a zero effect, a successful null, or an independent failure.
The model was not changed after any Wave 4 output.

## Null baselines and multiplicity

No empirical null, baseline, or negative-control test ran. Accordingly:

- empirical primary tests: 0;
- empirical diagnostic tests: 0;
- corrected empirical p-values: none;
- data-dependent model choices: none.

A code fixture verified that exactly 21 diagnostic p-values are handled as one
Holm family. A separate synthetic WLS fixture exercised CR1 inference, lower and
upper exposure bounds, all 20 LOO fits, and deterministic restricted wild-cluster
bootstrap replay with 99 draws. The prospective requirement of 99,999 draws was
not run, and the fixture did not use the required development residual template.
Its numerical values are deliberately labeled engineering metrics, not effects,
power, calibration, or human evidence.

## Cohort structure and dataset reuse

Eligible human people, pairs, hospitals, and independent networks were all zero.
No historical cohort was fitted, pooled, or counted again. The synthetic
software fixture is not a cohort. The expanded literature registry's dataset
reuse and independence corrections remain evidence metadata; they do not become
Wave 4 observations.

## Engineering results

Seven engineering checks passed:

1. decision/registry/model raw-byte hashes, evidence ancestry, and authorization;
2. empty astrology feature/mapping/interaction/weight surface and full/neutral equivalence;
3. complete IPIP-50 reverse-key scoring and distance endpoints;
4. UTC gap bounds, symmetric pair hash, fourteen nuisance columns, and twenty deterministic random columns;
5. synthetic WLS/CR1, gap-bound, LOO, and bootstrap seed-replay paths;
6. the exact 21-test Holm family;
7. empty human-data allowlist and owner/prospective outcome access boundary.

The focused implementation suite passed 39 tests. Ruff passed for the empirical
astrology code, tests, and Wave 4 runner.

## Artifact hashes

- input manifest SHA256: `79d14781465946339c37a36ce5771cbbb3b8da382a90cbe3a0c9f8d04622767b`;
- results JSONL SHA256: `3e91f16171e7925770c18f3edc87a3536e8b08eeb11bae6bd4cf980cc0880409`;
- engineering summary SHA256: `c0bb97bc27f85c39c61c40c21ba772c37d413c3b4c124125b81af7e881a37549`.

## Limitations and failure report

The central Wave 4 limitation is not a weak estimate but the absence of an
eligible development dataset. The correct result is `NOT_EVALUATED`, not a null.
Prospective recruitment and outcome collection remain unauthorized and blocked.
This work therefore cannot justify a scientific model revision, a validation
claim, an astrology claim, or person-level use. Scientific adjudication remains
with Pro.
