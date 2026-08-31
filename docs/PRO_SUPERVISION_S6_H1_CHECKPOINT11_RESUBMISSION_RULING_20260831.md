# Pro supervision checkpoint 11 resubmission ruling — S6/H1 pre-human governance

Date captured: 2026-08-31

## Exact decision boundary

`OWNER DECISION REQUIRED: YES`

`CHECKPOINT-11 VERDICT: NOT ACCEPTED — 59/60`

Failing requirement: `S6H1-30`.

Pro found the implementation evidence otherwise strong: all 28 hostile cases passed, the 60-node
V2 matrix passed mechanically, 699 repository tests passed at the implementation commit, no
production-source delta existed, protected-artifact comparisons reported zero mismatches, and no
prohibited external action occurred.

## Blocking provenance defect

Pro ruled that the preserved text currently labelled as a verbatim direct owner correction is the
assistant's subsequent interpretation rather than Joel's original wording. It contains advisory
phrases including:

- “I would make one correction to your proposed criterion”;
- “I would therefore use three statuses”; and
- “I would also drop the rationale…”.

Pro therefore ruled that this text cannot support the existing classifications
`DIRECT_OWNER_MESSAGE`, `OWNER_REATTESTED`, or bounded owner `MATCH` without Joel's explicit
confirmation. Pro explicitly corrected its preceding supervision ruling, which had accepted that
normalization as if it were verbatim owner text.

The controlling source capability and alignment are now:

- `capture_integrity: VERIFIED`;
- `acquisition_mode: ASSISTANT_INTERPRETATION`;
- `receipt_capability: INTERPRETIVE_NORMALIZATION_ONLY`; and
- `bounded_epoch5_policy_to_owner_alignment: UNCONFIRMED`.

Joel's earlier message established that prior chart exposure should not automatically exclude a
person, that people who found HD inaccurate might be useful, and tentatively proposed excluding
people who regard HD or astrology as working completely for them. Pro found that the message did
not explicitly ratify all of the following additions:

- exactly three substantive eligibility outcomes;
- mandatory blind adjudication for substantial technical familiarity;
- identity-defining self-concept as the controlling exclusion instead of the narrower proposed
  rule;
- rejection of the product-use rationale; and
- the complete normalized policy currently attributed to direct owner re-attestation.

## Requirement rulings

### Superseding `S6H1-18`: accepted

Human prior exposure is not automatically disqualifying. AstroHD-exposed repositories,
conversations, retrieval environments, and model sessions remain ineligible to originate
chart-blind content. Pro ruled that this separation is defensible and does not require the disputed
three-status policy.

### Clarified `S6H1-29`: accepted

Unknown, incomplete, or conflicting evidence may fail closed by blocking clean-role assignment
without automatically declaring the human ineligible. Pro ruled that this conservative process
rule does not contradict Joel's correction.

### Superseding `S6H1-30`: not accepted

The implementation is internally coherent and its synthetic tests pass, but Pro ruled that the
precise substantive policy it enforces has not been explicitly selected by Joel.

## Required alignment and assurance states

- `worker_to_contract_alignment: YELLOW`;
- `bounded_epoch5_policy_to_owner_alignment: UNCONFIRMED`;
- `root_contract_to_owner_alignment: PARTIAL`;
- `completion_claim: WORKING`;
- `parent_outcome: OPEN`;
- `operational_alignment: WARN`;
- `scientific_adequacy: WARN`;
- `release_adequacy: NOT_APPLICABLE`; and
- `release_permission: false`.

The deterministic, replay, construct-neutral Option B, B1 ordering, content-embargo, and
mapping-firewall foundations remain qualified. This defect concerns policy authority and source
attribution, not those scientific or deterministic surfaces.

## Exact owner decision required

### P1 — Ratify the implemented three-status policy (Pro recommendation)

Explicitly approve:

- prior HD or astrology exposure is not automatically disqualifying;
- substantial semantic, technical, or ontology-reproducing familiarity requires blind
  adjudication unless another ineligibility basis applies;
- identity-defining/comprehensive HD or astrology self-concept, or intentional derivation of
  constructs from it, makes someone ineligible for the clean H1 author role;
- unknown, incomplete, or conflicting evidence produces no substantive outcome; and
- belief, skepticism, mismatch, perceived accuracy, curiosity, usefulness, and product interest
  are not automatic decision rules.

Consequence: the current implementation can retain its substantive semantics. Only the
owner-source receipt and provenance records need correction to distinguish Joel's actual message
from the assistant's interpretation.

### P2 — Use Joel's narrower literal policy

Approve only:

- prior exposure is allowed;
- people who state that HD or astrology works completely for them are excluded; and
- substantial technical familiarity does not itself require adjudication unless Joel later
  decides otherwise.

Consequence: the current policy implementation must be revised. Pro assessed this as operationally
simpler but as carrying higher contamination risk because a person may reject HD while still being
capable of reproducing its ontology unconsciously.

### P3 — Supply a revised policy

Joel may specify another rule, particularly whether substantial technical familiarity is:

- eligible;
- subject to adjudication;
- automatically ineligible; or
- determined through another explicitly selected process.

Consequence: the implementation remains frozen until the revised policy is recorded and reviewed.

## Pro recommendation and hard stop

Pro recommends `P1` because it preserves Joel's core point that prior chart exposure is not
exclusionary while addressing the distinct risk that deep familiarity can shape constructs
regardless of belief. It also avoids treating self-reported accuracy percentages as a scientific
screening rule.

Required owner response: `P1`, `P2`, or `P3` with the revised rule.

No remediation, human action, screening design, construct work, construct-specific search,
mapping work, push, merge, migration, deployment, or external mutation is authorized before that
response.
