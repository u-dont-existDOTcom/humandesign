# Claude Opus 5.5 independent V4.3 remap — v2 method — 2026-09-23

Status: **POST-RESULT DEVELOPMENT EXPERIMENT / METHOD FROZEN BEFORE OPUS OUTPUT AND BEFORE V2 RERUN**.

The frozen v1 survey-instantiated V4.3 result remains unchanged. This v2 experiment begins only after that result was visible, so any improvement is development evidence, not independent confirmation.

## Question being tested

Did the first GPT-based target-aware translation lose useful survey information because it was anchored to the pre-existing neutral-domain crosswalk assignment or applied the V3.6 observable semantics too conservatively?

## Independent remap boundary

A fresh Claude Opus 5.5 CLI context receives:

- the complete frozen target-blind neutral profile;
- the same 19 candidate-unexposed V4.3 observable destinations and frozen behavior semantics;
- the historical five-level behavioral-confidence rubric.

It does **not** receive the prior GPT translations/adjudication, birth data, chart states, candidate identities, candidate rankings/scores, or prior recovery results.
Unlike v1 translation, Opus may select supporting evidence from any frozen neutral domain/facet rather than being anchored to the old crosswalk's domain assignment. It may not add observables, alter chart predicates or structural mapping weights, invent new contradictions, or change the scorer.

## Output contract

For all 19 observables, Opus must freeze:

- `relation = supported | not_established`;
- `behavioral_confidence ∈ {1.00, 0.75, 0.50, 0.25, 0.00}`;
- supporting neutral domain IDs and facet IDs;
- bounded evidence summary;
- limitations;
- rationale.

`not_established` requires `0.00`; `supported` requires nonzero confidence.

## V2 rerun rule

After the Opus translation is serialized and hashed, it may be compared descriptively with v1, but no confidence or relation may change after candidate ranking is generated.
The same already-committed survey-instantiated clean V4.3 adapter/scorer is then rerun with the Opus translation. CoreFit remains unavailable/constant, post-selection carriers remain excluded, and score-identical states remain merged across uninstantiated historical core changes.

The only decision this experiment is intended to change is whether the poor v1 V4.3 recovery is plausibly attributable in material part to the first translation/crosswalk mapping rather than to the frozen neutral survey evidence itself.

Private remap packet SHA-256: `84078b3bd9afc3170b71d34e6ded8fe1743f7646c50755e7befd8abf14947c0c`.
