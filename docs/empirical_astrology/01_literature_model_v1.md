# Literature Model v1b

## Status

This is the exact implementation of the frozen Wave 3B Pro decision. It is a
development research specification. It is not an empirically validated
astrology model, a Human Design validation, a production predictor, or an
authorization to recruit participants or collect outcomes.

The governing files are:

- `reference/empirical_astrology/literature_model_v1b_decision.json`
- `reference/empirical_astrology/literature_feature_registry_v1.json`
- `reference/empirical_astrology/literature_model_v1.json`

The loader hashes the raw bytes of the decision and feature registry, requires
the model to contain those hashes, and rejects version drift. It also verifies
that the repository descends from evidence checkpoint
`e7f82ab4a1b08705bf4429958a0d577b2758c407` when the Git ancestry gate is run.

## Executable surface

The model exposes one birth-derived feature:

| ID | Definition | Role |
|---|---|---|
| `TN-001` | Absolute recorded UTC birth-center gap in hours for an eligible pair born at the same hospital on the same local calendar date | Sole primary theory-neutral exposure |

The eligible range is `[0, 3]` hours. The feature is continuous and linear. The
implementation supplies no bins, splines, logarithms, searched thresholds,
zodiac variables, or participant-level interpretations.

The assembled model has:

- executable astrology features: `[]`;
- aspect-to-trait mappings: `[]`;
- executable aspect/orb/angularity interactions: `[]`;
- astrology weights: `{}`;
- astrology coefficient-vector length: `0`.

Full v1b and the theory-neutral model are therefore identical. CF-001 through
CF-008 cannot enter the personality model. The earlier unweighted geometry and
karaka calculators remain dormant research primitives and are not imported by
the assembled model.

## Pair eligibility and deterministic selection

`BirthRecord` validates the frozen category dictionaries and requires a
timezone-aware UTC-resolvable birth timestamp, a documented uncertainty
half-width no greater than one minute, and an uncertainty interval wholly inside
the recorded local date.

An unordered pair must:

- match on hospital, local birth date, sex-at-birth category, delivery-mode
  category, recruitment-source category, and record-precision category;
- belong to one independent healthcare/recruitment network;
- have no known common family, household, or close-relationship component;
- have a maximum possible UTC gap no greater than 180 minutes;
- differ by no more than five maternal-age years and one gestational week.

Participant, hospital, network, and pair priorities use the exact SHA-256/NUL
encoding frozen by Pro. Pair selection enumerates eligible edges, sorts by the
frozen pair hash, and greedily accepts disjoint pairs. It does not re-pair after
a date-support or exposure-support failure.

## Outcome

The frozen outcome uses the public-domain 50-item IPIP Big-Five factor-marker
sample. The scorer requires all items 1 through 50 exactly once, with integer
responses from 1 through 5. It applies the frozen positive/reverse keys to five
ten-item means in this order:

1. extraversion;
2. agreeableness;
3. conscientiousness;
4. emotional stability;
5. intellect/imagination.

For participants `i` and `j`, the primary distance is

\[
D_{ij} = \sqrt{\frac{1}{5}\sum_{k=1}^{5}
\left(\frac{s_{ik}-s_{jk}}{4}\right)^2}.
\]

It ranges from 0 to 1. Missing items are not prorated or imputed. The decision
requires the exact item wording, instructions, public source bytes, and
questionnaire package to be archived and hashed before any respondent use; this
implementation does not authorize that use.

## Fixed controls and inference

`build_pair_features` emits the fourteen nuisance columns in the exact frozen
order: eight circular local-clock terms, maternal-age mean/difference,
gestational-age mean/difference, and birthweight mean/difference. Hospital-date
fixed effects absorb site, date, season, and birth cohort within analyzed pairs.

The optional empirical-analysis module implements:

- equal-network weighted least squares;
- weighted within-hospital-date absorption;
- ordered, design-only rank filtering at relative tolerance `1e-10`;
- TN-001 appended last and rejected if zero or collinear;
- network-cluster CR1 covariance and Student-t intervals;
- lower/upper uncertainty-bound fits on the original pairs;
- all-network leave-one-out fits;
- restricted wild-cluster bootstrap-t with PCG64 and sorted network IDs;
- the twenty hash-defined random-feature diagnostics;
- Holm correction for the fixed 21-test diagnostic family.

Nonfinite fits, invalid cluster counts, `N <= k`, rank failure, duplicate pairs,
or repeated people raise `NotEstimable`. Failed bootstrap draws are not dropped
or redrawn.

## Prospective boundary

The complete prospective specification is preserved in the decision and model
JSON. Its launch status is `scientific_specification_frozen_not_launched`.
Structural validation of a freeze manifest does not grant launch authority.

Before a separately authorized launch, the frozen protocol requires two
untouched cohorts with disjoint people, families, hospitals, and networks; 20
networks, 100 disjoint pairs per network, and 4,000 people in each cohort; exact
support, completeness, power, null-calibration, blinding, and provenance gates;
and independent success in both cohorts. A positive result would establish only
the prespecified observational, theory-neutral association under that protocol.

## Development reporting

Human-data comparisons require an eligible, documented, non-owner development
dataset with the frozen outcome and covariates. Aggregate literature summaries,
Astro-Databank relationship/event cases, synthetic Human Design fixtures, and
owner-known cases are not substitutes.

When inputs are absent, reports use `NOT_EVALUATED`. A model rank/variation
failure after eligible data exist uses `NOT_ESTIMABLE`. Removing an astrology
family from this empty astrology surface uses
`NOT_APPLICABLE_NO_INCLUDED_FEATURE`. These states are never converted into a
zero effect or validation claim.
