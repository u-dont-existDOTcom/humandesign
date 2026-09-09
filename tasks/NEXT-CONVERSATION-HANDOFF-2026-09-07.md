# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-HUMAN-UI-DIRECT-CHOICE-CORRECTION-2026-09-09.md`
3. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-DIRECT-CHOICE-VERIFIED-2026-09-09.json`
4. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
5. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
6. `state/LIFE-PATTERNS-HUMAN-UI-HUMAN-FIRST-CORRECTION-2026-09-09.md`
7. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
8. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
9. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
10. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
11. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
12. `state/CURRENT-STATE.md`
13. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 correction, private v2 freeze, and the owner-led human-interface audit are complete through the latest **direct-choice** correction. **The current scientific blocker is still the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

## Direct-choice human task

The latest owner review identified that asking **“Enough information to code?”** before showing the behavioral values was still backwards: a human cannot judge information sufficiency for an unspecified downstream choice.

The current UI therefore asks the substantive question directly:

> **Which behavior or behaviors does the exact source clearly show?**

The concrete plain-language behavior choices are visible immediately.

Machine-facing state is derived from that substantive answer:

- one or more selected behaviors -> `observed`;
- **Doesn't apply to this story** -> `not_applicable`;
- **Not enough information** -> `insufficient`.

There is no generic `Partially` state because partial evidence can mean different things:

- a clearly supported subset of listed behaviors -> select those behaviors;
- several clearly observed behaviors -> select several, then answer the conditional order question;
- incomplete/unclear evidence that does not permit a reliable behavior choice -> Not enough information;
- absent prerequisite situation -> Doesn't apply.

This is presentation/control-flow only. The exact handoff, response schemas, behavioral values, selected 44+22 units, recurrence semantics, blinding, calibration selection and no-network boundary are unchanged.

## Human-first interaction rules still controlling

- one selected behavior -> `single` is automatic;
- multiple selected behaviors -> first ask whether the story establishes an order;
- only if order is established -> show the selected behaviors in plain language and let the auditor arrange them;
- non-action prerequisite checks appear only for selected non-action values;
- Other Specified description appears only when selected;
- repeated-series recurrence/exception questions remain because they are required comparison fields;
- one exact quote -> source provenance automatic;
- multiple exact quotes -> show actual quote text and ask which were relied on;
- no human-facing Rxx/NBM/source-segment IDs;
- generic optional influence, counterevidence, context/missingness/language/note fields are absent from the normal human pass;
- validation errors tell the auditor what concrete action to take.

## Public implementation

Direct-choice builder:

`scripts/build_life_patterns_human_calibration_ui_v2_direct_choice.py`

Tests:

`tests/unit/test_life_patterns_human_calibration_ui_v2_direct_choice.py`

Implementation/test head:

`196b37e8369c9493380393b506eaa9f9d0bebedc`

CI `34398433777`: **success — 645 passed, 7 expected skips; Ruff passed; strict mypy passed for 172 source files.**

Public-safe verification receipt:

`state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-DIRECT-CHOICE-VERIFIED-2026-09-09.json`

## Current owner-review private artifact

Use only:

- HTML: `Life-Patterns-Human-Calibration-V2-DIRECT-CHOICE-2026-09-09.html`
  - 3,996,334 bytes
  - SHA-256 `2fadb3c827379efc3ec0988be43ffff4f5e4708d91a7f7a9c48dc25a391ad4b5`
- kit: `Life-Patterns-Independent-Auditor-Kit-V2-DIRECT-CHOICE-2026-09-09.zip`
  - 802,612 bytes
  - SHA-256 `2dfc836fa2d7757e904ed593efba51baba22fefd9a9bf3ccfb209b80ef44c5e4`
  - two members: private HTML + `START-HERE.md`.

All earlier auditor kits are superseded for new collection.

Exact private Chromium smoke on the current HTML confirmed:

- `Bundle verified`;
- direct behavior question visible;
- meta “Enough information to code” wording absent;
- behavior choices visible immediately;
- two fallback choices visible;
- selecting a behavior clears any fallback choice;
- zero external network requests;
- zero page errors;
- zero console errors.

## Exact next gate

Continue owner review of the current direct-choice artifact until accepted. Then give only that current kit to an eligible independent theory-blind auditor.

The auditor completes all 44 episode + 22 repeated-series units plus the independence/exposure attestation without access to automated labels/consensus, target-model outputs/mappings, birth/chart data, expected answers, or AI assistance for coding judgments.

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
