# Checkpoint-4 Phase-0 corrections — lineage and replay-source proof

This packet implements only checkpoint-4 corrections 2.1 and 2.2. It does not change the
qualified chart engine, enumerator, adapter, evidence state machine, identity specification,
fixture artifact, result semantics, or replay receipts.

`state/NATAL-TIME-CHECKPOINT4-LINEAGE-ATTESTATION.json` binds the exact evaluated head
`90220a3d67e847d883b2060fa3578fe5026cc414` to the audited main baseline, the exact
checkpoint-3 reviewed head, the doc-only checkpoint-3 ruling commit, and the clean source commit
used by the local real-engine replay. It records every ordered commit and parent from the reviewed
head through the evaluated head, every anchor tree OID, all four required diff surfaces with
machine-readable name-status and statistics, complete diff digests, ancestry, absence of merge
commits, and byte/hash identity for the protected deterministic surface.

`state/NATAL-TIME-REPLAY-SOURCE-MANIFEST-V1.json` derives the local real-engine replay's transitive
repository-local Python import closure (including implicit package initializers) from Git objects,
adds its lock/config/frozen inputs, and requires every byte and Git blob to match between replay
source `1c59b8a...` and evaluated head `90220a3...`. The complete 12-path source-to-evaluated diff
is allowlisted explicitly; it contains only the produced replay artifacts, recovery documentation,
and a test-only aggregate check.
The manifest then verifies all nine committed receipts and rebuilds the committed aggregate and
index hashes without transition recomputation, requiring the checkpoint-4 expected index hash
`f7ead3c9...b75435` and aggregate hash `ee8b4882...e1665` exactly.

Generate once from the exact Git objects:

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint4_phase0.py
```

Validate the saved artifacts deterministically:

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint4_phase0.py --validate-only
```

Both JSON artifacts are canonical, newline-terminated, and content-hashed. The validator fails
closed on an unrecognized difference, changed import closure, replay-affecting byte mismatch,
invalid protected artifact hash, lineage/topology mismatch, receipt tamper, missing or extra
receipt, or aggregate mismatch.
