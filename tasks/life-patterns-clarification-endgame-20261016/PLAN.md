# Life Patterns review endgame — 2026-10-16

## Owner observation and objective

An already interviewed participant is answering independent reviewer clarifications through the existing Custom GPT. Every question says "1 of 1 remaining," but after a one-question batch the reviewer may issue another. The owner wants honest global progress, a clear ending, and ideally a browser/Railway final step instead of endless GPT interaction. Preserve all earlier 96 edited Q&As and later clarifications; do not restart, preempt independent review, or silently freeze partial evidence.

## Existing architecture recovered

GPT gathers/continues answers and uses versioned Action calls against existing Railway `life-patterns-participant` service. Railway stores encrypted source and independent reviewer state. The `fast-batch-v1` independent reviewer may admit 1–3 new useful questions per batch and eventually run full evidence synthesis. Thus "1 of 1" is a **current-batch** count, not the total left before completion. Current GPT Knowledge acknowledges unknown future batches but its instructions do not require a persistent participant-facing warning. No globally trustworthy future question count currently exists; inventing a number or deadline would worsen the problem.

The old attempt to put the entire interview on Railway/Venice ran into deployment/provider and throughput issues; the current public participant flow is disabled, though GPT review/submit endpoints are live. A GPT-to-browser finishing page would require a review-scoped, short-lived participant credential plus safe consent, record/freeze and secondary-module workflow. Sharing the existing GPT Bearer key or unguessable review ID in an ordinary public URL is **not** an admissible shortcut.

## This bounded repair

1. Extend Railway read-only review guidance with accurate **global stage**, actual count of previously answered/skipped clarifications, current batch size, explicit unknown future batches, and the concrete post-review stages (participant confirmation, CF-003 three questions, encrypted submission). Do not use current-batch count as overall remaining. Retain the service's current published semantics and status; do not alter reviewer admission or fixed source evidence.
2. Extend GPT display instructions/Knowledge guide to ban unqualified "1 of 1 remaining", require "question 1 of 1 **in this batch**; overall remaining unknown until independent review reaches ready", and show visible total clarifications answered and current stage after each round. Explain that a batch-end is never final completion and that optional pauses/stops preserve source.
3. Reproduce misleading one-question-batch scenario in deterministic fake service tests; test multi-round review, complete/ready, queued, paused, and unknown-future states, with zero DOB/chart leaks and unchanged source data.
4. Publish a cumulative update package for the **existing** Custom GPT, with latest Oct15 source-preserving completion guide and Oct9 Action, and place files directly in owner's Downloads. Do not claim that packaging updated the private GPT.
5. Validate the simplest possible Railway finish-handoff option at the incumbent service. If the secure participant capability, consent, and full source-preserving freeze cannot be implemented/tested within current boundaries, record it as a design candidate rather than deploying an insecure portal or turning on a Venice-dependent public survey.

## Boundaries

No automatic participant outreach, no third-party private review-source inspection, no new model calls/cost, no participant review id or Bearer credential in any artifact, and no mid-review migration. Keep finished owner sessions valid and older Action clients backward compatible. Do not impose a fixed lifetime clarification cap: unanswered constructs may remain unknown; global completion requires actual independent `ready` status and participant confirmation.
