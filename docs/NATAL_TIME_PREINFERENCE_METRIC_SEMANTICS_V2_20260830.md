# Natal-time pre-inference metric semantics v2 — 2026-08-30

## Status and supersession

`state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V2.json` is the Phase-0 correction 2.4
metric-semantics contract. It is documentation and machine-readable policy only. It does not
implement an evaluator, calculate participant metrics, select an operating point, or authorize
participant inference.

V2 preserves
`state/NATAL-TIME-PREINFERENCE-DESIGN-CONTRACT.json` at contract SHA-256
`c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9` and does not overwrite
it. V2 supersedes that contract only for the more specific interval, documentary-reference,
returned-output, and metric semantics below. V1's study roles, leakage rules, baselines,
measurement requirements, and prohibitions remain in force.

The v2 JSON contract is self-hashed after removing only `contract_sha256` and applying the same
sorted-key compact JSON canonicalization used by v1. Its contract SHA-256 is
`067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`.

## Canonical intervals

Every candidate or documentary-reference interval is expressed on the pinned UTC Python datetime
coordinate grid as a positive-width half-open interval `[start_utc, end_utc)`. The coordinate
successor is one microsecond. This is a representation convention, not a claim of astronomical
microsecond accuracy.

A frozen candidate interval's identity comprises its candidate-manifest digest, candidate-set
digest, interval ID, UTC endpoints, and canonical `full_state_sha256`. A selected interval belongs to
`C_i` only if every identity field exactly matches a frozen record. Matching endpoints or a state
digest alone is insufficient.

Endpoint conversion is explicit:

- A closed lower endpoint remains the canonical start.
- An open lower endpoint moves to its first representable successor.
- An open upper endpoint remains the canonical end.
- A closed upper endpoint moves to its first representable successor.
- A canonical interval with `end_utc <= start_utc` fails closed.

## Documentary rounding and endpoint canonicalization

Canonicalization requires the recorded value, declared rounding quantum, rounding direction or an
explicit unknown-direction status, timezone/fold resolution, and endpoint convention. It never
infers missing precision from display formatting.

For recorded value `v` and quantum `q`:

- floor or truncation maps to `[v, v+q)`;
- nearest maps to `[v-q/2, v+q/2)`, with nonrepresentable half-quantum endpoints rounded outward;
- ceiling's `(v-q, v]` cell maps to `[successor(v-q), successor(v))`; and
- a known quantum with unknown direction maps to the smallest half-open envelope containing all
  three compatible cells and is marked `rounding_direction_unresolved`.

If the quantum is missing or the local value cannot be mapped uniquely enough to a canonical UTC
interval, no eligible `T_i` is produced. The participant is not calibration or validation ground
truth for that freeze. A printed clock value is never promoted to a zero-width point.

## Multiple eligible documentary sources

Each independently eligible source is canonicalized before adjudication. Multiple extracts from
one underlying record remain one source lineage rather than independent corroboration.

- One eligible source supplies the operative `T_i`.
- Multiple non-superseded sources that canonicalize to exactly the same interval yield that
  unchanged interval as operative `T_i`; all source intervals and widths remain in the audit
  receipt.
- If two or more non-superseded sources canonicalize to distinct intervals, status is
  `conflicting_eligible_documentary_sources`. Overlap is not treated as an adjudication rule.
  There is no operative `T_i`, no validation-frontier metric, and no calibration or validation
  recovery claim for that connected component.

A documentary source can be superseded only through explicit archive or correction lineage
recorded before evaluation freeze. The method's output, chart fit, questionnaire response, or a
more favorable result cannot decide between sources. Distinct source intervals may not be
averaged, intersected, unioned, clipped, or otherwise combined.

## Candidate/reference-domain compatibility

Let `D_i` be the union of canonical intervals in frozen `C_i`. After successful canonicalization,
operative `T_i` is domain-compatible when it has a positive-width intersection with `D_i`.
Touching endpoints alone do not intersect.

If `T_i` has no positive-width intersection with `D_i`, status is
`reference_domain_incompatible`. The output is not called uncovered, incorrect, or abstaining.
All validation-frontier metrics are not applicable, and the participant is excluded from recovery
evaluation for that candidate freeze. Partial overlap remains compatible: the evaluator retains
the complete unchanged `T_i` and full documentary-reference width and does not clip `T_i` to
`D_i`. Private output-geometry diagnostics may be retained for debugging but cannot enter
validation summaries.

The documentary-reference width is `T_i.end_utc - T_i.start_utc` in microseconds. It is a
reference-precision descriptor, not a performance metric, weight, probability, confidence, or
denominator adjustment. It can remain descriptively available when the procedure abstains if
`T_i` is otherwise operative and compatible.

## Returned-output validity

The only output kinds are a nonempty `candidate_subset` or explicit `abstention`.

For `candidate_subset`, every selected record must be one unchanged, whole member of `C_i`.
Validation rejects:

- an empty non-abstaining selection, without silently converting it to abstention;
- duplicate interval IDs or duplicate complete candidate identities, without silently
  deduplicating them;
- partial intervals with changed endpoints;
- manufactured unions, splits, interpolated windows, or substituted state identities; and
- foreign intervals from another participant-local domain, manifest, candidate-set digest,
  civil-domain freeze, or engine/state provenance.

For `abstention`, `selected_intervals` is empty. An abstention carrying intervals is invalid.
Abstention is explicit, neither success nor error, and cannot be inferred from an empty or
malformed candidate-subset record.

## Metric applicability

Invalid candidate or output records produce no metric and use `not_computed_invalid_output`.
Missing, conflicting, uncanonicalizable, or domain-incompatible references use their specific
not-applicable status rather than false, zero, error, or abstention.

For a valid explicit abstention, all `S_i`-dependent components are
`not_applicable_abstention`: reference intersection, retained temporal width, canonical interval
count, unique state-identity count, and date coverage. Only the abstention indicator is true. The
independent documentary-reference width may remain a reference descriptor.

For a valid non-abstaining output with compatible `T_i`, report separately:

1. **Reference intersection.** True exactly when a selected half-open interval overlaps `T_i`
   with positive width; touching endpoints do not intersect.
2. **Temporal width retained.** Report summed `C_i` and `S_i` microseconds and their fraction.
3. **Canonical interval count retained.** Report `|C_i|`, `|S_i|`, and their fraction. Duplicate
   serialized selections have already failed rather than being collapsed.
4. **Unique full-state identity count retained.** Report the distinct full-state digests in each
   set and their fraction. Disjoint intervals carrying the same state count as multiple intervals
   but one unique state identity; they are not merged for width or interval count.
5. **Date coverage.** Report candidate and selected declared-date counts, their fraction, and
   reference-date intersection separately.
6. **Abstention.** False for a valid nonempty subset and true only for valid explicit abstention.
7. **Documentary-reference width.** Copy the separate reference descriptor without treating it as
   procedure performance.

Temporal width, canonical interval count, unique state-identity count, coverage, date coverage,
abstention, and reference precision cannot be combined into a scalar utility, composite success
score, duration mass, probability, preferred frontier point, or implicit ranking.

## Implementation boundary

This correction supplies a content-hashed contract and structural tests only. It deliberately
does not create metric or evaluator execution. A later authorized phase must implement executable
validators and calculations from this contract before any synthetic or participant evaluation.
The qualified deterministic engine, enumerator, state identity, evidence state machine, and replay
artifacts remain unchanged.
