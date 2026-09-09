# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
3. `state/LIFE-PATTERNS-HUMAN-UI-COMPREHENSION-DEFECT-2026-09-09.md`
4. `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-PLAIN-VERIFIED-2026-09-09.json`
5. `state/LIFE-PATTERNS-INDEPENDENT-AUDITOR-PLAIN-KIT-RECEIPT-2026-09-09.json`
6. `docs/research/LIFE_PATTERNS_INDEPENDENT_AUDITOR_START_HERE_PLAIN_2026-09-09.md`
7. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
8. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
9. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
10. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
11. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
12. `state/CURRENT-STATE.md`
13. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 method correction, private v2 freeze, and human-facing transport correction are complete. **The current scientific blocker is the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

## Owner-identified UI defect — resolved before human collection

Owner browser review of the earlier auditor kit showed that the UI exposed machine/codebook semantics instead of an intelligible human task. The decisive example paired a story where the narrator offered help to another person with `NBM-R16 — Help seeking/use`; the old screen did not plainly say that R16 asks whether the **narrator sought, accepted, declined, delegated to, or used somebody else's help for the narrator's own need**. `Supporting` and `Narrator influence / precedence` were also underspecified.

All earlier auditor kits are superseded for new human collection.

The new presentation layer:

- asks one ordinary-language behavior question per story/unit;
- explicitly defines narrator direction;
- says story/question pairs do not have to match;
- renders states as `Yes — clearly shown`, `No — does not fit`, and `Can't tell` while exporting the same frozen values;
- for R16 explicitly distinguishes seeking/using help from offering help;
- labels source citation as `Use this quote as evidence for the behavior I selected`;
- exposes influence only as optional metadata scoped to the selected behavior;
- collapses formal rules and advanced metadata unless needed;
- preserves the exact embedded private handoff, 44+22 units, response contracts, recurrence semantics and no-network/no-AI boundary.

Public implementation/test head:

`5583e4241f6c5146127db3100c59b2366e2a939a`

CI `34370038001`: **success — 617 passed, 7 expected skips; Ruff passed; strict mypy passed for 172 source files.**

## Current private human UI and delivery kit

Private plain HTML:

- delivery filename: `Life-Patterns-Human-Calibration-V2-PLAIN.html`
- bytes: `3,995,747`
- SHA-256: `5d064760d05c1ba7e04bef5eb4469f258eb448b15e4870fbd065a62a7c9384bb`

Current private auditor kit:

- filename: `Life-Patterns-Independent-Auditor-Kit-V2-PLAIN-2026-09-09.zip`
- bytes: `803,546`
- SHA-256: `1375a70fa6387e71f2402888d6b17e298c234f11b5c127da49d7f3cb969c6b49`
- members: the exact private plain HTML + `START-HERE.md`.

Public-safe receipt:

`state/LIFE-PATTERNS-INDEPENDENT-AUDITOR-PLAIN-KIT-RECEIPT-2026-09-09.json`

Focused browser verification on the exact HTML confirmed bundle verification, R16 help-direction clarity, No-path field suppression, scoped Yes-path citations/influence, humanized series recurrence controls, progress save/download/reload, fail-closed incomplete final export, and zero network requests/page errors.

The measurement-bearing handoff remains:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 44 episode + 22 repeated-series units
- historical `LPCA-5B3E6CFCCE49807050DF` selection reused without resampling.

## Exact next gate

Give the current plain-language private kit to an **eligible independent theory-blind human auditor**. The participant/theory-exposed owner cannot serve as the independent benchmark, though a separately identified sensitivity coding is possible.

Before and during the first pass, the auditor must not have access to automated labels, automated consensus, target-model outputs/mappings, birth/chart data, expected answers, or AI assistance for coding judgments.

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
