# Natal-time checkpoint-5 acceptance matrix

Status: generator and requirement inventory only. The final state artifact is
intentionally not generated until the separated reference-custody bundle,
receipts, evaluator source, and focused tests are committed at one exact source
commit.

## Purpose and boundary

`scripts/audit_natal_time_checkpoint5_acceptance_matrix.py` maps the prior and
current ChatGPT Pro acceptance rules to exact test, fixture, expected outcome,
controlled status/code, code, digest, contract, evaluator, source, and category
evidence. The inventory covers checkpoints 1 through 5 and gives separate
entries to every checkpoint-5 custody probe, disconnected-subset case, and
three-way reference-domain case. It also gives explicit entries to Pro's five
minimum demonstrations:

- full-`C_i` unit fractions;
- canonical reorder equivalence;
- repeated-state interval/state-count divergence;
- access-state binding on every valid receipt; and
- rejection of a rehash-added forbidden scalar or inferential field.

This is a synthetic, local evaluation-control artifact. It does not select
`S_i`, execute a baseline, make a human-validity or rectification-accuracy
claim, authorize participant inference, or authorize release or deployment.

## Exact-source and custody design

The generator reads every input with `git show <source>:<path>`. It therefore
cannot finalize from working-tree-only custody output. The exact source commit
and tree OID, checkpoint documents, contract bytes, test blobs, code blobs,
split schemas/manifests, inference-visible fixture digests, receipt digests,
access-state digests, and evaluator source/version digest are bound dynamically.

The matrix deliberately excludes evaluator-only reference bytes, canonical
`T_i` digests, direct per-fixture reference-custody digests, reference paths,
and combined fixture digests. Per-fixture digest evidence is typed as `applicable` or
`not_applicable`; an applicable digest must be a lowercase SHA-256 value and a
non-applicable digest must be null.

The saved matrix is self-hashed over canonical JSON excluding only its
`matrix_sha256` field. Validation rebuilds the matrix from its embedded exact
source commit and requires byte-equivalent content.

## Strict finalization gates

Final generation fails closed if any of the following is true:

- a separated schema, manifest, fixture, or receipt is absent from the exact
  source commit;
- a schema, manifest, contract, fixture-file, receipt-file, or receipt
  self-hash differs;
- split manifest fixture sets or counts disagree;
- V1, V2, or operative V3 contract digests differ;
- the evaluator version does not bind the exact committed evaluator sources;
- a mapped test or code symbol is absent from the source commit;
- a required fixture, receipt kind, controlled rejection code, metric
  invariant, or access binding differs;
- a requirement ID is missing/duplicated or an acceptance category is unknown;
- any custody-dependent field remains pending; or
- forbidden evaluator-only reference material appears in the matrix.

## Final artifact workflow

After the custody integration owner commits the final evaluator, split bundle,
receipts, and tests, build from that exact clean source commit:

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint5_acceptance_matrix.py \
  --source-commit <full-40-hex-source-commit>
```

The expected new artifact path is:

`state/NATAL-TIME-CHECKPOINT5-ACCEPTANCE-MATRIX.json`

Validate a saved artifact by reproducing it from its embedded source commit:

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint5_acceptance_matrix.py \
  --validate-only
```

The final checkpoint packet must separately record the exact-head test, strict
mypy, changed-file Ruff, privacy/history/build, protected-blob, and clean-tree
gates. The matrix binds their test and source definitions; it does not invent a
test-run receipt or claim that an unrecorded command ran.

## Values that remain intentionally dynamic

No placeholder values are emitted. These fields are resolved only from the
final committed custody source:

- exact source commit and tree OID;
- evaluator source blobs and evaluator-version digest;
- inference/evaluator schema and split-manifest digests;
- inference-visible fixture and receipt sets/counts/digests;
- access-state digests and actual controlled receipt statuses/codes;
- final test/code blob OIDs; and
- entry coverage summary and final matrix digest.

The earlier combined V1 fixture/manifest digests are not carried forward as
custody evidence.
