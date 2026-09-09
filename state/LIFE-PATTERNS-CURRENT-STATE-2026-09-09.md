# Life Patterns current state — 2026-09-09

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. Historical state remains preserved elsewhere.

## Current scientific gate

**Awaiting the independent theory-blind human first pass, after owner acceptance of the current direct-choice UI.**

No qualifying human annotations have been received. No automated Life Patterns coding, automated consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

Closed prerequisites include:

1. exact private v8/v8.1 recovery and hash verification;
2. recurrence-evidence correction in additive theory-blind v2;
3. exact private recurrence-v2 package/handoff freeze with the historical pre-label 44+22 calibration selection reused without resampling;
4. offline/no-network human UI implementation;
5. owner-led pre-collection usability corrections through the current direct-choice interaction model.

## Measurement identities remain unchanged

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- private handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- historical calibration: `LPCA-5B3E6CFCCE49807050DF`
- selected units: 44 episode + 22 repeated-series
- calibration resampled after revision: false.

The recurrence correction remains controlling: generalized behavioral self-report is evidence of **reported recurrence**; a self-selected confirming anecdote is not independent frequency evidence; recurrence strength and exceptions remain distinct; no fake numerical occurrence floor is required.

## Human-first direct-choice correction

Owner review established that asking whether there was **“Enough information to code”** before displaying the concrete behavioral values was itself a design error. A human cannot judge information sufficiency for an unspecified downstream choice.

The current UI therefore asks the substantive judgment directly:

> **Which behavior or behaviors does the exact source clearly show?**

The concrete plain-language behavior values are visible immediately.

The software derives the machine-facing applicability state:

- one or more selected behaviors -> `observed`;
- **Doesn't apply to this story** -> `not_applicable`;
- **Not enough information** -> `insufficient`.

There is no generic `Partially` state because different kinds of partial evidence have different meanings:

- if only some listed behaviors are clearly supported, select those behaviors;
- if several behaviors clearly occurred, select several;
- if the source contains suggestive but insufficient information to choose a behavior reliably, use Not enough information;
- if the prerequisite situation is absent, use Doesn't apply.

Correction record:

`state/LIFE-PATTERNS-HUMAN-UI-DIRECT-CHOICE-CORRECTION-2026-09-09.md`

Public-safe verification:

`state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-DIRECT-CHOICE-VERIFIED-2026-09-09.json`

## Remaining human-first interaction rules

- one selected behavior -> `value_relation=single` is automatic;
- multiple selected behaviors -> first ask whether the story establishes an order;
- only after Yes -> show selected behaviors in plain language and allow ordering;
- non-action prerequisite checks appear only for selected non-action values;
- Other Specified description appears only when selected;
- repeated-series recurrence/exception questions remain because they are required comparison fields;
- one exact quote -> source provenance auto-bound;
- multiple exact quotes -> actual quote text shown and auditor selects the quote(s) used;
- internal source IDs and Rxx/NBM value IDs are not human tasks;
- generic optional influence/counterevidence/context/missingness/language/note fields are omitted from the normal first pass;
- errors state what the human must do rather than exposing schema jargon.

This is presentation/control-flow only. The response schemas, code values, selected units and measurement semantics are unchanged.

## Public implementation verification

Current direct-choice builder:

`scripts/build_life_patterns_human_calibration_ui_v2_direct_choice.py`

Tests:

`tests/unit/test_life_patterns_human_calibration_ui_v2_direct_choice.py`

Implementation/test head:

`196b37e8369c9493380393b506eaa9f9d0bebedc`

Hosted CI `34398433777`: **success**

- 645 passed;
- 7 expected skips;
- Ruff passed;
- strict mypy passed for 172 source files.

## Current exact private owner-review artifact

Use only the direct-choice artifact:

- HTML: `Life-Patterns-Human-Calibration-V2-DIRECT-CHOICE-2026-09-09.html`
  - bytes: `3,996,334`
  - SHA-256: `2fadb3c827379efc3ec0988be43ffff4f5e4708d91a7f7a9c48dc25a391ad4b5`
- kit: `Life-Patterns-Independent-Auditor-Kit-V2-DIRECT-CHOICE-2026-09-09.zip`
  - bytes: `802,612`
  - SHA-256: `2dfc836fa2d7757e904ed593efba51baba22fefd9a9bf3ccfb209b80ef44c5e4`
  - two members: private HTML + `START-HERE.md`.

All earlier auditor kits are superseded for new collection.

### Exact private Chromium smoke

The current exact HTML bytes were rendered/operated in Chromium and passed:

- `Bundle verified`;
- direct behavior question visible;
- meta “Enough information to code” prompt absent;
- concrete behavior choices visible before any machine-state derivation;
- two fallback choices visible;
- selecting a behavior clears fallback selection;
- zero external network requests;
- zero page errors;
- zero console errors.

## Exact next action

Continue owner review of the current direct-choice artifact until accepted. Then an eligible independent theory-blind human auditor completes all 66 selected units plus the independence/exposure attestation before seeing any automated result.

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
