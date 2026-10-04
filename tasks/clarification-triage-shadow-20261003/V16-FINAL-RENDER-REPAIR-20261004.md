# V16 final render/persistence repair — 2026-10-04

V16 exposed three tuning failures after route-level gap/spec admission was separated from question wording:
- Y2 and Y8 had correctly admitted route-level gaps but participant-facing wording failed the wording-only gate.
- Y7 contained an unresolved preference/persistence target but triage/audit did not apply the same opposed-possibilities rule already used by admission.

Repair:
1. GapTriage and GapMatchAudit now treat a preference/intensity/persistence answer that leaves materially opposed possibilities open without a usual tendency, selection condition, or settled inclination as unresolved.
2. If a route-level gap is admitted but its current question fails wording review, the pipeline renders a replacement from the admitted route/spec and exact source anchors without reconsidering gap existence.
3. The replacement receives a separate wording-only review for construct discrimination, one-response-task form, and unsupported extension.
4. No render/review round trip occurs when the original question is already wording-approved.
5. Recovered omission questions use the same bounded render/review path when needed.

Focused verification before this note:
- Ruff passed.
- 30/30 shadow-triage tests passed.
- Contaminated Y2/Y7/Y8 replay passed 3/3.
- Y7/Y8 preserved their original wording rejection codes diagnostically while the replacement question cleared participant-facing rejection.

These are tuning results only. One fresh untouched validation packet remains required; if it passes, run one unchanged stability repeat and then the owner-scale 81-turn latency measurement.
