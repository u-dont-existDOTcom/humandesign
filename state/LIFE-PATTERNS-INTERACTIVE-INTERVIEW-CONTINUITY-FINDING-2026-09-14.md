# Life Patterns interactive-interview continuity finding — 2026-09-14

Status: **OWNER CLARIFICATION / PRODUCT-ARCHITECTURE CORRECTION**.

## Finding

The owner correctly identified that the project had already designed an interactive Life Patterns interview before the later coding/calibration work. The coding work was necessary as evidence-layer infrastructure, but it was not a replacement for the participant-facing interview.

The historical product roadmap already specified a conversational text interview as the MVP surface. The pattern-first longitudinal v8 design then made an explicit construct-level correction: the participant-facing interview should begin from the participant's own report of recurring patterns and use concrete episodes as evidence anchors, clarification, and counterexample checks rather than treating a collection of specific episodes as the product objective.

The later participant-adjudicated v2 semantic repair improved the research substrate: open-world facts, append-only corrections/provenance, participant authority over person-level patterns, genuine-absence gating, immutable evidence timing, and adapter firewalls. Those constraints belong behind the interaction surface. They do not require the participant to perform coding or annotation work.

The surfaced fact-review prototype therefore represented a product-layer wrong turn: internal evidence bookkeeping was exposed as the experience. The owner rejected that strategy on 2026-09-14.

The current hidden-ledger conversational probe fixes the most important layer-separation error by hiding the evidence ledger, but its opening currently asks for one specific situation first. That partially regresses the participant-facing elicitation strategy relative to the earlier v8 pattern-first design. This is not required by the accepted v2 semantics.

## Correct synthesis

The next participant-facing architecture should combine, rather than choose between, the two mature strands:

`pattern-first adaptive conversation -> minimal concrete anchors / contrasts / life-phase evidence -> hidden v2 evidence ledger -> informative synthesis / boundary check -> participant authority -> immutable freeze -> downstream adapters`

Keep the strongest v8 interaction principles:

- begin from what the participant reports as recurring, changing, puzzling, or context-dependent rather than requiring an arbitrary first episode;
- ask one main question per turn;
- establish meaningful context boundaries and developmental change;
- request only enough concrete evidence to anchor or challenge a claim;
- ask for a useful exception/counterexample without forcing one;
- distinguish participant-reported recurrence from evidentiary support strength.

Do **not** restore v8 as a closed fixed taxonomy. The accepted v2 open-world architecture remains authoritative. Historical domain prompts may be used as coverage scaffolding, not as an exhaustive ontology or forced classification scheme. Preserve an open residual route for patterns that do not fit predefined domains.

## Current runtime blocker observed by owner

During the first natural owner turn in the deployed hidden-ledger app, the UI returned:

`non-hypothesis moves cannot carry hypothesis fields`

The current `ConversationMove` validator correctly prohibits hypothesis payload on `follow_up`, `request_contrast`, and `boundary_question`, but the live model can return a non-hypothesis move while still populating `hypothesis_proposition` and/or `evidence_fact_ids`. The raw structured output therefore fails Pydantic validation before the interviewer reply is returned.

This is a mechanical model-output normalization defect, not evidence that the hidden-ledger or v2 semantics are invalid. Owner judgment of conversational information gain is blocked until it is repaired.

Because extraction is applied before `plan_turn`, a failed planning call may already have mutated the in-memory hidden ledger for that session. Owner should not simply resubmit the same first message into the same failed session as a repair strategy.

## Decision

Do not continue owner product judgment on the current deployment.

Repair the runtime move-normalization defect and reconcile the participant-facing opening/elicitation loop with the earlier pattern-first interaction design while preserving the accepted v2 hidden evidence contract. Then redeploy the owner-only prototype and resume bounded owner judgment.

This finding does not authorize external participant collection, automated participant coding, target-model activity, recruitment/contact, merge/release, or broader public deployment.
