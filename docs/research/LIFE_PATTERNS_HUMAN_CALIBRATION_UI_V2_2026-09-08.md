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

Builder:

`./scripts/build_life_patterns_human_calibration_ui_v2.py`

Compressed public-safe standalone template:

`./scripts/life_patterns_human_calibration_ui_v2_template.zlib.b64`

The compressed template contains only interface code/copy. It contains no participant evidence. Private participant-bearing handoff members are embedded only when the builder runs locally against a verified private handoff ZIP.

Example private build:

```bash
python scripts/build_life_patterns_human_calibration_ui_v2.py \
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

A private standalone UI was generated from those exact bytes:

- filename: `Life-Patterns-Human-Calibration-V2-OFFLINE.html`
- bytes: `3,980,290`
- SHA-256: `63baa191a93c49cbdfb459d4d5e3f96ff541bdddc3dd2183e5af743f48ce987b`

The generated private HTML is not committed.

## Verification performed in the continuation runtime

- input private handoff independently reverified before UI generation;
- builder deterministically reproduced the same private HTML bytes after source/template separation;
- generated JavaScript extracted and passed `node --check`;
- static scan found zero `fetch(`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `http://`, `https://`, `<img>`, `<iframe>`, or `<link>` usage;
- synthetic unit tests cover valid generation, member-hash tampering and unreceipted-extra-member rejection;
- repository CI is the engineering gate for the committed builder/tests.

### Visual verification limitation

A browser screenshot/interaction confirmation was attempted in the continuation environment, but the available Chromium runtime hung even on an empty page because of the container/browser environment. Therefore browser visual confirmation is **not claimed** here. This is an explicit degraded-mode verification gap, not a passed check. The standalone interface should receive a normal-browser smoke/visual pass before an external auditor is asked to use it if a suitable local browser execution surface is available.

## Scientific boundary

The UI is measurement transport only. It does not establish:

- the objective accuracy of participant self-report;
- construct validity;
- predictive validity;
- target-theory truth;
- eligibility for validation use.

Independent human coding must be completed and frozen before any automated Life Patterns coding is run. Human and automated outputs must then remain separately preserved before comparison.
