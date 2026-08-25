# Astro-Databank holistic canonical interpretation

**PHASE: DEVELOPMENT**

Date: 2026-08-25

This document is the **superseding endpoint** for the 2026-08-25 Astro-Databank holistic development work. It does not delete or rewrite the earlier exploratory audit. The earlier audit remains useful failure-analysis history showing how apparently strong whole-chart results can arise from incomplete positive-unlabeled semantics, cohort structure, and archive-source structure.

## Canonical data and engine

The final reproducible run uses the exact official Astro-Databank C sample bytes with SHA-256:

`a88b12d1edc47651319d33e5a1c47c002db44e6dbf99374e5943ff9c10ae9b17`

The chart engine uses the repository's verified pinned Swiss Ephemeris files and rejects fallback. The canonical ephemeris file-set SHA-256 is:

`f5644c27e3682b805ebdde58d593e5a53abfbaca1dc8c52f29f1cd06f2d5c401`

The conservative archive filter yields 4,750 A/AA timed public figures before engine-coverage exclusions. After the requested behavioral/vocation scope and verified-SWIEPH requirement, 4,366 people have usable chart + phenotype data. Fifty-three scope-eligible historical records are excluded because the repository's existing pinned Swiss block cannot calculate their full chart without fallback; they are not silently downgraded to Moshier.

The canonical model is the DEVELOPMENT-selected fast-body carrier representation:

- Personality + Design Sun gate/line;
- Personality + Design Moon gate/line;
- Personality + Design Mercury gate/line;
- Personality + Design Venus gate/line;
- Personality + Design Mars gate/line;
- K = 200 whole-chart neighbors;
- five-fold person-level cross-fitting;
- up to 50 deterministic matched decoys per person;
- candidate matching by sex + exact birth year + normalized nation;
- label opportunities conditioned during both background estimation and neighbor selection;
- dependency-normalized observed behavioral labels;
- 2,000 candidate-exchange randomization iterations.

The aggregate artifact is:

`reference/audits/astrodatabank_holistic_canonical_2026_08_25.json`

## Canonical pooled result

Evaluable people: **3,328**

Mean true-chart percentile: **50.794%**

Median true-chart percentile: **50.0%**

Candidate-exchange empirical p-value: **0.09545**

This is near chance and is not compelling evidence for whole-profile chart identification in this archive formulation.

The slow pre-cache canonical run and the optimized cached run produced the same aggregate statistics and the same report SHA-256:

`da922b21b02cd00d00047288e927e524d9993dedffb3e553512f2a7ff4518ba1`

Therefore the performance cache changed runtime, not the statistic or model semantics.

## Country transport

The corrected country-specific results are also null-like:

| Nation | Evaluable people | Mean true-chart percentile | Randomization p |
|---|---:|---:|---:|
| France | 1,086 | 49.293% | 0.7901 |
| United States | 1,333 | 50.786% | 0.1809 |
| Italy | 282 | 50.284% | 0.4328 |

Brazil and the United Kingdom are unevaluable under the frozen K/opportunity constraints and are reported as such rather than rescued by lowering K after inspection.

The earlier exploratory French result around the mid-60th percentile is therefore **superseded**. It disappeared after the training-time opportunity bug and archive-control problems were corrected.

## Collector-blocked result

A stricter run blocks the TRAINING neighborhood by Astro-Databank collector and also matches candidate decoys by collector, in addition to sex + exact birth year + nation.

Artifact:

`reference/audits/astrodatabank_holistic_canonical_collector_blocked_2026_08_25.json`

Evaluable people: **1,655**

Skipped/unestimable because their collector/opportunity strata cannot support K=200: **2,711**

Mean true-chart percentile: **49.279%**

Median true-chart percentile: **50.0%**

Candidate-exchange empirical p-value: **0.83308**

This is plainly null/slightly below chance. Smaller collector corpora remain unevaluable rather than receiving a post-hoc lower K.

## What caused the earlier positive-looking results

The development sequence exposed several distinct false-positive routes:

1. **Missing label treated correctly at scoring but incorrectly in training background.** People with no evidence that an ontology branch was assessed could influence the label baseline.
2. **Opportunity-denominator fix without opportunity-neighborhood fix.** People who were never assessed for a construct could still occupy the K nearest-neighbor slots and crowd out genuinely observed cases.
3. **Loose cohort matching.** Decade-level matching allowed slow astronomical structure to proxy historical cohort differences in vocation/biography.
4. **Region-code confusion.** Astro-Databank fields such as `CA (US)` or `ENG (UK)` had to be normalized to actual nations before interpreting geographic controls.
5. **Heterogeneous archive sources.** Cross-collector training can encode collection/source structure even when target and decoy candidates themselves share a collector label.

The durable implementation now addresses these failure modes explicitly.

## Scientific conclusion

The corrected Astro-Databank result is:

> **No convincing holistic person↔chart identification signal was detected in this sparse archival formulation.**

This is a meaningful negative result. It falsifies the earlier positive interpretation for this model/data combination and demonstrates why full-pipeline opportunity and provenance controls are necessary.

It does **not** establish that the richer person-level phenomenon discussed in detailed questionnaire/case histories is absent. Astro-Databank is a poor measurement analogue for those cases: most people have sparse, selectively coded biographical categories rather than a systematic behavioral instrument with childhood continuity, contextual conditions, counterexamples, confidence, and dependency structure.

The next scientifically relevant holistic test should therefore use the repository's rich `HumanCase` schema on a multi-person cohort, not further retune Astro-Databank until it yields a positive result.

## Epistemic status

- Astro-Databank remains DEVELOPMENT data.
- The early positive-looking archive results are superseded by the canonical null endpoint.
- The holistic method itself remains a candidate methodology because the archive does not measure the rich target well.
- Any future rich-cohort model may be optimized on DEVELOPMENT people, then frozen and tested on independent VALIDATION people.
