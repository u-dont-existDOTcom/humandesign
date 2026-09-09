# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-HUMAN-UI-PROVENANCE-SIMPLIFICATION-VERIFIED-2026-09-09.json`
3. `state/LIFE-PATTERNS-HUMAN-UI-REDUNDANT-CITATION-CONTROL-2026-09-09.md`
4. `state/LIFE-PATTERNS-HUMAN-UI-COMPREHENSION-DEFECT-2026-09-09.md`
5. `docs/research/LIFE_PATTERNS_INDEPENDENT_AUDITOR_START_HERE_PLAIN_2026-09-09.md`
6. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-09.md`
7. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
8. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
9. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
10. `state/LIFE-PATTERNS-RECURRENCE-EVIDENCE-CORRECTION-2026-09-08.md`
11. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
12. `state/CURRENT-STATE.md`
13. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 method correction, private v2 freeze, and both human-facing transport corrections are complete. **The current scientific blocker is the independent theory-blind human first pass.** No automated Life Patterns coding may start before that pass is frozen.

## Human UI corrections completed before collection

Owner browser review caught two independent usability defects before any qualifying human first pass:

1. the first plain UI did not make the narrator/behavior direction sufficiently explicit and exposed machine-oriented influence/source labels;
2. after a Yes answer it still presented source provenance as a redundant second behavioral question (`Use this quote as evidence...` / `This quote qualifies...`).

Both are now corrected in presentation-only layers. The current UI:

- asks one ordinary-language behavior question per selected story/unit;
- explicitly defines narrator direction and says story/question pairs do not have to match;
- uses `Yes — clearly shown`, `No — does not fit`, and `Can't tell` while exporting the same frozen states;
- clarifies directional observables such as R16 help-seeking/use;
- treats source citation as provenance rather than another substantive judgment;
- for a **single exact source segment**, automatically binds that segment as supporting provenance for a Yes answer with no visible citation checkbox;
- for **multiple exact source segments**, asks only `Which quote(s) show the behavior you selected?`;
- moves counterevidence into an optional collapsed exception/conflict control;
- shows no source-citation controls for No / Can't-tell answers;
- keeps influence optional and scoped only to the selected behavior;
- preserves the exact embedded private handoff, 44+22 selected units, response contracts, recurrence semantics, blinding, and no-network/no-AI boundary.

Public provenance-simplification implementation head:

`3ec4b9dc95f80fee46a4a44d9e052e03088c303a`

CI `34373413686`: **success — 622 passed, 7 expected skips; Ruff passed; strict mypy passed for 172 source files.**

## Current private human UI and delivery kit

Current private delivery HTML:

- filename inside kit: `Life-Patterns-Human-Calibration-V2-PLAIN.html`
- bytes: `3,997,285`
- SHA-256: `0d123b0eca37988157282f9b70f0030e7af106e33155e04b30ffe76f68eff568`

Current private auditor kit:

- filename: `Life-Patterns-Independent-Auditor-Kit-V2-PLAIN-PROVENANCE-2026-09-09.zip`
- bytes: `804,132`
- SHA-256: `291ffaa9bf886e6fe4bcf778b2d41264275bc3b74c11ce82d1df24894bf768d3`
- members: exact private HTML + current `START-HERE.md`.

Public-safe verification receipt:

`state/LIFE-PATTERNS-HUMAN-UI-PROVENANCE-SIMPLIFICATION-VERIFIED-2026-09-09.json`

Exact browser smoke on those private HTML bytes confirmed:

- bundle `LPHB2-F34245FAE32B513DDCFE` verified before evidence display;
- all 66 units available;
- single-source `EP-002 / NBM-R22`: Yes produces **zero visible supporting-citation checkboxes**, one hidden exact-source binding, and `readForm` exports `EP-002-SEG-01` as supporting provenance;
- multi-source `EP-003 / NBM-R07`: two visible source choices appear under `Which quote(s) show the behavior you selected?`;
- optional counterevidence control is collapsed by default;
- zero external network requests, page errors, or console errors.

The measurement-bearing handoff remains unchanged:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 44 episode + 22 repeated-series units
- historical `LPCA-5B3E6CFCCE49807050DF` selection reused without resampling.

## Exact next gate

Use **only** the current provenance-simplified private kit for an **eligible independent theory-blind human auditor**. All earlier auditor kits are superseded for new human collection.

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
