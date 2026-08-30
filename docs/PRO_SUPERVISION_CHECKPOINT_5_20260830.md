# Pro supervision checkpoint 5 — 2026-08-30

The following is the complete substantive ruling returned in the existing authenticated
ChatGPT Pro supervision conversation after review of exact final local head
`3b80ebbd6f42577ecc585a668ce4211937e7bda7`. UI-only citation labels were removed and rendered
math was normalized to `C_i`, `S_i`, `T_i`, and `D_i`; the ruling and authorization boundary are
otherwise preserved.

---

OWNER DECISION REQUIRED: NO

## 1. CHECKPOINT-5 VERDICT: QUALIFIED

The deterministic foundation remains qualified, and the checkpoint-4 Phase-0 closure is
accepted. The packet reports the required lineage attestation, replay-source attestation,
deliberate interruption/resumption proof, superseding metric contract, and bounded operational
evidence. It also reports exact protected-file identity, a clean worktree, passing tests, strict
typing, scoped linting, and privacy/history gates.

The synthetic evaluator is not yet unconditionally accepted. Four bounded issues remain:

1. The access-order design does not conclusively establish that every pre-`S_i` artifact visible
   to the inference side is independent of hidden `T_i`.
2. The verifier imposes an unapproved within-date contiguity restriction on `S_i`.
3. Partial `T_i`/`C_i`-domain overlap is treated as evaluable rather than as a distinct
   reference-domain incompatibility.
4. Replay-source equivalence is established only through checkpoint-4 head `90220a3`, while
   replay code subsequently changed before the current acceptance source.

These are contract and provenance defects, not evidence that the chart enumerator, replay
receipts, privacy gate, or deterministic interval calculations are wrong. No owner-level
scientific or product choice is required to correct them.

| Dimension | Ruling |
| --- | --- |
| Deterministic scientific foundation | Qualified and unchanged |
| Phase-0 lineage closure | Accepted |
| Real-engine replay receipts | Qualified, pending final-source binding |
| Interruption/resumption behavior | Accepted |
| Access-order leakage resistance | Remediation required |
| Schema closure | Provisionally accepted |
| Metric semantics | Remediation required |
| Protected provenance | Accepted for the 48 protected files; replay orchestration requires an extended attestation |
| Privacy and release boundary | Accepted for this synthetic/local scope |
| Scope compliance | Accepted |
| Participant inference or deployment readiness | Not authorized |

The packet confirms that no prohibited external or participant-facing action occurred.

## 2. Required corrections

### Blocking — 2.1 Remove the remaining hidden-reference commitment ambiguity

The packet states both that the precommit public-fixture digest excludes hidden `T_i` and that the
manifest binds the complete fixture file bytes. It also proves zero reference-parser calls before
authorized access. That is insufficient to prove access-order isolation. A manifest digest over
bytes containing `T_i` is itself `T_i`-dependent. Birth-time reference intervals are low-entropy
enough that an unkeyed hash could potentially be tested against candidate values. Zero parser
calls also does not exclude raw file reads, hashing, file-size observation, or another path that
handles the complete fixture bytes.

Create a superseding reference-custody contract with two physically and logically distinct
bundles:

- Inference-visible bundle: `C_i`, frozen method specification, preconstructed `S_i`, and its
  commitment.
- Evaluator-only reference bundle: `T_i`, documentary-source classification, precision metadata,
  custody metadata, and reference canonicalization.

No inference-visible pre-`S_i` artifact may contain:

- `T_i`;
- a deterministic digest of `T_i`;
- a digest of a file containing `T_i`;
- reference-file size or path metadata capable of varying with `T_i`; or
- a combined fixture digest whose bytes depend on `T_i`.

The evaluator may bind `T_i` privately before evaluation, but that binding must remain unavailable
to the inference role. The valid evaluation receipt may reveal the canonical reference digest only
after the exact `S_i` commitment is frozen.

Acceptance tests:

- Changing only `T_i` leaves every inference-visible precommit byte and digest unchanged.
- Before `S_i` commitment, instrumented execution performs zero open, read, stat, parse,
  serialization, or hash operations against the evaluator-only reference object.
- The inference role cannot enumerate, fetch, list, or address the evaluator reference object.
- The complete-fixture manifest is either created only by the evaluator after `S_i` commitment or
  split into separate inference and evaluator manifests.
- No unkeyed `T_i`-dependent commitment is exposed before `S_i` commitment.
- After authorized access, the receipt binds exact `S_i`, canonical `T_i`, reference custody,
  access state, evaluator version, and operative contract digests.
- Early-access, raw-byte-access, digest-access, file-metadata-access, and alternate-loader attempts
  all fail closed and produce no valid evaluation receipt.
- Deliberately changing `T_i` after evaluator access invalidates the reference custody chain.

This correction is required even though all current records are synthetic.

### Blocking — 2.2 Remove the unapproved within-date contiguity restriction

The verifier currently permits cross-date gaps but requires within-date contiguity. That is
inconsistent with the controlling definition of `S_i` as an unordered subset of unchanged whole
intervals from `C_i`. Contiguity is a structural prior. It would prohibit a future set-valued
procedure from retaining two separated intervals on the same date and could force disconnected
uncertainty into a false continuous window.

The generic verifier must accept any nonempty unordered subset of complete `C_i` intervals,
subject only to exact membership, no duplication, no partial interval, no manufactured boundary,
no foreign interval, and no overlap not already present in canonical `C_i`. It must not require
selected intervals to be temporally adjacent. A future single-contiguous-window output type would
be a separate method/product decision and is not authorized here.

Acceptance tests:

- Construct one synthetic date with at least four canonical intervals.
- Submit `S_i` containing the first and third intervals only; accept it without filling the gap.
- Temporal width is the sum of those two intervals only; interval-count fraction uses two; unique
  state count follows their full-state identities.
- Reordering produces the same commitment and receipt; duplication rejects; one manufactured
  spanning window rejects.
- No contiguous-window or best-window semantic appears in the generic receipt.

### Blocking — 2.3 Distinguish full reference compatibility from partial overlap

Preserving a partially overlapping `T_i` unclipped is correct. Calling it fully compatible is not.
Let `D_i` be the union of intervals in `C_i`. The verifier must use three states:

- `reference_domain_compatible` when `T_i` is a subset of `D_i`;
- `reference_domain_partially_incompatible` when the intersection has positive width but `T_i` is
  not a subset of `D_i`; and
- `reference_domain_incompatible` when the intersection has zero width.

For partial or complete incompatibility, do not clip, intersect, expand, or replace `T_i`; do not
modify `C_i`; do not issue a valid reference-accuracy result; make `reference_intersection`
non-applicable; report a candidate/reference-domain defect; and give the method neither credit nor
error. Documentary width and incompatibility status may remain diagnostics. This is not an
inference-metric choice.

Acceptance tests cover reference intervals fully contained in one canonical interval, fully
contained across adjacent intervals, extending before, extending after, extending across both
ends, wholly outside, endpoint-only contact, and multiple-date domains with the reference on an
included versus excluded date. Only full containment and the included-date case may produce valid
reference-evaluation receipts.

### Blocking — 2.4 Extend replay-source provenance through the acceptance source

Create a post-closure replay-delta attestation comparing receipt source `1c59b8a`, evaluated source
`90220a3`, operational source `b3e5314`, Phase-1 source `3c12801`, and acceptance source
`2f707858`. Classify every changed function/path as scientific engine input, fixture definition,
event/interval construction, receipt semantic construction, canonical serialization, digest
construction, independent verification, resumption/durability orchestration only, or
test/documentation/output only.

Route A, equivalence proof, is sufficient only if engine invocation, fixture inputs, event and
interval lists, receipt semantic fields, canonicalization, and digest functions are byte-identical
or mechanically equivalent through `2f707858`; every replay change affects only interruption,
durable writes, validation, or index recovery; all nine receipt bytes remain valid; aggregate-only
verification reproduces the declared index and aggregate hashes; and a changed semantic input
fails the equivalence validator.

Route B, regeneration, is required if receipt-semantic code changed: produce a new immutable set of
all nine receipts from a new clean source commit, preserve the old set, issue new source/fixture/
receipt/index/aggregate hashes, rerun production-versus-independent verification including Apia,
and never relabel the old receipts. The documentation-only difference from `2f707858` to
`3b80ebbd` does not require regeneration.

### Blocking — 2.5 Add a machine-readable checkpoint-5 acceptance matrix

For every prior/current acceptance rule, record requirement ID, test path/name, fixture ID,
expected outcome, actual controlled status/rejection code, receipt digest where applicable,
contract version, evaluator-version digest, exact source commit, and whether it exercises schema,
access order, metric semantics, provenance, or privacy.

At minimum demonstrate full-`C_i` unit fractions; canonical reorder equivalence; repeated-state
interval/state-count divergence; access-state binding on every valid receipt; and rejection of a
rehash-added forbidden scalar/inferential field.

### Non-blocking improvements

1. Rename public-fixture digest to `inference_visible_fixture_digest` or equivalent; public must
   not imply release authorization.
2. Keep the transient protected-test commits in lineage. Say protected files are byte-identical at
   reviewed and acceptance heads, not historically untouched.
3. Retain the corrected-command ledger including the zero-test, npm, and combined-file-mypy
   invocation errors and their corrected gates.
4. Keep lint claims scope-specific; do not claim repo-wide clean lint.

## 3. Next bounded slice authorized

### CHECKPOINT-5 REMEDIATION AND REFERENCE-CUSTODY CLOSURE ONLY

Local work and commits are authorized only on `codex/astrohd-relationship-continuation`. Push is
not authorized. The slice is limited to:

- separated inference-visible and evaluator-only reference bundles;
- closing all pre-`S_i` raw-byte and digest leakage paths;
- superseding the metric contract to remove within-date contiguity;
- adding the three-way reference-domain compatibility state;
- extending replay-source provenance through `2f707858`;
- adding the machine-readable acceptance matrix;
- synthetic fixtures/tests required to prove those corrections; and
- checkpoint-6 evidence.

No estimator, baseline execution, questionnaire work, participant workflow, or scientific
operating rule may be added.

Checkpoint 6 must return with exact final head/tree/diff from `b7660b8`; v3 contract preserving v1
and v2; both bundle schemas; custody/access model; pre-`S_i` invariance evidence; instrumented zero
open/read/stat/parse/serialize/hash traces; disconnected same-date `S_i` receipts; partial-domain
incompatibility receipts; post-closure replay attestation or regenerated receipts; complete
acceptance matrix; exact-head tests, mypy, Ruff, privacy/history/build, diff, protected-blob, and
clean-worktree gates; and confirmation of no prohibited action.

Successful local remediation does not authorize inference, push, merge, migration, or deployment.

## 4. Hard prohibitions

The following remain prohibited: push; PR actions; merge, rebase, cherry-pick, squash, force update,
or main mutation; GitHub governance changes; touching draft PR #1; Railway deployment or mutation;
secret-value reads; removing `OPENROUTER_API_KEY`; migration; production routes; participant access,
recruitment, or collection; questionnaire content/scoring/interpretation; any `S_i` chooser;
ranking/pruning/elimination/recommendation; priors, weights, scores, mass, probabilities,
confidence, or utility; numerical thresholds; participant-facing output; relationship evidence;
baseline execution; public-ledger work; human-validity/calibration/accuracy/benefit claims; or
qualified-engine/adapter/enumerator/evidence-state/identity/provenance/result-semantic changes.

No owner decision is required. The blocking findings are resolved by the existing scientific,
access-control, and set-valued-output contracts rather than by choosing a product direction or
inferential method.
