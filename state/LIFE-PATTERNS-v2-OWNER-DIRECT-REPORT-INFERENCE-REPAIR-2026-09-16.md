# Life Patterns v2 — direct participant report versus interviewer inference — 2026-09-16

## Owner correction

The prior natural-flow repair used the wrong target variable. It treated a synthesis as expendable when it was "too obvious" because it restated what the participant had already said. The owner corrected that **obviousness is not a reason to discard a Life Pattern**.

The relevant distinctions are instead:

1. **generic/high-base-rate versus person-specific**; and
2. **direct participant self-report versus interviewer inference**.

A person-specific pattern can be obvious to the participant precisely because it is something they already know and directly stated. In that case the product should not repeat the same proposition back merely to ask for confirmation. Explicit participant judgment is needed when the interviewer adds an inference, synthesis, comparison, scope claim, causal relation, or other proposition the participant did not already state.

No private interview narrative is stored in this receipt.

## Superseded behavior

The participant-facing button **True, but too obvious — just move on** and its associated server path are superseded and removed.

The earlier natural-flow receipt remains historical evidence of the previous candidate, but its rule that a near-verbatim person-specific synthesis should be omitted as a Life Pattern is no longer current authority.

## Current three-way logic

### 1. Generic / high-base-rate material

If the material is common to people in general and does not carry meaningful person-specific information, it is not promoted to a Life Pattern. The measurement area may still become sufficiently covered and advance through `topic_complete`.

### 2. Direct participant-authored person-specific pattern

If the participant has already explicitly stated the person-specific pattern and the interviewer is adding no new inference:

- no synthesis-confirmation UI is shown;
- the runtime requires the proposed wording to be an **exact contiguous substring of a participant message**;
- cited operative facts must derive from that same participant source turn;
- at least one cited fact must be `reported_appraisal_or_belief`;
- the original participant source provenance is used as the authority for the internal accepted pattern;
- the runtime records the Life Pattern and its v2 acceptance/adjudication row without inventing a separate participant-decision source;
- the visible interview simply says the area has enough information and moves to the finite continuation frontier.

The v2 schema still contains an adjudication object because the accepted substrate requires participant-authoritative person-level patterns. The original participant utterance itself is the adjudication evidence; there is no redundant second approval click.

If any of the strict direct-report checks fail, the runtime does **not** auto-record the pattern.

### 3. Interviewer inference

If the interviewer adds any proposition the participant did not explicitly state, the pattern remains an ephemeral working synthesis and is surfaced tentatively for participant judgment. The existing Yes / explain / edit / reject / keep-investigating controls remain the authority boundary.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_natural_flow.py`
- `src/hdmatch/api/life_patterns_v2_owner_natural_flow_ui.py`
- `tests/unit/test_life_patterns_v2_owner_natural_flow.py`

Application source deployed: `041d567d42bf5e344265289b89b3ca13b0471ad3`.

Regression checkpoint: `f8fa03c09d23621543faa13bdff693ea9150a305`.

## Verification

GitHub Actions run `35156655878`: **SUCCESS**.

- unit/integration tests: PASS
- Ruff: PASS
- strict mypy: PASS

Railway deployment `43411eeb-782e-468e-9f2b-1c29c46a6fd6`: **SUCCESS** from application source `041d567d42bf5e344265289b89b3ca13b0471ad3`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

## Regression coverage

The focused regression proves:

- a direct participant-authored pattern can be recorded without a second confirmation;
- the accepted wording is the participant's exact source wording;
- the adjudication provenance points to the original participant source rather than a fabricated decision event;
- a model paraphrase/inference still opens the synthesis-judgment state;
- non-verbatim wording fails closed to participant judgment;
- `topic_complete` remains available for covered material that does not yield a person-specific Life Pattern;
- the obsolete "too obvious" control and endpoint are absent from the participant-facing natural-flow UI.

## Mission Control

The corrected logic lesson is durably captured on the existing UDA correction branch as:

`feedback/mission-control/SDF-20260916-LIFE-PATTERNS-DIRECT-REPORT-VS-INFERENCE-018.json`

Truth state: `CAPTURED_BRANCH_ONLY`.

## Next consumer-seam check

The owner should refresh/recover and continue normal use. PASS requires:

1. a person-specific pattern already stated in the participant's own words can be recorded without being repeated back for approval;
2. generic/high-base-rate material is still not promoted merely because the participant stated it;
3. a genuine interviewer inference still surfaces for explicit judgment;
4. the obsolete "True, but too obvious" button is gone;
5. progress, bottom-positioned liveness, exact recovery, and finite continuation remain intact.

After the product seam passes, the scientific boundary remains a fresh target-blind measurement freeze followed by the narrowly authorized owner DOB/time recovery regression against the frozen historical benchmark.
