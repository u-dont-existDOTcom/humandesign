# Natal-time checkpoint 6 acceptance packet — 2026-08-30

## Scope and supervision boundary

ChatGPT Pro checkpoint 5 returned `OWNER DECISION REQUIRED: NO` and
`CHECKPOINT-5 VERDICT: QUALIFIED`. The exact ruling is
`docs/PRO_SUPERVISION_CHECKPOINT_5_20260830.md`. It accepted the deterministic foundation and
Phase-0 closure, then authorized only reference-custody, metric-v3, replay-provenance, acceptance-
matrix remediation, and checkpoint-6 evidence.

This packet contains only that authorized remediation. It introduces no estimator, `S_i` chooser,
questionnaire, baseline execution, participant workflow, ranking, pruning, score, weight, prior,
probability, confidence, threshold, recommendation, relationship evidence, live record, public
ledger, migration, deployment, or release.

## Exact source boundary

- Canonical comparison base: `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32` on `main` and
  `origin/main`.
- Exact implementation-evidence head:
  `067ed6cdd504b368b88c203ca6d058c20b2fb913`.
- Exact implementation-evidence tree:
  `7d6c05f73c90c0cb17ed894e8a9bd72593fa2db1`.
- Base-to-implementation diff: 212 files changed, 22,595 insertions, 54 deletions.
- Active local branch: `codex/astrohd-relationship-continuation`.

The commit adding this document is a documentation-only child of the implementation-evidence
head. The checkpoint submission records that later exact final head and tree directly, because a
tracked document cannot contain its own eventual commit identifier. No implementation or evidence
artifact changes between the implementation-evidence head and the submission head.

## Checkpoint-5 remediation

### 1. Physically and logically separated reference custody

The immutable synthetic evaluation bundle at `state/NATAL-TIME-SYNTHETIC-EVALUATION-V1/` contains:

- 35 inference fixtures under `inference/`;
- 35 evaluator-only reference-custody objects under `evaluator/`; and
- 35 postcommit receipts or diagnostic/rejection artifacts under `artifacts/`.

The inference schema and manifest contain no `T_i`, canonical-reference digest, reference-custody
ID or digest, reference path or size, evaluator source/version digest, or combined digest whose
bytes depend on `T_i`. Evaluator identity and reference custody first appear on the evaluator side
and in postcommit artifacts.

The access boundary uses a private sentinel-controlled capability and an unforgeable opened-
reference object. The reference loader is held in a module-private weak registry rather than on the
custody object. Authorized access consumes the one-shot loader exactly once into a deep-copied,
version-locked snapshot, destroys the loader entry, and requires a pre-metric integrity recheck.
Receipt validation binds the expected `S_i` values as well as their digest, so rehashing a changed
selection does not create a contextually valid receipt.

The test contract proves:

- changing only `T_i` leaves every inference-visible byte and digest unchanged;
- the precommit boundary performs zero evaluator-reference open, read, stat, parse, serialize, or
  hash operations;
- the inference role cannot list, address, fetch, or obtain a loader for the reference object;
- early raw, digest, metadata, and alternate-loader probes fail without producing an artifact;
- an unissued capability and a forged or insufficiently rechecked handoff fail closed;
- mutation before the preissue recheck or after authorized access invalidates custody; and
- every valid receipt binds exact `S_i`, canonical `T_i`, custody/access state, evaluator bytes,
  and operative v1, v2, and v3 contract digests.

Custody source commit: `8a00de79c6f25d8c72c608031143a10f42b59d02`.

| Artifact | Logical SHA-256 |
| --- | --- |
| Inference schema | `35e9676d94e008764721dca2f9361c350cbb8a2e72711f6d7fe9384c2c0d1e64` |
| Evaluator schema | `911084b5d101e8f56a77b8d32e493ab4af5c2b927e390907d8b50487cc95016f` |
| Inference manifest | `ce1cfedacdbf6e7358bad474cd507890f15664f57bbd15ba9017e0d5309ec48b` |
| Evaluator manifest | `bb589d0b0eaf60b50261bf06fb5af7486aa2fe0ee4d1abcf7b04ed590793f940` |
| Evaluation manifest | `873765791a9034d391523210b954fae23c2df3932ff281b90e9038150601d34b` |
| Evaluator version | `590f674df6f0bf40578086e52fe6a5e2872930cb033d2a4ff9466dbddb53258c` |

The artifact inventory contains 14 descriptive valid receipts, 16 fail-closed rejections, and five
reference-domain diagnostics.

### 2. Metric semantics v3

`state/NATAL-TIME-PREINFERENCE-METRIC-SEMANTICS-V3.json` preserves the exact v1 and v2 bytes and
supersedes v2 without modifying either earlier contract. Its logical digest is
`75a1629203724715054e2a1d7ea1b6ead7dc0ffd6cf5f4df2756c3e622b5f1fe`; its audit digest is
`ec7a6566e3f2c6f7e31a38b96122074bbdaeace500a3bf3a15973f6959655e58`.

V3 defines `S_i` as any nonempty unordered subset of unchanged whole intervals from `C_i`. It has
no adjacency or contiguity prior. A fixed same-date fixture selecting only the first and third of
four canonical intervals is accepted; its width is the sum of those intervals only, reordering is
equivalent, duplication rejects, and a manufactured gap-spanning interval rejects.

Let `D_i` be the exact union of the intervals in `C_i`. V3 distinguishes:

- `reference_domain_compatible` when `T_i` is contained in `D_i`;
- `reference_domain_partially_incompatible` for positive-width intersection without containment;
  and
- `reference_domain_incompatible` for zero-width intersection.

Partial and complete incompatibility never clip or replace `T_i`, modify `C_i`, or issue a valid
reference-accuracy result. They retain positive documentary width as a diagnostic and make the
reference intersection non-applicable. Fixed fixtures cover containment within one and across
adjacent intervals; extension before, after, and across both ends; wholly outside; endpoint-only
contact; and included versus excluded dates in a multiple-date domain.

### 3. Replay Route A provenance

`state/NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json` compares receipt source `1c59b8a`,
checkpoint-4 evaluated source `90220a3`, operational source `b3e5314`, Phase-1 source `3c12801`,
and acceptance source `2f707858425cb51f61c5d57e6a0364faf092b841`. Its logical digest is
`9479a5c34a1b2dfa65ba914b64ea30835f5d54383e04bbc2e13bda39e71dbbf7`.

The attestation classifies each changed replay path/function and establishes Route A: the only
post-closure replay-code delta is the fail-closed JSON loader wrapper. Engine invocation, fixture
inputs, event/interval construction, receipt semantics, canonicalization, digest construction,
and independent verification are byte-identical or mechanically equivalent through the
acceptance source. All nine receipts validate; aggregate-only replay reproduces the unchanged
index `f7ead3c9b3b4eb7102cfff5c74e3de3e261e3f6b8491ccfe8881fbf882b75435` and aggregate
`ee8b4882785bb1102b8f14cd23e0d4cc18416118109b0040b8313f86e6be1665`; a changed semantic input
fails the validator.

### 4. Machine-readable acceptance matrix

`state/NATAL-TIME-CHECKPOINT5-ACCEPTANCE-MATRIX.json` contains 81 entries spanning every prior and
current requirement family. Each entry records its requirement ID, exact committed test and
fixture, expected result, actual controlled status/rejection code, receipt or access digest where
applicable, contract version, evaluator-version digest, exact source commit, and acceptance
category.

- Matrix source commit: `da8d3ee5a4208e7e4ffb27daa54affcba4bd9d39`.
- Matrix source tree: `83eedaf647c2d727e735a98827e0d74b053edaf2`.
- Logical matrix digest:
  `71a09f8f12a7e44e5848d3f976ecad1eb4fba6f345b2061fcef65540763220d3`.
- Exact matrix-file SHA-256:
  `6c0c3a4d9ee2c48791b36a457a2bd65a70292c9b020565637e1135b3c9a66d3b`.

The matrix includes Pro's five explicit minima: full-`C_i` unit fractions, reorder equivalence,
repeated-state interval/state-count divergence, access-state binding on every valid receipt, and
rejection of a rehashed forbidden scalar/inferential field. It excludes hidden-reference content,
canonical `T_i` digests, and per-reference custody digests. Its `--validate-only` replay reproduces
from the exact source commit.

## Verification evidence

Verification at implementation-evidence head `067ed6cdd504b368b88c203ca6d058c20b2fb913`:

- full `pytest`: **372 passed** in 48.49 seconds;
- strict mypy across the complete source scope: **success, 132 source files**;
- Ruff check across the checkpoint-5 remediation range `3b80ebbd...HEAD`: **all checks passed**;
- Phase-0 lineage and operational-evidence validators: passed;
- replay-delta attestation validator: passed;
- metric-v3 audit `--check`: passed;
- acceptance-matrix `--validate-only`: passed and reproduced;
- private-artifact/history/build gate from the canonical base: passed;
- protected-core comparison: all 48 qualified protected blobs match checkpoint-3 head `8cc97025`;
- `git diff --check`: passed; and
- worktree: clean.

The exact submission head receives a forced full-test rerun plus the same strict-mypy, Ruff,
artifact, privacy/history/build, diff, protected-blob, and clean-worktree gates after this
documentation-only commit. Those exact final identifiers and results are supplied in the Pro
submission.

The full branch Ruff check has exactly one known import-order finding in protected file
`tests/unit/test_audit_natal_time_foundation_runner.py`. The file is byte-identical to the qualified
checkpoint-3 protected blob, so it was not reformatted. The exact Git-derived post-checkpoint-5
Ruff check is clean. A separate diagnostic Ruff format check found formatting-only differences in
the replay-delta script and its test; lint passes, the acceptance matrix is bound to their exact
source, and no protected or source-bound byte was changed for formatting.

Corrected execution ledger retained for supervision:

- a nonexistent privacy-test path selected zero tests; the correct full privacy/history/build gate
  passed;
- `npm test` was mistakenly invoked in this Python repository and returned `ENOENT`; the correct
  full pytest suite passed;
- a combined-file mypy invocation produced duplicate-module/tooling errors; the repository-
  compatible complete strict source scope and focused strict scopes passed;
- the first matrix replay exposed JSON integer-versus-string mapping-key normalization; the
  generator and validator were corrected before the immutable matrix source commit, and exact
  replay now passes; and
- protected-test formatting appeared transiently in commits `30159af` and `2f70785`; final bytes
  match checkpoint-3 for all 48 files. They are described as byte-identical at reviewed and
  acceptance heads, not as historically untouched.

## Fresh external read-only state

The 2026-08-30 checkpoint-6 refresh made no external changes:

- GitHub still reports public repository `u-dont-existDOTcom/humandesign`, default branch `main`,
  at `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`; main CI run `33283895301` passed.
- Draft PR #1 remains the only open PR, at `3bab2c58f6972b4a66b7b68bb8cde6ba507d64db`,
  merge state `DIRTY`, with its old failing `verify` check. It was not touched.
- Railway production service `relationship-web` is online with active successful deployment
  `60c360b2-6591-4e96-9d82-66e6808f82e5`, one EU West replica, public service domain, and attached
  `relationship-web-data` volume. It still corresponds to merged PR #17 / commit `450d806`, not
  this local natal-time branch.

No secret value, participant record, live study record, Railway setting/variable/data, GitHub
setting, PR, branch, deployment, or volume was read beyond the authorized metadata or changed.

## Requested checkpoint-6 ruling

Please answer first with exactly `OWNER DECISION REQUIRED: YES` or
`OWNER DECISION REQUIRED: NO`, then:

1. qualify or reject each of the four remediation surfaces above;
2. identify any remaining blocking defect with an exact acceptance test;
3. state whether the deterministic/Phase-0 foundation remains qualified; and
4. authorize at most one bounded next slice, preserving every hard prohibition unless explicitly
   and safely superseded.

Successful remediation does not itself authorize inference, push, PR action, merge, migration,
deployment, participant work, public release, or a scientific operating rule.
