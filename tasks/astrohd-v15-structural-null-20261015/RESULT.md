# AstroHD V1.5 — structural rank audit (2026-10-15)

**Outcome:** Structural-null diagnosis completed. Human birth-date identification remains **unvalidated**. The accepted V1.4d fitted six-rule astronomical result remains intact.

## Why the first-place result is predetermined

The September 25 V1.4d model selected six astronomical conditions satisfied at the already-known birth instant. The century scan verified 9 maximum-scoring minute-grid instants, all on one date, including the recorded time. This is a reproducible development fit, not a prospective prediction.

V1.5 kept those six rules and assigned modern interpretations from five neutral behavioral domains. Each clause yields +1 when the compatible behavior is supported, -1 when explicitly contradicted and 0 when unknown/mixed.

**Exact finding:** Since the fitted target satisfies *all six* astronomical clauses, any profile producing only positive or zero clause signs automatically gives it the mathematical maximum score against every conceivable six-bit competitor. It must rank **jointly first** in any decoy panel. Other charts may tie.

The previously reported provisional sign vector was `[+1,+1,+1,+1,0,+1]`: five positive clause votes, no negative votes. It came from just **three positively coded behavioral domains** (sharing insight, solitude, romantic connection); romantic connection supports three clause votes. Role entry and persuasion were mixed. The provisional full five-domain profile was researcher-coded, **not separately participant-confirmed**.

## Exhaustive code enumeration — no new astronomy scan

Exactly 3,125 combinations (five permissible codes across five behavioral domains) were enumerated using the untouched V1.5 bridge. All 64 possible chart feature masks were scored.

| Measure | Count |
| --- | ---: |
| Total five-domain code profiles | 3,125 |
| Unscorable all-zero profiles | 324 |
| Scorable profiles | 2,801 |
| Profiles guaranteed joint #1 for fitted full-six-clause chart | **956** |
| Profiles containing explicit negative clauses | 1,845 |
| Distinct six-rule sign vectors achievable | 162 |

956/3,125 = **30.592%** (34.13% of scorable profiles). These are uniformly enumerated hypothetical code combinations, **not a population estimate**. For the provisional five-positive/one-zero case, exactly two hypothetical masks (47 and 63) share the maximum possible score 5, regardless of how many random candidate dates were sampled.

## Actual 9,999-decoy negative controls

The original V1.5 panel seed, frozen model/bridge/scorer, Swiss files and exact candidate-panel hash were independently verified against the previous owner's private panel receipt. Only aggregate results enter Git; raw feature-mask counts, geographic coordinates and any private birth details remain owner-local.

| Hypothetical coded profiles on the actual fixed 9,999-decoy panel | Count |
| --- | ---: |
| Scorable profiles | 2,801 |
| Profiles yielding rank_best #1 for the fitted chart | **1,037** |
| Profiles yielding #1 with zero sampled ties | **166** |
| Profiles with negative contributions **still** yielding #1 | **81** |

The provisional respondent profile remains rank_best=rank_worst=1 on the same panel, but this is guaranteed given the full-six-feature target and nonnegative scoring signs. The all-supported profile also ranks first by construction. The absence of sampled ties is a separate, weak observation.

The source-verified original century scan's ordered rejection counts are `[43863794,8172234,547429,11912,615,8,9]`. For the five-positive, one-zero model, its fast-rejection logic bounds the number of maximum-scoring one-minute candidates to **9–624** across 52,596,001 minutes, or **8–623** other instants besides the recorded minute. The exact number of five-rule maxima remains unknown without a further scan. For a uniformly randomized panel of 9,999 alternative minute instants drawn without replacement, the probability of **no** sampled maximum-score ties is bounded between **0.888296 and 0.998480**. This is a mathematical sampling bound, not a full-century rerun and not a confidence interval.

**Decision:** The previous reports of #1 against 999/9999 decoys do **not** establish new questionnaire-to-birth information in this fitted development case. They should no longer be described as encouraging independent recovery.

## Engineering controls completed

- A pure deterministic evaluator enumerates every allowable five-domain response profile and every possible six-bit chart mask using the **unchanged frozen scorer**.
- A second evaluator reuses the original fixed 9,999-decoy panel, compares all 3,125 profiles and reproduces the previous panel/hash provenance.
- A third independent-cohort evaluation utility calculates an N×N respondent-profile vs independently calculated chart-mask score matrix, ranks true pairings and tests chart-label permutations. It retains unscorable respondents and distinguishes exact permutation nulls (N up to 8) from seeded Monte Carlo (larger cohorts).
- Actual personal input, raw questionnaire answers, source hashes tied to private files, and birth/place data were not committed. No V1.4d rule or V1.5 behavioral bridge, questionnaire or live deployment was modified.

## Next real scientific step — untouched humans

The existing participant-facing V1.5 birth-date research page was live-checked on October 15 with HTTP 200 and the expected frozen V1.5 behavioral-bridge hash. It already offers nine original behavior-first questions (or imported existing answers) plus manual review of five neutral interpretations. The optional credit-consuming AI interpretation is not required.

**The next missing evidence is at least one previously untested, consenting participant with a reliable independently supplied birth date/time and a first frozen neutral response profile.** Their chart must not have participated in selecting the six rules, question wording, or behavioral mapping. Freeze their review before birth-time/chart identity is revealed to the evaluator, retain skips and contradictions, and compare the true-chart score against seeded 999 and 9,999 alternatives with an all-positive baseline. Record negative outcomes, ties and profile-hash provenance; do not retune until the first result is archived. For a cohort, use the N×N identity matrix and permutation null, not owner-case rankings alone.

No untouched participant with a completed first frozen profile/birth pair was ingested or claimed in this pass. The owner need not re-answer any Life Patterns question. There was no outreach, participant-data access, payment, or new service deployment.

## Reproducible evidence

- Frozen source model: `tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-SIX-RULE-MODEL-20260925.json`.
- Verified exact century scan: `tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-EXACT-CENTURY-RESULT-20260925.json`.
- Signed behavior bridge: `reference/research/astrohd_v15_behavioral_bridge.json`.
- Unchanged candidate scoring: `src/hdmatch/evaluation/astrohd_v15_decoder.py`.
- Exact math and complete-profile enumeration: `audit_structural_null.py`; aggregate `AGGREGATE_RESULT.json`.
- Frozen sampled-decoy null: `audit_panel_null.py`; aggregate `AGGREGATE_PANEL_RESULT.json`.
- Consenting future cohort N×N evaluator: `cohort_rank_audit.py` (does not certify upstream consent/time-freeze provenance).
- Private pre-panel freeze and actual mask histograms are stored only in the owner's Downloads directory, protected with mode 0600.

**Progress classification:** Direct owner-goal validation remains **UNMET**. The negative-control result resolves why the owner development #1 figure cannot be used as standalone evidence of questionnaire predictive performance. The next gate is genuine independent participant evidence, not additional elaboration of the same person's questionnaire.

## Final verification receipt

- Repository-wide unit/integration tests with the working Swiss files exposed through `HDMATCH_EPHEMERIS_PATH`: **1,083 passed, 3 skipped** (the remaining skips require separate official HD chart smoke files, unrelated to this AstroHD audit).
- Focused structural, panel-null and cohort-matrix tests: **23 passed**.
- Authored Python lint and formatting: PASS.
- Exact same original model, behavioral bridge, scoring module, Swiss-file digests, seeded candidate-panel hash and independent panel size were verified by private readback, including the latest audit source hash.
- Owner-delivered HTML audit, next-participant protocol and researcher guide rendered in headless browser without page errors or outside network requests. Local report bytes were checked and mode-0600 delivered.
- Live existing V1.5 research interface: fresh read-only HTTP GET 200 and five-domain/nine-question contract match; this does not certify a new live participant submission.
- No private chart/source materials were staged in Git. The complete verification state is also recorded in `VERIFICATION-RECEIPT.json`.
