# Life Patterns current state — 2026-09-09

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. Historical state remains preserved elsewhere.

## Current scientific gate

**Awaiting the independent theory-blind human first pass.**

No qualifying human annotations have been received. No automated Life Patterns coding, automated consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

Closed prerequisites include:

1. exact private v8/v8.1 recovery and hash verification;
2. recurrence-evidence correction in additive theory-blind v2;
3. exact private recurrence-v2 package/handoff freeze with the historical pre-label 44+22 calibration selection reused without resampling;
4. offline/no-network human UI implementation;
5. owner-led pre-collection usability correction until the task is actually understandable and minimal for a human auditor.

## Measurement identities remain unchanged

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- private handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- historical calibration: `LPCA-5B3E6CFCCE49807050DF`
- selected units: 44 episode + 22 repeated-series
- calibration resampled after revision: false.

The recurrence correction remains controlling: generalized behavioral self-report is evidence of **reported recurrence**; a self-selected confirming anecdote is not independent frequency evidence; recurrence strength and exceptions remain distinct; no fake numerical occurrence floor is required.

## Human-first UI correction

Owner browser review exposed a broader design error: even after plain-language cleanup, the interface was still shaped around the response schema rather than around a human's actual judgment task.

Examples caught before collection:

- asking whether multiple selected behaviors happened in “this order” before any order was shown;
- displaying the order only after that answer, using opaque code IDs;
- showing many optional metadata controls that a rational auditor would skip, creating needless burden and missing-not-at-random auxiliary data;
- asking which quote established an influence relation when only one quote existed;
- exposing internal source IDs and code IDs;
- surfacing errors such as value-relation/non-action schema failures instead of telling the person what to fix.

The controlling policy is:

`docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`

Correction record:

`state/LIFE-PATTERNS-HUMAN-UI-HUMAN-FIRST-CORRECTION-2026-09-09.md`

### Current human flow

The independent auditor now sees only judgments that can change the planned calibration:

1. one exact story/pattern source + one plain behavioral question;
2. `Yes — clearly shown`, `No — does not fit`, or `Can't tell`;
3. if Yes, select the behavior(s) shown;
4. if one behavior is selected, `value_relation=single` is automatic and no relation control appears;
5. only if two or more behaviors are selected, ask whether the story establishes an order;
6. only if the auditor says Yes, show those selected behaviors in **plain language** and let the auditor arrange them;
7. only if a non-action behavior is selected, show the four required prerequisite checks;
8. only if Other Specified is selected, request a description;
9. repeated-series units ask the required recurrence/exception judgments in plain language;
10. one exact quote is auto-bound as provenance; if several exact quotes exist, show their actual text and ask which were relied on.

Generic optional influence, counterevidence, context qualifier, missingness, language and free-note entry are omitted from the normal first-pass flow. Their valid transport defaults are serialized automatically. The exact source remains preserved for later disagreement adjudication.

This is a presentation/collection-burden correction only. The response schemas, code values, selected units and measurement semantics are unchanged.

## Public implementation verification

Current final human-first builder:

`scripts/build_life_patterns_human_calibration_ui_v2_auditor_final.py`

Tests:

`tests/unit/test_life_patterns_human_calibration_ui_v2_auditor_final.py`

Implementation/test head:

`3447565cb56d5a6cd39d1a44877b3ca2604fdd1c`

Hosted CI `34384054801`: **success**

- 635 passed;
- 7 expected skips;
- Ruff passed;
- strict mypy passed for 172 source files.

The later state/policy head `46bb7010cb487d31435702ef4031ac3124d440d5` also passed CI `34384155046`.

Public-safe exact private verification receipt:

`state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-HUMAN-FIRST-VERIFIED-2026-09-09.json`

## Current exact private auditor artifact

Use only the human-first artifact:

- HTML: `Life-Patterns-Human-Calibration-V2-AUDITOR-2026-09-09.html`
  - bytes: `3,995,302`
  - SHA-256: `7866b98b9aab72a329825675bb037e951354c9093a35b0f218d335ef7a0a8b3e`
- kit: `Life-Patterns-Independent-Auditor-Kit-V2-AUDITOR-2026-09-09.zip`
  - bytes: `802,576`
  - SHA-256: `8e97c264045867b69db6a29af21cde8b2f3d5e3587a852b802504a38a0de1673`
  - two members: private HTML + `START-HERE.md`.

All earlier auditor kits are superseded for new collection.

### Exact private Chromium smoke

The current exact HTML bytes were rendered/operated in Chromium and passed:

- `Bundle verified` / exact handoff/package identities;
- 66 units total;
- zero external network requests;
- zero page errors;
- zero console errors;
- one behavior selected -> no relation task;
- multiple behaviors selected -> order question appears first;
- ordered selection -> plain-language behavior list appears for arrangement, with no internal Rxx IDs;
- one exact quote -> source provenance automatic;
- multiple exact quotes -> quote text shown for selection;
- generic influence/counterevidence/advanced optional fields absent;
- tested non-action failure produces a concrete human-readable instruction rather than schema jargon.

## Exact next action

An eligible independent theory-blind human auditor uses only the current human-first kit and completes all 66 selected units plus the independence/exposure attestation before seeing any automated result.

They return exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Preserve those exact raw bytes unchanged. Validate/content-address/freeze them before exposing automated output.

Only after that freeze may the >=3 isolated theory-blind automated development coding passes begin.

## Boundaries

- development only; validation use forbidden;
- no automated Life Patterns coding before the independent human pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy under this task state;
- no assistant-initiated participant/auditor contact or spending without separate authorization;
- never commit participant narrative or private HTML;
- do not reselect the 44+22 calibration units after seeing evidence merely because some story/observable pairs are negative or inapplicable.
