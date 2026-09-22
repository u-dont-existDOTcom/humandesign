# Blind rereview reconciliation — candidate dcede6b — 2026-09-22

Reviewed candidate: `dcede6bd5c7644cdbf7c689bc7bbc72ee7b9d8e6`

Blind verdict: `NOT_READY_FOR_FRESH_PILOT`; `semantic_change_required=true`.

## Confirmed blocker and repair

**M06 introduced an undefined replacement cue after removing route familiarity.** The reviewed wording said the driver made a turn the respondent “did not expect,” even though the respondent did not know the route. That allowed respondents to invent map knowledge, directions, geographical intuition, or another replacement cue.

The reconciled M06 now asks directly for the respondent's **familiarity boundary**: what they would need to already know about a route before a turn away from its usual path would carry meaning. This avoids fabricating an unfamiliar-route event and introduces no second cue. Admission/interpretation prohibit surprise, maps, directions, hazards, or other substitute signals; the evidence guide credits only the respondent's answer-originated familiarity threshold.

## Adopted nonblocking improvements

- F0 now holds relationship type constant (friends in both variants) and varies familiarity duration only: long-known versus newly-known friends.
- M11 now specifies a two-person meal with a friend, removing ambiguity about who the exchange concerns.
- The overloaded `PREFER-INFLUENCE` route was split into `PREFER-PERSUADE` for D05.preferred_use and `PREFER-EXCHANGE` for X08.preferred_use. Each has its own antecedent, wording, family, interpretation boundary, and evidence-guide route.

The split raises the canonical bank from 78 to **79 routes** while preserving all 73 source facets and 81 exact route–facet pairs.

## Verification

The reconciled candidate passes **490 / 490** deterministic checks. Canonical node IDs are unique; family membership exactly covers all 79 nodes; all 81 planning-target pairs exactly match evidence-guide routes; and the exploratory sensory-conflict item remains outside canonical evidence.

## Next gate

Commit the exact reconciled bytes and run another fresh mechanically firewalled GPT-5.6 Sol xhigh semantic review. The blind reviewer must audit all 79 canonical routes and must not receive any prior review findings, reconciliation, rationale, audits, verification verdicts, or private participant material before findings freeze.
