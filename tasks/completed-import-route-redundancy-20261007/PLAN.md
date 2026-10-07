# Completed-import route redundancy repair — 2026-10-07

Owner incident: a completed 81-turn recovered interview was asked the legacy G15 six-hour work-energy scenario again even though historical G15 plus matched R07/R08/R09/WORK-RECOVERY evidence and later retests were present. The candidate stores historical route identity under `source.historical_question_id` while most `canonical_question_id` fields are null.

Parent outcome: **OPEN** until a completed imported interview cannot be re-questioned merely because route IDs or prompt versions changed, the live reviewer applies tendency-first new-question policy, the exact private candidate regression does not emit G15 solely for the newer prompt wording, and the repaired service is deployed/read back.

Privacy boundary: the exact candidate is retrieved privately from Library for noncommitted regression only. Repository fixtures must be synthetic/minimized and contain no private participant record.

Repair direction:
1. Normalize imported route provenance from an explicitly recorded canonical ID, otherwise a verified `source.historical_question_id`, otherwise exact canonical wording. Preserve the raw source unchanged.
2. Make route/presentation/skip/dependency logic consume the normalized route identity, including already-saved worker states whose import occurred before this repair.
3. Treat a tendency-first successor as already presented when its verified historical predecessor was presented; a genuine follow-up may still be admitted only as a bounded repair tied to actual source.
4. Supply same-family historical source turns to triage/admission as redundancy context. Missing newer wording or unrecovered later turns are provenance gaps, not coverage permission.
5. Carry completed historical-source metadata into semantic admission. For completed/saturated imports, a new clarification must be source-exposed, material, and anchored to the relevant historical evidence; exact-version absence cannot be the justification.
6. Reject retired legacy routes from newly returned clarifications, including stale persisted clarifications at the public service boundary where safely recoverable.
7. Preserve current explicit pause/stop controls, exact source wording, old evidence scope, instrument hashes, and final-review authority.

Acceptance:
- Synthetic regression with null canonical IDs plus nested historical IDs: G15 lineage is presented/answered; TF1-G15 is repair-only, legacy G15 is not selectable, and R07/R08 dependencies bind.
- Completed-record regression includes G15, R07, R08, R09, WORK-RECOVERY and retest aliases; no canonical G15 or TF1-G15 can be emitted merely because a newer exact prompt was absent.
- Any G15-family clarification must identify a materially unresolved distinction, bind relevant source antecedents/family turns, and pass independent admission.
- The exact private 81-turn candidate is run locally/private against the unchanged model configuration; expected outcome is no G15 clarification for prompt-version completion. No private source is committed.
- Focused + participant suite + repository release gates; deployment/readback and synthetic live smoke before closeout.
