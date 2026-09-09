# Life Patterns current state — 2026-09-09

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. This file is additive and does not erase historical state in `state/CURRENT-STATE.md`.

## Current scientific gate

**Awaiting the independent theory-blind human first pass.**

The prior gates are closed:

1. exact private v8/v8.1 source recovery — complete and hash-verified;
2. recurrence-evidence defect identification — complete;
3. theory-blind recurrence-corrected v2 method implementation — complete;
4. exact private v2 package/handoff freeze with the historical pre-label calibration selection reused without resampling — complete;
5. human-facing standalone local/offline annotation UI implementation — complete;
6. engineering verification and bounded Chromium render/interaction smoke — complete.

No independent human first-pass annotations have yet been received. No automated Life Patterns coding, automated consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## Recurrence-corrected measurement

The owner-directed correction remains controlling:

- generalized behavioral self-report such as `I always X` is evidence of **reported recurrence**;
- a concrete confirming example elicited after that claim is not an independent frequency observation;
- recurrence probing prioritizes scope/denominator, boundary conditions, exceptions and exception frequency;
- concrete incidents are requested only when they add discriminating information;
- ordinary-language `always` does not itself prove explicit denial of exceptions;
- recurrence strength, exception status/frequency and evidence basis are separate fields;
- no fabricated numerical occurrence floor is required for generalized recurrence language.

Historical v1 artifacts remain immutable. The substantive recurrence-v2 implementation is pinned at `7b689f3adb49da599abb40ec2bff27ad97d3887f`; CI `34271174611` passed.

## Exact private v2 freeze

Public-safe identities:

- package: `LPKG2-F93D8245B78CD9FDCF5D`
- package SHA-256: `f93d8245b78cd9fdcf5dd96f1cc321171f628015ca155b8fae0df4fcb826313a`
- human handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- private transport ZIP: 422,297 bytes, 15 members, SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- historical calibration selection reused exactly: `LPCA-5B3E6CFCCE49807050DF`
- human calibration units: 44 episode + 22 repeated-series units
- calibration resampled after revision: false.

No private participant narrative or private handoff bytes are committed.

## Human-facing offline UI

Current exact private portable standalone UI:

- filename: `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- bytes: 3,982,068
- SHA-256: `66fda4ceada51b4f82fe2c7f8a93c6d9efe886e1063a9d23fece88b79f1f6690`
- embeds private participant evidence: true
- committed to Git: false
- server required: false
- external network requests required: false
- automated judgment used: false.

Public-safe source:

- base builder: `scripts/build_life_patterns_human_calibration_ui_v2.py`
- compressed template: `scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`
- portable SHA-256 wrapper: `scripts/build_life_patterns_human_calibration_ui_v2_portable.py`
- base tests: `tests/unit/test_life_patterns_human_calibration_ui_v2.py`
- portability tests: `tests/unit/test_life_patterns_human_calibration_ui_v2_portability.py`.

Portable implementation/test head `878ffb21d964a643acd04056f14064f323de0545` passed hosted CI `34302364461`: 608 tests passed, 7 expected skips, Ruff passed, strict mypy passed for 171 source files.

A bounded Chromium render/interaction smoke passed on the exact private HTML bytes. It verified the handoff before evidence display, rendered episode and repeated-series units, exposed the recurrence-v2 controls, exercised temporary save/download/reload, failed closed on incomplete final export, and made zero network requests with zero page or console errors. The temporary smoke response was not a research annotation. Public-safe receipt: `state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-BROWSER-SMOKE-2026-09-09.json`.

The container administratively blocked direct `file://`/local-HTTP navigation, so Chromium rendered the exact HTML bytes via `page.set_content`. The auditor should confirm the file opens normally on their local browser before beginning; no additional method-design decision is pending.

## Exact next action

An eligible independent human auditor must use the verified private standalone HTML and complete all 66 selected units without access to automated labels, automated consensus, target-model outputs/mappings, birth/chart data, or expected answers.

The auditor must also complete the independence/exposure attestation. The UI exports exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`.

Preserve those exact raw bytes unchanged on receipt. Validate and content-address/freeze the human first pass under the v2 response and attestation validators **before exposing any automated output**.

Only after that freeze may the >=3 isolated theory-blind automated development coding passes begin. Consensus and human-vs-automated comparison follow later. Target-model scoring/reveal remains unauthorized.

## Boundaries

- development only;
- validation use forbidden;
- no automated Life Patterns coding before the independent human pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy under this task state;
- no assistant-initiated participant/auditor contact or spending without separate authorization;
- never commit participant narrative or the private standalone HTML;
- never reconstruct private source material from summaries, memory, receipts, or transcript fragments.

Historical owner correction elsewhere in `state/CURRENT-STATE.md` remains intact, including that **there was never a completion policy**; this overlay does not supersede or remove that unrelated correction.
