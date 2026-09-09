# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-HUMAN-UI-FINAL-SIMPLIFICATION-VERIFIED-2026-09-09.json`
3. `state/LIFE-PATTERNS-HUMAN-UI-IRRELEVANT-RELATION-CONTROL-2026-09-09.md`
4. `state/LIFE-PATTERNS-HUMAN-UI-READABLE-SOURCE-LABELS-VERIFIED-2026-09-09.json`
5. `state/LIFE-PATTERNS-HUMAN-UI-PROVENANCE-SIMPLIFICATION-VERIFIED-2026-09-09.json`
6. `state/LIFE-PATTERNS-HUMAN-UI-REDUNDANT-CITATION-CONTROL-2026-09-09.md`
7. `state/LIFE-PATTERNS-HUMAN-UI-COMPREHENSION-DEFECT-2026-09-09.md`
8. `docs/research/LIFE_PATTERNS_INDEPENDENT_AUDITOR_START_HERE_PLAIN_2026-09-09.md`
9. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
10. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
11. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
12. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
13. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
14. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
15. `state/CURRENT-STATE.md`
16. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 method correction, private v2 freeze, and owner-led human-interface corrections are complete. **The current scientific blocker is the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

## Human UI corrections completed before collection

Owner browser review caught several distinct usability defects before any qualifying first pass. They are now corrected without changing the measurement contract:

- narrator/behavior direction is explicit;
- each unit is one plain behavior question with `Yes — clearly shown`, `No — does not fit`, or `Can't tell`;
- source provenance is bookkeeping, not a second behavioral judgment;
- a single exact source is auto-bound for a Yes answer;
- multiple exact sources are shown as readable `Exact quote N` labels plus the actual quote text;
- opaque source IDs such as `EP-002-SEG-01` remain hidden machine provenance values;
- internal behavior-code IDs are hidden from the human-facing list;
- counterevidence is optional and collapsed;
- influence is optional and scoped only to the selected behavior;
- if exactly one behavioral value is selected, `value_relation = single` is automatic and **no relation dropdown is shown**;
- only after two or more behaviors are selected does the UI ask whether their order is established.

The last item follows the general rule: do not ask a human to choose metadata already determined by the substantive choice they just made.

Final human-interface implementation head:

`67957dacbb7634f6b256459ccbff346d7687c256`

CI `34382061592`: **success — 628 passed, 7 expected skips; Ruff passed; strict mypy passed for 172 source files.**

Public implementation/verification:

- `scripts/build_life_patterns_human_calibration_ui_v2_final.py`
- `tests/unit/test_life_patterns_human_calibration_ui_v2_final.py`
- `state/LIFE-PATTERNS-HUMAN-UI-FINAL-SIMPLIFICATION-VERIFIED-2026-09-09.json`

## Current owner-deliverable private UI and kit

Use only:

- HTML: `Life-Patterns-Human-Calibration-V2-FINAL-2026-09-09.html`
  - 3,998,541 bytes
  - SHA-256 `48911ec2ea028f86e24b06493b54e18feaf5048e5f5540d2e8ef0bd3853f6ee7`
- kit: `Life-Patterns-Independent-Auditor-Kit-V2-FINAL-2026-09-09.zip`
  - 803,222 bytes
  - SHA-256 `da81d8f891671bae8d76672347a8fad969f5931287445019ed55922ca55500c6`

All earlier private auditor kits are superseded for new collection.

The measurement-bearing handoff remains unchanged:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 44 episode + 22 repeated-series units
- historical `LPCA-5B3E6CFCCE49807050DF` selection reused without resampling.

No human labels, automated labels, consensus, or target scoring have been run.

## Exact next gate

Give only the current final private kit to an **eligible independent theory-blind human auditor**. Before and during the first pass, the auditor must not have access to automated labels, automated consensus, target-model outputs/mappings, birth/chart data, expected answers, or AI assistance for coding judgments.

The auditor completes all 66 selected units plus the independence/exposure attestation and returns exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Preserve those raw bytes unchanged. Validate and freeze them before exposing any automated output.

Only after that freeze may the >=3 isolated theory-blind automated development passes begin. Consensus and human-vs-automated comparison come later. Target-model scoring/reveal remains unauthorized.

## Hard boundaries

- do not use any earlier auditor kit for new human collection;
- do not reselect calibration units after seeing evidence just because some unit pairs are negative/inapplicable;
- never reconstruct private source material from summaries or receipts;
- never commit participant narrative or private HTML;
- no automated Life Patterns coding before the human first pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
