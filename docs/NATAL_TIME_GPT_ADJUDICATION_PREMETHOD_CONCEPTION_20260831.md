# GPT adjudication protocol — pre-method conception

Date frozen: 2026-08-31

Status: source-free conception; no checkpoint-14 methods search has occurred

## Problem

A future automated adjudication workflow needs to preserve what each evaluation run knew, what it
did not know, and when its output became immutable. Repeating an evaluation in a new run is not the
same as obtaining a distinct underlying evaluator, and agreement between runs is not proof of
correctness. The control plane must expose these differences without yet choosing or executing an
adjudication method.

The workflow also needs to prevent a later reconciliation stage or an interested owner from
rewriting initial judgments, erasing disagreement, or converting a procedural failure into a
substantive outcome. A real-use boundary must remain closed until every currently unknown
operational and scientific prerequisite is explicitly resolved.

## Identity separation

The architecture should represent evaluator identity, service or artifact revision, run identity,
context identity, context history, configuration, evidence packet, initial commitment, and later
reconciliation record as separate provenance objects. Equality in one dimension must not imply
equality in another.

Separate initial runs may share hidden dependencies and systematic errors. Their separation is a
custody and access property, not a statistical-independence claim.

## Evidence custody and access order

Each initial run should bind an exact digest of one canonical synthetic evidence packet before any
judgment is committed. Access events should be ordered and attributable. Neither initial run may
receive the other run's unsealed output. Reconciliation may begin only after both initial
commitments exist and must consume immutable copies rather than editable working records.

The architecture should distinguish a missing or conflicting evidence state from a substantive
outcome. It should also distinguish a procedure that cannot be validated from a procedure that ran
validly but did not reach a determinate result.

## Sealing and disagreement

An initial commitment should be append-only and content-addressed. Correction should create a new,
linked record without deleting or replacing the original. A disagreement should remain an explicit
state even after reconciliation. Agreement may be recorded as an observed relationship between
initial outputs, but it must not be promoted to correctness.

No default consensus mechanism should be embedded at this stage. The control plane should preserve
the inputs and alternatives needed for a later authorized choice without preselecting how a
disagreement is resolved.

## Owner influence and confirmation risk

An owner can have a preference about the future result. Owner actions therefore require a distinct
event type and may supply governance or factual-correction records without mutating an initial
commitment or creating a clean substantive outcome. Any bypass must remain visibly non-clean and
cannot be reclassified by an owner event.

The architecture should make confirmation pressure observable through immutable history rather
than assuming that role labels remove the underlying conflict.

## Candidate independent mechanisms

1. A closed identity registry with separate opaque identifiers and digests for every evaluator,
   revision, run, context, history, configuration, evidence packet, commitment, and reconciliation
   record.
2. Two separately initialized synthetic initial-run slots that bind the same canonical packet and
   cannot access peer output before both commitments are sealed.
3. Append-only initial commitment records whose original bytes and outcome-state type cannot be
   mutated by reconciliation or owner activity.
4. A separately initialized reconciliation slot that can reference both sealed commitments while
   preserving disagreement and every original state.
5. An access-order ledger that fails closed on pre-seal cross-run access, mismatched packet digests,
   missing provenance, or reuse of one context as two contexts.
6. A typed state vocabulary that keeps insufficient evidence, evidence conflict, procedural
   invalidity, indeterminate status, and substantive outcomes distinct without choosing transition
   or resolution rules.
7. A real-use readiness register in which every operative selection and execution permission is
   unset until separately authorized.
8. Synthetic mutation probes that attempt to smuggle personal data, human-facing wording,
   operative settings, result claims, or prohibited domain content into otherwise valid metadata.

These mechanisms are candidates for comparison with existing work. They are not selected methods.

## Risks

- Separate runs may reproduce the same hidden bias or training-derived error.
- Context histories may differ despite superficially identical configuration labels.
- Equivalent-looking evidence packets may differ in ordering, omissions, or normalization.
- A later stage may erase disagreement by overwriting, summarizing, or relabeling initial records.
- Confidence-like metadata may invite unsupported averaging or majority decisions.
- Agreement may be mistaken for accuracy.
- Version drift may make a nominally repeated procedure non-reproducible.
- Owner influence may enter through evidence selection, factual-correction channels, or bypasses.
- Personal or domain content may leak into a nominally metadata-only protocol.
- A closed schema may still encode a hidden operative choice if field semantics are not audited.

## Constraints

- This checkpoint is synthetic and metadata-only.
- All operative evaluator, configuration, evidence, and resolution choices remain unset.
- No external evaluation execution occurs.
- No real-person evidence or result is represented.
- No human-facing language is authored.
- No substantive content, measurement, or later comparison work begins.
- Existing accepted artifacts remain unchanged.
- Production and external systems remain unchanged.
- Root completion and release remain false.

## Success conditions for the architecture

- Every identity and custody dimension can vary independently in synthetic tests.
- Pre-seal cross-run access and context reuse fail closed.
- Initial commitments remain immutable through every later synthetic stage.
- Disagreement, insufficient evidence, conflict, and procedural invalidity remain visible.
- No agreement, owner action, or reconciliation record can assert correctness or create a clean
  substantive result.
- Closed schemas reject personal, human-facing, operative-selection, result-smuggling, substantive,
  and later-comparison fields.
- The architecture remains neutral among future method choices.

## Unresolved topics

- A supportable evidence standard for future real adjudication.
- Scientifically adequate evaluator configuration or configuration set.
- Measurement of sensitivity to ordering, framing, labels, and repeated runs.
- Evidence needed to distinguish meaningfully heterogeneous configurations.
- Acceptable abstention and insufficient-evidence behavior.
- Reconciliation of disagreement without hiding correlated error.
- Feasible drift and reproducibility controls for a changing service or artifact.
- Privacy, retention, and access rules for real evidence.
- Validation required before any real-person use.

No answer, selection, threshold, transition rule, or reconciliation procedure is adopted here.
