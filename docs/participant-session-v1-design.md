# Participant Session v1

Status: implementation target for the first participant-facing AstroHD interview harness.

## Goals

Participant Session v1 separates confirmatory scientific evidence from post-hoc self-exploration while preserving both in one coherent experience.

The sequence is:

1. sealed birth intake
2. deterministic chart calculation and prediction freeze
3. blind holistic interview
4. confirmatory evidence lock
5. confirmatory ranking and prediction comparison
6. reveal
7. post-hoc clarification and self-exploration
8. exploratory final-profile ranking

The post-hoc score is intentionally retained because it is useful to the participant and to model development, but it must never overwrite or be merged into the confirmatory result.

## Required invariants

### Prediction freeze

Before any behavioral answer is accepted, the system must persist an immutable prediction freeze containing:

- normalized birth state
- chart output
- AstroHD prediction set
- code revision
- ephemeris/model provenance
- mapping version/hash
- question-bank version/hash
- ranking scope
- creation timestamp
- SHA-256 digest over canonical serialized freeze contents

No later answer may alter the frozen prediction object.

### Phase separation

Every answer and derived observation carries a phase:

- `confirmatory_blind`
- `posthoc_exploratory`

The confirmatory evidence set is append-only until it is locked. Once locked, it is immutable.

Post-hoc evidence may add nuance, exceptions, context, childhood/adult changes, examples, and counterexamples. It may produce a new final profile and a new ranking, but it does not change the confirmatory score.

### Two rankings

The participant-facing report may show both rankings:

1. **Confirmatory blind ranking**: calculated only from evidence collected before reveal/lock.
2. **Post-hoc exploratory final-profile ranking**: calculated from the participant's final refined profile, including post-reveal clarifications.

The second result must be labeled clearly as post-hoc/exploratory. It is useful for self-understanding and hypothesis generation but is not independent confirmatory evidence.

## Primary scientific target: the latent behavioral fingerprint

"Astrology predicts a person" contains several distinct hypotheses. Participant Session v1 must not collapse them into one score.

The primary natal test is deliberately narrow and clean:

> Does astronomical state at birth contain statistically recoverable information about persistent behavioral patterns that cannot be explained by chance?

Evidence is tagged by domain. Only `trait` and `behavior` observations may affect the primary natal rank. The following domains are retained but excluded from that score:

- `outcome`
- `timing`
- `environment`
- `conventional_covariate`

This prevents noisy external outcomes from either rescuing or damaging the cleaner natal-behavior hypothesis.

### Separate research layers

The system records enough structure for later experiments at distinct arrows:

1. **Natal chart -> latent behavioral fingerprint.** Can the frozen natal state predict persistent psychological and behavioral architecture?
2. **Traits -> characteristic behavior.** Where useful, distinguish a stated disposition from the repeated behavior it tends to produce.
3. **Behavior + environment -> outcomes.** Model careers, wealth, relationship outcomes and other life results using behavior together with opportunity structure and circumstances.
4. **Chart -> residual outcome increment.** After behavior and environment are known, does natal information add out-of-sample outcome prediction?
5. **Progressions/transits -> change or timing increment.** Do time-varying astrological states add predictive information about changes in the behavioral fingerprint or event timing?
6. **Chart -> residual increment after conventional covariates.** Compare ordinary predictors such as validated personality scales, cognitive measures where appropriate, childhood socioeconomic context, education, geography/country, age/cohort and other predeclared covariates against the same model with AstroHD features added.

These are different scientific claims and must be reported separately. Success in one layer does not establish another. In particular:

- natal behavioral prediction does not by itself establish fate/outcome prediction;
- outcome prediction does not establish a natal behavioral mechanism;
- a post-hoc exploratory rank cannot count as independent replication;
- timing claims require their own frozen prospective or held-out protocol.

For residual tests, compare a predeclared conventional baseline with the same model plus frozen AstroHD variables on held-out or prospective participants. Do not tune AstroHD features against the evaluation set.

## Interview behavior

The interviewer should begin with broad, natural prompts and dynamically choose follow-ups based on missing or ambiguous evidence. It should prioritize stable patterns and context over isolated event sampling.

For each important behavioral claim, the interviewer should seek, when useful:

- whether the pattern existed in childhood
- whether it changed in adulthood
- typical contexts where it appears
- contexts where it does not appear
- a concrete example
- a counterexample or meaningful exception
- confidence in the participant's own description
- an `other`/free-form path whenever supplied options are imperfect

Mixed or context-dependent answers should be represented as such rather than forced into one category. A later `other`/free-form clarification is allowed to neutralize an earlier forced-choice token for scoring while preserving both records in the append-only evidence history.

## Participant progress display

Before reveal, the system may expose non-contaminating progress indicators such as:

- profile evidence coverage
- dimensions with strong evidence
- dimensions still ambiguous
- robustness/stability of the inferred profile
- general discrimination of the current evidence set

It must not expose the true birth-state rank or any information that would reveal which candidate is the known true state before the confirmatory evidence is locked.

After lock/reveal, the participant may see:

- true birth-state rank/percentile from blind evidence
- prediction agreement by dimension
- supported / partial / contradicted / insufficient-evidence classifications
- robustness under evidence perturbation if available
- exploratory final-profile rank/percentile after post-hoc refinement
- a side-by-side explanation of which post-hoc clarifications changed the inferred profile or rank

## Scientific interpretation

The report must keep these separate:

- **AstroHD -> person**: how well the frozen true chart predicted independently elicited behavior.
- **Person -> birth state**: how highly the person's observed profile ranked the true birth state among candidates.
- **Post-hoc person -> birth state**: how highly the final refined profile ranks the true birth state after reveal and clarification. This is exploratory only.

The first two can be confirmatory when the intake/interview is genuinely blinded. The third is deliberately retained because it can reveal useful nuance and guide future hypotheses, but it must never be presented as independent validation.

## Blinding modes

### Scientific blind

The strongest mode collects DOB/time/place in a trusted external intake and gives the interviewer only an opaque session ID. The interviewer must not receive or infer the concealed birth tuple before confirmatory lock.

### Self-discovery

A participant may instead supply birth information directly in the conversational product. Predictions are still frozen before behavioral answers, which prevents retrospective rewriting, but because the interviewer may have seen the birth tuple this mode is labeled precommitted exploration rather than fully blinded evidence.

## API implementation target

The participant-safe API supports:

- create sealed session
- fetch public session status
- append participant evidence
- request/select next question
- lock confirmatory evidence
- compute/store confirmatory ranking without exposing it pre-reveal
- reveal confirmatory result
- append post-hoc clarification
- finalize exploratory profile
- compute exploratory final-profile ranking
- fetch final participant report

Session storage is append-only for evidence and immutable for freeze/lock/reveal/final artifacts, with explicit state transitions and provenance.

## Current v1 ranking scope

The production participant backend currently supports exact `known_birth_month` candidate-state ranking. `century_global` is represented in the schema but must fail closed until the completed century astronomy work is converted into a reusable, arbitrary-participant candidate-state cache and scoring path. A target-specific century audit must not be silently reused as if it were that production universe.
