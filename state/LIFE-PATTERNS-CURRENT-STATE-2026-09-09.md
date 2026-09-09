# Life Patterns current state — 2026-09-09

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. Historical state remains preserved elsewhere.

## Current scientific gate

**Awaiting the independent theory-blind human first pass.**

Closed prerequisites now include:

1. exact private v8/v8.1 recovery and hash verification;
2. recurrence-evidence defect correction in additive theory-blind v2;
3. exact private recurrence-v2 package/handoff freeze with historical pre-label calibration selection reused without resampling;
4. original offline human UI implementation and portability verification;
5. owner-detected human-comprehension correction before any qualifying human coding;
6. owner-detected redundant source-provenance control correction before any qualifying human coding;
7. engineering CI and exact-browser verification for the current human transport.

No qualifying independent human annotations have been received. No automated Life Patterns coding, automated consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Measurement identities remain unchanged

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- private handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- historical calibration: `LPCA-5B3E6CFCCE49807050DF`
- selected units: 44 episode + 22 repeated-series
- calibration resampled after revision: false.

The 2026-09-08 recurrence correction remains controlling: generalized behavioral self-report is evidence of **reported recurrence**; a self-selected confirming anecdote is not independent frequency evidence; recurrence strength, exception status/frequency and evidence basis remain separate; no fake numerical occurrence floor is required.

## Human transport corrections

Owner browser review found two usability defects before independent collection:

1. codebook/machine language obscured what behavior question was actually being asked and who the narrator/actor was;
2. after answering Yes and choosing a behavior, the UI still asked a redundant source-level `does this quote support/oppose it?` question even when there was only one exact source segment.

The second defect is recorded at:

`state/LIFE-PATTERNS-HUMAN-UI-REDUNDANT-CITATION-CONTROL-2026-09-09.md`

The correction preserves provenance without turning it into another substantive judgment:

- single exact source + Yes: source segment is auto-bound as supporting provenance with no visible citation checkbox;
- multiple exact sources + Yes: auditor selects only the exact quote(s) actually relied on;
- optional counterevidence lives in a collapsed exception/conflict control;
- No / Can't tell: no source-citation controls;
- response schemas/values, source-segment IDs, selected units, recurrence semantics, blinding and target-model isolation are unchanged.

Current public-safe implementation:

- `scripts/build_life_patterns_human_calibration_ui_v2_plain.py`
- `tests/unit/test_life_patterns_human_calibration_ui_v2_plain.py`
- `scripts/build_life_patterns_human_calibration_ui_v2_plain_provenance.py`
- `tests/unit/test_life_patterns_human_calibration_ui_v2_plain_provenance.py`
- `docs/research/LIFE_PATTERNS_INDEPENDENT_AUDITOR_START_HERE_PLAIN_2026-09-09.md`

Provenance-simplification implementation/test head `3ec4b9dc95f80fee46a4a44d9e052e03088c303a` passed hosted CI `34373413686`:

- 622 passed;
- 7 expected skips;
- Ruff passed;
- strict mypy passed for 172 source files.

## Current private plain-language UI

- delivery filename inside the kit: `Life-Patterns-Human-Calibration-V2-PLAIN.html`
- bytes: `3,997,285`
- SHA-256: `0d123b0eca37988157282f9b70f0030e7af106e33155e04b30ffe76f68eff568`
- private participant evidence embedded: true
- committed to Git: false
- embedded handoff fragment unchanged: true
- selected units changed: false
- response contract changed: false
- measurement semantics changed: false
- external network required: false.

Exact-browser verification on those private bytes confirmed:

- `Bundle verified` before evidence display;
- all 66 selected units bound;
- single-source `EP-002 / NBM-R22`: Yes shows zero visible supporting-citation checkboxes, auto-binds the sole exact source, and `readForm` exports `EP-002-SEG-01` as supporting provenance;
- multi-source `EP-003 / NBM-R07`: Yes shows two source choices under `Which quote(s) show the behavior you selected?`;
- optional counterevidence is collapsed by default;
- zero external network requests, page errors, or console errors.

Public-safe receipt:

`state/LIFE-PATTERNS-HUMAN-UI-PROVENANCE-SIMPLIFICATION-VERIFIED-2026-09-09.json`

## Current private auditor delivery kit

Use only:

`Life-Patterns-Independent-Auditor-Kit-V2-PLAIN-PROVENANCE-2026-09-09.zip`

- bytes: `804,132`
- SHA-256: `291ffaa9bf886e6fe4bcf778b2d41264275bc3b74c11ce82d1df24894bf768d3`
- members: exact current private HTML + `START-HERE.md`.

All earlier auditor kits are historical/superseded for new human collection.

## Exact next action

An eligible independent theory-blind human auditor uses the current provenance-simplified kit and completes all 44 episode + 22 repeated-pattern units plus the independence/exposure attestation **before seeing any automated output**.

The three raw exports are:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

Preserve those exact bytes unchanged, validate/content-address/freeze them, and only then begin the >=3 isolated theory-blind automated development coding passes.

## Boundaries

- development only; validation use forbidden;
- no automated Life Patterns coding before the independent human pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy under this task state;
- no assistant-initiated participant/auditor contact or spending without separate authorization;
- never commit participant narrative or private HTML;
- do not reselect the 44+22 calibration units after seeing evidence merely because some story/observable pairs are negative or inapplicable.
