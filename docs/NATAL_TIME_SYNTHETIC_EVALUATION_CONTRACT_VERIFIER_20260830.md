# Natal-time synthetic evaluation-contract verifier — 2026-08-30

## Scope

This local Phase-1 verifier exercises only the already frozen pre-inference evaluation contract.
It is bound to preserved v1 digest
`c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9` and operative
metric-semantics v2 digest
`067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`.

Every vector is conspicuously synthetic, uses only dates in 2099, and supplies `S_i` as a fixed
preconstructed test vector. The verifier has no function that chooses, ranks, prunes, scores,
weights, or recommends an interval. It imports no chart engine, Human Design model,
questionnaire, relationship module, random selector, or non-HD selector. A passing synthetic
receipt is not evidence of human recoverability, Human Design validity, calibration, accuracy,
rectification, or product usefulness.

## Capability and access order

`EvaluationSession` enforces the following state transition rather than trusting caller-provided
freeze booleans:

1. freeze the complete candidate domain and connected-component role assignment;
2. freeze a method specification bound to v1 and v2, declaring the supplied `S_i` to be a
   preconstructed test vector and declaring that no selection procedure exists;
3. validate and commit the exact `S_i` record;
4. permit the independent synthetic evaluator to invoke the hidden-reference supplier; and
5. compute separate components and issue a receipt.

Calling the hidden-reference supplier before step 3 invalidates the session without invoking the
supplier. Attempting to recommit or mutate `S_i` after step 4 also invalidates the session. These
paths produce only a `fail_closed_rejection` artifact with `valid_evaluation_receipt: false`, no
metrics, and a controlled violation code.

Before step 3, the verifier checks and hashes only the public fixture envelope; it neither parses
nor includes the hidden-reference subtree in that pre-commit digest. The subtree's closed-schema,
prohibited-field, status, source, canonical-instant validation, and canonical digest occur inside
the evaluator supplier after commitment. The bundle manifest separately binds the exact bytes of
the complete fixture file, including its still-opaque hidden subtree. This packaging-integrity hash
is produced only after receipt construction and is not exposed to candidate, method, or output
actors.

Connected-component assignments contain only synthetic observation and component codes. Every
component must occupy exactly one of `development`, `calibration`, or `locked_validation`.
Cross-role or contaminated components fail before hidden-reference access.

## Exact interval and reference semantics

`C_i` is unordered for commitment purposes. Candidate intervals may span nonconsecutive declared
civil dates. Intervals must be contiguous within each declared date and may not overlap globally;
gaps between separate date domains are allowed. Candidate-set commitment canonicalizes order but
does not deduplicate records.

A non-abstaining `S_i` must contain one or more exact whole records from `C_i`. Equality includes
the manifest digest, candidate-set digest, interval ID, both UTC endpoints, full-state digest, and
civil date. Duplicate IDs or records are rejected before canonical ordering. Proper subintervals,
manufactured unions, foreign IDs, substituted state/provenance, and altered civil dates are
rejected. Explicit abstention requires an empty selection.

The hidden synthetic reference is already expressed as a positive-width canonical half-open UTC
interval. Multiple surviving sources are usable only if their canonical intervals are exactly
identical. Distinct intervals fail closed even when they overlap; they are never averaged,
intersected, unioned, clipped, or selected. A reference is domain-compatible when it overlaps
`C_i` with positive width. Endpoint touching alone is not overlap. Partial overlap—including a
one-microsecond overlap—remains compatible, and the full unchanged documentary interval and width
are retained.

`no_eligible_reference` and `reference_canonicalization_failed` are explicit reference states.
They produce typed not-applicable components rather than parser defaults, zeros, false coverage,
or inference misses.

## Separate descriptive components

A valid descriptive receipt contains exactly these components:

- reference intersection;
- retained temporal-width numerator, denominator, and exact rational fraction;
- retained canonical-interval-count numerator, denominator, and exact rational fraction;
- retained unique full-state-identity-count numerator, denominator, and exact rational fraction;
- represented-date-count numerator, denominator, and exact rational fraction;
- documentary-reference width in integer microseconds; and
- explicit abstention.

No scalar summary or component ordering exists. Repeated nonadjacent intervals with the same full
state remain separate intervals while contributing one unique state identity. Date coverage is
reported independently of temporal width. Full `C_i` produces unit retention fractions without a
success label.

Not-applicable metric objects preserve their component-specific fields with JSON `null` values.
For abstention, all `S_i`-dependent components are `not_applicable_abstention`; documentary width
remains available when the reference is otherwise operative and compatible. For missing,
uncanonicalizable, conflicting, or domain-incompatible references, every reference-dependent
component uses its specific typed not-applicable status. The abstention field remains the explicit
fact of the committed output.

## Commitments and artifacts

The generator is
`scripts/build_natal_time_synthetic_evaluation_verifier.py`. It derives an evaluator-version
packet from the exact bytes of that generator and
`src/hdmatch/natal_time/evaluation_contract.py`. Receipts bind:

- the logical v1 and v2 contract digests;
- the public, order-insensitive fixture digest;
- the candidate-domain freeze digest;
- the frozen method-specification digest;
- the canonical preconstructed-`S_i` commitment;
- the hidden-reference digest;
- the capability/access-state digest;
- the evaluator-version digest; and
- the separate metrics-object digest.

Each receipt and rejection is self-hashed. The manifest additionally binds every fixture's
public logical digest, exact complete-file digest, receipt digest, exact receipt-file digest,
evaluator version, and verifier schema. The exact file digest plus the post-commit
hidden-reference digest bind both halves without granting pre-commit reference access. Artifacts live under
`state/NATAL-TIME-SYNTHETIC-EVALUATION-V1/`.

## Fixed adversarial vectors

The bundle includes valid component vectors for full `C_i`, abstention, selected/reference
boundary touching, repeated state identities, nonconsecutive multiple dates, wide documentary
precision, and a one-microsecond partial-domain overlap. Reference-inapplicability vectors cover
exactly identical corroborating source intervals, distinct overlapping documentary sources,
domain incompatibility by endpoint touch, no eligible reference, and canonicalization failure.

Fail-closed vectors cover empty non-abstention, proper partial interval, duplicate interval,
reordered output with duplication, foreign interval, manufactured union, early reference access,
post-reference `S_i` mutation, cross-role component assignment, and contamination. In-memory
mutants additionally exercise nested extra fields, prohibited personal/free-text/relationship and
inferential fields, invalid synthetic dates, and substituted civil-date/state/provenance fields.

## Preregistration structural verifier

The preregistration verifier accepts no prose, item content, choices, scoring keys, or generic
headings. It requires exact controlled identifier sets copied or normalized from the frozen
contracts:

- all 15 baseline/falsification IDs;
- all 11 measurement-development and reliability IDs;
- all three data-role and six actor-access IDs;
- all documentary eligibility, eligible-class, ineligible-class, and precision-rule IDs;
- all connected-component edge and leakage/contamination IDs;
- all seven separate metric-component IDs;
- all disclosure-threat and unresolved disclosure-control IDs;
- the complete prohibited-public-field set; and
- explicit `cohort-aggregate-only`, `release-disabled`, pre-release threat-review, and
  threat-model-not-anonymity-evidence declarations.

Missing, duplicate, unknown, or heading-only substitutes fail structural validation.

## Privacy and implementation boundary

Fixture parsers are closed schemas at every nesting level. IDs, status values, roles, event codes,
digests, synthetic dates, and canonical instants have controlled values or patterns. Arbitrary
free text and extra fields are not accepted. Real-person, contact, consent, recovery, exact
personal birth-record, relationship, household, response, and questionnaire fields are
prohibited. Receipt fields containing rank, best-candidate, score, weight, probability,
confidence, utility, stopping threshold, or recommendation semantics are prohibited recursively.

The release-disabled aggregate schema from Phase 0 remains only a threat-model artifact. It is not
anonymity, de-identification, disclosure-safety, or release evidence. This Phase-1 verifier does
not implement or publish a ledger and does not authorize a participant-facing output.
