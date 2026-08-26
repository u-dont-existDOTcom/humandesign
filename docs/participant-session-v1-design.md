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
- ephemeris manifest/version
- mapping version
- question-bank version
- scoring configuration
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

Mixed or context-dependent answers should be represented as such rather than forced into one category.

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

Post-hoc exploratory ranking is a third quantity and must not be presented as independent validation.

## API implementation target

The participant-safe API should support at minimum:

- create sealed session
- fetch public session status
- append participant answer
- request/select next question
- lock confirmatory evidence
- compute confirmatory ranking
- reveal confirmatory result
- append post-hoc clarification
- finalize exploratory profile
- compute exploratory final-profile ranking
- fetch final participant report

Session storage should be append-only for evidence and freeze records, with explicit state transitions and provenance.
