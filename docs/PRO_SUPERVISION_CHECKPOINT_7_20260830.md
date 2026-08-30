# Pro supervision checkpoint 7 — 2026-08-30

The following is the complete substantive ruling returned in the existing authenticated ChatGPT
Pro supervision conversation after review of exact final local head
`b581ab3b7397abf5aed5e6da7f7e04deb22e2a06`. UI-only labels were removed and rendered math was
normalized to `C_i`, `S_i`, `T_i`, and `D_i`; the ruling and authorization boundary are otherwise
preserved.

---

OWNER DECISION REQUIRED: NO

## Checkpoint-7 overall ruling

**CHECKPOINT-7 STATUS: QUALIFIED, WITH ONE NARROW CURRENT-HEAD PROVENANCE CLOSURE REQUIRED**

No supplied evidence indicates a defect in the qualified chart engine, deterministic interval
enumerator, evidence state machine, replay receipts, V3 metric semantics, access-order contract,
or synthetic evaluator calculations.

The remaining defect is narrower: the final replay-source closure terminates at checkpoint-6
submission head `a7a516fe7dc679909fba392a511570ae603e4fe3`, while checkpoint 7 is evaluated at
implementation head `d2ee0a3b875f2e21c37534d5e338947a6e3ff098` and submitted at
`b581ab3b7397abf5aed5e6da7f7e04deb22e2a06`. The packet does not yet provide a machine-readable
proof that no replay-semantic source changed between `a7a516f` and `d2ee0a3`.

That is a provenance-completeness defect, not a scientific-computation failure.

The prior checkpoint-6 scope explicitly excluded any estimator, `S_i` chooser, questionnaire,
baseline execution, participant workflow, ranking, probability, relationship evidence,
migration, deployment, or release; that remains the controlling boundary.

## 1. Evidence-surface rulings

### A. Final replay provenance closure

**RULING: QUALIFIED THROUGH `a7a516f`; CURRENT-HEAD EXTENSION REQUIRED**

The submitted closure appears sufficient for its declared range:

- It binds the original receipt source and checkpoint-5/6 heads.
- It inventories 58 replay-affecting files and 28 semantic functions.
- It establishes byte or AST identity across the checkpoint-6 range.
- It revalidates all nine receipts.
- It reconstructs the exact committed index and aggregate.
- It demonstrates fail-closed behavior after a controlled semantic mutation.
- It preserves prior receipts rather than relabeling them.

The limitation is purely temporal: checkpoint-7 implementation occurred after the closure's
terminal commit.

The statement that `d2ee0a3 -> b581ab3` changes only three documentation/state files is useful and
likely sufficient for the final documentation child, but the packet does not provide the
equivalent explicit comparison for:

`a7a516f -> d2ee0a3`

Because replay orchestration files are not necessarily included among the 48 checkpoint-3
protected files, protected-core identity alone does not close this gap.

### B. Oracle structural independence

**RULING: QUALIFIED**

The oracle is adequately qualified as a **structurally independent test implementation** because:

- It uses only the standard library.
- Its AST audit finds no imports from `hdmatch` or repository scripts.
- It does not call the production evaluator or builder.
- It independently implements the relevant interval, membership, count, date, reference,
  abstention, access-order, contamination, and prohibited-field semantics.
- It contains no method for generating, ranking, optimizing, or choosing `S_i`.
- Its exact source hash and version digest are declared and bound to V3.

This does not make the oracle an independent scientific validation of Human Design or of
birth-time recovery. It is an independent implementation of the already approved synthetic
evaluation contract.

The shared canonical fixture specification is acceptable. Structural independence does not
require independently inventing the test inputs; it requires independently computing the expected
semantics from those inputs.

### C. Adversarial production-versus-oracle comparison

**RULING: QUALIFIED**

The comparison is sufficient for the bounded synthetic contract:

- 41 committed cases.
- All 29 required coverage tags.
- 41/41 production–oracle agreement.
- Zero discrepancies.
- Explicit same-date disconnected-set coverage.
- Reordering invariance.
- Repeated-state interval-count versus unique-state-count divergence.
- Partial and complete reference-domain incompatibility.
- Endpoint-only nonintersection.
- Typed abstention.
- Precommit reference nonaccess.
- `T_i`-only precommit invariance.
- Recursive forbidden-field rejection.
- Six independently checked rehashed prohibited-field mutations.

This qualification applies to the committed adversarial domain. It is not a proof over every
possible malformed object or every future contract version.

### D. Mutation report

**RULING: QUALIFIED AS A TARGETED MUTATION AUDIT**

The report meets the checkpoint-6 requirement that removing major guards must cause test failure:

- Thirteen explicit mutations cover membership, abstention, access, contamination, domain,
  half-open, schema, and fraction guards.
- All thirteen were killed.
- No survivors were concealed.
- Each mutant ran in a fresh complete synthetic project tree.
- The source-identity test was appropriately deselected because it would trivially kill every
  source mutation without demonstrating semantic test sensitivity.
- Stable failing or erroring test nodes, rather than volatile timing or temporary paths, determine
  mutant death.
- The flawed missing-builder harness was corrected before committing mutation artifacts.
- The corrected harness exposed a genuine missing endpoint assertion, which was then added.

The result should remain described as a **targeted** mutation audit, not a complete mutation score
for the evaluator.

A non-blocking strengthening is specified below to ensure that every claimed kill is attributable
to semantic or access-contract behavior rather than another source-bound artifact check.

### E. Fail-closed discrepancy ledger

**RULING: QUALIFIED**

The ledger behavior is adequate:

- The real comparison produces zero entries and an unblocked completion state.
- An injected disagreement generates a self-hashed blocking ledger.
- A disagreement prevents successful checkpoint completion.
- The ledger reproduces exactly.
- No discrepancy is silently converted into agreement, omission, or warning-only status.

Its empty state proves agreement only for the committed comparison corpus. It does not imply
universal production–oracle equivalence.

### F. Synthetic custody boundary

**RULING: QUALIFIED WITH THE DECLARED LIMIT**

The synthetic/local/cooperative-code custody boundary remains acceptable for this phase.

It is not sufficient for live documentary records. A module-private registry, one-use capability,
and supported-interface protections do not isolate data from arbitrary hostile code executing
within the same process and operating-system identity.

The packet correctly preserves this limitation. Separate process identity, evaluator-only
credentials, storage permissions, and an independently enforceable access boundary remain a hard
prerequisite before any live `T_i`.

## 2. Blocking defect and exact acceptance test

### Blocking defect: checkpoint-7 current-head artifact and replay provenance is incomplete

Create one immutable machine-readable artifact, for example:

`state/NATAL-TIME-CHECKPOINT7-CURRENT-HEAD-CLOSURE.json`

It must bind:

- Checkpoint-6 final head: `a7a516fe7dc679909fba392a511570ae603e4fe3`.
- Oracle source commit: `01a60b28aac84a5b5ecbe66e64a489b8345e0d1b`.
- Checkpoint-7 implementation-evidence head: `d2ee0a3b875f2e21c37534d5e338947a6e3ff098`.
- Checkpoint-7 final documentation head: `b581ab3b7397abf5aed5e6da7f7e04deb22e2a06`.
- Final tree: `a4a8dfc1947df513cf2fbeac82000992b74bce9d`.
- The existing replay-closure logical and exact-file hashes.
- The oracle source, version, corpus, matrix, mutation-report, and discrepancy-ledger hashes.

### Required acceptance tests

#### Commit topology

- `a7a516f` is an ancestor of `d2ee0a3`.
- `01a60b28` is an ancestor of `d2ee0a3`.
- `d2ee0a3` is the direct parent of `b581ab3`.
- No merge commit or alternate-parent path occurs in the relevant range.
- The exact `d2ee0a3..b581ab3` name-status diff contains only:
  - `CURRENT_PLAN.md`
  - `state/CURRENT-STATE.md`
  - `docs/NATAL_TIME_CHECKPOINT7_ACCEPTANCE_20260830.md`

Any additional path fails the closure.

#### Replay-current-head binding

- Compare all 58 replay-affecting paths at `a7a516f` and `d2ee0a3`.
- Compare the AST-normalized bodies of all 28 replay-semantic functions at those heads.
- Fixture inputs, engine invocation, interval/event construction, independent verification,
  receipt semantic fields, canonical serialization, digest construction, and index construction
  must be identical.
- Changes limited to testing, documentation, fail-closed validation, or unrelated oracle code must
  be explicitly classified.
- Any change capable of altering a receipt's scientific or semantic contents requires:
  - Route B regeneration of all nine receipts from a new clean source commit; or
  - return to Pro without claiming closure.
- At `d2ee0a3`, aggregate-only validation must reconstruct exactly:
  - Index self-hash
    `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435`.
  - Aggregate SHA
    `ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`.
- A controlled mutation to any replay-semantic path or function must make the current-head closure
  fail.

#### Oracle-current-head binding

- The exact oracle source blob at `01a60b28`, `d2ee0a3`, and `b581ab3` must hash to:

  `4192061951696d28d9d2671c70e13bb69b38aeba95ee83dc9e53f40eadb234c3`

- The oracle version must recompute to:

  `f3a3fc3b273da8a7d9a94d8e6b2e02bbbd9169093979aec42d084c272b78b623`

- The AST audit must be rerun against the exact `d2ee0a3` oracle source and continue to find:
  - no `hdmatch` import;
  - no repository-script import;
  - no dynamic import of those modules;
  - no subprocess invocation of the production evaluator;
  - no `S_i`-generation or optimization path.
- The four oracle artifacts must reproduce from `d2ee0a3` and match their declared exact hashes.
- A controlled oracle-source mutation must invalidate the oracle-version and current-head closure.

#### Protected and scope checks

- All 48 checkpoint-3 protected paths remain byte-identical.
- No newly changed path introduces participant data, documentary reference data, relationship data,
  questionnaire content, candidate choice, or inferential semantics.
- The closure artifact must reproduce byte-for-byte.
- The worktree and index must be clean after validation.

If all 21 tests pass, the blocking provenance defect is closed without reopening deterministic or
replay conformance.

## 3. Non-blocking improvements

### A. Add a semantic-kill map for the mutation audit

For each of the thirteen mutants, record:

- Mutated function and exact transformation.
- Expected guard loss.
- Stable killing test node.
- Relevant assertion or controlled rejection code.
- Whether artifacts were rebuilt under the mutant source identity.
- Confirmation that the kill was not caused solely by source hash, evaluator-version,
  immutable-file, or artifact-digest mismatch.

At least one non-provenance semantic assertion should kill every mutant.

This is not required to rerun a broader mutation search. It makes the existing `13/13` claim more
auditable.

### B. Preserve the distinction between structural and external independence

Use:

> structurally independent synthetic contract oracle

Do not shorten this to:

> independently validated evaluator

The latter could imply independent scientific validation or an external codebase.

### C. Keep zero-discrepancy language bounded

Use:

> zero discrepancies across the committed 41-case adversarial corpus

Do not use:

> the production evaluator and oracle are equivalent

### D. Preserve corrected-command history

The import-path failure, nondeterministic raw-output hashing, missing-builder false-kill discovery,
immutable-generator `FileExistsError`, and Python-version mypy issue should remain in the
operational ledger. They are relevant evidence that failed checks were corrected rather than
hidden.

## 4. Deterministic and Phase-0 foundation

**DETERMINISTIC/PHASE-0 FOUNDATION: REMAINS QUALIFIED**

Nothing in this packet reopens the qualified deterministic scientific claim:

- The 48 protected checkpoint-3 paths remain byte-identical.
- The real-engine replay receipts remain unchanged.
- The original replay index and aggregate reproduce.
- The new oracle is test-only and does not participate in chart enumeration.
- No qualified chart, evidence, provenance, interval, or immutable-result semantics were modified.
- No live record, relationship evidence, or participant-facing inference entered the system.

The qualification remains narrowly engine-relative:

> The pinned engine deterministically partitions each admissible candidate civil-day domain into
> maximal intervals of constant declared full state, at the documented coordinate precision, with
> candidate-complete stable/variable facts.

It still does not establish:

- Human Design validity.
- Birth-time recoverability.
- Questionnaire validity.
- Human reliability.
- Real-world calibration.
- Participant benefit.
- Compatibility inference.
- Any probability or ranking semantics.

## 5. Next bounded slice authorized

## CHECKPOINT-7 CURRENT-HEAD CLOSURE AND OWNER-DECISION DOSSIER ONLY

Local work and local commits on `codex/astrohd-relationship-continuation` are authorized.
**Push is not authorized.**

### Phase 0 — current-head closure

Complete the blocking current-head provenance artifact and all 21 acceptance tests above.

If any replay-semantic change is found after `a7a516f`, stop unless Route B receipt regeneration is
performed under a new clean source commit. Do not relabel the existing receipt set.

If any qualified deterministic path differs, stop and return to Pro; deterministic conformance is
reopened.

### Phase 1 — owner-decision dossier

Only after Phase 0 passes, create a documentation-only decision dossier for the next scientific
direction. It may organize—but may not resolve—the following options:

- **Stop and archive the deterministic foundation.**
  - No human study.
  - Preserve the infrastructure as an auditable negative or neutral result.
- **Measurement-reliability phase before rectification.**
  - Study whether proposed self-report constructs can be elicited reliably without testing
    birth-time recovery.
  - No chart-based candidate selection.
- **Blinded falsification study design.**
  - Test whether a future HD-based method adds out-of-sample value over the strongest ordinary
    non-HD and permutation controls.
  - Still no estimator or questionnaire implementation in this slice.

The dossier may state:

- Scientific question.
- Evidence required.
- Primary failure modes.
- Minimum governance prerequisites.
- Approximate resource classes rather than approved expenditure.
- What would falsify or terminate each direction.
- Which existing methods-contract components are reusable.
- Which choices remain owner decisions.

It may not select:

- A study direction.
- A questionnaire construct.
- An estimator.
- An operating point.
- A cohort size.
- A recruitment plan.
- A probability interpretation.
- A participant-facing product objective.
- A public disclosure regime.

Checkpoint 8 must present that dossier as an explicit owner choice. No substantive scientific
implementation may continue after the dossier without an owner ruling.

## 6. Hard prohibitions

The following remain prohibited:

- Push to any remote.
- Opening or updating a pull request.
- Merge, rebase, cherry-pick, squash, or force-update.
- Main-branch or GitHub-governance changes.
- Touching stale draft PR #1.
- Railway mutation or deployment.
- Secret-value reads.
- Removing `OPENROUTER_API_KEY`.
- Database, storage, or volume migration.
- Production-route mounting.
- Live participant or documentary-reference access.
- Recruitment or data collection.
- Questionnaire items, response choices, scoring keys, or interpretations.
- Any procedure that generates or chooses `S_i`.
- Candidate ranking, pruning, elimination, recommendation, or best-window selection.
- Priors, weights, scores, duration mass, probabilities, confidence labels, utilities, or scalar
  summaries.
- Numerical operating, stopping, or abstention thresholds.
- Participant-facing natal output.
- Relationship evidence or compatibility inference.
- Execution of HD, non-HD, random, permutation, or mismatched-chart baselines.
- Public-ledger implementation or publication.
- Claims of HD validity, human calibration, rectification accuracy, or participant benefit.
- Modification of the qualified deterministic engine, adapter, enumerator, evidence state machine,
  identity, provenance, or immutable result semantics without reopening conformance.

No owner decision is required for the current closure because the remaining work is provenance
verification and preparation of a decision packet. **An owner decision becomes mandatory
immediately after that slice, before any measurement, study, inference, participant, push, merge,
migration, or deployment work.**
