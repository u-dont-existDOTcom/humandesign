# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before doing any substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-2026-09-07.md`
2. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
3. `state/LIFE-PATTERNS-HUMAN-HANDOFF-REGENERATION-VERIFIED-2026-09-08.json`
4. `tasks/ACTIVE-TASK.json`
5. `tasks/LIFE-PATTERNS-HUMAN-HANDOFF-REGEN-WORKER-2026-09-07.md`
6. `state/CURRENT-STATE.md`
7. `state/life-patterns-development-preparation-2026-09-06/README.md`
8. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

The earlier private-continuity blocker is **scientifically resolved**. On 2026-09-07 the owner supplied a private recovery archive containing both exact source JSONs, and both independently matched the previously committed byte sizes, SHA-256 identities and schema versions. On 2026-09-08 the deterministic recovery helper regenerated the private human-calibration handoff and verified the frozen package/calibration identities, the exact 44 episode + 22 series selection, the byte-identical handoff receipt, and every internal file against the committed hashes. The new outer transport ZIP has SHA-256 `8ff24ea90e06b393f50761a3a2317f831d3bc0f6dda30e91c20965fa1c1f6d5a`, is 378,206 bytes, and contains 15 members. The public-safe verification receipts are items 2 and 3 above. No participant narrative was committed.

This does **not** mean a fresh runtime automatically has the private bytes. Before using narrative-bearing material, reacquire either the regenerated private handoff matching the new transport identity above or the exact private recovery archive/source files from the owner-accessible attachment/File Library. If regeneration is ever necessary again, verify:

- v8: 54,488 bytes; SHA-256 `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`
- v8.1: 25,844 bytes; SHA-256 `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`

Do not reconstruct either source from summaries, memories, public receipts or transcript fragments.

The repository provides the fail-closed deterministic recovery helper used for the completed regeneration:

`scripts/regenerate_life_patterns_human_calibration_from_recovery.py`

and bounded execution instructions:

`tasks/LIFE-PATTERNS-HUMAN-HANDOFF-REGEN-WORKER-2026-09-07.md`

If the regenerated private handoff is unavailable in a future runtime, use only those exact recovered source bytes with that helper. It replays the already-frozen preparation/export procedure with the original source-commit/timestamp binding and fails unless it reproduces the frozen package/calibration identities, all committed internal handoff file hashes, the byte-identical handoff receipt, and the exact 44 episode + 22 series selection. A regenerated outer ZIP is only a transport container and need not reproduce the lost historical ZIP's metadata/compression hash. Do not tweak selection, packet content, measurement definitions, archive metadata, or labels to force agreement.

The recovery/regeneration portion of handoff step 5 is complete. Its sole remaining substep is to obtain and freeze an **independent blind human first pass** plus actual exposure/independence attestation before any automated-label exposure.

Blank forms are not annotations. The independent human codes Life Patterns neutral behavioral evidence; they are not auditing Survey-v2 answers or Survey-v2 scoring.

Only after the human first pass is frozen may handoff steps 6 onward proceed: at least three isolated automated passes per stratum, separate deterministic consensus, comparison with the already-frozen human pass, theory-blind retain/revise decision, and a separately frozen validation route if justified.

Do not merge, deploy, contact/recruit participants or auditors, spend money, run automated coding before the human gate, run target-model scoring/reveal, or alter the frozen measurement chain unless separately authorized.
