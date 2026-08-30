# Natal-time synthetic evaluation-contract verifier — 2026-08-30

## Scope and contract bindings

This local verifier exercises only frozen, preconstructed synthetic evaluation vectors. It is
bound to preserved study-design v1 digest
`c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9`, preserved
metric-semantics v2 digest
`067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`, and operative
metric/reference-domain v3 digest
`75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe`.

Every vector uses synthetic 2099 dates and supplies `S_i` as a fixed test vector. The verifier has
no function that constructs, ranks, prunes, scores, weights, or recommends `S_i`. It imports no
chart engine, Human Design inference model, questionnaire, relationship module, or selector. A
passing receipt is not evidence of recoverability, calibration, validity, rectification, accuracy
on people, or product usefulness.

## Physically separate bundles

The generated state tree has three deliberately separated surfaces:

```text
state/NATAL-TIME-SYNTHETIC-EVALUATION-V1/
├── inference/
│   ├── schema.json
│   ├── manifest.json
│   └── fixtures/SYNTH-FIXTURE-*.json
├── evaluator/
│   ├── schema.json
│   ├── manifest.json
│   └── references/SYNTH-CUSTODY-*.json
├── receipts/SYNTH-FIXTURE-*.json
└── evaluation-manifest.json
```

The inference-visible fixture contains only frozen `C_i`, the frozen method specification, the
preconstructed `S_i`, component-role declarations, contamination state, execution plan, and
`inference_visible_fixture_digest`. It contains no `T_i`, reference-custody identifier or digest,
canonical-`T_i` digest, reference path, byte size, combined-file digest, or evaluator manifest
locator. Its manifest binds only inference-visible schema and fixture files.
Evaluator-version data and exact evaluator/generator source-file hashes are deliberately absent
from that schema and manifest because the generator contains evaluator-only synthetic reference
vectors. Those bindings appear only on the evaluator side and in postcommit artifacts.

The evaluator-only object has a different closed schema and an opaque `SYNTH-CUSTODY-*` identity.
It contains the synthetic reference, documentary-source classification, precision
classification, custody classification, mutation-test mode, and its self-hash. Only the
evaluator-only manifest maps a frozen inference fixture to that object. The postcommit evaluation
manifest binds both separated manifests and the resulting artifacts; it is not an inference-role
input.

Changing only `T_i` or evaluator custody changes no inference-visible byte, fixture digest, or
inference-manifest entry.

## Custody capability and access order

`EvaluationSession` and `EvaluatorReferenceCustody` use ordered states, not caller-provided freeze
booleans:

1. validate and freeze complete `C_i` plus connected-component role assignments;
2. freeze a v1/v2/v3-bound method specification that declares a preconstructed `S_i` and no
   selection procedure;
3. validate exact membership and commit canonical `S_i`;
4. release an opaque capability bound to that exact `S_i` commitment;
5. let evaluator custody authorize the capability, then address, open, read, parse, serialize, and
   hash the evaluator-only object;
6. hand canonical reference data and custody binding to the metric evaluator; and
7. consume the loader into a deep-copied, version-locked custody snapshot, destroy the loader,
   and re-hash that exact snapshot immediately before metric computation and artifact issuance.

Before step 3, the custody operation counters for raw byte, open, read, stat, path, size, parse,
serialization, hash, listing, and addressability are all zero. Constructing custody places its
loader in an evaluator-private weak registry rather than on the custody instance. The inference
session holds no evaluator object, loader, locator, metadata, or enumeration surface. Calling the
normal access event early, presenting an unissued capability, or forging a reference handoff fails
before the loader is invoked. The one-shot loader registry entry is removed during authorized open.
Explicit early raw-byte, digest, metadata, and alternate-loader probes likewise fail closed while
all underlying operation counts remain zero.

After authorized access, a change to the version-locked snapshot fails the mandatory pre-artifact
custody check with `t_i_mutated_after_evaluator_access`. Replacement or mutation of the caller's
former loader backing cannot alter that consumed snapshot. Receipt issuance also requires the
evaluator-issued, exact-`S_i`-bound integrity-recheck handoff; a caller-supplied digest is not
accepted. Post-access `S_i` recommitment likewise invalidates the session. None of these paths can
emit a valid metric receipt or domain diagnostic.

## Exact `C_i` and unconstrained subset geometry

`C_i` remains the complete unordered candidate collection. Its positive-width half-open intervals
must be contiguous and non-overlapping within every declared civil-date domain and must not
overlap globally. Gaps between nonconsecutive declared date domains remain outside `D_i`.

A non-abstaining `S_i` is any nonempty unordered subset of exact whole `C_i` records. Equality
includes manifest and set digests, interval ID, endpoints, full-state digest, provenance, and civil
date. Duplicate IDs or complete records are rejected before canonical ordering. Proper
subintervals, manufactured spanning windows, foreign IDs, and substituted state or provenance are
rejected. `S_i` has no adjacency, contiguity, connectivity, or one-window validity requirement.

The fixed disconnected case has one synthetic date partitioned into four intervals and selects
only the first and third. Its temporal width sums those two intervals without filling the
unselected middle interval; interval retention is `2/4`; the repeated full-state identity is
counted once; and date coverage is independent. Reversing the same exact members preserves the
canonical fixture, `S_i` commitment, and receipt. A duplicated member and a manufactured first-to-
third spanning interval fail closed.

## Exact domain union and three-way reference status

`D_i` is the exact set union of unchanged `C_i` intervals, not their convex hull. After source
eligibility, lineage adjudication, precision preservation, and canonicalization, the evaluator
sums the exact positive-width intersection of `T_i` with the non-overlapping `C_i` partition:

- `reference_domain_compatible`: the overlap width equals the complete unchanged `T_i` width, so
  `T_i` is a subset of `D_i`;
- `reference_domain_partially_incompatible`: overlap width is positive but less than the complete
  `T_i` width; or
- `reference_domain_incompatible`: overlap width is zero, including endpoint-only contact.

Containment may span adjacent candidate intervals. A boundary inside `T_i` is not a defect.
Containment on either declared date of a multiple-date domain is compatible. A reference on an
excluded intervening date remains incompatible because the gap is not filled.

Partial or complete incompatibility never clips, intersects, expands, or replaces `T_i` or changes
`C_i`. It emits a closed `reference_domain_diagnostic`, not a valid reference-evaluation receipt.
That diagnostic binds exact `S_i`, canonical `T_i`, custody, access state, evaluator version, and
all three contracts. It contains only the controlled domain status, typed-null
`reference_intersection`, and the positive full documentary-reference width. It gives the method
neither credit nor error and contains no component metric object.

Fixed domain cases cover containment in one interval, containment across adjacent intervals,
extension before, extension after, extension across both date-domain ends, wholly outside,
endpoint-only contact, and included versus excluded dates in a multiple-date domain.

## Separate descriptive components

For a compatible operative reference, a non-abstaining descriptive receipt reports only:

- reference intersection;
- retained temporal-width numerator, denominator, and exact fraction;
- retained canonical-interval-count numerator, denominator, and exact fraction;
- retained unique full-state-identity-count numerator, denominator, and exact fraction;
- represented-date-count numerator, denominator, and exact fraction;
- documentary-reference width in integer microseconds; and
- explicit abstention.

No scalar summary or component ordering exists. Repeated nonadjacent intervals remain distinct
intervals while contributing one state identity. Endpoint-only contact is not intersection.
Abstention gives every `S_i`-dependent component a typed-null `not_applicable_abstention` value
while retaining documentary width for an otherwise operative compatible reference.

No eligible reference, canonicalization failure, and conflicting distinct source intervals retain
their v2 typed not-applicable behavior. Exactly identical intervals from separate documentary
sources corroborate one operative `T_i`; distinct intervals fail closed and are never averaged,
intersected, unioned, clipped, or selected.

## Receipts, schemas, and fixed failures

Every ordinary receipt binds the preserved v1 and v2 digests, operative v3 digest,
`inference_visible_fixture_digest`, candidate freeze, frozen method, canonical `S_i`, canonical
`T_i` when one exists, evaluator-custody digest, custody access-state digest, combined access-state
digest, evaluator-version digest derived from exact module and generator bytes, and metrics digest.
Each ordinary receipt, domain diagnostic, and fail-closed rejection has a closed shape and a
self-hash; rehashing an unknown top-level or nested field does not make it valid. Contextual
validation additionally compares externally frozen fixture, `S_i`, custody, access, and evaluator
bindings; recomputing a receipt self-hash after changing one of those bindings does not satisfy the
contextual validator.

Fixed failures cover empty non-abstention; partial, duplicate, foreign, and manufactured intervals;
early ordinary reference access; early raw-byte, digest, metadata, and alternate-loader probes;
post-access `S_i` and `T_i` mutation; cross-role connected components; and contamination. Rejected
artifacts carry controlled violation codes and no metrics.

The preregistration structural validator accepts no prose, item content, choices, scoring keys, or
generic headings. It requires exact controlled sets for all 15 baselines, 11 measurement
requirements, data roles, actor access, source eligibility and precision, connected-component
edges, leakage/contamination, metric components, disclosure threats and controls, prohibited
public fields, and disclosure-surface declarations.

## Privacy and implementation boundary

All schemas are closed. IDs, status values, roles, event codes, digests, synthetic dates, and UTC
instants use controlled values or patterns. Participant, contact, consent, recovery, personal
birth-record, relationship, household, response, questionnaire, arbitrary free-text, rank,
best-candidate, score, weight, probability, confidence, utility, threshold, and recommendation
fields are prohibited recursively.

The release-disabled aggregate schema from Phase 0 remains only a threat-model artifact, not
anonymity, de-identification, disclosure-safety, or release evidence. This verifier does not run on
people, create a selector or estimator, modify protected deterministic chart components, authorize
a participant-facing output, or alter replay/provenance artifacts.
