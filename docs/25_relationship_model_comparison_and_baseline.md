# 25 — Relationship Model Comparison + Science Baseline

Status: development architecture. The three current pairs are development cases, not untouched validation.

## Decision after first three-pair audit

The prior AstroHD three-partner comparison was stated before the owner supplied corrective lived-experience rankings. Those timestamped predictions can therefore be audited descriptively rather than rewritten after feedback.

Criterion:

`reference/development_cases/relationship_phenotype_three_pair_v1.json`

Pre-feedback prediction snapshot:

`reference/development_cases/prior_astrohd_three_pair_prediction_snapshot_v1.json`

Audit:

`reference/development_cases/prior_astrohd_three_pair_audit_v1.json`

Reusable scorer:

`scripts/relationship_pairwise_audit_v1.py`

Result across the 10 currently known directional pairwise comparisons:

- sexual chemistry/satisfaction: 0/1;
- romantic connection/passion: 0/1;
- communication/intellectual fit: 1/2;
- emotional ease/regulation: 2/3;
- engulfment pressure: 1/3;
- overall: 4/10 = 0.40.

This is descriptive small-N development evidence, not an inferential significance test. The 0.50 binary-ordering reference is included only to make clear that the observed performance is not promising.

## Interpretation

The failure is not well described as `astrology got compatibility slightly wrong`.

The model collapsed distinct relationship phenotypes into an overly broad compatibility/intensity narrative. In particular, it failed to discriminate:

- exceptional sexual satisfaction from generic attraction/intensity;
- romantic bond from dramatic synastry;
- intellectual communication from emotional/relationship symbolism;
- outward emotional ease from emotional transparency;
- engulfment/low autonomy from intimacy or binding symbolism.

Do not rescue these misses by re-labelling the same aspects after the outcomes are known.

## Existing-work scan: stronger non-symbolic baseline

### Large-scale machine-learning relationship-quality study

Joel, Eastwick et al. (2020), PNAS, pooled 43 longitudinal dyadic datasets from 29 laboratories.

DOI: `10.1073/pnas.1917036117`

The strongest relationship-specific predictors were:

1. perceived partner commitment;
2. appreciation;
3. sexual satisfaction;
4. perceived partner satisfaction;
5. conflict.

Relationship-specific self-report variables predicted substantially more relationship-quality variance than simple objective relationship descriptors. Actor-reported variables were substantially more predictive than partner-reported variables. Objective variables such as married/dating/cohabiting status generally mattered little, with relationship length a notable exception.

Decision: use a relationship-process/science baseline as the primary serious comparator to HD/Western/AstroHD rather than inventing another symbolic compatibility scalar.

### Perceived responsiveness / intimacy process

Perceived partner responsiveness is the experience that the partner understands, validates, and cares for the discloser. It is central to the interpersonal-process model of intimacy and subsequent relationship research.

Use it separately from `communication_intellectual_fit`: someone can be intellectually brilliant to talk to while emotionally unavailable, or emotionally caring while intellectually mismatched.

## Models to compare

### R-RPV — criterion phenotype

`docs/24_empirical_relationship_phenotype_model.md`

This is the observed target vector, not a predictor. It must never be scored as though it predicted itself.

### R-SCI — relationship-science process baseline

Use directly measured, relationship-specific variables. Do not collapse them before domain prediction.

Core variables:

- perceived partner commitment;
- appreciation;
- perceived partner satisfaction;
- perceived responsiveness;
- conflict frequency/intensity;
- repair quality;
- sexual satisfaction;
- sexual communication;
- desire match/discrepancy;
- autonomy support / felt autonomy;
- emotional disclosure/readability;
- communication continuity;
- relationship length/exposure.

Domain mappings must be frozen prospectively:

- `sexual_chemistry_satisfaction`: early sexual satisfaction, desire match, sexual responsiveness/communication, sexual autonomy;
- `romantic_connection_passion`: appreciation, passion/longing, perceived commitment, self-expansion, romantic contact desire;
- `communication_intellectual_fit`: felt mental understanding, conversational depth, productive disagreement, communication continuity;
- `emotional_accessibility_transparency`: disclosure, readability, response continuity, perceived responsiveness;
- `emotional_ease_regulation`: conflict arousal, recovery, volatility, emotional safety/ease;
- `engulfment_pressure`: felt autonomy, pressure to merge/reassure/sacrifice, pursuit-withdraw intensity, space without punishment;
- `trust_safety`: reliability, honesty, trust, felt interpersonal safety;
- `practical_life_fit`: observed goal/geography/routine/resource/relationship-structure compatibility.

A variable cannot predict the identical outcome measured at the same instant. For longitudinal prediction, freeze Time-0 process measures and predict Time-1/Time-2 outcomes.

### R-BASIC — low-information non-symbolic baseline

Use only variables that are genuinely available before the outcome being predicted:

- age/life-stage gap;
- relationship length at prediction freeze;
- geographic distance;
- current cohabitation/shared-life exposure;
- relationship structure/exclusivity;
- independently stated future goals;
- language/communication constraints;
- major practical incompatibilities known before outcome.

Leakage rule: when a variable is effectively the target itself (for example communication frequency used to `predict` current communication continuity), exclude it for that target. The baseline is intended to detect whether a sophisticated model beats obvious real-world information.

### R-HD

Canonical HD relationship mechanics only:

- combined Center configuration;
- composite Definition/splits;
- Electromagnetic/Dominance/Compromise/Companionship;
- shared Gates;
- sourced higher-level geometry where available.

There is currently no frozen mapping from these mechanics to the RPV domains. The current three pairs therefore cannot provide an honest HD-only accuracy score. Any mapping created after observing these outcomes is development-only and must be tested on later pairs.

### R-WA

Western synastry only:

- frozen planetary positions;
- frozen aspect family/orbs;
- angles/houses where birth data permit;
- no Human Design features.

As with R-HD, domain mappings were not frozen before the current outcome reveal. Build candidate mappings only as development hypotheses and test them prospectively or on different held-out pairs.

### R-AstroHD

Joint HD + Western layer. The prior conversational version is the only current model with genuinely pre-feedback cross-pair domain predictions, and it scored 0.40 pairwise accuracy on the known comparisons. Do not fit a new version to these three and report its fit to them as evidence.

## Current three-pair development findings

The observed criterion currently contains these strong rankings:

- Pair 1 > Pair 2 for sexual chemistry/satisfaction;
- Pair 1 > Pair 2 for romantic connection/passion;
- Pair 2 > Pair 1 and Pair 2 > Pair 3 for communication/intellectual fit;
- Pair 3 > Pair 2 > Pair 1 for outward emotional ease/regulation;
- Pair 1 > Pair 2 > Pair 3 for engulfment pressure, with lower confidence for Pair 3 because the relationship is early.

Pair 3 also demonstrates why `introvert/extrovert` needs decomposition: strong introversion/social withdrawal and low readability coexist with relatively easy outward emotional expression when engaged.

## Next test architecture

### Development stage

Use these three cases only to:

- refine domain definitions;
- expose failure modes;
- define candidate R-HD/R-WA/R-AstroHD mappings;
- define R-SCI and R-BASIC instruments;
- decide what must be measured prospectively.

Do not optimize a final scoring formula to reproduce the three-case ordering.

### Prospective stage

For an ongoing early relationship or a new untouched pair:

1. freeze birth-derived R-HD/R-WA/R-AstroHD predictions before additional relationship outcome evidence;
2. collect R-BASIC variables at the same freeze;
3. collect Time-0 R-SCI process variables without using future outcomes;
4. freeze/hash the prediction package;
5. collect R-RPV outcomes at prespecified later windows;
6. compare domain-level prediction errors and pairwise/rank discrimination;
7. retain misses and unknowns.

Preferred early follow-up windows for development are roughly 30 and 90 days because they are long enough for communication, autonomy, conflict, and intimacy processes to reveal themselves while still preserving a genuinely prospective baseline. Longer-term commitment/practical-life outcomes require later windows.

## Model-selection rule

Prefer the simplest model that improves held-out domain prediction.

- If R-SCI >> all symbolic models, use relationship science for practical prediction and retain HD/AstroHD only as exploratory phenomenology.
- If R-HD or R-WA adds incremental held-out information over R-SCI/R-BASIC, retain the incremental layer.
- If merged R-AstroHD does not beat the strongest separate symbolic model and the non-symbolic baseline, drop the merge.
- Never award a model credit merely because a failed prediction can be narratively reinterpreted after the fact.
