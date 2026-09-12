# Life Patterns: book-informed methods implementation receipt

Date: 2026-09-06
Disposition: draft PR #24 only; no merge, deployment, validation promotion, or target-model execution.

## Bound implementation and verification

Baseline: `0ab5cf12f4c907274da51e75477d7b4410a81d40`.
Implementation and tests: `78d936233103318d6fdfa8f7bc8f0b79bc285a0e`.
Source review memo added at `1a14ad5e810d1926907326114c3ea205e37c4300`.
GitHub Actions run: `34054407573`; verify job: `101543515987`.
CI tested the PR merge ref `89c8e364aca2402d702f983ccdbcb06a6c9013ec`, merging the implementation head into PR #24's unchanged base `40154251534cffebaf7f2b78b48c5a97c707b629`.

Verified results from the job log:

- 506 passed, 6 skipped; 512 collected.
- Ruff: all checks passed (`ruff check src tests --ignore E501,I001`).
- mypy: no issues in 152 source files.
- The six skips are three shallow-checkout historical-commit checks and three unavailable external ephemeris-file checks, not newly skipped interview tests.
- 34 new cases: 28 helper tests and 6 integration tests.
- The 28 helper cases also passed locally. Full repository verification was performed by GitHub Actions, not claimed as a local full checkout run.

## What is implemented

`life_patterns_interview_methods.py` consolidates source-grounded interviewing guidance, exact bounded question/answer context, and a validated clarification-note contract. `life_patterns_interview_app.py` integrates the helpers into provider input, persists the fixed opener for new sessions, appends process notes to assistant turns, provides an authenticated latest-note view, and records method/prompt provenance.

The context view preserves the first 1,200 characters and a separate tail of up to 400 characters for clipped entries. It retains the actual preceding interviewer turn, original text length, full stored-text hash, offsets, and omission counts. This does not mean the full conversation fits in every model request.

Clarification dispositions are open, answered, unknown, declined, not_asked_burden, and not_material. Notes must cite existing participant turns; invalid, duplicate, assistant-only, or future references cannot pass the relevant source checks. Historical notes remain in the conversation. A latest-state view is derived without rewriting prior notes.

The log's policy is `model_reported_interview_process_not_behavioral_evidence`. The software validates structure and reference identity, not whether an issue was truly resolved. Notes do not count as episodes or alter scientific evidence labels. Participant-approved episodes remain the existing map input.

New session behavior is `life-patterns-conversation-v4`; methods policy is `life-patterns-interview-methods-v2`. Existing session version labels and original turns are not retroactively rewritten. The standalone v8/v8.1 participant records and frozen codebook are unchanged.

## Source review and non-adopted methods

See `docs/research/LIFE_PATTERNS_FULL_TEXT_METHODS_ADAPTATION_2026-09-06.md` for chapter/section locators, actual source inventory, and rationale. This was selected full-text review, not a cover-to-cover reading claim. The calendar source is the supplied 18-page 2019 chapter, not the entire handbook or the originally suggested 2009 volume.

The adaptation retains purposeful follow-ups, selective probing, generic/event-memory distinctions, participant-supplied timeline cues, and scale/index distinctions. It excludes interviewer-suggested hidden causes, directional change elicitation, compulsory cognitive-probing batteries, and an unvalidated overall personality score.

## Limits

No actual LLM interviewing session or randomized comparison was run. Mocked-provider and synthetic tests verify implementation contracts, not better listening, reduced participant time, truthful recall, semantic accuracy of notes, coding reliability, or AstroHD validity. The existing workflow is not newly made into an automatic end-to-end finish/export state machine. This patch does not add a separate participant-reviewed series-to-map pipeline or change research freeze schemas.

No source book, private extraction, participant account, identifying information, or private export was committed. No participant is asked to repeat the completed interview for this implementation.
