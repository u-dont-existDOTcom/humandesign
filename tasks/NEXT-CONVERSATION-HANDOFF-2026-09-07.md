# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before doing any substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-2026-09-07.md`
2. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
3. `tasks/ACTIVE-TASK.json`
4. `tasks/LIFE-PATTERNS-HUMAN-HANDOFF-REGEN-WORKER-2026-09-07.md`
5. `state/CURRENT-STATE.md`
6. `state/life-patterns-development-preparation-2026-09-06/README.md`
7. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

The earlier private-continuity blocker is **scientifically resolved at the source level**: on 2026-09-07 the owner supplied a private recovery archive containing both exact source JSONs, and both independently matched the previously committed byte sizes, SHA-256 identities and schema versions. The public-safe verification receipt is item 2 above. No participant narrative was committed.

This does **not** mean a fresh runtime automatically has the private bytes. Before regenerating or using narrative-bearing material, reacquire the exact private recovery archive/source files from the owner-accessible attachment/File Library and verify:

- v8: 54,488 bytes; SHA-256 `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637`
- v8.1: 25,844 bytes; SHA-256 `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7`

Do not reconstruct either source from summaries, memories, public receipts or transcript fragments.

The repository now provides a fail-closed deterministic recovery helper:

`scripts/regenerate_life_patterns_human_calibration_from_recovery.py`

and bounded execution instructions:

`tasks/LIFE-PATTERNS-HUMAN-HANDOFF-REGEN-WORKER-2026-09-07.md`

If the original exact human-calibration ZIP is unavailable, use only those exact recovered source bytes with that helper. It replays the already-frozen preparation/export procedure with the original source-commit/timestamp binding and fails unless it reproduces the frozen package/calibration identities, all committed internal handoff file hashes, the byte-identical handoff receipt, and the exact 44 episode + 22 series selection. The new outer ZIP is only a transport container and need not reproduce the lost historical ZIP's metadata/compression hash. Do not tweak selection, packet content, measurement definitions, archive metadata, or labels to force agreement.

The current handoff step 5 has two remaining substeps, in order:

1. regenerate and verify the private human-calibration handoff in an execution environment, returning the actual private auditor ZIP to the owner and committing only a public-safe regeneration receipt;
2. obtain and freeze an **independent blind human first pass** plus actual exposure/independence attestation before any automated-label exposure.

Blank forms are not annotations. The independent human codes Life Patterns neutral behavioral evidence; they are not auditing Survey-v2 answers or Survey-v2 scoring.

Only after the human first pass is frozen may handoff steps 6 onward proceed: at least three isolated automated passes per stratum, separate deterministic consensus, comparison with the already-frozen human pass, theory-blind retain/revise decision, and a separately frozen validation route if justified.

Do not merge, deploy, contact/recruit participants or auditors, spend money, run automated coding before the human gate, run target-model scoring/reveal, or alter the frozen measurement chain unless separately authorized.
