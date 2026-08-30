# Natal-time pre-inference metric semantics v3 — 2026-08-30

## Status and narrow supersession

The operative machine-readable contract is
`state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json`, with logical contract SHA-256
`75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe`.
It implements checkpoint-5 contract corrections 2.2 and 2.3 only. It does not modify the
evaluator, select `S_i`, run a baseline, calculate a participant result, or authorize participant
inference.

V1 and v2 remain preserved byte-for-byte. V3 supersedes v2 only where v2 treated partial
candidate/reference-domain overlap as compatible or could be read to permit an adjacency rule on
selected `S_i`. Every other v2 interval, documentary-source, output-validity, metric, and
prohibition rule remains operative, as do all non-superseded v1 study-design rules.

The preservation bindings are:

- v1 logical contract `c721dcdd5ed9e144ca4795523420e226bc13dc8a739669991c365c1bb4d3f6c9`
  and exact file SHA-256
  `dc76792218c32ccca392ecdfb2cd706f3f3df6112df2a15a40310bd99be0ed04`;
- v2 logical contract `067417a49c158fd7d7d1d31c3b21a584c1d1259aa85d60a30e9a6d3f39976f5e`
  and exact file SHA-256
  `a1244378acbb7c0cf5a3f6464c7d1186dda9c70dac300357e28f9d530cb5adfd`.

## Candidate partition and selected-subset geometry are different rules

`C_i` remains the complete canonical candidate set. Within each declared candidate civil-day
domain, its positive-width half-open intervals must form the complete gap-free, non-overlapping
partition required by the preserved candidate-set contract. No qualifying candidate interval may
be omitted, and no intervals may be merged across a full-state change.

That candidate-construction completeness rule does not constrain the geometry of a returned
subset. A non-abstaining `S_i` is **any nonempty unordered subset** of exact unchanged whole
interval records from frozen `C_i`. The selected members need not be adjacent, contiguous, or
connected. They may be separated by unselected intervals on the same date or by gaps between
candidate dates. A generic candidate-subset verifier must therefore accept the first and third of
four same-date intervals without adding the second or manufacturing a spanning window.

Every preserved validity rule still applies: exact whole-record membership, no duplicate IDs or
identities, no partial interval, no changed endpoint, no manufactured union/split/interpolation,
and no foreign manifest, candidate set, civil domain, provenance, or full-state identity. Duplicate
detection occurs before canonical ordering. After that validation, reordering the same members has
no semantics and must produce the same commitment and receipt.

A contiguous-window or best-window output would be a separate method and product choice. It is
not part of the generic `S_i` contract and remains unauthorized.

## Exact candidate domain

`D_i` is exactly the set union of every unchanged interval in `C_i`:

`D_i = union_{I in C_i} I`.

It is not the convex hull or a single bounding interval. If declared candidate-date domains are
separated, the gap remains outside `D_i`. Compatibility classification may not fill that gap,
expand `D_i`, or alter `C_i`.

## Three reference-domain states

Classification occurs only after documentary eligibility, source-lineage adjudication, precision
preservation, and canonicalization have produced one operative positive-width half-open `T_i`.
Let overlap width be the summed positive elapsed width of `T_i intersect D_i`. Endpoint-only
contact contributes zero.

1. `reference_domain_compatible`: `T_i` is a subset of `D_i`. Every coordinate in `T_i` is
   covered by the union of `C_i`; no positive-width portion lies outside. `T_i` may span adjacent
   canonical intervals because their union remains continuous across their shared boundary.
2. `reference_domain_partially_incompatible`: overlap width is positive, but `T_i` is not a
   subset of `D_i`. This includes a reference extending before, after, or across both ends of the
   candidate domain.
3. `reference_domain_incompatible`: overlap width is zero. Wholly outside intervals and
   endpoint-only contact are in this state.

Partial overlap is no longer evaluable. For partial or complete incompatibility, the evaluator
must not issue a valid reference-accuracy result or valid reference-evaluation receipt.
`reference_intersection` is respectively
`not_applicable_reference_domain_partially_incompatible` or
`not_applicable_reference_domain_incompatible`, never `true` or `false`. The method receives
neither credit nor error.

No classification may clip `T_i` to `D_i`, substitute the intersection for `T_i`, expand `D_i`,
fill a candidate-domain gap, or change an endpoint in either object. The complete unchanged
documentary width and the incompatibility status may remain diagnostic. Documentary width remains
a precision descriptor, not coverage, error, probability, confidence, score, weight, or partial
credit.

## Disconnected-subset metrics

When `S_i` is otherwise valid, each retained component uses only selected members:

- temporal width is the sum of selected interval widths, without filling unselected gaps;
- interval count is the number of selected exact records, whether adjacent or not;
- unique-state count is the number of distinct selected `full_state_sha256` values; and
- date coverage counts only dates represented by at least one selected member.

These remain separate. V3 adds no scalar outcome, threshold, preferred frontier point, ranking,
or ordering.

## Required edge cases

The machine-readable contract enumerates every checkpoint-5 case:

- first-and-third same-date selection, its reordered equivalent, duplicate rejection, and
  manufactured spanning-window rejection;
- `T_i` wholly contained in one interval;
- `T_i` wholly contained across adjacent intervals;
- `T_i` extending before, extending after, and extending across both domain ends;
- wholly outside and endpoint-only contact;
- a multiple-date candidate domain with `T_i` on an included date; and
- a multiple-date candidate domain with `T_i` on an excluded date.

Only containment in one interval, containment across adjacent intervals, and the included-date
case permit a valid reference-evaluation receipt. Partial and complete incompatibility produce
only typed diagnostic status and documentary width.

## Reproducible audit

`scripts/audit_natal_time_metric_semantics_v3.py` verifies the exact v1/v2 bytes and logical
hashes, the v3 self-hash, the separation of `C_i` partition validation from `S_i` adjacency, the
exact three-state classification, every required edge case, neutral incompatibility disposition,
and absence of evaluator or selector implementation. Its deterministic receipt is
`state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3-AUDIT.json`.

This contract does not change the qualified engine, adapter, enumerator, evidence state machine,
identity, replay, Phase-1 verifier, reference-custody bundle, or checkpoint acceptance matrix.
