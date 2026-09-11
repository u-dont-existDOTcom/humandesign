# Life Patterns V5 private portable adapter — 2026-09-11

Status: public-safe execution architecture for owner-review candidate generation only. No participant text or generated private HTML is contained here.

## Why this adapter exists

The canonical public V5 owner-facing builder remains:

`scripts/build_life_patterns_human_calibration_ui_v5_final.py`

In the 2026-09-11 ChatGPT sandbox, the exact private V2 transport ZIP was available locally, but the GitHub-connected public repository could not be checked out through Git/network and the connector could not mount the compressed V2 HTML-template chain into the local sandbox. Continuing to optimize that blocked execution path would not advance the owner-review outcome.

A bounded strategy switch therefore preserved the accepted measurement semantics while changing only the delivery/execution layer. The adapter is **not a new measurement design**. It reuses the accepted V5 contract mechanics and the exact already-frozen private selected-unit handoff.

## Input identity and fail-closed verification

The adapter accepts only the exact outer transport:

- filename: `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256: `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- bytes: `422297`
- members: `15`

It independently verifies the inner receipt and receipt-bound archive content:

- receipt id: `LPHB2-F34245FAE32B513DDCFE`
- receipt SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- packet count: `8`
- every receipt-declared member hash
- every LPBP2 packet content address
- exact selected coverage: `44 episode + 22 series = 66 units`

Outer ZIP identity and inner receipt identity remain distinct.

## Reused accepted V5 mechanics

The adapter preserves the same controlling semantics already implemented and publicly verified at implementation head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02` / CI `34623829382`:

- choices grouped by accepted behavioral facet;
- no global `value_relation` question;
- cross-facet co-presence never implies chronology;
- same-facet multiple facts ask stage/window separation only when needed;
- chronology is asked only after distinct stages are established;
- temporal edges are emitted only when order is explicitly established;
- all stages within one selected episode/series unit share one evidence unit unless a genuinely independent opportunity is established elsewhere;
- mixed hybrids retain separate affirmative and absence components;
- an affirmative hybrid component can remain observed when the paired absence gate is insufficient, while the combined parent assertion is withheld;
- pure absence-dependent values use one separately gated absence component;
- four-part gates remain awareness / opportunity / feasibility / established nonoccurrence;
- non-mention and silence never establish absence;
- one exact source auto-binds provenance;
- multiple exact sources use claim-specific source selection;
- repeated-series outputs retain recurrence-v2 fields and never count a confirming anecdote as independent frequency evidence;
- machine graph IDs remain hidden from the human-facing task.

The top-level human fallback labels are exactly:

- `Doesn't apply to this story` — only when the prerequisite is affirmatively absent;
- `Not enough information` — when the source is insufficient.

## Private packaging

The generated HTML embeds:

1. the exact outer private transport ZIP bytes as base64, preserving its SHA-256 exactly;
2. a base64 JSON display/index projection generated only after all outer/inner verification passes.

The projection avoids raw participant text appearing literally in the HTML source. The generated file includes a CSP with `connect-src 'none'` and requires no external network resource.

Private output is never committed to GitHub.

## Browser/export behavior

The adapter provides:

- exact-source display;
- unit navigation;
- local progress persistence;
- progress-backup download;
- auditor-attestation download;
- final V5 episode and series JSONL export names;
- fail-closed final export until all 66 units have a saved top-level response;
- conditional hybrid, absence, source-provenance, and stage/chronology controls.

## Verification performed

Public-safe receipt:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-OWNER-REVIEW-CANDIDATE-2026-09-11.json`

Technical checks include:

- exact outer ZIP SHA/size/members;
- exact inner receipt hash and all member/packet hashes;
- 44+22 selected-unit coverage;
- generated HTML SHA/size;
- embedded outer ZIP re-decoding to the exact original SHA;
- full exact-source strings checked for literal plaintext leakage;
- JavaScript syntax check with Node;
- Chromium DOM/interaction smoke with zero external network requests and zero console errors;
- save/reload persistence;
- R05-O2 separate affirmative + four-gate absence UI;
- R14-i four-gate pure absence and fail-closed incomplete gate;
- multi-source claim-specific provenance;
- progress and attestation downloads;
- incomplete final export fail-closed;
- public-only synthetic graph smoke for R14-i, partial R05-O2, ordered two-stage one-evidence-unit behavior, and series recurrence-v2 envelope fields.

### Sandbox browser limitation

Managed Chromium blocks direct `file://` and localhost navigation in this sandbox, and an opaque in-memory origin has no native `SubtleCrypto`. Therefore:

- the exact outer ZIP was cryptographically verified in Python before generation and again by decoding the bytes embedded in the generated HTML;
- the HTML DOM and interaction code was exercised in Chromium through `set_content`;
- only the unlock button's digest call was shimmed with the already independently verified digest.

This limitation is recorded rather than silently treated as a normal local-browser smoke.

## Decision and remaining gate

This adapter is suitable as a **private owner-review candidate**, not yet as the scientific collection surface.

Before independent human collection is authorized, one of these must occur after explicit owner usability acceptance:

1. **Promote/adapt:** commit the portable adapter implementation plus focused tests and obtain green CI against the public V5 validator; or
2. **Canonical regenerate:** run `scripts/build_life_patterns_human_calibration_ui_v5_final.py` against the exact private outer transport in an environment with a local repository checkout/template chain, then smoke that exact result.

The accepted V5 scientific semantics stay fixed in either route. Owner usability feedback should modify presentation only unless it reveals a genuine semantic defect.
