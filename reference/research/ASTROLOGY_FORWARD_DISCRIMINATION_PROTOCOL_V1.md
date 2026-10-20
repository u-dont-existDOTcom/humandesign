# Astrology forward discrimination contract v1 — a falsifiable layer, not a new astrology theory

**Date:** 2026-10-20 UTC; **scope:** Western Lilly/Hellenistic/Jyotish natal trait predictions, later Chinese BaZi and Zi Wei after chart parity. **Status:** implemented experimental evaluation adapter, not integrated into the production participant flow and not evidence that astrology predicts personality. It leaves historical source study and the pre-outcome Hale V2 forecast unchanged.

## Owner goal and diagnosis

The Hale comparison exposed a real defect: the source interpretation contained both sides of many personality axes, contextual disclaimers, broadly applicable coaching prompts, and positive/negative archetypes. A retrospective comparison awarded 'matches' without uniformly discounting such alternatives. The *independently frozen* project predictions were methodologically better preserved but often too broadly worded to distinguish a particular person's responses from other participants' responses. **Freezing a vague sentence does not make it discriminating.**

This protocol makes the prediction *surface* falsifiable and machine-scorable. It does not improve, rewrite, or prove the ancient rules. No rule is added just because it matches Hale. The already-existing project requirements for source-native chart fidelity, birth-time robustness, pre-outcome freeze, actual-human held-out testing, proper scoring and hard negatives still apply.

## Mandatory distinction: chart source != prediction != evidence of prediction

1. **Source-only / symbolic interpretation:** original astrological testimony, archetypes, strengths/shadows, speculative life guidance, alternative paths and contemplative questions. Keep all of them in the source/interpretation ledger. They may be useful culturally or reflectively, but **score zero predictions** unless translated into a separate, frozen measurable claim.
2. **Null/unresolved:** tradition gives conflicting testimonies or no directional contrast. Preserve this as NULL or UNRESOLVED without post-hoc reassigning the answer. Its presence reduces directional coverage, but is **not** a miss on a claim the model never made.
3. **Directional prediction:** select one most likely outcome among an exhaustive, mutually exclusive, predeclared response set. Specify actual real-life context, respondent recall window, observable measurement, rule provenance, and all outcomes that count *against* the preference. A probabilistic distribution must cover **every** outcome; no free-standing additional 'A or not-A' statement may earn an independent success.
4. **Conditional opposite outcomes:** predict contexts *before* seeing answers. If e.g. a person usually withdraws under stress **but** seeks others for instrumental responsibilities, encode distinct, independently measurable context-specific questions, or a predeclared joint-outcome categorical question with options including 'both' and 'neither'. Do not count whichever context happened to be mentioned after reveal. Genuine co-occurrence is allowed; free choice of contradictory stories is not.
5. **Observed evidence:** participant-blind responses captured after a verified independent model freeze. Wrong outcomes reduce the score; don't excuse them as latent gifts, shadow expressions, 'not-self', timing, trauma, unconsciously hidden motives or missing life lessons unless that contingency was independently measurable and frozen ahead of time. Unknowns stay unknown and lower coverage.

## Machine-checkable v1 adapter

Script: `scripts/score_astrology_forward_claims_v1.py`; tests: `tests/test_astrology_forward_claims_v1.py`.

Prediction input is UTF-8 JSON with schema `astrology-forward-claims-v1`. Top-level required fields:
- `study_id`, `arm_id`, `ruleset_version`, `phase` = `DEVELOPMENT|VALIDATION|FINAL_TEST`, `created_at_utc` ISO UTC;
- `chart_feature_sha256`, `questionnaire_sha256` — exact input hashes, not the raw private birth inputs;
- `probability_status` = `DECLARED_UNCALIBRATED|DEVELOPMENT_CALIBRATED`; **do not call hand-assigned probabilities calibrated**;
- `decoy_panels`: entries `{id, panel, panel_source_ref}`. Evidential phase requires both `matched` and `broad`; provenance and cohort independence need separate audit;
- `claims` array: every **candidate domain**, including NULL and UNRESOLVED, not just claims that sound promising.

Each claim requires `claim_id`, unique `question_id`, `status`, `domain`, `context`, `response_window`, `operational_definition`, `dependency_cluster`, `source_rule_refs`. NULL and UNRESOLVED require a `reason` and **cannot** carry scoring distributions. DIRECTIONAL additionally requires `outcomes` (two or more distinct exclusive choices), `preferred_option` (unique most likely outcome), `counterexample_outcomes` (all other outcomes exactly), `predicted` and `baseline` probability maps over every choice, `baseline_source_ref` (a *previously measured* distribution/model), and `decoys` (a probability map for each declared chart alternative).

Validator enforces: finite positive probabilities summing to 1; exactly one preferred outcome with a probability above the baseline frequency; no duplicate claim/question IDs; no dual full-credit alternatives; explicit counterexamples; complete decoy coverage; no directional-credit fields on nulls; and chronological, byte-hash-bound scoring responses.

**Important limit:** The validator cannot detect purely *semantic* duplication across different question IDs, dishonest source-base-rate provenance, all social/cultural leakage, birth-chart calculation errors, manipulation of preregistration dates or whether the claimed statistical probabilities are well calibrated. An independent reviewer must check these, and the complete package must be frozen in authenticated immutable history before the respondent answers. A string, a local timestamp or matching hash alone **is not proof of blinding**.

Responses use `astrology-forward-responses-v1` with `prediction_sha256` (SHA-256 of the *exact UTF-8 prediction JSON bytes*), `captured_at_utc`, and `answers` mapping question IDs to a single declared outcome. `__UNKNOWN__` and `__MISSING__` abstain and are reported; they never become successes. A response file must never be stored in the public repository without appropriate participant permission.

Commands:

```bash
python3 scripts/score_astrology_forward_claims_v1.py /private/frozen_predictions.json
python3 scripts/score_astrology_forward_claims_v1.py /private/frozen_predictions.json --responses /private/frozen_responses.json > /private/evaluation.json
python3 -m unittest discover -s tests -p test_astrology_forward_claims_v1.py -v
```

## Scoring and what it does NOT prove

For each answered directional claim and every chart alternative:

- **Multiclass Brier loss:** sum over outcomes of (declared probability minus observed indicator)^2 (lower is better). Model skill = baseline Brier loss minus true-chart Brier loss.
- **Log loss:** minus natural log of the probability assigned to the observed outcome (lower is better). True-chart log skill = baseline log loss minus true-chart log loss; true-over-decoy margin = decoy log loss minus true-chart log loss.
- **Miss penalty:** if the observed option is an explicit counterexample, the model receives its precommitted lower probability and generally loses relative to the baseline. Nothing is excused because another passage in a long narrative mentioned that outcome.
- **Repeated probes:** collapse per-question skill within each `dependency_cluster` to a cluster mean, then average clusters. This prevents repeated differently worded versions of one construct inflating total evidence. Report unscored nulls, incomplete responses, directional-claim coverage, and all decoy results.
- **Chart discrimination:** the true chart must beat matched decoys (same cohort/season/place as declared) and broad decoys. If every chart gives the same predictions, chart-specific advantage is **zero even if the person matches the description**.

The script reports a directional hit count as diagnostics but **never** equates it to predictive accuracy or statistical significance. It returns `independent_freeze_proven_by_this_tool=false` and `human_predictive_validity_proven_by_this_tool=false` explicitly. A nonzero positive skill on one person's already-known outcomes cannot validate astrology.

## Study protocol and matched baselines

- **Development:** use people whose outcomes were already known (including Hale) only for devising better, measurable constructs and identifying irreconcilable contradictions; do not re-label their success as validation. Inspect full source rule coverage, not just rules producing flattering matches. Preserve misses and nulls.
- **Freeze:** inventory all applicable currently frozen rule families before selecting a fixed set of meaningful directional tests; incomplete historical source coverage is disclosed, not converted into a new block on development testing; freeze rule families, allowed alternatives and source hierarchy, exact chart engine/ephemeris flags, question set, missingness, event windows, prediction/decoy probabilities, calibrated baseline, analysis, number of comparisons, and primary statistic. The source-study lane continues in parallel; adding future source rules creates a *new* model version, not a change to the frozen cohort's model.
- **Controls:** two panel types (nuisance-matched and broad), cohort participant-chart permutation, no-chart empirical frequencies, and when feasible demographic/season-of-birth controls. A strong text-only model of responses/traits is a valuable additional baseline. **Accuracy must beat the strongest relevant non-astrology baseline, not just a 50/50 coin flip.** Generic statements often fit nearly everyone; base-rate correction is central.
- **Independent human test:** start with small development pilot for wording/measurement; then a genuinely untouched, prospective person-split cohort, with full reported uncertainty/power calculation before choosing sample size. Analyze candidate-rule complexity and multiple testing. Do not pool Western/Jyotish/Chinese/HD/numerology after viewing outcomes to rescue one weak arm. Hold a separate final cohort for any fusion claim.
- **Stop or downgrade:** if consistent forward effects do not exceed the non-astrological baseline within a predeclared practical effect size bound, report failure for that model and reduce investing in interpretive complexity. A null result cannot prove *every possible* astrological rule false, but neither can changing the rules after every failure be presented as cumulative success.

## Representative failure scenarios (mechanically tested)

A uniform 'independent **or** accommodating' prediction with 0.5/0.5 outcomes is rejected: it has no unique forecast. A specificity-free model claiming the majority response at a lower probability than the baseline is rejected. NULL claims carrying probability maps are rejected. Contradicting answers earn negative skill. Identical predictions from the true and alternative chart give zero chart-discrimination margin. Missing answers remain visible with zero credit; duplicate question IDs are rejected; same-cluster repeat probes are capped; mismatched frozen-file hashes are rejected.

## Relation to previous artifacts

- Existing descriptive chart coverage: `reference/research/ASTROLOGY_DEEP_ANALYSIS_PROTOCOL_V1.json` and `scripts/validate_astrology_deep_analysis_receipt.py` already ensure positive/negative testimonies and nulls are documented. These *do not* prove discriminating predictive claims; this adapter is a separate opt-in downstream layer.
- Source archive: B07bb Lilly / Chinese V7 untouched by this change.
- Frozen Hale first pass: `tasks/hale-cleanroom-first-pass-20261003/FIRST_PASS_PREDICTION_RECORD_V2.md` untouched by this change. Hale's old descriptive '6 vs 4' score was expressly withdrawn after detecting alternative-outcome bias; it is NOT repaired retroactively by translating her known answers into this new schema.
- HD forward-blind: `docs/20_forward_blind_prospective_validation.md` remains its own mechanics and does not become one pooled astrology success score.

## Existing empirical literature (background, not a substitute for our test)

- Carlson, *Nature* (1985), DOI `10.1038/318419a0`: double-blind natal-personality study reporting negative results; Ertel's later reanalysis in the *Journal of Scientific Exploration* disputed the strength of that negative result, itself not decisive validation.
- Hartmann, Reuter & Nyborg, *Personality and Individual Differences* 40 (2006), DOI `10.1016/j.paid.2005.11.017`: large cohorts found no conventional date-of-birth/Sun-sign relation to personality or intelligence. That does not exhaustively test all precise multivariate horoscopic methods.
- Preregistration principles: *Psychological Science*, Association for Psychological Science, recommended plans locked and timestamped before data inspection. The project requires the same distinction between exploratory development and locked confirmation.