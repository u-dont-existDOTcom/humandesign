# Checkpoint-4 operational evidence

`state/NATAL-TIME-CHECKPOINT4-OPERATIONAL-EVIDENCE.json` records the checkpoint-4
nonblocking diagnostics. It is operational evidence only: it does not enter scientific identity
or results, describe Railway or a deployment, establish throughput, or promise future runtime.

The replay index binds engine identity V4, so the artifact repeats its pinned platform, Python,
package, ephemeris, and timezone facts. These are identity-bound runtime context, not live CPU,
memory, load, scheduler, or process telemetry.

The original ext4 files retain observable birth, modification, and status-change timestamps for
nine durable receipts and the final index. The inode-birth span is `1126.967377817` seconds, but
inode birth precedes hard-link publication. A more conservative durable-write lower bound uses
the first receipt's status-change time and final-index modification time: `1126.942930551`
seconds. It excludes all work before the first receipt and cannot distinguish computation,
independent verification, serialization, orchestration, or filesystem overhead. The writer
fsyncs file contents but not the directory, so this is not a sudden-power-loss guarantee. No
defensible end-to-end duration was captured, so none is invented.

The artifact also derives two changed-path manifests directly from Git: checkpoint-4
`8cc97025...90220a3` and Phase-0 closure `90220a3...50118dc`. It stores each complete name-status
manifest, the seven lint-relevant Python paths, and the exact Ruff 0.16.4 command that passed.
The repo-wide diagnostic command still reports 1,812 historical violations and exits nonzero;
that debt is neither hidden nor waived. The independently passing changed-file scopes make a new
lint regression visible. Phase-1 paths are deliberately excluded and must be recorded separately
at checkpoint 5.

Generate once and validate deterministically:

```bash
.venv/bin/python scripts/audit_natal_time_checkpoint4_operational_evidence.py
.venv/bin/python scripts/audit_natal_time_checkpoint4_operational_evidence.py --validate-only
```
