# Life Patterns participant-adjudicated neutral substrate v1 — CANDIDATE — 2026-09-12

Status: **candidate only; not production, not validation-approved, not authorized for human collection.**

Branch: `codex/discover-life-patterns-mvp`

Companion contract:

`state/LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-CONTRACT-v1-CANDIDATE-2026-09-12.json`

This artifact was authored in the fresh target-theory-blind semantic-repair context required by:

`tasks/LIFE-PATTERNS-FRESH-THEORY-BLIND-SEMANTIC-REPAIR-LAUNCH-2026-09-12.md`

It does not authorize production implementation. A different fresh target-theory-blind reviewer must review this candidate before any implementation proceeds.

## 1. Decision

The minimum shared frozen substrate actually required by the Life Patterns research design is **not** a comprehensive externally coded behavioral ontology.

The required substrate is:

1. **bounded episodes**;
2. **minimal source-grounded episode facts in an open world**;
3. **candidate person-level pattern propositions linked to those facts**;
4. **recursive participant adjudication of whether each proposed pattern characterizes the participant and under what scope/conditions**;
5. **exact provenance, append-only history, and deterministic immutable freeze**;
6. **one adapter-facing frozen projection that prevents downstream rereading of raw narrative**.

A compact vocabulary may exist for retrieval or question generation, but it is optional metadata. It is not the semantic authority and a fact must remain fully representable when no vocabulary term fits it.

This chooses the worker's second substrate option — **minimally structured episode facts + participant-adjudicated person-level patterns** — while retaining the third option only as a non-authoritative indexing aid.

## 2. Method-necessity / manufactured-prerequisite check

### Real prerequisites

The downstream comparison problem genuinely requires all competing downstream adapters to consume the same pre-result, target-theory-blind representation. It also genuinely requires that representation to be immutable/content-addressed and that downstream code cannot call back into raw narrative when a convenient distinction is missing.

The episode layer must therefore retain enough literal information to support audit, participant questions, counterexamples, and later neutral reuse without relying on a target-specific reread.

### Manufactured prerequisites rejected

None of the following follows from the real requirement above:

- every behavior must map into a fixed behavioral-domain taxonomy;
- every episode must select from a closed set of categorical values;
- every possible value must be preclassified as action/non-action;
- person-level recurrence must be derived from external episode counts;
- every ordinary episode must be represented through a graph of facets, event stages, windows, evidence units, value assertions, component assertions, and relation edges;
- an `Other Specified` code must be the only escape hatch for novel positive behavior.

Those mechanisms can be useful in narrower contexts, but making them universal prerequisites recreates the architecture error identified in the root-cause audit.

## 3. Alternative substrate comparison

| Candidate | Strength | Failure mode | Disposition |
|---|---|---|---|
| Participant-adjudicated pattern claims + episode provenance only | Very small and participant-centered | Too lossy for source audit, question generation, correction, and later neutral reuse; forces rereading of raw narrative when the pattern wording omits a needed factual distinction | Reject as core substrate |
| Minimal episode facts + participant-adjudicated patterns | Preserves literal evidence while keeping person-level recurrence with the participant; supports audit and a no-reread boundary without a closed ontology | Requires careful separation of fact, appraisal, absence, proposal, and adjudication | **Adopt for candidate v1** |
| Compact extensible episode-fact vocabulary only | Useful for retrieval and question generation | Vocabulary can silently become a lossy ontology if it controls whether a fact is preserved | Retain only as optional, separately versioned index metadata |
| Fixed comprehensive categorical codebook | High mechanical standardization | Makes taxonomy fit a prerequisite for preserving ordinary facts; encourages external-coder person-level truth and recurrent schema expansion | Supersede as presumed primary architecture |

## 4. Epistemic layers

The candidate deliberately uses a small number of **epistemic/record roles**, not behavioral trait categories.

### 4.1 Source provenance

Every substantive episode fact points to one or more exact source records through stable identifiers, locators, and content hashes. The raw source archive is separately bound by hash.

The research freeze can prove where a fact came from without making raw transcript text available to downstream adapters.

### 4.2 Episode

An episode is a bounded reported occurrence. It provides the factual ground from which candidate patterns may be proposed.

An episode has:

- a neutral summary;
- exact source provenance;
- atomic fact references;
- optional uncertainty notes.

It does **not** require membership in a fixed observable/domain taxonomy.

### 4.3 Episode fact

An episode fact is an atomic source-grounded proposition. The only required classification is its epistemic assertion type:

- positive occurrence;
- reported appraisal or belief;
- reported outcome or resolution;
- context;
- explicit temporal relation;
- admitted absence.

These types answer questions such as "what sort of claim is this and what evidence rule applies?" They do not claim to enumerate the behavioral content of human life.

Positive facts remain plain natural-language propositions with exact provenance. If no current vocabulary term describes the behavior, the fact is still complete and admissible.

Reported appraisal stays reported appraisal. A participant saying a course felt too difficult is a supported report that they described it that way; it is not silently promoted into an objective hidden-cause claim.

Temporal/sequence claims require source support. Sequence is not inferred merely because two facts occur in the same episode.

### 4.4 Absence assessment

A genuine claim that something did **not** occur is represented separately from positive facts.

An absence assessment records:

- the actor;
- the exact absent proposition;
- the relevant window/opportunity;
- awareness;
- opportunity;
- reasonable feasibility;
- established nonoccurrence;
- exact source provenance.

An absence becomes an admissible `admitted_absence` episode fact **only when all four gates are established**.

If any gate is `not_established` or `unclear`, the assessment remains an audit record but does not instantiate a negative fact.

Critically, gate failure has no authority over independent positive facts. A failed stronger absence claim cannot erase, weaken, recode, or demote a supported positive occurrence, outcome, appraisal, or sequence claim.

Silence and missing evidence are not nonoccurrence.

## 5. Open-world behavior capture

The historical universal `OS — Other Specified` mechanism solved a real problem inside a closed codebook: preserving supported behavior that did not fit named values.

In this candidate, the core fact layer is already open text. Therefore `OS` is no longer required as the semantic escape hatch.

A positive fact that does not fit any current index term is simply preserved as a positive fact.

Optional indexing may still produce a vocabulary-gap record. That is useful feedback for blind refinement, but it does not alter the fact's admissibility or wording.

An index layer, if used, must satisfy all of these conditions:

- separately versioned and target-theory-blind;
- removable without semantic loss;
- never required to preserve a fact;
- never permitted to replace the fact proposition;
- never treated as evidence that unindexed behavior did not occur.

## 6. Participant-adjudicated pattern loop

The person-level semantic loop is normative:

`episode -> minimal facts -> candidate pattern question -> participant adjudication -> nuance/examples/counterexamples -> revised question when needed -> participant adjudication -> accepted/rejected/unresolved pattern`

### 6.1 Candidate pattern proposal

A candidate pattern is a hypothesis, not a fact. It must be linked to at least one preproposal episode-fact anchor.

The proposal record preserves:

- exact proposition;
- question text shown to the participant;
- evidence links;
- stable pattern-thread ID;
- revision index;
- previous proposal link when revised.

### 6.2 Participant adjudication

The participant decides whether the proposed person-level pattern characterizes them.

Allowed decisions:

- `accept`;
- `revise`;
- `reject`;
- `unresolved`.

Adjudication history is append-only.

`accept` records participant-approved wording. `revise` records the participant's corrected wording/scope and requires a new proposal in the same thread before that thread can resolve accepted. Rejection and unresolved status remain available for audit but do not become admissible person-level patterns.

There is no episode-count threshold that can override participant adjudication.

### 6.3 Nuance, examples, counterexamples, and retrieval discrepancy

Evidence links explicitly distinguish when an example existed **before** the pattern proposal versus when it was elicited **after** the proposal.

Postproposal examples are primarily scope/boundary information. They must not be silently counted as an unbiased recurrence-frequency sample.

A participant may genuinely recognize a recurring pattern yet fail to retrieve another example on demand. That discrepancy can be recorded and probed; lack of a new example does not automatically invalidate an otherwise accepted pattern.

Conversely, multiple episodes that look similar to an external coder do not authorize an accepted person-level pattern after the participant rejects that generalization.

Counterexamples and exceptions attached to an accepted pattern are first-class scope information, not noise to be discarded.

## 7. Resolved pattern semantics

A resolved person-level pattern is derived from one append-only pattern thread.

An **accepted** pattern requires:

- at least one preproposal factual anchor;
- a participant `accept` adjudication on the terminal proposal;
- participant-approved wording.

The resolved view carries scope and exception information forward.

Rejected and unresolved threads remain in the research audit so the process is reconstructible, but they are not admissible person-level patterns in the downstream projection.

There is no automatic recurrence score in the semantic core.

## 8. External calibration boundary

External human/AI calibration remains useful, but its target changes.

### Appropriate external calibration targets

- whether each episode fact is faithful to its cited source;
- whether provenance points to the right source segment;
- whether positive occurrence, reported appraisal, outcome/resolution, context, sequence, and absence are kept epistemically distinct;
- whether an explicit temporal relation is actually supported;
- whether every admitted absence satisfies the four-part gate;
- whether failed absence gates leave positive facts intact;
- whether candidate pattern questions are non-leading and grounded in their anchors;
- whether participant corrections and scope limits are preserved exactly enough;
- whether freezes are deterministic and downstream adapters are unable to reread raw narrative.

### Inappropriate external calibration targets

- majority external-coder vote as the ground truth for whether a person-level pattern characterizes the participant;
- a recurrence threshold that converts episode counts into person-level truth over participant rejection.

An external reviewer may evaluate whether an accepted pattern is traceably grounded and whether the participant process was faithfully recorded. That reviewer does not replace the participant as the authority on the participant-level recurrence judgment.

## 9. Downstream adapter boundary and anti-rereading mechanism

The full research freeze keeps the audit chain. The **admissible downstream projection** is narrower.

It includes:

- admissible episode facts;
- accepted participant-adjudicated patterns;
- scope and exceptions attached to accepted patterns;
- preproposal anchors and explicit counterexamples linked to those accepted patterns;
- provenance identifiers/locators/content hashes;
- exact contract and freeze hashes.

It excludes:

- raw transcript/raw narrative text;
- any source resolver;
- not-admitted absence assessments as negative evidence;
- rejected/unresolved proposals as substantive person-level patterns;
- any target-specific or post-result reinterpretation fields.

Mechanical anti-rereading rule:

> A downstream adapter receives only the frozen adapter projection. If a distinction needed by that adapter is not represented there, the result is `unmeasured/not_represented`. The adapter may not fetch or reinterpret the source narrative to manufacture that distinction.

Every downstream output must bind the exact `freeze_payload_sha256`. All downstream adapters in the same comparison must bind the same freeze.

A later semantic correction requires a new target-theory-blind substrate revision and a new freeze. Historical freezes remain immutable.

This is the mechanism that satisfies the real cross-model fairness prerequisite without requiring one exhaustive behavioral ontology.

## 10. Disposition of historical mechanics

### Retain as normative invariants

- target-theory-blind substantive authoring/review;
- bounded episode grounding;
- exact provenance;
- deterministic/content-addressed artifacts;
- immutable freeze and append-only audit history;
- missingness distinct from negative evidence;
- reported appraisal distinct from objective fact;
- explicit sequence only when source-supported;
- strict awareness/opportunity/reasonable-feasibility/nonoccurrence gates for genuine absence claims;
- failed absence gates cannot damage positive facts;
- downstream no-reread boundary.

### Adapt

- participant claim review -> recursive participant pattern adjudication;
- historical `OS` gap handling -> open-world facts plus optional non-authoritative vocabulary-gap reporting;
- recurrence firewall -> explicit preproposal/postproposal evidence roles plus participant authority;
- external-coder reliability -> episode-fact fidelity/procedural calibration;
- stage/evidence ownership -> simple fact/evidence links, with additional stage structure only where an actual semantic need is demonstrated.

### Supersede as presumed universal core

- fixed 22-observable coverage requirement;
- exhaustive categorical subcode membership;
- automatic person-level recurrence from episode counts;
- complete non-action classification of every categorical value;
- universal facet/event-stage/evidence-unit graph representation;
- a closed-code `OS` mechanism as the only route for novel positive facts.

Historical V1/V2/V5 artifacts remain immutable development history. This candidate does not rewrite them.

## 11. Focused semantic/mechanical test requirements

Production implementation is **not** authorized by this candidate, but a later implementation must have focused tests proving at least the following:

1. an uncategorized positive fact survives capture, freeze, and adapter projection without an `OS` code;
2. changing/removing an optional index term cannot alter the underlying fact proposition;
3. any non-established absence gate prevents creation of an admissible absence fact;
4. a failed/unclear absence assessment leaves independently supported positive facts unchanged;
5. silence cannot satisfy established nonoccurrence;
6. reported appraisal remains separate from event/outcome assertion;
7. unsupported sequence cannot be emitted as a temporal-relation fact;
8. one factual preproposal anchor plus participant acceptance can resolve a pattern without a minimum episode count;
9. multiple similar episodes cannot resolve a pattern accepted after participant rejection;
10. participant acceptance is not invalidated solely because no new postproposal example is recalled;
11. postproposal examples are role-marked and cannot feed automatic recurrence counting;
12. a `revise` decision preserves the prior proposal and creates a monotonic revision chain;
13. rejected/unresolved threads remain auditable but are omitted from the admissible downstream pattern projection;
14. the adapter projection contains no raw source narrative and exposes no source resolver;
15. an adapter cannot recover an unrepresented distinction by calling back to source narrative;
16. all downstream adapters in one comparison bind the identical freeze hash;
17. canonical serialization is deterministic and semantic mutation changes the freeze hash;
18. neutral-substrate validation rejects target-specific/result-derived fields;
19. no completion denominator or automatic coverage claim is manufactured.

The machine-readable candidate contract carries the same requirements in `focused_semantic_test_requirements`.

## 12. Candidate acceptance gate

This artifact does **not** pass itself.

Before production implementation, a different fresh target-theory-blind context must review this candidate and its companion contract using the candidate-specific review prompt produced with them.

That review must explicitly check:

- whether the proposed substrate is actually sufficient to prevent downstream narrative reinterpretation;
- whether the schema has accidentally recreated a hidden closed ontology;
- whether participant authority is correctly limited to person-level pattern adjudication rather than source-fact fabrication;
- whether absence, missingness, positive facts, appraisal, and temporal claims are kept distinct;
- whether open-world facts are genuinely lossless;
- whether postproposal examples can accidentally become recurrence counts;
- whether the adapter projection is mechanically capable of enforcing the no-reread boundary;
- whether any field is a manufactured prerequisite without a demonstrated downstream purpose.

Until that separate review passes, status remains **candidate-only / implementation-blocked / human-collection-blocked**.
