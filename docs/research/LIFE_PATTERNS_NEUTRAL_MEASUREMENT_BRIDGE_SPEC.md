# Life Patterns Neutral Measurement Bridge — Design Specification

Status: **content-neutral framework implemented and CI-gated; theory-blind substantive development candidate now preserved; validation promotion remains blocked on blind human reliability evidence and core authority-gate integration**. This document defines the neutral observational layer required before any birth-derived model can be scored against the Life Patterns behavioral freeze.

Date: 2026-09-03

## Purpose

The behavioral freeze preserves what the participant reported and approved. A later model tournament needs a shared target representation that does not silently encode Human Design, AstroHD, astrology, or another candidate model. This bridge converts frozen participant evidence into explicit, versioned observational codes while preserving source provenance, missingness, context, counterevidence, participant revisions, and coder identity.

The bridge is not a personality diagnosis and is not a participant-facing interpretation layer. It exists so different model families can be evaluated against the same behavioral evidence rather than each receiving its own bespoke target representation.

## Independent conception preserved before existing-work scan

The independent conception is recorded in:

- `state/LIFE-PATTERNS-MEASUREMENT-BRIDGE-INDEPENDENT-CONCEPTION-2026-09-03.md`

The initial mechanism was:

1. freeze participant-reviewed episodes and exact source evidence;
2. define a theory-blind observable vocabulary with explicit code states;
3. code episodes before model outputs are available to the coder;
4. preserve contradictory/context-specific evidence instead of collapsing it into a single personality label;
5. aggregate descriptively and deterministically;
6. require reliability evidence before automation or confirmatory scoring;
7. keep later model adapters thin and declarative.

The subsequent scan changed implementation details but not that core chronology.

## Existing-work scan and reuse decision

### Reuse / adapt

The project composes established ideas rather than treating software structure as a substitute for measurement science:

- AERA / APA / NCME-style validity reasoning: validity is evidence supporting interpretations/uses, not a property conferred by software passing tests;
- Human Behaviour Ontology / Behaviour Change ontology ecosystem: reuse stable external behavior concepts where genuinely applicable rather than renaming ordinary constructs;
- OBO-style stable identifiers, provenance, versioning, explicit deprecation/supersession, and reuse before duplication;
- Cognitive Atlas / PhenX-style construct and measurement catalogs as discovery inputs rather than assumed direct mappings;
- directed/team qualitative content-analysis discipline: frozen codebooks, inclusion/exclusion criteria, examples/near misses, explicit adjudication, version-controlled changes;
- within-person / repeated-measures reasoning: preserve context and repeated episodes rather than force one timeless trait value;
- raw agreement plus chance-corrected agreement and full confusion patterns;
- selective classification / reject-option principles: abstention is a legitimate outcome;
- tool-neutral annotation exchange rather than making a vendor UI part of the scientific record.

### LLM annotation disposition

LLM annotation remains experiment-only, not the benchmark. Trained-human coding is the initial benchmark; any automated coder is version-pinned, compared against a frozen human-coded reference set, and cannot become scoreable merely because it is cheap or internally consistent.

## Theory-blind substantive-content policy

The earlier Life Patterns human-only H1 rule has been superseded for this project by the binding theory-blind policy:

- `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`

The separate Survey-v2 H1 specification is unchanged.

Under the current Life Patterns policy, substantive neutral content may be authored by a human or AI/model context provided target-theory information is absent from the relevant authorship context and provenance/contamination controls are preserved. Generic prior exposure to astrology or personality ideas is not treated as automatic disqualification.

Prompt-author steering is handled separately from generator/session blindness. A detailed prompt written by a theory-exposed source can produce a development candidate, but validation promotion requires an independent minimally seeded theory-blind replication plus reconciliation before human reliability work can support a final validation candidate.

## Preserved substantive development sequence

The branch now preserves, separately and without retroactive overwriting:

1. the first theory-blind development draft;
2. a theory-exposed leakage/codability audit;
3. the minimally seeded independent replication prompt;
4. the independent replication draft;
5. the replication crosswalk;
6. the exact theory-blind reconciliation prompt;
7. the exact reconciled candidate.

Current reconciled candidate:

- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

The reconciled candidate contains 22 primary episode-level observables and deliberately moves recurrence, context-linked variability, temporal change, state-linked comparison, and prior-experience linkage into derived summaries or metadata where they would otherwise double-count the same underlying evidence.

It is a **development candidate**, not a validation candidate.

## Blind human reliability pilot

The development pilot is specified in:

- `docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

The pilot requires:

- a frozen development-only corpus manifest;
- two or more independent theory-blind human coders;
- frozen coder-training receipts;
- segmentation before substantive coding;
- explicit prerequisite/applicability decisions;
- the four-part non-action gate: awareness, opportunity, feasibility, established non-action;
- sequence preservation;
- missingness/abstention;
- separate narrator-explicit influence vs temporal precedence;
- first-pass outputs frozen before coder discussion;
- reliability computed from pre-adjudication outputs;
- preserved original labels after adjudication;
- post-pilot substantive revision only in a theory-blind context.

The protocol does not authorize recruiting/contacting coders or spending.

## Theory-blind authority and pilot receipt contracts

Implemented in:

- `src/hdmatch/evaluation/theory_blind_authority.py`
- `src/hdmatch/evaluation/pilot_reliability.py`

The authority contract binds exact content, authoring-context provenance, prompt/output hashes for AI-influenced authorship, prompt seed level, replication/reconciliation where required, blind human-human reliability evidence, exact-content review, chronology, and immutable content addressing.

The pilot receipt contract binds corpus selection, independent coder outputs, first-pass freeze, and post-freeze adjudication without introducing target-model content.

These contracts do not manufacture reliability or construct validity. They record externally produced evidence and fail closed when required dependencies are absent.

## Artifact chronology

The intended confirmatory path is now:

1. participant interview and approved episodes;
2. participant-reviewed immutable behavioral freeze (`BPF-*`);
3. theory-blind substantive development with exact prompt/output provenance;
4. independent minimally seeded replication and reconciliation where required;
5. exact reconciled development candidate frozen;
6. blind human development/double-coding pilot;
7. reliability report and disagreement analysis bound to exact content/procedure/corpus;
8. theory-blind post-pilot revision/review;
9. validation-candidate ontology version frozen;
10. blind validation coding of behavioral freezes;
11. only coding artifacts passing the scoreability gate may feed later tournament execution;
12. target-model prediction/scoring occurs downstream under the separately frozen tournament contract.

The model tournament preregistration may pin the measurement-bridge/codebook contract before the final coded evidence exists. The eventual tournament execution layer must bind the actual scoreable coding artifact; the preregistration manifest itself must not be rewritten post hoc to include observed target results.

## Neutral ontology release

Implemented in `src/hdmatch/evaluation/neutral_measurement.py`.

Each release has:

- ontology ID/version/status;
- scope statement;
- explicit observable definitions and stable IDs;
- exact coding-procedure / aggregation-policy / contamination-policy identities and hashes;
- source commit and release timestamp;
- synthetic-fixture flag;
- content-authority binding;
- explicit statement that software validation does not establish construct validity.

The full payload is canonicalized and content-addressed as `LPO-*` with SHA-256. Immutable writes reuse repository-wide canonical artifact primitives.

### Remaining core integration mismatch

The generic theory-blind authority contract is implemented, but `neutral_measurement.py` still wires `frozen_for_validation` directly to the legacy `HumanContentAuthorityReceipt` field and H1 wording.

Until that core integration is generalized:

- legacy human-only content can still use the stricter old path;
- AI-authored theory-blind content must **not** be mislabeled as human-authored to bypass the old field;
- the current reconciled candidate remains development-only anyway because real blind human reliability evidence does not yet exist;
- this mismatch is engineering debt, not a scientific requirement.

## Stable IDs and semantic revision

An observable may retain an ID only when its core meaning remains stable. The semantic fingerprint includes at minimum:

- definition;
- unit of analysis;
- value type / allowed values or numeric bounds;
- insufficient semantics;
- not-applicable semantics.

Changing core meaning under the same stable ID is rejected. A genuine semantic revision gets a new ID and may declare a superseded prior ID.

## Coding state model

Episode coding distinguishes:

- `observed`;
- `contradicted`;
- `mixed`;
- `insufficient`;
- `not_applicable`.

The reconciled candidate further clarifies that a multi-step sequence within one episode is not itself `mixed`; sequence is retained explicitly, while `mixed` belongs to an aggregation scope with materially different values not resolved by a supported context split.

`insufficient` is not zero evidence, and `not_applicable` is not a negative observation. Neither may carry artificial classifier confidence.

## Frozen evidence binding

The bridge verifies the behavioral-freeze content address before coding and independently checks approved episode hashes, frozen source-turn hashes, unique source-turn identities, episode-to-source-turn provenance, input modality, and participant-revision provenance.

A coded record cannot cite a source turn outside its frozen episode. A forged outer freeze hash does not rescue stale inner episode/source-turn hashes.

## Coder identity and blindness

Every coding run identifies coder and version. Human coders require a training receipt. Automated coders require a pinned implementation hash. Coding runs affirm that birth data and chart/model outputs were unavailable.

An automated coder may not become tournament-scoreable without a separate human-benchmark automation-validation receipt.

## Annotation exchange

Implemented in `src/hdmatch/evaluation/annotation_exchange.py`.

The format is canonical JSONL and tool-neutral. Annotation tasks bind behavioral freeze, ontology, episode/source turns, eligible observable IDs, coding-guidelines hash, and chart/model blindness.

## Aggregation policy

The current generic aggregation is descriptive and distribution-preserving. It does not infer one timeless trait value.

The reconciled codebook makes the same conceptual distinction more explicit: person-level recurrence, repeated-condition behavior, context variability, and temporal change are derived summaries over primary episode codes rather than independent duplicate observations.

The current software aggregation label remains:

`descriptive_distribution_preserving_no_trait_collapse`

Any future transformation from these distributions to a model-specific prediction target belongs in a separately frozen scoring/model-adapter contract, not in the neutral measurement layer.

## Reliability report contract

The existing framework records exact ontology/coding-procedure/corpus hashes, comparison type, coder IDs, per-observable double-coded N, class distribution, raw agreement, optional Krippendorff-style alpha, optional Gwet-style agreement coefficient, abstention/adjudication rates, confusion matrices, and error categories.

The blind-pilot protocol additionally requires separate analysis of episode segmentation, prerequisites/applicability, non-action gate components, sequence coding, missingness, context modifiers, counterepisode identification, recurrence, context splits, derived summaries, and coder burden.

Reliability does not establish construct validity.

## Validation and scoreability readiness

A current substantive coding artifact cannot become tournament-scoreable merely because the reconciled codebook exists.

The intended validation gate requires at minimum:

- exact frozen substantive content;
- policy-compliant theory-blind provenance;
- replication/reconciliation where required;
- blind human reliability-development evidence;
- selected observables promoted to `validation_candidate` only after blind development review;
- ontology frozen for validation;
- nonempty validation coding run;
- human reliability baseline for every used observable;
- validation run type;
- human-benchmark automation receipt for automated coders;
- all freeze/ontology/coding integrity checks passing.

The current reconciled v1 candidate does **not** satisfy that gate because human double-coding/reliability work has not yet occurred.

## No validity inference

This branch may establish deterministic engineering/governance properties and preserve theory-blind development artifacts. It does not establish:

- construct validity;
- coding reliability;
- Human Design/AstroHD validity;
- participant benefit;
- birth-time recovery accuracy;
- empirical model discrimination.

Those require subsequent blind human reliability work, frozen validation coding, and separately authorized independent model testing.
