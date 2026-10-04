# V16 untouched validation result - 2026-10-04

The v16 packet and blind targets were committed and pushed before implementation replay. All ten cases were scored; Sonnet/high and Opus 5.5/max agreed exactly on Y1-Y9, while Y10 required G23 and permitted M05.

First untouched implementation replay: 7/10 passed.

Failures:
- Y2: expected M09 + G19. Both route-level gaps were proposed and admitted, but the M09 rendered question failed the wording-only unsupported_extension gate.
- Y7: expected PREFER-EXCHANGE. The route had already been presented; its answer said persistence varied between continuing and dropping the negotiation, with both about equally likely. Triage returned review-ready and no route was recovered.
- Y8: expected PREFER-EXCHANGE. The route-level gap was proposed and admitted, but its rendered repair question failed the wording-only unsupported_extension gate.

This confirms the gap-spec split is functioning: Y2/Y8 no longer lose valid gaps. They now fail only participant-facing wording readiness. Y7 is separate: the source itself leaves the persistence target unsettled, but the triage/match-audit rubric does not yet apply the explicit opposed-possibilities rule used by GapAdmission.

Next repair:
1. apply the same preference/intensity/persistence unresolved rule to GapTriage and GapMatchAudit;
2. when an admitted gap has question_approved false, render a replacement from the admitted route/spec and exact source anchors without reconsidering whether the gap exists;
3. independently recheck only that replacement's construct discrimination, one-task form, and unsupported extension;
4. do not add any repair call when the original question is already approved.

V16 is tuning evidence, not promotion evidence.
