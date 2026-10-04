# V9 validation-spec reconciliation — 2026-10-04

## Frozen v9 result

The first untouched v9 implementation replay scored 6/10 against the precommitted v9 expected targets. P1, P4, P6, and P7 failed.

No implementation change was made before diagnosis.

## Specification defect

The original blind adjudication prompt used simplified route meanings plus an over-broad rule that a “check/ask first” response is merely procedural unless it states a downstream criterion. That rule is not valid uniformly across the frozen routes:

- G19 asks what matters; naming tiredness, time remaining, or duration can answer the route without giving a threshold or final choice.
- M11 asks what the respondent would say next; its frozen interpretation limit explicitly allows asking about budget.
- M09 asks which properties matter in the app tradeoff; “I’d read reviews first” does not identify a property/result and can remain preliminary.

## Post-hoc exact-authority reconciliation

Fresh Sonnet/high and Claude Opus 5.5/max contexts received the exact frozen route questions, admission rules, interpretation limits, and the four failed synthetic cases. They did not receive implementation output or the prior adjudication.

Both independently returned the same corrected dispositions:
- P1: review ready.
- P4: review ready.
- P6: review ready.
- P7: clarify M09 only.

Those corrected dispositions match the actual v9 participant-facing outputs on all four cases; the other six cases already matched their frozen targets.

## Scientific disposition

Do **not** relabel v9 as an untouched 10/10 pass. The corrected adjudication occurred after implementation output existed, so it is development evidence demonstrating a target-specification defect.

The implementation remains unchanged. Promotion now requires a new untouched validation packet whose adjudicators receive exact route authority and the route-specific response-task rule from the outset.
