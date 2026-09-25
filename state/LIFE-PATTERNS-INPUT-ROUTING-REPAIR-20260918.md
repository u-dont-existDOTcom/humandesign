# Life Patterns input-routing unknown-source repair — 2026-09-18

Status: IMPLEMENTED AND DEPLOYED to the existing owner-development surface.

## Owner-observed failure

The owner submitted a new answer and the interface immediately returned Input routing cited an unknown historical source, while preserving the draft and offering Retry / reconcile / backup controls.

The currently available recovery backup predates that failed submission. It contains historical process-turn references that resolve to real earlier participant messages. It therefore cannot identify the exact new router field that failed. The exception is emitted only when the router's advisory historical_process_turn_ids contains at least one ID outside the session's known participant turns. The reason the model produced such an ID is not preserved after the rolled-back operation and is not inferred here.

## Causal defect

historical_process_turn_ids is an optional semantic hygiene suggestion: it can quarantine earlier clarification/challenge-only user turns from current elicitation. The runtime incorrectly elevated this advisory field into a fatal integrity check. An unrecognized suggestion could not safely remove evidence, but it also did not need to invalidate the current participant answer.

This was a composition defect between a fallible semantic router and deterministic evidence handling, not evidence that the participant's answer was invalid.

## Repair

The workflow now deduplicates the router's historical-process IDs and intersects them with actual prior participant turn IDs.

- Recognized IDs retain the existing quarantine behavior.
- Unknown IDs and assistant-role IDs cannot enter process_turn_ids.
- Unknown IDs no longer abort the participant's current operation.
- The private working audit records ignored_unknown_historical_process_turn_count when this happens, without retaining fabricated IDs.
- evidence_quotes remains strict: current behavioral evidence must still be exact participant-source text. No source-fidelity validation was weakened.
- Sol/xhigh model selection, inference approval, source-summary behavior, recovery, revision/idempotency and pause behavior are unchanged.

## Verification

- focused input-routing regression: PASS;
- affected workflow/dialogue tests: PASS;
- browser consumer suite: 20 PASS, zero page errors;
- added browser case injects a nonexistent historical process-turn reference and proves the current answer is processed without an error while the unknown hint is ignored;
- Ruff under the repository CI configuration: PASS;
- strict mypy: PASS, 208 source files;
- hosted CI on application head 2549e5d15fc8fef4f9f67c4b7014e04709cc76f9: run 35396017161, SUCCESS;
- Railway deployment ed917580-1574-4cc5-8dc2-03504aa3cb44: SUCCESS;
- /healthz: HTTP 200, build survey-sol-xhigh-2026-09-18.4, build commit matches the application head, model profile remains GPT-5.6 Sol/xhigh for interviewer and extraction with no automatic fallback.

The first browser attempt during development collided with an unrelated pre-existing loopback listener and therefore exercised stale fixture code; it failed a pre-existing clarification case. That run is infrastructure-invalid for product judgment. Re-running against a newly allocated isolated loopback port passed all 20 scenarios.

Test-efficiency telemetry observed 15.93 seconds of test execution over 518.78 seconds of task time at the captured checkpoint; no forced redundant-green rerun was performed.

## Outcome

This directly repairs the reported runtime failure. It does not establish that every future question or synthesis is useful. Owner-outcome advancement for conversational quality remains unmeasured on this new candidate.

The already-saved failed answer is expected to be retryable after refresh because the client retained the revision-bound operation and draft. No re-entry of earlier answers is required.
