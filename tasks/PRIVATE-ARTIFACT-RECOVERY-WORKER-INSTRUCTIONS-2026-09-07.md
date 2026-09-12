# Private Life Patterns artifact recovery — worker instructions

Use these instructions only in the **old worker/conversation workspace that originally created the private Life Patterns files**. The goal is byte-for-byte recovery and export, not reconstruction.

## Goal

Recover and return to the owner the exact private human-calibration ZIP if it still exists. If the ZIP is gone, recover the two exact private source JSON files and regenerate the ZIP only through the already-frozen repository procedure.

Do not perform any other project work.

## Hard constraints

- Do **not** reconstruct v8/v8.1 from summaries, chat memory, public GitHub receipts, transcript fragments, or handoff prose.
- Do **not** run automated coding, consensus, human-vs-LLM comparison, target-model scoring/reveal, merge, deployment, recruitment/contact, or measurement changes.
- Do **not** overwrite the original private files.
- Do **not** commit private narrative-bearing files to GitHub.
- Do **not** ask the owner questions unless an actual non-recoverable tradeoff appears. Exhaust the search first.

## Expected exact artifacts

Primary target:

`experiments/private/life-patterns/human-calibration-2026-09-06.zip`

Expected ZIP identity:

- bytes: `379729`
- SHA-256: `a5cba3a33f3103ff9e16f4cff6b82a090e8380b837a21852167c47a0a99c83b4`
- members: `15`

Fallback source identities:

### v8

- bytes: `54488`
- SHA-256: `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`

### v8.1

- bytes: `25844`
- SHA-256: `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`

## Required procedure

1. Search the old workspace directly for the primary ZIP path above.
2. If found, compute SHA-256, byte size, and ZIP member count.
3. If all three match, copy/export that **exact ZIP** to a user-accessible attachment/download location and return the file to the owner. Do not regenerate it.
4. If the exact ZIP is not found, search the entire workspace recursively for files matching the exact v8 and v8.1 SHA-256 values. Search by hash, not only filename.
5. If both exact source files are found, preserve them unchanged and use the already-frozen Humandesign repository preparation/export procedure to regenerate the auditor ZIP. Use the frozen source commit/procedure recorded in the repository recovery/preparation receipts; do not invent a new procedure.
6. Verify the regenerated ZIP against the expected ZIP SHA-256 `a5cba3a33f3103ff9e16f4cff6b82a090e8380b837a21852167c47a0a99c83b4`, size `379729`, and 15 members.
7. If the regenerated ZIP matches exactly, export/attach that ZIP to the owner.
8. If the regenerated ZIP does **not** match exactly, do not tweak files, timestamps, ordering, compression, or code ad hoc. Report the mismatch, the exact source hashes found, the produced archive hash/size/member count, and stop.
9. If neither the exact ZIP nor both exact source files can be recovered, report that the frozen v8/v8.1 execution is unrecoverable from this workspace and stop. Do not create substitutes.

## Search guidance

Search likely locations first, then recursively across the worker filesystem/workspace for:

- `human-calibration-2026-09-06.zip`
- `life_patterns_v8_transfer_record.json`
- v8/v8.1 JSON files under `experiments/private/life-patterns/`
- files of approximately 54,488 and 25,844 bytes

For every plausible candidate, verify SHA-256 before treating it as authoritative.

## Success response

If successful, return only the essential result:

- exact artifact recovered or regenerated;
- verified SHA-256, byte size, member count;
- a direct user-accessible file attachment/download link;
- whether recovery came from the original ZIP or from the two exact source files.

Do not merely return the old private filesystem path. The purpose of this task is to **transfer the actual bytes out of the old workspace** so the new Humandesign continuation can use them.

## Canonical GitHub recovery record

Before regenerating from source, read current GitHub state in `u-dont-existDOTcom/humandesign`, branch `codex/discover-life-patterns-mvp`, especially:

- `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-2026-09-07.md`
- `state/life-patterns-development-preparation-2026-09-06/README.md`

Those records define the frozen identities and prohibit reconstruction from summaries.