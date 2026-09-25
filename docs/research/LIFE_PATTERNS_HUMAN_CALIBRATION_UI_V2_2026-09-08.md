# Life Patterns human calibration UI v2 — 2026-09-08

Status: **development-only local/offline annotation interface** for the recurrence-corrected private human handoff v2. It is not a participant-facing product, does not perform automated coding, and does not authorize target-model scoring.

## Purpose

The independent human coder should not hand-edit JSON. This interface turns the exact frozen human-calibration handoff into one self-contained HTML file that:

- verifies the handoff before revealing evidence;
- presents one selected episode/series × observable unit at a time;
- makes exact participant source text primary and transfer summaries visibly secondary;
- exposes the exact neutral observable definition, criteria, allowed values, Other Specified and non-action rules;
- preserves the recurrence-v2 distinction between generalized reported recurrence, exceptions, evidence basis and bounded episodes;
- blocks structurally invalid combinations before a response can be saved/exported;
- collects the independent/blinding declaration as an ordinary form rather than requiring JSON editing;
- exports the exact response/attestation interchange contracts required by the v2 validators.

## Implementation

Base verified builder:

`./scripts/build_life_patterns_human_calibration_ui_v2.py`

Compressed public-safe standalone template:

`./scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`

Portable local-cryptography wrapper:

`./scripts/build_life_patterns_human_calibration_ui_v2_portable.py`

The compressed template contains only interface code/copy. It contains no participant evidence. Private participant-bearing handoff members are embedded only when the builder runs locally against a verified private handoff ZIP.

The portable wrapper does **not** reinterpret or rewrite the measurement. It first calls the base verified builder, then fail-closed replaces exactly one strict WebCrypto-only SHA-256 gate with a verifier that prefers native `crypto.subtle` and falls back to a self-contained pure-JavaScript SHA-256 implementation when WebCrypto is unavailable in the local document context. The response contract, evidence, codebook, recurrence semantics, packet identities and offline/no-network boundary remain unchanged.

Recommended private build:

```bash
python scripts/build_life_patterns_human_calibration_ui_v2_portable.py \
  --handoff-zip /private/path/human-calibration-v2.zip \
  --output-html /private/path/Life-Patterns-Human-Calibration-V2-OFFLINE.html
```

Do **not** commit the generated HTML: it embeds private participant evidence.

## Pre-display integrity gate

The Python builder fails closed unless it verifies:

1. unique ZIP member names and no directory entries;
2. the exact `LPHB2-*` public-safe receipt content address;
3. exact receipt-declared member set and SHA-256 for every member;
4. the expected recurrence-v2 handoff flags and response schema versions;
5. blank episode/series response rows contain no annotation state;
6. response-schema and blank-attestation version bindings;
7. every human LPBP2 packet content address;
8. no prior automated labels, consensus, target-model information, birth/chart information or resampling flag in packets;
9. exact package/manual/recurrence-policy/human-prompt bindings across packets;
10. exact selected episode and series unit coverage between packets and blank response rows.

The generated browser application re-verifies the embedded receipt, member hashes, packet content addresses and selected-unit coverage before it reveals any evidence.

## Network/privacy boundary

The generated file is standalone and requires no server. Its CSP denies external content and connections, including:

- `default-src 'none'`
- `connect-src 'none'`
- `img-src 'none'`
- `font-src 'none'`
- `object-src 'none'`
- `frame-src 'none'`
- `worker-src 'none'`
- `form-action 'none'`

There are no fetch/XHR/WebSocket/EventSource calls. No AI is invoked. All annotation state exists in browser memory unless the auditor explicitly downloads a progress/export file.

## Human workflow

The interface distinguishes **Episode** and **Repeated series** visually and semantically.

For each unit it provides:

- exact source segments and selectable source citations;
- neutral observable definition and measurement criteria;
- `observed / insufficient / not_applicable` state;
- exact allowed values and single/ordered/unordered relation;
- Other Specified description when applicable;
- four-part non-action gate when a registered non-action value is selected;
- missingness flags, context qualifiers, life phase, language and notes;
- episode-only influence relation/source provenance;
- series-only reported recurrence strength, exception status/frequency, frequency evidence basis, optional bounded rate/count and recurrence scope.

A generalized recurrence report does not require a fabricated occurrence floor, and confirming anecdotes are never counted by the interface as independent frequency support.

## Progress and final export

Progress files bind themselves to the exact handoff receipt and are fully revalidated on reload.

Final export is blocked unless all selected units have valid saved responses and all independence/blinding attestation fields are completed in the eligible direction. It produces exactly:

- `episode_responses.completed.jsonl`
- `series_responses.completed.jsonl`
- `auditor_attestation.completed.json`

The attestation completion timestamp is generated only at final export. Favorable independence/blinding declarations are never pre-selected.

## Current real private build

The owner-reuploaded recurrence-corrected handoff verified on 2026-09-08 is:

- handoff: `LPHB2-F34245FAE32B513DDCFE`
- handoff SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- package: `LPKG2-F93D8245B78CD9FDCF5D`
- selected units: `44 episode + 22 series`

The current private portable standalone UI generated from those exact bytes is:

- filename: `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- bytes: `3,982,068`
- SHA-256: `66fda4ceada51b4f82fe2c7f8a93c6d9efe886e1063a9d23fece88b79f1f6690`

The generated private HTML is not committed.

## Verification performed

Engineering verification:

- input private handoff independently reverified before UI generation;
- base builder deterministically reproduced its expected private HTML bytes after source/template separation;
- generated JavaScript extracted and passed syntax checking;
- static scan found zero `fetch(`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `http://`, `https://`, `<img>`, `<iframe>`, or `<link>` usage;
- unit tests cover valid generation, member-hash tampering and unreceipted-extra-member rejection;
- portability tests fail closed on template drift and verify native-WebCrypto preference plus the SHA-256 fallback injection;
- hosted CI `34302364461` on portability implementation/test head `878ffb21d964a643acd04056f14064f323de0545` passed **608 tests with 7 expected skips**, Ruff, and strict mypy for 171 source files.

### Chromium render/interaction smoke — passed 2026-09-09

The exact current private portable HTML bytes completed a bounded Chromium interaction smoke. Public-safe receipt:

`state/LIFE-PATTERNS-HUMAN-CALIBRATION-UI-V2-BROWSER-SMOKE-2026-09-09.json`

Verified behavior included:

- embedded handoff cryptographic verification completed before evidence display;
- first episode and exact participant source rendered;
- repeated-series evidence rendered separately;
- recurrence-v2 controls appeared for observed series evidence;
- one explicitly temporary smoke-only response was saved, progress was downloaded/reloaded and state was restored;
- incomplete final export failed closed until all 66 units and the eligible attestation are complete;
- zero external network requests;
- zero page errors;
- zero console errors.

The temporary smoke response is **not** a research annotation and was not submitted or committed. Private screenshots used for visual inspection are not committed.

The execution container administratively blocks direct `file://` and local HTTP navigation, so the exact HTML bytes were rendered in Chromium via `page.set_content`. The auditor should confirm the file opens normally in their own local browser before beginning. This is an operational environment caveat, not an unresolved measurement-method decision.

## Scientific boundary

The UI is measurement transport only. It does not establish:

- the objective accuracy of participant self-report;
- construct validity;
- predictive validity;
- target-theory truth;
- eligibility for validation use.

The **current scientific gate is the independent theory-blind human first pass**. It must be completed and frozen before any automated Life Patterns coding is run. Human and automated outputs must then remain separately preserved before comparison.
