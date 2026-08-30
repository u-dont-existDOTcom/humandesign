# Pro supervision checkpoint 6 — 2026-08-30

The following is the complete substantive ruling returned in the existing authenticated ChatGPT
Pro supervision conversation after review of exact final local head
`a7a516fe7dc679909fba392a511570ae603e4fe3`. UI-only citation labels were removed and rendered
math was normalized to `C_i`, `S_i`, `T_i`, and `D_i`; the ruling and authorization boundary are
otherwise preserved.

---

OWNER DECISION REQUIRED: NO

## 1. CHECKPOINT-6 VERDICT: QUALIFIED

On the packet supplied, checkpoint-5 remediation is substantively complete. The deterministic and
Phase-0 foundation remains qualified within the previously approved, engine-relative claim.

The evaluated implementation-evidence head is
`067ed6cdd504b368b88c203ca6d058c20b2fb913`; the final head
`a7a516fe7dc679909fba392a511570ae603e4fe3` adds only the checkpoint document. The complete branch
remains local, with a clean worktree and passing exact-head gates.

### Remediation-surface rulings

#### 1. Reference custody: QUALIFIED

The packet closes the checkpoint-5 leakage defect for the present **synthetic, local,
cooperative-code threat model**:

- Inference-visible artifacts exclude `T_i`, reference digests, custody identifiers, reference
  paths and sizes, evaluator provenance, and combined hashes dependent on `T_i`.
- Evaluator references are separated into evaluator-only objects.
- Access requires a private one-use capability and creates a version-locked snapshot.
- Tests reportedly establish invariance when only `T_i` changes and zero precommit
  open/read/stat/parse/serialize/hash operations.
- Valid receipts bind exact `S_i`, canonical `T_i`, custody and access state, evaluator bytes, and
  all operative contract versions.

This qualification does **not** establish security against arbitrary malicious Python code running
in the same process. A module-private registry and sentinel are an application-level access
boundary, not an operating-system security boundary. That limitation is non-blocking while all
records remain synthetic; it becomes a hard stop before live documentary reference data.

#### 2. Metric semantics v3: QUALIFIED

V3 correctly:

- preserves V1 and V2 rather than overwriting them;
- permits any nonempty unordered subset of whole `C_i` intervals;
- removes the within-date contiguity prior;
- accepts disconnected same-date selections without filling the gap;
- rejects duplicates and manufactured spanning intervals;
- separates complete compatibility, partial incompatibility, and complete incompatibility;
- withholds reference-accuracy results for partial or complete domain incompatibility; and
- preserves `T_i` and `C_i` without clipping or replacement.

The resulting semantics remain descriptive and set-valued. They do not authorize a mechanism for
choosing `S_i`, an operating threshold, or an inferential interpretation.

#### 3. Replay Route-A provenance: QUALIFIED WITH FINAL-HEAD CLOSURE REQUIRED

The supplied attestation supports Route A through acceptance source
`2f707858425cb51f61c5d57e6a0364faf092b841`: semantic replay inputs and construction are reported
unchanged or mechanically equivalent, all nine receipts validate, aggregate-only reconstruction
reproduces the committed hashes, and altered semantic input fails validation.

One narrow provenance gap remains: the replay attestation terminates at `2f707858`, while the
current implementation-evidence head is `067ed6c` and the final submission head is `a7a516f`. The
exact-head validator passed, but the packet does not explicitly state that every replay-affecting
byte remained identical from `2f707858` through `067ed6c`. This is a documentation and
source-binding defect, not a demonstrated replay failure.

#### 4. Machine-readable acceptance matrix: QUALIFIED

The matrix has 81 entries, records requirement-to-test-to-fixture mappings, includes the five
expressly required checkpoint-5 minima, excludes hidden reference material, and reproduces through
its validate-only path.

Its qualification is bounded to the committed source and evaluator versions it identifies. It is
not a substitute for independent verification of the computations under test.

## 2. Required corrections

### Blocking

#### 2.1 Bind replay provenance to the checkpoint-6 implementation-evidence head

Create a content-hashed, machine-readable final replay-source closure covering:

- Receipt-generation source: `1c59b8aae3c096c84a8116d49c0cb0525029837e`.
- Checkpoint-5 acceptance source: `2f707858425cb51f61c5d57e6a0364faf092b841`.
- Checkpoint-6 implementation-evidence head: `067ed6cdd504b368b88c203ca6d058c20b2fb913`.
- Documentation-only final head: `a7a516fe7dc679909fba392a511570ae603e4fe3`.

It must inventory all files and functions capable of affecting:

- fixture inputs;
- engine invocation;
- event or interval construction;
- independent verification;
- receipt semantic fields;
- canonical serialization;
- digest construction;
- index construction and validation; and
- durable-write and resume behavior.

Acceptance tests:

- `1c59b8a`, `2f707858`, `067ed6c`, and `a7a516f` form the declared ancestor chain.
- `067ed6c` is the direct parent of the documentation-only submission commit, as claimed.
- Every replay-semantic file has identical Git blob bytes at `2f707858` and `067ed6c`; or every
  difference is explicitly classified and mechanically proven to affect only fail-closed loading,
  durability, testing, or documentation.
- Any difference affecting fixture inputs, engine calls, interval/event output, receipt contents,
  canonicalization, or digest formation forces Route B regeneration of all nine receipts from a
  new clean source commit.
- At `067ed6c`, committed receipt bytes validate and aggregate-only reconstruction reproduces
  index self-hash `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435`
  and aggregate SHA `ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`.
- The validator fails after a controlled change to any replay-semantic byte.
- The attestation itself reproduces byte-for-byte.
- No existing receipt or earlier attestation is overwritten.

This is the only remaining blocking checkpoint-6 correction.

### Non-blocking

#### 2.2 Narrow the custody-security terminology

Replace “unforgeable” with wording such as:

> capability-guarded and unforgeable through the supported application interface

unless the threat model explicitly excludes hostile in-process code.

Before any live reference data, require physical enforcement through separate process identity,
storage permissions, and evaluator-only credentials. Do not rely solely on Python privacy
conventions.

#### 2.3 Keep the exact verification scope visible

The full suite, strict typing, changed-file linting, privacy/history/build gate, protected-file
comparison, and clean-worktree checks passed. The packet also correctly preserves the one
historical protected-file Ruff finding rather than claiming repository-wide clean lint.

Continue recording:

- exact interpreter used;
- exact changed-file Ruff range;
- historical lint exclusions;
- failed or corrected invocations; and
- exact artifact source commit versus documentation-only final commit.

#### 2.4 Preserve synthetic-only scope labels

The packet states that no estimator, `S_i` chooser, questionnaire, baseline execution, ranking,
participant workflow, or deployment was introduced. Preserve those explicit scope labels in every
derived artifact.

## 3. Next bounded slice authorized

## FINAL PROVENANCE CLOSURE AND INDEPENDENT SYNTHETIC EVALUATOR ORACLE ONLY

Local commits on `codex/astrohd-relationship-continuation` are authorized. **Push remains
prohibited.**

### Phase 0 — final provenance closure

Complete blocking correction 2.1.

If any replay-semantic source changed after `2f707858`, stop after either:

- returning the discrepancy to Pro; or
- regenerating a new immutable receipt set under Route B and returning it for review.

Do not proceed by relabeling the existing receipts.

### Phase 1 — structurally independent synthetic evaluator oracle

After Phase 0 passes, implement a test-only oracle that independently recomputes the approved V3
descriptive results and rejection classifications.

The oracle must not import or call the production evaluation functions being checked. It may
consume the same canonical synthetic fixture specification, but must independently implement:

- whole-interval membership validation;
- duplicate and manufactured-boundary rejection;
- canonical unordered-set handling;
- temporal-width calculation;
- canonical interval-count calculation;
- unique full-state-count calculation;
- date coverage;
- documentary width;
- reference-domain containment classification;
- half-open reference-intersection semantics; and
- abstention and non-applicable component handling.

It may use only preconstructed synthetic `S_i`. It must contain no procedure that generates,
ranks, optimizes, or chooses `S_i`.

### Required adversarial corpus

Include deterministic, committed cases for:

- full `C_i`;
- single-interval `S_i`;
- disconnected first-and-third same-date intervals;
- reordered equivalent `S_i`;
- duplicate interval;
- partial interval;
- manufactured gap-spanning interval;
- foreign interval;
- repeated nonadjacent intervals with the same full-state identity;
- multiple candidate dates;
- `T_i` contained within one interval;
- `T_i` spanning several included intervals;
- partial reference overlap before the domain;
- partial reference overlap after the domain;
- partial overlap across both ends;
- zero-width or endpoint-only contact;
- wholly incompatible reference date;
- abstention;
- empty non-abstention;
- documentary-source conflict;
- precommit `T_i`-access attempt;
- post-access `S_i` mutation;
- cross-role connected-component contamination;
- nested forbidden-field insertion; and
- rehashed scalar, score, probability, confidence, threshold, or recommendation insertion.

### Acceptance rules

- The production verifier and independent oracle agree on every valid descriptive component.
- They agree on every controlled rejection or diagnostic classification.
- Reordering an unordered `S_i` changes neither commitment nor metrics.
- Interval count and unique-state count diverge correctly when full-state identities repeat.
- Partial and complete reference-domain incompatibility produce no valid accuracy result.
- Abstention does not become zero width, zero retained states, success, or failure.
- The oracle performs no reference read before the exact `S_i` commitment.
- Changing only `T_i` leaves every inference-visible precommit byte unchanged.
- Mutation testing demonstrates that removing each major access, schema, or metric guard causes at
  least one test to fail.
- Any oracle/verifier discrepancy produces a fail-closed discrepancy ledger and blocks checkpoint
  completion.
- No artifact contains participant data or a participant-like exact birth record.
- No output contains a scalar summary, candidate preference, rank, score, probability, confidence,
  utility, threshold, or recommendation.
- The 48 qualified deterministic files remain byte-identical.
- Full tests, strict mypy, exact changed-file Ruff, privacy/history/build gates, artifact validators,
  and `git diff --check` pass at the implementation-evidence head.
- The worktree and index are clean.

Return to Pro at checkpoint 7 with the final replay-source closure, independent-oracle source and
version digest, adversarial comparison matrix, mutation report, discrepancy ledger, exact
head/tree, and confirmation that no prohibited action occurred.

## 4. Deterministic and Phase-0 status

The deterministic engine, exact interval enumerator, evidence state machine, immutable records,
real-engine fixtures, replay receipts, and Phase-0 foundation remain **QUALIFIED**.

The exact-head packet reports 372 passing tests, strict typing across 132 source files, successful
artifact and privacy gates, zero mismatches across the 48 protected files, and a clean worktree.

This qualification remains limited to deterministic behavior relative to the pinned engine,
ephemeris, timezone database, runtime, floating-point coordinate behavior, and state-identity
contract. It does not extend to Human Design validity, birth-time recoverability, human
calibration, participant benefit, or relationship inference.

## 5. Hard prohibitions

No authorization is granted for:

- push to any remote branch;
- opening or updating a pull request;
- merge, rebase, cherry-pick, squash, force-update, or main mutation;
- GitHub governance, ruleset, or branch-protection changes;
- touching stale draft PR #1;
- Railway mutation or deployment;
- secret-value reads;
- removing `OPENROUTER_API_KEY`;
- migration or storage changes;
- production-route mounting;
- live participant or documentary-reference access;
- recruitment or data collection;
- questionnaire content, choices, scoring keys, or interpretations;
- any procedure that generates or chooses `S_i`;
- candidate ranking, pruning, elimination, recommendation, or best-window selection;
- priors, weights, scores, duration mass, probabilities, confidence, utility, or scalar
  aggregation;
- numerical operating, stopping, or abstention thresholds;
- participant-facing output;
- relationship evidence or compatibility inference;
- execution of HD, non-HD, random, permutation, or mismatched-chart baselines;
- public-ledger implementation or publication;
- claims of HD validity, human calibration, rectification accuracy, or participant benefit; or
- modification of the qualified deterministic engine, adapter, enumerator, evidence state
  machine, identity, provenance, or immutable result semantics.

The read-only external state remains unchanged, and the packet reports no push, PR action,
production mutation, participant access, inference, or release.
