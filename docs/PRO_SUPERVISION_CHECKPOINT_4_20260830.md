# ChatGPT Pro supervision checkpoint 4 — 2026-08-30

Conversation: `Scientific Audit Checkpoint`

Evaluated branch: `codex/astrohd-relationship-continuation`

Evaluated head: `90220a3d67e847d883b2060fa3578fe5026cc414`

The response below was captured from the existing authenticated ChatGPT Pro conversation. Formatting has been normalized to Markdown; the ruling and requirements are preserved.

---

OWNER DECISION REQUIRED: NO

## 1. CHECKPOINT-4 VERDICT: QUALIFIED

The deterministic replay and synthetic pre-inference contract substantively satisfy the checkpoint-3 acceptance package. The deterministic foundation remains scientifically qualified within its previously limited claim.

The packet supports acceptance of:

- Fixture-granular real-engine replay across all required civil-day cases.
- Direct real-engine fail-closed handling of the skipped Apia date.
- Immutable per-fixture receipts and astronomy-free aggregate verification.
- Preservation of the qualified engine, adapter, enumerator, evidence, provenance, and immutable-record implementations.
- Formal `C_i`, `T_i`, and `S_i` separation.
- Documentary-reference precision preservation.
- Development/calibration/validation separation at connected-component level.
- Executable leakage and contamination validators.
- Non-scalar coverage–width–state-count–abstention evaluation.
- Complete null, negative-control, and ordinary non-HD baseline specification.
- Requirements-only measurement design with no questionnaire content.
- Synthetic-only feasibility calculations with no selected cohort size or effect.
- Release-disabled aggregate schema and disclosure threat model.
- Methods classification and machine-readable unresolved decisions.
- Exact-head tests, typing, changed-file linting, privacy gates, and clean worktree.
- No external mutation, participant access, inference implementation, or production exposure.

It is not marked **ACCEPTED** because the packet leaves one formal lineage discrepancy and two replay/metric semantics insufficiently evidenced. These are bounded remediation items, not evidence that the deterministic science failed.

The deterministic qualification remains limited to reproducible partitioning and stable/variable set facts relative to the pinned engine and its demonstrated coordinate behavior. It does not validate Human Design, birth-time recovery, questionnaire inference, human calibration, relationship interpretation, or any probability-like semantics.

## 2. Required corrections

### Blocking corrections

These block unconditional checkpoint-4 acceptance and must be completed before the next synthetic verifier work begins.

### 2.1 Close the checkpoint-head lineage discrepancy

Checkpoint 3 was reviewed in this conversation at:

`8cc97025f1e30c52a156e3c7bb5068baf5aea39b`

The current packet instead labels:

`5251c6f`

as the “checkpoint-3 base,” without explaining its relationship to the reviewed head. The replay is separately bound to source commit:

`1c59b8aae3c096c84a8116d49c0cb0525029837e`

and the current head is:

`90220a3d67e847d883b2060fa3578fe5026cc414`

That may be completely benign, but the chain cannot be inferred.

Create a content-hashed machine-readable lineage attestation that includes:

- Main baseline `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`.
- Reviewed checkpoint-3 head `8cc97025f1e30c52a156e3c7bb5068baf5aea39b`.
- The role and parentage of `5251c6f`.
- Replay source commit `1c59b8aae3c096c84a8116d49c0cb0525029837e`.
- Current head `90220a3d67e847d883b2060fa3578fe5026cc414`.
- Tree hashes for all four relevant commits.
- Complete ordered commit list and parent topology from the reviewed checkpoint-3 head to current head.
- Total current diff against `b7660b8`, not only the diff against `5251c6f`.
- Name-status and statistics for:
  - `8cc97025..5251c6f`
  - `5251c6f..1c59b8a`
  - `1c59b8a..90220a3`
  - `b7660b8..90220a3`

Acceptance tests:

- `8cc97025f1e30c52a156e3c7bb5068baf5aea39b` is an ancestor of the current head.
- `1c59b8aae3c096c84a8116d49c0cb0525029837e` is an ancestor of the current head.
- Every protected deterministic file has the same byte hash at the reviewed checkpoint-3 head and current head.
- The three immutable artifacts retain the declared hashes.
- No unreported merge commit or alternate-parent path exists between the reviewed head and current head.
- The attestation reproduces byte-for-byte.
- If the reviewed checkpoint-3 head is not an ancestor, stop and return to Pro. Do not repair the discrepancy by rebasing, cherry-picking, or rewriting history.
- If any protected deterministic file differs, deterministic conformance is reopened and this checkpoint becomes unqualified.

### 2.2 Bind the replay source to the current evaluated source

Generating receipts from an intermediate clean source commit and committing the outputs later is valid. It requires proof that no replay-affecting implementation changed afterward.

Create a complete replay-affecting source manifest covering:

- Replay orchestration.
- Receipt schemas and canonicalization.
- Source-integrity checks.
- Fixture definitions.
- Engine adapter invocation.
- Independent verifier invocation.
- Coverage/result digest construction.
- Aggregate-index construction and validation.

Acceptance tests:

- Every replay-affecting file has identical bytes at `1c59b8a` and `90220a3`, except output artifacts and documentation that cannot affect replay results.
- The allowed-difference list is explicit and fail-closed.
- Any non-allowlisted difference fails validation.
- If replay-affecting source changed, regenerate all nine receipts from a new clean source commit and issue a new index rather than asserting equivalence.
- At current head, aggregate-only verification reconstructs the index from committed receipt bytes and exactly matches:
  - Index self-hash `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435`.
  - Aggregate SHA `ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`.

### 2.3 Demonstrate actual interruption and resumption

Checkpoint 3 required that interrupted execution resume from valid receipts and that incomplete work never be treated as success. The packet describes granular receipts and aggregate reconstruction, but it does not report a deliberate interruption/resume test.

Add a temporary-directory integration test that:

- Begins with no receipts.
- Completes a strict subset of fixtures.
- Simulates interruption before index completion.
- Proves aggregate verification rejects the incomplete receipt set.
- Resumes without recomputing or changing already valid receipts.
- Completes the remaining fixtures.
- Produces an aggregate byte-identical to a clean uninterrupted execution.
- Proves missing, duplicated, corrupted, wrong-head, wrong-engine, and stale receipts each fail closed.
- Proves a partially written receipt is never treated as durable.
- Proves the Apia fail-closed receipt is required and cannot be replaced by omission.

The test may use fast synthetic receipt payloads for orchestration behavior, provided the committed real-engine receipt schema is exercised and no astronomy result is simulated as real.

### 2.4 Remove metric-edge ambiguity before executable evaluation

The current definition says `S_i` is a subset of `C_i` or abstention. Mathematically, the empty set is a subset. That ambiguity must be closed before metric code is written.

Create a superseding, content-hashed contract version linked to the current contract digest. Do not overwrite the existing artifact.

The superseding contract must state:

- A non-abstaining `S_i` must contain at least one unchanged whole interval from `C_i`.
- An empty non-abstaining `S_i` is invalid, not a maximally narrow result.
- Duplicate intervals, partial intervals, manufactured boundaries, and intervals outside `C_i` are invalid.
- Abstention produces an abstention result; it does not receive coverage `true`, coverage `false`, temporal width `0`, or state count `0`.
- If `T_i` does not intersect the complete domain represented by `C_i`, the case is a reference/candidate-domain incompatibility. It must be reported separately and excluded from method-accuracy scoring.
- Documentary endpoint and rounding conventions are canonicalized explicitly.
- Conflicting eligible documentary time sources fail closed under a predeclared adjudication status. They may not be silently averaged, intersected, or selected.
- Documentary-reference width is always retained as an output characteristic.
- “Retained interval count” and “retained unique full-state-identity count” are distinct quantities. Repeated nonadjacent intervals with the same state hash must not disappear from the interval-count metric.
- No scalar combination of coverage, width, interval count, unique-state count, date coverage, reference precision, or abstention is created.

Update the unresolved-decision register to reference the superseding contract while preserving the old contract and digest.

### Non-blocking corrections

These do not prevent the remediation slice from proceeding:

- Replace “production replay” with “local real-engine replay” or “production-code-path replay.” “Production” currently risks implying that deployed Railway state was exercised.
- Record the changed-file Ruff command and changed-path manifest in the checkpoint artifact so the 1,812 historical violations cannot obscure future lint regressions.
- Record machine and runtime duration metadata for expensive fixture generation as operational diagnostics. These must not enter scientific identity or be treated as performance guarantees.
- Add a concise statement that the release-disabled aggregate schema is a threat-model artifact, not evidence that the proposed fields are sufficiently anonymous for release.

## 3. Next bounded slice authorized

### CHECKPOINT-4 CLOSURE AND SYNTHETIC EVALUATION-CONTRACT VERIFIER ONLY

This is a local, reversible, synthetic-only slice with a mandatory internal gate.

### Phase 0 — mandatory checkpoint-4 closure

Complete all blocking corrections above.

If any ancestry, protected-file, replay-source, receipt, or interruption test fails, stop and return to Pro. Do not continue to Phase 1.

Successful Phase 0 does not authorize push, merge, migration, deployment, or participant work.

### Phase 1 — synthetic evaluation-contract verifier

After Phase 0 passes, build only a local verifier for the already frozen evaluation contract.

The verifier may:

- Consume conspicuously synthetic `C_i`, hidden synthetic `T_i`, and **preconstructed** synthetic `S_i` fixtures.
- Enforce artifact ordering:
  - Candidate-domain freeze.
  - Study/method-specification freeze.
  - `S_i` commitment.
  - Evaluator-only `T_i` access.
  - Metric receipt.
- Compute only the separate descriptive components:
  - Reference intersection.
  - Retained temporal-width fraction.
  - Retained interval-count fraction.
  - Retained unique-state-identity fraction.
  - Date coverage.
  - Documentary-reference width.
  - Explicit abstention.
- Create content-hashed evaluation receipts.
- Enforce connected-component role separation and contamination status.
- Validate that a future preregistration contains all required baseline, leakage, measurement, source-eligibility, and disclosure sections.
- Exercise adversarial fixed fixtures for endpoint behavior, repeated state identities, multiple candidate dates, wide documentary intervals, invalid documentary conflict, and reference-domain incompatibility.

The verifier must not choose `S_i`. Fixed synthetic `S_i` fixtures are test vectors, not outputs of a rectification method.

### Phase-1 acceptance tests

- `T_i` cannot be read before the `S_i` commitment is frozen.
- Modifying `S_i` after `T_i` exposure invalidates the component and produces no valid evaluation receipt.
- A participant or connected component cannot occupy more than one data role.
- Full `C_i` produces width and interval-retention fractions of one, without being called successful inference.
- Abstention leaves coverage and retention metrics non-applicable rather than zero.
- Empty non-abstention is rejected.
- Partial, duplicate, reordered-with-duplication, foreign, or manufactured intervals are rejected.
- Canonical reordering without semantic changes produces the same digest.
- `T_i` outside the candidate domain produces `reference_domain_incompatible`, not an inference miss.
- Boundary-touching behavior follows the declared canonical endpoint semantics.
- Retained interval count and unique-state count differ correctly when state identities repeat.
- Multiple-date coverage is reported separately from temporal width.
- No output contains rank, best candidate, score, weight, probability, confidence, utility, stopping threshold, or recommendation.
- No scalar summary is derivable from the public verifier schema.
- No random, HD-based, questionnaire-based, or non-HD model is implemented to select candidate intervals.
- No relationship field is accepted.
- No real participant identifier, exact personal birth record, contact field, consent field, recovery field, or free text is accepted.
- Every evaluation receipt binds the contract digest, fixture digest, access-state digest, and evaluator-version digest.
- Protected deterministic files remain byte-identical to the qualified versions.
- Exact-head tests, strict mypy, changed-file Ruff, privacy gates, hash checks, and a clean worktree pass.

Return at checkpoint 5 with:

- The lineage attestation.
- Replay-source manifest.
- Forced interruption/resumption evidence.
- Superseding metric-semantics contract.
- Evaluation-verifier schemas.
- All adversarial fixture receipts.
- Exact-head commit and total diff from `b7660b8`.
- Confirmation that no prohibited action occurred.

## 4. Explicit prohibitions

No authorization is granted for:

- Push to a remote branch.
- Opening or updating a pull request.
- Merge, rebase, cherry-pick, or force-update.
- Main-branch or GitHub-governance changes.
- Touching stale draft PR #1.
- Railway access beyond the already described read-only status checks.
- Deployment, configuration mutation, variable mutation, or secret-value reads.
- Removing `OPENROUTER_API_KEY`.
- Migration or storage changes.
- Production route mounting.
- Live participant access.
- Recruitment or data collection.
- Questionnaire content or response choices.
- Any procedure that selects, ranks, prunes, eliminates, or recommends candidate intervals.
- Priors, weights, scores, duration mass, probabilities, confidence labels, or utilities.
- Numerical stopping or abstention thresholds.
- Participant-facing output.
- Relationship evidence or compatibility inference.
- Actual execution of the planned HD or non-HD baselines.
- Public-ledger implementation or publication.
- Human-validity, calibration, accuracy, or rectification claims.
- Modification of the qualified deterministic engine, adapter, enumerator, evidence state machine, identity, provenance, or immutable result semantics.

No owner decision is required because the corrections follow directly from the existing scientific and provenance contract. The next owner decision remains deferred until a genuinely consequential choice is presented, such as selecting a participant-facing research objective, questionnaire-development direction, estimator family, operating point, cohort commitment, disclosure regime, push/merge path, or deployment plan.
