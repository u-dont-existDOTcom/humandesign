# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before doing any substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
3. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-VERIFIED-2026-09-08.json`
4. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_V2_2026-09-08.md`
5. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_REQUIREMENTS_2026-09-08.md`
6. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
7. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
8. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
9. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_PRIOR_WORK_SCAN_2026-09-08.md`
10. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
11. `state/CURRENT-STATE.md`
12. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The earlier recovery, recurrence-method revision, private-v2-freeze and offline-UI implementation gates are now complete at the engineering/artifact level.

### Recurrence-corrected method

Pinned substantive method implementation head:

`7b689f3adb49da599abb40ec2bff27ad97d3887f`

CI `34271174611`: success.

The new additive v2 path preserves historical v1 artifacts while correcting the episode-centric recurrence defect. Generalized behavioral self-report is direct **reported recurrence** evidence; a self-selected confirming anecdote is not independent frequency evidence. Exceptions, recurrence strength and evidence basis remain distinct. No target-model information was used to make this revision.

### Exact private v2 freeze

The owner reuploaded the generated recurrence-corrected private handoff, and the continuation independently reverified it before UI work.

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- owner-reuploaded transport ZIP: 422,297 bytes; SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`; 15 members
- reused historical calibration: `LPCA-5B3E6CFCCE49807050DF`
- selected units: 44 episode + 22 series
- selection reused without resampling
- no human labels, automated labels, consensus or target scoring exist.

No private participant text or private handoff bytes are committed.

### Offline human calibration UI

A standalone local/offline annotation interface is implemented and reproducible from the verified private handoff.

Committed source/test components:

- `scripts/build_life_patterns_human_calibration_ui_v2.py`
- `scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`
- `tests/unit/test_life_patterns_human_calibration_ui_v2.py`

Implementation/test-bearing head:

`aba22fe18f65dcf7cb3f67b494b9cc343b0c752e`

CI `34290496491`: success — 605 passed, 7 expected skips, Ruff passed, strict mypy passed for 171 source files.

The exact private HTML produced from the owner-reuploaded handoff is:

- filename: `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- bytes: 3,980,290
- SHA-256: `63baa191a93c49cbdfb459d4d5e3f96ff541bdddc3dd2183e5af743f48ce987b`

That HTML embeds private participant evidence and must remain private/offline; it is not committed.

The UI re-verifies the handoff before displaying evidence, presents one selected unit at a time, exposes only theory-neutral measurement material, blocks invalid response combinations, has no AI/network dependency, supports bound progress save/reload, collects the blinding attestation without favorable defaults, and exports exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

## Exact next gate

A **real normal-browser visual/interaction smoke pass** is still required before asking an external independent auditor to use the UI. The continuation environment's Chromium runtime hung even on an empty page, so browser usability is explicitly **unverified**, not inferred from static tests.

Bounded smoke criteria:

1. open the exact private standalone HTML locally;
2. confirm its integrity verification succeeds and the first evidence unit renders;
3. navigate between units and inspect exact source + observable content;
4. save one valid response, download progress, reload that progress and confirm the saved response returns;
5. verify the final attestation/export controls are present;
6. confirm the browser does not make external network requests.

If that passes, the exact same private UI may be given to an **independent theory-blind human auditor**. The participant/theory-exposed owner cannot serve as the independent benchmark, though a separately identified owner sensitivity coding remains possible.

The independent auditor must complete and freeze all 44 episode + 22 series units plus the v2 attestation **before seeing any automated output**.

Only after that human first pass is frozen may the >=3 isolated automated development passes begin. Consensus and human-vs-automated comparison come later. Target-model scoring/reveal remains unauthorized.

## Hard boundaries

- never reconstruct private source material from summaries, receipts, memory or transcript fragments;
- never commit participant narrative or the private standalone HTML;
- no merge/deploy;
- no participant/auditor recruitment or contact without separate authorization;
- no spending;
- no automated Life Patterns coding before the human first pass is frozen;
- no target-model scoring/reveal.
