# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
3. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
4. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-VERIFIED-2026-09-08.json`
5. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-BROWSER-SMOKE-2026-09-09.json`
6. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_V2_2026-09-08.md`
7. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_UI_REQUIREMENTS_2026-09-08.md`
8. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
9. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
10. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
11. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_PRIOR_WORK_SCAN_2026-09-08.md`
12. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
13. `state/CURRENT-STATE.md`
14. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

Recovery, recurrence-method correction, the exact private recurrence-v2 freeze, and the human-facing offline UI gate are complete. **The current scientific blocker is the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

### Recurrence-corrected method

Pinned substantive method head:

`7b689f3adb49da599abb40ec2bff27ad97d3887f`

CI `34271174611`: success.

The additive v2 method preserves historical v1 artifacts while correcting the episode-centric recurrence defect:

- generalized behavioral self-report is direct **reported recurrence** evidence;
- a confirming anecdote selected after the recurrence claim is not independent frequency evidence;
- recurrence strength, exception status/frequency, and evidence basis remain separate;
- no fake numerical occurrence floor is required for generalized recurrence language;
- no target-model information was used to make the revision.

### Exact private v2 freeze

Verified private identities:

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- owner-reuploaded transport ZIP: 422,297 bytes; SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`; 15 members
- historical calibration selection reused exactly: `LPCA-5B3E6CFCCE49807050DF`
- selected units: 44 episode + 22 repeated-series units
- no resampling
- no human labels, automated labels, consensus, or target scoring.

No private participant text or private handoff bytes are committed.

### Offline human calibration UI — gate closed

Base UI components:

- `scripts/build_life_patterns_human_calibration_ui_v2.py`
- `scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`
- `tests/unit/test_life_patterns_human_calibration_ui_v2.py`

Portable local-crypto layer:

- `scripts/build_life_patterns_human_calibration_ui_v2_portable.py`
- `tests/unit/test_life_patterns_human_calibration_ui_v2_portability.py`

Portable implementation/test head:

`878ffb21d964a643acd04056f14064f323de0545`

CI `34302364461`: **success — 608 passed, 7 expected skips; Ruff passed; strict mypy passed for 171 source files.**

The exact private portable standalone HTML is:

- filename: `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- bytes: 3,982,068
- SHA-256: `66fda4ceada51b4f82fe2c7f8a93c6d9efe886e1063a9d23fece88b79f1f6690`

It embeds private participant evidence and must remain private/offline; it is not committed. Native WebCrypto is preferred; a self-contained pure-JavaScript SHA-256 fallback preserves local content-address verification when WebCrypto is unavailable. This changes no measurement or response semantics.

A Chromium render/interaction smoke passed on those exact HTML bytes. The UI:

- cryptographically verified `LPHB2-F34245FAE32B513DDCFE` before showing evidence;
- rendered the first episode and exact participant source;
- navigated to repeated-series evidence;
- exposed the recurrence-v2 fields when `Observed` was selected;
- saved one explicitly temporary smoke response, downloaded progress, reloaded it, and restored state;
- failed closed when final export was attempted without all 66 units and a valid attestation;
- made **zero network requests**;
- produced zero page errors and zero console errors.

The temporary smoke response was not a research annotation and was never submitted or committed. Container policy blocks `file://`/HTTP navigation, so the exact bytes were loaded into Chromium via `page.set_content`; the auditor should simply confirm the private file opens normally on their own browser before beginning.

## Exact next gate — independent human first pass

Give the exact verified private standalone HTML to an **eligible independent theory-blind human auditor**. The participant/theory-exposed owner cannot serve as the independent benchmark, although a separately identified owner sensitivity pass remains possible.

Before beginning, the auditor should confirm the file opens normally. During the first pass they must not have access to:

- automated coder labels;
- automated consensus;
- target-model outputs or mappings;
- birth/chart data;
- expected answers.

The auditor must complete all **44 episode + 22 repeated-series units** and the independence/exposure attestation. The UI exports exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Preserve those exact raw exports unchanged. Validate and freeze them with the v2 first-pass/attestation validators before exposing any automated output.

Only after the independent human first pass is frozen may the >=3 isolated theory-blind automated development passes begin. Consensus and human-vs-automated comparison come later. Target-model scoring/reveal remains unauthorized.

## Hard boundaries

- never reconstruct private source material from summaries, receipts, memory, or transcript fragments;
- never commit participant narrative or the private standalone HTML;
- no merge/deploy;
- no assistant-initiated participant/auditor recruitment or contact without separate authorization;
- no spending;
- no automated Life Patterns coding before the human first pass is frozen;
- no target-model scoring/reveal.
