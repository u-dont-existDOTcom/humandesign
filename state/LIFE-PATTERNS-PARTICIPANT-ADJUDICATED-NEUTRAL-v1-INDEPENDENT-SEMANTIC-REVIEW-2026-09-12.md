# Life Patterns participant-adjudicated neutral substrate v1 — independent semantic review — 2026-09-12

candidate_reviewed: LIFE-PATTERNS-PARTICIPANT-ADJUDICATED-NEUTRAL-v1-CANDIDATE-2026-09-12
verdict: BLOCKED
semantic_change_required: true
safe_for_implementation: false
blocking_findings: 6

Status: public-safe independent fresh target-theory-blind semantic disposition. This review does not authorize production implementation, human collection, automated participant coding, target-model mapping/scoring/reveal, merge/deploy, recruitment/contact, or spending.

## Review identity and independence

Review boundary:

- candidate-producing head: `d5f95598c2f48b0a6a4ddfedd35b6e6e9e58d7eb`;
- reviewed architecture blob: `427e115593d2ddff2469b4eecc38d3abeacd9d90`;
- reviewed contract blob: `e5adaca6b560bc360e7a9036c81e061bf17c3548`;
- live PR head at pre-write check: `b7bf7826fc62d5061fdc1f2a1da131e039f607fe`.

The architecture and contract blobs at the live PR head were verified identical to the blobs at the candidate-producing head.

This review used only the candidate-specific permitted authority chain and candidate artifacts. It did not inspect target-model mappings/scoring, fit/results, birth/chart outputs, prior predictions, or the candidate producer's private reasoning.

## Overall judgment

The candidate **does fix the main upstream architecture error**: it no longer makes a comprehensive fixed behavioral ontology the prerequisite for preserving ordinary behavior, and it correctly restores participant adjudication as the authority for person-level recurrence/typicality. The open-world episode-fact direction, strict genuine-absence gate, attributed appraisal semantics, immutable freeze, and no-raw-source adapter boundary are all directionally sound.

It is nevertheless **not yet semantically safe for implementation**. Six contract gaps leave important invariants unenforceable or ambiguously representable. These are narrower than the rejected fixed-codebook architecture and do not justify returning to a closed ontology.

## Criterion disposition

- **A. Substrate necessity/sufficiency — BLOCKED.** The substrate is structurally minimal enough, but fact uncertainty/corrections and downstream person-level authority are not yet preserved strongly enough.
- **B. Episode-fact semantics — BLOCKED.** Positive/appraisal/sequence/open-world behavior is sound, but negative-claim routing, correction semantics, and fact-level uncertainty are underspecified.
- **C. Absence semantics — BLOCKED.** The four gates are correct once an `absence_assessment` is used, but the contract does not forbid encoding a genuine real-world nonoccurrence under another free-text assertion type.
- **D. Open-world behavior — PASS.** Optional indexing is genuinely non-authoritative and removable without semantic loss.
- **E. Participant pattern authority — BLOCKED.** Acceptance/rejection/count rules are directionally correct, but revision grounding and downstream re-aggregation can escape the intended participant-authority boundary.
- **F. Elicited-example bias — BLOCKED.** Evidence roles exist, but their proposal-relative semantics can relabel postproposal evidence as preproposal after a revision.
- **G. Downstream anti-rereading boundary — BLOCKED.** Raw-source rereading is prohibited, but uncertainty and participant-rejection semantics are not mechanically preserved strongly enough in the projection contract.
- **H. Complexity / manufactured prerequisites — PASS.** The required object set is substantially smaller and each core object has a legitimate provenance, epistemic, adjudication, audit, or freeze role. No hidden replacement behavioral ontology was found.

## Blocking findings

### LP-PAN-v1-REV-001 — genuine absence can bypass the four-gate route

**Exact candidate location**

- architecture §4.3 `Episode fact` and §4.4 `Absence assessment`;
- contract `objects.episode_fact.rules` plus `objects.absence_assessment`.

**Literal failure mode**

The contract requires `absence_assessment_id` when `assertion_type == admitted_absence`, but it does not state the converse semantic rule: a proposition whose truth condition is a genuine real-world nonoccurrence must use the absence route and may not be encoded as `positive_occurrence`, `context`, `reported_outcome_or_resolution`, or another free-text assertion type.

Because fact propositions are open text, an implementation can satisfy the literal contract while placing a negated/nonoccurrence proposition in a non-absence assertion type, thereby avoiding awareness, opportunity, reasonable-feasibility, and established-nonoccurrence gates.

Attributed beliefs/appraisals containing negation are not the problem; e.g. a participant reporting that they *believed* something would not happen remains a reported belief. The defect concerns claims that assert the nonoccurrence itself.

**Why this violates permitted authority**

The participant co-coding architecture and the candidate architecture both require genuine absence/nonoccurrence claims to receive the strict gate, while ordinary positive facts and attributed appraisals do not. The current machine-readable contract makes the gate conditional on a label that can itself be chosen incorrectly, instead of making the semantic content control the route.

**Smallest repair needed**

Add a normative exclusivity rule: any episode-fact proposition asserting genuine real-world absence/nonoccurrence must be backed by an admitted four-gate absence assessment; other assertion types may not be used to encode that negative claim. Preserve the exception for explicitly attributed belief/appraisal about absence.

### LP-PAN-v1-REV-002 — evidence timing can reset across proposal revisions

**Exact candidate location**

- architecture §6.3 `Nuance, examples, counterexamples, and retrieval discrepancy`;
- contract `structural_enums.pattern_evidence_role` and `objects.pattern_evidence_link`.

**Literal failure mode**

Evidence roles are attached to a specific `proposal_id`. In a recursive thread, an example elicited after proposal P0 but before revised proposal P1 can be relabeled `preproposal_anchor` for P1, because it is literally pre-P1 even though it was elicited only after the participant had already been exposed to the pattern hypothesis.

That permits postproposal selected evidence to acquire the privileged semantics of a preproposal anchor after revision.

**Why this violates permitted authority**

The participant co-coding authority says examples requested after a candidate pattern has been proposed are selected scope/boundary evidence, not an unbiased recurrence sample. The candidate review contract specifically requires preproposal/postproposal bias to remain explicit. Proposal-relative roles are insufficient across recursive revisions.

**Smallest repair needed**

Make evidence acquisition role immutable relative to the first pattern-thread proposal, or otherwise store an immutable `first_available_before_pattern_proposal`/acquisition-phase fact that revisions cannot reset. Revised proposals may use later examples for scope, contradiction, or wording refinement, but may not relabel them as original preproposal evidence.

### LP-PAN-v1-REV-003 — revised/terminal proposals need not remain grounded in a factual anchor

**Exact candidate location**

- architecture §6.1 `Candidate pattern proposal`, which states that a candidate pattern must be linked to at least one preproposal episode-fact anchor;
- contract `objects.pattern_proposal.rules`, which requires a preproposal anchor only for **a first proposal**;
- contract `objects.resolved_pattern.rules`.

**Literal failure mode**

After a `revise` adjudication, a later proposal can legally contain no preproposal anchor that actually grounds the revised proposition. The resolved pattern needs at least one preproposal anchor somewhere in the chain, but the contract does not require that the terminal accepted proposition remain substantively linked to a factual anchor supporting that formulation.

A revision can therefore drift away from the episode evidence while still satisfying the literal structural contract.

**Why this violates permitted authority**

The replacement architecture is explicitly `episode -> minimal factual decomposition -> candidate recurring-pattern question -> participant adjudication -> revision -> participant adjudication`. Participant authority determines whether a person-level pattern characterizes them, but it does not convert an ungrounded system proposition into episode-grounded evidence. The candidate architecture itself says every candidate pattern is a hypothesis linked to at least one preproposal episode-fact anchor.

**Smallest repair needed**

Require every proposal revision that can become terminal/accepted to retain at least one valid factual anchor supporting the current proposition, with the original acquisition role preserved. A participant revision may alter wording/scope, but the accepted resolved pattern must remain traceably grounded rather than merely inherit an unrelated anchor from an earlier proposal.

### LP-PAN-v1-REV-004 — participant correction of episode facts has no deterministic provenance/supersession semantics

**Exact candidate location**

- contract `authority_split.episode_fact_authority`;
- contract `objects.episode_fact.optional_fields.participant_correction_note`;
- architecture §4.3 plus the stated requirement for exact provenance/append-only history.

**Literal failure mode**

A participant can correct an extracted episode fact, but the contract provides only an optional free-text `participant_correction_note`. It does not require correction-source provenance, say whether the original proposition remains admissible, define whether a corrected fact supersedes the original, or prevent in-place mutation of the proposition.

A source-faithful but wrong extraction can therefore remain as an ordinary admissible fact alongside an ambiguous note, or be silently rewritten without an auditable correction chain.

**Why this violates permitted authority**

The permitted architecture requires participant corrections to remain representable, exact provenance to be retained, original records not to be silently overwritten, and source facts not to be fabricated merely by participant pattern authority. A note without source binding and supersession semantics does not determine which literal episode fact downstream adapters may consume.

**Smallest repair needed**

Define append-only episode-fact correction/supersession semantics using existing provenance primitives: preserve the original fact, bind the correction to exact participant-response provenance, identify which fact it corrects/supersedes, and deterministically expose only the current admissible corrected fact in the downstream projection while retaining the historical fact for audit. This need not introduce a behavioral ontology.

### LP-PAN-v1-REV-005 — uncertainty is not preserved at the fact/projection level

**Exact candidate location**

- architecture §4.2 `Episode` allows only episode-level optional `uncertainty notes`;
- contract `objects.episode.optional_fields.uncertainty_notes`;
- contract `objects.episode_fact`, which has no fact-level uncertainty/evidential qualification;
- `admissible_downstream_projection`, which includes episode facts but does not include episode-level uncertainty notes.

**Literal failure mode**

Two facts in one episode can differ in certainty, but the contract has no fact-level uncertainty semantics. The downstream projection can therefore carry a proposition as an ordinary admissible episode fact while dropping the uncertainty note that qualified it in the full episode object.

The contract also has no normative fallback requiring uncertainty to be encoded losslessly into the fact proposition itself.

**Why this violates permitted authority**

The root-cause audit explicitly retains uncertainty as a first-class corrective invariant, and the participant co-coding architecture requires uncertainty to be preserved rather than forced into labels. The review launch also requires uncertainty to remain representable. A downstream adapter must not receive an apparently unqualified fact when the frozen neutral record knew that fact was uncertain.

**Smallest repair needed**

Carry uncertainty/evidential qualification at the episode-fact level, or impose an equally explicit lossless rule that binds uncertainty to each affected fact and carries it into the admissible projection. Do not add a behavioral category taxonomy; this is epistemic metadata only.

### LP-PAN-v1-REV-006 — downstream adapters can still reconstruct person-level recurrence from episode facts after participant rejection

**Exact candidate location**

- contract `admissible_downstream_projection.includes` and `.excludes`;
- contract `normative_invariants` on participant recurrence/rejection;
- architecture §9 `Downstream adapter boundary and anti-rereading mechanism`.

**Literal failure mode**

The projection exposes all admissible episode facts but omits rejected/unresolved pattern threads. The contract forbids raw-source rereading, yet it does not explicitly forbid a downstream adapter from aggregating several episode facts into a new person-level recurrence/typicality claim.

Because the adapter does not receive the participant's rejected thread, it can be structurally unable to know that the participant already rejected that same generalization. The person-level participant-authority invariant can therefore be functionally bypassed after freeze even without rereading raw narrative.

**Why this violates permitted authority**

The participant co-coding architecture states that multiple similar episodes cannot override participant rejection and that person-level recurrence is participant-adjudicated. The candidate's own normative invariants repeat that rule. A downstream projection must preserve enough semantics, or impose a strong enough adapter rule, that target-specific post-freeze processing cannot recreate the externally finalized recurrence that the architecture rejects.

**Smallest repair needed**

Add a downstream semantic rule that episode facts may be consumed only as episode-level evidence and may not be aggregated into a person-level recurrence/typicality claim; person-level recurrence/typicality must come from accepted resolved patterns. If a later adapter design needs another person-level summary, it must be created through a new target-theory-blind participant-adjudicated freeze rather than target-specific post-freeze aggregation.

## Nonblocking implementation suggestions

These do not change the BLOCKED verdict and should not be mistaken for additional semantic blockers:

1. Make explicit in implementation validation that provenance locators/hashes identify the exact cited source segment or a deterministically resolvable bounded record, not merely a broad container.
2. Ensure `scope_note`, `exception_note`, and any resolved scope/exception text are source-bound to the participant adjudication that supports them and cannot be silently broadened by system synthesis.
3. Add ordinary referential-integrity checks for IDs, thread membership, link ownership, uniqueness, and canonical serialization. These are expected implementation mechanics, not reasons to re-expand the semantic ontology.

## Required repair cycle

The next substantive semantic change must occur in a **different fresh target-theory-blind context**. It should:

1. treat this review artifact as the exact blocker ledger;
2. preserve the open-world participant-adjudicated architecture and repair only the six defects above plus any directly required consistency edits;
3. avoid reintroducing a comprehensive fixed behavioral ontology, universal event-stage graph, recurrence threshold, or `Other Specified` escape hatch as a manufactured prerequisite;
4. publish a new versioned candidate architecture/contract rather than mutating the reviewed v1 artifacts;
5. produce a new exact candidate-specific fresh blind review prompt;
6. update canonical state to point to the new candidate-producing head and prompt;
7. stop before production implementation or any human/target-model activity.

A separate fresh target-theory-blind reviewer must then review that new candidate. The present review context must not perform the semantic repair or self-approve a revised candidate.
