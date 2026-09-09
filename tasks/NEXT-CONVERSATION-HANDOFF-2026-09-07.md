# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
3. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-HUMAN-FIRST-VERIFIED-2026-09-09.json`
4. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
5. `state/LIFE-PATTERNS-HUMAN-UI-HUMAN-FIRST-CORRECTION-2026-09-09.md`
6. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
7. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
8. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
9. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
10. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
11. `state/CURRENT-STATE.md`
12. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 method correction, private v2 freeze, and pre-collection human-interface audit are complete. **The current scientific blocker is the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

## Human-first calibration transport

Owner browser review established a stronger UI principle than the earlier incremental fixes:

> The auditor should make only judgments that can change the planned calibration. Machine bookkeeping is automatic. A conditionally required judgment appears only when its condition is present. Truly optional auxiliary metadata that is not part of the planned human comparison is not shown.

The current flow therefore behaves as follows:

- one story/pattern source + one plain behavioral question;
- Yes / No / Can't tell;
- if Yes, select behavior(s);
- one selected behavior -> `single` is automatic, no relation control;
- two or more selected behaviors -> first ask whether the story establishes an order;
- only after Yes -> show the selected behaviors **in plain language** and let the auditor arrange them;
- non-action prerequisite checks appear only for selected non-action values;
- Other Specified description appears only when selected;
- repeated-series recurrence/exception questions remain because they are required comparison fields;
- one exact quote -> source provenance auto-bound;
- multiple exact quotes -> actual quote text shown and auditor selects the quote(s) used;
- no human-facing internal Rxx/NBM/source-segment IDs;
- generic influence, counterevidence, context/missingness/language/note fields are absent from the normal human pass and serialize valid defaults automatically;
- validation errors tell the auditor the concrete action required rather than exposing schema terminology.

This is presentation/collection burden only. The exact handoff, response schemas, behavioral values, 44+22 selected units, recurrence semantics, blinding and no-network boundary are unchanged.

## Public implementation

Current final human-first builder:

`scripts/build_life_patterns_human_calibration_ui_v2_auditor_final.py`

Tests:

`tests/unit/test_life_patterns_human_calibration_ui_v2_auditor_final.py`

Implementation/test head:

`3447565cb56d5a6cd39d1a44877b3ca2604fdd1c`

CI `34384054801`: **success — 635 passed, 7 expected skips; Ruff passed; strict mypy passed for 172 source files.**

The later state/policy head `46bb7010cb487d31435702ef4031ac3124d440d5` also passed CI `34384155046`.

## Current owner-deliverable private artifact

Use only:

- HTML: `Life-Patterns-Human-Calibration-V2-AUDITOR-2026-09-09.html`
  - 3,995,302 bytes
  - SHA-256 `7866b98b9aab72a329825675bb037e951354c9093a35b0f218d335ef7a0a8b3e`
- kit: `Life-Patterns-Independent-Auditor-Kit-V2-AUDITOR-2026-09-09.zip`
  - 802,576 bytes
  - SHA-256 `8e97c264045867b69db6a29af21cde8b2f3d5e3587a852b802504a38a0de1673`
  - two members: HTML + `START-HERE.md`.

All earlier auditor kits are superseded for new collection.

The measurement-bearing private handoff remains:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 44 episode + 22 repeated-series units
- historical `LPCA-5B3E6CFCCE49807050DF` selection reused without resampling.

Exact private Chromium smoke passed with 66 units, zero network/page/console errors, correct conditional ordering, plain order labels, automatic sole-source provenance, readable multi-source quote selection, hidden auxiliary fields and human-readable non-action errors.

## Exact next gate

Give only the current human-first kit to an eligible independent theory-blind auditor. They complete all 66 units plus the independence/exposure attestation without access to automated labels/consensus, target-model outputs/mappings, birth/chart data, expected answers, or AI assistance for coding judgments.

They return exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Preserve those exact bytes, validate and freeze them, and only then start >=3 isolated theory-blind automated coding passes.

## Hard boundaries

- do not use any earlier auditor kit for new collection;
- do not reselect calibration units because some story/observable pairs are negative or inapplicable;
- never reconstruct private source material from summaries or receipts;
- never commit participant narrative or private HTML;
- no automated Life Patterns coding before the human first pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
