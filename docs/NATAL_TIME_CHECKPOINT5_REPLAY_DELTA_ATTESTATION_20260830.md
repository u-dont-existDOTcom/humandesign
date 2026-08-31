# Checkpoint-5 post-closure replay-delta attestation

`state/NATAL-TIME-CHECKPOINT5-REPLAY-DELTA-ATTESTATION.json` compares the exact receipt source
`1c59b8a`, checkpoint-4 evaluated source `90220a3`, operational source `b3e5314`, Phase-1 source
`3c12801`, and acceptance source `2f707858`.

Route A is established mechanically. The complete prior replay import/input inventory is
byte-identical across all five sources except `src/hdmatch/natal_time/replay.py`. AST comparison
finds exactly one changed definition: `_load_json_object`. Its valid-JSON path normalizes to the
same AST; the change only converts JSON-decode, Unicode-decode, and filesystem read failures into
the existing fail-closed `ReplayValidationError`. No engine invocation, fixture input,
event/interval construction, receipt semantic field, canonicalization, digest construction, or
independent-verification function changed.

The attestation classifies every pairwise changed path using the checkpoint-5 categories, binds
the complete replay-affecting path inventory, and records AST hashes for the scientific and
receipt-semantic surfaces. All nine original receipt bytes are then passed through the exact
acceptance-source `_validate_receipt` implementation. Its aggregate builder reproduces index
`f7ead3c9...b75435` and aggregate `ee8b4882...e1665` exactly. A fixture-input mutation is rehashed
to bypass the receipt self-hash check and is still rejected at the semantic binding.

No receipt was regenerated or relabeled. Route B remains mandatory for any future
receipt-semantic change.

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint5_replay_delta.py
.venv/bin/python scripts/audit_natal_time_checkpoint5_replay_delta.py --validate-only
```
