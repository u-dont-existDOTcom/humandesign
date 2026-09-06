# Life Patterns — MI-informed interviewer implementation receipt

Date: 2026-09-06
Status: implementation receipt for draft PR #24; no deployment, merge, target-model scoring, or validation promotion.

## Inputs

This implementation follows the source-based applicability assessment in:

`docs/research/LIFE_PATTERNS_MOTIVATIONAL_INTERVIEWING_APPLICABILITY_2026-09-06.md`

and the observed Life Patterns pilot failures already documented in the repository, especially redundant questioning, unclarified material uncertainties, overreliance on exact episodes, and participant/interviewer mismatch.

The Motivational Interviewing material is adapted only for source-grounded listening, shared focus, autonomy, and deliberate neutrality. Directional change-evocation, change planning, selective reinforcement of change talk, and praise of preferred behavior are explicitly prohibited in the research interviewer.

## Runtime changes

Implemented in `src/hdmatch/api/life_patterns_interview_app.py`:

- replaced episode-first interviewer framing with pattern-first, evidence-anchored interviewing;
- added source-grounded reflective listening with an explicit prohibition on adding motives, emotions, causes, regret, or other inferred meaning;
- added a follow-up gate: before asking, the interviewer must identify the specific missing/conflicting fact and how materially different answers would change the retained account;
- material unresolved ambiguity is prioritized over collecting new coverage;
- existing answers must be reused rather than requested again;
- repeated-series reports can remain legitimate self-report without forcing a dated episode solely to satisfy an evidence label;
- exception checks are limited to logically comparable propositions rather than mechanically soliciting counterexamples;
- interaction mismatch such as "already said," "obvious," or "I don't know what you mean" is treated first as a possible interviewer error; the interviewer must check context, acknowledge, simplify once if material, or skip;
- explicit autonomy protections preserve `unknown`, `skip`, `pause`, and narrowed claims;
- explicit neutrality prohibits evoking change talk, strengthening commitment, planning change, or affirming/praising a particular behavioral pattern;
- `coverage_focus` may be `none_material` instead of inventing another question;
- interview session behavior version advanced to `life-patterns-conversation-v3`.

## Long-interview context fix

The prior runtime sent only the last 18 conversation turns to the model. This could cause earlier participant answers to fall out of model context and contribute to redundant questions.

The updated runtime now sends:

- 24 recent full conversation turns; and
- a compact participant-statement index retaining up to 80 participant turns, with each text entry capped at 1,200 characters and explicit truncation metadata.

This is a deterministic context-availability aid, not an LLM-generated summary or scientific evidence transformation.

## Participant-facing UI changes

Implemented in `src/hdmatch/api/life_patterns_interview_ui.py`:

- introduction and first prompt are pattern-first rather than demanding a consequential episode;
- textarea guidance says concise pattern descriptions are sufficient and examples are requested only when useful;
- UI tells participants the interviewer may briefly reflect its understanding and should not make them repeat supplied information;
- progress copy describes participant-approved evidence anchors rather than a story quota;
- pending AI-extracted examples are now described accurately as awaiting factual review before they count as evidence;
- removed the misleading pending-state message that a provisional extraction had already been added to the evidence map.

## Regression tests

Added:

- `tests/unit/test_life_patterns_interviewer_conduct.py`
- `tests/unit/test_life_patterns_interview_ui_conduct.py`

Tests bind the pattern-first/follow-up/neutrality/mismatch policy, older participant-statement retention, history bounds/truncation behavior, participant-facing pattern-first framing, and the pending-evidence wording.

## Verification

Implementation head before this receipt:

`ee8992c575e86a6cba599d85a1464b3cf7a178f9`

GitHub Actions CI run:

`34042063675`

Result: **success**

- pytest: **472 passed, 6 expected skips**;
- Ruff: **all checks passed**;
- mypy: **success, no issues in 151 source files**.

An earlier CI attempt failed only because a new regression test asserted an exact sentence fragment with mismatched capitalization; the test was revised to check the policy invariant case-insensitively. The runtime implementation did not need to be rolled back.

## Scientific boundary

These changes improve interviewer conduct and context retention. They do not establish interview validity, discriminative power, construct validity, coding reliability, or AstroHD performance. The completed v8/v8.1 participant record remains unchanged. No participant narratives or identifying content are stored in this public receipt.
