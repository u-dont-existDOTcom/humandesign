# Owner-trained scenario survey v8 — Q1 freeze — 2026-09-24

Status: **TARGET-AWARE OWNER TRAINING / POST-SELECTION DEVELOPMENT, NOT VALIDATION**.

## Source and review boundary

The predeclared `OWNER-TRAINING-V8-CLAUDE-METHOD-20260924.md` pass completed successfully with exact model `claude-opus-5-5` at `max` effort. The raw run and parsed design remain private because they contain participant-specific evidence/coding.

- private raw-run SHA-256: `892a56c14dfdd3b4d3e9fc6bc2e822d312f09aa6818f97bbbb92947a71591c6f`
- private parsed-design SHA-256: `3c5774f04696a58ccf9ac3737aa92e73d9bf26da326da606c3fddaf81832fdda`
- Claude schema: `owner-training-v8-claude-design-v1`
- selected construct: `V8.PROFILE24.OPPORTUNITY_ROUTE`

Claude output is proposal-only. The supervising review independently re-applied the seven final rendered-question checks and accepted the construct with a wording repair that makes the relevant temporal relation explicit and adds an insufficient-evidence branch.

## Why this construct is admitted

This question measures one ordinary-life distinction: whether adult collaborative opportunities were routed primarily through a relationship that already existed **before** the opportunity arose, versus routes where no collaborator/route source already knew the participant.

It is retained because it:
- is behaviorally interpretable without chart/Human-Design jargon;
- separates the target's 2/5 profile neighborhood from both relevant 2/4 competitors;
- is not a hidden Channel-vs-Gate mechanism bonus;
- has plausible ordinary answers on both sides plus mixed/insufficient outcomes;
- does not infer sociability, charisma, networking skill, competence, reputation, career success, or general introversion/extroversion.

This is a narrow v8 development subconstruct. It is **not** by itself a full Survey-v2 `PROFILE_24` classification.

## Exact frozen Q1

> Thinking only about adult work, projects, or collaborations that involved other people and that you actually ended up doing: before each one started, did the opportunity mostly come through someone who already knew you (a friend, acquaintance, or referral), or mostly through a route where nobody involved already knew you (for example a public posting/application, cold outreach, or an open online group)? If it's mixed, roughly how does it split? If there aren't enough examples to tell, say that.

Construct ID: `V8.PROFILE24.OPPORTUNITY_ROUTE`.

## Frozen coding before answer

- `familiar_route`: the opportunity mostly arose through a pre-existing friend/acquaintance or a referral originating from such a relationship.
- `unfamiliar_route`: the opportunity mostly arose through routes where the relevant people did not already know the participant.
- `mixed`: substantial examples exist on both sides without one route clearly predominating.
- `insufficient`: too few eligible interpersonal examples to characterize the route. Solo/self-authored work is not automatically `unfamiliar_route`; it is outside this construct unless another person/opportunity route is actually involved.

The code updates only the appropriate member of `DC:PROFILE_STRUCTURE`. Profile-family members remain dependency-normalized and cannot create multiple denominator units merely because several structural/profile fields encode the same family.

## Final rendered-question admission

- context binding: PASS
- premise sufficiency: PASS
- discrimination: PASS
- nonredundancy: PASS
- construct alignment: PASS
- single response task: PASS
- expected information gain: PASS

If the owner answers outside the offered branches, preserve the literal answer privately and code only what it supports. Do not force a branch.

## Sequential queue and stop rule

Ask Q1 only. Preserve the exact answer privately, apply the frozen code, then recompute the observable-level owner-training comparison for:
1. target vs persistent 2013 competitor;
2. recorded 10:25 neighborhood vs relevant same-date 1985 alternatives.

The next candidates are predeclared, not automatically admitted:

1. `V8.PROFILE5.UNMET_EXPECTATION_REACTION` — eligible only if the Q1 result leaves the profile-family distinction unresolved enough to matter.
2. `V8.ORGANIZED_DETAIL.LEARNING_STRUCTURE` — date-recovery candidate only if the 2013 comparison remains materially unresolved after profile-family evidence.

Each future exact wording must still pass the seven final rendered-question checks at time of use. Do not reopen RHYTHM_ROUTINE, CENTER_ROOT, body-specific Moon/Mars gate storytelling, or Channel-vs-Gate mechanism scoring in this owner-training round merely because the target remains behind.

A stage is settled when the current observable-level margin exceeds the maximum possible swing of all still-admissible queued items, or the queue is exhausted. A target loss/tie at queue exhaustion is recorded as negative/ambiguous development evidence, not rescued with new target-shaped questions.
