# Current state — Life Patterns — 2026-09-18

The latest owner natural-use attempt exposed an immediate runtime failure while submitting a new ordinary answer: Input routing cited an unknown historical source. That failure is repaired and deployed. Controlling receipt: state/LIFE-PATTERNS-INPUT-ROUTING-REPAIR-20260918.md.

Application head: 2549e5d15fc8fef4f9f67c4b7014e04709cc76f9. Railway deployment ed917580-1574-4cc5-8dc2-03504aa3cb44, build survey-sol-xhigh-2026-09-18.4, health HTTP 200. Hosted CI run 35396017161: SUCCESS. All model stages remain GPT-5.6 Sol/xhigh with no fallback.

## Failure and repair

The semantic input router may optionally identify earlier participant turns that were only interview-process feedback so they can be excluded from current behavioral evidence. The runtime previously treated any router-supplied historical turn ID that did not resolve to an actual prior participant turn as a fatal validation error. That advisory hygiene field therefore had authority to abort a valid current answer.

The repair keeps the evidence boundary strict while removing that brittle coupling:

- current evidence excerpts still must be exact substrings of the participant's current message;
- recognized historical process IDs still quarantine only real prior participant turns;
- unknown or assistant-role historical IDs are ignored for quarantine rather than allowed to remove evidence or abort the current answer;
- the audit record preserves only a count of ignored unknown hints, not fabricated IDs;
- answer processing, extraction, question selection, revision binding, rollback, pause and recovery semantics are otherwise unchanged.

The available uploaded recovery backup predates the failed submission. Its stored historical process IDs resolve to earlier participant turns. Therefore it does not contain the newly failed router payload and cannot establish why the model emitted an unrecognized ID. The screenshot plus exact exception path establishes the runtime failure boundary; the model-side cause remains unobserved.

## Verification

Focused dialogue regression and adjacent workflow tests passed. The actual browser consumer seam now includes a route response with a deliberately nonexistent historical process-turn ID: the current answer is retained and processed, no error is shown, the unknown hint is not added to process_turn_ids, and the runtime records one ignored hint. The complete synthetic browser suite passed 20 scenarios with zero page errors.

Ruff passed with the repository's CI rule ignoring E501 and I001, and strict mypy passed across 208 source files. Hosted CI passed on the exact integrated code head. One earlier browser attempt in this repair used a port already occupied by an unrelated fixture and was invalidated; it was rerun on an isolated ephemeral loopback port and passed. No owner session or private transcript was replayed into the service, and no new model call was required for this deterministic runtime repair.

## Next action and authority

The root owner outcome remains OPEN. The immediate runtime failure is fixed, but this is not evidence that the interview's general semantic quality now passes. The meaningful next observation is the owner's natural use of the changed candidate.

The failed browser operation was revision-bound and left the participant draft visible. After refresh, Retry saved operation should resubmit the preserved answer under the repaired runtime; no prior answers need to be re-entered. If a new failure appears, continue the authorized repair automatically in the same turn.

Preserve participant authority, original source wording, the accepted v2 evidence core, target-blind elicitation, Sol/xhigh, and the separate later owner post-freeze recovery criterion. No external recruitment, chart-aware questioning, scientific-validation claim, protected-main merge or public release was performed. The HumanDesign development pull request remains draft/open/unmerged.

There was never a completion policy. Preserve state/OWNER-CORRECTION-2026-09-02.md.
