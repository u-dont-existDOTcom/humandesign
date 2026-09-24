# V4.3 scoring-architecture prior-work and novelty ledger — 2026-09-23

## Task

- Project: Human Design / Life Patterns owner recovery calibration
- Task/decision: choose the next scoring architecture after V4.3 pathway-rarity scoring separated candidates that were identical on the measured participant-observable evidence
- Branch: `chat/scenario-owner-recovery-calibration-20260923`

## Gate state

- Applicability: `required`
- Trigger: repeated refinement of a bespoke evidence score plus a direct result showing outcome separation driven entirely by hidden mechanism/pathway differences.
- Independent conception: `V43-SCORING-ARCHITECTURE-INDEPENDENT-CONCEPTION-20260923.md`, committed before outside methodological search.

## Search formulations

- Combining correlated diagnostic/classification features without double-counting.
- Multiple latent mechanisms producing the same observed behavior.
- Likelihood-ratio evidence versus marginal feature rarity/self-information.
- Conditional-dependence-aware alternatives to naive additive evidence.
- Internal baseline: observable-normalized Survey-v2 scorer and its full-universe noise/recoverability audits.
## Existing-work scan

### Academic literature

| Source | What it contributes | Fit / limit |
| --- | --- | --- |
| Friedman & Goldszmidt, *Building classifiers using Bayesian networks*, AAAI 1996 | Tree-augmented Naive Bayes explicitly captures dependencies among attributes rather than assuming independence. | Requires training/reference data; not a justification for hand-authored probabilities. |
| Friedman, Geiger & Goldszmidt, *Bayesian Network Classifiers*, Machine Learning 29 (1997), DOI 10.1023/A:1007465528199 | General dependency-aware classifier family; TAN is a tractable middle ground between naive independence and unrestricted networks. | Needs empirical class/feature distributions. |
| van Rijn & Rijmen, *On the explaining-away phenomenon in multivariate latent variable models*, Br J Math Stat Psychol 68 (2015), DOI 10.1111/bmsp.12046 | Multiple latent causes for one observation create conditional dependencies; mechanism alternatives should be modeled as latent structure, not separate observed evidence. | Conceptual/measurement-model guidance, not a ready-made scorer here. |
| Fenton & Neil, *Calculating the Likelihood Ratio for Multiple Pieces of Evidence*, 2021, arXiv:2106.05328 | Dependent pieces of evidence can be represented in a causal Bayesian network and used to derive coherent likelihood ratios. | Requires defensible conditional probability models. |
| Morrison & Stoel, *Forensic strength of evidence statements should preferably be likelihood ratios...*, Aust J Forensic Sci 46 (2014), DOI 10.1080/00450618.2013.833648 | Evidence strength should compare how probable the observed evidence is under competing hypotheses using relevant data/statistical models. | Forensic context; transferable evidential principle, not domain validation. |

### Mature internal implementation

The repository's Survey-v2 contract is the strongest directly reusable implementation baseline.
Survey-v2 already does several things V4.3 does not:

- normalizes candidate structure to the **participant observable** first: candidate value is 1 when any frozen predicate grouped under the observable matches;
- uses explicit positive / negative / mixed / insufficient / abstention outcomes rather than positive support plus sparse bespoke contradiction rules;
- gives each dependency cluster at most one unit of scoring weight and macro-averages members instead of summing hidden structural rarity;
- uses candidate-blind entropy selection for adaptive follow-up;
- has complete-century synthetic recoverability/noise audits over 288,938 exact structural states.

The Survey-v2 synthetic audits show the implementation can mechanically recover its own generated answer vectors and tolerate declared answer noise. This is **not empirical evidence that Human Design predicts human behavior**; it is evidence that the scoring/search architecture is internally recoverable and noise-aware.

## Existing-work map

### Already solved

- Observable-level normalization of alternative structural mechanisms: Survey-v2.
- Explicit abstention/mixed/negative measurement states: Survey-v2.
- Dependency-cluster normalization: Survey-v2.
- Candidate-blind adaptive information-gain questioning: Survey-v2.
- General methods for correlated evidence: Bayesian networks / TAN / latent-variable models.
- Evidence weighting principle: likelihood of observed evidence under competing hypotheses, not marginal rarity alone.
### Partially solved

- Translating the current scenario-v7 free-text neutral profile into observable categorical evidence while preserving conditions and uncertainty.
- Dependency structure among the Life Patterns observables.
- Empirical response likelihoods `P(answer | candidate-predicted observable)`; no independent human dataset currently estimates these.

### Composable

- Scenario-v7 neutral measurement and provenance.
- Survey-v2 observable normalization + dependency-cluster scoring + abstention semantics.
- Survey-v2 adaptive tie-breaking.
- Later empirical likelihood or Bayesian-network calibration once independent participant data exists.

### Genuinely unresolved

- Which behavioral observables, if any, are empirically associated with chart states in new independent participants.
- Calibrated human-response likelihoods and cross-observable dependencies.
- The minimal additional observable set needed to distinguish residual candidate ties without target leakage.

## Decision

- Disposition: **adapt + compose**
- Do not invent another hand-tuned rarity score.
- Do not patch V4.3 pathway weights to make the owner case rank better.
- Treat V4.3 as a historical descriptive scorer, not the primary architecture for scenario-v7 behavior-only recovery.
## Integration

- **Established:** participant-observable normalization, abstention, dependency control, adaptive entropy questioning, likelihood-based evidential principles.
- **Borrowed:** Survey-v2 candidate normalization and cluster-weighting semantics.
- **Modified:** scenario-v7 needs richer conditional/mixed evidence than Survey-v2's original fixed binary prompts.
- **Novel remainder:** a scenario-v7 → observable evidence adapter and, later, empirical response-likelihood calibration.
- **Uncertain / experiment-required:** whether observable-only recovery works on independent humans rather than synthetic answers.

## External baseline

- Strongest academic baseline: dependency-aware probabilistic classification / Bayesian networks with likelihood-based evidence.
- Strongest mature internal baseline: Survey-v2 observable-normalized dependency-cluster scorer.
- Simple baseline: confidence-weighted observable match with explicit abstention and no pathway rarity.
- Intended advantage: score only distinctions the participant measurement actually contains.

## Research refresh trigger

Refresh this ledger before fitting empirical likelihoods, learning dependency graphs, or making scientific claims from independent participant data. Do not repeat the literature scan for ordinary implementation of the selected observable-normalized baseline.
