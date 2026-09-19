# Life Patterns v2 — working-ledger audit checkpoint distinction — 2026-09-16

## Owner correction

The owner clarified that preserving the hidden ledger is primarily valuable because it allows the current extraction/reasoning state to be audited after a product failure. Preserving a ledger snapshot must **not** imply that the ledger is already correct, canonical, scientifically valid, or ready to score.

## Failure mechanism

The first exact-recovery implementation conflated two separate properties:

1. **recovery exactness** — can the same working state be reconstructed after a restart?;
2. **scientific validity** — has that working ledger survived participant correction, semantic validation, and the later freeze boundary?

An exact copy of a defective ledger is still defective. Exact preservation is evidence retention, not validation.

## Repair

The browser-local automatic snapshot remains because it prevents the evidence needed for debugging/audit from disappearing during development. It remains local to the participant browser; the development service does not durably persist private interview narrative on Railway or Git.

However, the snapshot is now explicitly marked:

- `snapshot_role = unvalidated_working_audit_checkpoint`;
- `canonical_measurement = false`;
- `scientific_freeze = false`;
- recovery status `working_ledger_validation_status = unvalidated`;
- `requires_audit_before_scientific_use = true`;
- `scientific_freeze_eligible = false`.

The participant-facing controls are renamed **Download audit/recovery snapshot** and **Import audit/recovery snapshot**. Copy explicitly states that the snapshot may itself contain ledger mistakes and that exact restoration does not certify correctness.

## Intended use

- Automatic browser checkpoint: prevent data loss and preserve exact defective state for audit if a failure occurs.
- Download/upload snapshot: allow supervising Chat to inspect the actual hidden ledger and diagnose extraction/provenance/semantic defects rather than reconstructing them from visible prose.
- Import snapshot: resume the exact working development state after infrastructure loss.
- Scientific freeze: remains a distinct later boundary; an audit/recovery snapshot does not become a scientific measurement merely because it is exact or resumable.

## Privacy boundary

No automatic Git or durable Railway storage of private owner interview narrative is introduced. Browser-local persistence remains the default recovery mechanism.
